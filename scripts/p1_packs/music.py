# -*- coding: utf-8 -*-
"""Music Freestyle packs."""


def register(_p):
    _p(
        "Did you learn to play an instrument as a child?",
        "school_choir_songs",
        logic="先明确是否学过乐器，再举例音乐课合唱/唱歌，补频率与校园回忆感受。",
        kitHint="课堂歌曲素材：童年挂合唱与儿歌，不硬说成钢琴等乐器。",
        words={
            "正面回答": ["Not really", "No instrument", "We sang instead"],
            "来源或举例": ["music class", "children's songs", "classroom singing"],
            "频次": ["every week in primary school", "before school festivals"],
            "感受": ["warm", "enjoyable", "made school lighter"],
        },
        sample=(
            "Not really — I didn't learn a real instrument like the piano. "
            "In music class we mostly sang simple children's songs with the whole class, "
            "and sometimes practised a festival song together. "
            "That was every week when I was in primary school. "
            "It felt warm and made school days a bit lighter."
        ),
        sampleZh=(
            "不算学过——我没学钢琴那种正式乐器。"
            "音乐课主要是全班一起唱简单的儿歌，有时还会练节日歌曲。"
            "上小学时大概每周都有。"
            "感觉很温馨，也让上学轻松一点。"
        ),
    )
    _p(
        "Did you learn to play an instrument as a child?",
        "wireless_earbuds_music",
        logic="先答童年没学乐器，再转到爱听歌的习惯来源，补听得多少与放松感受。",
        kitHint="耳机听歌套装：乐器题答「听」不答「戴」，童年以听歌习惯带入。",
        words={
            "正面回答": ["No, I didn't", "Not an instrument", "I listened more"],
            "来源或举例": ["pop songs on the radio", "my parents' phone", "simple playlists"],
            "频次": ["quite often after school", "on weekends at home"],
            "感受": ["relaxing", "enjoyable", "easy way to unwind"],
        },
        sample=(
            "No, I didn't learn to play an instrument as a child. "
            "What I did enjoy was listening — my parents often played pop songs at home, "
            "and I started building simple playlists on my phone later. "
            "I listened quite often after school and at weekends. "
            "It was an easy, relaxing habit for me."
        ),
        sampleZh=(
            "没有，童年没学过乐器。"
            "但我喜欢听——家里常放流行歌，后来我也在手机上做简单歌单。"
            "放学后和周末听得挺多。"
            "对我来说是轻松又放松的习惯。"
        ),
    )
    _p(
        "Did you learn to play an instrument as a child?",
        "focus_wired_headphones",
        logic="先否定学乐器，再举例后来用音乐辅助学习，补听轻音乐的频率与专注感受。",
        kitHint="有线耳机偏学习：童年仍先扣「乐器」，再 lightly 连到听音乐习惯。",
        words={
            "正面回答": ["No", "Never seriously", "Listening came first"],
            "来源或举例": ["soft instrumental music", "study playlists", "calm tracks"],
            "频次": ["more in high school", "when I needed to focus"],
            "感受": ["calming", "helpful", "not stressful"],
        },
        sample=(
            "No, I never learned an instrument properly as a child. "
            "I got into music more in high school, especially soft instrumental tracks when I studied. "
            "I didn't use headphones every day back then, but I liked calm playlists. "
            "That became more regular when exams got harder. "
            "It felt calming rather than another skill to master."
        ),
        sampleZh=(
            "没有，童年没正经学过乐器。"
            "上高中后更常接触音乐，复习时会听轻柔的纯音乐。"
            "小时候不是天天戴耳机，但喜欢安静的歌单。"
            "考试变难后听得更有规律。"
            "让我觉得平静，而不是又多一门要练的技能。"
        ),
    )
    _p(
        "Do you listen to music while doing other things?",
        "wireless_earbuds_music",
        logic="先正面答是否边做边听，再举例地铁/自习场景与耳机用途，补频率与减压感受。",
        kitHint="音乐为主：耳机只说明「怎么听」，不写成只聊耳塞。",
        words={
            "正面回答": ["Yes, often", "Quite a lot", "Especially on the go"],
            "来源或举例": ["pop and light rock", "subway commutes", "wireless earbuds"],
            "频次": ["every weekday on the subway", "sometimes while tidying my room"],
            "感受": ["helps me relieve stress", "blocks noise", "keeps me in a good mood"],
        },
        sample=(
            "Yes, quite often. I usually listen to pop or light rock, "
            "and I wear wireless earbuds on the subway so the noise doesn't bother me. "
            "I do this almost every weekday, and sometimes when I'm tidying my room. "
            "It helps me relieve stress and stay in a calmer mood."
        ),
        sampleZh=(
            "挺常的。我一般听流行或轻摇滚，"
            "地铁上会戴无线耳机，免得被噪音烦到。"
            "工作日几乎都会，收拾房间时有时也会。"
            "能减压，心情也更平稳。"
        ),
    )
    _p(
        "Do you listen to music while doing other things?",
        "school_choir_songs",
        logic="先答会或不会边做边听，再落到哼课堂老歌/轻唱，补何时与轻松感受。",
        kitHint="课堂歌曲：边做事时可能轻声哼唱，仍算「听音乐」情境。",
        words={
            "正面回答": ["Sometimes", "Yes, quietly", "When the task is easy"],
            "来源或举例": ["old classroom songs", "simple children's songs", "humming softly"],
            "频次": ["while doing housework", "on relaxed evenings"],
            "感受": ["light", "nostalgic", "puts me in a good mood"],
        },
        sample=(
            "Sometimes, yes. When I'm doing something easy like housework, "
            "I hum old classroom songs I learned as a kid — simple children's songs, nothing fancy. "
            "I don't do it every day, but on relaxed evenings it's quite common. "
            "It feels light and nostalgic, and it puts me in a good mood."
        ),
        sampleZh=(
            "有时候会的。做家务这种轻松活时，"
            "我会轻轻哼小时候课堂学过的儿歌，不复杂。"
            "不是天天，但悠闲的晚上挺常见。"
            "很轻松，也有点怀念，心情会好起来。"
        ),
    )
    _p(
        "Do you listen to music while doing other things?",
        "focus_wired_headphones",
        logic="先答复习时会不会边听边做，再说明图书馆戴有线耳机听纯音乐，补频率与专注影响。",
        kitHint="学习场景：音乐类型与专注为主，耳机是听的方式。",
        words={
            "正面回答": ["Yes, while studying", "Only soft music", "Not with lyrics always"],
            "来源或举例": ["instrumental playlists", "wired headphones in the library", "low-volume tracks"],
            "频次": ["most weekdays in the library", "on long reading nights"],
            "感受": ["helps me focus", "blocks chatter", "less distracting than silence"],
        },
        sample=(
            "Yes, but mainly when I'm studying. I play soft instrumental music, "
            "and in the library I use wired headphones so I don't disturb anyone. "
            "I do this most weekdays when I have long reading, and on heavy assignment nights. "
            "It blocks chatter and helps me focus without feeling too lonely."
        ),
        sampleZh=(
            "会，但多半是学习时。我会放轻柔的纯音乐，"
            "图书馆里用有线耳机，不打扰别人。"
            "工作日长时间阅读时常听，作业多的晚上也会。"
            "能挡住杂音，更容易专注，又不会像完全安静那么闷。"
        ),
    )
    _p(
        "What kind of music do you like?",
        "wireless_earbuds_music",
        logic="先点明喜欢的曲风，再说明为何及何时听，补频率与心情感受。",
        kitHint="曲风与通勤听歌习惯一体，耳机仅作收听方式。",
        words={
            "正面回答": ["Pop and light rock", "Happy songs", "Easy to listen to"],
            "原因或时间": ["since I started university", "on noisy subway rides"],
            "频次": ["almost every day", "on commutes and before bed"],
            "感受": ["helps me chill out", "uplifting", "familiar"],
        },
        sample=(
            "I like pop and light rock — nothing too heavy, mostly easy songs I can sing along to. "
            "I got into this more after I started university and took the subway every day. "
            "I listen almost daily, especially on commutes and sometimes before bed. "
            "It helps me chill out and feel a bit more upbeat."
        ),
        sampleZh=(
            "我喜欢流行和轻摇滚——别太重，多是能跟唱的歌。"
            "上大学天天坐地铁后更爱听这些。"
            "几乎每天都听，通勤时多，睡前有时也会。"
            "能放松，也让人精神一点。"
        ),
    )
    _p(
        "What kind of music do you like?",
        "school_choir_songs",
        logic="先答喜欢的歌类型（儿歌/合唱），再连到音乐课经历，补何时唱与温暖感受。",
        kitHint="课堂歌曲决定「喜欢简单旋律、合唱感」的回答角度。",
        words={
            "正面回答": ["Simple melodies", "Children's songs", "School-style songs"],
            "原因或时间": ["from music lessons as a child", "when we sang together"],
            "频次": ["still sometimes at home", "when I'm in a nostalgic mood"],
            "感受": ["warm", "easy to remember", "makes me smile"],
        },
        sample=(
            "I like simple melodies — children's songs and those easy classroom songs we learnt at school. "
            "I picked that up in music class when everyone sang together, so the tunes stuck in my head. "
            "I still play them sometimes at home when I'm feeling nostalgic. "
            "They feel warm and always make me smile a little."
        ),
        sampleZh=(
            "我喜欢简单的旋律——儿歌和学校里学的那些好唱的歌。"
            "音乐课大家一齐唱，旋律就刻在脑子里了。"
            "想怀旧时在家偶尔还会放。"
            "很温馨，总让我有点想笑。"
        ),
    )
    _p(
        "What kind of music do you like?",
        "focus_wired_headphones",
        logic="先答偏好纯音乐/轻器乐，再说明学习时需要，补听的时间和专注感受。",
        kitHint="专注套装：喜欢「不抢注意力的音乐」，不是只谈耳机。",
        words={
            "正面回答": ["Soft instrumentals", "Calm piano or guitar", "Little or no lyrics"],
            "原因或时间": ["when I need to focus in the library", "after I switched to wired headphones"],
            "频次": ["most study sessions", "especially before exams"],
            "感受": ["helps me focus", "calming", "not distracting"],
        },
        sample=(
            "I like soft instrumentals — calm piano or guitar, usually without loud lyrics. "
            "I started preferring that when I studied in the library with wired headphones. "
            "I listen during most study sessions, especially before exams. "
            "It keeps me focused and feels calming, not distracting."
        ),
        sampleZh=(
            "我喜欢轻柔的纯音乐——钢琴或吉他，歌词不吵的那种。"
            "在图书馆戴有线耳机学习后就更偏这种。"
            "大部分学习时段都会听，考前尤其多。"
            "能专注，也平静，不太分心。"
        ),
    )
    _p(
        "When do you usually listen to music?",
        "wireless_earbuds_music",
        logic="先答通常何时听，再说明地铁等原因与行为，补频率与减压影响。",
        kitHint="行为习惯四步：时间线扣通勤听歌，耳机是细节。",
        words={
            "正面回答": ["On my commute", "After class", "When I need a break"],
            "原因": ["the subway is noisy", "music relaxes my mind"],
            "时间线+行为描述": ["put on earbuds and play a playlist", "listen on the way to campus"],
            "影响": ["blocks noise", "helps me review words calmly", "arrive in a better mood"],
        },
        sample=(
            "I usually listen on my commute, especially on the subway to campus. "
            "The carriage is noisy, so music relaxes my mind and blocks the sound. "
            "I put on my earbuds, open a playlist, and listen the whole way. "
            "It helps me review vocabulary calmly and I arrive in a better mood."
        ),
        sampleZh=(
            "一般在通勤时听，尤其是去学校的地铁上。"
            "车厢很吵，音乐能让我放松、盖住噪音。"
            "我会戴上耳机打开歌单，一路听完。"
            "能平静背单词，到站心情也好些。"
        ),
    )
    _p(
        "When do you usually listen to music?",
        "school_choir_songs",
        logic="先答何时会听/哼唱，再连课堂歌习惯，补频率与轻松影响。",
        kitHint="唱歌课素材：听的时间点可落在回忆性播放或轻哼。",
        words={
            "正面回答": ["In the evening", "When I'm alone", "On quiet weekends"],
            "原因": ["old school songs cheer me up", "singing along feels easy"],
            "时间线+行为描述": ["play classroom songs softly", "hum while cooking or showering"],
            "影响": ["lifts my mood", "brings back school memories", "helps me unwind"],
        },
        sample=(
            "I usually listen in the evening or on quiet weekends when I'm at home alone. "
            "Old classroom songs cheer me up, so I play them softly or hum while I'm cooking. "
            "It's not strict — maybe a few times a week when I feel like it. "
            "It lifts my mood and helps me unwind after a long day."
        ),
        sampleZh=(
            "通常是晚上或独自在家、安静的周末。"
            "老的课堂歌能让我开心，做饭时会轻轻放或哼两句。"
            "不算固定，一周大概几次，看心情。"
            "能提气，忙完一天也容易放松。"
        ),
    )
    _p(
        "When do you usually listen to music?",
        "focus_wired_headphones",
        logic="先答图书馆/复习时段，再说明戴耳机听纯音乐，补频率与专注影响。",
        kitHint="专注学习时段为主，音乐类型服务专注而非取代题干。",
        words={
            "正面回答": ["In the library", "During revision", "At night before deadlines"],
            "原因": ["chatter distracts me", "instrumental tracks keep a steady rhythm"],
            "时间线+行为描述": ["plug in wired headphones", "play a low-volume playlist"],
            "影响": ["finish reading faster", "stay on task", "feel less stressed"],
        },
        sample=(
            "I usually listen when I'm in the library or revising at night before deadlines. "
            "Background chatter distracts me, so instrumental tracks give me a steady rhythm. "
            "I plug in my wired headphones and keep the volume low on a short playlist. "
            "I stay on task, finish reading faster, and feel less stressed."
        ),
        sampleZh=(
            "一般在图书馆或赶 deadline 前的晚上复习时听。"
            "周围说话会分心，纯音乐能让我节奏稳一点。"
            "插上有线耳机，歌单音量开低。"
            "更能坚持做题，阅读也快些，没那么焦虑。"
        ),
    )
    _p(
        "How do you usually discover new music?",
        "wireless_earbuds_music",
        logic="先答发现新歌的渠道，再举例 app/朋友推荐，补频率与尝鲜感受。",
        kitHint="discovery 走流媒体与社交推荐，耳机只在最后一步收听时出现。",
        words={
            "正面回答": ["Through apps", "Friends' shares", "Daily mixes"],
            "原因": ["algorithms know my taste", "classmates send links"],
            "时间线+行为描述": ["scroll recommended lists on the subway", "save tracks to a playlist"],
            "影响": ["fresh songs without much effort", "keeps commutes interesting"],
        },
        sample=(
            "I usually discover new music through streaming apps and friends' shares. "
            "The daily mix knows I like pop, and classmates sometimes send me links on chat apps. "
            "On the subway I scroll recommended lists and save anything I like to a playlist. "
            "It keeps my commutes interesting without much effort."
        ),
        sampleZh=(
            "多半靠流媒体和朋友分享。"
            "每日推荐知道我爱流行，同学也常在微信发链接。"
            "地铁上我会刷推荐，喜欢的就加进歌单。"
            "通勤不那么闷，也不用花很大力气找新歌。"
        ),
    )
    _p(
        "How do you usually discover new music?",
        "school_choir_songs",
        logic="先答如何接触新歌（活动/课堂/同学），再举例节日合唱新歌，补频率与参与感受。",
        kitHint="发现途径可来自学校活动与合唱排练，不是乐器课。",
        words={
            "正面回答": ["At school events", "From classmates", "Music class sometimes"],
            "原因": ["festival rehearsals need new songs", "friends sing trending tunes"],
            "时间线+行为描述": ["learn a song in music class", "search the full version online later"],
            "影响": ["easy to join in", "connects me with old school memories"],
        },
        sample=(
            "I often discover songs through school events or what classmates sing — "
            "like when we rehearsed a new festival song in music class. "
            "I'd learn the chorus there, then search the full version online later. "
            "That still happens occasionally when friends share something catchy. "
            "It feels easy to join in and reminds me of school."
        ),
        sampleZh=(
            "我常在学校活动或同学唱的歌里接触到新歌——"
            "比如音乐课排练节日歌曲。"
            "先在课上学会副歌，回家再搜完整版。"
            "现在偶尔朋友分享琅琅上口的歌也会听。"
            "容易跟唱，也勾起上学时的记忆。"
        ),
    )
    _p(
        "How do you usually discover new music?",
        "focus_wired_headphones",
        logic="先答发现渠道（学习向歌单/视频），再说明筛选纯音乐习惯，补频率与实用影响。",
        kitHint="偏 study playlist 与 instrumental 频道，发现的是「适合学习的音乐」。",
        words={
            "正面回答": ["Study playlists online", "Instrumental channels", "Curated lists"],
            "原因": ["I need focus-friendly tracks", "lyrics pull my attention away"],
            "时间线+行为描述": ["browse focus playlists before the library", "test tracks while reading"],
            "影响": ["builds a reliable study list", "saves time before exams"],
        },
        sample=(
            "I usually discover new music through online study playlists and instrumental channels. "
            "I need focus-friendly tracks, so I avoid songs with loud lyrics. "
            "Before a library session I browse a few lists and test tracks while reading a page. "
            "That builds a reliable playlist and saves time when exams get busy."
        ),
        sampleZh=(
            "我多半在网上找学习歌单和纯音乐频道。"
            "需要不抢注意力的曲子，歌词太吵的不行。"
            "去图书馆前会浏览几个列表，边读一页边试听。"
            "慢慢攒出靠谱歌单，考前也省时间。"
        ),
    )
    _p(
        "How has your taste in music changed over the years?",
        "wireless_earbuds_music",
        logic="对比过去与现在的曲风，分别说明特点，再谈个人更偏哪段与感受。",
        kitHint="对比类：童年简单流行 → 大学通勤重节奏一点的 pop，耳机只是后来习惯。",
        words={
            "正面回答": ["It has changed", "More pop now", "Still light music"],
            "选项1的特点与作用": ["as a child: simple children's songs and radio hits", "easy and familiar"],
            "选项2的特点与作用": ["now: pop and light rock on daily commutes", "blocks noise and lifts energy"],
            "个人感受": ["I still avoid heavy metal", "current taste fits my lifestyle"],
        },
        sample=(
            "Yes, it has changed quite a bit. As a child I only heard simple children's songs "
            "and whatever was on the radio at home — easy and familiar. "
            "Now on daily commutes I go for pop and light rock with my earbuds, "
            "because it blocks noise and gives me more energy. "
            "I still avoid really heavy music, but my current taste fits my lifestyle better."
        ),
        sampleZh=(
            "变了不少。小时候只是儿歌和家里收音机上的歌，简单又熟。"
            "现在每天通勤会听流行、轻摇滚，用耳机挡噪音、提点精神。"
            "还是很不爱特别重的金属，但现在的口味更合生活节奏。"
        ),
    )
    _p(
        "How has your taste in music changed over the years?",
        "school_choir_songs",
        logic="对比童年合唱曲风与长大后自选歌，说明各自作用，再谈怀念与现状感受。",
        kitHint="同一素材：从全班儿歌过渡到自己喜欢但仍爱简单旋律。",
        words={
            "正面回答": ["Yes, partly", "From choir songs to more variety", "Still simple tunes"],
            "选项1的特点与作用": ["childhood: classroom and festival songs", "taught me to sing with others"],
            "选项2的特点与作用": ["now: wider genres but still catchy songs", "I choose what matches my mood"],
            "个人感受": ["nostalgic about school songs", "more freedom now"],
        },
        sample=(
            "Yes, partly. When I was a child my taste was basically classroom and festival songs — "
            "simple tunes everyone could sing, which taught me to join in with others. "
            "Now I listen to a wider range, but I still pick catchy songs that match my mood. "
            "I'm nostalgic about those school songs, yet I enjoy having more freedom now."
        ),
        sampleZh=(
            "有一部分变了。小时候基本就是课堂和节日合唱——"
            "简单的曲子大家都能唱，也让我敢跟别人一起唱。"
            "现在听的种类多了，但还是挑琅琅上口、合心情的。"
            "很怀念学校的歌，也喜欢现在选择更自由。"
        ),
    )
    _p(
        "How has your taste in music changed over the years?",
        "focus_wired_headphones",
        logic="对比早年爱听有歌词的歌与现在偏纯音乐，说明各自对学习的作用，再谈个人偏好。",
        kitHint="口味变化主线是 lyrics → instrumentals，与图书馆专注一致。",
        words={
            "正面回答": ["Definitely", "Toward instrumentals", "Less pop with lyrics"],
            "选项1的特点与作用": ["teen years: pop with lyrics for fun", "felt lively after class"],
            "选项2的特点与作用": ["recent years: soft instrumentals for study", "helps concentration in the library"],
            "个人感受": ["I miss singing along sometimes", "study habits shaped my taste"],
        },
        sample=(
            "Definitely. In my teen years I loved pop with lyrics — it felt lively after class. "
            "Recently, especially since I study in the library with wired headphones, "
            "I've moved toward soft instrumentals because they help concentration. "
            "I still miss singing along sometimes, but my study habits have really shaped my taste."
        ),
        sampleZh=(
            "肯定变了。十几岁时爱听有歌词的流行，课后听着很热闹。"
            "最近几年，尤其常在图书馆戴有线耳机学习后，"
            "越来越偏轻柔纯音乐，因为更利于专注。"
            "有时还是想念跟唱，但学习习惯确实改变了口味。"
        ),
    )