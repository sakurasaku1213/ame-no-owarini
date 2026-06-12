## リアル雨エフェクト
## HTML版のCanvas実装を Ren'Py のカスタム displayable に移植したもの。
## 3層パララックスの雨脚・窓ガラスを伝う雫・サッシの跳ね返り・稲光（タイトルのみ）を描く。

init python:
    import random
    import math as _math

    _RS = 1280.0 / 760.0  # 元デザイン座標(760x300)→画面座標(1280x505)のスケール

    def _sc_rect(r):
        return [r[0] * _RS, r[1] * _RS, r[2] * _RS, r[3] * _RS]

    class Rain(renpy.Displayable):

        def __init__(self, spawn, clips, glass, sill, bolt=False, **kwargs):
            super(Rain, self).__init__(**kwargs)
            self.spawn = _sc_rect(spawn)      # 雨粒の発生範囲（窓全体）
            self.clips = [_sc_rect(c) for c in clips]  # 雨が見えてよい矩形（ガラス面）
            self.glass = [_sc_rect(g) for g in glass]  # 雫が付く面
            self.sill = sill * _RS            # 跳ね返りの高さ（窓の下枠）
            self.bolt = bolt                  # 稲光の有無
            self.st = []   # 雨脚
            self.dr = []   # ガラスの雫
            self.sp = []   # 跳ね返り
            self.last = None
            self.t = 0.0
            self.next_bolt = 5.0
            self.bolt_t = 9.0
            n = int(min(160, max(28, (spawn[2] * spawn[3]) / 700)))
            for _ in range(n):
                self.st.append(self._streak(True))
            ga = sum(g[2] * g[3] for g in glass)
            for _ in range(int(min(26, max(7, ga / 1400)))):
                self.dr.append(self._drop(True))

        def _streak(self, init):
            r = random.random()
            layer = 0 if r < .45 else (1 if r < .8 else 2)
            sp = self.spawn
            return {
                "layer": layer,
                "x": sp[0] + random.random() * sp[2],
                "y": (sp[1] + random.random() * sp[3]) if init else (sp[1] - 30 - random.random() * 100),
                "len": [17.0, 29.0, 47.0][layer] + random.random() * [13, 17, 24][layer],
                "vy": [390.0, 675.0, 1045.0][layer] * (.85 + random.random() * .3),
                "a": int([33, 51, 87][layer] + random.random() * 20),
                "w": [1, 2, 3][layer],
            }

        def _drop(self, init):
            g = random.choice(self.glass)
            return {
                "g": g,
                "x": g[0] + 3 + random.random() * (g[2] - 6),
                "y": (g[1] + random.random() * g[3]) if init else (g[1] + 2 + random.random() * 12),
                "r": 2.2 + random.random() * 3.5,
                "vy": 0.0,
                "slide": 0.0,
                "wob": random.random() * 6.28,
                "trail": [],
            }

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            if self.last is None:
                self.last = st
            dt = max(0.0, min(.05, st - self.last))
            self.last = st
            self.t += dt
            c = rv.canvas()
            wind = -37 + _math.sin(self.t * .5) * 17 + _math.sin(self.t * .17) * 24

            # 稲光
            bolt = 0.0
            if self.bolt:
                if self.t > self.next_bolt:
                    self.bolt_t = 0.0
                    self.next_bolt = self.t + 9 + random.random() * 15
                    try:
                        renpy.music.play("audio/thunder.wav", channel="thunder")
                    except Exception:
                        pass
                self.bolt_t += dt

                def _p(x):
                    return _math.exp(-x * 16) if x >= 0 else 0.0
                bolt = min(.8, .55 * _p(self.bolt_t) + .8 * _p(self.bolt_t - .13) + .3 * _p(self.bolt_t - .32))
                if bolt > .012:
                    for cl in self.clips:
                        c.rect((216, 226, 255, int(bolt * 150)),
                               (int(cl[0]), int(cl[1]), int(cl[2]), int(cl[3])))

            # 雨脚（3層パララックス・突風で角度がゆらぐ）
            sp = self.spawn
            for s in self.st:
                vx = wind * (.4 + s["layer"] * .4)
                s["x"] += vx * dt
                s["y"] += s["vy"] * dt
                if s["x"] < sp[0] - 15:
                    s["x"] += sp[2] + 30
                if s["x"] > sp[0] + sp[2] + 15:
                    s["x"] -= sp[2] + 30
                if s["y"] > sp[1] + sp[3] + 10:
                    if s["layer"] == 2 and random.random() < .4 and len(self.sp) < 26:
                        self.sp.append({"x": s["x"], "t": 0.0})
                    s.update(self._streak(False))
                    continue
                y2 = s["y"]
                y1 = y2 - s["len"]
                x2 = s["x"]
                x1 = x2 - vx / s["vy"] * s["len"]
                a = min(160, int(s["a"] * (1 + bolt * 1.5)))
                col = (190, 208, 242, a)
                for cl in self.clips:
                    if x2 < cl[0] - 2 or x2 > cl[0] + cl[2] + 2:
                        continue
                    cy1 = max(y1, cl[1])
                    cy2 = min(y2, cl[1] + cl[3])
                    if cy2 - cy1 < 2:
                        continue
                    k1 = (cy1 - y1) / s["len"]
                    k2 = (cy2 - y1) / s["len"]
                    c.line(col,
                           (int(x1 + (x2 - x1) * k1), int(cy1)),
                           (int(x1 + (x2 - x1) * k2), int(cy2)), s["w"])

            # サッシの跳ね返り
            for p in self.sp[:]:
                p["t"] += dt
                if p["t"] > .3:
                    self.sp.remove(p)
                    continue
                k = p["t"] / .3
                a = int((1 - k) * 100)
                c.circle((200, 218, 250, a), (int(p["x"] - k * 15), int(self.sill - k * 12 * (1 - k))), 1)
                c.circle((200, 218, 250, a), (int(p["x"] + k * 18), int(self.sill - k * 15 * (1 - k))), 1)

            # 窓ガラスを伝う雫（停滞と滑落・蒸発する軌跡）
            decay = _math.pow(.45, dt) if dt > 0 else 1.0
            for d in self.dr:
                if d["slide"] > 0:
                    d["vy"] = min(57, d["vy"] + 44 * dt * d["r"] / 4)
                    d["y"] += d["vy"] * dt
                    d["wob"] += dt * 7
                    d["x"] += _math.sin(d["wob"]) * .2
                    d["slide"] -= dt
                    if (not d["trail"]) or d["y"] - d["trail"][-1][1] > 3.7:
                        d["trail"].append([d["x"], d["y"], 80.0])
                        if len(d["trail"]) > 16:
                            d["trail"].pop(0)
                else:
                    d["vy"] = 0.0
                    if random.random() < dt * (.06 + d["r"] * .03):
                        d["slide"] = .4 + random.random() * 1.4
                g = d["g"]
                if d["y"] > g[1] + g[3] + 3:
                    d.update(self._drop(False))
                    continue
                for tr in d["trail"]:
                    tr[2] *= decay
                d["trail"] = [tr for tr in d["trail"] if tr[2] > 6]
                for tr in d["trail"]:
                    c.circle((205, 222, 250, int(tr[2])), (int(tr[0]), int(tr[1])), max(1, int(d["r"] * .42)))
                c.circle((208, 224, 252, 90), (int(d["x"]), int(d["y"])), max(1, int(d["r"])))
                c.circle((255, 255, 255, 130), (int(d["x"] - d["r"] * .3), int(d["y"] - d["r"] * .35)), max(1, int(d["r"] * .32)))

            renpy.redraw(self, 0)
            return rv

## シーンごとの雨。タイトルはブラインドの隙間から見える雨＋稲光。
## 屋内は窓ガラス面（桟で区切られたペイン）にだけ降る。
image rain_title = Rain(
    [140, 28, 480, 216],
    [[140, 28, 480, 4], [140, 43, 480, 8], [140, 62, 480, 8], [140, 81, 480, 8],
     [140, 100, 480, 8], [140, 119, 480, 8], [140, 138, 480, 106]],
    [[140, 150, 480, 94]], 244, bolt=True)

image rain_shosai = Rain(
    [40, 40, 170, 150],
    [[40, 40, 83, 73], [128, 40, 82, 73], [40, 118, 83, 72], [128, 118, 82, 72]],
    [[40, 40, 83, 73], [128, 40, 82, 73], [40, 118, 83, 72], [128, 118, 82, 72]], 190)

image rain_ima = Rain(
    [563, 41, 146, 128],
    [[563, 41, 71, 128], [640, 41, 69, 128]],
    [[563, 41, 71, 128], [640, 41, 69, 128]], 169)

image rain_dai = Rain(
    [595, 49, 92, 80],
    [[595, 49, 92, 80]],
    [[595, 49, 92, 80]], 129)
