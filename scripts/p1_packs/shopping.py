# -*- coding: utf-8 -*-
"""Shopping Freestyle packs."""


def register(_p):
    _p(
        "What was the last thing you bought?",
        "fruit_groceries",
        logic="先答最近买的食物杂货，再细节、多久买一次、感受。",
        kitHint="水果生鲜：最近一次买苹果香蕉等。",
        words={
            "正面回答": ["Some apples", "Bananas and eggs", "Fresh groceries"],
            "来源或举例": ["campus shop", "vitamins in fruit", "cook simple meals"],
            "频次": ["picked them up yesterday", "small top-up trips"],
            "感受": ["practical", "fresh", "worth the walk"],
        },
        sample=(
            "The last thing I bought was a bag of apples and a few bananas at a shop near campus. "
            "I wanted something fresh to snack on instead of only instant noodles. "
            "I picked them up just yesterday on a quick errand. "
            "I find that choice practical and worth the short walk."
        ),
        sampleZh=(
            "我最近买的是学校附近店里的一袋苹果和几个香蕉。"
            "想吃点新鲜的，不总泡面。"
            "就是昨天顺路买的。"
            "挺实用，走几步也值得。"
        ),
    )
    _p(
        "What was the last thing you bought?",
        "mall_street_market",
        logic="先答最近买的日用品或衣服，商超或街市场景，频次感受。",
        kitHint="商超街市：手机支付、日用杂物。",
        words={
            "正面回答": ["Toothpaste", "A phone cable", "Socks"],
            "来源或举例": ["shopping mall basement", "paid with my phone", "discount shelf"],
            "频次": ["bought last weekend", "when something breaks"],
            "感受": ["convenient", "quick", "good enough quality"],
        },
        sample=(
            "The last thing I bought was a phone charging cable in a mall near the subway. "
            "My old one broke, so I paid with my phone at a small electronics counter. "
            "I got it last weekend on the way back from class. "
            "It was quick and convenient, and the quality is good enough for daily use."
        ),
        sampleZh=(
            "我最近买的是地铁口商场里的一根手机充电线。"
            "原来的坏了，就在小柜台用手机付款。"
            "上周末下课顺路买的。"
            "又快又方便，质量日常够用。"
        ),
    )
    _p(
        "Who did you go shopping with when you were a child?",
        "mall_street_market",
        logic="点名童年陪购者（父母），再写去哪儿买、频次、感受。",
        kitHint="必须点明 parents；商超或街市购物场景。",
        words={
            "正面回答": ["My parents", "Mum and dad", "Mainly my mum"],
            "来源或举例": ["weekend mall", "street market snacks", "cart full of basics"],
            "频次": ["most Saturdays", "before spring festival"],
            "感受": ["warm", "a bit boring as a kid", "safe"],
        },
        sample=(
            "When I was a child I usually went shopping with my parents, especially my mum. "
            "We visited malls for clothes and sometimes a street market for snacks before festivals. "
            "That was most Saturdays or before spring festival. "
            "It felt warm and safe, though a bit boring when I just waited by the fitting room."
        ),
        sampleZh=(
            "小时候我通常和父母一起逛，尤其是妈妈。"
            "周末去商场买衣服，过节前有时去街市买小吃。"
            "多是周六，或者春节前。"
            "觉得很安心亲切，就是等试衣时小孩觉得有点闷。"
        ),
    )
    _p(
        "Who did you go shopping with when you were a child?",
        "fruit_groceries",
        logic="童年和妈妈（或父母）买蔬菜水果，点名人物，频次感受。",
        kitHint="生鲜购物=和 parents 去菜场或超市果蔬区。",
        words={
            "正面回答": ["My mum", "Both parents", "My mum picked fruit"],
            "来源或举例": ["touch oranges", "weigh vegetables", "small wet market"],
            "频次": ["twice a week", "Sunday mornings often"],
            "感受": ["learned to choose ripe fruit", "noisy but lively", "family habit"],
        },
        sample=(
            "I usually went with my mum, and my dad came along when we needed heavier bags. "
            "She taught me to tap oranges and pick leafy greens at the wet market or supermarket. "
            "We shopped for groceries about twice a week, often on Sunday mornings. "
            "It was noisy but lively, and it became a small family habit."
        ),
        sampleZh=(
            "一般是妈妈带我去，东西多的时候爸爸也会跟去。"
            "她教我在菜场或超市挑橘子、挑青菜。"
            "一周大概两次买生鲜，很多是周日上午。"
            "虽吵但热闹，也成了家里的小习惯。"
        ),
    )
    _p(
        "Do you enjoy shopping?",
        "mall_street_market",
        logic="喜好：是否享受，原因可短逛不长按，频次，感受。",
        kitHint="商超街市：喜欢边逛边吃小吃、用手机付钱。",
        words={
            "正面回答": ["Sometimes", "Only short trips", "Not big sales crowds"],
            "原因或时间": ["street food smells", "easy phone pay", "no long queues"],
            "频次": ["once or twice a month", "with friends sometimes"],
            "感受": ["relaxed in small doses", "tiring if too long", "social fun"],
        },
        sample=(
            "Sometimes I enjoy shopping if it is a short trip to a mall or street market with friends. "
            "I like the food smells and paying quickly with my phone without long queues. "
            "I do that about once or twice a month. "
            "In small doses it feels relaxed and social; too many hours feel tiring."
        ),
        sampleZh=(
            "有时候挺享受，尤其是和朋友短途逛商场或街市。"
            "喜欢小吃香味，也喜欢手机快付、不用排长队。"
            "一个月一两次吧。"
            "短逛轻松又有社交感，太久还是会累。"
        ),
    )
    _p(
        "Do you enjoy shopping?",
        "fruit_groceries",
        logic="喜不喜欢买菜挑水果；原因健康；频次；实用感受。",
        kitHint="买菜享受=挑蔬果的烟火气，不是买衣服。",
        words={
            "正面回答": ["Yes, light grocery runs", "Picking fruit is OK", "Not fashion shopping"],
            "原因或时间": ["fresh colours", "cook healthier", "quick list in mind"],
            "频次": ["weekly small trips", "after class sometimes"],
            "感受": ["grounded", "practical joy", "not exciting but fine"],
        },
        sample=(
            "I enjoy light grocery runs more than fashion shopping. "
            "Choosing colourful fruit and planning a simple meal feels grounded and healthy. "
            "I make those trips weekly, sometimes after class. "
            "It is not exciting, but I get practical joy from it."
        ),
        sampleZh=(
            "比起买衣服，我更享受轻量的买菜。"
            "挑水果、想一顿简单饭，让人觉得踏实健康。"
            "每周都会去，有时下课后顺路。"
            "不算刺激，但有实在的满足感。"
        ),
    )
    _p(
        "Do you like shopping?",
        "mall_street_market",
        logic="同 enjoy 结构略换表述：喜不喜欢购物，原因、频次、感受。",
        kitHint="街市夜市闲逛 vs 网购对比可轻点。",
        words={
            "正面回答": ["Generally yes", "In moderation", "Depends on the place"],
            "原因或时间": ["live music at night markets", "see products in hand", "chat with stall owners"],
            "频次": ["a few times a month", "more before holidays"],
            "感受": ["lively", "wallet careful", "happy enough"],
        },
        sample=(
            "Generally I like shopping in moderation, especially night markets where music and lights feel lively. "
            "I can hold products, chat with stall owners and pay with a quick scan. "
            "I go a few times a month, more before holidays. "
            "I stay careful with my wallet but leave happy enough."
        ),
        sampleZh=(
            "总体来说喜欢适度逛，尤其夜市有音乐灯光很热闹。"
            "能摸实物、跟摊主聊两句，扫码也快。"
            "一个月几次，节前更勤。"
            "钱包会管住，但心情还挺不错。"
        ),
    )
    _p(
        "Do you like shopping?",
        "fruit_groceries",
        logic="喜欢买菜胜过长时间逛街；原因新鲜实惠；频次感受。",
        kitHint="like shopping = 果蔬区短购。",
        words={
            "正面回答": ["For groceries yes", "Not hours of malls", "Short lists only"],
            "原因或时间": ["save money cooking", "fruit for study snacks", "ten-minute errand"],
            "频次": ["twice a week", "quick after subway"],
            "感受": ["efficient", "satisfying", "less guilt than takeaways"],
        },
        sample=(
            "For groceries I do like shopping — short lists of fruit and vegetables near the subway. "
            "Cooking saves money and gives me healthier study snacks. "
            "I shop about twice a week on quick errands. "
            "It feels efficient and less guilty than ordering takeaways every night."
        ),
        sampleZh=(
            "买菜我还是喜欢的——地铁口附近短清单买点果蔬。"
            "自己煮省钱，学习零食也健康些。"
            "一周大概两次，很快买完。"
            "高效，也比天天外卖少点负罪感。"
        ),
    )
    _p(
        "How often do you go shopping?",
        "mall_street_market",
        logic="行为习惯：频率、原因、过程、影响。",
        kitHint="一月几次商超街市补货。",
        words={
            "正面回答": ["Once or twice a week", "Small trips", "Not every day"],
            "原因": ["daily needs", "see friends at the mall", "street market bargains"],
            "时间线+行为描述": ["after class detour", "phone pay", "twenty minutes max"],
            "影响": ["stays affordable", "break from desk", "don't overspend"],
        },
        sample=(
            "I go shopping about once or twice a week for small daily needs. "
            "I often detour after class to a mall or nearby street stalls, pay by phone, and leave within twenty minutes. "
            "That keeps spending affordable and gives me a short break from my desk. "
            "I try not to overspend on things I do not need."
        ),
        sampleZh=(
            "一周购物大概一两次，多是补日用品。"
            "下课后常绕去商场或街边摊，手机付钱，二十分钟以内走人。"
            "开销可控，也能离开书桌透口气。"
            "尽量不乱买用不上的东西。"
        ),
    )
    _p(
        "How often do you go shopping?",
        "fruit_groceries",
        logic="买菜频率更高；原因吃饭；行为；饮食影响。",
        kitHint="果蔬采购频率=how often shopping 的合理解读。",
        words={
            "正面回答": ["Two or three times a week", "Fresh top-ups", "More if I cook"],
            "原因": ["fruit goes off fast", "cheap canteen plus fruit", "parents' habit"],
            "时间线+行为描述": ["evening market run", "check fridge first", "carry light bag"],
            "影响": ["eat more vitamins", "less instant food", "steady routine"],
        },
        sample=(
            "For groceries I shop two or three times a week because fruit goes off quickly. "
            "I check the fridge, buy a light bag of apples or greens, and cook simple meals. "
            "Evening market runs fit my schedule after study. "
            "I eat more vitamins and rely less on instant noodles."
        ),
        sampleZh=(
            "买菜一周两三次，水果放不住。"
            "先看冰箱，买一轻袋苹果或青菜，简单做点饭。"
            "学习后傍晚去一趟刚好。"
            "维生素多些，也少泡方便面了。"
        ),
    )
    _p(
        "Do you prefer shopping online or in shops?",
        "mall_street_market",
        logic="对比：倾向线下街市商超摸实物，线上快但品质不稳，感受。",
        kitHint="手机付实体店=偏线下但现代。",
        words={
            "正面回答": ["In shops for most things", "Online for books", "Depends on item"],
            "选项1的特点与作用": ["see colour and size", "street food nearby", "instant take home"],
            "选项2的特点与作用": ["cheaper delivery", "good for heavy items", "return hassle"],
            "感受": ["trust my eyes", "mix both", "enjoy walking to stalls"],
        },
        sample=(
            "For clothes and snacks I prefer shops and street markets where I can see colour and size. "
            "I still pay with my phone, but I like taking food home instantly. "
            "Online is fine for books or heavy items, though returns can be a hassle. "
            "Overall I trust my eyes in person, yet I mix both channels."
        ),
        sampleZh=(
            "衣服零食我更爱去店里或街市，能看颜色和尺码。"
            "照样手机付款，但能马上拎回家。"
            "买书或重物网购也行，就是退换麻烦。"
            "总体信眼睛，线上线下会搭配用。"
        ),
    )
    _p(
        "Do you prefer shopping online or in shops?",
        "fruit_groceries",
        logic="生鲜偏线下挑；线上套餐偶尔；对比品质；感受。",
        kitHint="水果蔬菜必须线下，别把答题说成只网购。",
        words={
            "正面回答": ["In shops for produce", "Online for staples", "Touch fruit in person"],
            "选项1的特点与作用": ["smell and ripeness", "talk to sellers", "small local market"],
            "选项2的特点与作用": ["apps for rice and oil", "heavy bags delivered", "less fun"],
            "感受": ["fresher in hand", "convenient blend", "weekly ritual"],
        },
        sample=(
            "I prefer buying fruit and vegetables in shops so I can check ripeness by smell and touch. "
            "Talking to sellers at a small market near campus feels fresher than mystery boxes online. "
            "I only use apps for rice, oil and other heavy staples. "
            "I enjoy the weekly ritual in person and still like the convenience of mixed shopping."
        ),
        sampleZh=(
            "果蔬我宁愿去店里，能闻能摸成熟度。"
            "校门小市场跟摊主聊两句，比网购盲盒踏实。"
            "米面油重物才用应用下单。"
            "每周亲手挑菜挺有仪式感，也保留了网购的方便。"
        ),
    )