## 画面とスタイル（GUIテンプレート不使用・全カスタム）

################################################################ スタイル

style default:
    font "fonts/ipaexm.ttf"
    size 26
    color "#efe9da"
    line_spacing 8

style button:
    background Solid("#141b2c")
    hover_background Solid("#1d2740")
    insensitive_background Solid("#0d1118")
    padding (22, 9)

style button_text:
    size 24
    color "#e8e3d3"
    hover_color "#f6edd8"

style say_window is default:
    xpos 0
    ypos 505
    xsize 1280
    ysize 215
    background Solid("#0a0e1a")
    padding (40, 20)

style say_label:
    size 23
    bold True

style say_dialogue:
    size 27
    line_spacing 10
    xsize 1190

style choice_button is button:
    xminimum 460
    background Solid("#0b101de6")
    hover_background Solid("#1d2740")

style choice_button_text is button_text:
    size 25

################################################################ 基本画面

screen say(who, what):
    window:
        style "say_window"
        vbox:
            spacing 6
            if who is not None:
                text who id "who" style "say_label"
            text what id "what" style "say_dialogue"

screen choice(items):
    style_prefix "choice"
    vbox:
        xalign 0.5
        yalign 0.40
        spacing 9
        for i in items:
            textbutton i.caption action i.action

screen confirm(message, yes_action, no_action):
    modal True
    zorder 300
    add Solid("#000000aa")
    frame:
        align (.5, .5)
        padding (44, 32)
        background Solid("#11182a")
        vbox:
            spacing 26
            text message xalign .5 size 26
            hbox:
                spacing 44
                xalign .5
                textbutton "はい" action yes_action
                textbutton "いいえ" action no_action

screen notify(message):
    zorder 250
    text message pos (20, 16) size 20 color "#d9b36a"
    timer 3.0 action Hide("notify")

################################################################ 探偵手帳

screen notebook(select=False, prompt=""):
    modal True
    zorder 100
    default sel = None
    add Solid("#000000b4")
    frame:
        align (.5, .5)
        xsize 960
        ysize 632
        padding (26, 20)
        background Solid("#11182a")
        vbox:
            spacing 14
            hbox:
                spacing 18
                text "探偵手帳" color "#d9b36a" size 28 bold True
                if prompt:
                    text prompt color "#d98c6a" size 22 yalign 1.0
                null width 30
                textbutton ("やめる" if select else "閉じる"):
                    action Return(None)
                    xalign 1.0
            hbox:
                spacing 22
                vbox:
                    spacing 7
                    xsize 380
                    for eid in ev:
                        button:
                            xfill True
                            action SetScreenVariable("sel", eid)
                            background (Solid("#1a2238") if sel == eid else Solid("#0d1321"))
                            hover_background Solid("#1a2238")
                            padding (10, 6)
                            hbox:
                                spacing 12
                                add ("images/icon_" + eid + ".png") xysize (40, 40)
                                text EVDATA[eid]["name"] size 23 yalign .5
                vbox:
                    spacing 12
                    xsize 500
                    if sel:
                        hbox:
                            spacing 14
                            add ("images/icon_" + sel + ".png") xysize (64, 64)
                            text EVDATA[sel]["name"] color "#d9b36a" size 27 yalign .5
                        text ev_desc(sel) size 21 line_spacing 8
                        if select:
                            null height 6
                            textbutton "これをつきつける！":
                                action Return(sel)
                                background Solid("#3a1c1c")
                                hover_background Solid("#552525")
                    else:
                        text "左の一覧から証拠を選ぶ" size 21 color "#8b94a8"

################################################################ 証拠入手カード

screen itemget(eid):
    modal True
    zorder 150
    button:
        xfill True
        yfill True
        background None
        action Return()
    frame:
        align (.5, .42)
        padding (40, 28)
        background Solid("#0a0e18f0")
        vbox:
            spacing 10
            add ("images/icon_" + eid + ".png") xysize (72, 72) xalign .5
            text ("『" + EVDATA[eid]["name"] + "』を手帳に記録した") color "#d9b36a" size 26 xalign .5
            text EVDATA[eid]["short"] size 20 color "#c9cfdd" xalign .5

################################################################ 尋問

screen testimony(stxt, idx, total):
    modal True
    frame:
        style "say_window"
        vbox:
            spacing 8
            text "水原の証言　[idx]／[total]" color "#9adfae" size 22 bold True
            text stxt color "#9adfae" size 27 line_spacing 10 xsize 1190
    hbox:
        xalign .5
        ypos 652
        spacing 12
        textbutton "◀ 前へ" action Return("prev")
        textbutton "次へ ▶" action Return("next")
        textbutton "ゆさぶる" action Return("press")
        textbutton "証拠をつきつける" action Return("present")
        textbutton "手帳" action Return("notebook")
    key "K_LEFT" action Return("prev")
    key "K_RIGHT" action Return("next")

screen lives_hud():
    zorder 90
    frame:
        pos (1010, 10)
        padding (14, 6)
        background Solid("#0a0e1ab4")
        text lives_str() color "#d96a6a" size 30

screen flashscr(txt):
    zorder 200
    add Solid("#f3ecd8")
    text txt align (.5, .45) size 96 color "#15182a" bold True

################################################################ タイトル／エンド

screen titlescr():
    modal True
    vbox:
        align (.5, .44)
        spacing 16
        text "― 私立探偵・灰崎の事件簿 ―" size 22 color "#9aa6bd" xalign .5 kerning 6
        text "雨の終わりに" size 66 color "#f0e8d4" xalign .5 kerning 14
        text "クリック／Enterで読み進める　＊プレイ時間 約10分" size 17 color "#6b7690" xalign .5
        null height 12
        textbutton "調査をはじめる" action Return() xalign .5

screen endscr():
    modal True
    add Solid("#06080f")
    vbox:
        align (.5, .44)
        spacing 20
        text "完" size 110 color "#e8e0c8" xalign .5
        text "― 雨の終わりに ―" size 24 color "#9aa6bd" xalign .5 kerning 8
        null height 18
        textbutton "もう一度はじめから" action Return() xalign .5
