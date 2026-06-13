## 画面とスタイル（GUIテンプレート不使用・全カスタム）

################################################################ スタイル

style default:
    font "fonts/ipaexm.ttf"
    size 26
    color "#efe9da"
    line_spacing 8

style button:
    background Frame("images/ui_btn.png", 3, 3)
    hover_background Frame("images/ui_btn_hover.png", 3, 3)
    insensitive_background Solid("#0d1118")
    padding (22, 9)
    activate_sound "audio/select.wav"

style button_text:
    size 24
    color "#e8e3d3"
    hover_color "#f6edd8"

## 下端に固定し、文章が長いときは上方向に伸びる（文字拡大時にあふれない）
style say_window is default:
    xpos 0
    yanchor 1.0
    ypos 720
    xsize 1280
    yminimum 215
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
    xsize 360
    background Frame("images/ui_choice.png", 3, 3)
    hover_background Frame("images/ui_choice_hover.png", 3, 3)

style choice_button_text is button_text:
    size 24

################################################################ 基本画面

screen say(who, what):
    window:
        style "say_window"
        vbox:
            spacing 6
            if who is not None:
                text who id "who" style "say_label"
            text what id "what" style "say_dialogue"

## 選択肢はHTML版と同じくシーン下部に出す（現場の絵と直前のセリフを隠さない）。
## 項目が多い段階Cの調べる(8項目)は2列にして画面中央を覆わないようにする。
screen choice(items):
    style_prefix "choice"
    vpgrid:
        cols (2 if len(items) > 5 else 1)
        xalign 0.5
        yanchor 1.0
        ypos 500
        spacing 8
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

screen notebook(select=False, prompt="", cancel=None):
    modal True
    zorder 100
    default sel = None
    add Solid("#000000b4")
    key "K_ESCAPE" action Return("__cancel__")
    key "mouseup_3" action Return("__cancel__")
    frame:
        align (.5, .5)
        xsize 960
        ysize 632
        padding (26, 20)
        background Solid("#11182a")
        fixed:
            textbutton (cancel or ("やめる" if select else "閉じる")):
                action Return("__cancel__")
                align (1.0, 0.0)
            vbox:
                spacing 14
                hbox:
                    spacing 18
                    text "探偵手帳" color "#d9b36a" size 28 bold True
                    if prompt:
                        text prompt color "#d98c6a" size 22 yalign 1.0
                hbox:
                    spacing 22
                    vbox:
                        spacing 7
                        xsize 380
                        for eid in ev:
                            button:
                                xfill True
                                action SetScreenVariable("sel", eid)
                                background (Frame("images/ui_item_sel.png", 3, 3) if sel == eid else Frame("images/ui_item.png", 3, 3))
                                hover_background (Frame("images/ui_item_sel.png", 3, 3) if sel == eid else Frame("images/ui_btn.png", 3, 3))
                                padding (10, 6)
                                hbox:
                                    spacing 12
                                    add ("images/icon_" + eid + ".png") xysize (40, 40)
                                    text (("▶ " if sel == eid else "") + EVDATA[eid]["name"]) size 23 yalign .5
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
    key "K_ESCAPE" action Return()
    key "mouseup_3" action Return()
    key "K_RETURN" action Return()
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
            text "― クリックで閉じる ―" size 16 color "#8a93a8" xalign .5

################################################################ 尋問

screen testimony(stxt, idx, total):
    modal True
    frame:
        style "say_window"
        padding (40, 18, 40, 84)
        vbox:
            spacing 8
            text "水原の証言　[idx]／[total]" color "#9adfae" size 22 bold True
            text stxt color "#9adfae" size 26 line_spacing 9 xsize 1190
    hbox:
        xalign .5
        ypos 658
        spacing 12
        textbutton "◀ 前へ" action Return("prev")
        textbutton "次へ ▶" action Return("next")
        textbutton "ゆさぶる（Ｚ）" action Return("press")
        textbutton "つきつける（Ｘ）" action Return("present")
        textbutton "手帳（Ｎ）" action Return("notebook")
    key "K_LEFT" action [Play("sound", "audio/select.wav"), Return("prev")]
    key "K_RIGHT" action [Play("sound", "audio/select.wav"), Return("next")]
    key "K_z" action [Play("sound", "audio/select.wav"), Return("press")]
    key "K_x" action [Play("sound", "audio/select.wav"), Return("present")]
    key "K_n" action [Play("sound", "audio/select.wav"), Return("notebook")]

