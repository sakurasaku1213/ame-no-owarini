## 本編：オープニング〜調査パート〜中間推理

label start:
    $ ev = []
    $ flg = []
    $ lives = 5
    $ stage = "A"
    $ loc = "shosai"
    ## 設定画面の「最初からやり直す」で尋問中から戻った場合の後始末
    hide screen lives_hud
    stop music fadeout 1.0
    scene bg title
    show rain_title as rain
    play ambient "audio/rain.wav" loop fadein 2.0
    call screen titlescr
    play sound "audio/select.wav"
    play music "audio/bgm_calm.wav" loop fadein 2.0
    jump intro

################################################################ オープニング

label intro:
    "六月。雨は、もう三日も降りつづいていた。"
    "私立探偵・灰崎修（はいざき・しゅう）。それが俺の名だ。看板に偽りはないが、あいにく客はない。"
    "事務所の電話が鳴ったのは、九時半を回った頃だった。"
    show bust kumai at bustpos
    kum "「俺だ、熊井だ。……灰崎、推理作家の東山宗一郎を知ってるな」"
    hide bust
    hai "「ベストセラー作家だろう。何度か世話になった――本にだが」"
    show bust kumai at bustpos
    kum "「その東山が死んだ。自宅の書斎で、毒をあおってな。机には遺書ときた」"
    kum "「自殺で片づきそうな話だ。……だが、どうにも引っかかる。お前の目を貸せ」"
    hide bust
    hai "「……雨の夜の呼び出しは高くつくぜ、警部殿」"
    "俺は受話器を置き、トレンチコートの襟を立てた。――長い夜になりそうだった。"
    scene bg shosai with dissolve
    show rain_shosai as rain
    "東山邸、二階の書斎。線香と、冷めた珈琲のにおい。"
    show bust kumai at bustpos
    kum "「来たな。現場はこの書斎だ。仏さんはもう運んだが、ほかはそのままにしてある」"
    hide bust
    hai "「相変わらず手回しのいいことで」"
    if not persistent.cleared:
        sysc "◆コマンドで調査を進めよう。「調べる」で現場を、「話す」で聞き込みを。困ったら「考える」。"
    jump roam

################################################################ 調査ループ

label roam:
    call check_triggers
    if stage == "TRIAL":
        jump trial
    if loc == "shosai":
        jump menu_shosai
    elif loc == "ima":
        jump menu_ima
    else:
        jump menu_dai

label menu_shosai:
    menu:
        "調べる":
            call examine_shosai
        "話す（熊井警部）":
            call talk_kumai
        "移動する" if "unlockMove" in flg:
            call move_menu
        "考える":
            call think
        "手帳を見る" if ev:
            call screen notebook()
    jump roam

label menu_ima:
    menu:
        "調べる":
            call examine_ima
        "話す":
            call talk_ima
        "移動する":
            call move_menu
        "考える":
            call think
        "手帳を見る" if ev:
            call screen notebook()
    jump roam

label menu_dai:
    menu:
        "調べる":
            call examine_dai
        "話す（熊井警部）":
            call talk_kumai
        "移動する":
            call move_menu
        "考える":
            call think
        "手帳を見る" if ev:
            call screen notebook()
    jump roam

################################################################ 移動

label move_menu:
    python:
        _dest = pick([(LOCNAME[l] + "へ", l) for l in ["shosai", "ima", "dai"] if l != loc])
    if _dest == "__cancel__":
        return
    $ loc = _dest
    $ _ln = LOCNAME[_dest]
    if _dest == "shosai":
        scene bg shosai with dissolve
        show rain_shosai as rain
    elif _dest == "ima":
        scene bg ima with dissolve
        show rain_ima as rain
    else:
        scene bg dai with dissolve
        show rain_dai as rain
    "――[_ln]――"
    return

################################################################ 書斎を調べる

