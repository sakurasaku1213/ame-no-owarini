## 対決パート：証言の尋問〜自白〜エピローグ

init python:
    ## 証言データ。t=証言文 / press=ゆさぶる時のラベル /
    ## ok=正解の証拠ID / okl=正解時のラベル / near=惜しい証拠とそのラベル
    TRIAL = {
        "R1": {
            "intro": "r1_intro",
            "sts": [
                {"t": "「あの夜は八時前に屋敷を出て、駅前の本屋にいました。戻ったのは九時すぎです」",
                 "press": "r1s1_press", "near": {"memo_k": "r1s1_near_memok"}},
                {"t": "「戻ってすぐ、奥様の悲鳴が聞こえました。それで二階の書斎へ駆けつけたんです」",
                 "press": "r1s2_press"},
                {"t": "「書斎の入口から見えました。机に伏せた先生と……ワープロ打ちの、遺書が」",
                 "press": "r1s3_press", "ok": "isho", "okl": "r1_ok",
                 "near": {"wapro": "r1s3_near_wapro"}},
                {"t": "「でも怖くて、書斎には一歩も入れませんでした。あとは奥様のそばで、警察を待っただけです」",
                 "press": "r1s4_press", "near": {"sink": "r1s4_near_sink", "cup": "r1s4_near_cup"}},
            ]},
        "R2": {
            "intro": "r2_intro",
            "sts": [
                {"t": "「遺書のことは、あとで廊下で、奥様から聞いたんです。だから知っていた。それだけだ」",
                 "press": "r2s1_press", "ok": "memo_k", "okl": "r2_ok",
                 "near": {"isho": "r2s1_near_isho", "wapro": "r2s1_near_wapro", "memo_t": "r2s1_near_memot"}},
                {"t": "「動転してたんですよ。あの晩のことは、細かいことまで覚えちゃいない」",
                 "press": "r2s2_press"},
                {"t": "「……とにかく！　僕はそれ以上、何も知りません」",
                 "press": "r2s3_press"},
            ]},
        "R3": {
            "intro": "r3_intro",
            "sts": [
                {"t": "「遺書の中身くらい、想像はつく。僕は先生の文章を、誰より読んできたんだ」",
                 "press": "r3s1_press"},
                {"t": "「だいたい、僕には先生を殺す理由がない！　拾ってもらった恩はあっても、恨みなんて――」",
                 "press": "r3s2_press", "ok": "oubo", "okl": "r3_ok",
                 "near": {"note": "r3s2_near_note"}},
            ]},
    }

################################################################ 尋問エンジン

label trial:
    play music "audio/bgm_tense.wav" loop
    scene bg ima with dissolve
    show rain_ima as rain
    $ lives = 5
    show screen lives_hud
    "居間の空気が、張りつめた。"
    show bust kumai at bustpos
    kum "「水原渉さん。手間だが、あの夜のことをもう一度聞かせてくれ」"
    show bust mizuhara at bustpos
    miz "「……何度でも。でも、まるで尋問ですね」"
    hide bust
    hai "（さあ、始めようか。――嘘は必ず、どこかで軋む）"
    sysc "◆証言を読み、怪しければ「ゆさぶる」。矛盾を見つけたら、その証言に「証拠をつきつける」。"
    sysc "◆見当違いの証拠はライフ（◆）が減る。ゼロになっても、この尋問の最初からやり直せる。"
    sysc "◆キー操作：←→で証言移動、Ｚでゆさぶる、Ｘでつきつける、Ｎで手帳。"
    $ renpy.block_rollback()
    $ cur_round = "R1"
    call run_round
    $ cur_round = "R2"
    call run_round
    $ cur_round = "R3"
    call run_round
    hide screen lives_hud
    jump confession

label run_round:
    call expression TRIAL[cur_round]["intro"]
    $ st_idx = 0

