# -*- coding: utf-8 -*-
"""Jokes & Comedies Freestyle packs."""


def register(_p):
    _p(
        "Who is the funniest person you know?",
        "douyin_scroll_habit",
        logic="先点名认识的人，再说明他如何用短视频逗笑你，补上频率与解压感受。",
        kitHint="本题必须答「人」：抖音只是他分享好笑片段的方式，不是把抖音说成最搞笑。",
        words={
            "正面回答": ["My roommate", "A close friend", "Someone on my floor"],
            "来源或举例": ["light Douyin clips", "short jokes", "funny dorm stories"],
            "频次": ["most evenings", "after study", "before sleep"],
            "感受": ["helps me relax", "makes everyone laugh", "relaxed"],
        },
        sample=(
            "My roommate is the funniest person I know on campus. "
            "He saves light Douyin clips and tells short jokes that make us laugh after study. "
            "That happens most evenings in the dorm before I sleep. "
            "I find his humour really helps me relax when everyone feels tired."
        ),
        sampleZh=(
            "我宿舍室友是我认识里最搞笑的人。"
            "他会收藏轻松的抖音片段，学习后在宿舍讲短笑话逗大家笑。"
            "多数晚上睡前都会这样。"
            "我觉得大家在累的时候，他的幽默很解压。"
        ),
    )
    _p(
        "Who is the funniest person you know?",
        "comedy_hang_out",
        logic="先答具体的人，再举看喜剧、聚会的细节，补周末频率与温暖感受。",
        kitHint="喜剧片/聚会是这位朋友逗笑你的方式；主角仍是这个人。",
        words={
            "正面回答": ["My roommate", "My best friend", "A classmate"],
            "来源或举例": ["watch comedies", "hang out with friends", "turn small stories funny"],
            "频次": ["most weekends", "Friday nights", "when we eat together"],
            "感受": ["warm", "easy to enjoy", "relieves stress"],
        },
        sample=(
            "My roommate is the funniest person I know. "
            "He watches light comedies with friends and turns small dorm stories into a good laugh. "
            "We do that most weekends when we hang out and eat together. "
            "I find his humour warm and easy to enjoy after a long week."
        ),
        sampleZh=(
            "我室友是我认识里最搞笑的人。"
            "他和朋友看轻松喜剧，还把宿舍小事讲得好笑。"
            "周末一起出去吃饭时常常如此。"
            "我觉得忙一周后，这种幽默温暖又好接受。"
        ),
    )
    _p(
        "What made you laugh when you were a child?",
        "douyin_scroll_habit",
        logic="先点童年笑源，再举动画片/同学笑话（非抖音童年硬套），补当时频率与诚实感受。",
        kitHint="童年题用校园/卡通；成年刷抖音的梗别当成小时候的主线。",
        words={
            "正面回答": ["Simple cartoons", "Classmates' jokes", "Silly playground moments"],
            "来源或举例": ["funny clips on TV", "short jokes", "playground games"],
            "频次": ["after school", "at weekends", "with friends"],
            "感受": ["honest", "easy to remember", "light-hearted"],
        },
        sample=(
            "As a child I laughed at simple cartoons and classmates' silly jokes on the playground. "
            "A short funny clip on TV after homework could keep me smiling for the whole evening. "
            "That happened quite often after school and at weekends. "
            "I find those laughs honest and easy to remember now."
        ),
        sampleZh=(
            "小时候我笑简单动画片和同学在操场上的傻笑话。"
            "写完作业看电视里短搞笑片段，能开心一整晚。"
            "放学后和周末挺常见。"
            "现在想起来那种笑很真实、好记。"
        ),
    )
    _p(
        "What made you laugh when you were a child?",
        "comedy_hang_out",
        logic="先说童年易被逗笑的事，再举和家人看喜剧或朋友打闹，补频率与快乐回忆。",
        kitHint="素材=喜剧片/聚会回忆版：童年看轻松喜剧、家人朋友一起笑。",
        words={
            "正面回答": ["Family comedies", "Friends' stories", "Simple jokes"],
            "来源或举例": ["watch movies", "hang out with cousins", "enjoy a good laugh"],
            "频次": ["on holidays", "after dinner", "with family"],
            "感受": ["warm memories", "happy", "relaxed"],
        },
        sample=(
            "As a child I laughed most when my family watched light comedies after dinner. "
            "My cousins also told small funny stories when we hung out on holidays. "
            "That was quite often during school breaks at home. "
            "I find those memories warm and still make me smile."
        ),
        sampleZh=(
            "小时候晚饭后全家看轻松喜剧时我最爱笑。"
            "假期和表兄妹聚会时，他们也会讲好笑的小事。"
            "学校放假在家时挺常见。"
            "我觉得那些回忆很暖，现在想起来还会笑。"
        ),
    )
    _p(
        "Are you good at telling jokes?",
        "comedy_hang_out",
        logic="先诚实说水平，再说明更爱听/看喜剧而非正式讲段子，补朋友场合与轻松影响。",
        kitHint="「不擅长讲笑话」合法；重点在和朋友看喜剧、自然幽默。",
        words={
            "正面回答": ["Not really", "Only simple ones", "I'm better at listening"],
            "来源或举例": ["watch comedies", "share funny daily stories", "hang out with friends"],
            "频次": ["at weekends", "after exams", "in the dorm"],
            "感受": ["relaxed", "enjoy a good laugh", "natural"],
        },
        sample=(
            "Not really — I am not great at telling staged jokes. "
            "I am better at watching light comedies with friends and sharing funny daily stories in the dorm. "
            "That happens at weekends or after exams when everyone needs a break. "
            "I find that kind of humour more natural and relaxing for me."
        ),
        sampleZh=(
            "不太行——我不太会讲那种完整段子。"
            "我更擅长和朋友看轻松喜剧，或在宿舍聊好笑的小事。"
            "周末或考完试需要放松时常见。"
            "我觉得这种幽默更自然，也让我放松。"
        ),
    )
    _p(
        "Are you good at telling jokes?",
        "douyin_scroll_habit",
        logic="先否定或弱化讲笑话能力，再说明会转发好笑短视频逗朋友，补晚上频率与气氛影响。",
        kitHint="讲笑话弱项时，可用分享搞笑短视频带动宿舍气氛。",
        words={
            "正面回答": ["Not especially", "I forward funny clips", "Simple humour only"],
            "来源或举例": ["Douyin funny clips", "short videos", "quick shares"],
            "频次": ["most evenings", "before sleep", "after study"],
            "感受": ["lightens the mood", "quick laugh", "stress relief"],
        },
        sample=(
            "Not especially. I cannot tell long jokes well, but I forward funny Douyin clips to my roommate. "
            "A fifteen-second clip is enough to light up the mood after study. "
            "I do that most evenings before sleep in the dorm. "
            "I find quick shared humour a simple stress relief for both of us."
        ),
        sampleZh=(
            "不太会。我讲不好长笑话，但会把好笑的抖音片段转给室友。"
            "学习后十几秒的片段就够活跃气氛。"
            "多数晚上睡前在宿舍会这样。"
            "我觉得这种快速共享的幽默对咱俩都是简单解压。"
        ),
    )
    _p(
        "Do you like telling jokes?",
        "comedy_hang_out",
        logic="先表态有时喜欢轻松 humour，再说明原因在与朋友互动，补周末频率与减压感受。",
        kitHint="喜好题：喜欢的是和朋友一起笑，不是当脱口秀演员。",
        words={
            "正面回答": ["Sometimes", "Yes, in a light way", "With close friends"],
            "原因或时间": ["relieve stress", "after a long week", "since secondary school"],
            "频次": ["at weekends", "Friday nights", "when friends visit"],
            "感受": ["cheers me up", "closer to friends", "relaxed"],
        },
        sample=(
            "Sometimes I do, but only in a light way with close friends. "
            "After a long week I like turning small dorm stories into a laugh while we watch comedies. "
            "That is usually at weekends or on Friday nights. "
            "I find it cheers me up and keeps friendships easy."
        ),
        sampleZh=(
            "有时喜欢，但也只和熟朋友轻松讲讲。"
            "忙完一周，我一边看喜剧一边把宿舍小事讲得好玩。"
            "一般在周末或周五晚上。"
            "我觉得这能让我开心，也让朋友相处更轻松。"
        ),
    )
    _p(
        "Do you like telling jokes?",
        "douyin_scroll_habit",
        logic="先说你更常分享好笑视频而非正式讲笑话，再补原因与晚间频率及心情影响。",
        kitHint="「喜欢」可落在分享搞笑短视频，不必硬说自己爱讲段子。",
        words={
            "正面回答": ["Yes, in a small way", "I like sharing clips", "Not long jokes"],
            "原因或时间": ["quick laugh", "easy to share", "after class"],
            "频次": ["every evening", "before sleep", "when bored"],
            "感受": ["fun", "relieves stress", "light mood"],
        },
        sample=(
            "Yes, in a small way — I like sharing funny short videos more than telling long jokes. "
            "A quick clip is easy to send when a friend looks tired after class. "
            "I do that almost every evening before sleep. "
            "I find it fun and it relieves stress without taking much time."
        ),
        sampleZh=(
            "算喜欢一点——我更爱分享搞笑短视频，不爱讲长笑话。"
            "同学下课后看着累，发个小片段很方便。"
            "几乎每天睡前都会。"
            "我觉得好玩又解压，也不费时间。"
        ),
    )
    _p(
        "What kind of comedy do you enjoy?",
        "comedy_hang_out",
        logic="先点明偏好轻松喜剧，再说明原因与时间场景，补周末频率与放松感受。",
        kitHint="偏好=轻喜剧+和朋友看；别答成只刷手机不互动。",
        words={
            "正面回答": ["Light comedies", "Gentle humour", "Short funny films"],
            "原因或时间": ["after exams", "with friends", "not too aggressive"],
            "频次": ["most weekends", "in the dorm", "sometimes at the cinema"],
            "感受": ["relaxed", "enjoy a good laugh", "not too noisy"],
        },
        sample=(
            "I enjoy light comedies and gentle humour more than loud stand-up shows. "
            "After exams I like watching them with friends in the dorm because they are not too aggressive. "
            "That is most weekends when we have time to hang out. "
            "I find that style relaxed and easy to enjoy."
        ),
        sampleZh=(
            "我喜欢轻松喜剧、温和幽默，不太听吵闹的脱口秀。"
            "考完试在宿舍和朋友看，因为不会太刺激。"
            "周末有空聚会时大多如此。"
            "我觉得这种风格放松、好接受。"
        ),
    )
    _p(
        "What kind of comedy do you enjoy?",
        "douyin_scroll_habit",
        logic="先答喜欢短片/生活向搞笑内容，再说明晚上刷短视频的场景，补频率与解压感受。",
        kitHint="抖音=搞笑内容类型之一，答「何种喜剧」而非只说我爱刷抖音。",
        words={
            "正面回答": ["Short funny clips", "Life-style humour", "Quick sketches"],
            "原因或时间": ["easy after study", "on my phone", "when I need a break"],
            "频次": ["most evenings", "before sleep", "on the subway"],
            "感受": ["quick laugh", "light mood", "stress buster"],
        },
        sample=(
            "I enjoy short funny clips and everyday life humour more than long theatre comedy. "
            "On my phone I watch quick sketches when I need a break after study. "
            "That is most evenings, sometimes on the subway too. "
            "I find them a quick laugh and a light stress buster if I do not scroll too long."
        ),
        sampleZh=(
            "我喜欢短搞笑片段和贴近生活的幽默，不太看长篇舞台喜剧。"
            "学习后会在手机上看快速小段子放松。"
            "多数晚上如此，地铁上有时也会。"
            "我觉得能快速笑一下、减压，但自己也得控制别刷太久。"
        ),
    )
    _p(
        "Why do you think comedy shows are so popular these days?",
        "comedy_hang_out",
        logic="先给观点，再举压力与社交需求为例，说明喜剧的作用，补个人感受。",
        kitHint="观点题四步用「举例或原因/作用或影响」；可用周末看喜剧解压。",
        words={
            "正面回答": ["People need to relax", "Life feels stressful", "Yes, they are popular"],
            "举例或原因": ["work or study pressure", "watch comedies with friends", "cheap entertainment"],
            "作用或影响": ["relieve stress", "share a good laugh", "escape briefly"],
            "感受": ["understandable", "healthy in moderation", "relaxed"],
        },
        sample=(
            "I think people need easy ways to relax, so comedy shows stay popular. "
            "Many students feel study pressure and watch light comedies with friends at weekends. "
            "Shared laughter helps them relieve stress and forget deadlines for a while. "
            "I find that understandable and healthy in moderation."
        ),
        sampleZh=(
            "我觉得大家需要轻松的放松方式，所以喜剧节目一直很受欢迎。"
            "很多学生有学业压力，周末和朋友看轻喜剧。"
            "一起笑能减压，暂时忘掉截止日期。"
            "我觉得这可以理解，适度也挺健康。"
        ),
    )
    _p(
        "Why do you think comedy shows are so popular these days?",
        "douyin_scroll_habit",
        logic="先答短视频时代让人更易接触喜剧，再举例手机上看短段子，说影响与个人感受。",
        kitHint="抖音可支撑「短、快、易传播」，但主题是喜剧为何流行，不是夸抖音本身。",
        words={
            "正面回答": ["Short formats spread fast", "Phones make comedy easy", "Yes, very popular"],
            "举例或原因": ["funny clips online", "quick to watch", "after class breaks"],
            "作用或影响": ["lighten the mood", "cheap stress relief", "easy to share"],
            "感受": ["convenient", "can be addictive", "mostly positive"],
        },
        sample=(
            "I think comedy is popular because short funny clips spread fast on phones. "
            "After class many people watch quick sketches during a five-minute break. "
            "That lightens the mood and works as cheap stress relief they can share. "
            "I find it convenient, though it can be addictive if there is no limit."
        ),
        sampleZh=(
            "我觉得喜剧很受欢迎，很大程度上是因为手机里好笑的短内容传得特别快。"
            "下课后很多人用五分钟间隙看小段子。"
            "能调节心情，也是便宜的减压方式，还能转发。"
            "我觉得方便，但没节制的话也容易上瘾。"
        ),
    )