label examine_shosai:
    python:
        _opts = [("机の上（封筒）" + chk("isho"), "isho")]
        if stage == "C":
            _opts.append(("机の引き出し" + chk("note"), "drawer"))
        _opts += [
            ("珈琲カップ" + chk("cup"), "cup"),
            ("万年筆と原稿用紙" + chk("pen"), "pen"),
            ("ワープロ" + chk("wapro"), "wapro"),
            (("書棚" + chk("oubo")) if stage == "C" else "書棚", "shodana"),
            ("窓" + fchk("sMado"), "mado"),
        ]
        _t = pick(_opts)
    if _t == "isho":
        call hs_isho
    elif _t == "drawer":
        call hs_drawer
    elif _t == "cup":
        call hs_cup
    elif _t == "pen":
        call hs_pen
    elif _t == "wapro":
        call hs_wapro
    elif _t == "shodana":
        call hs_shodana
    elif _t == "mado":
        call hs_mado
    return

label hs_isho:
    if "isho" in ev:
        "封筒と遺書。何度見ても、活字の遺書というやつは冷たい。"
        return
    hai "「机の上に、封筒……これが例の遺書か」"
    show bust kumai at bustpos
    kum "「ワープロで打たれて、印字されたものだ。封のされた封筒に入っていた」"
    kum "「開けたのはうちの鑑識だ。九時四十分。それまで中身は誰も見ちゃいない」"
    hide bust
    "――『我が最後の作品「雨の終わりに」を世に残し、先に逝く。誰も恨まない。東山宗一郎』"
    hai "「……題は『雨の終わりに』、か。署名まで活字とはな」"
    call get_ev("isho")
    return

label hs_cup:
    if "cup" in ev:
        "飲み残しの珈琲。毒はこの中にあった。"
        return
    hai "「飲みかけの珈琲だ。……こいつに毒が？」"
    show bust kumai at bustpos
    kum "「即効性の毒物だ。検出済みだよ。仏さんの胃からも同じものが出てる」"
    hide bust
    hai "「自分で淹れて、自分で盛ったか。あるいは――」"
    call get_ev("cup")
    return

label hs_pen:
    if "pen" in ev:
        "書きかけの原稿。最後の文字は「雨」。その先は、もう書かれることがない。"
        return
    hai "「使い込まれた万年筆だ。インクは満タン……隣に、書きかけの原稿用紙」"
    "原稿は、文の途中で途切れていた。――最後の文字は『雨』。"
    show bust kumai at bustpos
    kum "「執筆の途中で手が止まった。……そんなところだろうな」"
    hide bust
    call get_ev("pen")
    return

label hs_wapro:
    if "wapro" in ev:
        "ワープロ。遺書はこの一台で打たれた。"
        return
    hai "「ワープロが一台。電源は落ちてる」"
    show bust kumai at bustpos
    kum "「遺書はこいつで打たれたと見ていい。印字の癖が一致した」"
    hide bust
    hai "「作家の最期の言葉が、活字か。……妙に味気ない話だ」"
    call get_ev("wapro")
    return

label hs_shodana:
    if stage != "C":
        "壁一面の本。乱れはない。初版本の谷崎が、涼しい顔で並んでいる。"
        return
    if "oubo" in ev:
        "本の奥に隠されていた、古い応募原稿。――『雨の終わり』水原渉。"
        return
    hai "「……待て。本の奥に、何か挟んである」"
    "古い原稿の束だった。表紙には――『雨の終わり』　水原渉。"
    show bust kumai at bustpos
    kum "「二年前の新人賞の応募作……の、控えの写しだな。なぜこんな所に」"
    kum "「……思い出したぞ。その年の選考委員は、東山宗一郎だ」"
    hide bust
    hai "「読むまでもない、か。筋は、あの『遺作』と同じだ」"
    call get_ev("oubo")
    return

label hs_drawer:
    if "note" in ev:
        "創作ノート。改題を知っていたのは、清書を頼まれた水原だけ。"
        return
    hai "「引き出しの奥に、ノート……創作ノートか」"
    "最後の頁。昨日の日付。――『題を「雨の終わりに」と改める。水原くんに清書を頼んだ。田淵くんには、次に会うとき伝えるつもりだ』"
    hai "「……改題を知っていたのは、水原だけ、ということになるな」"
    show bust kumai at bustpos
    kum "「田淵は『雨上がりの街』としか聞いてない、と言ったな。……面白くなってきた」"
    hide bust
    call get_ev("note")
    return

