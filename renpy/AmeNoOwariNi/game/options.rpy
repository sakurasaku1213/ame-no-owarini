## 『雨の終わりに』 基本設定

define config.name = "雨の終わりに"
define config.version = "1.0"
define config.window_title = "雨の終わりに ― 私立探偵・灰崎の事件簿 ―"
define config.save_directory = "AmeNoOwariNi-2026"

define config.screen_width = 1280
define config.screen_height = 720

## テキスト表示速度（1秒あたりの文字数。クリックで全文表示）
define config.default_text_cps = 40

define config.default_music_volume = 0.8
define config.default_sfx_volume = 0.8

## ウィンドウを閉じるときの確認
define config.quit_action = Confirm("ゲームを終了しますか？", Quit(confirm=False))

## タスクバー・タイトルバーのアイコン
define config.window_icon = "images/icon_note.png"

## Esc・右クリックで開くのは自作の簡易設定画面（音量・演出・やり直し・終了）
define _game_menu_screen = "settingsscr"

## メニュー中も直前のセリフのウィンドウを残す（黒帯化を防ぐ）。
## 既定では "menu" でも window が隠れるが、それを外して直前の一行を出したままにする。
define config.window = "auto"
define config.window_auto_hide = ["scene", "call screen", "say-centered", "say-bubble"]

## 演出ひかえめ（フラッシュ・揺れの軽減）と周回フラグ
default persistent.lowflash = False
default persistent.cleared = False

init python:
    ## 雨の環境音用チャンネルと雷鳴用チャンネル
    renpy.music.register_channel("ambient", mixer="sfx", loop=True, tight=True)
    renpy.music.register_channel("thunder", mixer="sfx", loop=False)

## タイトル画面（メインメニュー）は使わず、起動したら直接ゲームを始める
label main_menu:
    return
