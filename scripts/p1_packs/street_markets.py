# -*- coding: utf-8 -*-
"""Street Markets Freestyle packs."""


def register(_p):
    _p(
        "When was the last time you went to a street market?",
        "mall_street_market",
        logic="先答上次时间，再写买什么、和谁；频次式补充；感受。",
        kitHint="街市最近一次：扫码买早餐或小零食。",
        words={
            "正面回答": ["Last weekend", "Two weeks ago", "Saturday morning"],
            "来源或举例": ["breakfast jianbing", "paid with phone", "short visit with mum"],
            "频次": ["not weekly", "before holidays sometimes"],
            "感受": ["lively", "fun not for bulk", "quick errand"],
        },
        sample=(
            "The last time was last Saturday morning with my mum near our neighbourhood market. "
            "We bought breakfast pancakes and a few oranges, and I paid with my phone at the stall. "
            "I do not go weekly — maybe before holidays. "
            "It was lively and fun for a short visit, not for big weekly shopping."
        ),
        sampleZh=(
            "上次是上周六早上，和妈妈去小区门口早市。"
            "买了煎饼当早餐和几个橙子，我手机扫码付的。"
            "不是每周都去，大节前有时去。"
            "挺热闹，适合短逛，不适合大宗采购。"
        ),
    )
    _p(
        "When was the last time you went to a street market?",
        "hometown_local_food",
        logic="上次回家乡逛老市场吃小吃；时间地点；感受记忆。",
        kitHint="家乡美食=街市场景，扣「什么时候去过街市」。",
        words={
            "正面回答": ["During spring festival", "Last trip home", "Winter holiday"],
            "来源或举例": ["hometown night market", "local rice noodles", "childhood stall"],
            "频次": ["once per holiday", "when visiting parents"],
            "感受": ["nostalgic", "crowded", "worth the queue"],
        },
        sample=(
            "I went during winter holiday when I visited my hometown and walked through the old night market. "
            "I ate local rice noodles at a stall I remembered from childhood. "
            "That happens about once each holiday when I see my parents. "
            "It felt nostalgic, crowded and worth the queue."
        ),
        sampleZh=(
            "寒假回家那次逛了老城夜市。"
            "在小时候记得的摊子吃了家乡米粉。"
            "每个长假回家大概会有一次。"
            "又挤又怀旧，排队也值得。"
        ),
    )
    _p(
        "When was the last time you went to a street market?",
        "fruit_groceries",
        logic="上周去菜场买水果最近时间；细节行为；感受实用。",
        kitHint="果蔬街市=最近一次买水果。",
        words={
            "正面回答": ["About ten days ago", "This month", "Sunday morning"],
            "来源或举例": ["picked apples", "weighed greens", "reusable bag"],
            "频次": ["every two or three weeks", "top-up trips"],
            "感受": ["fresh smell", "practical", "short walk from subway"],
        },
        sample=(
            "About ten days ago on a Sunday morning I stopped at a street vegetable market after the subway. "
            "I picked apples, weighed a bunch of greens and carried them in a reusable bag. "
            "I top up every two or three weeks. "
            "The fresh smell felt practical after a short walk from the station."
        ),
        sampleZh=(
            "十来天前周日上午，地铁出来顺路去了蔬菜街市。"
            "挑了苹果、称了一把青菜，环保袋拎着走。"
            "两三周补一次货。"
            "生鲜味儿很踏实，出站走几步就到。"
        ),
    )
    _p(
        "Are there many street markets in your country?",
        "mall_street_market",
        logic="先答多，再举社区早市、夜市例子，频次观察，感受。",
        kitHint="国家层面仍有许多街市与夜市。",
        words={
            "正面回答": ["Yes, quite many", "Still common", "Especially in cities"],
            "来源或举例": ["neighbourhood morning fairs", "tourist night bazaars", "wet markets"],
            "频次": ["daily in some towns", "weekends busier"],
            "感受": ["part of daily life", "compete with malls", "both survive"],
        },
        sample=(
            "Yes, there are still quite many street markets in my country, especially near residential areas. "
            "You see morning fairs for groceries and busier night bazaars on weekends. "
            "Some towns host them daily, others on fixed weekday slots. "
            "They are part of daily life and coexist with malls rather than disappear."
        ),
        sampleZh=(
            "挺多的，住宅区附近尤其常见。"
            "有清晨买菜集，周末夜市更闹。"
            "有的城镇天天有，有的固定星期几。"
            "是生活一部分，和商场并存没消失。"
        ),
    )
    _p(
        "Are there many street markets in your country?",
        "hometown_local_food",
        logic="家乡小吃街市作为例证说明国内街市多；感受文化。",
        kitHint="家乡美食街=证明街市仍然存在。",
        words={
            "正面回答": ["Yes around hometown", "Food streets famous", "Tourists visit too"],
            "来源或举例": ["snack alleys", "local brands", "festival crowds"],
            "频次": ["busy every evening", "peak on holidays"],
            "感受": ["cultural pride", "noisy energy", "authentic taste"],
        },
        sample=(
            "Yes — even my hometown has famous snack streets that feel like permanent markets. "
            "Locals buy daily staples while tourists queue for the same regional dishes. "
            "Evenings stay busy, and holidays push crowds higher. "
            "They carry cultural pride and noisy energy with authentic taste."
        ),
        sampleZh=(
            "有，老家就有出名的小吃街，像常驻市集。"
            "本地人买日用，游客排同款地方菜。"
            "晚上一直很旺，假期人更多。"
            "有文化自信，嘈杂但味道地道。"
        ),
    )
    _p(
        "Are there many street markets in your country?",
        "fruit_groceries",
        logic="从蔬果露天摊数量说明街市多；对比超市；感受。",
        kitHint="菜农摊贩=街市数量例证。",
        words={
            "正面回答": ["Many produce stalls", "Every district", "Some shrink but stay"],
            "来源或举例": ["trucks at dawn", "leafy piles", "price boards"],
            "频次": ["daily supply rhythm", "before sunrise starts"],
            "感受": ["competitive prices", "messy but real", "still needed"],
        },
        sample=(
            "There are many open-air produce stalls in most districts, so street markets remain common. "
            "Trucks arrive before sunrise with leafy piles and handwritten price boards. "
            "Some old blocks shrank, but new corners pop up near subways. "
            "They look messy yet real, with competitive prices people still need."
        ),
        sampleZh=(
            "多数城区都有露天菜摊，街市仍然普遍。"
            "天亮前货车带着青菜和手写价签来。"
            "老街区有的缩小，地铁口也有新集。"
            "虽乱但真实，价钱实惠，大家也离不开。"
        ),
    )
    _p(
        "Are there many street markets in China?",
        "mall_street_market",
        logic="同 country 题但更具体：城管规范、保留早市夜市；感受。",
        kitHint="中国街市规范化但仍多。",
        words={
            "正面回答": ["Yes, still many", "Cleaner than before", "Registered stalls"],
            "来源或举例": ["fixed pitch numbers", "QR health signs", "community bazaars"],
            "频次": ["daily groceries", "night snacks weekends"],
            "感受": ["more orderly", "still lively", "urban and rural both"],
        },
        sample=(
            "Yes, China still has many street markets in cities and towns, though they look more orderly now. "
            "Stalls have fixed pitch numbers and QR health signs, especially in big cities. "
            "Morning groceries and weekend night snacks keep them busy. "
            "They stay lively from megacities to smaller county seats."
        ),
        sampleZh=(
            "中国城乡仍有大量街市，只是比过去整齐些。"
            "摊位有固定编号，大城市还常见卫生扫码信息。"
            "清晨买菜、周末夜宵都撑得住人流。"
            "从大城市到县城都还挺热闹。"
        ),
    )
    _p(
        "Are there many street markets in China?",
        "hometown_local_food",
        logic="以中国家乡小吃街为例肯定数量；政策与烟火气；感受。",
        kitHint="地方小吃街说明中国街市仍多。",
        words={
            "正面回答": ["Definitely yes", "Every city has some", "Hometown food streets"],
            "来源或举例": ["night snack lane", "regional dishes", "family recipes"],
            "频次": ["evenings busy", "holiday peaks"],
            "感受": ["proud local taste", "tourist plus locals", "still affordable"],
        },
        sample=(
            "Definitely yes — nearly every city I have visited keeps some snack streets or morning fairs. "
            "My hometown lane sells regional dishes from family recipes at affordable prices. "
            "Locals and tourists mix on busy evenings and holiday peaks. "
            "I feel proud of that local taste and glad it stays affordable."
        ),
        sampleZh=(
            "当然有——去过不少城市都有小吃街或早集。"
            "老家巷子卖祖传口味的家乡菜，价钱亲民。"
            "晚上和假期本地人游客混在一起。"
            "为家乡味自豪，也高兴还没贵到吃不起。"
        ),
    )
    _p(
        "Are there many street markets in China?",
        "fruit_groceries",
        logic="中国菜市密度高；便民服务点；感受生计。",
        kitHint="菜市场网点= China 街市多。",
        words={
            "正面回答": ["Very common", "15-minute life circle", "Wet markets steady"],
            "来源或举例": ["community veggie points", "farm trucks", "elder shoppers"],
            "频次": ["daily rhythm", "dawn busiest"],
            "感受": ["supports livelihoods", "fresh chain short", "familiar scene"],
        },
        sample=(
            "Street vegetable markets are very common in China within the fifteen-minute neighbourhood circle. "
            "Farm trucks and community veggie points serve elders and students on a daily rhythm. "
            "Dawn is the busiest time before prices shift. "
            "The scene feels familiar, keeps livelihoods going and shortens the fresh-food chain."
        ),
        sampleZh=(
            "中国街坊十五分钟圈里菜市场很常见。"
            "农家车、社区菜点每天服务老人和学生。"
            "黎明最忙，过会儿价会有变化。"
            "这景象熟悉，养着小摊生计，菜也更新鲜。"
        ),
    )
    _p(
        "What do people usually buy on the street market?",
        "mall_street_market",
        logic="先答常买生鲜零食日用品；举例；自己观察频次；感受实用。",
        kitHint="街市主线：菜果、早点、小百货。",
        words={
            "正面回答": ["Fresh produce", "Breakfast food", "Household basics"],
            "原因": ["lower price", "see quality", "social chat"],
            "时间线+行为描述": ["morning bags heavy", "scan small payments", "smell guides choices"],
            "影响": ["local economy", "short trips", "less packaging"],
        },
        sample=(
            "People usually buy fresh vegetables, fruit, breakfast snacks and small household goods on street markets. "
            "Morning shoppers leave with heavy bags after they smell fruit and chat with stall owners. "
            "Many pay with a quick scan instead of long checkout lines. "
            "That keeps local stalls busy and cuts packaging from big supermarkets."
        ),
        sampleZh=(
            "大家通常买生鲜、早点和小日用品。"
            "早上闻着果香、跟摊主聊两句，袋子就沉甸甸了。"
            "很多人扫码付，不用超市排长队。"
            "让小摊有生意，包装也比大超市少。"
        ),
    )
    _p(
        "What do people usually buy on the street market?",
        "hometown_local_food",
        logic="人们买家乡小吃、卤味、米面特产；扣 markets 不是只谈旅游。",
        kitHint="家乡食物=街市购买内容之一，合规则 8。",
        words={
            "正面回答": ["Local snacks", "Spicy skewers", "Rice noodles"],
            "原因": ["authentic recipe", "festival mood", "gift for relatives"],
            "时间线+行为描述": ["queue at famous stall", "take away hot", "share with family"],
            "影响": ["supports old brands", "memory food", "night economy"],
        },
        sample=(
            "Besides groceries, people buy hometown snacks like spicy skewers, braised duck and fresh rice noodles. "
            "They queue at famous stalls, carry hot portions home or mail them to relatives as gifts. "
            "Weekend nights fuel the local night economy. "
            "It supports old brands and turns food into shared memory."
        ),
        sampleZh=(
            "除了买菜，还会买麻辣串、卤鸭、鲜米粉等家乡小吃。"
            "名店要排队，热乎乎的拎回家或寄给亲戚当礼。"
            "周末夜撑着小城夜市经济。"
            "养活老牌子，也把味道变成共同记忆。"
        ),
    )
    _p(
        "What do people usually buy on the street market?",
        "fruit_groceries",
        logic="常买蔬果为核心；称重讨价还价；行为影响健康饮食。",
        kitHint="买 fruit veg 是街市主品类。",
        words={
            "正面回答": ["Leafy greens", "Seasonal fruit", "Roots and tofu"],
            "原因": ["farm to stall fast", "pick ripeness", "cheaper bundles"],
            "时间线+行为描述": ["check leaves", "compare two stalls", "reusable bag"],
            "影响": ["cook same day", "less waste", "vitamins at home"],
        },
        sample=(
            "Most bags start with leafy greens, seasonal fruit, roots and tofu from nearby farms. "
            "Shoppers compare two stalls, tap melons and bundle bargains into reusable bags. "
            "They often cook the same day so leaves do not wilt. "
            "That brings vitamins home cheaply with less waste."
        ),
        sampleZh=(
            "篮子先装青菜、时令水果、根茎和豆腐，多来自附近农户。"
            "货比两家、拍瓜挑熟，便宜捆扎塞进环保袋。"
            "常当天炒掉，怕叶子蔫了。"
            "便宜把维生素带回家，也减少浪费。"
        ),
    )
    _p(
        "Do you prefer to go shopping in the shopping mall or on the street market?",
        "mall_street_market",
        logic="对比：日常街市 vs 商场买衣服电子产品；个人感受。",
        kitHint="混合偏好：菜去街市，杂物去商场。",
        words={
            "正面回答": ["Depends on the item", "Market for food", "Mall for clothes"],
            "选项1的特点与作用": ["street food smells", "lower veg prices", "lively chat"],
            "选项2的特点与作用": ["AC comfort", "clear sizes", "one-stop brands"],
            "个人感受": ["enjoy both roles", "hate mall crowds sales", "markets for soul"],
        },
        sample=(
            "For fruit and breakfast I prefer street markets — lively, cheap and honest in smell. "
            "Malls win for clothes, shoes and electronics with clear sizes and air conditioning. "
            "Sales crowds in malls tire me, while markets feel messy but human. "
            "I enjoy both when each plays its role."
        ),
        sampleZh=(
            "买果子和早饭我爱街市，热闹便宜闻着真。"
            "买衣服鞋电器还是商场，尺码清楚还有空调。"
            "商场打折挤死人，市集乱点但有人情味。"
            "各干各的活我都挺喜欢。"
        ),
    )
    _p(
        "Do you prefer to go shopping in the shopping mall or on the street market?",
        "hometown_local_food",
        logic="小吃家乡味选街市，买衣服仍商场；对比特点；情感偏好。",
        kitHint="家乡味道牵引偏爱街市，但不否定商场。",
        words={
            "正面回答": ["Street market for food", "Mall for basics", "Heart leans market"],
            "选项1的特点与作用": ["hometown taste", "warm stall aunties", "late-night skewers"],
            "选项2的特点与作用": ["predictable chain stores", "fast phone service", "less character"],
            "个人感受": ["nostalgia", "practical split", "flavour wins stomach"],
        },
        sample=(
            "For hometown flavour I always pick street markets — aunties remember my order and skewers sizzle at night. "
            "Malls are fine for predictable chain basics and fast phone service when I am in a rush. "
            "They have less character but save time. "
            "My heart leans to markets because flavour wins my stomach, yet I shop both."
        ),
        sampleZh=(
            "要讲家乡味我一定站街市，摊主阿姨认得我，深夜串串滋啦响。"
            "赶时间买标品我会去商场，连锁齐全服务好。"
            "没那么有特色，但省时间。"
            "心里偏市集，因为胃诚实，可两边都会逛。"
        ),
    )
    _p(
        "Do you prefer to go shopping in the shopping mall or on the street market?",
        "fruit_groceries",
        logic="果蔬必街市；商场买洗护；对比新鲜度与价格；感受。",
        kitHint="生鲜选街市，是合理的 prefer 对比。",
        words={
            "正面回答": ["Market for produce", "Mall for shampoo", "Clear split"],
            "选项1的特点与作用": ["see ripeness", "talk to farmers", "morning deals"],
            "选项2的特点与作用": ["clean aisles", "member points", "heavy bottles delivered"],
            "个人感受": ["trust hands", "mall is backup", "weekly ritual market"],
        },
        sample=(
            "I clearly prefer street markets for fruit and vegetables where I can see ripeness and talk to farmers. "
            "Malls are my backup for shampoo, detergent and member-point promotions. "
            "Sunday morning market runs became a weekly ritual; mall trips are quicker errands. "
            "I trust my hands in markets and use malls when shelves feel easier for heavy bottles."
        ),
        sampleZh=(
            "果蔬我一定偏街市，能看熟度也能跟农户聊。"
            "洗发水洗衣液、会员积分才去商场。"
            "周日早市成了每周仪式，商场是补货快跑。"
            "手里挑菜信自己，重物用商场货架省力。"
        ),
    )