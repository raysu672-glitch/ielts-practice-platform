# -*- coding: utf-8 -*-
"""Shoes Freestyle packs."""


def register(_p):
    _p(
        "What kind of shoes do you wear most often?",
        "campus_sneakers",
        logic="先答最常穿的鞋型，举例舒适球鞋，补工作日频率与脚感感受。",
        kitHint="舒适球鞋：校园通勤为核心。",
        words={
            "正面回答": ["Comfortable sneakers", "Simple trainers", "Most days"],
            "来源或举例": ["a pair my parents bought", "soft soles for walking"],
            "频次": ["every weekday on campus", "when I commute"],
            "感受": ["loose and comfortable", "practical", "no sore feet"],
        },
        sample=(
            "I wear comfortable sneakers most often — simple trainers with soft soles for walking. "
            "My parents bought me a reliable pair before a busy school term. "
            "I put them on every weekday on campus and when I commute. "
            "They feel loose and comfortable, and my feet don't get sore."
        ),
        sampleZh=(
            "最常穿舒服的运动鞋——鞋底软、适合走路的板鞋。"
            "爸妈在忙学期前给我买过一双靠谱的。"
            "平日上学、通勤每天都穿。"
            "宽松舒服，脚也不会酸。"
        ),
    )
    _p(
        "What kind of shoes do you wear most often?",
        "style_shoes_weekend",
        logic="先答工作日与周末分别穿什么，补频率与不同场合感受。",
        kitHint="周末好看鞋：平日仍球鞋为主，周末鞋是补充细节。",
        words={
            "正面回答": ["Sneakers on weekdays", "Stylish pair at weekends", "Depends on plans"],
            "来源或举例": ["roommate's suggestion", "city-centre shopping trips"],
            "频次": ["sneakers most days", "nicer shoes when I hang out"],
            "感受": ["comfort daily", "happy on weekends", "balanced"],
        },
        sample=(
            "On weekdays I still wear sneakers most often for walking around campus. "
            "At weekends I sometimes change to a slightly stylish pair when I hang out in the city centre. "
            "Sneakers win on busy days; the nicer shoes come out maybe once or twice a week. "
            "That balance keeps me comfortable but still lets me dress up a little."
        ),
        sampleZh=(
            "工作日还是最常穿球鞋在校园走。"
            "周末去市中心玩有时会换一双好看一点的。"
            "忙的日子一定是球鞋；时髦些的鞋大概一周一两次。"
            "既舒服，偶尔也能打扮一下。"
        ),
    )
    _p(
        "What kind of shoes did you wear as a child?",
        "campus_sneakers",
        logic="先答童年鞋型，再连父母选购与现在球鞋习惯，补频率与舒服感受。",
        kitHint="童年可与现在舒适路线一脉相承。",
        words={
            "正面回答": ["School shoes and sneakers", "Parents chose", "Mostly practical"],
            "来源或举例": ["white sneakers for PE", "sturdy school shoes"],
            "频次": ["every school day", "for sports class too"],
            "感受": ["safe for running", "comfortable enough", "not fashion-focused"],
        },
        sample=(
            "As a child I mostly wore sturdy school shoes on weekdays and simple sneakers for PE. "
            "My parents usually chose them — they cared more about fit than fashion. "
            "I wore those almost every school day. "
            "They felt safe for running and comfortable enough, even if they weren't trendy."
        ),
        sampleZh=(
            "小时候平日多是结实的皮鞋，体育课穿简单球鞋。"
            "多半是父母挑的，看重合脚胜过好看。"
            "差不多天天上学都穿。"
            "跑步稳、也够舒服，就是不潮。"
        ),
    )
    _p(
        "What kind of shoes did you wear as a child?",
        "style_shoes_weekend",
        logic="先答童年鞋，对比当时学校鞋与后来想要的款式，补频率与感受。",
        kitHint="可提小时候也以舒适鞋为主，长大才在意周末款式。",
        words={
            "正面回答": ["Plain school shoes", "Later wanted nicer ones", "Childhood was practical"],
            "来源或举例": ["uniform rules", "festival shoes occasionally"],
            "频次": ["school shoes daily", "special shoes rarely"],
            "感受": ["practical", "a bit plain", "happy on rare dress-up days"],
        },
        sample=(
            "As a child I mainly wore plain school shoes because of uniform rules. "
            "I only had slightly nicer shoes for festivals or family photos — not very often. "
            "So practically every school day was the same practical pair. "
            "They felt a bit plain, but I was happy on those rare dress-up days."
        ),
        sampleZh=(
            "小时候主要是朴素的校鞋，校服规定那样。"
            "过节或拍全家福才会穿稍好看一点的，很少。"
            "上学日子基本天天同一双实用的鞋。"
            "有点单调，但那种偶尔打扮的日子很开心。"
        ),
    )
    _p(
        "Do you like buying shoes?",
        "campus_sneakers",
        logic="先答喜不喜欢买鞋，说明偏好舒适实用，补购买频率与省心感受。",
        kitHint="舒适向：不爱频繁买，重耐穿。",
        words={
            "正面回答": ["Not really", "Only when needed", "Comfort first"],
            "原因或时间": ["sneakers last a long time", "busy with study"],
            "频次": ["once or twice a year", "when soles wear out"],
            "感受": ["practical", "not stressful", "saves money"],
        },
        sample=(
            "Not really — I only buy shoes when I really need a new pair. "
            "Good sneakers last a long time, and I'm usually busy with study anyway. "
            "I might shop once or twice a year, when the soles wear out. "
            "It feels practical, not stressful, and it saves money."
        ),
        sampleZh=(
            "不太喜欢——真要换才买。"
            "好球鞋能穿很久，平常也忙学习。"
            "一年也就买一两次，鞋底磨坏了再说。"
            "挺务实，不费神，也省钱。"
        ),
    )
    _p(
        "Do you like buying shoes?",
        "style_shoes_weekend",
        logic="先答是否喜欢买鞋，周末款带来一点乐趣，补频率与心情感受。",
        kitHint="周末好看鞋让「买鞋」有一点兴趣但不沉迷。",
        words={
            "正面回答": ["Sometimes", "For weekends", "A little enjoyable"],
            "原因或时间": ["hanging out with friends", "trying on nicer designs"],
            "频次": ["a few times a year", "when there are sales"],
            "感受": ["fun but not addictive", "makes weekends special"],
        },
        sample=(
            "Sometimes — I don't love shoe shopping, but picking a stylish weekend pair can be fun. "
            "Usually a roommate or friend comes along when we hang out near the mall. "
            "I only do it a few times a year, often when there are sales. "
            "It's enjoyable but not addictive, and it makes weekends feel a bit special."
        ),
        sampleZh=(
            "有时——不算爱逛鞋店，但挑一双周末穿得好看的还挺开心。"
            "一般室友或朋友一起去商场附近玩时会顺路看。"
            "一年也就几次，常有打折才去。"
            "好玩但不上头，也让周末有点仪式感。"
        ),
    )
    _p(
        "What is your favourite type of shoes?",
        "campus_sneakers",
        logic="先答最爱鞋型，再讲舒适原因，补穿着频率与脚感感受。",
        kitHint="最爱=舒适球鞋，与素材一致。",
        words={
            "正面回答": ["Sneakers", "Light trainers", "Comfort above all"],
            "原因或时间": ["long walks on campus", "since my parents bought a good pair"],
            "频次": ["almost every day", "for sports too"],
            "感受": ["supportive", "easy to match clothes", "reliable"],
        },
        sample=(
            "My favourite type is sneakers — light trainers that are easy to walk in all day. "
            "I prefer them because campus involves long walks between classes. "
            "I wear them almost every day, even for light sports. "
            "They feel supportive, match most clothes, and stay reliable."
        ),
        sampleZh=(
            "最喜欢运动鞋——轻便、能走一整天那种。"
            "校园上课来回走很远，所以偏爱这个。"
            "几乎天天穿，轻度运动也穿。"
            "支撑好、好搭配，也一直耐穿。"
        ),
    )
    _p(
        "What is your favourite type of shoes?",
        "style_shoes_weekend",
        logic="先答最爱类型（分场景），平日球鞋周末稍有型，补频率与心情感受。",
        kitHint="最爱可「分场景」但仍先回答 favourite 逻辑。",
        words={
            "正面回答": ["Sneakers for weekdays", "Cleaner leather or canvas for weekends", "Depends"],
            "原因或时间": ["comfort on busy days", "want to look neat when I go out"],
            "频次": ["sneakers daily", "stylish pair on outings"],
            "感受": ["comfortable routine", "confident on weekends"],
        },
        sample=(
            "If I have to choose, I still love sneakers for daily life, "
            "but my favourite 'dress-up' type is a cleaner canvas or leather pair for weekends. "
            "Weekdays need comfort; going out with friends I want to look a bit neater. "
            "So sneakers are daily, and the stylish ones appear on outings — that mix makes me feel confident."
        ),
        sampleZh=(
            "硬要选的话，日常生活还是最爱球鞋，"
            "但周末最爱干净一点的帆布或皮质款。"
            "平日要舒服，跟朋友外出想利落些。"
            "所以平日球鞋、外出好看鞋——这样我比较有自信。"
        ),
    )
    _p(
        "How often do you buy new shoes?",
        "campus_sneakers",
        logic="先答购买频率，再讲球鞋耐穿原因，补时间线与省钱影响。",
        kitHint="舒适球鞋耐穿 → 低频购买。",
        words={
            "正面回答": ["Not very often", "Once or twice a year", "When worn out"],
            "原因": ["quality sneakers last", "don't chase fashion"],
            "时间线+行为描述": ["check soles after a term", "order online or at a mall"],
            "影响": ["saves money", "less decision fatigue", "feet stay used to one pair"],
        },
        sample=(
            "Not very often — maybe once or twice a year when my sneakers are clearly worn out. "
            "I don't chase fashion, and a decent pair can last a full term or more. "
            "After exams I usually check the soles, then buy online or at a nearby mall. "
            "It saves money and I don't waste time comparing styles every month."
        ),
        sampleZh=(
            "不常买——一年大概一两次，球鞋明显穿坏了才换。"
            "不追潮流，好一点的能撑一学期甚至更久。"
            "考完试我会看鞋底，再网上或商场买。"
            "省钱，也不用老花时间比款式。"
        ),
    )
    _p(
        "How often do you buy new shoes?",
        "style_shoes_weekend",
        logic="先答频率，区分平日球鞋与周末鞋更换节奏，补行为与预算影响。",
        kitHint="两双逻辑：球鞋慢换，周末鞋稍快。",
        words={
            "正面回答": ["Sneakers rarely", "Weekend shoes sometimes", "A few times a year"],
            "原因": ["weekday comfort is priority", "weekend style is extra"],
            "时间线+行为描述": ["replace sneakers when old", "pick a new weekend pair in sales season"],
            "影响": ["balanced spending", "feet stay comfortable", "weekends feel fresher"],
        },
        sample=(
            "I replace everyday sneakers slowly — only when they're old, so that might be once a year. "
            "For a slightly stylish weekend pair I sometimes shop in the sales season with friends. "
            "Overall I'd buy new shoes a few times a year at most, not every month. "
            "That keeps spending balanced, my feet comfortable, and weekends feeling a bit fresher."
        ),
        sampleZh=(
            "平时球鞋换得慢——旧了才换，大概一年一双。"
            "周末好看一点的鞋有时会趁打折季跟朋友去买。"
            "加起来一年最多买几次，不会月月买。"
            "花费均衡，脚也舒服，周末还有点新意。"
        ),
    )
    _p(
        "Which matters more to you in a pair of shoes, comfort or style?",
        "style_shoes_weekend",
        logic="先正面表态，再分别说舒适与好看的用处，强调分场景但表态清晰。",
        kitHint="周末鞋套装也要诚实对比：平日舒适周末可看重一点 style。",
        words={
            "正面回答": ["Comfort on weekdays", "Style matters a bit at weekends", "It depends"],
            "选项1的特点与作用": ["comfort: long walks and classes", "protects feet all week"],
            "选项2的特点与作用": ["style: cleaner look when hanging out", "boosts confidence briefly"],
            "个人感受": ["comfort wins overall", "style is a weekend bonus"],
        },
        sample=(
            "Overall comfort matters more, especially on weekdays with long walks between classes. "
            "Comfortable sneakers protect my feet all week, so I won't trade that for fashion daily. "
            "Style still has a role — a cleaner pair can boost my confidence when I hang out at weekends. "
            "So comfort wins overall, and style is more like a weekend bonus for me."
        ),
        sampleZh=(
            "总的来说舒适更重要，工作日上课走来走去尤其如此。"
            "舒服的球鞋能护脚一整周，我不会天天拿好看换这个。"
            "好看也有用——周末出门一双利落的鞋会让我自信一点。"
            "所以整体还是舒适优先，好看算周末加成。"
        ),
    )
    _p(
        "Which matters more to you in a pair of shoes, comfort or style?",
        "campus_sneakers",
        logic="明确舒适优先，再对比好看鞋的局限，补个人坚定感受。",
        kitHint="舒适球鞋套装：comfort clearly wins，仍要写 style 一侧。",
        words={
            "正面回答": ["Comfort, definitely", "Style is secondary", "No doubt"],
            "选项1的特点与作用": ["comfort: soft soles and support", "keeps me active without pain"],
            "选项2的特点与作用": ["style: looks sharper but can hurt", "fine for short outings only"],
            "个人感受": ["I choose sneakers first", "uncomfortable shoes ruin the day"],
        },
        sample=(
            "Comfort matters more to me, definitely. "
            "Soft soles and good support let me walk around campus without pain — that's essential. "
            "Stylish shoes can look sharper, but tight or hard ones ruin my day after an hour. "
            "I pick sneakers first, and I only accept style when the pair still feels OK on my feet."
        ),
        sampleZh=(
            "对我来说绝对是舒适更重要。"
            "软底、支撑好才能在校园走一天不难受——这是刚需。"
            "好看的鞋是利落，但挤脚或硬的一小时就毁一天。"
            "我先选球鞋，只有脚上也舒服时才接受一点款式。"
        ),
    )