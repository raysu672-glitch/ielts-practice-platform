# -*- coding: utf-8 -*-
"""Hometown Freestyle packs."""


def register(_p):
    # --- Where is your hometown? (shishi) ---
    _p(
        "Where is your hometown?",
        "hometown_local_food",
        logic="先直接报名字与省份/区域，再轻轻带到老城小吃街作地标，补回去频率与亲切感受。",
        kitHint="地点必须在前：城镇名+方位；小吃只是举例地标，不能整段只聊吃的。",
        words={
            "正面回答": ["a medium-sized city", "in eastern China", "Jiangsu province"],
            "来源或举例": ["near a old breakfast street", "by the river", "a few hours from my university city"],
            "频次": ["two or three times a year", "every long holiday"],
            "感受": ["familiar", "relaxed", "always feels like home"],
        },
        sample=(
            "My hometown is a medium-sized city in Jiangsu, in eastern China. "
            "It's by the river, with an old breakfast street people know well — not far from where I live for university. "
            "I go back two or three times a year on long holidays. "
            "It always feels familiar and relaxed."
        ),
        sampleZh=(
            "家乡是江苏一座中等城市，在华东。"
            "靠着河边，有条大家都熟悉的老早茶街，离我上大学的城市不算远。"
            "一年大概回去两三次，逢长假期。"
            "总是很亲切，人也放松。"
        ),
    )
    _p(
        "Where is your hometown?",
        "canteen_and_takeaways",
        logic="先答城镇位置与离大学距离，食堂/外卖口味仅作「在那边生活过」的轻对比，补回家频率。",
        kitHint="食堂素材不能抢答：where 必须给地名 first；饮食只轻轻带过。",
        words={
            "正面回答": ["a smaller city inland", "north of my campus city", "where I went to school before university"],
            "来源或举例": ["high school canteen there", "night market near the bus station", "home cooking on weekends"],
            "频次": ["every summer holiday", "Spring Festival for sure"],
            "感受": ["slower pace", "nostalgic", "easy to settle in"],
        },
        sample=(
            "My hometown is a smaller inland city north of where I study now. "
            "I went to high school there — we ate at the school canteen on weekdays and the night market near the bus station at weekends. "
            "I return every summer holiday and for Spring Festival. "
            "The pace is slower, and I feel nostalgic but easy to settle in."
        ),
        sampleZh=(
            "家乡是座更靠北的内陆小城，在我现在念书城市的北边。"
            "我高中在那儿上的——平日吃食堂，周末去汽车站旁的夜市。"
            "每年暑假都会回，春节一定回。"
            "节奏慢些，有点怀旧，也很快能重新适应。"
        ),
    )
    _p(
        "Where is your hometown?",
        "family_car_passenger",
        logic="先答家乡在哪个市/县与大概方向，再举例爸妈开车去周边古镇作地理补充，补假期探望频率。",
        kitHint="汽车出行作「周边地名」补充，主答仍是 hometown 位置。",
        words={
            "正面回答": ["a county town", "about three hours by car", "south-west of my university"],
            "来源或举例": ["parents drive to nearby water towns", "high-speed rail also reaches it", "family visits relatives there"],
            "频次": ["every long holiday by car", "sometimes by train"],
            "感受": ["close to family", "peaceful", "good memories on the road"],
        },
        sample=(
            "My hometown is a county town south-west of my university city, about three hours by car or one and a half by high-speed rail. "
            "My parents often drive me to nearby water towns when we visit relatives. "
            "We go by car every long holiday, sometimes by train if tickets are tight. "
            "It feels peaceful and close to family, with good road-trip memories."
        ),
        sampleZh=(
            "家乡是大学所在城市西南方向的一座县城，开车大约三小时，高铁一个半小时左右。"
            "假期爸妈常开车带我去附近水乡走亲戚。"
            "每个长假期基本坐车回，票紧时就坐火车。"
            "很安宁，离家人近，路上也挺多回忆。"
        ),
    )

    # --- What is your hometown best known for? (shishi) ---
    _p(
        "What is your hometown best known for?",
        "hometown_local_food",
        logic="先直接说最有名的（如小吃/早茶），再举具体店舖例子，补游客或当地人频率与自豪感受。",
        kitHint="本地小吃是主素材：最出名可直接答 food。",
        words={
            "正面回答": ["local street food", "breakfast snacks", "a famous rice noodle soup"],
            "来源或举例": ["the old breakfast lane", "families queue on Sundays", "tourists take photos"],
            "频次": ["locals eat daily", "I have it every trip home"],
            "感受": ["proud", "delicious", "part of our identity"],
        },
        sample=(
            "My hometown is best known for local street food, especially a famous rice noodle soup. "
            "On the old breakfast lane families queue on Sunday mornings, and tourists take photos of the steam. "
            "Locals eat there almost daily; I never miss it when I go back. "
            "I'm proud of that taste — it feels part of who we are."
        ),
        sampleZh=(
            "家乡最有名的是街头小吃，尤其那碗米粉汤。"
            "老早点街上周日一早要排队，游客也爱拍热气腾腾的照片。"
            "本地人几乎天天吃；我每次回去必吃。"
            "我为这味道自豪，觉得像我们的名片。"
        ),
    )
    _p(
        "What is your hometown best known for?",
        "canteen_and_takeaways",
        logic="先答出名的是平价美食与夜市，再对比学校食堂与街边小摊，补周末或晚间热闹频率。",
        kitHint="食堂外卖套装：家乡以「吃得实惠热闹」闻名。",
        words={
            "正面回答": ["cheap tasty food", "night market", "student-friendly canteen culture"],
            "来源或举例": ["high school canteen", "takeaways by phone", "snacks after nine p.m."],
            "频次": ["busy every weekend night", "during festivals"],
            "感受": ["lively", "welcoming", "hard to forget the smell"],
        },
        sample=(
            "It's best known for cheap, tasty food — a lively night market and even our high school canteen people still talk about. "
            "Takeaways arrive by phone after nine, and the smell of snacks fills the street on weekends. "
            "It gets busy every weekend night, especially during festivals. "
            "The place feels welcoming and hard to forget."
        ),
        sampleZh=(
            "家乡最有名的是便宜好吃的：热闹的夜市，还有大家还在聊的高中食堂。"
            "晚上九点后人打电话叫外卖，周末街上到处是小吃香味。"
            "每周末晚上都挤，过节更挤。"
            "很有人情味，味道也让人忘不了。"
        ),
    )
    _p(
        "What is your hometown best known for?",
        "family_car_passenger",
        logic="先答周边水乡/短途自驾游出名，再举爸妈开车去的景点，补假期出行频率与放松感受。",
        kitHint="汽车套装：家乡以「周边自驾游」或水乡出名。",
        words={
            "正面回答": ["short road trips", "water towns nearby", "scenic drives"],
            "来源或举例": ["parents drive on holidays", "passengers by the window", "old bridges and rivers"],
            "频次": ["most long holidays", "summer weekends"],
            "感受": ["relaxed", "family time", "good views"],
        },
        sample=(
            "It's best known for short road trips to water towns and rivers nearby. "
            "On holidays my parents drive, and I sit by the window over old bridges — lots of visitors do the same routes. "
            "That happens most long holidays and many summer weekends. "
            "It feels relaxed, with good views and easy family time."
        ),
        sampleZh=(
            "家乡周边出名的是短途自驾和水乡。"
            "假期爸妈开车，我坐在窗边过老桥——不少游客也走这条线。"
            "长假期经常如此，暑假周末也很多。"
            "放松，风景好，也适合一家人。"
        ),
    )

    # --- What do you like most about your hometown? (xihao) ---
    _p(
        "What do you like most about your hometown?",
        "hometown_local_food",
        logic="先答最喜欢家乡味道，再讲原因与儿时记忆，补回家吃的频率与幸福感。",
        kitHint="喜欢什么：local food 可为主线。",
        words={
            "正面回答": ["the food", "familiar breakfast taste", "stalls my parents took me to"],
            "原因或时间": ["memories from growing up", "warm on winter mornings", "every holiday ritual"],
            "频次": ["first thing when I arrive", "twice each trip"],
            "感受": ["happy", "comforted", "recharged"],
        },
        sample=(
            "I like the food in my hometown most — especially the breakfast stall my parents always took me to. "
            "That taste brings back growing up, and it's warm on cold winter mornings. "
            "It's the first thing I eat when I arrive, usually twice each trip. "
            "I feel happy, comforted and recharged for the term."
        ),
        sampleZh=(
            "我最喜欢家乡的味道，尤其是父母常带我去的那家早点。"
            "那口味道连着成长记忆，冬天早晨喝着特别暖。"
            "每次回去第一餐往往就是那儿，一趟大概吃两次。"
            "开心又踏实，开学前能量也回来了。"
        ),
    )
    _p(
        "What do you like most about your hometown?",
        "canteen_and_takeaways",
        logic="先答最喜欢物价亲民、吃喝方便，再举夜市与外卖，补周末和室友追忆学校食堂的感受。",
        kitHint="食堂外卖：喜欢「吃得随性实惠」。",
        words={
            "正面回答": ["affordable food", "easy takeaways", "night market with friends"],
            "原因或时间": ["high school friends", "late snacks", "no stress about budget"],
            "频次": ["every Friday night at home", "when I visit each holiday"],
            "感受": ["relaxed", "social", "like being a student again"],
        },
        sample=(
            "I like how affordable and easy food is in my hometown — the night market and quick takeaways with high-school friends. "
            "We used to buy late snacks on Fridays with no budget stress. "
            "I still do that every visit on holiday weekends. "
            "It feels relaxed and social, like being a student again."
        ),
        sampleZh=(
            "我最喜欢家乡吃得便宜又方便——夜市和跟高中朋友叫外卖。"
            "以前周五晚上买宵夜完全不用纠结钱。"
            "现在放假回去周末还会那样。"
            "轻松又热闹，像回到学生时代。"
        ),
    )
    _p(
        "What do you like most about your hometown?",
        "family_car_passenger",
        logic="先答最喜欢和家人一起出门兜风，再讲车窗风景与聊天，补假期自驾频率与亲密感受。",
        kitHint="汽车套装：喜欢 family trips 氛围。",
        words={
            "正面回答": ["family road trips", "sitting by the window", "short drives to the countryside"],
            "原因或时间": ["parents' jokes in the car", "escape from homework", "harvest season views"],
            "频次": ["most Spring Festival days", "one trip each summer"],
            "感受": ["close to parents", "peaceful", "memories I keep"],
        },
        sample=(
            "I like family road trips in my hometown most — sitting by the window while my parents joke in the car. "
            "Short drives to the countryside let me escape homework stress and see harvest colours. "
            "We do that most Spring Festival days and at least one summer trip. "
            "I feel close to my parents, peaceful, with memories I keep."
        ),
        sampleZh=(
            "我最喜欢家乡一家人开车出去玩，坐在窗边听爸妈车上开玩笑。"
            "去郊外转一圈能躲开作业压力，秋收颜色也好看。"
            "春节大多会出门，暑假至少一次。"
            "跟父母亲近，心里平静，都是很珍藏的回忆。"
        ),
    )

    # --- Would you like to live in your hometown in the future? (xihao) ---
    _p(
        "Would you like to live in your hometown in the future?",
        "hometown_local_food",
        logic="先表明想不想回，再谈工作机会与割舍不了的味道，补毕业后几年设想与纠结感受。",
        kitHint="未来是否回乡：food 作情感砝码，但仍要答愿意/不愿意。",
        words={
            "正面回答": ["Maybe later", "Not right after graduation", "Part of me wants to"],
            "原因或时间": ["more jobs in the big city now", "miss hometown breakfast", "after parents retire"],
            "频次": ["visit often anyway", "maybe in ten years"],
            "感受": ["torn", "practical", "still love the taste"],
        },
        sample=(
            "Maybe later, not right after graduation — there are more jobs in my university city now. "
            "Still, I miss hometown breakfast and part of me wants to be nearer my parents when they retire. "
            "I'd visit often anyway and might move back in about ten years. "
            "I feel torn but practical, and I still love that taste."
        ),
        sampleZh=(
            "以后也许吧，刚毕业应该不会——现在大学这边机会更多。"
            "不过我想家的早点，父母退休我也希望离他们近一些。"
            "反正会常回去，也许十年后真搬回去。"
            "纠结但理性，对家乡味道还是放不下。"
        ),
    )
    _p(
        "Would you like to live in your hometown in the future?",
        "canteen_and_takeaways",
        logic="先说短期不想回，因职业发展；再讲想念便宜吃喝与老朋友，补偶尔长住设想与放松感受。",
        kitHint="外卖食堂：生活成本低是回乡诱惑之一。",
        words={
            "正面回答": ["Not for the first few years", "Open-minded later", "Depends on work"],
            "原因或时间": ["career in a bigger city", "cheap living and friends back home", "remote work maybe"],
            "频次": ["long visits each year", "maybe trial stay after five years"],
            "感受": ["flexible", "nostalgic", "life could be easier there"],
        },
        sample=(
            "I would not live in my hometown for the first few years — I need career steps in a bigger city. "
            "But cheap food, takeaways and old friends make life easier back home, and remote work might change things. "
            "I'll do long visits yearly and maybe a trial stay after five years. "
            "I feel flexible and nostalgic; life there could be simpler."
        ),
        sampleZh=(
            "头几年我不会住回家乡，得在大城市发展职业。"
            "但家乡吃喝便宜、老朋友在，要是能远程上班也许会变。"
            "每年长假多待一阵，五年后也许试住一段时间。"
            "心态开放也挺怀旧，那边生活可能更轻松。"
        ),
    )
    _p(
        "Would you like to live in your hometown in the future?",
        "family_car_passenger",
        logic="先说愿意离父母近一些，但接受先在大城市打拼，再讲开车陪他们出游的愿望，补中长期计划与家庭感受。",
        kitHint="汽车套装：回乡动机含「离父母/家庭出行近」。",
        words={
            "正面回答": ["Yes, eventually", "After some years away", "Closer to my parents"],
            "原因或时间": ["family road trips easier", "help parents as they age", "build career first"],
            "频次": ["see them monthly if I return", "weekend drives to water towns"],
            "感受": ["responsible", "warm", "worth waiting a bit"],
        },
        sample=(
            "Yes, eventually — after a few years building my career elsewhere. "
            "I'd like to live nearer my parents so weekend drives to water towns are easy and I can help as they age. "
            "If I move back I could see them monthly and still do those trips. "
            "It feels responsible and warm, worth waiting a bit."
        ),
        sampleZh=(
            "最终会想回吧，先在外面几年把事业站稳。"
            "离父母近，周末开车去水乡方便，他们年纪大我也好照顾。"
            "回去了能每月见他们，自驾出游也照旧。"
            "觉得有担当也温馨，值得先等几年。"
        ),
    )

    # --- What do people in your hometown usually do at the weekend? (xingwei) ---
    _p(
        "What do people in your hometown usually do at the weekend?",
        "hometown_local_food",
        logic="先概括周末活动，再讲原因与时间线（早茶、夜市），补对氛围的影响与本人喜爱感受。",
        kitHint="行为习惯：本地人周末吃小吃、逛老街。",
        words={
            "正面回答": ["eat out", "walk the old street", "meet relatives for breakfast"],
            "原因": ["familiar taste", "slow Sunday", "social habit"],
            "时间线+行为描述": ["Saturday night market", "Sunday morning tea", "short walk by the river"],
            "影响": ["strong community feel", "happy", "tourists join too"],
        },
        sample=(
            "Most people eat out and stroll at weekends. "
            "Saturday nights go to the night market for snacks; Sunday mornings meet relatives for tea on the old street. "
            "Families often walk by the river after. "
            "It builds a strong community feel, and even tourists join — I always enjoy it when I'm home."
        ),
        sampleZh=(
            "大家周末多半会出去吃、逛逛。"
            "周六晚上逛夜市吃东西，周日早上在老街喝早茶见亲戚。"
            "饭后不少人沿河散步。"
            "社区氛围浓，游客也会来——我回家总觉得开心。"
        ),
    )
    _p(
        "What do people in your hometown usually do at the weekend?",
        "canteen_and_takeaways",
        logic="先答周末逛街吃东西叫外卖，再讲年轻人聚会原因，补行为细节与热闹影响。",
        kitHint="食堂外卖：周末=聚餐+外卖放松。",
        words={
            "正面回答": ["order takeaways", "night market", "karaoke with classmates"],
            "原因": ["no school next day", "cheap options", "hang out"],
            "时间线+行为描述": ["Friday night takeout", "Saturday mall food court", "Sunday family lunch"],
            "影响": ["recharge for the week", "keep friendships", "local shops busy"],
        },
        sample=(
            "Young people often order takeaways, hit the night market or sing karaoke with classmates on weekends. "
            "With no school next day, cheap food helps them hang out and recharge. "
            "Friday night takeout, Saturday food court, Sunday family lunch is a common pattern. "
            "It keeps friendships alive and local shops busy."
        ),
        sampleZh=(
            "年轻人周末常叫外卖、逛夜市或和同学唱K。"
            "第二天不用上课，便宜吃喝也方便聚会、缓口气。"
            "周五外卖、周六商场吃、周日家里聚餐挺常见。"
            "友谊维系得住，小店生意也好。"
        ),
    )
    _p(
        "What do people in your hometown usually do at the weekend?",
        "family_car_passenger",
        logic="先答很多家庭周末开车短途出游，再讲原因与典型路线，补对休息与亲子时间的影响。",
        kitHint="汽车套装：周末短途自驾是 local routine。",
        words={
            "正面回答": ["short car trips", "visit water towns", "picnic in the countryside"],
            "原因": ["good roads", "kids free from school", "fresh air"],
            "时间线+行为描述": ["Saturday morning on the highway", "lunch at a village", "home by dinner"],
            "影响": ["family bonds", "tourism income", "relaxed Monday"],
        },
        sample=(
            "Many families take short car trips at weekends — water towns or countryside picnics. "
            "Good roads and kids free from school push parents to leave Saturday morning and return by dinner. "
            "They lunch in a village, kids play by the river. "
            "It strengthens family bonds, brings tourism income and people feel relaxed on Monday."
        ),
        sampleZh=(
            "很多家庭周末会开车短途出游，去水乡或郊外野餐。"
            "路好、孩子放假，爸妈往往周六早上出发、晚饭前回家。"
            "在村里吃午饭，孩子在河边玩。"
            "增进亲情，也带动旅游，周一精神好一些。"
        ),
    )

    # --- How has your hometown changed since you were a child? (duibi) ---
    _p(
        "How has your hometown changed since you were a child?",
        "hometown_local_food",
        logic="先总说变化大，再对比老街小吃今昔，补个人感受。",
        kitHint="对比：传统小吃街 vs 现在更商化/干净。",
        words={
            "正面回答": ["quite a lot", "cleaner streets", "same taste, new shops"],
            "选项1的特点与作用": ["today: renovated old street", "more tourists", "brighter at night"],
            "选项2的特点与作用": ["childhood: quieter lane", "only locals", "cheaper bowls"],
            "个人感受": ["proud but nostalgic", "glad food stayed", "a bit crowded now"],
        },
        sample=(
            "It has changed quite a lot. "
            "Today the old breakfast street is renovated, brighter at night and packed with tourists, though the soup taste stayed similar. "
            "When I was small it was a quieter lane mainly for locals with cheaper bowls. "
            "I'm proud but nostalgic, glad the food survived though it's more crowded now."
        ),
        sampleZh=(
            "变化挺大的。"
            "如今老早茶街翻新了，夜里更亮，游客多，但汤的味道还算像。"
            "小时候那条街安静，多是本地人，价格也便宜些。"
            "自豪也怀旧，庆幸味道还在，就是现在挤了点。"
        ),
    )
    _p(
        "How has your hometown changed since you were a child?",
        "canteen_and_takeaways",
        logic="先答变化体现在外卖与商超增多，再对比儿时少量选择和现在手机下单，补感受。",
        kitHint="食堂外卖：饮食选择数字化对比。",
        words={
            "正面回答": ["more takeaway apps", "new malls", "school canteen upgraded too"],
            "选项1的特点与作用": ["now: phone orders in minutes", "food courts", "24-hour shops"],
            "选项2的特点与作用": ["before: canteen and a few stalls", "cash only", "closed early"],
            "个人感受": ["convenient", "miss simple nights", "health choices wider"],
        },
        sample=(
            "Eating options changed most — takeaway apps, malls and even our old school canteen got an upgrade. "
            "Now you order on your phone in minutes with food courts open late. "
            "As a child we mostly had the canteen, a few stalls and cash before nine p.m. "
            "It's convenient with wider healthy choices, though I miss those simple nights a bit."
        ),
        sampleZh=(
            "饮食变化最大——外卖软件、商场，连老高中食堂都翻新了。"
            "现在手机几分钟下单，美食广场开到很晚。"
            "小时候多是食堂加几家小摊，九点后用现金。"
            "方便、健康选择也多，但偶尔还是会想念那时简单的夜晚。"
        ),
    )
    _p(
        "How has your hometown changed since you were a child?",
        "family_car_passenger",
        logic="先总说交通与自驾更容易，再对比儿时土路/现在高速，补周末出游方式变化感受。",
        kitHint="汽车套装：路况与自驾频率对比。",
        words={
            "正面回答": ["better roads", "more cars", "easier weekend trips"],
            "选项1的特点与作用": ["now: highway to water towns", "parking lots", "family SUVs common"],
            "选项2的特点与作用": ["childhood: bumpy county roads", "one family car", "shorter trips"],
            "个人感受": ["proud of development", "traffic jams new problem", "still love window views"],
        },
        sample=(
            "Roads and cars changed the weekend routine most. "
            "Now a highway reaches water towns with big parking lots, and many families have SUVs for trips. "
            "When I was little we had one car on bumpy county roads and shorter routes. "
            "I'm proud of the development, though traffic jams are a new problem — I still love the window views."
        ),
        sampleZh=(
            "路况和车子让周末生活变得最不一样。"
            "现在有高速直达水乡，停车场也大，很多家庭都有 SUV 出游。"
            "小时候家里就一辆车，走乡路坑坑洼洼，路程也短。"
            "我为发展自豪，但堵车是新烦恼——我还是爱坐在车窗边看风景。"
        ),
    )