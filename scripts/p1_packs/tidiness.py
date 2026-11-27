# -*- coding: utf-8 -*-
"""Tidiness Freestyle packs."""


def register(_p):
    # --- Are you a tidy person? (shishi) ---
    _p(
        "Are you a tidy person?",
        "tidy_desk_habit",
        logic="先诚实回答是否整洁，再举书桌收纳例子，补学习前后频率与专注感受。",
        kitHint="书桌收纳是整洁题主素材：直接扣「你是不是整洁的人」。",
        words={
            "正面回答": ["Most of the time", "Yes, before studying", "I try to be"],
            "来源或举例": ["a tidy desk", "storage boxes", "put things away"],
            "频次": ["every evening before study", "weekend mornings"],
            "感受": ["practical", "less stressed", "helps me strive in study"],
        },
        sample=(
            "Most of the time, yes — especially about my desk. "
            "I use small storage boxes and put things away before I study. "
            "I do that every evening and sometimes on weekend mornings. "
            "A clear desk feels practical and less stressful."
        ),
        sampleZh=(
            "大部分时间算整齐，尤其书桌这边。"
            "用小收纳盒，学习前把东西收好。"
            "每天晚上都会，周末早上有时也会。"
            "桌面清爽实用，压力也小些。"
        ),
    )
    _p(
        "Are you a tidy person?",
        "parents_tidy_home",
        logic="先说自己现在算比较整齐，再讲童年受妈妈影响，补周末打扫频率与踏实感受。",
        kitHint="父母整理是第二套：从童年习惯说明你现在算不算整洁。",
        words={
            "正面回答": ["Fairly tidy", "Better than before", "Thanks to my parents"],
            "来源或举例": ["mum kept rooms neat", "weekend deep clean", "put toys away"],
            "频次": ["every weekend at home", "when I visit parents"],
            "感受": ["calmer", "organised", "used to order"],
        },
        sample=(
            "I'm fairly tidy now, though I wasn't perfect as a kid. "
            "My mum kept our rooms neat and we did a deeper clean every weekend. "
            "When I visit my parents I still tidy a bit out of habit. "
            "A clean room feels calmer and more organised."
        ),
        sampleZh=(
            "我现在算比较整齐，小时候倒没那么自觉。"
            "妈妈会把房间收拾整齐，周末还会大扫除。"
            "回家看父母时我也会顺手整理一下。"
            "干净房间让人心静，也更有条理。"
        ),
    )
    _p(
        "Are you a tidy person?",
        "dorm_apartment_life",
        logic="先说明宿舍算「够用整洁」、非洁癖，再举公共区域轮流值日，补平时与室友共处的实用感受。",
        kitHint="居所素材在整洁题：强调宿舍共用区与室友分工，仍是「你是否整洁」。",
        words={
            "正面回答": ["Reasonably tidy", "Not perfect", "I try in the dorm"],
            "来源或举例": ["shared kitchen shift", "sweep our floor", "roommate reminders"],
            "频次": ["most weeks", "before parents visit"],
            "感受": ["practical", "shows respect", "avoids arguments"],
        },
        sample=(
            "I'm reasonably tidy, not perfect. "
            "In the dorm we take turns with the shared kitchen and sweep our floor most weeks. "
            "My roommate sometimes reminds me before parents visit. "
            "It feels practical, shows respect and avoids small arguments."
        ),
        sampleZh=(
            "我算比较整齐，但不是吹毛求疵那种。"
            "宿舍里我们轮流收拾共用厨房，每周也会扫地。"
            "父母要来之前室友有时会提醒我。"
            "挺实用，也尊重别人，少拌嘴。"
        ),
    )

    # --- Who kept your room tidy when you were a child? (shishi) ---
    _p(
        "Who kept your room tidy when you were a child?",
        "parents_tidy_home",
        logic="直接点名主要是妈妈（或父母），再举收拾玩具/周末大扫除，补频率与温暖感受。",
        kitHint="父母整理是本题主素材；人物必须清楚。",
        words={
            "正面回答": ["My mum mostly", "My parents", "Mum with a bit from me"],
            "来源或举例": ["put toys away", "weekend deep clean", "asked me to help"],
            "频次": ["every weekend", "after school light tidying"],
            "感受": ["warm", "calmer home", "learnt small habits"],
        },
        sample=(
            "My mum mostly kept my room tidy when I was a child. "
            "She asked me to put toys away after school and did a deeper clean every weekend. "
            "That happened almost every week. "
            "It made our home calmer, and I learnt small habits from her."
        ),
        sampleZh=(
            "小时候主要是妈妈收拾我的房间。"
            "她会让我放学收拾玩具，周末再大扫除。"
            "差不多每周都这样。"
            "家里更安静，我也学到一点小习惯。"
        ),
    )
    _p(
        "Who kept your room tidy when you were a child?",
        "tidy_desk_habit",
        logic="先说妈妈为主，再提自己后来开始收书桌，补中学频率与现在仍保持的影响。",
        kitHint="第二套：从妈妈过渡到自己也收书桌，仍答「谁」为主。",
        words={
            "正面回答": ["My mum", "Later I joined in", "Parents first, me later"],
            "来源或举例": ["desk and textbooks", "before sleep", "middle school habit"],
            "频次": ["from about middle school", "every night then"],
            "感受": ["organised", "proud now", "still do it at dorm"],
        },
        sample=(
            "My mum kept things tidy when I was little, but from middle school I started clearing my desk before sleep. "
            "She still helped on weekends; I handled books and papers daily. "
            "I did that every night back then. "
            "I still keep the habit in my dorm now."
        ),
        sampleZh=(
            "小时候主要是妈妈，中学起我睡前会自己清书桌。"
            "周末还是她多收拾，平日我自管书本作业。"
            "那时几乎每晚都这样。"
            "现在住宿舍我仍然保持着。"
        ),
    )

    # --- Do you like to keep things tidy? (xihao) ---
    _p(
        "Do you like to keep things tidy?",
        "tidy_desk_habit",
        logic="先表明喜欢整洁，尤其书桌，再讲方便学习的原因，补每晚整理频率与减压感受。",
        kitHint="喜好+书桌收纳：喜欢整理是因为学习需要。",
        words={
            "正面回答": ["Yes, I do", "Especially my desk", "Definitely"],
            "原因或时间": ["clear mind for homework", "after a messy month we agreed", "before exams"],
            "频次": ["every evening", "extra on Sunday"],
            "感受": ["practical", "less anxious", "easier to start work"],
        },
        sample=(
            "Yes, I do, especially keeping my desk tidy. "
            "A clear surface makes homework easier, and my roommate and I agreed after one messy month. "
            "I tidy every evening, sometimes extra on Sunday. "
            "It feels practical, less anxious, and easier to start work."
        ),
        sampleZh=(
            "喜欢，尤其书桌要保持整齐。"
            "桌面清爽写作业顺手，有次乱成一团后我和室友就约好了。"
            "每晚都会收，周日有时多收拾一点。"
            "实用，也少焦虑，更好开工。"
        ),
    )
    _p(
        "Do you like to keep things tidy?",
        "parents_tidy_home",
        logic="先答喜欢，因童年家里干净让人舒服，再讲现在延续妈妈习惯，补回家与宿舍频率与温馨感受。",
        kitHint="父母家记忆解释「为何喜欢整洁」。",
        words={
            "正面回答": ["Yes", "I like a calm room", "It feels better"],
            "原因或时间": ["mum's cleaning routine", "childhood weekends", "quiet Sunday mornings"],
            "频次": ["when I visit home", "in the dorm most days"],
            "感受": ["warm", "relaxed", "respectful to others"],
        },
        sample=(
            "Yes, I like keeping things tidy — a calm room just feels better. "
            "My mum's weekend cleaning when I was small left quiet Sunday mornings in my mind. "
            "I still tidy when I visit home and most days in the dorm. "
            "It feels relaxed and respectful to my roommate too."
        ),
        sampleZh=(
            "喜欢，房间干净心里舒服些。"
            "小时候妈妈周末打扫，我对宁静的周日早上印象很深。"
            "回家时会收拾，宿舍也大多日子会整理。"
            "放松，也是对室友的尊重。"
        ),
    )
    _p(
        "Do you like to keep things tidy?",
        "dorm_apartment_life",
        logic="先答喜欢、尤其公共区域，再讲狭小宿舍乱糟糟会挡路的原因，补每周分工与相处感受。",
        kitHint="宿舍狭小空间解释为何「喜欢」整洁。",
        words={
            "正面回答": ["Yes, in a small dorm", "Especially shared areas", "Quite a lot"],
            "原因或时间": ["limited space", "roommate comfort", "parents might visit"],
            "频次": ["most weeks", "before holidays"],
            "感受": ["practical", "fair to roommate", "ready for guests"],
        },
        sample=(
            "Yes, especially in a small dorm where mess blocks the walkway. "
            "It's fair to my roommate, and I feel better before parents visit. "
            "We split chores most weeks and do a deeper tidy before holidays. "
            "It feels practical and keeps things fair."
        ),
        sampleZh=(
            "喜欢，宿舍小，乱起来连路都挡。"
            "对室友也公平，父母要来前我也更安心。"
            "多半每周分工，放假前会大扫除一次。"
            "很实用，也维持公平相处。"
        ),
    )

    # --- How often do you tidy your room? (xingwei) ---
    _p(
        "How often do you tidy your room?",
        "parents_tidy_home",
        logic="先说现在自己每周两三次，童年主要靠妈妈，按时间线描述收拾动作与影响。",
        kitHint="频率题：对比童年父母与现在自己动手。",
        words={
            "正面回答": ["Two or three times a week", "More before visitors", "Childhood: mum daily lightly"],
            "原因": ["small dorm", "mum's influence", "exam weeks need order"],
            "时间线+行为描述": ["weeknights clear desk", "Saturday sweep floor", "at home mum still helps sometimes"],
            "影响": ["calmer room", "less conflict", "exam focus better"],
        },
        sample=(
            "I tidy my dorm two or three times a week now. "
            "My mum used to handle most of it daily when I was small, so I picked up lighter habits later. "
            "On weeknights I clear the desk; on Saturday I sweep; at home she may still help a bit. "
            "The room stays calmer and I focus better in exam weeks."
        ),
        sampleZh=(
            "现在宿舍大概一周收拾两三次。"
            "小时候主要靠妈妈每天轻量打扫，我才慢慢学会。"
            "平日收书桌，周六扫地；回家她有时还会帮我一点。"
            "房间安静些，考试周也更好专心。"
        ),
    )
    _p(
        "How often do you tidy your room?",
        "tidy_desk_habit",
        logic="先说几乎每晚收书桌、周末稍大扫除，再讲怕分心原因，补行为细节与学习影响。",
        kitHint="书桌收纳主答频率：每晚为主。",
        words={
            "正面回答": ["Almost every evening", "A bit more on weekends", "Before big assignments"],
            "原因": ["clutter on shared desk", "roommate agreement", "find notes faster"],
            "时间线+行为描述": ["after dinner put books in boxes", "Sunday wipe the surface", "throw rubbish out"],
            "影响": ["start homework quicker", "fewer lost papers", "roommate happy"],
        },
        sample=(
            "I tidy almost every evening, and a bit more on weekends. "
            "Clutter on our shared desk slows me down, so we agreed to clear it after dinner. "
            "I put books in boxes, wipe the surface on Sunday and take rubbish out. "
            "I start homework quicker and lose fewer papers."
        ),
        sampleZh=(
            "几乎每晚都会整理，周末再多一点。"
            "共用书桌一乱我就慢，所以约好饭后收拾。"
            "书入盒，周日擦桌面，垃圾带出去。"
            "写作业更快，资料也不容易丢。"
        ),
    )
    _p(
        "How often do you tidy your room?",
        "dorm_apartment_life",
        logic="先答每周固定一次大扫除、平日小收拾，再讲宿舍值日原因，补行为与室友相处影响。",
        kitHint="宿舍公共与私人区轮流，回答「多久一次」。",
        words={
            "正面回答": ["Once a week deep clean", "Daily small pick-up", "When floor looks bad"],
            "原因": ["dorm rules", "shared kitchen smell", "roommate schedule"],
            "时间线+行为描述": ["Wednesday kitchen duty", "nightly clothes on rack", "Saturday vacuum corridor"],
            "影响": ["smell better", "less mould worry", "easier to invite friends"],
        },
        sample=(
            "We do a deeper tidy about once a week, plus small pick-ups daily. "
            "Dorm rules and a smelly kitchen push us to stay on schedule with my roommate. "
            "I'm on kitchen duty Wednesday, hang clothes nightly, and we vacuum on Saturday. "
            "The place smells better and friends feel welcome to visit."
        ),
        sampleZh=(
            "大概每周大扫除一次，平时小收拾每天都有。"
            "宿舍规定加上厨房味道，我和室友就按表来。"
            "周三我值日厨房，每晚挂衣服，周六吸走廊。"
            "住着没异味，也方便请同学来玩。"
        ),
    )

    # --- Do you think that it is necessary to be tidy? (guandian) ---
    _p(
        "Do you think that it is necessary to be tidy?",
        "tidy_desk_habit",
        logic="先表明认为有必要，再以书桌找资料为例，说明对学习的影响与感受。",
        kitHint="观点题用书桌例子论证「有必要」。",
        words={
            "正面回答": ["Yes, to a degree", "Quite necessary for students", "Not obsessive, but yes"],
            "举例或原因": ["find textbooks quickly", "shared dorm respect", "exam stress"],
            "作用或影响": ["saves time", "less arguing", "clearer thinking"],
            "感受": ["practical", "fair", "healthier mindset"],
        },
        sample=(
            "Yes, I think it's necessary to a degree — not obsessed, but useful. "
            "On a tidy desk I find textbooks quickly and think more clearly before exams. "
            "In a shared dorm it also saves time and cuts small arguments. "
            "Overall it feels practical and fair."
        ),
        sampleZh=(
            "我觉得有必要，但不用到强迫症那种程度。"
            "书桌整齐找书快，考前思路也更清楚。"
            "宿舍共用还省时间，也少拌嘴。"
            "总的来说实用也公平。"
        ),
    )
    _p(
        "Do you think that it is necessary to be tidy?",
        "parents_tidy_home",
        logic="先答有必要，举家里整洁减少争执为例，说明对孩子习惯的作用与温暖感受。",
        kitHint="父母家例子：整洁对家庭氛围的影响。",
        words={
            "正面回答": ["Yes", "Helps family life", "Children learn habits"],
            "举例或原因": ["mum's weekend clean", "less shouting about mess", "guests comfortable"],
            "作用或影响": ["calmer mood", "kids copy adults", "healthier home"],
            "感受": ["warm", "responsible", "worth the effort"],
        },
        sample=(
            "Yes, I think being tidy is necessary for a peaceful home. "
            "When Mum kept things in order on weekends, we argued less about lost things and guests felt comfortable. "
            "Kids copy that and grow more responsible. "
            "The effort feels warm and worth it."
        ),
        sampleZh=(
            "我认为整洁对家庭生活挺必要。"
            "妈妈周末把家收拾好，我们少为找东西吵架，来客也自在。"
            "孩子也会学着更有责任心。"
            "这份付出温馨，也值得。"
        ),
    )
    _p(
        "Do you think that it is necessary to be tidy?",
        "dorm_apartment_life",
        logic="先答在宿舍尤其必要，以卫生与室友关系为例，说明公共区域影响与实用感受。",
        kitHint="宿舍狭小共用，论证整洁必要性。",
        words={
            "正面回答": ["Especially in dorms", "Yes for shared spaces", "Basic level is enough"],
            "举例或原因": ["kitchen rubbish", "bathroom mould", "narrow walkway"],
            "作用或影响": ["fewer complaints", "healthier air", "longer friendly living"],
            "感受": ["respectful", "adult", "less awkward"],
        },
        sample=(
            "Yes, it is necessary to be tidy, especially in dorms where everyone shares tight space. "
            "Kitchen rubbish and a wet bathroom cause mould and complaints fast. "
            "Keeping things tidy keeps air healthier and friendships longer. "
            "It feels respectful and less awkward day to day."
        ),
        sampleZh=(
            "有必要保持整洁，尤其在大家挤在一起的宿舍。"
            "厨房垃圾、卫生间潮湿很快发霉也会被吐槽。"
            "收拾干净空气好，相处时间也更长。"
            "日常更尊重彼此，也没那么尴尬。"
        ),
    )

    # --- How have your tidying habits changed as you've got older? (duibi) ---
    _p(
        "How have your tidying habits changed as you've got older?",
        "tidy_desk_habit",
        logic="先总述从依赖妈妈到自己收书桌，再对比童年与大学两套习惯，补感受。",
        kitHint="成长对比：父母整理 → 自己书桌习惯。",
        words={
            "正面回答": ["Much more self-reliant", "From Mum to my desk", "Stricter with myself now"],
            "选项1的特点与作用": ["now: nightly desk routine", "roommate rules", "exam periods"],
            "选项2的特点与作用": ["childhood: mum did more", "I only put toys away", "weekends deep clean"],
            "个人感受": ["more responsible", "occasionally lazy", "proud when consistent"],
        },
        sample=(
            "They've changed a lot — I'm far more self-reliant now. "
            "As a kid Mum did most cleaning and I only put toys away before weekends. "
            "At university I tidy my desk nightly with my roommate, especially near exams. "
            "I feel more responsible, though occasionally lazy, and proud when I stay consistent."
        ),
        sampleZh=(
            "变化挺大，现在很多事靠自己了。"
            "小时候妈妈打扫为主，我只在周末前收玩具。"
            "上大学每晚和室友收书桌，考前更勤快。"
            "更有责任心，偶尔也会偷懒，坚持住时挺自豪。"
        ),
    )
    _p(
        "How have your tidying habits changed as you've got older?",
        "parents_tidy_home",
        logic="先答现在标准更高、仍会求助父母，再对比儿时完全靠妈妈与现在分担，补情感感受。",
        kitHint="第二套强调与父母的角色变化。",
        words={
            "正面回答": ["Higher standards now", "Still learn from Mum", "Less mess tolerated"],
            "选项1的特点与作用": ["today: split dorm chores", "before visitors", "budget storage"],
            "选项2的特点与作用": ["childhood: Mum's routine", "Dad fixed broken shelves", "family weekends"],
            "个人感受": ["grown up", "grateful", "sometimes miss help"],
        },
        sample=(
            "I've got stricter with myself as I've grown up. "
            "Today I split dorm chores and tidy before visitors; in childhood Mum's routine and Dad fixing shelves did most of it. "
            "I tolerate less mess now, though I still learn tips when I visit her. "
            "I feel grown up and grateful, and sometimes miss that easy help."
        ),
        sampleZh=(
            "年龄越大对自己要求越高。"
            "现在宿舍分工打扫、来客前收拾；小时候靠妈妈打扫、爸爸修架子。"
            "我更受不了乱，回家还是会向她学几招。"
            "觉得长大了也感恩，有时也会想念那份照顾。"
        ),
    )