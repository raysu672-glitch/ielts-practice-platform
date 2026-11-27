# -*- coding: utf-8 -*-
"""Home & Accommodation Freestyle packs."""


def register(_p):
    # --- Do you live in a house or a flat? (shishi) ---
    _p(
        "Do you live in a house or a flat?",
        "dorm_apartment_life",
        logic="先直接说住宿舍还是租房，再举例说明位置与室友，补居住多久与踏实感受。",
        kitHint="本题切「居所类型」：dorm 或 rented flat，不要跑去聊整洁习惯。",
        words={
            "正面回答": ["a flat", "campus dorms", "a rented apartment"],
            "来源或举例": ["with my roommate", "a residential area", "10 minutes from the subway"],
            "频次": ["since I started university", "for about two years now"],
            "感受": ["practical", "loose and comfortable", "easy for commuting"],
        },
        sample=(
            "I live in a flat — well, campus dorms that work like a small flat with my roommate. "
            "It's in a residential area about 10 minutes' walk from the subway. "
            "I've been there since I started university, for about two years now. "
            "I find it practical and quite comfortable after classes."
        ),
        sampleZh=(
            "我住的是公寓——其实是和室友一起住的宿舍，跟小平层差不多。"
            "在居民区，离地铁走大概十分钟。"
            "上大学后就一直住那儿，快两年了。"
            "下课后住着挺实用、也蛮舒服的。"
        ),
    )
    _p(
        "Do you live in a house or a flat?",
        "tidy_desk_habit",
        logic="先答住所类型，再轻轻带到书桌角落是主要活动区，补晚上学习频率与顺手感受。",
        kitHint="整洁素材在本题只做「书桌角落」软性场景，主答仍是 house/flat。",
        words={
            "正面回答": ["a flat", "dorm rooms", "not a house"],
            "来源或举例": ["a desk corner", "two beds in one room", "storage boxes"],
            "频次": ["every evening before study", "most nights at the desk"],
            "感受": ["compact but workable", "helps me focus", "fine for a student"],
        },
        sample=(
            "I live in a flat, or more exactly a university dorm room with my roommate — not a house. "
            "My main spot at home is a desk corner where I keep books in small boxes. "
            "I sit there most evenings before I study. "
            "It's compact, but a clear desk still helps me focus."
        ),
        sampleZh=(
            "我住公寓，准确说是和室友的宿舍，不是独栋房子。"
            "家里我常待的是书桌那一角，书用小箱子收着。"
            "多数晚上学习前都会坐那儿。"
            "空间不大，但书桌干净时我更能集中。"
        ),
    )
    _p(
        "Do you live in a house or a flat?",
        "parents_tidy_home",
        logic="先答现在住 flat，再对比童年家里更像 house，补周末回家频率与想念感受。",
        kitHint="父母整理素材仅作童年家的柔和背景；现在仍是 flat/dorm 正面回答。",
        words={
            "正面回答": ["a flat now", "campus accommodation", "not a house anymore"],
            "来源或举例": ["childhood house with parents", "my own small room back then", "weekend visits home"],
            "频次": ["every month or so", "on longer holidays"],
            "感受": ["different but normal", "warmer at parents' place", "used to both"],
        },
        sample=(
            "I live in a flat on campus now, not a house. "
            "When I was a child we had a small house with my parents, and my mum kept everything neat there. "
            "I still go back every month or so on a longer weekend. "
            "Both feel normal — campus is practical, and home still feels warm."
        ),
        sampleZh=(
            "我现在住校内公寓，不是独栋房子。"
            "小时候和父母住过小房子，妈妈会把家里收拾得很整齐。"
            "大概每个月长一点的周末会回去一趟。"
            "两种生活都习惯——学校这边方便，家里仍很温馨。"
        ),
    )

    # --- Who do you live with? (shishi) ---
    _p(
        "Who do you live with?",
        "dorm_apartment_life",
        logic="直接点明室友姓名/关系，再补是否曾与校外租房同伴，最后说平时相处频率与感受。",
        kitHint="必须点名「和谁」：室友、父母等人物，不能只描述宿舍家具。",
        words={
            "正面回答": ["my roommate", "one classmate", "just the two of us"],
            "来源或举例": ["Li Wei from my major", "we share one dorm", "sometimes cook noodles together"],
            "频次": ["every night on campus", "most weekdays together"],
            "感受": ["easy to get along", "not lonely", "practical for study"],
        },
        sample=(
            "I live with my roommate Li Wei — he's from my major and we share one dorm. "
            "Sometimes we cook simple noodles together after evening classes. "
            "We're together most nights on campus during term time. "
            "It's easy to get along, and I don't feel lonely."
        ),
        sampleZh=(
            "我和室友李伟住一起，同专业，一个宿舍。"
            "晚上没课后有时会一起煮点面条。"
            "学期里大多数晚上都在一块儿。"
            "相处挺顺，也不觉得孤单。"
        ),
    )
    _p(
        "Who do you live with?",
        "tidy_desk_habit",
        logic="先答室友是谁，再提到俩人轮流收拾共用桌，补每晚习惯与少摩擦感受。",
        kitHint="仍先答「和谁住」；书桌整洁只是共同生活的细节。",
        words={
            "正面回答": ["my roommate", "two of us in the dorm", "no family on campus"],
            "来源或举例": ["we agreed to tidy the desk", "put textbooks away", "split small chores"],
            "频次": ["every night before sleep", "before long study sessions"],
            "感受": ["fewer small arguments", "respectful", "works for both"],
        },
        sample=(
            "I live with my roommate — just the two of us in the dorm, no family here. "
            "We agreed to clear the shared desk every night and put textbooks away. "
            "We do that before sleep or before a long study session. "
            "It keeps small arguments down and feels respectful."
        ),
        sampleZh=(
            "我和室友住，宿舍里就我们俩，家人不在这边。"
            "我们约好每晚收拾共用书桌，把课本收好。"
            "睡前或长时间学习前都会做。"
            "小摩擦少了，彼此也更尊重一点。"
        ),
    )
    _p(
        "Who do you live with?",
        "parents_tidy_home",
        logic="先说现在与室友住，童年曾与父母同住并点名妈妈，补假期回家与父母相处感受。",
        kitHint="对比童年父母家与现在室友；人物必须是父母/室友，不是房间摆设。",
        words={
            "正面回答": ["my roommate now", "my parents when I was young", "family back in my hometown"],
            "来源或举例": ["mum kept our rooms tidy", "dad worked nearby", "holiday visits"],
            "频次": ["every long holiday", "a few times a month by video"],
            "感受": ["warm at parents' home", "independent at dorm", "close to both"],
        },
        sample=(
            "Right now I live with my roommate on campus. "
            "As a child I lived with my parents — my mum mostly kept our rooms tidy and my dad worked nearby. "
            "I go back to see them every long holiday. "
            "The dorm feels independent, but I still feel close to my family."
        ),
        sampleZh=(
            "现在我与室友住在学校。"
            "小时候和父母住，妈妈主要收拾房间，爸爸在附近上班。"
            "每个长假期都会回去看他们。"
            "宿舍让我更独立，但和家人的联系仍然很近。"
        ),
    )

    # --- Which room in your home do you like best? (xihao) ---
    _p(
        "Which room in your home do you like best?",
        "dorm_apartment_life",
        logic="先点名最喜欢的房间/角落，再讲原因与常用时间，补频率与放松感受。",
        kitHint="必须答具体房间：书桌角、阳台等，不能把「整栋宿舍」当房间名。",
        words={
            "正面回答": ["the desk corner", "our little balcony", "the quiet side by the window"],
            "原因或时间": ["good light for reading", "after evening classes", "me time"],
            "频次": ["most evenings", "whenever I stay in"],
            "感受": ["loose and comfortable", "my own little space", "helps me unwind"],
        },
        sample=(
            "I like the desk corner by the window best — it's my own little space in the dorm. "
            "The light is good for reading after evening classes, so I can have some me time. "
            "I'm there most evenings when I don't go out. "
            "It feels loose and comfortable, and helps me unwind."
        ),
        sampleZh=(
            "我最喜欢窗边的书桌角，在宿舍里算我的小天地。"
            "傍晚课后光线适合看书，能有点自己的时间。"
            "不出去的话大多数晚上都在那儿。"
            "松弛舒服，也能缓一缓。"
        ),
    )
    _p(
        "Which room in your home do you like best?",
        "parents_tidy_home",
        logic="先说童年家里最喜欢的房间（如客厅/自己卧室），再讲妈妈收拾得干干净净的原因，补周末与温馨感受。",
        kitHint=" childhood 家的具体房间；整洁父母素材可作背景，房间名仍要清楚。",
        words={
            "正面回答": ["my bedroom at home", "the small living room", "the tidy side of our flat"],
            "原因或时间": ["mum kept it calm", "quiet on Sunday mornings", "childhood memories"],
            "频次": ["every time I visit", "on holidays at home"],
            "感受": ["warm", "organised", "relaxed"],
        },
        sample=(
            "I like my bedroom at my parents' place best, though I live on campus now. "
            "My mum always kept it calm and organised, so Sunday mornings there felt quiet. "
            "I still sleep there whenever I visit on holidays. "
            "It feels warm and relaxed, with childhood memories."
        ),
        sampleZh=(
            "我最喜欢我父母家的卧室，虽然平时住学校。"
            "妈妈总把那儿收拾得安静整齐，周日早上特别静。"
            "放假回家还是睡那间。"
            "温馨放松，也有很多童年记忆。"
        ),
    )
    _p(
        "Which room in your home do you like best?",
        "tidy_desk_habit",
        logic="直接答最喜欢书桌区，解释收拾干净才好学习，补每晚整理频率与专注感受。",
        kitHint="「书桌角/学习区」是合法房间答案；紧扣喜好与使用习惯。",
        words={
            "正面回答": ["the desk area", "my study corner", "where my laptop sits"],
            "原因或时间": ["a clear desk helps", "before homework every night", "less clutter"],
            "频次": ["every evening before study", "weekend mornings too"],
            "感受": ["practical", "easier to focus", "less stressed"],
        },
        sample=(
            "I like the desk area in our dorm best — it's basically my study corner. "
            "A clear desk helps me focus, so I put things away before homework every night. "
            "I tidy it every evening and sometimes on weekend mornings. "
            "I feel less stressed and it's practical for long assignments."
        ),
        sampleZh=(
            "最喜欢宿舍的书桌区，算我的学习角。"
            "桌面干净更好集中，所以每晚写作业前都会收一收。"
            "晚上基本都会整理，周末早上有时也会。"
            "压力小一点，写长作业也更顺手。"
        ),
    )

    # --- What kind of home would you like to have in the future? (xihao) ---
    _p(
        "What kind of home would you like to have in the future?",
        "dorm_apartment_life",
        logic="先描述理想住所类型与位置，再讲安静、近地铁等原因，补毕业后设想与期待感受。",
        kitHint="未来家：租房/小公寓近地铁，从 dorm 生活自然延伸。",
        words={
            "正面回答": ["a small rented flat", "near the subway", "a quiet residential area"],
            "原因或时间": ["after graduation", "easier commute", "a bit more space"],
            "频次": ["maybe in a few years", "when I start working"],
            "感受": ["independent", "practical", "comfortable"],
        },
        sample=(
            "I'd like a small rented flat near the subway in a quiet residential area. "
            "After graduation an easier commute matters, and I'd want a bit more space than a dorm. "
            "Maybe in a few years when I start working. "
            "It sounds independent, practical and comfortable."
        ),
        sampleZh=(
            "希望以后租一间离地铁近的小公寓，在安静的居民区。"
            "毕业后通勤很重要，也想比宿舍宽敞一点。"
            "大概几年后工作时会考虑。"
            "那样会更独立、实用也舒服。"
        ),
    )
    _p(
        "What kind of home would you like to have in the future?",
        "tidy_desk_habit",
        logic="先说要带书房/书桌的家，再解释整洁工作区的原因，补日常整理习惯与效率感受。",
        kitHint="未来家可强调「有书桌的书房」；仍是 home 题，不是纯整洁题。",
        words={
            "正面回答": ["a flat with a proper desk", "a small study room", "enough shelves"],
            "原因或时间": ["study and work from home", "keep things in order", "after university"],
            "频次": ["daily when I work", "evenings for side projects"],
            "感受": ["comfortable", "organised", "less messy"],
        },
        sample=(
            "I'd like a flat with a proper desk or even a small study corner, not just a bed and a chair. "
            "I may study or work from home after university, so I want shelves to keep things in order. "
            "I'd use it every day for notes and homework. "
            "A tidy corner would feel comfortable and less messy."
        ),
        sampleZh=(
            "希望以后住的公寓能有一张像样的书桌，甚至一小块学习角，而不是只有床和椅子。"
            "大学毕业后可能在家学习或工作，需要柜子把东西收整齐。"
            "每天都会用来看笔记和作业。"
            "整齐的一角会更舒服，也少乱糟糟的。"
        ),
    )
    _p(
        "What kind of home would you like to have in the future?",
        "parents_tidy_home",
        logic="先说想离父母不远的小家，再提干净温馨像童年家，补假期相聚频率与踏实感受。",
        kitHint="父母家记忆软化描绘「温馨整洁」，未来家仍是你自己的住所设想。",
        words={
            "正面回答": ["a small place not too far from parents", "clean and cosy", "my own flat"],
            "原因或时间": ["visit on weekends", "childhood home felt calm", "balance independence and family"],
            "频次": ["maybe Sunday lunch together", "long holidays at their place"],
            "感受": ["warm", "settled", "not too lonely"],
        },
        sample=(
            "I'd like my own small flat, not too far from my parents' hometown. "
            "A clean, cosy place would remind me of how calm their home felt when I was a child. "
            "I'd visit for Sunday lunch sometimes and stay longer in holidays. "
            "That balance feels warm and settled, not too lonely."
        ),
        sampleZh=(
            "想有自己的小公寓，离父母老家别太遠。"
            "干净温馨一点，像小时候家里那种安稳的感觉。"
            "也许周日一起吃午饭，长假多待几天。"
            "独立和亲情兼顾，踏实又不孤单。"
        ),
    )

    # --- What do you usually do at home in the evenings? (xingwei) ---
    _p(
        "What do you usually do at home in the evenings?",
        "dorm_apartment_life",
        logic="先概括晚上在家做什么，再讲原因与时间线（课后回宿舍），补习惯影响与放松感受。",
        kitHint="晚间宿舍生活：作业、聊天、简单做饭，扣「在家」而非外出通勤。",
        words={
            "正面回答": ["stay in the dorm", "homework and relax", "sometimes cook"],
            "原因": ["tired after classes", "save money", "quiet time"],
            "时间线+行为描述": ["come back around six", "shower, eat, then review notes", "chat with roommate"],
            "影响": ["keeps the day steady", "some me time", "ready for tomorrow"],
        },
        sample=(
            "I usually stay in the dorm in the evenings. "
            "I'm often tired after classes, so I save money and enjoy quiet time instead of going out. "
            "I come back around six, shower, eat something simple, review notes and chat with my roommate. "
            "It keeps my day steady and leaves me ready for tomorrow."
        ),
        sampleZh=(
            "晚上我多半待在宿舍。"
            "上完课挺累，也想省点钱，就在宿舍安静待着。"
            "大概六点回来，洗澡吃饭，看看笔记，和室友聊几句。"
            "一天节奏稳，也为明天做好准备。"
        ),
    )
    _p(
        "What do you usually do at home in the evenings?",
        "tidy_desk_habit",
        logic="先说晚上先收拾书桌再学习，再讲怕杂物分心的原因，补每晚流程与专注影响。",
        kitHint="收拾书桌是晚间行为的一部分，主答仍是「晚上在家做什么」。",
        words={
            "正面回答": ["tidy then study", "clear the desk first", "short break after dinner"],
            "原因": ["clutter distracts me", "roommate agreed", "easier to start homework"],
            "时间线+行为描述": ["after dinner about seven", "put books in boxes", "then one or two hours of study"],
            "影响": ["focus faster", "fewer conflicts", "sleep with a clear mind"],
        },
        sample=(
            "In the evening I usually tidy the desk and then study. "
            "Clutter distracts me, and my roommate agreed we should clear it first. "
            "After dinner, around seven, I put books in boxes and study for one or two hours. "
            "I focus faster and go to sleep with a clearer mind."
        ),
        sampleZh=(
            "晚上我通常先收拾书桌再学习。"
            "东西乱我会分心，室友也同意先清桌面。"
            "晚饭后大概七点，把书放进箱子，学一两个小时。"
            "更容易进入状态，睡前心里也清爽些。"
        ),
    )
    _p(
        "What do you usually do at home in the evenings?",
        "parents_tidy_home",
        logic="先说现在宿舍晚间学习与休息，对比童年在家帮妈妈收玩具，补假期在家晚间习惯与温馨影响。",
        kitHint="父母整理仅作童年晚间小事对比；当前答案仍是宿舍晚间 routine。",
        words={
            "正面回答": ["study and rest in the dorm", "on holidays help a bit at home", "watch something light"],
            "原因": ["assignments due", "childhood habit of small chores", "wind down"],
            "时间线+行为描述": ["evenings on campus: notes then videos", "at parents' home: put things away after dinner"],
            "影响": ["keeps family calm", "feels responsible", "relaxed before bed"],
        },
        sample=(
            "On campus I usually study a bit and then watch something light in the evening. "
            "At my parents' place on holidays I still put small things away after dinner, like I did as a kid when Mum asked me to. "
            "That old habit keeps their home calm, and I feel responsible. "
            "Either way I can relax properly before bed."
        ),
        sampleZh=(
            "在学校晚上一般会学一会儿，再看看轻松的视频。"
            "放假在父母家饭后还是会收拾小东西，像小时候妈妈让我收玩具那样。"
            "家里更清静，我也觉得有担当。"
            "不管怎样，睡前都能好好放松。"
        ),
    )

    # --- How is your home different from the one you lived in as a child? (duibi) ---
    _p(
        "How is your home different from the one you lived in as a child?",
        "dorm_apartment_life",
        logic="先总述现在宿舍与童年家的不同，再分述宿舍特点与父母家特点，补个人感受。",
        kitHint="对比「现在 flat/dorm」与「童年 house/家」；人物与空间都要点到。",
        words={
            "正面回答": ["quite different", "dorm now, family house before", "smaller but mine"],
            "选项1的特点与作用": ["campus dorm with roommate", "independent", "near class"],
            "选项2的特点与作用": ["parents' house", "more space", "family meals together"],
            "个人感受": ["freer now", "still miss home", "both suit their time"],
        },
        sample=(
            "It's quite different — I live in a campus dorm with a roommate now, but I grew up in my parents' house. "
            "The dorm is smaller and nearer class, so I feel freer and more independent day to day. "
            "Their house had more space and we always had family meals together. "
            "I still miss that warmth, but both homes suit their time in my life."
        ),
        sampleZh=(
            "很不一样——现在和室友住宿舍，小时候在父母家。"
            "宿舍更小、离课近，日常更自由独立。"
            "以前房子大，一家人经常一起吃饭。"
            "我还是会想家的温馨，但两个阶段都挺适合当时的我。"
        ),
    )
    _p(
        "How is your home different from the one you lived in as a child?",
        "tidy_desk_habit",
        logic="先答整体不同，再比「现在自己收书桌」与「童年家里较整齐」，补感受。",
        kitHint="整洁差异是对比的一个维度，仍要描述两处「家」本身。",
        words={
            "正面回答": ["I manage my own desk now", "Mum handled more before", "dorm vs childhood bedroom"],
            "选项1的特点与作用": ["roommate and shared desk", "tidy every night", "student life"],
            "选项2的特点与作用": ["parents' home", "mum cleaned more", "calmer weekends"],
            "个人感受": ["more responsible", "sometimes messy", "proud when it's clear"],
        },
        sample=(
            "My home today is a dorm with a shared desk, while childhood was my own bedroom at my parents' place. "
            "Now I tidy every night with my roommate; back then Mum handled most of the cleaning. "
            "The dorm fits busy student life; their place felt calmer on weekends. "
            "I'm more responsible now, and proud when the desk stays clear."
        ),
        sampleZh=(
            "现在是和室友共用书桌的宿舍，小时候是父母家的独立卧室。"
            "如今每晚和室友一起收；那时大多是妈妈打扫。"
            "宿舍配繁忙学业；老家周末更宁静。"
            "我现在更负责，桌面干净时也挺有成就感。"
        ),
    )
    _p(
        "How is your home different from the one you lived in as a child?",
        "parents_tidy_home",
        logic="先概括从父母家到宿舍的变化，再对比妈妈打理的家与自己独立住，补情感感受。",
        kitHint="父母整理视角突出「谁收拾」变化，但两个问题选项仍是两个「家」。",
        words={
            "正面回答": ["from parents' tidy house to dorm", "less help now", "more choices myself"],
            "选项1的特点与作用": ["dorm with roommate", "cook simple meals", "no parents nearby"],
            "选项2的特点与作用": ["mum kept rooms neat", "dad at home evenings", "family routine"],
            "个人感受": ["grown up", "occasionally homesick", "grateful for both"],
        },
        sample=(
            "Today I live in a dorm with a roommate and no parents nearby; as a child I was in my mum's tidy house with my dad home in the evenings. "
            "We cook simple meals ourselves now, while back then family routine meant Mum kept everything neat and we ate together. "
            "I feel more grown up, though sometimes a bit homesick. "
            "I'm grateful for both stages."
        ),
        sampleZh=(
            "现在和室友住宿舍，父母不在身边；小时候住在妈妈收拾得很整齐的家，爸爸晚上也常在家。"
            "如今自己煮简单饭，那时妈妈操持家务，一家人一起吃饭。"
            "觉得更长大了，偶尔也会想家。"
            "两个阶段我都很感激。"
        ),
    )