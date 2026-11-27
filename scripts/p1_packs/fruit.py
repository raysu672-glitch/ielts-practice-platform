# -*- coding: utf-8 -*-
"""Fruit and vegetables Freestyle packs."""


def register(_p):
    _p(
        "Which vegetables did you dislike as a child?",
        "fruit_groceries",
        logic="直接点名讨厌的蔬菜（如苦瓜、芹菜），再举例、频次、现在感受。",
        kitHint="必须说出具体蔬菜名；买菜记忆可轻点。",
        words={
            "正面回答": ["Bitter melon", "Celery", "Eggplant"],
            "来源或举例": ["mum's stir-fry", "school lunch tray", "strong smell"],
            "频次": ["most weeks at dinner", "until junior high"],
            "感受": ["gag reflex", "eat some now", "funny memory"],
        },
        sample=(
            "As a child I really disliked bitter melon and celery on my dinner plate. "
            "The bitter taste and strong smell made me push them to the side. "
            "That happened most weeks until junior high. "
            "I can eat a little now, but it is still a funny memory."
        ),
        sampleZh=(
            "小时候很讨厌晚饭里的苦瓜和芹菜。"
            "又苦又冲的味道让我总把菜拨到一边。"
            "初中前几乎每周都会碰上。"
            "现在能吃一点了，想起来还是觉得好笑。"
        ),
    )
    _p(
        "Which vegetables did you dislike as a child?",
        "canteen_and_takeaways",
        logic="点名校食堂出现的光杆芹菜、过多胡萝卜；外卖不是问题核心。",
        kitHint="食堂托盘蔬菜为主，外卖只作偶尔对比。",
        words={
            "正面回答": ["Plain boiled celery", "Too much carrot", "Watery cabbage"],
            "来源或举例": ["school canteen tray", "lunch queue", "steamed not fried"],
            "频次": ["school days often", "less on weekends"],
            "感受": ["boring taste", "healthier now", "understand parents"],
        },
        sample=(
            "I disliked plain boiled celery and piles of carrot from the school canteen. "
            "Lunch trays looked healthy but tasted boring after I queued with classmates. "
            "That was common on school days, less at weekends when mum cooked at home. "
            "I still find canteen celery dull, though I understand why they served it."
        ),
        sampleZh=(
            "我讨厌食堂里水煮芹菜和一大堆胡萝卜。"
            "跟同学排队打饭，样子健康但味道寡淡。"
            "上学日常吃，周末在家妈妈做会好点。"
            "还是对芹菜无感，但能理解学校用意。"
        ),
    )
    _p(
        "Which vegetables did you dislike as a child?",
        "mall_street_market",
        logic="童年跟父母买菜时被逼尝苦瓜等；点名蔬菜；频次感受。",
        kitHint="街市=B菜摊试吃，引出具体讨厌蔬菜。",
        words={
            "正面回答": ["Bitter gourd slices", "Coriander haters", "Okra slime"],
            "来源或举例": ["market tasting", "mum's grocery bag", "wet market smell"],
            "频次": ["Sunday shopping", "before holidays"],
            "感受": ["pulled faces", "respect market fresh", "still skip okra"],
        },
        sample=(
            "At the street market my mum made me try bitter gourd slices, and I hated the taste instantly. "
            "I also avoided okra because the slime felt weird in my mouth. "
            "That happened on Sunday shopping trips before holidays. "
            "I still pull faces at okra, though I respect how fresh the market vegetables look."
        ),
        sampleZh=(
            "街市上妈妈让我试吃苦瓜，我当场就不喜欢了。"
            "秋葵黏滑的口感我也躲。"
            "节前周日买菜常碰到。"
            "秋葵仍不想吃，但认可摊上菜新鲜。"
        ),
    )
    _p(
        "Do people often grow vegetables by themselves?",
        "fruit_groceries",
        logic="先答有的人种、城市年轻人少买；举例长辈阳台；频次；感受。",
        kitHint="自种=阳台小葱，买生鲜仍是主流。",
        words={
            "正面回答": ["Some do", "Not most students", "Older relatives sometimes"],
            "来源或举例": ["balcony pots", "buy from markets", "herbs on windowsill"],
            "频次": ["seasonal planting", "daily buying for most"],
            "感受": ["nice but time-consuming", "practical to buy", "respect gardeners"],
        },
        sample=(
            "Some people grow vegetables, especially older relatives with balcony pots for scallions or lettuce. "
            "In cities most students like me just buy fresh produce from markets every few days. "
            "Home planting is seasonal and takes time students rarely have. "
            "I respect home gardeners, but buying is more practical for my life."
        ),
        sampleZh=(
            "有人会种，多是长辈在阳台种小葱、生菜。"
            "城里学生像我这样还是几天买一买市场生鲜。"
            "自种要看季节，也没那么多时间。"
            "佩服会种菜的人，但我买着吃更现实。"
        ),
    )
    _p(
        "Do people often grow vegetables by themselves?",
        "canteen_and_takeaways",
        logic="自种不多；食堂供菜为主；偶尔家乡土产；感受。",
        kitHint="食堂供餐视角，不单讲外卖。",
        words={
            "正面回答": ["Not very often in cities", "School gardens rare", "Some hometown plots"],
            "来源或举例": ["canteen bulk cooking", "grandparents' yard", "no dorm soil"],
            "频次": ["mostly buy daily", "visit village once a year"],
            "感受": ["rely on suppliers", "understand rural cousins", "fine either way"],
        },
        sample=(
            "Not very often in cities — we rely on canteens and suppliers for bulk vegetables. "
            "Some cousins in my hometown still have small plots, but dorm life has no soil to plant in. "
            "I see home-grown food once a year when I visit them. "
            "I am fine buying daily and understand why rural families still grow their own."
        ),
        sampleZh=(
            "城里不常见——食堂和供应商大宗供菜。"
            "老家表兄妹还有小块地，宿舍没土可种。"
            "一年回乡能见一两次自家菜。"
            "天天买也行，也理解农村还会自种。"
        ),
    )
    _p(
        "Do people often grow vegetables by themselves?",
        "mall_street_market",
        logic="街市摊主算半自种卖；对比市民买家；频次感受。",
        kitHint="街市=小农散户，不等于人人自种。",
        words={
            "正面回答": ["Farmers sell there", "Urban families seldom", "Small holders nearby"],
            "来源或举例": ["morning market trucks", "greenhouse towns", "phone orders too"],
            "频次": ["daily market supply", "rare home plots in flats"],
            "感受": ["fresh from nearby farms", "buying is normal", "respect small growers"],
        },
        sample=(
            "Urban families seldom grow much themselves, but nearby farmers sell on street markets every morning. "
            "Trucks bring greenhouse lettuce and local greens, while apps can top up later in the day. "
            "Home planting in flats is rare, so buying stays normal. "
            "I respect small growers and still enjoy picking their baskets in person."
        ),
        sampleZh=(
            "城里家庭很少自己种多少，但清晨街市有附近农户来卖。"
            "货车拉大棚生菜和本地青菜，白天还能用手机补货。"
            "公寓自种很少，所以买菜仍是常态。"
            "我认可小农户，也喜欢亲手挑他们摊上的菜。"
        ),
    )
    _p(
        "What is your favourite fruit?",
        "fruit_groceries",
        logic="喜好：最爱水果名，原因口感营养，频次，感受。",
        kitHint="苹果香蕉等超市常买水果。",
        words={
            "正面回答": ["Apples", "Bananas", "Mangoes in summer"],
            "原因或时间": ["sweet but not heavy", "easy to carry", "vitamins for study"],
            "频次": ["almost daily", "buy weekly"],
            "感受": ["reliable snack", "never bored", "cheap enough"],
        },
        sample=(
            "My favourite fruit is the apple — sweet, crunchy and not too heavy after class. "
            "Bananas are a close second when I need energy before sports. "
            "I buy apples almost daily or weekly at the campus shop. "
            "They are a reliable, cheap snack that I never get bored of."
        ),
        sampleZh=(
            "我最爱苹果，清甜爽脆，课后吃也不腻。"
            "要运动前香蕉也算第二爱。"
            "校园店里几乎天天或每周都会买。"
            "便宜省心，当零食也吃不厌。"
        ),
    )
    _p(
        "What is your favourite fruit?",
        "canteen_and_takeaways",
        logic="最爱水果可来自食堂水果档或早餐；不单外卖。",
        kitHint="食堂水果杯、早餐香蕉，外卖仅偶尔。",
        words={
            "正面回答": ["Orange segments", "Watermelon summer", "Pear slices"],
            "原因或时间": ["canteen fruit cup", "breakfast tray", "cool in summer"],
            "频次": ["lunch about twice a week", "more in summer"],
            "感受": ["refreshing", "balanced meal", "skip if queue long"],
        },
        sample=(
            "My favourite fruit is watermelon in summer, especially the chilled cubes at the school canteen. "
            "In winter I like orange segments on the breakfast tray more than greasy street snacks. "
            "I grab them about twice a week at lunch, more when it is hot. "
            "They feel refreshing and make the meal balanced."
        ),
        sampleZh=(
            "夏天最爱西瓜，尤其食堂冰过的块。"
            "冬天早饭碟里的橙子比油腻路边小吃更讨喜。"
            "午饭大约一周两次，天热更勤。"
            "吃着清爽，也让一餐更均衡。"
        ),
    )
    _p(
        "What is your favourite fruit?",
        "mall_street_market",
        logic="最爱市集时令水果，原因新鲜，频次，感受。",
        kitHint="街市荔枝、草莓等时令。",
        words={
            "正面回答": ["Lychee season", "Strawberries", "Local peaches"],
            "原因或时间": ["smell ripe at stalls", "short season excitement", "parents bought bags"],
            "频次": ["when in season", "street market Sundays"],
            "感受": ["worth the queue", "memories", "juicy"],
        },
        sample=(
            "My favourite fruit depends on the season — lychee from street markets is hard to beat in early summer. "
            "I love the smell when they are ripe on the stall and my parents used to buy whole bags. "
            "We shop for them on Sunday markets only while the season lasts. "
            "They are juicy, worth the queue and tied to warm memories."
        ),
        sampleZh=(
            "最爱看季节——初夏街市的荔枝最难取代。"
            "摊上熟了就香气很足，爸妈以前成袋买。"
            "只在当季周日去街市买。"
            "多汁，排队也值得，还有童年记忆。"
        ),
    )
    _p(
        "Do you like eating vegetables?",
        "fruit_groceries",
        logic="是否喜欢蔬菜，原因健康炒菜，频次，感受。",
        kitHint="在家清淡炒蔬菜。",
        words={
            "正面回答": ["Yes, more than before", "Not every kind", "Leafy greens OK"],
            "原因或时间": ["cook lightly at dorm", "parents' habit", "less oily"],
            "频次": ["most dinners", "with rice"],
            "感受": ["healthier", "still skip bitter ones", "practical"],
        },
        sample=(
            "Yes, I like eating vegetables more than I did as a kid, especially leafy greens stir-fried lightly. "
            "They balance rice and feel healthier than only meat dishes. "
            "I eat them at most dinners when I cook in the dorm. "
            "I still skip bitter ones, but overall it feels practical and good for me."
        ),
        sampleZh=(
            "喜欢，比小时候接受度高，尤其清炒青菜。"
            "配米饭也健康，比光吃肉好。"
            "宿舍做饭时多数晚餐会有。"
            "苦的还不行，但总体上挺实在也有益。"
        ),
    )
    _p(
        "Do you like eating vegetables?",
        "canteen_and_takeaways",
        logic="喜欢食堂青菜盒饭里的蔬菜，不是只吃外卖。",
        kitHint="食堂荤素窗口、少油蔬菜。",
        words={
            "正面回答": ["Canteen greens OK", "Prefer steamed", "Not greasy takeaways only"],
            "原因或时间": ["cheap set meal", "queue with classmates", "less oil than delivery"],
            "频次": ["weekdays lunch", "sometimes breakfast veg"],
            "感受": ["balanced tray", "boring but fine", "save money"],
        },
        sample=(
            "I like vegetables on the canteen set meal — steamed greens with tofu, not heavy sauce. "
            "It is cheaper and less oily than ordering greasy takeaways every lunch. "
            "I eat that on most weekdays with classmates in the queue. "
            "It looks boring but keeps the tray balanced and saves money."
        ),
        sampleZh=(
            "我喜欢食堂套餐里的蔬菜——清蒸青菜配豆腐，不要厚芡。"
            "比天天点油腻外卖便宜也清爽。"
            "工作日午饭大多和同学排队吃。"
            "卖相普通，但荤素均衡又省钱。"
        ),
    )
    _p(
        "Do you like eating vegetables?",
        "mall_street_market",
        logic="喜欢街市现买现做的新鲜蔬菜感。",
        kitHint="早市买来当天炒，突出新鲜。",
        words={
            "正面回答": ["Yes, fresh ones", "Crunchy stalks", "Colourful plates"],
            "原因或时间": ["buy morning, cook noon", "stalls look vivid", "share with roommates"],
            "频次": ["weekend cooking", "market trips Sundays"],
            "感受": ["tastes alive", "worth washing", "social meal"],
        },
        sample=(
            "Yes, especially when I buy colourful vegetables at the morning market and cook the same day. "
            "Crunchy stalks and vivid leaves taste alive compared with sad fridge bags. "
            "I do that on Sundays with roommates when we share a simple meal. "
            "Washing takes time, but the social meal is worth it."
        ),
        sampleZh=(
            "喜欢，尤其早市买回五颜六色菜当天炒。"
            "比冰箱里蔫掉的袋装菜脆嫩有生气。"
            "周日会和室友一起做简餐。"
            "洗菜费功夫，但一起吃饭很值得。"
        ),
    )
    _p(
        "How often do you eat vegetables?",
        "fruit_groceries",
        logic="行为习惯：几乎每天，原因自己买菜，流程，影响健康。",
        kitHint="frequency=with grocery habit。",
        words={
            "正面回答": ["Almost daily", "Once a day minimum", "Twice on cooking days"],
            "原因": ["stock greens in fridge", "cheap bulk", "parents' advice"],
            "时间线+行为描述": ["rinse and chop", "quick stir fry", "ten-minute prep"],
            "影响": ["less greasy skin", "more fiber", "steady energy"],
        },
        sample=(
            "I eat vegetables almost daily because I keep greens in the fridge after grocery runs. "
            "I rinse, chop and stir-fry in about ten minutes before study. "
            "On days I cook twice I might have vegetables twice. "
            "I get steadier energy and less greasy takeaways."
        ),
        sampleZh=(
            "几乎天天吃，因为买菜后会囤青菜。"
            "洗切快炒十来分钟就能吃。"
            "做两顿饭的话可能一天两顿都有菜。"
            "精力稳一些，油腻外卖也少点。"
        ),
    )
    _p(
        "How often do you eat vegetables?",
        "canteen_and_takeaways",
        logic="工作日食堂几乎每天有菜；外卖加餐时补沙拉或汤；影响。",
        kitHint="食堂频率为主，外卖点菜加蔬菜。",
        words={
            "正面回答": ["Weekdays daily", "Weekends less regular", "Add salad if takeaway"],
            "原因": ["set meal includes veg", "busy dorm kitchen", "health guilt"],
            "时间线+行为描述": ["lunch queue tray", "dinner simple soup", "occasional delivery veg box"],
            "影响": ["OK on campus", "watch weekend gaps", "feel balanced"],
        },
        sample=(
            "On weekdays I eat vegetables daily through the canteen set meal at lunch. "
            "Dinner might be simple soup with greens when I am lazy to cook. "
            "If I order takeaway I add a cheap vegetable side. "
            "Campus life stays balanced, though weekends need more planning."
        ),
        sampleZh=(
            "工作日几乎每天吃，靠午饭食堂套餐里的菜。"
            "晚饭懒得做就喝点青菜汤。"
            "点外卖会加个便宜素菜。"
            "在校还挺均衡，周末要多计划一下。"
        ),
    )
    _p(
        "How often do you eat vegetables?",
        "mall_street_market",
        logic="周末去街市买菜后吃菜更勤；习惯一周两三次大量蔬菜。",
        kitHint="街市采购周驱动 frequency。",
        words={
            "正面回答": ["Two or three times a week heavy", "Daily light garnish", "More on Sunday prep"],
            "原因": ["market bundles cheap", "cook for two days", "share with friends"],
            "时间线+行为描述": ["Sunday wash all", "fridge boxes", "weeknight reheat"],
            "影响": ["save time", "eat enough fiber", "less midweek takeaway"],
        },
        sample=(
            "I eat a lot of vegetables two or three times a week after Sunday market bundles. "
            "I wash everything once, box it in the fridge and stir-fry on weeknights. "
            "Between those meals I still add light garnish daily. "
            "It saves time, gives enough fiber and cuts midweek takeaway."
        ),
        sampleZh=(
            "周日街市捆一大把菜后，一周里三四顿会蔬菜很多。"
            "一次性洗好分装，工作日快炒。"
            "其余日子配菜也会有一点。"
            "省时间、纤维够，周中外卖也少点。"
        ),
    )
    _p(
        "How has the way people buy fruit and vegetables changed?",
        "fruit_groceries",
        logic="对比：以前菜场如今手机生鲜+超市；各自特点；感受。",
        kitHint="buy groceries change 用手机单+社区店。",
        words={
            "正面回答": ["More apps", "Still need to see fruit", "Mixed habits"],
            "选项1的特点与作用": ["delivery slots", "cold chain boxes", "good for busy weeks"],
            "选项2的特点与作用": ["wet market mornings", "pick ripeness", "chat with sellers"],
            "个人感受": ["convenient blend", "watch freshness online", "old markets stay"],
        },
        sample=(
            "People now mix phone grocery orders with quick trips to community shops for fruit. "
            "Apps help busy weeks with cold-chain boxes, but many still touch apples before buying. "
            "Traditional wet markets survive for morning shoppers who want to chat and bargain. "
            "I like the convenient blend if freshness is honest online."
        ),
        sampleZh=(
            "现在大家会手机买菜，也会去社区店挑水果。"
            "忙的时候冷链配送省事，买苹果很多人仍要亲手挑。"
            "早市还在，爱还价聊两句的人去那儿。"
            "兼顾方便，只要网购新鲜度靠谱我就接受。"
        ),
    )
    _p(
        "How has the way people buy fruit and vegetables changed?",
        "canteen_and_takeaways",
        logic="食堂采购集中+学生自选沙拉；对比过去；外卖配菜升级；感受。",
        kitHint="食堂供应链+学生营养意识，外卖非唯一。",
        words={
            "正面回答": ["Central canteen buying", "More salad bars", "Less frozen only"],
            "选项1的特点与作用": ["bulk contracts", "steady lunch veg", "school health rules"],
            "选项2的特点与作用": ["old oily trays", "few choices", "less greens"],
            "个人感受": ["healthier trend", "still uneven", "canteen matters"],
        },
        sample=(
            "Schools buy vegetables in bulk for canteens, while students now expect salad bars and lighter sides. "
            "Compared with old oily trays with little greens, today's choices look healthier on paper. "
            "Takeaway apps add vegetable side options, but campus meals still shape daily habits most. "
            "I welcome the trend, though quality is uneven between schools."
        ),
        sampleZh=(
            "学校食堂集中采购，学生也想要沙拉吧和清淡配菜。"
            "比起当年油腻少菜的托盘，现在选择名义上更健康。"
            "外卖能加素菜，但校园餐仍最影响日常。"
            "方向挺好，各校品质还不平衡。"
        ),
    )
    _p(
        "How has the way people buy fruit and vegetables changed?",
        "mall_street_market",
        logic="商场超市+街市线上线下并存；扫码付；对比早年现金-only市场。",
        kitHint="街市扫码、预售、社区团购并存。",
        words={
            "正面回答": ["Scan to pay", "Night markets online", "Mall finesse sections"],
            "选项1的特点与作用": ["QR at stalls", "live streams selling", "young vendors"],
            "选项2的特点与作用": ["cash and haggling before", "less traceability", "smaller variety"],
            "个人感受": ["livelier markets", "trust good stalls", "heritage kept"],
        },
        sample=(
            "Street markets now use QR payments and even live streams, while malls add fine fruit sections upstairs. "
            "Ten years ago many stalls were cash-only with less variety and traceability. "
            "Community group buying fills fridges, yet Sunday markets still feel lively. "
            "I trust stalls with honest quality and glad the heritage is kept in a modern way."
        ),
        sampleZh=(
            "街市能扫码甚至直播卖货，商场楼上也有精品水果区。"
            "十年前不少摊只收现金，品种和溯源都弱些。"
            "社区团购会填满冰箱，但周日市集依旧热闹。"
            "我信口碑好的摊位，也高兴老传统换了新方式还在。"
        ),
    )