label round_loop:
    $ _rd = TRIAL[cur_round]
    $ _st = _rd["sts"][st_idx]
    show bust mizuhara at bustpos
    $ _act = renpy.call_screen("testimony", stxt=_st["t"], idx=st_idx + 1, total=len(_rd["sts"]))
    if _act == "prev":
        $ st_idx = (st_idx - 1) % len(_rd["sts"])
        jump round_loop
    elif _act == "next":
        $ st_idx = (st_idx + 1) % len(_rd["sts"])
        jump round_loop
    elif _act == "notebook":
        call screen notebook()
        jump round_loop
    elif _act == "press":
        call do_flash("待った！", True)
        call expression _st["press"]
        jump round_loop
    ## 証拠をつきつける
    $ _eid = renpy.call_screen("notebook", select=True, prompt="どの証拠をつきつける？")
    if _eid == "__cancel__":
        jump round_loop
    $ _st = TRIAL[cur_round]["sts"][st_idx]
    if _st.get("ok") == _eid:
        call do_flash("そこだ！")
        call expression _st["okl"]
        hide bust
        return
    elif _eid in _st.get("near", {}):
        call expression _st["near"][_eid]
        jump round_loop
    else:
        call wrong_present
        if lives <= 0:
            call gameover_seq
        jump round_loop

label do_flash(txt, small=False):
    play sound "audio/slam.wav"
    $ renpy.show_screen("flashscr", txt=txt, dim=(small or persistent.lowflash))
    if not small and not persistent.lowflash:
        with hpunch
    $ renpy.pause(0.45 if small else 0.85, hard=True)
    $ renpy.hide_screen("flashscr")
    return

label wrong_present:
    $ lives -= 1
    $ renpy.block_rollback()
    play sound "audio/buzz.wav"
    if not persistent.lowflash:
        with vpunch
    show bust mizuhara at bustpos
    miz "「……それが、何か？　僕の話と、何の関係があるんです」"
    show bust kumai at bustpos
    kum "「（おい灰崎、的を外すな。次はないと思って撃て）」"
    hide bust
    return

label gameover_seq:
    play sound "audio/buzz.wav"
    show bust kumai at bustpos
    kum "「待て待て、灰崎。今のは筋が通らん。……下手な追及は冤罪のもとだ」"
    show bust mizuhara at bustpos
    miz "「……探偵さん、お疲れなんじゃないですか」"
    hide bust
    "――頭を冷やせ。証言と証拠、噛み合わない一点はどこだ。"
    sysc "◆ライフが回復した。この尋問を、最初の証言からやり直す。"
    $ lives = 5
    $ st_idx = 0
    $ renpy.block_rollback()
    return

################################################################ ラウンド1：あの夜のこと

label r1_intro:
    sysc "――水原の証言『あの夜のこと』――"
    return

label r1s1_press:
    hai "「本屋で何を買った」"
    show bust mizuhara at bustpos
    miz "「……文庫を何冊か立ち読みして、結局、何も。雨がひどくなる前に帰ろうと思って」"
    hide bust
    hai "（書名ひとつ出てこない、か。……曖昧だが、崩すにはまだ弱い）"
    return

label r1s1_near_memok:
    hai "「奥さんは言ってたぜ。九時すぎに戻ったあんたは、ろくに濡れてもいなかったとな」"
    show bust mizuhara at bustpos
    miz "「こ、小降りになった時を見はからって、走って帰ったんです」"
    hide bust
    hai "（あの土砂降りで、か。……だが言い逃れられた。これだけじゃ詰め切れん）"
    return

label r1s2_press:
    show bust mizuhara at bustpos
    miz "「玄関で靴を脱いでいる時でした。心臓が、止まるかと思った」"
    hide bust
    hai "（……ここは淀みなく喋るな）"
    return

label r1s3_press:
    hai "「確かに見たんだな？　入口から」"
    show bust mizuhara at bustpos
    miz "「ええ、はっきりと。……忘れもしませんよ」"
    hide bust
    hai "（はっきりと、ね。……今の言葉、覚えておくぜ）"
    return

label r1s3_near_wapro:
    show bust mizuhara at bustpos
    miz "「ええ、先生がワープロで遺書を……。それが、何か？」"
    hide bust
    hai "（こいつ自身が毎日使う機械だ。『打てた』というだけじゃ縛れない……）"
    hai "（そうじゃない。遺書そのものに――『見えたはずのないもの』があるはずだ）"
    return

