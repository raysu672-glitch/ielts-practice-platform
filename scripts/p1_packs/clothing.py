# -*- coding: utf-8 -*-
"""Clothing Freestyle packs."""


def register(_p):
    _p(
        "Who chose your clothes when you were a child?",
        "campus_tee_coat",
        logic="先点明主要是父母选，再举例 T 恤外套，补频率与当时感受。",
        kitHint="童年谁选衣：必须先出现 parents/mum。",
        words={
            "正面回答": ["My parents", "Mostly my mum", "They decided"],
            "来源或举例": ["simple t-shirts", "a coat for cold days", "easy campus outfits"],
            "频次": ["every new school term", "when I grew taller"],
            "感受": ["practical", "warm enough", "not much choice"],
        },
        sample=(
            "My parents chose most of my clothes, especially my mum. "
            "She picked simple t-shirts and a coat for cold mornings before school. "
            "That happened every new term, or when I grew taller and needed bigger sizes. "
            "It felt practical and warm enough, though I didn't have much say."
        ),
        sampleZh=(
            "主要是父母选，尤其是我妈。"
            "她给我挑简单的 T 恤，天冷再加外套上学。"
            "每个新学期或长高要换码时都会买。"
            "很实用也够暖和，就是没什么发言权。"
        ),
    )
    _p(
        "Who chose your clothes when you were a child?",
        "campus_sweatshirt",
        logic="先答父母做主，再举例卫衣外套，补换衣频率与舒服感受。",
        kitHint="卫衣套装仍先 parents 出场。",
        words={
            "正面回答": ["My parents did", "Dad for sizes", "Mum for style"],
            "来源或举例": ["a sweatshirt", "thick coat", "campus casual look"],
            "频次": ["in cooler months", "before middle school started"],
            "感受": ["warm", "loose", "easy to put on"],
        },
        sample=(
            "My parents did — my dad checked sizes and my mum chose the style. "
            "They bought me a sweatshirt and a thicker coat when I started middle school. "
            "In cooler months they updated things when the old clothes were too small. "
            "Everything felt warm, loose, and easy to put on before I rushed out."
        ),
        sampleZh=(
            "父母选的——我爸看尺码，我妈看款式。"
            "上初中时给我买卫衣和厚一点的外套。"
            "天冷的时候衣服小了就会换。"
            "暖和、宽松，出门前也好穿。"
        ),
    )
    _p(
        "Who chose your clothes when you were a child?",
        "dressing_mirror_home",
        logic="先答童年父母拍板，再提后来对镜试穿，补从少到有发言权的感受。",
        kitHint="穿衣镜题也要先 parents，镜子是长大后的细节。",
        words={
            "正面回答": ["My parents first", "Later I had some say", "Mum still paid"],
            "来源或举例": ["school uniforms", "weekend casual clothes", "mirror checks at home"],
            "频次": ["parents chose until high school", "I tried outfits in my teens"],
            "感受": ["gradual freedom", "still practical", "more confidence later"],
        },
        sample=(
            "When I was young my parents chose everything — my mum bought school and weekend clothes. "
            "I didn't care much until high school, when I started trying outfits in front of a mirror at home. "
            "Even then she still paid, but she'd listen if something didn't fit well. "
            "I slowly got more freedom and a bit more confidence about how I looked."
        ),
        sampleZh=(
            "小时候全是父母定，我妈买上学和周末穿的衣服。"
            "到高中才开始在意，在家镜子前试穿。"
            "还是她付钱，但不合身也会听我的意见。"
            "慢慢有更多自由，对外表也自信一点。"
        ),
    )
    _p(
        "Do you spend a lot of time choosing clothes?",
        "campus_tee_coat",
        logic="先正面答耗时多少，再讲 T 恤外套固定搭配，补出门前频率与省事感受。",
        kitHint="舒适校园穿搭 → 选择时间短。",
        words={
            "正面回答": ["Not really", "A few minutes", "Same basic combo"],
            "来源或举例": ["t-shirt plus coat", "a sweatshirt sometimes", "grab and go"],
            "频次": ["every weekday morning", "before I head to campus"],
            "感受": ["practical", "saves time", "good enough"],
        },
        sample=(
            "Not really — maybe a few minutes on weekdays. "
            "I usually grab a t-shirt and a coat, or a sweatshirt if it's chilly, and that's enough. "
            "Every morning before campus I do the same quick check. "
            "It feels practical, saves time, and still looks good enough for class."
        ),
        sampleZh=(
            "不算——工作日大概几分钟。"
            "一般拿 T 恤加外套，冷就换卫衣，够了。"
            "每天上学前都这样快速看一下。"
            "省事省时，上课也看得过去。"
        ),
    )
    _p(
        "Do you spend a lot of time choosing clothes?",
        "campus_sweatshirt",
        logic="先答花不多时间，再讲看天气选卫衣外套，补频率与温暖实用感受。",
        kitHint="冷天套件：决策点在气温。",
        words={
            "正面回答": ["Only a little", "Weather decides", "Not fashion-focused"],
            "来源或举例": ["sweatshirt layer", "coat for wind", "check the forecast"],
            "频次": ["most cool mornings", "before leaving the dorm"],
            "感受": ["warm", "quick", "no stress"],
        },
        sample=(
            "Only a little. I check the weather, then decide between a sweatshirt and a coat — no long fashion debate. "
            "On cool mornings I spend maybe two or three minutes before I leave the dorm. "
            "That happens most weekdays in autumn and winter. "
            "It's warm, quick, and honestly not stressful."
        ),
        sampleZh=(
            "就一点点。先看天气，再在卫衣和外套里选，不纠结潮流。"
            "凉爽的早上出门前大概两三分钟。"
            "秋冬平日大都这样。"
            "暖和、快，也不纠结。"
        ),
    )
    _p(
        "Do you spend a lot of time choosing clothes?",
        "dressing_mirror_home",
        logic="先答会比别人多几分钟，再讲对镜整理，补出门前频率与得体感受。",
        kitHint="穿衣镜：「花时间」合情合理但仍是快流程。",
        words={
            "正面回答": ["A bit more", "Maybe ten minutes", "Still not hours"],
            "来源或举例": ["full-length mirror", "check collar and sleeves", "quick outfit change"],
            "频次": ["every day before I go out", "when I meet friends"],
            "感受": ["neater", "more confident", "worth the few minutes"],
        },
        sample=(
            "A bit more than my roommates — maybe ten minutes, not hours. "
            "I use the full-length mirror in my room to check collars, sleeves, and whether colours match. "
            "I do that every day before I go out, and a little longer when I meet friends. "
            "It makes me look neater and feel more confident, so the time feels worth it."
        ),
        sampleZh=(
            "比室友多一点点——大概十分钟，不是几小时。"
            "用房间里的全身镜看领口、袖子、颜色搭不搭。"
            "每天出门前都会，见朋友会多看一下。"
            "更利落也更自信，我觉得这时间值得。"
        ),
    )
    _p(
        "What kind of clothes do you like to wear?",
        "campus_tee_coat",
        logic="先答喜欢的类型（休闲舒适），再讲 T 恤外套原因，补穿着频率与感受。",
        kitHint="喜好紧扣 casual campus。",
        words={
            "正面回答": ["Casual clothes", "Comfortable layers", "Simple colours"],
            "原因或时间": ["easy for campus life", "since middle school"],
            "频次": ["almost every weekday", "whenever I am on campus"],
            "感受": ["loose and comfortable", "neat enough", "low maintenance"],
        },
        sample=(
            "I like casual clothes — a simple t-shirt with a coat or sweatshirt when it's cold. "
            "Campus life means a lot of walking, so comfort and layers matter more than fancy brands. "
            "I dress like this almost every weekday. "
            "It feels loose, comfortable, and still neat enough for class."
        ),
        sampleZh=(
            "喜欢休闲的——简单 T 恤，冷天加外套或卫衣。"
            "校园走路多，舒适和能叠穿比名牌重要。"
            "工作日几乎天天这样穿。"
            "宽松舒服，上课也够得体。"
        ),
    )
    _p(
        "What kind of clothes do you like to wear?",
        "campus_sweatshirt",
        logic="先答偏爱卫衣类，再讲保暖方便，补冷天频率与舒服感受。",
        kitHint="卫衣+外套是喜好核心。",
        words={
            "正面回答": ["Sweatshirts", "Loose tops", "A coat when windy"],
            "原因或时间": ["cool mornings on campus", "easy to layer"],
            "频次": ["most days in autumn", "after late-night study"],
            "感受": ["warm", "relaxed", "cozy"],
        },
        sample=(
            "I like sweatshirts and other loose tops, with a coat when it's windy. "
            "Cool mornings on campus can be harsh, and layers are easy to adjust in class. "
            "I wear them most days in autumn and sometimes after late-night study when I'm tired. "
            "They feel warm, relaxed, and a bit cozy."
        ),
        sampleZh=(
            "喜欢卫衣之类宽松上衣，风大再加外套。"
            "校园早晨凉，上课也方便增减。"
            "秋天几乎天天穿，熬夜复习后也常穿。"
            "暖和、放松，有点居家那种舒服。"
        ),
    )
    _p(
        "What kind of clothes do you like to wear?",
        "dressing_mirror_home",
        logic="先答喜欢整洁得体的休闲款，再讲对镜确认后再出门，补频率与自信感受。",
        kitHint="喜欢「看起来整齐」的 casual，镜前确认是习惯。",
        words={
            "正面回答": ["Neat casual clothes", "Clean simple outfits", "Not too formal"],
            "原因或时间": ["I check myself in the mirror", "since I had my own room"],
            "频次": ["daily before heading out", "extra care for meetings"],
            "感受": ["confident", "tidy", "comfortable still"],
        },
        sample=(
            "I like neat casual clothes — clean t-shirts or a sweatshirt, not too formal. "
            "Since I had my own room I've checked outfits in the mirror before heading out. "
            "I do that daily, and I spend a bit more care before meetings or interviews. "
            "I feel confident and tidy, but still comfortable."
        ),
        sampleZh=(
            "喜欢干净利落的休闲——T 或卫衣，不太正式。"
            "有自己房间后出门前都会在镜前看一眼。"
            "每天都这样，开会或面试前会更讲究。"
            "自信也整齐，但还是舒服。"
        ),
    )
    _p(
        "Do you like wearing T-shirts?",
        "campus_tee_coat",
        logic="先正面答喜不喜欢 T 恤，再讲校园与搭配原因，补频率与舒服感受。",
        kitHint="T 恤是 campus_tee_coat 主轴。",
        words={
            "正面回答": ["Yes, I do", "Most of the year", "Easy choice"],
            "原因或时间": ["light for classrooms", "match with a coat easily"],
            "频次": ["almost every weekday", "under a jacket in spring"],
            "感受": ["breathable", "simple", "saves decision time"],
        },
        sample=(
            "Yes, I do — T-shirts are my default on campus for most of the year. "
            "Classrooms can get warm, and a T-shirt pairs easily with a coat when I go outside. "
            "I wear them almost every weekday, sometimes under a light jacket in spring. "
            "They feel breathable and simple, and they save me decision time in the morning."
        ),
        sampleZh=(
            "喜欢——全年大部分时间在学校都靠 T 恤打底。"
            "教室有时热，外面加外套也好搭。"
            "工作日几乎天天穿，春天有时再套薄夹克。"
            "透气省事，早上也不用想太久。"
        ),
    )
    _p(
        "Do you like wearing T-shirts?",
        "campus_sweatshirt",
        logic="先答是否喜欢 T 恤，并与卫衣对比偏好场景，补频率与舒适感受。",
        kitHint="可承认天冷更爱卫衣，但夏天仍爱 T 恤。",
        words={
            "正面回答": ["Yes, in warm weather", "Sweatshirt when cold", "Still a fan"],
            "原因或时间": ["summer and early autumn", "sweatshirt replaces tee in winter"],
            "频次": ["tees on hot days", "sweatshirts most winter weekdays"],
            "感受": ["light and cool", "cozy when layered", "practical"],
        },
        sample=(
            "Yes, I like T-shirts when the weather is warm — summer and early autumn on campus. "
            "In winter I switch to a sweatshirt because it's cozier, but I still keep a few tees for the gym. "
            "So tees on hot days, sweatshirts most winter weekdays. "
            "Both feel practical — light and cool, or warm when layered."
        ),
        sampleZh=(
            "喜欢，天热时穿——夏天和初秋在校园。"
            "冬天改卫衣更暖和，但健身还会穿几件 T。"
            "热天 T 恤，冬天平日多卫衣。"
            "都实用——透气凉快，或叠穿保暖。"
        ),
    )
    _p(
        "Do you like wearing T-shirts?",
        "dressing_mirror_home",
        logic="先答喜欢，再讲镜前看版型颜色，补频率与得体感受。",
        kitHint="喜欢简洁 T，镜前挑哪件。",
        words={
            "正面回答": ["Yes", "Simple plain ones", "Easy to match"],
            "原因或时间": ["quick mirror check", "look clean for class"],
            "频次": ["most days unless very cold", "I rotate a few favourites"],
            "感受": ["neat", "confident", "comfortable"],
        },
        sample=(
            "Yes, I like wearing T-shirts — especially simple plain ones that are easy to match. "
            "I pick between a few favourites after a quick look in the mirror so I look clean for class. "
            "I wear them most days unless it's very cold. "
            "They feel neat, comfortable, and they give me enough confidence before I leave."
        ),
        sampleZh=(
            "喜欢，尤其纯色好搭的那种。"
            "对着镜子挑几件常穿的，上课看着精神。"
            "不太冷的日子大多穿 T。"
            "利落舒服，出门也有底气。"
        ),
    )
    _p(
        "What kind of clothes do you usually wear?",
        "campus_tee_coat",
        logic="先答日常穿着类型，再讲起床到出门行为，补频率与高效影响。",
        kitHint="行为习惯：get dressed 流程。",
        words={
            "正面回答": ["Casual campus wear", "T-shirt and coat", "Same routine"],
            "原因": ["classes and walking", "weather changes quickly"],
            "时间线+行为描述": ["get dressed after breakfast", "grab coat by the door"],
            "影响": ["leave on time", "stay comfortable all day", "less morning stress"],
        },
        sample=(
            "I usually wear casual campus clothes — a t-shirt with a coat or sweatshirt if it's chilly. "
            "After breakfast I get dressed quickly because classes start early. "
            "I grab my coat by the door and head out on foot or by subway. "
            "That routine helps me leave on time, stay comfortable all day, and avoid morning stress."
        ),
        sampleZh=(
            "一般穿校园休闲——T 恤，冷天加外套或卫衣。"
            "早饭后很快穿好，因为课开得早。"
            "门口拿外套，步行或地铁走。"
            "这样不迟到，一整天也舒服，早上也不慌。"
        ),
    )
    _p(
        "What kind of clothes do you usually wear?",
        "campus_sweatshirt",
        logic="先答平时穿卫衣类，再讲冷天出门行为，补频率与保暖影响。",
        kitHint="冷天默认卫衣+外套。",
        words={
            "正面回答": ["Sweatshirt days", "Coat on top", "Casual trainers"],
            "原因": ["mornings are cold", "long hours indoors then outside"],
            "时间线+行为描述": ["pull on a sweatshirt", "add coat before the walk to class"],
            "影响": ["stay warm between buildings", "fewer colds", "focus better in class"],
        },
        sample=(
            "In cool weather I usually wear a sweatshirt with a coat on top and casual trainers. "
            "Mornings are cold, and I move between chilly corridors and windy paths. "
            "I pull on the sweatshirt first, then add the coat before walking to class. "
            "I stay warm between buildings, catch fewer colds, and focus better in class."
        ),
        sampleZh=(
            "凉天通常卫衣外套运动鞋。"
            "早晨冷，走廊和室外风又大。"
            "先套卫衣，走去上课前再加外套。"
            "楼与楼之间不挨冻，感冒少一点，上课也更专注。"
        ),
    )
    _p(
        "What kind of clothes do you usually wear?",
        "dressing_mirror_home",
        logic="先答日常休闲装，再讲镜前整理再出门，补频率与得体影响。",
        kitHint="穿衣镜嵌入出门流程。",
        words={
            "正面回答": ["Simple casual outfits", "Clean and tidy look", "Not formal"],
            "原因": ["want to look presentable", "mirror shows the full picture"],
            "时间线+行为描述": ["stand in front of the mirror", "straighten shirt and check shoes"],
            "影响": ["feel ready for the day", "avoid embarrassing mistakes", "save face in public"],
        },
        sample=(
            "I usually wear simple casual outfits — a t-shirt or sweatshirt, jeans, and sneakers. "
            "I want to look presentable, so I stand in front of the mirror and straighten my shirt before I leave. "
            "That happens every weekday, and I double-check shoes if I'm meeting teachers. "
            "I feel ready for the day and avoid small embarrassing mistakes in public."
        ),
        sampleZh=(
            "平常就是简单休闲——T 或卫衣、牛仔裤、球鞋。"
            "想看着精神点，出门前在镜前拉一下衣服。"
            "工作日每天都这样，见老师还会再看一眼鞋。"
            "觉得准备好出门，公众场合也不容易出糗。"
        ),
    )
    _p(
        "Do you prefer comfortable clothes or fashionable ones?",
        "campus_tee_coat",
        logic="先表态偏舒适，再分别描述舒适与时尚的作用，补个人感受。",
        kitHint="对比类：舒适优先，时尚点到为止。",
        words={
            "正面回答": ["Comfortable clothes", "Fashion is extra", "Clear preference"],
            "选项1的特点与作用": ["comfort: soft fabrics and loose fit", "helps long campus days"],
            "选项2的特点与作用": ["fashionable: sharper look but tighter", "fine for short events"],
            "个人感受": ["I relax in comfy clothes", "trends don't matter daily"],
        },
        sample=(
            "I prefer comfortable clothes, especially for busy campus days. "
            "Soft fabrics and a loose fit help me sit through classes and walk between buildings without feeling squeezed. "
            "Fashionable outfits can look sharper for a short event, but tight styles tire me out quickly. "
            "So I relax in comfy clothes daily, and trends don't matter much to me."
        ),
        sampleZh=(
            "我更偏舒适，尤其是校园忙的日子。"
            "软料宽松，坐课、走路不会绑得难受。"
            "时髦款短时间活动好看，但紧身款很快累。"
            "所以平日放松穿舒服的，潮流不太在意。"
        ),
    )
    _p(
        "Do you prefer comfortable clothes or fashionable ones?",
        "campus_sweatshirt",
        logic="先答舒适优先，对比卫衣实用与追求潮流，补天冷场景感受。",
        kitHint="卫衣素材支撑 comfort wins。",
        words={
            "正面回答": ["Comfort first", "Sweatshirts over trends", "Practical taste"],
            "选项1的特点与作用": ["comfort: warm sweatshirts and coats", "good for cold commutes"],
            "选项2的特点与作用": ["fashionable: slimmer cuts and logos", "look nice but less warm"],
            "个人感受": ["I choose warmth", "style is secondary in winter"],
        },
        sample=(
            "I prefer comfortable clothes — warm sweatshirts and coats win in winter. "
            "They keep me warm on cold commutes and still feel loose in the classroom. "
            "More fashionable slim cuts and big logos can look nice in photos, but they're often less warm. "
            "I choose warmth first, and style is secondary when the weather turns cold."
        ),
        sampleZh=(
            "我更选舒服——冬天卫衣外套优先。"
            "通勤保暖，教室里也宽松。"
            "修身、大 logo 的时髦款拍照好看，但往往不够暖。"
            "天冷我先要暖和，好看排在后面。"
        ),
    )
    _p(
        "Do you prefer comfortable clothes or fashionable ones?",
        "dressing_mirror_home",
        logic="先答在舒适与好看间取平衡，对比两者作用，补镜前整理后的感受。",
        kitHint="镜子用户：comfort base + light fashion check，仍要选边。",
        words={
            "正面回答": ["Comfort base", "A little style", "Balance"],
            "选项1的特点与作用": ["comfort: easy fabrics I wear all day", "no itching or tight waist"],
            "选项2的特点与作用": ["fashionable touches: colour match in the mirror", "look tidy for social life"],
            "个人感受": ["won't suffer for trends", "neat casual is enough"],
        },
        sample=(
            "I start with comfortable clothes — easy fabrics I can wear all day without a tight waist. "
            "Then I add a little style by matching colours in the mirror so I look tidy with friends. "
            "Pure fashion pieces that hurt comfort are a no for me, even if they photograph well. "
            "I won't suffer for trends; neat casual is enough, and the mirror helps me get there quickly."
        ),
        sampleZh=(
            "先从舒服入手——面料省事，腰带不勒。"
            "再在镜子里配一下颜色，跟朋友见面看着整齐。"
            "再好看但不舒服的潮流我不买，拍照再美也不行。"
            "不为追流行吃苦；干净休闲就够，镜子帮我快速搞定。"
        ),
    )