label hs_mado:
    $ setf("sMado")
    "窓の鍵は、内側から掛かっている。窓の外は篠突く雨。"
    show bust kumai at bustpos
    kum "「出入りは廊下側の扉だけだ。鍵は掛かっていなかった」"
    hide bust
    return

################################################################ 居間・台所を調べる

label examine_ima:
    python:
        _t = pick([("応接の卓" + fchk("iTaku"), "taku"), ("窓" + fchk("iMado"), "mado")])
    if _t == "taku":
        $ setf("iTaku")
        "湯呑が三つ。茶は、とうに冷めきっている。誰も口をつけた様子はない。"
    elif _t == "mado":
        $ setf("iMado")
        "雨はまだ止まない。庭の灯籠が、ぼんやりと滲んで見えた。"
    return

label examine_dai:
    python:
        _t = pick([("流し（水切りカゴ）" + chk("sink"), "sink"), ("勝手口" + fchk("dKatte"), "katte"), ("食器棚" + fchk("dShokki"), "shokki")])
    if _t == "sink":
        call hs_sink
    elif _t == "katte":
        $ setf("dKatte")
        "勝手口の鍵は、内側から掛かっている。……出入りした者は、玄関を通ったことになる。"
    elif _t == "shokki":
        $ setf("dShokki")
        "客用のカップが行儀よく並んでいる。一客分、間が空いているように見えるのは――気のせいか。"
    return

label hs_sink:
    if "sink" in ev:
        "洗いたてのカップ。誰が、いつ洗った？"
        return
    hai "「水切りカゴに、洗いたてのカップが一客……」"
    show bust kumai at bustpos
    kum "「手伝いの婆さんは今日は休みだそうだ。朝から誰も洗い物はしてない――はずだがな」"
    hide bust
    hai "「誰かが先生と差し向かいで珈琲を飲んで、自分のカップだけ洗った。……そう読めなくもないな」"
    call get_ev("sink")
    return

################################################################ 聞き込み

label talk_ima:
    python:
        _p = pick([("佳代子", "kayoko"), ("田淵", "tabuchi"), ("水原", "mizuhara"), ("熊井警部", "kumai")])
    if _p == "kayoko":
        call talk_kayoko
    elif _p == "tabuchi":
        call talk_tabuchi
    elif _p == "mizuhara":
        call talk_mizuhara
    elif _p == "kumai":
        call talk_kumai
    return

label talk_kayoko:
    if stage == "C":
        show bust kayoko at bustpos
        kay "「……主人が、自殺でないのなら。いったい、誰が……」"
        hide bust
        return
    python:
        _t = pick([("発見のとき" + fchk("k1"), "a"), ("先生のこと" + fchk("k2"), "b"), ("水原のこと" + fchk("k3"), "c")])
    if _t == "a":
        $ setf("k1")
        show bust kayoko at bustpos
        kay "「九時に、お茶をお持ちして……襖を開けたら、机に、主人が伏せていて……」"
        kay "「気が動転して、悲鳴を……。水原さんが、駆けつけてくださいました」"
        hide bust
        hai "「遺書は、ご覧になりましたか」"
        show bust kayoko at bustpos
        kay "「いいえ……。遺書があったことさえ、警察の方に伺うまで、何も」"
        hide bust
    elif _t == "b":
        $ setf("k2")
        show bust kayoko at bustpos
        kay "「執筆は、いつも万年筆でした。機械は大の苦手で……」"
        kay "「ワープロは、水原さんのお仕事の道具です。主人は触りもしませんでした」"
        kay "「原稿の清書は、すべて水原さんがなさっていましたから」"
        hide bust
        hai "（機械嫌いの作家、か。……覚えておこう）"
    elif _t == "c":
        $ setf("k3")
        show bust kayoko at bustpos
        kay "「九時すぎにお戻りになって……あら、と思ったんです」"
        kay "「あの土砂降りでしたのに、ほとんど濡れていらっしゃらなくて」"
        hide bust
        hai "（……傘を差しても、肩くらいは濡れる雨だ）"
    return

