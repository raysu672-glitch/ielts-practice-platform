# -*- coding: utf-8 -*-
"""Watch Freestyle packs (preview-page style)."""


def register(_p):
    _p(
        "Do you wear a watch?",
        "simple_watch_gift",
        logic="先答是否戴表，再交代开学礼物来源、日常佩戴频率与便利感受。",
        kitHint="普通手表礼物：开学收表、抬腕看时间，不用掏手机。",
        words={
            "正面回答": ["Yes, I do", "Most days", "On my left wrist"],
            "来源或举例": ["a simple watch", "start-of-term gift", "from my parents"],
            "频次": ["every school day", "from morning to evening"],
            "感受": ["handy", "quick glance", "less phone distraction"],
        },
        sample=(
            "Yes, I do wear a watch most days. "
            "My parents gave me a simple one at the start of term so I could check the time quickly. "
            "I put it on every school morning and keep it on until I get home. "
            "It is handy because I do not have to pull out my phone in class."
        ),
        sampleZh=(
            "是的，大多数时候我都戴手表。"
            "开学时爸妈送我一块普通表，方便快速看时间。"
            "每个上学日早上戴上，回家才摘。"
            "挺实用，上课也不用掏手机。"
        ),
    )
    _p(
        "Do you wear a watch?",
        "phone_time_check",
        logic="先说不戴表，再说手机看时间习惯与使用场景，最后聊是否打算买表。",
        kitHint="手机看时间：不戴表时用锁屏或状态栏，与戴表题形成第二套答法。",
        words={
            "正面回答": ["Not really", "I use my phone", "No watch on me"],
            "来源或举例": ["lock screen", "quick swipe", "alarm on phone"],
            "频次": ["dozens of times a day", "between classes"],
            "感受": ["good enough for now", "maybe a watch later"],
        },
        sample=(
            "Not really — I do not wear a watch at the moment. "
            "When I need the time, I just glance at my phone lock screen or the corner of the screen. "
            "I probably check it many times a day, especially between classes. "
            "A phone is enough for now, though I might get a simple watch later."
        ),
        sampleZh=(
            "目前一般不戴手表。"
            "要看时间就扫一眼手机锁屏或屏幕角标。"
            "一天看好多次，课间尤其频繁。"
            "眼下手机够用，以后也许会买块简单的表。"
        ),
    )
    _p(
        "Have you ever got a watch as a gift?",
        "simple_watch_gift",
        logic="先肯定收过礼物表，交代谁送的、何时送，再说后来怎么用。",
        kitHint="开学礼物线：父母送表、动机是看时间省事，自然扣「礼物」问法。",
        words={
            "正面回答": ["Yes, I have", "Once", "A proper gift"],
            "来源或举例": ["my parents", "start of the school year", "a plain dial"],
            "频次": ["still wear it", "on weekdays mainly"],
            "感受": ["thoughtful", "useful every day"],
        },
        sample=(
            "Yes, I have. My parents bought me a watch at the start of the school year. "
            "They wanted me to be on time without always checking my phone. "
            "I still wear it on most weekdays. "
            "I thought it was a thoughtful gift, and I use it every day."
        ),
        sampleZh=(
            "有的。开学那年爸妈给我买过一块表。"
            "他们希望我不总看手机也能准时。"
            "工作日大多还戴着。"
            "我觉得礼物很贴心，也确实天天用。"
        ),
    )
    _p(
        "Have you ever got a watch as a gift?",
        "phone_time_check",
        logic="先答没收过表，再举手机或其它小礼物对比，说明自己习惯手机看时间。",
        kitHint="不戴表素材：诚实说无表礼物，用手机替代仍可完整回答本题。",
        words={
            "正面回答": ["No, not a watch", "Never", "Other gifts instead"],
            "来源或举例": ["birthday money", "a phone case", "family dinners"],
            "频次": ["phone for time since junior high"],
            "感受": ["fine without one", "might like one someday"],
        },
        sample=(
            "No, I have never received a watch as a gift. "
            "My family usually gives me things like birthday money or something for my phone. "
            "I have used my phone to tell the time since junior high. "
            "I am fine without a watch, but I would not mind one as a gift someday."
        ),
        sampleZh=(
            "没有，我没收过手表当礼物。"
            "家里通常给红包或手机配件之类。"
            "初二起我就用手机看时间。"
            "没有表也行，以后当礼物送我也可以。"
        ),
    )
    _p(
        "Why do some people wear expensive watches?",
        "simple_watch_gift",
        logic="先概括戴名表的人图什么，再对比自己普通表，最后谈个人看法。",
        kitHint="从「普通表为用」反衬别人要品牌与面子，素材仍是自己戴便宜表的经历。",
        words={
            "正面回答": ["Status", "Fashion", "More than telling time"],
            "来源或举例": ["brand logos", "leather or metal bands", "social media"],
            "频次": ["at work or events", "not every student"],
            "感受": ["understandable", "not my priority"],
        },
        sample=(
            "I think some people wear expensive watches to show status or taste, not just to tell the time. "
            "A big brand on your wrist can make you look successful in meetings or photos. "
            "You see that more with adults at work than with students like me. "
            "I understand it, but my cheap watch is enough for my life."
        ),
        sampleZh=(
            "我觉得有人戴贵表是为了身份和品味，不只是看时间。"
            "手腕上的大牌在开会或拍照里显得「成功」。"
            "职场成年人多，学生里少见。"
            "我能理解，但我便宜的表就够用。"
        ),
    )
    _p(
        "Why do some people wear expensive watches?",
        "phone_time_check",
        logic="先答贵表原因，再举自己用手机看时间作对比，说明年轻人选择不同。",
        kitHint="手机党视角：别人买表当首饰，自己觉得手机计时更自然。",
        words={
            "正面回答": ["Jewellery", "Collecting", "Old habit"],
            "来源或举例": ["smartphones everywhere", "younger generation", "classic designs"],
            "频次": ["daily for some adults", "rare among classmates"],
            "感受": ["different choices", "both OK"],
        },
        sample=(
            "Some people treat an expensive watch like jewellery or a hobby — they enjoy the design and the brand story. "
            "Others grew up wearing a watch every day, so they keep that habit. "
            "Many young people like me just use a phone, so we do not feel the same need. "
            "I think both choices are fine; it depends on lifestyle."
        ),
        sampleZh=(
            "有人把名表当首饰或收藏，喜欢设计和品牌故事。"
            "也有人从小习惯戴表，就一直戴着。"
            "很多年轻人用手机，需求不一样。"
            "两种选择都可以，看生活方式。"
        ),
    )
    _p(
        "Do you think it is important to wear a watch?",
        "simple_watch_gift",
        logic="先表态因人而异，用戴表上课经历举例，再谈守时作用与个人感觉。",
        kitHint="戴普通表：强调课堂抬腕看时间、少打扰，支撑「重要但不必须」。",
        words={
            "正面回答": ["It depends", "Helpful for some", "Not essential"],
            "举例或原因": ["classes and exams", "punctual for buses", "phone rules in school"],
            "作用或影响": ["better time sense", "fewer late arrivals"],
            "感受": ["useful for me", "others manage fine"],
        },
        sample=(
            "I think it depends — a watch can be helpful, but it is not essential for everyone. "
            "For me it is useful in school when teachers do not want phones out all the time. "
            "A quick look at my wrist helps me finish tasks on time and catch the bus. "
            "Still, many people manage perfectly well with a phone only."
        ),
        sampleZh=(
            "因人而异——表有帮助，但不是人人必备。"
            "在学校不能总掏手机时，对我挺有用。"
            "抬腕看一眼能按时做完事、赶上公交。"
            "很多人只用手机也毫无问题。"
        ),
    )
    _p(
        "Do you think it is important to wear a watch?",
        "phone_time_check",
        logic="先说不认为人人都需要表，举手机与闹钟够用，再谈特殊职业才更需要。",
        kitHint="手机看时间：论证日常计时不依赖手表，表对特定人群更重要。",
        words={
            "正面回答": ["Not for everyone", "Phones work", "Situation matters"],
            "举例或原因": ["alarms and calendars", "sport watches for runners", "pilots or nurses"],
            "作用或影响": ["less extra gadget", "miss it if phone dies"],
            "感受": ["comfortable without one", "open to either"],
        },
        sample=(
            "I do not think everyone must wear a watch today. "
            "Most daily planning is on my phone — alarms, calendar, and the clock in the corner. "
            "That works for study and commuting, though a dead battery can be annoying. "
            "Jobs like nursing might still need a proper watch, but students often do fine without."
        ),
        sampleZh=(
            "我不觉得现在人人都得戴表。"
            "日程、闹钟、时钟都在手机上，学习通勤够用。"
            "没电会麻烦，但多数时候没事。"
            "护士等职业也许更需要表，学生往往不戴也行。"
        ),
    )
    _p(
        "Do you think it is important to wear a watch? Why?",
        "simple_watch_gift",
        logic="先给有条件的「重要」，再用自己戴表原因展开，说明为何与手机互补。",
        kitHint="礼物表故事：父母用意+课堂场景，直接回答 Why。",
        words={
            "正面回答": ["Yes, in some situations", "Because of habits", "For quick checks"],
            "举例或原因": ["parents' gift reason", "exam timing", "no phone in class"],
            "作用或影响": ["stay punctual", "look more prepared"],
            "感受": ["glad I wear one", "would feel lost without it"],
        },
        sample=(
            "Yes, I think it can be important, especially if you are in places where phones are distracting or not allowed. "
            "My parents gave me a watch so I would be punctual without staring at a screen. "
            "During exams or tight schedules, one glance is faster and calmer. "
            "That is why I am glad I wear one — I would feel a bit lost without it on school days."
        ),
        sampleZh=(
            "我觉得在有些场合挺重要，尤其不宜总看手机的地方。"
            "爸妈送表就是希望我准时、别老盯着屏幕。"
            "考试或行程紧时，抬腕更快也更稳。"
            "所以上学日戴着心里踏实，没有表会有点慌。"
        ),
    )
    _p(
        "Do you think it is important to wear a watch? Why?",
        "phone_time_check",
        logic="先答对多数人不太重要并说明理由，再承认极端场景手表更好。",
        kitHint="手机为主：Why 落在方便、多功能；表只是补充选项。",
        words={
            "正面回答": ["Not really for me", "Because phones do more", "Optional tool"],
            "举例或原因": ["one device for calls and time", "free maps", "student budget"],
            "作用或影响": ["simpler daily carry", "watch as backup"],
            "感受": ["happy with phone", "no strong need yet"],
        },
        sample=(
            "For me it is not very important, because my phone already tells the time and handles my schedule. "
            "I can set reminders, check buses, and call my family on the same device. "
            "Buying a watch would be an extra cost for something I rarely miss. "
            "I might want one later for sport or style, but I do not feel a strong need now."
        ),
        sampleZh=(
            "对我没那么重要，手机既能看时间又能管日程。"
            "提醒、查车、打电话都在一台设备上。"
            "再买表是多一笔开销，而我很少耽误事。"
            "以后运动或讲究搭配也许会买，眼下需求不强。"
        ),
    )