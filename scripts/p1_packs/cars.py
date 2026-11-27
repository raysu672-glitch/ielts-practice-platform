# -*- coding: utf-8 -*-
"""Cars Freestyle packs (preview-page style)."""


def register(_p):
    _p(
        "Do you have a car?",
        "subway_bus_commute",
        logic="先答没有自己的车，说明日常地铁公交通勤，再对比以后想开车的想法。",
        kitHint="地铁通勤素材：诚实无车，出行靠轨交与公交，仍完整回答「有车吗」。",
        words={
            "正面回答": ["No, not my own", "I am a student", "Family has one"],
            "来源或举例": ["subway line", "bus from the station", "student ID discount"],
            "频次": ["twice a day on school days", "rush hour sometimes"],
            "感受": ["cheap and reliable", "hope to drive later"],
        },
        sample=(
            "No, I do not have my own car — I am still a student. "
            "I usually take the subway and then a short bus ride to campus. "
            "I do that twice a day on weekdays, even when rush hour is crowded. "
            "It is cheap and reliable, though I would like to learn to drive in a few years."
        ),
        sampleZh=(
            "没有，我还没自己的车，还是学生。"
            "平时先坐地铁，再换一小段公交到学校。"
            "工作日每天往返，高峰有时很挤。"
            "省钱也准时，不过几年后想学开车。"
        ),
    )
    _p(
        "Do you have a car?",
        "family_car_passenger",
        logic="先答家里有车但非自己的，再讲假期当乘客出行，顺带说暂无驾照。",
        kitHint="全家开车：父亲或家人有车，本人坐车多，区分「家里有」和「我有」。",
        words={
            "正面回答": ["Not mine", "My dad drives", "We share one family car"],
            "来源或举例": ["weekend trips", "supermarket runs", "holiday highways"],
            "频次": ["a few times a month", "longer drives in summer"],
            "感受": ["comfortable as passenger", "want my licence someday"],
        },
        sample=(
            "I do not have a car of my own, but my family has one and my dad usually drives. "
            "I often sit in the back on weekend trips to the supermarket or relatives' homes. "
            "In summer we might take longer highway drives a few times. "
            "I enjoy being a passenger for now, but I hope to get a licence later."
        ),
        sampleZh=(
            "我自己没车，但家里有一辆，大多是爸爸开。"
            "周末去超市或走亲戚我常坐后座。"
            "夏天偶尔会开更远的高速几次。"
            "当乘客挺舒服，以后也想考驾照。"
        ),
    )
    _p(
        "What do you remember about car journeys as a child?",
        "hometown_local_food",
        logic="先回忆坐车回乡，再写路上细节与到家吃小吃，频率与感受跟车程走。",
        kitHint="回乡小吃线：爸妈开车回老家、服务区零食、到家吃熟悉摊位——必须是 car，不能改答大巴。",
        words={
            "正面回答": ["Yes, holiday car trips", "Back to my hometown", "Snacks in the car"],
            "来源或举例": ["my dad driving", "rest-stop snacks", "breakfast stall near home"],
            "频次": ["every Spring Festival", "once or twice a year"],
            "感受": ["a bit long but happy", "the food made it worth it"],
        },
        sample=(
            "Yes — I remember car trips back to my hometown when I was a kid. "
            "My dad drove, and my mum packed snacks; we always stopped for a quick bite near our old neighbourhood. "
            "We did that every Spring Festival, and maybe once more in summer. "
            "The ride felt long, but I was happy because hometown food was waiting."
        ),
        sampleZh=(
            "记得小时候坐车回老家。"
            "爸爸开车，妈妈带零食，到老街口那家早餐摊总会停一下。"
            "每年春节一次，夏天偶尔再去。"
            "路有点长，但想到家乡小吃就开心。"
        ),
    )
    _p(
        "What do you remember about car journeys as a child?",
        "family_car_passenger",
        logic="聚焦家人开车出游的具体画面：谁开车、去哪、车上玩什么。",
        kitHint="假期乘客视角：后座看风景、父亲放歌，天然适合「童年车程」。",
        words={
            "正面回答": ["Back seat view", "Dad's driving", "Singing along"],
            "来源或举例": ["sea-side cities", "toll stations", "comic books in the car"],
            "频次": ["summer holidays", "once or twice a summer"],
            "感受": ["safe and happy", "miss those slow trips"],
        },
        sample=(
            "What sticks in my mind is sitting in the back while my dad drove us to nearby cities in summer. "
            "He played old songs on the radio, and I read comics or counted bridges out of the window. "
            "We might do one or two of those trips each holiday. "
            "I felt safe and happy, and I kind of miss how slow and relaxed those journeys were."
        ),
        sampleZh=(
            "印象最深是夏天爸爸开车带我们周边城市玩，我坐在后面。"
            "车里放着老歌，我看漫画或数桥。"
            "每个假期大概一两次。"
            "觉得很安心开心，也怀念那种慢悠悠的路途。"
        ),
    )
    _p(
        "What kind of car would you like to own?",
        "subway_bus_commute",
        logic="先描述理想车型，理由来自通勤痛点（挤、远），地铁经历作对比动机。",
        kitHint="地铁素材引出「以后想要小巧省油、好停车」的车，地铁仅作 contrast。",
        words={
            "正面回答": ["A small electric car", "Easy to park", "Not too expensive"],
            "原因或时间": ["after I graduate", "tired of rush-hour crowds", "short city trips"],
            "频次": ["would use daily for work", "weekend drives sometimes"],
            "感受": ["more freedom", "worth saving for"],
        },
        sample=(
            "I would like a small electric car that is easy to park in the city. "
            "After I graduate and start work, I am tired of squeezing onto the subway every rush hour. "
            "I would use it daily for commuting and maybe short weekend trips. "
            "It would give me more freedom, so I think it is worth saving up for."
        ),
        sampleZh=(
            "我想要一辆好停放的小纯电动车。"
            "毕业后上班不想天天高峰挤地铁。"
            "平时通勤，周末短途也能开。"
            "更自由，值得攒钱买。"
        ),
    )
    _p(
        "What kind of car would you like to own?",
        "family_car_passenger",
        logic="先答想要的家庭用车类型，联系假期全家出游经验说空间与舒适。",
        kitHint="全家出游经历支撑「大空间 SUV、能装行李」的喜好。",
        words={
            "正面回答": ["A comfy SUV", "Room for family", "Good boot space"],
            "原因或时间": ["learn to drive first", "copy what worked on trips", "within budget"],
            "频次": ["family outings monthly", "long drives on holidays"],
            "感受": ["practical dream", "excited to plan routes"],
        },
        sample=(
            "I would love a comfortable SUV with space for my parents and luggage. "
            "Our family trips taught me that a bigger boot makes holidays much easier. "
            "Once I pass my driving test, I would use it for monthly family outings and longer holiday drives. "
            "It is a practical dream, and I already enjoy planning routes on maps."
        ),
        sampleZh=(
            "我想要一辆舒服的 SUV，能坐下家人还能装行李。"
            "全家出游让我觉得大后备箱特别省事。"
            "考完驾照后想每月家庭出门、假期跑远点。"
            "务实一点的梦想，我已经爱在地图上排路线了。"
        ),
    )
    _p(
        "How do you usually get around your city?",
        "subway_bus_commute",
        logic="正面说主要交通方式，按时间线描述典型一天，再讲高峰影响。",
        kitHint="地铁公交是本题主轴；措辞直接用 PDF 里的 subway / bus / rush hour。",
        words={
            "正面回答": ["Subway first", "Then a bus", "Walking the last bit"],
            "原因": ["fast in traffic", "student discount", "station near home"],
            "时间线+行为描述": ["leave after breakfast", "transfer at one stop", "arrive before class"],
            "影响": ["usually on time", "crowded but cheap"],
        },
        sample=(
            "I usually use the subway and then take a bus for the last part. "
            "The station is about a ten-minute walk from home, and the student card saves money. "
            "On a normal school day I leave after breakfast, transfer once, and arrive before the first class. "
            "Rush hour is crowded, but it is still cheaper and more predictable than taxis."
        ),
        sampleZh=(
            "我主要坐地铁，最后再换一段公交。"
            "家到站点步行十来分钟，学生卡也省钱。"
            "平常吃完早饭出门，换乘一次，赶在第一节课前到。"
            "高峰很挤，但比打车便宜也更可控。"
        ),
    )
    _p(
        "How do you usually get around your city?",
        "family_car_passenger",
        logic="分场景：平日轨交，周末或采购时坐家里车，形成完整出行习惯。",
        kitHint="全家开车补「非日常」场景；平日仍可交代地铁，但车是补充细节。",
        words={
            "正面回答": ["Mix of modes", "Public transport weekdays", "Family car weekends"],
            "原因": ["dad needs the car for work", "subway faster alone", "shopping needs space"],
            "时间线+行为描述": ["bike to station weekdays", "car for big shops Saturday"],
            "影响": ["flexible routine", "less stress carrying bags"],
        },
        sample=(
            "On weekdays I still take the subway to school because it is faster when I am alone. "
            "On Saturdays my dad often drives if we buy heavy things or visit relatives across town. "
            "I walk or cycle to the station in the morning, and I sit in the passenger seat on family errands. "
            "That mix keeps my routine flexible and saves me from carrying huge bags on the train."
        ),
        sampleZh=(
            "工作日我一个人还是坐地铁上学，比较快。"
            "周六买东西多或跨城走亲戚时常常爸爸开车。"
            "早上步行或骑车去站点，家里办事我就坐副驾驶。"
            "这样安排灵活，也不用提着大包挤地铁。"
        ),
    )
    _p(
        "How do you think cars will change in the future?",
        "subway_bus_commute",
        logic="先总述电动化与共享化，用本市地铁扩建造对比，谈对出行格局的影响。",
        kitHint="地铁视角看未来：车更绿、更少私有，轨交与小车分工更清。",
        words={
            "正面回答": ["More electric", "Smarter systems", "Fewer private owners maybe"],
            "举例或原因": ["battery progress", "subway networks growing", "ride apps"],
            "作用或影响": ["cleaner air downtown", "less parking pressure"],
            "感受": ["hopeful", "still need good transit"],
        },
        sample=(
            "I think cars will become more electric and connected, with software handling a lot of driving tasks. "
            "At the same time, cities like mine keep extending subway lines, so some trips may shift to rail. "
            "That could mean cleaner air downtown and less pressure to find parking. "
            "I feel hopeful, but good public transport still needs to grow with those changes."
        ),
        sampleZh=(
            "我觉得车会更电动、更智能，很多驾驶任务交给软件。"
            "我们城市地铁也在延长，部分出行会转到轨交。"
            "市中心空气和停车压力可能都会好转。"
            "我挺乐观，但公交地铁也得同步跟上。"
        ),
    )
    _p(
        "How do you think cars will change in the future?",
        "family_car_passenger",
        logic="从家庭用车需求出发谈自动驾驶、安全与长途体验的变化。",
        kitHint="假期公路旅行经验用来举例未来车内娱乐与辅助驾驶。",
        words={
            "正面回答": ["Safer motorways", "More driver assistance", "Better in-car tech"],
            "举例或原因": ["family road trips", "tired drivers", "navigation updates"],
            "作用或影响": ["fewer accidents", "more relaxing holidays"],
            "感受": ["excited but cautious", "rules must keep up"],
        },
        sample=(
            "I imagine future family cars will be much safer on motorways, with sensors watching tired drivers. "
            "When we drive for holidays, maps and music already update live — that will only get smoother. "
            "Passengers might relax or chat more while the car handles boring highway stretches. "
            "I am excited about that, but laws and training need to keep up so people trust the technology."
        ),
        sampleZh=(
            "以后家用车上高速应该更安全，系统能发现司机疲劳。"
            "我们度假自驾时导航和音乐已实时更新，以后会更顺。"
            "枯燥高速段可能交给辅助驾驶，乘客更能休息聊天。"
            "我很期待，但法规培训也得跟上，大家才信得过。"
        ),
    )
    _p(
        "Do you prefer to be a driver or a passenger?",
        "family_car_passenger",
        logic="对比题：先亮明更爱当乘客，分别写开车与坐车特点，落在家庭出游感受。",
        kitHint="假期坐车舒服、不看路，是「乘客派」切口；开车留到选项对比。",
        words={
            "正面回答": ["Passenger for now", "Not ready to drive long trips"],
            "选项1的特点与作用": ["driver: control and timing", "needs focus and licence"],
            "选项2的特点与作用": ["passenger: rest and enjoy view", "chat with family"],
            "个人感受": ["less stress", "happy to help navigate"],
        },
        sample=(
            "For now I prefer being a passenger, especially on family holidays. "
            "As a driver you must watch every lane and stay calm in traffic, which takes a lot of focus. "
            "As a passenger I can nap, enjoy the scenery, or help with navigation and snacks. "
            "That feels less stressful, so I am happy in the back seat until I am a confident driver."
        ),
        sampleZh=(
            "眼下我更喜欢当乘客，尤其是全家出游。"
            "开车得一直盯路、堵车也不能慌，很费神。"
            "坐车可以打盹、看风景，或帮忙导航、分零食。"
            "压力小很多，驾照练熟前我都愿坐后排。"
        ),
    )
    _p(
        "Do you prefer to be a driver or a passenger?",
        "subway_bus_commute",
        logic="先表态短期偏好乘客/坐车，对比自己将来想开车的原因与地铁习惯。",
        kitHint="地铁通勤者：现阶段不爱开车堵路，但未来想自己握方向盘；选项对比要清晰。",
        words={
            "正面回答": ["Passenger today", "Driver maybe later"],
            "选项1的特点与作用": ["driver: freedom and direct routes", "parking headaches"],
            "选项2的特点与作用": ["passenger on transit: read or rest", "no fuel worries"],
            "个人感受": ["practical choice now", "curious to try driving"],
        },
        sample=(
            "Right now I prefer being a passenger, whether on the subway or in a friend's car. "
            "Driving looks free because you choose the route, but parking and fuel are headaches in a big city. "
            "On the train I can read or rest without watching the road. "
            "Later, when I have more experience, I would like to try driving myself for short trips."
        ),
        sampleZh=(
            "目前我更愿意当乘客，坐地铁或坐朋友车都一样。"
            "开车看似自由选路线，但在大城市停车加油都烦。"
            "坐地铁我能看书休息，不用看路。"
            "以后有经验了，短途也想自己试开一开。"
        ),
    )