label talk_tabuchi:
    if stage == "C":
        show bust tabuchi at bustpos
        tab "「し、調べ直しですか。私はもう、申し上げることは何も……」"
        hide bust
        return
    python:
        _t = pick([("あの夜のこと" + fchk("t1"), "a"), ("新作のこと" + fchk("t2"), "b")])
    if _t == "a":
        $ setf("t1")
        show bust tabuchi at bustpos
        tab "「八時に、原稿を頂きに伺いました。ですが奥様が『誰にも会いたくないそうで』と……」"
        tab "「三十分ほど居間で粘りましたが、お会いできず、諦めて帰りました」"
        tab "「まさか、それきりになるとは……」"
        hide bust
    elif _t == "b":
        $ setf("t2")
        show bust tabuchi at bustpos
        tab "「次の長編です。題は『雨上がりの街』。傑作になると、先生も……」"
        hide bust
        hai "「『雨上がりの街』？　……『雨の終わりに』じゃなく、か」"
        show bust tabuchi at bustpos
        tab "「え？　いえ、私は『雨上がりの街』としか伺っておりません。改題のお話も、何も」"
        hide bust
        hai "（遺書の題と、食い違う。……担当編集が知らない改題、ね）"
    return

label talk_mizuhara:
    if stage == "C":
        show bust mizuhara at bustpos
        miz "「……まだ何か？　僕は、早く休みたいんですが」"
        hide bust
        return
    python:
        _t = pick([("あの夜のこと" + fchk("m1"), "a"), ("先生のこと" + fchk("m2"), "b")])
    if _t == "a":
        $ setf("m1")
        show bust mizuhara at bustpos
        miz "「八時前に屋敷を出て、駅前の本屋にいました。戻ったのは九時すぎです」"
        miz "「そうしたら、奥様の悲鳴が聞こえて……あとは、ご存じの通りです」"
        hide bust
    elif _t == "b":
        $ setf("m2")
        show bust mizuhara at bustpos
        miz "「厳しい人でした。でも、行き場のなかった僕を拾ってくれた……恩人です」"
        hide bust
        hai "「あんたの仕事は？」"
        show bust mizuhara at bustpos
        miz "「資料集めと、清書です。先生の原稿は、全部僕がワープロで打ち直すんです」"
        hide bust
    return

################################################################ 考える（ヒント）

label think:
    python:
        _rest = remaining_tasks()
        if stage == "A":
            _hint = ("（まずは現場だ。……" + "、".join(_rest) + "。気になる物は全部見ておく）") if _rest else "（現場はあらかた見た。次だ）"
        elif stage == "B":
            _hint = ("（……" + "。".join(_rest) + "。それからだ）") if _rest else "（材料は揃ったか。……熊井と整理するか）"
        else:
            _hint = ("（書斎だ。" + "と、".join(_rest) + "――熊井はそう言っていた）") if _rest else "（……役者は揃った）"
    hai "[_hint]"
    return

## 熊井警部との会話（ヒントを警部の言葉で）
label talk_kumai:
    python:
        _rest = remaining_tasks()
        if stage == "A":
            _kh = ("「まずは現場だ。……" + "、".join(_rest) + "。気になる物は、全部見ておけ」") if _rest else "「現場はあらかた見たな。……家の者の話を聞きに行くか」"
        elif stage == "B":
            _kh = ("「焦るな。……" + "。".join(_rest) + "。話はそれからだ」") if _rest else "「材料は揃ったようだな。……そろそろ、整理といくか」"
        else:
            _kh = ("「" + "と、".join(_rest) + "。さっき言ったろう、見落とすなよ」") if _rest else "「……役者は揃ったな」"
    show bust kumai at bustpos
    kum "[_kh]"
    hide bust
    return

################################################################ 進行トリガー

label check_triggers:
    if stage == "A" and "isho" in ev and "cup" in ev and "pen" in ev and "wapro" in ev:
        $ stage = "B"
        $ setf("unlockMove")
        show bust kumai at bustpos
        kum "「現場はこんなものか。……家の者は居間に集めてある」"
        kum "「女房の佳代子さん、担当編集の田淵、住み込みの弟子の水原だ。話を聞いてやってくれ」"
        hide bust
        hai "「ああ。……台所も借りるぜ。猫舌なんでね、家の中が気になるんだ」"
        sysc "◆「移動する」コマンドが使えるようになった。居間と台所へ行ける。"
        return
    if stage == "B" and "sink" in ev and all(f in flg for f in ["k1", "k2", "k3", "t1", "t2", "m1", "m2"]):
        if "memo_k" not in ev:
            "俺は手帳に、佳代子と田淵の言葉を書き留めた。"
            call get_ev("memo_k")
            call get_ev("memo_t")
        call quiz
        return
    if stage == "C" and "note" in ev and "oubo" in ev:
        show bust kumai at bustpos
        kum "「……役者は揃ったな」"
        hide bust
        hai "「ああ。居間へ行こう。――水原に、訊きたいことができた」"
        $ stage = "TRIAL"
        return
    return

