# -*- coding: utf-8 -*-
"""Singing Freestyle packs."""


def register(_p):
    _p(
        "What songs did you sing when you were a child?",
        "singing_ktv_songs",
        logic="先直接列举童年唱的歌，再扩展到后来 KTV，补频率与开心感受。",
        kitHint="KTV 套装：童年从儿歌讲起，再 lightly 连到朋友唱歌。",
        words={
            "正面回答": ["Simple children's songs", "School songs first", "Quite a few"],
            "来源或举例": ["nursery rhymes", "classroom favourites", "later pop at KTV"],
            "频次": ["often at home as a kid", "now at KTV with friends"],
            "感受": ["happy", "fun", "not about being talented"],
        },
        sample=(
            "When I was a child I sang simple children's songs and those easy nursery rhymes at home. "
            "At school we had a few classroom favourites too. "
            "Later with friends I moved on to pop songs at KTV, but the childish ones came first. "
            "I wasn't serious every day, but singing made me happy even without real talent."
        ),
        sampleZh=(
            "小时候在家唱简单的儿歌和那些好记的童谣。"
            "学校也有几首班上常唱的歌。"
            "后来和朋友去 KTV 才唱流行歌，但最早还是那些小儿歌。"
            "不是天天认真练，但就算没天赋唱着也开心。"
        ),
    )
    _p(
        "What songs did you sing when you were a child?",
        "school_choir_songs",
        logic="先答童年唱什么，紧扣音乐课与节日合唱，补上课频率与温暖感受。",
        kitHint="课堂歌曲：来源必须是学校合唱与儿歌。",
        words={
            "正面回答": ["Classroom songs", "Children's songs", "Festival songs"],
            "来源或举例": ["music teacher's choices", "whole-class singing", "spring festival rehearsing"],
            "频次": ["weekly music lessons", "before school shows"],
            "感受": ["warm", "memorable", "made shy kids join in"],
        },
        sample=(
            "Mostly classroom songs and simple children's songs from music lessons. "
            "Our teacher picked easy tunes, and the whole class sang together. "
            "Before school shows we also rehearsed festival songs, maybe weekly in term time. "
            "It felt warm, and even shy classmates would join in."
        ),
        sampleZh=(
            "主要是音乐课上的课堂歌和简单儿歌。"
            "老师选好唱的歌，全班一起唱。"
            "演出前还会排练节日歌曲，学期里大概每周都有。"
            "很温馨，害羞的同学也愿意开口。"
        ),
    )
    _p(
        "Have you ever learnt how to sing?",
        "singing_ktv_songs",
        logic="先正面答是否学过，说明主要是自学和 KTV 练出来的，补频率与放松影响。",
        kitHint="没正经声乐课也合法：KTV 与自我练习算「学过一点」。",
        words={
            "正面回答": ["A little", "Not professionally", "Mostly by practising"],
            "来源或举例": ["KTV with classmates", "following lyrics on screen", "copying singers"],
            "频次": ["most weekends with friends", "more before holidays"],
            "感受": ["enjoyable", "social", "helps me de-stress"],
        },
        sample=(
            "A little, but not in a professional way. "
            "I learnt mainly by going to KTV with classmates — following the lyrics on screen "
            "and copying how other people sing. "
            "I do that most weekends, more when we have holidays. "
            "It's enjoyable and social, and it helps me de-stress."
        ),
        sampleZh=(
            "算学过一点，但不是专业那种。"
            "主要是和同学去 KTV，盯着屏幕歌词、模仿别人怎么唱。"
            "大部分周末会去，放假前更勤。"
            "好玩也社交，还能减压。"
        ),
    )
    _p(
        "Have you ever learnt how to sing?",
        "school_choir_songs",
        logic="先答学校里有没有学过唱，举例音乐课，补频率与课堂影响。",
        kitHint="音乐课合唱即「学过怎么唱」的合法来源。",
        words={
            "正面回答": ["Yes, in school", "Basic skills", "Not private lessons"],
            "来源或举例": ["music class", "choir-style practice", "festival rehearsals"],
            "频次": ["every week in primary school", "extra before performances"],
            "感受": ["encouraging", "simple", "built my confidence"],
        },
        sample=(
            "Yes, in a basic way at school — we had music class and choir-style practice. "
            "The teacher showed us how to breathe and stay in tune for simple songs. "
            "That was every week in primary school, with extra rehearsals before performances. "
            "It was encouraging and built a bit of confidence, even though the songs were simple."
        ),
        sampleZh=(
            "在学校算学过基础——有音乐课，也有像合唱那样的练习。"
            "老师会教呼吸、简单歌怎么跟调子。"
            "小学大概每周都有，演出前会多加练。"
            "挺鼓励人的，歌虽简单但让我敢开口一点。"
        ),
    )
    _p(
        "Do you like singing?",
        "singing_ktv_songs",
        logic="先正面答喜不喜欢，再讲 KTV 与朋友原因，补频率与快乐感受。",
        kitHint="喜欢的是「唱」和社交氛围，不是炫技。",
        words={
            "正面回答": ["Yes, I do", "With friends", "Even if I'm not great"],
            "原因或时间": ["KTV nights are fun", "since high school hangouts"],
            "频次": ["most weekends", "sometimes after exams"],
            "感受": ["happy", "relaxed", "shared laughter"],
        },
        sample=(
            "Yes, I do, especially with friends at KTV — I'm not amazing, but it's fun anyway. "
            "I got into it more in high school when classmates started weekend hangouts. "
            "I sing most weekends, sometimes after exams when everyone wants to relax. "
            "It makes me happy and we always share a good laugh."
        ),
        sampleZh=(
            "喜欢，尤其和朋友在 KTV——唱得一般但好玩。"
            "高中同学常周末聚会后就更爱去了。"
            "大部分周末会唱，考完试想放松时也会。"
            "开心，大家总能笑成一团。"
        ),
    )
    _p(
        "Do you like singing?",
        "school_choir_songs",
        logic="先答是否喜欢唱，再连音乐课合唱原因，补频率与温馨感受。",
        kitHint="课堂合唱带来「喜欢集体唱」而非独唱表演。",
        words={
            "正面回答": ["Yes, casually", "In a group", "Simple songs"],
            "原因或时间": ["singing with classmates feels easy", "from music lessons"],
            "频次": ["still hum old songs at home", "when friends ask for a chorus"],
            "感受": ["warm", "nostalgic", "not stressful"],
        },
        sample=(
            "Yes, casually — I like singing in a group more than performing alone. "
            "Music lessons at school made it feel easy because everyone joined in. "
            "I still hum those old songs at home, or when friends want a quick chorus. "
            "It feels warm and nostalgic, and not stressful at all."
        ),
        sampleZh=(
            "喜欢，算随意那种——更爱跟大家一起唱，不爱单独表演。"
            "学校音乐课人人都唱，所以不觉得难。"
            "在家还会哼老歌，朋友起哄时也会跟两句。"
            "温馨又怀旧，也不紧张。"
        ),
    )
    _p(
        "When do you usually sing?",
        "singing_ktv_songs",
        logic="先答通常何时唱，再讲 KTV 时间线与行为，补频率与社交影响。",
        kitHint="行为习惯：周末 KTV 为主轴。",
        words={
            "正面回答": ["At weekends", "With friends", "After busy weeks"],
            "原因": ["need to relax", "KTV is our usual hangout"],
            "时间线+行为描述": ["book a small room", "take turns on the mic"],
            "影响": ["relieves stress", "strengthens friendships", "lightens my mood"],
        },
        sample=(
            "I usually sing at weekends with friends, especially after a busy week. "
            "We book a small KTV room, order snacks, and take turns on the mic. "
            "That happens most Saturdays if everyone is free, sometimes on Sunday evenings too. "
            "It relieves stress, lightens my mood, and keeps us close."
        ),
        sampleZh=(
            "一般在周末和朋友唱，忙完一周尤其会。"
            "我们会订小包厢，吃点东西，轮流拿麦。"
            "周六大家有空时多半会去，周日晚上有时也会。"
            "能减压、心情变好，感情也保持着。"
        ),
    )
    _p(
        "When do you usually sing?",
        "school_choir_songs",
        logic="先答何时会唱（如今多为即兴），再连童年课堂习惯，补频率与放松影响。",
        kitHint="现在时点：居家哼唱/朋友小聚，素材仍扣 singing。",
        words={
            "正面回答": ["Evenings at home", "When I'm in a good mood", "Sometimes with classmates"],
            "原因": ["old school songs pop into my head", "humming is easy"],
            "时间线+行为描述": ["play a classroom song softly", "sing along while tidying"],
            "影响": ["lifts my spirits", "quick break from study", "reminds me of school"],
        },
        sample=(
            "These days I usually sing in the evening at home when I'm in a good mood. "
            "Old school songs pop into my head, so I play one softly or hum while I'm tidying. "
            "Maybe a few times a week — sometimes classmates join in on a video call. "
            "It's a quick break from study and lifts my spirits."
        ),
        sampleZh=(
            "现在多半晚上在家心情好时会唱。"
            "老课堂歌会突然冒出来，我就轻轻放或边收拾边哼。"
            "一周大概几次，有时同学视频里也会跟唱。"
            "算学习间隙，也让人提神。"
        ),
    )
    _p(
        "Do you think singing can bring happiness to people?",
        "singing_ktv_songs",
        logic="先正面观点，再举 KTV 例子，说明作用与个人感受。",
        kitHint="观点类：用聚会唱歌证明「带来快乐」。",
        words={
            "正面回答": ["Yes, definitely", "Especially together", "Even average singers"],
            "举例或原因": ["KTV nights with friends", "laughing at mistakes", "shared favourites"],
            "作用或影响": ["releases stress", "creates memories", "bonds people"],
            "感受": ["hopeful", "happy", "inclusive"],
        },
        sample=(
            "Yes, definitely — singing can bring happiness, especially when people do it together. "
            "At KTV we laugh at small mistakes and cheer when someone nails a favourite song. "
            "That releases stress and creates shared memories after tough study weeks. "
            "I always leave feeling happier and more connected to my friends."
        ),
        sampleZh=(
            "当然能——一起唱特别容易让人开心。"
            "KTV 里唱砸了我们也会笑，唱好一首大家爱的歌会一起欢呼。"
            "能释放压力，备考苦一点的日子也会留下共同回忆。"
            "我出来情绪总是更好，跟朋友的联结也更紧。"
        ),
    )
    _p(
        "Do you think singing can bring happiness to people?",
        "school_choir_songs",
        logic="先肯定观点，再举学校合唱例子，说明对害羞同学的作用与感受。",
        kitHint="课堂合唱体现「人人能参与的快乐」。",
        words={
            "正面回答": ["Yes, I think so", "Simple songs work", "Group singing matters"],
            "举例或原因": ["whole-class singing", "festival rehearsals", "easy melodies"],
            "作用或影响": ["shy students join in", "lightens the school day", "builds belonging"],
            "感受": ["warm", "inclusive", "encouraging"],
        },
        sample=(
            "Yes, I think so. Even simple songs can make people happy when everyone sings together. "
            "In school music class, shy students would finally join festival rehearsals "
            "because the melodies were easy. "
            "That lightened the school day and gave people a sense of belonging. "
            "The mood always felt warm and encouraging."
        ),
        sampleZh=(
            "我觉得能。简单的歌大家一起唱也容易让人高兴。"
            "学校音乐课上，害羞的同学也会在节日排练里开口，"
            "因为旋律好跟。"
            "让上学轻松一点，也有归属感。"
            "气氛总是温馨、让人敢试。"
        ),
    )
    _p(
        "How popular is karaoke now compared with the past?",
        "school_choir_songs",
        logic="对比现在 KTV 与过去课堂唱歌的流行程度，再谈个人感受。",
        kitHint="对比类：课堂集体唱「当年更普遍」vs 现在商业 KTV。",
        words={
            "正面回答": ["Karaoke is still popular", "Different from school days", "Both have fans"],
            "选项1的特点与作用": ["past: everyone sang together in music class", "low cost and inclusive"],
            "选项2的特点与作用": ["now: KTV apps and rooms are trendy", "more private and flexible"],
            "个人感受": ["I miss classroom singing", "modern KTV is convenient"],
        },
        sample=(
            "Karaoke is still popular, but it feels different from when I was a child. "
            "In the past, almost everyone sang together in music class — it was low cost and very inclusive. "
            "Now KTV apps and private rooms are trendy, so people choose their own time and songs. "
            "I miss that classroom warmth, yet I enjoy how convenient modern karaoke is."
        ),
        sampleZh=(
            "卡拉 OK 还是受欢迎，但跟小时候感觉不一样。"
            "以前几乎人人都在音乐课一起唱——花得少，谁都能参与。"
            "现在是 KTV 软件和包厢更潮，时间歌曲都自选。"
            "我怀念课堂那种热闹，但也觉得现在的 KTV 很方便。"
        ),
    )
    _p(
        "How popular is karaoke now compared with the past?",
        "singing_ktv_songs",
        logic="对比过去家庭/简单娱乐与现在 KTV 社交，说明各自特点与个人观感。",
        kitHint="个人从儿歌到周末 KTV 亲历对比。",
        words={
            "正面回答": ["More commercial now", "Still part of social life", "Definitely still common"],
            "选项1的特点与作用": ["past: simple singing at home or school", "fewer choices but more daily"],
            "选项2的特点与作用": ["now: weekend KTV with friends", "wide song lists and better sound"],
            "个人感受": ["I go out to sing more now", "it feels more like an event"],
        },
        sample=(
            "I'd say karaoke is more commercial now, but still a big part of social life. "
            "In the past I mostly sang simple songs at home or at school, with fewer choices but more daily habit. "
            "Now my friends book KTV most weekends — huge song lists and better sound systems. "
            "I go out to sing more than before, and it feels more like a proper event."
        ),
        sampleZh=(
            "我觉得现在更商业化了，但仍是社交生活很大一块。"
            "以前主要在家或学校唱简单的歌，选择少但更日常。"
            "现在朋友周末常订 KTV，歌多、音响也好。"
            "我外出唱歌比过去多，更像一件像样的活动。"
        ),
    )