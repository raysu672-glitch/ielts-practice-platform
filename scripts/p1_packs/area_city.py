# -*- coding: utf-8 -*-
"""The area / city you live in Freestyle packs."""


def register(_p):
    # ===== The area you live in =====

    # --- How long have you lived there? (shishi) ---
    _p(
        "How long have you lived there?",
        "dorm_apartment_life",
        logic="先答住了多久，再举搬进宿舍/租房时间与地点特征，补日常习惯与踏实感受。",
        kitHint="居所素材：从入学搬家说起，扣居住时长。",
        words={
            "正面回答": ["about two years", "since first year", "most of my degree"],
            "来源或举例": ["campus dorms then same block", "residential area", "with the same roommate"],
            "频次": ["full term time", "summers sometimes elsewhere"],
            "感受": ["used to it", "practical", "feels like my base"],
        },
        sample=(
            "About two years — since first year when I moved into campus dorms in this residential area. "
            "I kept the same block and roommate after that reshuffle. "
            "I'm there full term time, though some summers I stay elsewhere. "
            "I'm used to it and it feels like my practical base in the city."
        ),
        sampleZh=(
            "大概两年——大一下半年搬进这个居民区里的宿舍。"
            "换宿之后还是同一栋楼、同一个室友。"
            "学期多半都在，暑假有时不住这儿。"
            "习惯了，也觉得是城里实实在在的落脚点。"
        ),
    )
    _p(
        "How long have you lived there?",
        "subway_bus_commute",
        logic="先答时长，再以「因地铁搬来」说明选址，补每天通勤印证住得久。",
        kitHint="地铁素材：择居因通勤，时长与路线一致。",
        words={
            "正面回答": ["nearly two years", "since I picked this route", "most of university"],
            "来源或举例": ["10-minute walk to the subway", "Line 2 every morning", "bus backup in rain"],
            "频次": ["weekdays prove it", "rush hour regular"],
            "感受": ["convenient", "reliable", "worth the walk"],
        },
        sample=(
            "Nearly two years — since I chose this neighbourhood for the subway about ten minutes' walk away. "
            "I take Line 2 on weekday mornings and sometimes a bus in heavy rain. "
            "Rush-hour commuting most weekdays shows I've stayed put. "
            "It feels convenient, reliable and worth the short walk."
        ),
        sampleZh=(
            "快两年——我选这片就是因为走十分钟能到地铁。"
            "工作日早上坐2号线，大雨偶尔改公交。"
            "天天高峰期通勤，说明我一直住在这儿。"
            "方便、靠谱，多走几步也值。"
        ),
    )
    _p(
        "How long have you lived there?",
        "nearby_park_walk",
        logic="先答住了多久，再提到发现公园后决定留下，补傍晚散步习惯与舒缓感受。",
        kitHint="公园素材：因附近绿地择居，用散步频率佐证时长。",
        words={
            "正面回答": ["about two years", "since I found the park", "since second term"],
            "来源或举例": ["park 10 minutes away", "evening walk habit", "roommate joined later"],
            "频次": ["most fine evenings", "weekends too"],
            "感受": ["calmer", "lucky choice", "helps me reset"],
        },
        sample=(
            "About two years — I have lived in this area since early university. "
            "There is a park about ten minutes away, and I walk there most fine evenings with my roommate. "
            "That evening habit has stayed with me the whole time. "
            "The walks calm me, and the area still feels like home."
        ),
        sampleZh=(
            "大概两年——上大学起就住这片。"
            "步行大约十分钟有公园，晴天晚上常和室友去走走。"
            "这个傍晚习惯一直保持到现在。"
            "散步让人静下来，这片也仍像落脚的地方。"
        ),
    )

    # --- What facilities are there near where you live? (shishi) ---
    _p(
        "What facilities are there near where you live?",
        "nearby_park_walk",
        logic="先总述附近设施，公园作主设施，再补便利店/地铁等，补使用频率与便利感受。",
        kitHint="公园_walk主答：facilities 包含绿地与步道。",
        words={
            "正面回答": ["a park", "a convenience store", "a subway entrance"],
            "来源或举例": ["10-minute walk", "running track", "benches and trees"],
            "频次": ["evenings and weekends", "before exams for air"],
            "感受": ["really convenient", "healthy", "free relaxation"],
        },
        sample=(
            "There's a park about ten minutes' walk away, plus a convenience store and a subway entrance nearby. "
            "The park has a track, benches and plenty of trees. "
            "I use the park most evenings and weekends, especially before exams for fresh air. "
            "It's really convenient, healthy and free relaxation."
        ),
        sampleZh=(
            "步行十分钟有个公园，旁边还有便利店和地铁口。"
            "公园有跑道、长椅和不少树。"
            "多数晚上和周末会去，考前尤为常去透气。"
            "很方便，也健康，还不用花钱放松。"
        ),
    )
    _p(
        "What facilities are there near where you live?",
        "dorm_apartment_life",
        logic="先列举生活设施，宿舍/小区里食堂、洗衣、快递点等，补学生日常使用频率。",
        kitHint="居所：宿舍区配套是合法 facilities。",
        words={
            "正面回答": ["canteen", "laundry room", "parcel lockers"],
            "来源或举例": ["residential campus block", "small gym", "study room on floor two"],
            "频次": ["daily meals", "weekly laundry"],
            "感受": ["saves time", "student-friendly", "enough for daily life"],
        },
        sample=(
            "Near my dorm there's a canteen, laundry room, parcel lockers and even a small gym in the residential block. "
            "Floor two has a quiet study room classmates use. "
            "I eat there daily and do laundry weekly. "
            "It saves time and feels student-friendly for daily life."
        ),
        sampleZh=(
            "宿舍附近有食堂、洗衣房、快递柜，小区里还有小健身房。"
            "二楼有自习室，同学常去。"
            "我每天在食堂吃，一周洗一次衣服。"
            "省时间，对学生也挺够用。"
        ),
    )
    _p(
        "What facilities are there near where you live?",
        "subway_bus_commute",
        logic="先答交通设施为主，地铁站、公交站、共享单车，补通勤日使用频率与省时感受。",
        kitHint="通勤套：facilities=出行配套。",
        words={
            "正面回答": ["subway station", "bus stop", "shared bikes"],
            "来源或举例": ["Line 2 and Line 10 transfer", "rush-hour buses", "bike dock at the gate"],
            "频次": ["every weekday", "sometimes late library nights"],
            "感受": ["really convenient", "fast to campus", "reliable"],
        },
        sample=(
            "Near where I live, transport is the main facility — a subway station ten minutes away, a bus stop downstairs and shared bikes at the gate. "
            "Line 2 links to Line 10 for campus, and buses still run on late library nights. "
            "I use them every weekday. "
            "It's really convenient, fast to campus and reliable."
        ),
        sampleZh=(
            "我住的附近，主要设施是出行——走十分钟地铁，楼下公交站，门口还有共享单车。"
            "2号线换10号线去学校，泡图书馆晚了公交也还开。"
            "工作日天天用。"
            "很方便，去学校快，也相对靠谱。"
        ),
    )

    # --- What would you improve about your area if you could? (shishi) ---
    _p(
        "What would you improve about your area if you could?",
        "dorm_apartment_life",
        logic="先点最想改进处（如隔音/快递），再举具体例子，补学生受影响频率与烦恼感受。",
        kitHint="宿舍区痛点：噪音、空间、管理等。",
        words={
            "正面回答": ["sound insulation", "more quiet hours", "bigger study rooms"],
            "来源或举例": ["thin dorm walls", "late-night chatting", "queues at parcel lockers"],
            "频次": ["most exam weeks", "every evening"],
            "感受": ["distracting", "hopeful for change", "still manageable"],
        },
        sample=(
            "I'd improve sound insulation — dorm walls are thin and late-night chatting wakes people during exam weeks. "
            "I'd also add bigger study rooms because parcel locker queues crowd the corridor every evening. "
            "That bothers me most days in term time. "
            "It's distracting but still manageable if neighbours cooperate."
        ),
        sampleZh=(
            "我想改善隔音——宿舍墙薄，考试周夜里聊天会吵醒人。"
            "也想多几间大自习室，快递柜排队晚上常堵走廊。"
            "学期里几乎天天烦这事。"
            "分心但能忍，要是大家自觉些就好些。"
        ),
    )
    _p(
        "What would you improve about your area if you could?",
        "subway_bus_commute",
        logic="先说想缓解地铁高峰拥挤，再举排队与换乘例子，补工作日影响与期待感受。",
        kitHint="通勤套：改进=交通拥挤/班次。",
        words={
            "正面回答": ["less crowded rush hour", "more trains", "clearer signs at the exit"],
            "来源或举例": ["packed carriages", "long platform queue", "confusing transfer signs"],
            "频次": ["every weekday morning", "worse on rain days"],
            "感受": ["tired", "hope for upgrade", "still better than traffic jams"],
        },
        sample=(
            "I'd improve my area by easing rush-hour crowding on the subway — carriages are packed and platform queues are long every weekday morning. "
            "A few more trains and clearer exit signs would help, especially on rainy days. "
            "It makes me tired, but it's still better than road jams."
        ),
        sampleZh=(
            "我想改进住的片区，先缓解地铁早高峰拥挤——车厢挤、站台排长队，工作日早上天天如此。"
            "多几班车、出口指示牌更清楚就好了，下雨天尤其需要。"
            "挺累的，但总比路面堵车强。"
        ),
    )
    _p(
        "What would you improve about your area if you could?",
        "nearby_park_walk",
        logic="先说公园灯光/跑道维护，再举晚间散步例子，补使用频率与安全感受。",
        kitHint="公园套：改进绿地照明或设施。",
        words={
            "正面回答": ["brighter lights", "repair the running track", "more rubbish bins"],
            "来源或举例": ["dark corners after nine", "uneven track", "takeaway boxes left on benches"],
            "频次": ["most evening walks", "weekends busier"],
            "感受": ["a bit unsafe", "hope the council fixes it", "still love the park"],
        },
        sample=(
            "I'd improve the area by brightening lights in the park and repairing the running track — some nearby corners feel dark after nine and the surface is uneven. "
            "More bins would help too because takeaway boxes sit on benches on busy weekends. "
            "I notice this on most evening walks. "
            "It feels a bit unsafe, though I still love the park and hope the council fixes it soon."
        ),
        sampleZh=(
            "我想改进这片区：把公园灯弄亮一点，跑道也修好——附近有的角落九点后偏暗，跑道也不平。"
            "多想多设几个垃圾桶，周末外卖盒老堆在长椅上。"
            "多数傍晚散步都会注意到。"
            "有点不放心，但还是喜欢这公园，希望市政赶紧修。"
        ),
    )

    # --- What is the area where you live like? (xihao) ---
    _p(
        "What is the area where you live like?",
        "dorm_apartment_life",
        logic="先描绘片区气质（安静、学生多），再举例设施与人群，补居住频率与舒适感受。",
        kitHint="居所：居民区/宿舍区画像。",
        words={
            "正面回答": ["quiet and student-heavy", "residential", "safe at night"],
            "原因或时间": ["near campus", "families and renters mix", "guards at the gate"],
            "频次": ["every day coming back", "late nights still OK"],
            "感受": ["loose and comfortable", "familiar faces", "good for studying"],
        },
        sample=(
            "It's a quiet, student-heavy residential patch near campus — families and renters mix, with guards at the gate. "
            "Even late nights feel safe when I walk back from the library. "
            "I'm there every day and see familiar faces on the same paths. "
            "It feels loose, comfortable and good for studying."
        ),
        sampleZh=(
            "这片离学校近，安静，学生多，居民和租客都有，门口有保安。"
            "图书馆晚归也觉得安全。"
            "每天都在这儿，常在路上遇到熟人。"
            "松弛舒服，也挺适合学习。"
        ),
    )
    _p(
        "What is the area where you live like?",
        "subway_bus_commute",
        logic="先答区域气质偏便利、略吵，再举地铁商圈与通勤人流，补工作日体验与务实感受。",
        kitHint="通勤视角： bustling but convenient.",
        words={
            "正面回答": ["busy but convenient", "full of commuters", "shops near the station"],
            "原因或时间": ["subway hub", "morning rush", "late-night convenience stores open"],
            "频次": ["rush hour daily", "weekend calmer"],
            "感受": ["lively", "practical", "used to the noise"],
        },
        sample=(
            "It's busy but convenient — a commuter area with shops around the subway hub. "
            "Morning rush fills the street, though weekends are calmer and late-night stores stay open. "
            "I feel that rhythm every weekday. "
            "It's lively and practical; I've got used to the noise."
        ),
        sampleZh=(
            "热闹但方便——地铁商圈，上班上学的人流多。"
            "早高峰街面挤，周末安静些，夜里便利店也开着。"
            "工作日每天感受这个节奏。"
            "有烟火气也务实，噪音习惯了就好。"
        ),
    )
    _p(
        "What is the area where you live like?",
        "nearby_park_walk",
        logic="先答绿化好、生活节奏适中，再以公园为核心描述，补散步频率与舒缓感受。",
        kitHint="公园：片区=宜居+绿地。",
        words={
            "正面回答": ["green and relaxed", "not too central", "mix of old and new buildings"],
            "原因或时间": ["park as a lungs", "elders morning tai chi", "students evening walks"],
            "频次": ["most evenings", "weekend picnics sometimes"],
            "感受": ["pleasant", "breathable", "balanced pace"],
        },
        sample=(
            "The area where I live is green and relaxed, not right in the city centre — old and new buildings sit around a nearby park that works like lungs for the block. "
            "Elders do tai chi mornings; students walk evenings like me. "
            "I'm there most evenings and sometimes weekend picnics. "
            "The pace feels pleasant, breathable and balanced."
        ),
        sampleZh=(
            "我住的片区绿化好、节奏舒缓，不在最市中心——新老楼围着附近公园，像绿肺。"
            "早上老人太极，晚上学生散步，我也常去。"
            "多数傍晚都在，周末偶尔野餐。"
            "住着舒服，透气，节奏刚好。"
        ),
    )

    # --- What do you like most about your neighbourhood? (xihao) ---
    _p(
        "What do you like most about your neighbourhood?",
        "dorm_apartment_life",
        logic="先答最喜欢什么（邻里氛围/便利），再讲原因与日常接触，补频率与归属感感受。",
        kitHint="居所：最喜欢社区生活氛围。",
        words={
            "正面回答": ["friendly neighbours", "everything student needs", "feels safe"],
            "原因或时间": ["parcel help each other", "guards know students", "canteen downstairs"],
            "频次": ["daily small chats", "when parcels arrive"],
            "感受": ["supported", "not lonely", "like a small community"],
        },
        sample=(
            "I like the friendly neighbours most — people help each other with parcels and guards know us by face. "
            "With a canteen downstairs, everything a student needs is close. "
            "We exchange small chats daily, especially when parcels arrive. "
            "I feel supported, not lonely, like a small community."
        ),
        sampleZh=(
            "我最喜欢邻居和气——大家会互相帮拿快递，保安也认得我们。"
            "楼下食堂，学生要的都近。"
            "每天聊两句，快递多的时候尤其热络。"
            "有种被照顾、不孤单的小社区感。"
        ),
    )
    _p(
        "What do you like most about your neighbourhood?",
        "subway_bus_commute",
        logic="先答最喜欢出行方便，再举地铁与夜公交，补通勤日频率与省时感受。",
        kitHint="通勤：最喜欢 transport links.",
        words={
            "正面回答": ["transport links", "fast to campus", "options when it rains"],
            "原因或时间": ["avoid traffic jams", "read notes on the train", "bus if subway delays"],
            "频次": ["twice daily commutes", "late nights too"],
            "感受": ["really convenient", "saves energy", "reliable overall"],
        },
        sample=(
            "What I like most about my neighbourhood is the transport links — the subway gets me to campus fast and buses cover late nights. "
            "I avoid jams, read notes on the train and switch to buses if the subway delays. "
            "Twice-daily commutes prove how much I rely on it. "
            "It's really convenient, saves energy and feels reliable overall."
        ),
        sampleZh=(
            "我最喜欢这个社区的出行——地铁去学校快，夜里公交也补上。"
            "躲开堵车，车上还能看笔记，地铁延误就改公交。"
            "每天来回都靠它。"
            "很方便省力，整体也挺靠谱。"
        ),
    )
    _p(
        "What do you like most about your neighbourhood?",
        "nearby_park_walk",
        logic="先答最喜欢公园近，再讲散步解压原因，补傍晚频率与心情影响感受。",
        kitHint="公园：最喜欢 green escape.",
        words={
            "正面回答": ["the park nearby", "easy evening walks", "free stress relief"],
            "原因或时间": ["after study", "roommate company", "better than scrolling"],
            "频次": ["most evenings", "extra before exams"],
            "感受": ["calmer", "healthier", "lucky to have it"],
        },
        sample=(
            "I like the nearby park most — ten minutes away for easy evening walks after study. "
            "My roommate sometimes comes, and it's better than endless scrolling on my phone. "
            "I go most evenings, extra before exams. "
            "I feel calmer, a bit healthier and lucky to have it."
        ),
        sampleZh=(
            "最喜欢附近的公园——走十分钟，学完傍晚就能逛。"
            "室友有时一起，比一直刷手机强多了。"
            "多数晚上去，考前更勤。"
            "心里静下来，也健康一点，觉得挺幸运。"
        ),
    )

    # --- How has your area changed over the last few years? (duibi) ---
    _p(
        "How has your area changed over the last few years?",
        "dorm_apartment_life",
        logic="先总说变化，再对比旧宿舍区与现在楼宇/配套，补个人感受。",
        kitHint="居所：宿舍区翻新与配套升级。",
        words={
            "正面回答": ["quite a bit", "new blocks", "better canteen"],
            "选项1的特点与作用": ["today: renovated dorms", "parcel lockers", "brighter corridors"],
            "选项2的特点与作用": ["few years ago: older buildings", "smaller canteen", "only cash payments"],
            "个人感受": ["more comfortable", "slightly pricier", "worth the upgrade"],
        },
        sample=(
            "It has changed quite a bit. "
            "Today we have renovated dorms, parcel lockers and brighter corridors, while a few years ago buildings were older with a smaller canteen and cash only. "
            "Rent crept up slightly but daily life is more comfortable. "
            "I think the upgrade was worth it."
        ),
        sampleZh=(
            "这几年变化不小。"
            "现在有翻新宿舍、快递柜、走廊也更亮；几年前楼旧、食堂小，还只能现金。"
            "房租涨了一点，但日子舒服多了。"
            "我觉得这升级值。"
        ),
    )
    _p(
        "How has your area changed over the last few years?",
        "subway_bus_commute",
        logic="先答交通改善最大，再对比新旧地铁客流与线路，补通勤体验感受。",
        kitHint="通勤：地铁延伸/新线对比。",
        words={
            "正面回答": ["more subway lines", "bus routes added", "less walking in rain"],
            "选项1的特点与作用": ["now: new station exit", "more frequent trains", "phone ticket gates"],
            "选项2的特点与作用": ["before: one line only", "long bus detours", "paper tickets often"],
            "个人感受": ["faster commutes", "still crowded", "grateful for progress"],
        },
        sample=(
            "Transport changed the most. "
            "Now there's a new station exit, more frequent trains and phone ticket gates, whereas before we relied on one line, long bus detours and paper tickets. "
            "Commutes are faster though still crowded. "
            "I'm grateful for the progress."
        ),
        sampleZh=(
            "交通变化最大。"
            "如今有新出站口、班次更密、手机过闸；以前只靠一条线，公交得绕远，纸质票也常见。"
            "通勤快了些，但还是挤。"
            "有进步挺感恩的。"
        ),
    )
    _p(
        "How has your area changed over the last few years?",
        "nearby_park_walk",
        logic="先答公园翻新是主变化，再对比旧公园与现况，补散步体验感受。",
        kitHint="公园：绿地改造对比。",
        words={
            "正面回答": ["park renovated", "more paths", "sometimes too popular"],
            "选项1的特点与作用": ["today: new lights and track", "fitness corners", "weekend events"],
            "选项2的特点与作用": ["before: darker paths", "fewer benches", "quieter"],
            "个人感受": ["safer now", "a bit noisier", "still my favourite spot"],
        },
        sample=(
            "The park renovation stands out. "
            "Today there are new lights, a fixed track and fitness corners with weekend events, but before paths were darker with fewer benches and it was quieter. "
            "Evenings feel safer though a bit noisier. "
            "It's still my favourite spot in the neighbourhood."
        ),
        sampleZh=(
            "公园翻新最显眼。"
            "现在有新灯、修好跑道、健身器材，周末还有活动；以前路暗、椅子少，也更安静。"
            "晚上安全多了，但也吵一点。"
            "仍是我最喜欢的角落。"
        ),
    )

    # ===== The city you live in =====

    # --- Which city do you live in now? (shishi) ---
    _p(
        "Which city do you live in now?",
        "subway_bus_commute",
        logic="先直接报城市名与角色（上大学），再举地铁通勤细节，补居住时长与融入感受。",
        kitHint="城市+地铁通勤：主答城市名与生活，不跑题到广告。",
        words={
            "正面回答": ["a large eastern city", "where I study at university", "live here for my degree"],
            "来源或举例": ["Line 2 to campus", "rush-hour crowds", "mix of old lanes and new towers"],
            "频次": ["every weekday commute", "two years so far"],
            "感受": ["busy but exciting", "getting used to it", "convenient for students"],
        },
        sample=(
            "I live in a large eastern city where I study at university — I've been here about two years. "
            "I take Line 2 to campus most weekdays through rush-hour crowds, between old lanes and new towers. "
            "The commute is daily, so I know the city rhythm quickly. "
            "It's busy but exciting, convenient for students and I'm getting used to it."
        ),
        sampleZh=(
            "我现在住在一座华东大城市，在这里上大学，快两年了。"
            "工作日大多坐2号线去学校，穿过早高峰，老城巷弄和高楼混在一起。"
            "每天通勤，很快熟悉城市节奏。"
            "热闹也有意思，对学生方便，我也在慢慢适应。"
        ),
    )
    _p(
        "Which city do you live in now?",
        "dorm_apartment_life",
        logic="先报大学城/现居城市，再写宿舍生活与周边，补住了多久与适应感受。",
        kitHint="宿舍生活：城市身份=求学城市；不要扯广告屏。",
        words={
            "正面回答": ["a university city", "moved here for college", "not my hometown"],
            "来源或举例": ["campus dorms", "canteen downstairs", "quiet residential block"],
            "频次": ["full term time", "about two years so far"],
            "感受": ["busy but fine", "getting used to it", "practical for study"],
        },
        sample=(
            "I live in a university city now — I moved here for college, not from my hometown. "
            "I stay in campus dorms in a quiet residential block, with a canteen downstairs. "
            "I have been here about two years, full term time. "
            "It feels busy but practical for study, and I am getting used to it."
        ),
        sampleZh=(
            "我现在住在一座大学城，为念书搬来，不是家乡。"
            "住校内宿舍，一片比较安静的居民区，楼下有食堂。"
            "大概两年了，学期里基本都在。"
            "忙但方便学习，也在慢慢适应。"
        ),
    )

    # --- What is the best way to get around your city? (shishi) ---
    _p(
        "What is the best way to get around your city?",
        "subway_bus_commute",
        logic="先明确地铁（+公交补充）最佳，再举线路与换乘例子，补使用频率与省时感受。",
        kitHint="get-around 题优先地铁公交套装，正面答交通方式。",
        words={
            "正面回答": ["the subway", "metro plus bus", "avoid peak driving"],
            "来源或举例": ["Line 2 and 10", "bus when it rains", "shared bikes last mile"],
            "频次": ["every weekday", "weekends for downtown"],
            "感受": ["really convenient", "cheap for students", "predictable time"],
        },
        sample=(
            "The subway is the best way, with buses and shared bikes for the last mile. "
            "I use Line 2 and 10 on weekdays and grab a bus in heavy rain. "
            "That's my routine every day to campus and downtown on weekends. "
            "It's really convenient, cheap for students and gives predictable travel time."
        ),
        sampleZh=(
            "地铁最好，公交和共享单车补最后一程。"
            "平日用2号线和10号线，大雨改公交。"
            "每天去学校，周末进城也这样。"
            "很方便，学生便宜，时间也好估。"
        ),
    )
    _p(
        "What is the best way to get around your city?",
        "nearby_park_walk",
        logic="先答短途走路/骑共享，长途仍靠地铁；举例公园周边，频次与感受。",
        kitHint="第二套：短距离步行+地铁组合，不讲广告。",
        words={
            "正面回答": ["Walk for short trips", "Subway for longer ones", "Mix both"],
            "来源或举例": ["park and shops nearby", "Line 2 for downtown", "shared bikes sometimes"],
            "频次": ["walk most evenings", "subway every school day"],
            "感受": ["cheap", "healthy enough", "saves waiting in traffic"],
        },
        sample=(
            "For short trips I walk, and for longer ones I take the subway. "
            "The park and small shops near my dorm are close enough on foot, and Line 2 takes me downtown. "
            "I walk most evenings and ride the subway every school day. "
            "It is cheap, a bit healthier, and I avoid sitting in traffic."
        ),
        sampleZh=(
            "短途我走路，远一点就坐地铁。"
            "宿舍附近公园和小店步行就到，进城坐2号线。"
            "多数晚上走路，上学日每天地铁。"
            "省钱，也活动一下，还能避开堵车。"
        ),
    )

    # --- Where would you take a friend who was visiting your city? (shishi) ---
    _p(
        "Where would you take a friend who was visiting your city?",
        "subway_bus_commute",
        logic="先点目的地（老城/江景/校园），再说地铁怎么去，补一日游安排与好客感受。",
        kitHint="带朋友游城：地铁串联景点。",
        words={
            "正面回答": ["old town by the river", "the university area", "a night market"],
            "来源或举例": ["subway then walk", "bus along the river", "cheap local snacks"],
            "频次": ["one-day trip", "evening for lights"],
            "感受": ["show city culture", "fun", "easy to plan"],
        },
        sample=(
            "I'd take them to the old town by the river — subway, a short walk and snacks at a night market. "
            "We could show campus in the afternoon and see lights in the evening. "
            "It's a simple one-day loop I could repeat with any visitor. "
            "It shows city culture, feels fun and is easy to plan on public transport."
        ),
        sampleZh=(
            "我会带去江边老城——地铁加走一段，夜市吃点小吃。"
            "下午可逛学校片区，晚上看灯光。"
            "一日游就能走完，每个朋友来都能照用。"
            "有城市味道，也好玩，公交好安排。"
        ),
    )
    _p(
        "Where would you take a friend who was visiting your city?",
        "nearby_park_walk",
        logic="先推荐公园与江边步道，再说轻松好逛，补一天安排与好客感受。",
        kitHint="带朋友：公园绿地与步道，不扯广告。",
        words={
            "正面回答": ["a riverside park", "tree-lined paths", "benches by the water"],
            "来源或举例": ["ten-minute walk from subway", "evening lights", "cheap snacks nearby"],
            "频次": ["a half-day walk", "sunset if we can"],
            "感受": ["relaxed", "easy to chat", "proud to show"],
        },
        sample=(
            "I would take them to a riverside park with tree-lined paths. "
            "It is about ten minutes from the subway, and there are cheap snacks nearby. "
            "We could walk for half a day and stay for sunset if the weather is good. "
            "It is relaxed and easy to chat, and I would feel proud to show it."
        ),
        sampleZh=(
            "我会带他们去江边公园，沿树荫步道走走。"
            "地铁出来大概十分钟，附近也有便宜小吃。"
            "半日够逛，天气好还能看日落。"
            "轻松好聊天，我也挺愿意当向导。"
        ),
    )

    # --- What do you like most about living in this city? (xihao) ---
    _p(
        "What do you like most about living in this city?",
        "subway_bus_commute",
        logic="先答最喜欢出行/机会，再讲地铁串联实习与校园，补平日频率与开放感受。",
        kitHint="城市喜好：地铁带来的便利与机会。",
        words={
            "正面回答": ["mobility", "internship options", "never stuck in one corner"],
            "原因或时间": ["fast subway", "weekend downtown", "library till late then bus home"],
            "频次": ["daily commutes", "explore each month"],
            "感受": ["free", "really convenient", "good for students"],
        },
        sample=(
            "I like the transport most — the subway lets me get to campus, internships and downtown easily. "
            "I take it every weekday, and sometimes I visit a new place at weekends. "
            "After the library I can still catch a late bus home. "
            "That freedom feels really convenient for students."
        ),
        sampleZh=(
            "我最喜欢这座城市的交通——地铁去学校、实习、进城都方便。"
            "工作日天天坐，周末有时去新地方。"
            "图书馆晚了还能坐公交回家。"
            "这种自由对学生特别方便。"
        ),
    )
    _p(
        "What do you like most about living in this city?",
        "nearby_park_walk",
        logic="先答最喜欢有公园透气，再讲忙完可散步，频次与放松感受。",
        kitHint="城市喜好第二套：绿地缓冲学习压力。",
        words={
            "正面回答": ["green parks", "easy evening walks", "fresh air after study"],
            "原因或时间": ["close to dorm", "free and quiet", "better than scrolling"],
            "频次": ["most fine evenings", "longer at weekends"],
            "感受": ["calmer", "lucky", "less stressed"],
        },
        sample=(
            "I like the green parks most — easy evening walks after study. "
            "They are close to my dorm, free and quieter than malls. "
            "I go on most fine evenings, and longer at weekends. "
            "I feel calmer and less stressed living in a city with that space."
        ),
        sampleZh=(
            "我最喜欢城里的公园——学完能傍晚走走。"
            "离宿舍近，免费，也比商场安静。"
            "晴天晚上多半去，周末会多逛一会儿。"
            "有这种空间，我觉得更平静、压力也小些。"
        ),
    )

    # --- What's the weather like where you live? (xihao) ---
    _p(
        "What's the weather like where you live?",
        "subway_bus_commute",
        logic="先描述四季/雨热特点，再讲对地铁出行影响，补不同季节频率与适应感受。",
        kitHint="天气+地铁：雨夏挤地铁、冬天室内站。",
        words={
            "正面回答": ["humid summers", "mild winters", "rainy season in June"],
            "原因或时间": ["AC in stations", "umbrella rush", "dry cold wind"],
            "频次": ["check apps each morning", "bus detours in storms"],
            "感受": ["manageable", "plan around rain", "subway helps in heat"],
        },
        sample=(
            "Humid summers, mild winters and a rainy June — that's typical here. "
            "I check weather apps each morning because storms push me from bikes to the subway or buses. "
            "Station air-conditioning helps in heat; dry cold wind hits above ground in winter. "
            "It's manageable if I plan around rain, and the subway helps in summer."
        ),
        sampleZh=(
            "夏天潮、冬天温和，六月梅雨是常态。"
            "早上看天气软件，暴雨就让我改地铁公交，不骑车。"
            "夏天站里有空调；冬天地上干冷风一吹很明显。"
            "安排好雨天就还撑得住，酷暑地铁帮大忙。"
        ),
    )
    _p(
        "What's the weather like where you live?",
        "weather_search_tools",
        logic="先答本地气候，再讲常查手机天气再出门，频次与适应感受。",
        kitHint="天气题第二套：查天气工具支撑「怎么应对」，主答仍是气候本身。",
        words={
            "正面回答": ["four seasons", "hot sticky August", "rainy weeks in spring"],
            "原因或时间": ["check the weather app", "carry an umbrella", "avoid sudden storms"],
            "频次": ["almost every morning", "before I leave the dorm"],
            "感受": ["used to it", "app helps a lot", "like clear autumn best"],
        },
        sample=(
            "We have four seasons here — sticky August, rainy spring weeks, and a clear autumn I like best. "
            "I check the weather app almost every morning before I leave the dorm. "
            "That helps me carry an umbrella and avoid sudden storms. "
            "I am used to it, and the app makes planning much easier."
        ),
        sampleZh=(
            "这里四季分明——八月闷热，春天多雨，我最爱晴朗秋天。"
            "几乎每天早上出门前都会看天气软件。"
            "好带伞，也能避开突然的暴雨。"
            "已经习惯了，软件让安排轻松很多。"
        ),
    )

    # --- How has your city changed over the past ten years? (duibi) ---
    _p(
        "How has your city changed over the past ten years?",
        "subway_bus_commute",
        logic="先总说交通变化最大，再对比新旧地铁网，补个人出行感受。",
        kitHint="十年变化：地铁线网扩张对比。",
        words={
            "正面回答": ["huge transport upgrades", "more lines", "smarter tickets"],
            "选项1的特点与作用": ["today: five lines crossing", "phone pay", "less bus-only trips"],
            "选项2的特点与作用": ["ten years ago: two lines", "paper tickets", "longer bus rides"],
            "个人感受": ["proud", "still crowded", "life easier"],
        },
        sample=(
            "Transport upgraded the most over ten years. "
            "Today five subway lines cross the city with phone payment, whereas a decade ago we had two lines, paper tickets and longer bus rides. "
            "Mornings are still crowded, but daily life is easier. "
            "I'm proud of the progress even if rush hour hasn't vanished."
        ),
        sampleZh=(
            "十年里交通升级最大。"
            "如今五条地铁交汇、手机支付；十年前只有两条线、纸质票，公交绕更远。"
            "早高峰还是挤，但日子好过了。"
            "为有进步自豪，虽然高峰期仍在。"
        ),
    )
    _p(
        "How has your city changed over the past ten years?",
        "nearby_park_walk",
        logic="先总说公园与公共空间变化，再对比过去，补个人散步感受。",
        kitHint="城市十年变化第二套：绿地/步道升级，不讲广告。",
        words={
            "正面回答": ["more parks", "better night lighting", "cleaner paths"],
            "选项1的特点与作用": ["now: new tracks and benches", "evening walks feel safer"],
            "选项2的特点与作用": ["before: darker corners", "fewer places to sit"],
            "个人感受": ["happier to walk", "still busy city", "nice upgrade"],
        },
        sample=(
            "Parks and public paths have changed a lot over ten years. "
            "Today there are new tracks, better night lights and more benches, while older parks felt darker with fewer places to sit. "
            "Evening walks feel safer now. "
            "I am happier to walk after study, even though the city is still busy."
        ),
        sampleZh=(
            "十年里公园和公共步道变化很大。"
            "现在有新跑道、更好的夜灯和更多长椅；以前角落更暗，也少地方坐。"
            "傍晚散步更安心。"
            "学完更愿意出去走，尽管城市依然很忙。"
        ),
    )