screen lives_hud():
    zorder 90
    frame:
        pos (1010, 10)
        padding (14, 6)
        background Solid("#0a0e1ab4")
        text lives_str() color "#d96a6a" size 30

screen flashscr(txt, dim=False):
    zorder 200
    add Solid("#f3ecd8d2" if dim else "#f3ecd8")
    text txt align (.5, .45) size 96 color "#15182a" bold True

################################################################ タイトル／エンド

screen titlescr():
    modal True
    key "K_RETURN" action Return()
    key "K_KP_ENTER" action Return()
    add Solid("#05070c") alpha 0.34
    vbox:
        align (.5, .44)
        spacing 14
        text "― 私立探偵・灰崎の事件簿 ―" size 22 color "#9aa6bd" xalign .5 kerning 6
        text "雨の終わりに" size 66 color "#f0e8d4" xalign .5 kerning 14
        text "クリック／Enter：進む　Ctrl：スキップ　ホイール上：読み返し" size 18 color "#8a93a8" xalign .5
        text "Esc／右クリック：設定　＊プレイ時間 約10分" size 18 color "#8a93a8" xalign .5
        if persistent.cleared:
            text "※2周目：Ctrl押しっぱなしで高速スキップ" size 17 color "#d9b36a" xalign .5
        null height 10
        textbutton "調査をはじめる" action Return() xalign .5

screen endscr():
    modal True
    key "K_RETURN" action Return()
    key "K_KP_ENTER" action Return()
    add Solid("#06080f")
    vbox:
        align (.5, .44)
        spacing 20
        text "完" size 110 color "#e8e0c8" xalign .5
        text "― 雨の終わりに ―" size 24 color "#9aa6bd" xalign .5 kerning 8
        null height 18
        textbutton "もう一度はじめから" action Return() xalign .5

################################################################ 設定（Esc／右クリック）

screen settingsscr():
    tag menu
    modal True
    zorder 120
    add Solid("#000000b4")
    key "K_ESCAPE" action Return()
    key "mouseup_3" action Return()
    frame:
        align (.5, .5)
        padding (44, 32)
        background Solid("#11182a")
        vbox:
            spacing 20
            text "設定" color "#d9b36a" size 28 bold True xalign .5
            hbox:
                spacing 16
                text "ＢＧＭ音量" size 22 yalign .5
                bar value Preference("music volume") xsize 320 ysize 26 yalign .5:
                    left_bar Solid("#d9b36a")
                    right_bar Solid("#2e3a55")
                    thumb None
            hbox:
                spacing 16
                text "効果音音量" size 22 yalign .5
                bar value Preference("sound volume") xsize 320 ysize 26 yalign .5:
                    left_bar Solid("#d9b36a")
                    right_bar Solid("#2e3a55")
                    thumb None
            textbutton ("演出ひかえめ（フラッシュ・揺れ）：オン" if persistent.lowflash else "演出ひかえめ（フラッシュ・揺れ）：オフ"):
                action ToggleField(persistent, "lowflash")
                xalign .5
            null height 6
            hbox:
                spacing 22
                xalign .5
                textbutton "ゲームに戻る" action Return()
                textbutton "最初からやり直す" action Confirm("最初からやり直しますか？\n（進行は失われます）", Start())
                textbutton "終了" action Confirm("ゲームを終了しますか？", Quit(confirm=False))
            text "Ctrl：既読スキップ　ホイール上：読み返し　Alt+Enter：全画面" size 17 color "#8a93a8" xalign .5
