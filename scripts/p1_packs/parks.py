# -*- coding: utf-8 -*-
"""Public gardens and parks Freestyle packs."""


def register(_p):
    _p(
        "Is there a park near your home?",
        "nearby_park_walk",
        logic="先肯定有/没有，再描述步行距离与常在园内做什么，频次感受。",
        kitHint="附近公园散步：10分钟步行+傍晚透气为主线。",
        words={
            "正面回答": ["Yes, quite near", "About ten minutes' walk", "A small city park"],
            "来源或举例": ["trees and paths", "evening stroll", "bench after study"],
            "频次": ["most evenings", "when I need fresh air"],
            "感受": ["convenient", "calming", "practical"],
        },
        sample=(
            "Yes, there is a small park about a ten-minute walk from my home. "
            "I go there for fresh air after study, usually along the tree-lined paths. "
            "I visit most evenings when I am not too busy. "
            "I find that park convenient and calming."
        ),
        sampleZh=(
            "有，步行大概十分钟有个小公园。"
            "学习后会去透气，常走树下的路。"
            "不太忙时多数傍晚会去。"
            "觉得很近，也让人平静。"
        ),
    )
    _p(
        "Is there a park near your home?",
        "yellow_bike_gift",
        logic="先答附近有公园，再写骑车几分钟到门口、在园内简要活动；车是代步。",
        kitHint="黄车仅作「怎么去公园」，公园本身仍是答题核心。",
        words={
            "正面回答": ["Yes, nearby", "Five minutes by bike", "Not huge but useful"],
            "来源或举例": ["ride my yellow bike", "park at the gate", "short loop inside"],
            "频次": ["at weekends", "when the weather is clear"],
            "感受": ["quick access", "light exercise", "handy"],
        },
        sample=(
            "Yes, a park near my home is only about five minutes away by bike. "
            "I ride my yellow bike to the gate and then walk or cycle slowly on the inner path. "
            "I do that mainly at weekends when the weather is clear. "
            "I find it a handy way to get green space without a long trip."
        ),
        sampleZh=(
            "有，骑车大概五分钟就到家门口附近的公园。"
            "骑小黄车到门口，再在园内慢骑或散步。"
            "天气晴好时周末常去。"
            "不用跑远就能接触绿化，很方便。"
        ),
    )
    _p(
        "Is there a park near your home?",
        "light_sports_walk",
        logic="先答公园距离，再强调可在园内慢跑拉伸，频次与运动感受。",
        kitHint="轻运动：公园=散步慢跑场地，而非别的场所。",
        words={
            "正面回答": ["Yes, walking distance", "Good for jogs", "Open paths"],
            "来源或举例": ["warm-up laps", "stretching", "quiet corners"],
            "频次": ["twice a week", "before or after study"],
            "感受": ["keeps me active", "simple", "refreshing"],
        },
        sample=(
            "Yes, there is a park within walking distance that has open paths for light exercise. "
            "I sometimes jog a slow lap or stretch near the benches after sitting all day. "
            "I try to go there about twice a week. "
            "It keeps me active in a simple, refreshing way."
        ),
        sampleZh=(
            "有，走路能到，跑道和空地适合轻运动。"
            "有时会慢跑一圈，或在长椅旁拉伸。"
            "大概一周两次。"
            "用很简单的方式保持活动，人也会清爽些。"
        ),
    )
    _p(
        "What did you do in parks when you were a child?",
        "nearby_park_walk",
        logic="童年公园活动优先：跑玩、踢球、散步；再频次与怀旧感受。",
        kitHint="公园玩耍记忆：朋友、草坪、傍晚散步。",
        words={
            "正面回答": ["Ran around", "Played simple games", "Walked with parents"],
            "来源或举例": ["grass field", "friends after school", "feed the fish"],
            "频次": ["after school often", "weekends with family"],
            "感受": ["happy", "free", "good memories"],
        },
        sample=(
            "As a child I mostly ran around on the grass and played tag with friends after school. "
            "Sometimes my parents walked me there to feed the fish in a small pond. "
            "I went quite often on weekdays and at weekends. "
            "I have happy, free memories of that park."
        ),
        sampleZh=(
            "小时候我常在草地上跑，和同学玩追逐游戏。"
            "爸妈有时也会带我去喂小池子里的鱼。"
            "工作日和周末都经常去。"
            "是很开心、很自由的回忆。"
        ),
    )
    _p(
        "What did you do in parks when you were a child?",
        "yellow_bike_gift",
        logic="先写园内骑车、学平衡；再写骑车到公园；童年频次感受。",
        kitHint="黄车在公园=骑行玩乐，不是上学路上主讲。",
        words={
            "正面回答": ["Cycled slowly", "Practised turns", "Rode with friends"],
            "来源或举例": ["yellow birthday bike", "wide park path", "stop at the fountain"],
            "频次": ["many weekends", "when homework finished"],
            "感受": ["proud", "a bit of freedom", "fun"],
        },
        sample=(
            "In the park I practised cycling on wide paths with my small yellow bike. "
            "I learned to turn slowly and sometimes raced with classmates near the fountain. "
            "I did that on many weekends after I finished homework. "
            "I felt proud and it was real fun for a kid."
        ),
        sampleZh=(
            "在公园里我骑着黄色小自行车在宽路上练拐弯。"
            "还在喷泉附近和同学慢慢比过谁骑得稳。"
            "很多周末写完作业就会去。"
            "小朋友觉得很自豪，也很好玩。"
        ),
    )
    _p(
        "What did you do in parks when you were a child?",
        "light_sports_walk",
        logic="童年在公园慢跑、踢球、跳绳等活动，再时间频次与感受。",
        kitHint="运动向童年公园：踢毽子、慢跑，不是谈健身房为主。",
        words={
            "正面回答": ["Kicked a ball", "Skipped rope", "Chased on the track"],
            "来源或举例": ["school sports day practice", "simple team games", "PE homework"],
            "频次": ["twice a week after school", "more in summer"],
            "感受": ["tiring but fun", "healthy habit", "close friends"],
        },
        sample=(
            "I often kicked a ball or skipped rope with classmates on the open ground in the park. "
            "Sometimes we practised for school sports day on the small track. "
            "We met there about twice a week after school, more often in summer. "
            "It was tiring but fun, and it started a healthy habit with close friends."
        ),
        sampleZh=(
            "我常和同学在公园空地踢球、跳绳。"
            "有时还在小跑道上练运动会项目。"
            "放学大概一周两次，夏天更频繁。"
            "虽累但开心，也和好友养成了运动习惯。"
        ),
    )
    _p(
        "What do you like to do in a park?",
        "nearby_park_walk",
        logic="喜好类：先说喜欢在公园散步听鸟声，原因、频次、感受。",
        kitHint="现行习惯：傍晚散步解压。",
        words={
            "正面回答": ["Take a walk", "Listen to birds", "Clear my head"],
            "原因或时间": ["quiet after class", "no ticket needed", "close to home"],
            "频次": ["most evenings", "longer on Sunday"],
            "感受": ["peaceful", "helps me reset", "simple"],
        },
        sample=(
            "I like taking a slow walk and listening to birds in the park after class. "
            "It is quiet, free, and only minutes from my dorm. "
            "I do it most evenings, sometimes longer on Sunday. "
            "I find it peaceful and it helps me reset."
        ),
        sampleZh=(
            "下课后我喜欢在公园里慢走，听听鸟叫。"
            "安静、不用门票，离宿舍也近。"
            "多数晚上会去，周日有时待久一点。"
            "很平静，能让我把脑子清空一下。"
        ),
    )
    _p(
        "What do you like to do in a park?",
        "yellow_bike_gift",
        logic="先说喜欢在园内骑行一圈，原因锻炼；周末频次；放松感受。",
        kitHint="骑车是园内活动，答案仍扣「在公园做什么」。",
        words={
            "正面回答": ["Cycle a loop", "Ride slowly", "Feel the breeze"],
            "原因或时间": ["fresh air", "light workout", "escape screens"],
            "频次": ["at weekends", "about an hour"],
            "感受": ["unwinding", "keeps me fit", "enjoyable"],
        },
        sample=(
            "I like cycling a slow loop on the wide path inside the park. "
            "The air feels fresher there, and it is a light workout without a gym fee. "
            "I usually ride for about an hour at weekends. "
            "I find it enjoyable and it helps me unwind from screens."
        ),
        sampleZh=(
            "我喜欢在公园宽路上慢慢骑一圈。"
            "空气更好，也像轻度锻炼，还不用办卡。"
            "周末一般会骑大约一小时。"
            "挺享受，也能从屏幕前抽离一下。"
        ),
    )
    _p(
        "What do you like to do in a park?",
        "light_sports_walk",
        logic="先说喜欢慢跑或拉伸，再写原因时间和频次感受。",
        kitHint="园内运动：慢跑、拉伸、简单体能。",
        words={
            "正面回答": ["Jog slowly", "Stretch", "Do light sports"],
            "原因或时间": ["sit too long in class", "free open ground", "meet a friend to run"],
            "频次": ["two or three times a week", "before dinner"],
            "感受": ["energised", "clear head", "healthy"],
        },
        sample=(
            "I like jogging slowly and stretching on the open ground in the park. "
            "After long classes my legs feel stiff, and the park is free and close. "
            "I go there two or three times a week, usually before dinner. "
            "I feel more energised and my head stays clearer."
        ),
        sampleZh=(
            "我喜欢在公园空地上慢跑和做拉伸。"
            "课上坐久了腿发僵，公园又近又不用花钱。"
            "一周两三天，多在晚饭前去。"
            "人会精神些，脑子也更清醒。"
        ),
    )
    _p(
        "Did you like going to parks as a child?",
        "nearby_park_walk",
        logic="喜好童年公园：喜欢、原因有朋友和草地、频次、美好回忆。",
        kitHint="步行逛公园童年喜好，黄车不抢戏。",
        words={
            "正面回答": ["Yes, really", "Loved it", "One of my favourite places"],
            "原因或时间": ["grass to run on", "parents walked with me", "peaceful after school"],
            "频次": ["quite often", "many weekends"],
            "感受": ["warm memories", "still like parks", "relaxed"],
        },
        sample=(
            "Yes, I really liked going to parks as a child. "
            "There was grass to run on and my parents sometimes walked with me after school. "
            "I went quite often on weekends. "
            "I still have warm memories, and I like parks now as well."
        ),
        sampleZh=(
            "喜欢，小时候很喜欢去公园。"
            "有大草地能跑，爸妈有时放学后会陪我走走。"
            "周末经常去。"
            "回忆很暖，现在我也仍爱去公园。"
        ),
    )
    _p(
        "Did you like going to parks as a child?",
        "yellow_bike_gift",
        logic="喜欢因能在园内骑车；原因礼物车后常去；频次；自由感感受。",
        kitHint="童年喜欢公园=在那里骑车玩。",
        words={
            "正面回答": ["Yes, especially for cycling", "Loved the paths", "Felt free"],
            "原因或时间": ["got my yellow bike", "junior high", "wide paths in summer"],
            "频次": ["many weekends", "after homework"],
            "感受": ["independent", "fun", "good memories"],
        },
        sample=(
            "Yes, especially after I got my small yellow bike in junior high. "
            "The park had wide paths where I could practise riding without busy traffic. "
            "I went there on many weekends when homework was done. "
            "It felt independent and fun, and I still remember that freedom."
        ),
        sampleZh=(
            "喜欢，尤其初中收到黄色小自行车之后更喜欢。"
            "公园路宽，练车不怕和大马路车挤在一起。"
            "很多周末做完作业就去。"
            "有种独立感也很好玩，还记得那种自由。"
        ),
    )
    _p(
        "Did you like going to parks as a child?",
        "light_sports_walk",
        logic="喜欢因在公园运动游戏；原因小伙伴；频次；健康开心感受。",
        kitHint="童年公园=踢球跳绳，不是健身房。",
        words={
            "正面回答": ["Yes, for games", "Loved sports there", "Always active"],
            "原因或时间": ["classmates met there", "school sports practice", "summer evenings"],
            "频次": ["twice a week", "more in holidays"],
            "感受": ["energetic", "close friends", "healthy fun"],
        },
        sample=(
            "Yes, I liked parks because we played ball games and skipped rope with classmates. "
            "We sometimes practised for sports day on the park track in summer evenings. "
            "That was about twice a week, more in holidays. "
            "It felt energetic, healthy fun with close friends."
        ),
        sampleZh=(
            "喜欢，可以和同学在公园踢球、跳绳。"
            "夏天傍晚有时在跑道练运动会。"
            "大概一周两次，假期更勤。"
            "和好友一起动起来，又健康又开心。"
        ),
    )
    _p(
        "How often do you go to parks?",
        "nearby_park_walk",
        logic="行为习惯：频率+原因解压+傍晚散步行为+影响。",
        kitHint="学生晚饭后公园散步重置状态。",
        words={
            "正面回答": ["Quite often", "Several times a week", "Almost every week"],
            "原因": ["need fresh air", "near home", "cheap break"],
            "时间线+行为描述": ["walk after dinner", "ten-minute loop", "phone away"],
            "影响": ["sleep better", "less stressed", "easy habit"],
        },
        sample=(
            "I go to a nearby park several times a week, usually after dinner. "
            "I take a short loop with my phone away to clear my head from study. "
            "It is close, so the habit is easy to keep. "
            "I sleep a bit better and feel less stressed."
        ),
        sampleZh=(
            "一周会去附近公园好几次，多半是晚饭后。"
            "绕一小圈，把手机放下，让脑子从学习里出来。"
            "很近，所以习惯好坚持。"
            "睡眠好一点，压力也小些。"
        ),
    )
    _p(
        "How often do you go to parks?",
        "yellow_bike_gift",
        logic="频率以周末骑车去公园为主；原因锻炼；行为描述；放松影响。",
        kitHint="骑车到公园或园内骑，频率仍是「去公园」。",
        words={
            "正面回答": ["Most weekends", "About once a week", "When weather is fine"],
            "原因": ["light exercise", "same park route", "unwind"],
            "时间线+行为描述": ["ride to the gate", "slow lap inside", "about an hour"],
            "影响": ["fitter", "less screen time", "refreshed"],
        },
        sample=(
            "I visit a park about once a week, mostly at weekends when the weather is fine. "
            "I ride my yellow bike to the gate and do a slow lap inside for around an hour. "
            "It is my simple exercise without going far. "
            "I feel fitter, use screens less, and come back refreshed."
        ),
        sampleZh=(
            "大概一周去一次公园，晴好周末居多。"
            "骑小黄车到门口，在园里慢慢骑一圈，大约一小时。"
            "不用跑远就算锻炼了。"
            "身体轻松些，少刷手机，回来也清爽。"
        ),
    )
    _p(
        "How often do you go to parks?",
        "light_sports_walk",
        logic="一周慢跑几次；原因久坐；行为；体能影响。",
        kitHint="去公园=去运动，频率按锻炼算。",
        words={
            "正面回答": ["Two or three times a week", "Regular but not daily", "Before exams more"],
            "原因": ["sitting all day", "free track", "meet a running buddy"],
            "时间线+行为描述": ["slow jog", "stretch after", "twenty minutes"],
            "影响": ["better focus", "healthier routine", "lighter mood"],
        },
        sample=(
            "I go to the park for light sports two or three times a week. "
            "I jog slowly for about twenty minutes and stretch before heading back to study. "
            "When exams get close I try not to skip it. "
            "My focus is better and my mood feels lighter."
        ),
        sampleZh=(
            "一周去公园做轻运动两三次。"
            "慢跑大概二十分钟，再拉伸就回宿舍学习。"
            "临考也会尽量不停。"
            "注意力更好，心情也轻快些。"
        ),
    )
    _p(
        "How have the parks in your city changed in recent years?",
        "nearby_park_walk",
        logic="对比类：先总说变好，再写步道座椅等新设施，对比以前简陋，个人感受。",
        kitHint="近年公园改造：步道、栏杆、晚上照明。",
        words={
            "正面回答": ["More user-friendly", "Cleaner paths", "Better lighting"],
            "选项1的特点与作用": ["new benches", "clearer signs", "safer night walks"],
            "选项2的特点与作用": ["older dusty corners", "fewer facilities before", "less organised"],
            "个人感受": ["proud of the area", "use parks more", "still not perfect"],
        },
        sample=(
            "I think parks in my city have become more user-friendly in recent years. "
            "Many now have new benches, clearer signs and better evening lighting, so evening walks feel safer. "
            "Before, some corners felt dusty and paths were uneven. "
            "I use parks more now, though a few old corners still need work."
        ),
        sampleZh=(
            "这几年我市的公园更人性化了。"
            "多了长椅、指示牌，晚上灯也更亮，傍晚散步更安全。"
            "以前有些角落尘土多，路也不太平。"
            "我现在更常去，不过少数老地方还得继续改。"
        ),
    )
    _p(
        "How have the parks in your city changed in recent years?",
        "yellow_bike_gift",
        logic="近年增加自行车道或共享停放区；对比以前只能步行；骑行爱好者感受。",
        kitHint="公园变化扣骑行友好，不跑题到地铁。",
        words={
            "正面回答": ["More bike-friendly", "Wider paths", "Clear cycling lines"],
            "选项1的特点与作用": ["marked bike lanes", "repair stands", "less conflict with walkers"],
            "选项2的特点与作用": ["narrow paths before", "walkers and cyclists mixed", "slower rides"],
            "个人感受": ["more enjoyable", "still watch speed", "welcome change"],
        },
        sample=(
            "Parks near me have got more bike-friendly, with clearer lines for cyclists and walkers. "
            "Some added small repair stands, so a flat tyre is less stressful on a weekend ride. "
            "In the past paths were narrow and everyone mixed together. "
            "Riding feels more enjoyable now, though I still watch my speed."
        ),
        sampleZh=(
            "附近公园对骑车更友好了，步行和骑行分区更清楚。"
            "有的还配了小修车架，周末轮胎没气也不慌。"
            "以前路窄，人车混一起。"
            "现在骑起来更舒服，我也会注意别太快。"
        ),
    )
    _p(
        "How have the parks in your city changed in recent years?",
        "light_sports_walk",
        logic="新增健身步道或塑胶跑道；对比以前泥地；爱运动的人感受。",
        kitHint="运动设施升级是公园变化主话题。",
        words={
            "正面回答": ["Better sports zones", "Rubber tracks", "More outdoor gyms"],
            "选项1的特点与作用": ["softer for knees", "rain drains faster", "free equipment"],
            "选项2的特点与作用": ["dusty dirt tracks", "wet muddy days", "fewer places to stretch"],
            "个人感受": ["motivated to move", "small city progress", "crowded at peak times"],
        },
        sample=(
            "Many parks now have rubber running tracks and simple outdoor gym bars. "
            "The surface is softer for knees and drains faster after rain, unlike old dusty dirt paths. "
            "Before, wet days turned the ground muddy and I skipped jogging. "
            "I feel more motivated to move, even if it gets crowded at peak times."
        ),
        sampleZh=(
            "很多公园铺了塑胶跑道和简易户外健身器材。"
            "对膝盖友好，雨后也比以前泥路干爽。"
            "过去一下雨场地烂泥，我就懒得跑。"
            "更愿意动了，只是高峰时段人会挤一点。"
        ),
    )