label r1s4_press:
    show bust mizuhara at bustpos
    miz "「情けない話ですけどね。……死体を見るのは、初めてだったから」"
    hide bust
    return

label r1s4_near_sink:
    hai "「台所に洗いたてのカップが一客あった。先生と誰かが、差し向かいで珈琲を飲んだんじゃないのか」"
    show bust mizuhara at bustpos
    miz "「……家政婦さんでしょう」"
    show bust kumai at bustpos
    kum "「今日は休みだ」"
    show bust mizuhara at bustpos
    miz "「なら、奥様では？　僕じゃありませんよ」"
    hide bust
    hai "（はぐらかされた。……外堀じゃない、本丸を突くべきだ）"
    return

label r1s4_near_cup:
    hai "「毒は、机のこのカップから出た」"
    show bust mizuhara at bustpos
    miz "「……先生がご自分で口にされたものでしょう。僕が書斎に入っていない以上、関係のない話だ」"
    hide bust
    hai "（毒の出どころは確かだ。だが“誰が入れたか”までは語らない……。こいつの『見た』という言葉のほうが怪しい）"
    return

label r1_ok:
    hai "「『ワープロ打ちの遺書が見えた』――確かにそう言ったな、水原さん」"
    hai "「だがこの遺書は、封のされた封筒の中にあった。開けたのは警察の鑑識、九時四十分だ」"
    show bust kumai at bustpos
    kum "「発見のとき、机にあったのは『封筒』だけだ。中身がワープロ打ちだと、入口から透けて見えたのか？」"
    show bust mizuhara at bustpos
    miz "「あ……」"
    hide bust
    hai "「答えてもらおうか。――なぜあんたは、遺書がワープロで打たれていたことを知ってる？」"
    return

################################################################ ラウンド2：遺書について

label r2_intro:
    show bust mizuhara at bustpos
    miz "「ち、違う……違うんだ。聞いてください」"
    hide bust
    sysc "――水原の証言『遺書について』――"
    return

label r2s1_press:
    hai "「いつ、どこで聞いた」"
    show bust mizuhara at bustpos
    miz "「だから、警察が来る前です。廊下で、奥様が、その……遺書がどうとか……」"
    hide bust
    hai "（……言葉が濁ったな）"
    return

label r2s1_near_isho:
    hai "（遺書そのものをもう一度突きつけても、堂々巡りだ）"
    hai "（『奥様から聞いた』という言い訳――それを直接潰す“証言”があるはずだ）"
    return

label r2s1_near_wapro:
    show bust mizuhara at bustpos
    miz "「それで遺書が打たれたんでしょう？　僕は毎日使ってる。……だから、何です？」"
    hide bust
    hai "（道具は語らない、か。……“誰から聞いたのか”という嘘そのものを、証言で潰すべきだ）"
    return

label r2s1_near_memot:
    hai "「田淵もまだ、遺書のことは何ひとつ知らされていなかった」"
    show bust mizuhara at bustpos
    miz "「な、なら、なおさら奥様から聞いたんですよ」"
    hide bust
    hai "（外堀は埋まった。残るは“奥様から”の一点……それを直接潰す証言だ）"
    return

label r2s2_press:
    show bust mizuhara at bustpos
    miz "「あなただって、恩人の死体を見れば分かりますよ」"
    hide bust
    hai "（さっきは『はっきり見た、忘れもしない』と言ったくせにな）"
    return

label r2s3_press:
    show bust mizuhara at bustpos
    miz "「……っ。早く、終わりにしてください」"
    hide bust
    return

label r2_ok:
    hai "「奥さんの証言だ。――『遺書のことは、警察に言われるまで、存在すら知らなかった』」"
    show bust mizuhara at bustpos
    miz "「そ、そんな……じゃあ、刑事の誰かから……」"
    show bust kumai at bustpos
    kum "「言っておくがな。遺書の存在は、まだ公表しとらん。家の者にも、報道にもだ」"
    kum "「中身がワープロ打ちだと知り得たのは――鑑識と、わしと、灰崎と。あとは『書いた人間』だけだ」"
    show bust mizuhara at bustpos
    miz "「ぼ、僕じゃない……僕じゃ……」"
    hide bust
    return

