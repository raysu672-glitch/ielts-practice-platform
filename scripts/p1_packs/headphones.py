# -*- coding: utf-8 -*-
"""Headphones Freestyle packs (preview-page style)."""


def register(_p):
    _p(
        "When did you get your first pair of headphones?",
        "focus_wired_headphones",
        logic="先交代第一次拥有有线耳机的时间与场景，再写用途频率与感受。",
        kitHint="图书馆有线耳机：备考或自习时买/用，自然回答「何时第一副」。",
        words={
            "正面回答": ["In senior high", "Before a big exam", "A wired pair"],
            "来源或举例": ["study shop near school", "library revision", "long cable"],
            "频次": ["used every study night", "weekends too"],
            "感受": ["helped me concentrate", "cheap but reliable"],
        },
        sample=(
            "I got my first proper headphones in senior high, just before an important exam term. "
            "My mum bought a simple wired pair so I could listen to English drills in the library without disturbing others. "
            "I used them almost every study night and often at weekends too. "
            "They were cheap but reliable, and they really helped me concentrate."
        ),
        sampleZh=(
            "第一副像样的耳机是高三大考前买的。"
            "我妈买了有线款，方便我在图书馆听英语练习不打扰别人。"
            "几乎每个自习日晚上用，周末也常戴。"
            "便宜但耐用，确实帮我更专注。"
        ),
    )
    _p(
        "When did you get your first pair of headphones?",
        "wireless_earbuds_music",
        logic="先答第一次入耳式或蓝牙耳机时间，举听歌通勤场景，补频次与印象。",
        kitHint="地铁听歌素材：为通勤降噪买耳塞，时间线清晰扣第一副耳机。",
        words={
            "正面回答": ["About two years ago", "Wireless earbuds", "Birthday gift"],
            "来源或举例": ["online order", "noise on the subway", "small charging case"],
            "频次": ["daily commute since then", "gym sometimes"],
            "感受": ["felt like an upgrade", "music sounded clearer"],
        },
        sample=(
            "My first wireless earbuds came about two years ago as a birthday gift. "
            "I asked for them because the subway was noisy and I wanted clearer music on the way to school. "
            "I have used them on almost every commute since then, and sometimes at the gym. "
            "It felt like a real upgrade compared with my old phone earpieces."
        ),
        sampleZh=(
            "第一副无线耳塞大概是两年前生日收到的。"
            "地铁太吵，我想要路上听歌更清楚就向家人要了这个。"
            "从那以后几乎每天通勤都戴，偶尔健身也用。"
            "比起手机附赠耳塞，明显感觉升了一档。"
        ),
    )
    _p(
        "Do you use headphones?",
        "focus_wired_headphones",
        logic="先肯定常用，聚焦自习戴有线耳机的原因与习惯，再说影响。",
        kitHint="图书馆专注线：用耳机听网课、白噪音，回答「用不用」很直接。",
        words={
            "正面回答": ["Yes, often", "For study", "Especially wired ones"],
            "来源或举例": ["library desk", "online lectures", "low volume"],
            "频次": ["most evenings", "before exams"],
            "感受": ["blocks chatter", "easier to focus"],
        },
        sample=(
            "Yes, I use headphones quite often, especially when I study in the library. "
            "I put on a wired pair to follow online lectures or soft background sounds at low volume. "
            "That happens most evenings and more often before exams. "
            "They block other people's chatter and make it easier to focus."
        ),
        sampleZh=(
            "是的，我经常戴耳机，尤其在图书馆自习时。"
            "有线耳机听网课或低音量的背景声。"
            "大多在晚上，考前更频繁。"
            "能挡住旁边说话声，更容易集中。"
        ),
    )
    _p(
        "Do you use headphones?",
        "wireless_earbuds_music",
        logic="先答用耳塞听歌通勤，描述何时戴与听什么，感受轻松。",
        kitHint="地铁降噪听歌：日常出行必戴，扣「是否使用耳机」。",
        words={
            "正面回答": ["Definitely", "Almost every trip", "Wireless earbuds"],
            "来源或举例": ["subway platform", "playlists on phone", "noise cancelling"],
            "频次": ["twice a day", "long rides on weekends"],
            "感受": ["relaxing", "passes time quickly"],
        },
        sample=(
            "Definitely — I use wireless earbuds almost every time I take the subway. "
            "I connect them to my phone and play playlists while I wait and ride. "
            "On school days that is twice a day, and weekend trips can be longer. "
            "The music is relaxing and makes the journey pass more quickly."
        ),
        sampleZh=(
            "当然用，坐地铁几乎都会戴无线耳塞。"
            "连上手机放歌，等车乘车都在听。"
            "上学日一天两次，周末路程更长也戴。"
            "听着放松，时间过得快。"
        ),
    )
    _p(
        "How often do you use headphones?",
        "focus_wired_headphones",
        logic="行为习惯类：先给频率判断，写原因与典型一晚怎么用，再说对学习影响。",
        kitHint="自习有线耳机：几乎每晚图书馆，频率答得具体。",
        words={
            "正面回答": ["Several times a week", "More near exams", "Regular habit"],
            "原因": ["quiet listening in shared rooms", "follow pronunciation"],
            "时间线+行为描述": ["after dinner at desk", "library on weekends", "unplug when done"],
            "影响": ["steady study rhythm", "less procrastination"],
        },
        sample=(
            "I would say several times a week, and almost daily when exams are close. "
            "After dinner I use wired headphones at my desk to listen to pronunciation clips. "
            "At weekends I take the same pair to the library for a longer session. "
            "That steady rhythm helps me start work faster and waste less time online."
        ),
        sampleZh=(
            "一周好几次，临近考试几乎天天戴。"
            "晚饭后在书桌戴有线耳机听发音。"
            "周末带去图书馆学更久。"
            "节奏固定，开工更快，也少瞎刷手机。"
        ),
    )
    _p(
        "How often do you use headphones?",
        "wireless_earbuds_music",
        logic="先答高频（通勤+碎片时间），按一天时间线描述，再谈情绪影响。",
        kitHint="地铁听歌：每天往返必戴，偶尔睡前，频率高且好举例。",
        words={
            "正面回答": ["Every day", "Sometimes before sleep", "High use"],
            "原因": ["block noise", "enjoy music on the go"],
            "时间线+行为描述": ["morning commute", "ride home", "short wind-down tracks"],
            "影响": ["better mood", "do not drain phone much"],
        },
        sample=(
            "I use them every day — morning and evening on the subway, and sometimes briefly before sleep. "
            "In the morning I play upbeat songs to wake up; on the way home I pick calmer tracks. "
            "At night I might listen for ten minutes to wind down, but not too loud. "
            "It improves my mood, and the battery case means I am not charging all the time."
        ),
        sampleZh=(
            "每天都用——早晚地铁，有时睡前听一会儿。"
            "早上放节奏快的醒神，回家选安静一点的。"
            "夜里大概十分钟放松，音量不大。"
            "心情好些，充电盒也方便，不用老插电。"
        ),
    )
    _p(
        "What do you usually listen to with your headphones?",
        "focus_wired_headphones",
        logic="先列学习内容为主，再写具体资源与场景，说对专注的帮助。",
        kitHint="专注学习线：英语听力、网课、白噪音，直接回答听什么。",
        words={
            "正面回答": ["Study audio", "English listening", "Not much pop"],
            "原因": ["exam practice", "repeat sentences"],
            "时间线+行为描述": ["IELTS clips", "teacher recordings", "rain sounds sometimes"],
            "影响": ["better recall", "stay in the zone"],
        },
        sample=(
            "With my study headphones I mainly listen to English listening practice and short teacher recordings. "
            "I repeat sentences, pause, and write notes at my desk or in the library. "
            "Sometimes I add quiet rain sounds if the room is noisy. "
            "It helps me stay in the zone and remember phrases better."
        ),
        sampleZh=(
            "自习耳机主要听英语听力和老师短录音。"
            "我会跟读、暂停、记笔记，在书桌或图书馆。"
            "太吵时偶尔加很轻的雨声。"
            "更容易进入状态，短语记得牢。"
        ),
    )
    _p(
        "What do you usually listen to with your headphones?",
        "wireless_earbuds_music",
        logic="先答流行与轻音乐为主，举通勤歌单习惯，说放松作用。",
        kitHint="地铁听歌：流行、民谣、播客片段，扣「听什么」。",
        words={
            "正面回答": ["Pop and folk", "Occasional podcasts", "Favorite playlists"],
            "原因": ["relax on the train", "discover new songs"],
            "时间线+行为描述": ["shuffle on commute", "save tracks at night", "short podcast clips"],
            "影响": ["stress relief", "learn casual English phrases"],
        },
        sample=(
            "On my earbuds I usually listen to pop and soft folk music, plus short podcast clips now and then. "
            "I shuffle playlists on the train and save new songs when I get home. "
            "Some English podcasts are only five minutes, so they fit between stops. "
            "It is stress relief, and I pick up casual phrases without feeling like study."
        ),
        sampleZh=(
            "耳塞上常听流行和轻民谣，偶尔听很短播客。"
            "地铁上随机播放，回家把新歌收藏。"
            "有些英文播客就五分钟，两站之间能听完。"
            "解压，还能不知不觉学点口语表达。"
        ),
    )
    _p(
        "In what situations should people not wear headphones?",
        "focus_wired_headphones",
        logic="观点题：先明确几种不该戴场景，举图书馆与马路例子，再说安全影响。",
        kitHint="自己图书馆用耳机，更能说清「何时该摘下」的规矩与安全。",
        words={
            "正面回答": ["When crossing roads", "During conversations", "In some quiet zones"],
            "举例或原因": ["cannot hear traffic", "rude to teachers", "library rules at desks"],
            "作用或影响": ["avoid accidents", "show respect"],
            "感受": ["common sense", "I lower volume near roads"],
        },
        sample=(
            "People should not wear headphones when they need to hear warnings, like crossing busy roads or cycling in traffic. "
            "They should also take them off when someone is talking to them directly, such as a teacher or a cashier. "
            "Even in a library, blasting music can break the quiet rules. "
            "I think it is common sense — I always lower or remove mine near streets."
        ),
        sampleZh=(
            "需要听到警示就别戴，比如过繁忙路口或在车流里骑车。"
            "别人当面跟你说话也该摘下，对老师或收银员是礼貌。"
            "图书馆里音量太大也破规矩。"
            "这是常识——我在路边会把音量调低或摘掉。"
        ),
    )
    _p(
        "In what situations should people not wear headphones?",
        "wireless_earbuds_music",
        logic="从通勤经验谈地铁闸门、骑车与夜间跑步等不宜戴全降噪的情况。",
        kitHint="地铁听歌素材反向用：全降噪看不见车声、报站，举例更有力。",
        words={
            "正面回答": ["On bike lanes", "Station platforms edges", "When driving"],
            "举例或原因": ["miss train announcements", "car horns", "legal rules"],
            "作用或影响": ["safer for everyone", "fewer near misses"],
            "感受": ["one ear out sometimes", "music can wait"],
        },
        sample=(
            "I think people should avoid full noise cancelling when they ride a bike or stand near the edge of a subway platform. "
            "If you cannot hear announcements or a horn, small mistakes can become dangerous. "
            "Drivers should not wear earbuds at all — that is illegal in many places. "
            "I sometimes leave one ear out on the train; music can wait when safety matters."
        ),
        sampleZh=(
            "骑车或站在站台边缘时，别全开降噪。"
            "听不见报站或喇叭，小疏忽也可能出事。"
            "开车更不该戴耳塞，很多地方还违法。"
            "我在地铁有时只戴一边；安全时音乐可以等等。"
        ),
    )
    _p(
        "Which do you prefer, big headphones or small earbuds?",
        "wireless_earbuds_music",
        logic="对比题：先选耳塞，分别写大耳罩与耳塞优缺点，落在通勤方便。",
        kitHint="地铁听歌偏耳塞：轻便、降噪够用，与大耳机对比鲜明。",
        words={
            "正面回答": ["Small earbuds", "Easier to carry", "Good enough sound"],
            "选项1的特点与作用": ["big headphones: comfort at home", "bulky in bag"],
            "选项2的特点与作用": ["earbuds: pocket size", "quick on subway"],
            "个人感受": ["prefer light gear", "might buy big ones for desk"],
        },
        sample=(
            "I prefer small earbuds for everyday life. "
            "Big headphones sound warm and comfy at home, but they are bulky in my bag and sweaty in summer. "
            "Earbuds fit in a pocket, connect fast, and are enough for my subway rides. "
            "I like light gear when I move around, though I might get big ones later just for desk study."
        ),
        sampleZh=(
            "日常我更爱小耳塞。"
            "大头戴在家暖和舒服，但占地方夏天也闷。"
            "耳塞放口袋、连接快，坐地铁够用。"
            "在外面喜欢轻便，以后或许再买大头戴专门自习。"
        ),
    )
    _p(
        "Which do you prefer, big headphones or small earbuds?",
        "focus_wired_headphones",
        logic="先选大头戴或有线大耳，对比自习沉浸与耳塞轻便，个人感受偏学习。",
        kitHint="图书馆有线大耳：沉浸、不漏音，与耳塞对比扣偏好题。",
        words={
            "正面回答": ["Bigger over-ear style", "For long study", "Wired is fine"],
            "选项1的特点与作用": ["over-ear: blocks noise", "comfort for hours"],
            "选项2的特点与作用": ["earbuds: fine for short trips", "easy to lose"],
            "个人感受": ["choose by task", "love focus at library"],
        },
        sample=(
            "For studying I prefer bigger over-ear headphones with a cable — they sit on my ears for hours without hurting. "
            "They block library noise better than tiny earbuds, so I do not raise the volume too much. "
            "Earbuds are great for a twenty-minute bus ride, but they are easier to lose and less comfortable for long sessions. "
            "So I choose by task, and I love that deep focus at the library."
        ),
        sampleZh=(
            "学习时我更喜欢有线大包耳，戴久耳不累。"
            "比小耳塞更隔噪，不用把音量开太大。"
            "耳塞适合短程公交，但容易丢，长时间也不舒服。"
            "看场景选，我最爱图书馆那种沉浸感。"
        ),
    )