################################################################ 中間推理（推理クイズ）

label quiz:
    $ quiz_miss = 0
    show bust kumai at bustpos
    kum "「灰崎、そろそろ整理といこう。……署の連中は、自殺で上げる気でいる」"
    kum "「遺書はある。毒も即効性。書斎の窓は内鍵、出入りは廊下の扉だけ。家には身内しかいない」"
    kum "「だがな。――お前の手帳から一つ出せ。『自殺』と食い違うものを、だ」"
    hide bust

label quiz_pick:
    $ _eid = renpy.call_screen("notebook", select=True, prompt="「自殺」と食い違う証拠は？", cancel="考え直す")
    if _eid == "isho":
        jump quiz_isho
    elif _eid == "memo_k" or _eid == "memo_t":
        show bust kumai at bustpos
        kum "「いい線だ。証言は揃ってる。……だがな、出すべきは“その証言が刺さる物”のほうだ」"
        kum "「机の上にあったろう。佳代子さんの話と、突き合わせてみろ」"
        hide bust
        call quiz_more_hint
        jump quiz_pick
    elif _eid == "wapro":
        show bust kumai at bustpos
        kum "「惜しいな。それと『組み合わせて』初めて引っかかる物が、手帳にあるだろう」"
        hide bust
        call quiz_more_hint
        jump quiz_pick
    elif _eid == "pen":
        show bust kumai at bustpos
        kum "「万年筆か。……悪くない筋だが、まず大本命があるだろう」"
        hide bust
        call quiz_more_hint
        jump quiz_pick
    elif _eid == "__cancel__":
        show bust kumai at bustpos
        kum "「逃げるなよ、灰崎。お前の手帳の中だ」"
        hide bust
        jump quiz_pick
    else:
        show bust kumai at bustpos
        kum "「……それは別に、食い違っちゃおらんだろう」"
        hide bust
        call quiz_more_hint
        jump quiz_pick

## 誤答が続いたらヒントを濃くする
label quiz_more_hint:
    $ quiz_miss += 1
    if quiz_miss == 3:
        show bust kumai at bustpos
        kum "「……機械嫌いの男と、活字の遺書。並べてみろ。答えはお前の手帳の中だ」"
        hide bust
    return

label quiz_isho:
    show bust kumai at bustpos
    kum "「ほう、遺書ときたか。……遺書の、何が引っかかる」"
    hide bust
    menu:
        "ワープロで打たれていること":
            jump quiz_correct
        "文面が短すぎること":
            show bust kumai at bustpos
            kum "「……そこじゃない気がするな。もう一度だ」"
            hide bust
            jump quiz_isho
        "日付がないこと":
            show bust kumai at bustpos
            kum "「……そこじゃない気がするな。もう一度だ」"
            hide bust
            jump quiz_isho

label quiz_correct:
    play sound "audio/ding.wav"
    hai "「佳代子さんは言った。先生は大の機械嫌い、ワープロには触りもしない、とな」"
    hai "「執筆も手紙も万年筆の男が――人生最後の言葉だけ、活字で残すか？」"
    show bust kumai at bustpos
    kum "「……あり得んな。万年筆のインクは満タン、原稿用紙も山ほどあるときてる」"
    kum "「こいつが殺しなら、遺書は偽物。打った人間が、別にいる」"
    kum "「書斎をもう一度、隅まで洗うぞ。机の引き出しと、書棚の奥だ。来い」"
    hide bust
    "俺たちは書斎へ取って返した。"
    $ stage = "C"
    $ loc = "shosai"
    scene bg shosai with dissolve
    show rain_shosai as rain
    return
