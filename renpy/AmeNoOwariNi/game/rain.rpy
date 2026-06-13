## リアル雨エフェクト（全画面・前景レイン）
## AI生成の背景は窓位置がまちまちなので、窓ガラスにクリップする旧方式はやめ、
## 画面全体に降る前景の雨（3層パララックス）として描く。背景に焼き込まれた窓の雨と重なって雰囲気を出す。
## タイトルだけ稲光＋雷鳴を伴う。

init python:
    import random
    import math as _math

    class Rain(renpy.Displayable):

        def __init__(self, bolt=False, density=150, **kwargs):
            super(Rain, self).__init__(**kwargs)
            self.bolt = bolt
            self.st = []
            self.last = None
            self.t = 0.0
            self.next_bolt = 5.0
            self.bolt_t = 9.0
            for _ in range(density):
                self.st.append(self._streak(True))

        def _streak(self, init):
            r = random.random()
            layer = 0 if r < .45 else (1 if r < .8 else 2)
            return {
                "layer": layer,
                "x": random.random() * 1380 - 50,
                "y": (random.random() * 720) if init else (-30 - random.random() * 120),
                "len": [16.0, 27.0, 44.0][layer] + random.random() * [12, 16, 22][layer],
                "vy": [620.0, 980.0, 1500.0][layer] * (.85 + random.random() * .3),
                "a": int([26, 42, 70][layer] + random.random() * 18),
                "w": [1, 2, 3][layer],
            }

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            if self.last is None:
                self.last = st
            dt = max(0.0, min(.05, st - self.last))
            self.last = st
            self.t += dt
            c = rv.canvas()
            wind = -45 + _math.sin(self.t * .5) * 20 + _math.sin(self.t * .17) * 28

            # 稲光（タイトルのみ）
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
                _cap = .35 if renpy.store.persistent.lowflash else .7
                bolt = min(_cap, .5 * _p(self.bolt_t) + .7 * _p(self.bolt_t - .13) + .28 * _p(self.bolt_t - .32))
                if bolt > .012:
                    c.rect((212, 224, 255, int(bolt * 120)), (0, 0, 1280, 720))

            # 全画面の雨脚（3層パララックス・突風で角度がゆらぐ）
            for s in self.st:
                vx = wind * (.4 + s["layer"] * .4)
                s["x"] += vx * dt
                s["y"] += s["vy"] * dt
                if s["x"] < -60:
                    s["x"] += 1440
                if s["x"] > 1380:
                    s["x"] -= 1440
                if s["y"] > 740:
                    s.update(self._streak(False))
                    continue
                y2 = s["y"]
                y1 = y2 - s["len"]
                x2 = s["x"]
                x1 = x2 - vx / s["vy"] * s["len"]
                a = min(150, int(s["a"] * (1 + bolt * 1.5)))
                c.line((190, 208, 242, a), (int(x1), int(y1)), (int(x2), int(y2)), s["w"])

            renpy.redraw(self, 0)
            return rv

## 各シーンの雨。背景が変わっても全画面に降るので位置調整は不要。
image rain_title = Rain(bolt=True, density=170)
image rain_shosai = Rain(density=150)
image rain_ima = Rain(density=150)
image rain_dai = Rain(density=150)
