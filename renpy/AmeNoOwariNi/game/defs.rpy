## 登場人物・証拠データ・画像・ヘルパー定義

define hai = Character("灰崎", color="#e8e3d3")
define kum = Character("熊井警部", color="#d9a05b")
define kay = Character("佳代子", color="#7fb6a4")
define tab = Character("田淵", color="#9aa7c7")
define miz = Character("水原", color="#b78bc9")
define sysc = Character(None, what_color="#d9b36a")
define narrator = Character(None, what_color="#b9c2d6")

## 背景（1280x505・画面上部に表示。下部215pxはメッセージウィンドウ領域）
image bg title = "images/bg_title.png"
image bg shosai = "images/bg_shosai.png"
image bg ima = "images/bg_ima.png"
image bg dai = "images/bg_dai.png"

## 人物バストアップ（タグを bust で共有しているので、同時に一人だけ表示される）
image bust kumai = "images/bust_kumai.png"
image bust kayoko = "images/bust_kayoko.png"
image bust tabuchi = "images/bust_tabuchi.png"
image bust mizuhara = "images/bust_mizuhara.png"

## バストアップの定位置（背景の下端に足を揃える）
transform bustpos:
    xalign 0.5
    yanchor 1.0
    ypos 505

## 雨のフェードアウト用（自白シーンで使う）
transform tfadeout(d=4.0):
    linear d alpha 0.0

## ゲーム状態
default ev = []           # 入手した証拠IDのリスト
default flg = []          # 進行フラグ
default lives = 5         # 尋問のライフ
default stage = "A"       # 調査段階 A → B → C → TRIAL
default loc = "shosai"    # 現在地
default cur_round = "R1"  # 尋問の現在ラウンド
default st_idx = 0        # 表示中の証言番号

init python:
    LOCNAME = {"shosai": "書斎", "ima": "居間", "dai": "台所"}

    EVDATA = {
        "isho": {
            "name": "遺書",
            "short": "ワープロで打たれ、封筒に封入されていた。",
            "desc": "ワープロで打たれた遺書。\n『我が最後の作品「雨の終わりに」を世に残し、先に逝く。誰も恨まない。――東山宗一郎』\n封のされた封筒に入っており、開封したのは警察の鑑識（九時四十分）。それまで中身は誰も見ていない。"},
        "cup": {
            "name": "珈琲カップ",
            "short": "飲み残しから即効性の毒物が検出された。",
            "desc": "書斎の机にあった珈琲カップ。飲み残しから即効性の毒物が検出された。胃の内容物からも同じ毒物が出ている。"},
        "pen": {
            "name": "万年筆と原稿用紙",
            "short": "インクは満タン。原稿は「雨」の一字で途切れていた。",
            "desc": "先生愛用の万年筆。インクは満タンで、傍らには書きかけの原稿用紙。\n最後の文字は「雨」。文の途中で、ぷつりと途切れている。"},
        "wapro": {
            "name": "ワープロ",
            "short": "書斎にあった一台。遺書はこれで打たれた。",
            "desc": "書斎のワープロ。印字の癖から、遺書はこの一台で打たれたと見られる。"},
        "sink": {
            "name": "洗われたカップ",
            "short": "台所の水切りカゴに、洗いたてのカップが一客。",
            "desc": "台所の水切りカゴにあった、洗いたてのカップ。家政婦は今日は休み。\n誰かが先生と差し向かいで珈琲を飲み、自分のカップだけ洗った――そう考えられなくもない。"},
        "note": {
            "name": "創作ノート",
            "short": "昨日の日付で、新作の改題が記されている。",
            "desc": "先生の創作ノート。最後の頁、昨日の日付。\n『題を「雨の終わりに」と改める。水原くんに清書を頼んだ。田淵くんには、次に会うとき伝えるつもりだ』"},
        "oubo": {
            "name": "古い応募原稿",
            "short": "『雨の終わり』水原渉・作。二年前の新人賞応募作。",
            "desc": "書棚の奥に隠されていた原稿の写し。表紙には『雨の終わり』水原渉――二年前の新人賞応募作。\n筋立ても人物も、東山宗一郎の「遺作」と瓜二つ。その年の選考委員は東山だった。"},
        "memo_k": {
            "name": "佳代子の証言メモ",
            "short": "機械嫌い／遺書を知らない／濡れていない水原。",
            "desc": "佳代子の証言。\n・主人は大の機械嫌いで、ワープロには触りもしない。清書はすべて水原の仕事。\n・遺書のことは、警察に言われるまで存在すら知らなかった。\n・九時すぎに戻った水原は、あの雨なのにほとんど濡れていなかった。"},
        "memo_t": {
            "name": "田淵の証言メモ",
            "short": "八時に来訪も会えず。新作の題は『雨上がりの街』としか聞いていない。",
            "desc": "編集者・田淵の証言。\n・八時に原稿を受け取りに来たが、先生には会えず、三十分待って帰った。\n・新作の題は『雨上がりの街』としか聞いていない。改題の話は知らない。"},
    }

    def ev_desc(eid):
        """証拠の説明文。聞き込みの進行で内容が増えるものはここで合成する。"""
        d = EVDATA[eid]["desc"]
        if eid == "wapro" and "k2" in flg:
            d += "\n先生は大の機械嫌いで、このワープロに触ることはなかった（佳代子の証言）。清書はすべて水原の仕事。"
        return d

    def chk(eid):
        return "　✓" if eid in ev else ""

    def fchk(f):
        return "✓ " if f in flg else ""

    def setf(f):
        if f not in flg:
            flg.append(f)

    def lives_str():
        return "◆" * lives + "◇" * max(0, 5 - lives)

    def pick(opts):
        """動的な選択メニュー（「やめる」付き）。値を返す。"""
        return renpy.display_menu(list(opts) + [("やめる", None)])

## 証拠入手の共通処理
label get_ev(eid):
    if eid in ev:
        return
    $ ev.append(eid)
    play sound "audio/ding.wav"
    call screen itemget(eid)
    return
