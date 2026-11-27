# -*- coding: utf-8 -*-
"""Travelling Freestyle packs."""


def register(_p):
    _p(
        "Where did you go on holiday when you were a child?",
        "subway_bus_commute",
        logic="先答童年假期去的具体地方，再写怎么去；地铁只是去那里的交通，不是假期本身。",
        kitHint="海边或近郊小城为主轴；地铁只出现在「怎么到目的地」里。",
        words={
            "正面回答": ["A coastal city", "Nearby towns", "Relatives' place"],
            "来源或举例": ["summer break", "subway then high-speed train", "two or three days"],
            "频次": ["once or twice each summer", "main school holidays"],
            "感受": ["warm memories", "simple trips", "happy"],
        },
        sample=(
            "As a child I usually spent summer holidays in a nearby coastal city with my parents. "
            "We took the subway to the main train station first, then a high-speed train for the rest. "
            "We did that about once or twice each summer. "
            "Those trips were simple but warm, and I still remember the sea breeze."
        ),
        sampleZh=(
            "小时候暑假常和父母去附近一座海边城市。"
            "我们先坐地铁到火车站，再转高铁。"
            "每年暑假大概一两次。"
            "行程不复杂但很温馨，我还记得海风。"
        ),
    )
    _p(
        "Where did you go on holiday when you were a child?",
        "family_car_passenger",
        logic="先答去了哪里度假，再写爸爸开车、后座看风景，频次与感受扣童年假期。",
        kitHint="全家开车：目的地是亲戚家或周边城市，材质是假期乘客视角。",
        words={
            "正面回答": ["Grandparents' town", "Lake area", "A small city nearby"],
            "来源或举例": ["dad in front", "back-seat snacks", "highway rest stops"],
            "频次": ["every spring festival", "one summer road trip"],
            "感受": ["safe and relaxed", "happy", "cozy"],
        },
        sample=(
            "We often spent holidays at my grandparents' town or a lake area not too far away. "
            "My dad drove while I sat in the back with comics and snacks my mum packed. "
            "That happened every spring festival and maybe one longer summer trip. "
            "I felt safe and relaxed, and those slow road trips still feel cozy to me."
        ),
        sampleZh=(
            "假期常去爷爷奶奶那边或不太远的湖区。"
            "爸爸开车，我在后座看漫画、吃妈妈带的零食。"
            "每年春节基本都会去，夏天偶尔再开远一趟。"
            "很安心放松，那种慢悠悠的车旅现在想起来仍很暖。"
        ),
    )
    _p(
        "Where did you go on holiday when you were a child?",
        "hometown_local_food",
        logic="先答回老家过节，再写熟悉小吃摊与家人，频次与想念感受。",
        kitHint="童年假期=回乡吃本地小吃；目的地是家乡，不是骑车故事。",
        words={
            "正面回答": ["My hometown", "Grandparents' neighbourhood", "Local food streets"],
            "来源或举例": ["same breakfast stall", "family-style dishes", "old market nearby"],
            "频次": ["every Spring Festival", "once more in summer sometimes"],
            "感受": ["happy and full", "familiar", "warm"],
        },
        sample=(
            "As a child I often spent holidays back in my hometown with my grandparents. "
            "We always went to the same breakfast stall near our old neighbourhood, and I loved the local snacks. "
            "We did that every Spring Festival, and sometimes once more in summer. "
            "Those trips felt warm and familiar, and I still miss that food."
        ),
        sampleZh=(
            "小时候假期常回老家跟爷爷奶奶住。"
            "总会去老街口那家早餐摊，特别爱吃家乡小吃。"
            "每年春节必去，夏天偶尔再回去。"
            "觉得很亲切，现在还想念那些味道。"
        ),
    )
    _p(
        "Do you prefer sitting by the window when you travel?",
        "subway_bus_commute",
        logic="先表态更喜靠窗，再对比窗边看景与过道位起身方便；地铁火车适用。",
        kitHint="出行通勤素材用于长途轨交；必须写出窗位和过道/其他座的差别。",
        words={
            "正面回答": ["Yes, the window", "Definitely window", "Prefer a window seat"],
            "来源或举例": ["watch stations pass", "aisle seat noisier", "stretch legs in aisle"],
            "频次": ["on trains and coaches", "less picky on short subway hops"],
            "感受": ["more relaxed", "journey feels shorter", "comfortable"],
        },
        sample=(
            "Yes, I prefer the window when I travel by train or coach. "
            "By the window I can watch the scenery change, and the journey feels a bit shorter. "
            "An aisle seat is easier if I need to stand up, but it feels noisier and more cramped. "
            "Personally I feel more comfortable by the window on longer trips."
        ),
        sampleZh=(
            "喜欢，坐火车或长途大巴我更想靠窗。"
            "能看窗外风景，路程也显得短一点。"
            "过道位起身方便，但更吵、也更挤。"
            "长途我还是觉得窗位更舒服。"
        ),
    )
    _p(
        "Do you prefer sitting by the window when you travel?",
        "family_car_passenger",
        logic="先答喜欢后座靠窗，再对比中间位被挡视野与驾驶位要专心路况。",
        kitHint="假期车上：后座窗位看桥和路牌，中间座视野差。",
        words={
            "正面回答": ["Back-seat window", "Yes, beside the glass", "Window if I can"],
            "来源或举例": ["count bridges", "middle seat blocked view", "dad needs the front"],
            "频次": ["on family road trips", "weekend drives"],
            "感受": ["calmer", "enjoy the view", "less car-sick"],
        },
        sample=(
            "Yes, I like the back-seat window when my family drives on holidays. "
            "I can watch fields and bridges go past, and I feel less car-sick than in the middle. "
            "The middle seat blocks the view, and the front is for my dad to focus on driving. "
            "I find the window calmer and better for enjoying the trip."
        ),
        sampleZh=(
            "喜欢，家里开车出游时我常坐后座靠窗。"
            "能看田野和桥，也比坐中间不那么晕车。"
            "中间视野被挡，前面要留给爸爸专心开车。"
            "我觉得靠窗更安静，也更适合欣赏路程。"
        ),
    )
    _p(
        "Do you prefer sitting by the window when you travel?",
        "yellow_bike_gift",
        logic="先答轨交出行喜靠窗，再对比过道位；顺带说短途骑车无座次之分。",
        kitHint="带自行车转乘时仍答火车窗位偏好；骑车本身不作窗/过道对比。",
        words={
            "正面回答": ["Window on the train", "Yes for long rides", "Not for cycling itself"],
            "来源或举例": ["bike folded nearby", "aisle for quick exit", "scenery on the line"],
            "频次": ["when I take the train out of town", "weekend trips sometimes"],
            "感受": ["more peaceful", "worth the view", "practical mix"],
        },
        sample=(
            "On a train I definitely prefer the window, especially when I take my bike for a weekend trip. "
            "I like seeing hills and villages from the glass, and the ride feels less boring. "
            "An aisle place is handier with luggage, but people walking past make it harder to rest. "
            "I feel more peaceful by the window, even if the bike sits folded beside me."
        ),
        sampleZh=(
            "坐火车我一定更想靠窗，尤其周末带着车出去玩的时候。"
            "能看山丘和村镇，旅途也不那么闷。"
            "过道旁放行李方便，但人来人往不好休息。"
            "即便自行车折在旁边，我还是觉得窗边更安静。"
        ),
    )
    _p(
        "What kind of places do you like to visit?",
        "subway_bus_commute",
        logic="先答喜去的地方类型，再说轨交方便到的城市街区或海边，再频次与感受。",
        kitHint="地铁可达的街区、博物馆、海滨——目的地在前，交通在后。",
        words={
            "正面回答": ["Historic districts", "Coastal cities", "Walkable downtown areas"],
            "原因或时间": ["easy by subway and train", "good food streets", "less driving stress"],
            "频次": ["a few times a year", "long weekends when I can"],
            "感受": ["convenient", "relaxed", "worth the ticket"],
        },
        sample=(
            "I like historic districts and coastal cities where I can walk around after I arrive. "
            "They are easy to reach by subway and train, and I enjoy small food streets without driving. "
            "I try to visit places like that a few times a year on long weekends. "
            "I find those trips convenient and relaxing."
        ),
        sampleZh=(
            "我喜欢能到了之后逛街的历史街区，还有海边城市。"
            "坐地铁和火车挺方便，也喜欢不用开车就能逛小吃街。"
            "一年会找机会去几次，多是小长假。"
            "觉得这种出行省心又放松。"
        ),
    )
    _p(
        "What kind of places do you like to visit?",
        "family_car_passenger",
        logic="先答喜自然或亲戚城市，再因家人开车适合近郊湖泊山地，频次感受跟上。",
        kitHint="全家自驾：湖泊、山地、走亲戚适合当乘客。",
        words={
            "正面回答": ["Lakes and hills", "Towns with relatives", "Scenic highways"],
            "原因或时间": ["family car makes it easy", "picnic stops", "not too far"],
            "频次": ["once or twice a season", "mainly holidays"],
            "感受": ["warm", "slow pace", "happy"],
        },
        sample=(
            "I enjoy lakes, hills and towns where we have relatives, because the pace feels slow and warm. "
            "A family car makes those places easy without rushing for tickets. "
            "We might go once or twice each holiday season. "
            "I find those passenger trips happy and unhurried."
        ),
        sampleZh=(
            "我喜欢湖泊、山景，还有有亲戚的小城，节奏慢又亲切。"
            "家里开车去这些地方不用抢车票。"
            "每个大假期大概去一两次。"
            "当乘客出游我觉得开心也不赶。"
        ),
    )
    _p(
        "What kind of places do you like to visit?",
        "hometown_local_food",
        logic="先答喜欢能吃本地小吃的地方，再讲回乡或市集原因，频次与感受。",
        kitHint="喜好目的地=有熟悉街头食物的小城/家乡，不是通勤地铁主线。",
        words={
            "正面回答": ["Food streets", "Hometown markets", "Places with local snacks"],
            "原因或时间": ["taste feels familiar", "easy to chat with family", "simple holidays"],
            "频次": ["every long holiday if I can", "sometimes short weekend trips"],
            "感受": ["happy and full", "relaxed", "worth the trip"],
        },
        sample=(
            "I like places with good local food streets and small markets. "
            "The taste feels familiar, and it is easy to chat with family while we eat. "
            "I try to go on every long holiday if I can. "
            "Those trips make me happy and relaxed, and the food alone is worth it."
        ),
        sampleZh=(
            "我喜欢有本地小吃街和小市集的地方。"
            "味道熟悉，边吃边跟家人聊天也轻松。"
            "能赶上的长假期我都会去。"
            "又开心又放松，光是吃就值了。"
        ),
    )
    _p(
        "Where would you most like to travel in the future?",
        "subway_bus_commute",
        logic="先答最想去的地方，理由可含轨交发达易逛，频次设想与期待感受。",
        kitHint="未来目的地：西南小城或江南古镇等轨交+步行友好。",
        words={
            "正面回答": ["A slower city abroad", "Southwest China", "A famous food city"],
            "原因或时间": ["good metro to explore", "after graduation", "budget travel"],
            "频次": ["maybe one longer trip", "when I save enough"],
            "感受": ["excited", "curious", "worth planning"],
        },
        sample=(
            "I would most like to travel to a famous food city in southwest China after I graduate. "
            "I imagine using the local metro to explore old streets without renting a car. "
            "I might plan one longer trip when I save enough money. "
            "I feel excited and curious, and it seems worth planning early."
        ),
        sampleZh=(
            "毕业后我最想去西南一座以美食出名的城市。"
            "想靠当地地铁逛老街，不用租车。"
            "攒点钱后也许安排一次稍长的旅行。"
            "又期待又好奇，觉得值得提前规划。"
        ),
    )
    _p(
        "Where would you most like to travel in the future?",
        "family_car_passenger",
        logic="先答想和家人自驾的目的地，原因时间、多久去一次、感受。",
        kitHint="未来仍可用全家公路旅行：草原、高原湖等适合坐后座梦想。",
        words={
            "正面回答": ["Grassland or high lake", "Western routes", "National park edge"],
            "原因或时间": ["family road trip dream", "dad would drive", "photos together"],
            "频次": ["maybe once after work starts", "long holiday only"],
            "感受": ["hopeful", "shared memory", "relaxing"],
        },
        sample=(
            "I would love a family road trip to a grassland or high lake in the west one day. "
            "My dad would drive while we stop for photos and simple hikes. "
            "I hope we can do it once after I start work and have a long holiday. "
            "I find that idea hopeful and relaxing as a shared memory."
        ),
        sampleZh=(
            "希望以后能和家人自驾去西部草原或高原湖泊。"
            "爸爸开车，我们一路停车拍照、散散步。"
            "工作后有一次长假就想实现。"
            "觉得是温馨又放松的共同回忆。"
        ),
    )
    _p(
        "Where would you most like to travel in the future?",
        "yellow_bike_gift",
        logic="先答想骑车环游型目的地，如岛国小城或环岛绿道，原因频次感受。",
        kitHint="黄车挂「骑行旅行」梦想，不同于日常上学。",
        words={
            "正面回答": ["A cycling island", "Scenic bike route", "Small coastal towns"],
            "原因或时间": ["love slow travel", "ride my own pace", "after exams"],
            "频次": ["one dedicated trip", "maybe with a friend"],
            "感受": ["free", "adventurous", "memorable"],
        },
        sample=(
            "I would most like to travel to a place with a famous coastal bike route, maybe with a friend. "
            "I could ride at my own pace and stop whenever the view looks good. "
            "I imagine doing it once as a reward after a big exam period. "
            "I think it would feel free, adventurous and memorable."
        ),
        sampleZh=(
            "我最想去有海边骑行路线的地方，也许和朋友一起。"
            "可以按自己的节奏骑，风景好就停下来。"
            "想在大考之后当奖励去一次。"
            "会觉得自由、有点冒险，也很难忘。"
        ),
    )
    _p(
        "How often do you travel?",
        "subway_bus_commute",
        logic="行为习惯：先答频率不高或偶尔，因学业忙；再写长假坐轨交出游的流程与影响。",
        kitHint="学生常态：平时少出游，寒暑假才坐火车地铁远门。",
        words={
            "正面回答": ["Not very often", "A few times a year", "Mainly holidays"],
            "原因": ["busy with study", "tickets cost money", "short breaks stay local"],
            "时间线+行为描述": ["check train apps", "subway to the station", "two-day city breaks"],
            "影响": ["recharged", "manageable budget", "look forward to breaks"],
        },
        sample=(
            "Honestly I do not travel very often because campus life keeps me busy. "
            "I usually wait for winter or summer break, book trains on my phone, and take the subway to the station first. "
            "That might happen two or three times a year for short city breaks. "
            "Those trips recharge me without breaking my student budget too much."
        ),
        sampleZh=(
            "说实话不常旅行，学校事情多。"
            "一般等寒暑假在手机订票，再坐地铁去火车站。"
            "一年大概两三次短途城市游。"
            "能缓口气，也不太超支。"
        ),
    )
    _p(
        "How often do you travel?",
        "family_car_passenger",
        logic="先答一年几次家人自驾，原因学业紧，再写放假上车去亲戚或景区，影响是陪伴感。",
        kitHint="全家开车决定出游次数：春节、国庆为主要窗口。",
        words={
            "正面回答": ["A few family trips", "Twice a year maybe", "Holidays only"],
            "原因": ["parents' schedule", "school terms", "shared car"],
            "时间线+行为描述": ["pack the night before", "dad drives highways", "stay with relatives"],
            "影响": ["closer as a family", "simple habits", "good rest"],
        },
        sample=(
            "I travel with my family only a few times a year, mainly at spring festival and summer. "
            "We pack the night before, and my dad handles the long highway driving. "
            "We often stay with relatives or visit a nearby scenic spot for two days. "
            "Those rides keep us closer and give me a proper rest from study."
        ),
        sampleZh=(
            "一年也就和家人出门几次，多是春节和暑假。"
            "前一晚会收拾行李，长途路段爸爸开车。"
            "常去亲戚家或附近景区住两天。"
            "路上相处多，也能从学习里彻底休息一下。"
        ),
    )
    _p(
        "How often do you travel?",
        "yellow_bike_gift",
        logic="先答周末近郊骑车小游算轻旅行，原因省钱锻炼，行为周末流程，影响放松。",
        kitHint="黄车：把周末骑行近郊算作低频「出游」，仍 honesty 说不大远行。",
        words={
            "正面回答": ["Light trips at weekends", "Not far", "Rare long holidays"],
            "原因": ["keep fit", "save money", "bike is ready"],
            "时间线+行为描述": ["ride to a nearby town", "train plus bike sometimes", "one-day loops"],
            "影响": ["less stress", "fresh air", "enough for now"],
        },
        sample=(
            "I rarely take big holidays, but I do light trips at weekends when the weather is good. "
            "Sometimes I cycle to a nearby town, or take a short train and ride my yellow bike there. "
            "That might be once or twice a month as a one-day loop. "
            "It reduces stress and gives me fresh air, which is enough for now."
        ),
        sampleZh=(
            "长假不常去，但天气好周末会就近玩一下。"
            "有时骑到邻镇，有时短途火车再骑车。"
            "一个月大概一两次一日小环线。"
            "能减压透气，目前我也挺满足。"
        ),
    )
    _p(
        "Do you prefer travelling alone or with other people?",
        "subway_bus_commute",
        logic="对比类：先表态更喜结伴或独行，再分述各选项特点，最后个人感受。",
        kitHint="轨交出游：结伴拼车票攻略；独行灵活但略孤单。",
        words={
            "正面回答": ["With other people", "Mostly with friends", "Depends on distance"],
            "选项1的特点与作用": ["share plans", "split costs", "safer at night stations"],
            "选项2的特点与作用": ["flexible timetable", "quiet thinking", "solo tickets easier"],
            "个人感受": ["companionship wins", "balance both", "happy with friends"],
        },
        sample=(
            "I usually prefer travelling with other people, especially on trains where plans are easier to share. "
            "With friends we split costs, chat on the ride, and feel safer arriving at a new station at night. "
            "Travelling alone is more flexible, but long rides can feel a bit lonely. "
            "Overall I feel happier with company on most trips."
        ),
        sampleZh=(
            "我多数时候更喜欢和别人一起，坐火车时好一起商量行程。"
            "朋友可以分摊费用，路上聊天，晚上到新站也更安心。"
            "一个人时间自由，但坐久了会有点孤单。"
            "总的来说大部分旅程有伴我更开心。"
        ),
    )
    _p(
        "Do you prefer travelling alone or with other people?",
        "family_car_passenger",
        logic="对比独自背包与与家人自驾：后座聊天 vs 自己订全部行程，谈个人感受。",
        kitHint="全家车旅天然是「与他人同行」素材，也可坦诚说偶尔想独处。",
        words={
            "正面回答": ["With family on road trips", "Sometimes alone for city breaks", "Mostly with others"],
            "选项1的特点与作用": ["shared music", "no ticket stress", "warm meals together"],
            "选项2的特点与作用": ["choose my own pace", "light backpack", "meet new people"],
            "个人感受": ["family trips cozy", "solo OK short trips", "mix is fine"],
        },
        sample=(
            "On long road trips I prefer travelling with my family because the car feels cozy and shared. "
            "We listen to the same playlists, stop for meals together, and nobody worries about tickets. "
            "Alone city breaks let me choose museums and cafes at my own pace, but I miss talking in the car. "
            "I like family trips most, yet a short solo visit now and then is fine too."
        ),
        sampleZh=(
            "长途自驾我更喜欢和家人一起，车里气氛温馨。"
            "一起听歌、停车吃饭，也不用各自抢票。"
            "一个人城市短途能按自己节奏逛馆喝咖啡，但会想念车里聊天。"
            "多数时候爱合家出游，偶尔独行短途也可以。"
        ),
    )
    _p(
        "Do you prefer travelling alone or with other people?",
        "yellow_bike_gift",
        logic="对比独自骑行与友伴同骑：速度默契 vs 自由停点，个人感受落点。",
        kitHint="骑行旅行：可结伴可单飞，写清两种骑法差别。",
        words={
            "正面回答": ["With a close friend", "Sometimes solo", "Depends on route"],
            "选项1的特点与作用": ["motivate each other", "share repair tools", "photos together"],
            "选项2的特点与作用": ["stop anywhere", "own speed", "quiet thinking"],
            "个人感受": ["friend for long routes", "solo for short", "both enjoyable"],
        },
        sample=(
            "For a long bike route I prefer going with a close friend so we can motivate each other uphill. "
            "We share snacks, repair tools, and take photos when the view is good. "
            "Riding alone on a short path lets me stop anywhere without waiting, which feels peaceful. "
            "Both styles are enjoyable, but I pick a friend when the trip is tiring."
        ),
        sampleZh=(
            "长一点的骑行路线我更喜欢和熟朋友一起，上坡能互相打气。"
            "可以分零食、共用修车工具，好景一起拍照。"
            "短途独自骑想停就停，挺安静。"
            "两种方式都喜欢，太累的路程我会选有伴。"
        ),
    )