################################################################ ラウンド3：動機

label r3_intro:
    show bust mizuhara at bustpos
    miz "「……はっ、ははっ。……知ってたら、何だって言うんですか」"
    hide bust
    sysc "――水原の証言『動機』――"
    return

label r3s1_press:
    hai "「想像で『ワープロ打ち』まで当てたのか。大した想像力だ。――作家になれるぜ」"
    show bust mizuhara at bustpos
    miz "「…………っ」"
    hide bust
    hai "（今の一言、妙に効いたな……）"
    return

label r3s2_press:
    show bust mizuhara at bustpos
    miz "「住み込みで、清書も、資料集めも……僕は先生に尽くしてきた。それの、どこに恨みが？」"
    hide bust
    return

label r3s2_near_note:
    hai "「改題後の題を知っていたのは、あんただけだ」"
    show bust mizuhara at bustpos
    miz "「だから何です？　題を知ってたら、殺人犯ですか」"
    hide bust
    hai "（題そのものじゃ弱い。……『動機』を、形にして突きつける）"
    return

label r3_ok:
    hai "「――これが、あんたの『理由』だ」"
    hai "「二年前の新人賞応募作。『雨の終わり』、水原渉」"
    hai "「読み比べたよ。東山宗一郎の『遺作』と、筋から人物まで、瓜二つだ」"
    show bust kumai at bustpos
    kum "「その年の選考委員は東山だ。落とした原稿の写しが、なぜか書棚の奥に隠してあった」"
    show bust mizuhara at bustpos
    miz "「……っ、あ……ああ……」"
    hide bust
    hai "「題まで、最後にはあんたの『雨の終わりに』へ寄せていった。……皮肉なもんだな」"
    return

################################################################ 自白

label confession:
    play music "audio/bgm_sad.wav" loop fadein 2.0
    "水原は、しばらく床を見つめていた。やがて――ぽつりと、笑った。"
    show bust mizuhara at bustpos
    miz "「……はは。……ずっと、信じてたんですよ。落選にも、意味があるって」"
    miz "「先生に拾われたのも、何かの縁だと思った。雑用も、清書も、苦じゃなかった」"
    miz "「先月、新作の清書を頼まれましてね。……一枚目で、分かりました。これは、僕の物語だって」"
    miz "「問い詰めたら、先生は笑ったんだ。――『君の習作を、私が小説にしてやったんだ。感謝したまえ』って」"
    miz "「あの夜……珈琲に毒を入れて、向かいに座って、先生が飲み干すのをずっと待ってました」"
    miz "「遺書は、僕が打ちました。先生の字は、誰にも真似できないから」"
    miz "「……当たり前だ。僕が一番、あの万年筆の字に、憧れてたんだから」"
    hide bust
    "――ふと、気づいた。窓を叩く音が、止んでいる。"
    show rain_ima as rain at tfadeout(4.0)
    stop ambient fadeout 4.0
    show bust mizuhara at bustpos
    miz "「……雨、あがったんですね」"
    miz "「先生。……僕の雨は、いつ、あがるんでしょうね」"
    show bust kumai at bustpos
    kum "「……行くぞ」"
    hide bust
    jump epilogue

################################################################ エピローグ

label epilogue:
    scene bg shosai with dissolve
    "水原渉は、静かに連行された。"
    "書斎の机には、書きかけの原稿用紙。――『雨』の一字で途切れた、東山宗一郎の最後の字。"
    show bust kumai at bustpos
    kum "「盗作の件も、含めて調べる。……あの新作は、お蔵入りだろうな」"
    hide bust
    hai "「いや――いつか出るさ。今度は、正しい名前でな」"
    "濡れた街に、月が出ていた。長い雨の季節が、終わろうとしていた。"
    $ persistent.cleared = True
    stop music fadeout 3.0
    play music "audio/bgm_calm.wav" loop fadein 3.0
    call screen endscr
    $ renpy.full_restart()
