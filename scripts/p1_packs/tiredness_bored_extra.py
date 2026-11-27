# -*- coding: utf-8 -*-
"""Tiredness Freestyle packs (distinct from Feeling bored)."""


def register(_p):
    _p(
        "How does tiredness affect your work or studies?",
        "study_library_classes",
        logic="先答疲倦如何拖累课堂与图书馆学习，再举例错题与犯困，频次与挫败感。",
        kitHint="影响学习题：用上课/图书馆场景扣题，不要改成骑车或公园故事。",
        words={
            "正面回答": ["Hurts my focus", "Slower reading", "More small mistakes"],
            "来源或举例": ["library revision", "evening classes", "notes with typos"],
            "频次": ["on busy weeks", "before big deadlines"],
            "感受": ["need real rest", "quality drops", "frustrating"],
        },
        sample=(
            "Tiredness hurts my focus when I study in the library or finish assignments. "
            "I read more slowly and make more small mistakes in my notes. "
            "That shows up on busy weeks before deadlines. "
            "I find it frustrating, and I need proper rest instead of pushing for hours."
        ),
        sampleZh=(
            "在图书馆学习或赶作业时，疲倦会拉低专注。"
            "看书变慢，笔记里也更多小错。"
            "任务多的那几周尤其明显。"
            "挺烦的，硬撑不如好好休息。"
        ),
    )
    _p(
        "How does tiredness affect your work or studies?",
        "nearby_park_walk",
        logic="疲倦让效率下降，再写傍晚散步如何帮恢复一点清醒，频次感受。",
        kitHint="公园散步是恢复手段的侧面提及，答题轴仍是疲倦对学习的影响。",
        words={
            "正面回答": ["Harder to concentrate", "Yawn in class", "Forget details"],
            "来源或举例": ["back-to-back lectures", "evening revision", "short park walks help a bit"],
            "频次": ["most busy terms", "after poor sleep"],
            "感受": ["dragging", "need breaks", "walks help slightly"],
        },
        sample=(
            "When I am tired, it is harder to concentrate and I sometimes yawn in class. "
            "I forget small details when I review at night after poor sleep. "
            "That happens most terms when lectures stack up. "
            "A short park walk after study helps a little, but sleep still matters most."
        ),
        sampleZh=(
            "累的时候很难集中注意力，上课也会打哈欠。"
            "睡得差时晚上复习容易忘细节。"
            "课排得满的学期常有这种情况。"
            "学后去公园走走略好一点，但睡眠还是最关键。"
        ),
    )
    _p(
        "How does tiredness affect your work or studies?",
        "light_sports_walk",
        logic="疲倦降效率；轻度慢跑能改善精力但太累就不能练，频率感受平衡。",
        kitHint="运动恢复：谈影响为主，运动是边界例子。",
        words={
            "正面回答": ["Harder to focus", "Skip gym when exhausted", "Heavy eyes"],
            "来源或举例": ["long lab reports", "jog only when energy OK", "stretch instead"],
            "频次": ["every exam season", "after all-nighters"],
            "感受": ["unbalanced", "need sleep first", "light sport later"],
        },
        sample=(
            "Tiredness makes it hard for me to focus, especially in exam weeks with long reports. "
            "If I am really tired I skip jogging and only stretch a little. "
            "That happens after I sleep late. "
            "I feel off balance, so sleep comes first and light sport comes later."
        ),
        sampleZh=(
            "疲倦会让我很难专心，考季写长报告时尤其明显。"
            "实在太累就不跑，只做一点拉伸。"
            "睡得晚之后常这样。"
            "会觉得不舒服，先睡够再谈轻运动。"
        ),
    )
    _p(
        "What used to make you tired when you were a child?",
        "yellow_bike_gift",
        logic="童年累因：长课、早起骑车上学；频次；当时感受。",
        kitHint="累因可含骑车上学，但答点仍是「什么让你累」。",
        words={
            "正面回答": ["Early mornings", "Long school days", "Cycling in rain"],
            "来源或举例": ["ride to school", "PE classes", "homework at night"],
            "频次": ["weekdays often", "winter more"],
            "感受": ["sleepy in class", "still worth it", "normal kid tiredness"],
        },
        sample=(
            "As a child long school days and early mornings made me tired. "
            "Riding my yellow bike to school in cold rain also wore me out before class even started. "
            "That was common on weekdays, especially in winter. "
            "I felt sleepy in lessons, but it was normal kid tiredness."
        ),
        sampleZh=(
            "小时候课业长、起床早让我很困。"
            "冬天雨天骑车上学，还没上课就累了。"
            "工作日常见，冬天更多。"
            "上课想睡，但也是正常的孩童疲劳。"
        ),
    )
    _p(
        "What used to make you tired when you were a child?",
        "nearby_park_walk",
        logic="童年累因：疯玩后仍要写作业、走很远回家，频次感受。",
        kitHint="公园疯跑玩累≠公园题跑偏，这里是童年为何疲倦。",
        words={
            "正面回答": ["Playing too long", "Walking home late", "Summer heat"],
            "来源或举例": ["ran in the park", "evening homework", "missed nap time"],
            "频次": ["many summer afternoons", "before exams in primary school"],
            "感受": ["happy but exhausted", "fell asleep early", "worth the fun"],
        },
        sample=(
            "Playing in the park too long on hot summer afternoons used to make me tired. "
            "I still had homework after I walked home, so I rarely napped. "
            "That happened many times before primary-school exams. "
            "I was happy but exhausted and fell asleep early, which felt worth the fun."
        ),
        sampleZh=(
            "夏天午后在公园玩太久会特别累。"
            "走回家还得写作业，基本不午睡。"
            "小学考前那段日子经常如此。"
            "又开心又困，早早睡着也觉得值。"
        ),
    )
    _p(
        "What used to make you tired when you were a child?",
        "light_sports_walk",
        logic="童年运动量大、体育课后腿酸仍是疲倦原因，频次感受。",
        kitHint="体育课、社团练跑导致累，合理扣题。",
        words={
            "正面回答": ["PE classes", "Sports-day practice", "Running drills"],
            "来源或举例": ["park track laps", "coach shouting", "heavy schoolbag after"],
            "频次": ["twice a week at school", "more before competitions"],
            "感受": ["sore legs", "proud anyway", "slept deeply"],
        },
        sample=(
            "PE classes and sports-day practice in the park often made me tired as a child. "
            "Coach made us run laps until my legs felt sore, and I still carried a heavy bag home. "
            "We trained about twice a week, more before competitions. "
            "I was exhausted but proud, and I usually slept deeply."
        ),
        sampleZh=(
            "体育课和运动会集训常常把我练累。"
            "教练让我们在公园跑道跑到腿酸，回家还得背沉书包。"
            "一周大概两次，比赛前更密集。"
            "虽然很累但也有成就感，晚上睡得特别香。"
        ),
    )
    _p(
        "Do you often get tired?",
        "yellow_bike_gift",
        logic="先答是否常累，举熬夜学习例，周末骑车帮恢复，频次感受。",
        kitHint="常累+恢复：骑车是疲劳后活动，不是替代答「累不累」。",
        words={
            "正面回答": ["Quite often", "Especially in term time", "Yes, with late study"],
            "来源或举例": ["assignments", "weekend bike ride helps", "screens at night"],
            "频次": ["most weekdays", "recover at weekends"],
            "感受": ["manageable", "need balance", "riding refreshes me"],
        },
        sample=(
            "Yes, I get tired quite often during term time with late study and phone screens. "
            "A slow bike ride at the weekend in the park helps me recover a bit. "
            "Weekdays feel heavy most weeks, weekends lighter after I ride. "
            "It is manageable if I keep that balance."
        ),
        sampleZh=(
            "会，学期里熬夜学习和看手机常常让我累。"
            "周末在公园慢慢骑一圈能缓一点。"
            "工作日多数周挺沉，骑完周末会好些。"
            "只要保持这种平衡还算撑得住。"
        ),
    )
    _p(
        "Do you often get tired?",
        "nearby_park_walk",
        logic="是否常累+久坐学习原因+傍晚散步稍解乏，频次感受。",
        kitHint="散步是轻恢复举例，主题仍是疲倦频率。",
        words={
            "正面回答": ["Fairly often", "Not always", "Depends on sleep"],
            "来源或举例": ["desk study", "short evening walks", "poor sleep nights"],
            "频次": ["several nights a week", "walk when I can"],
            "感受": ["drained sometimes", "walks take the edge off", "need earlier bedtime"],
        },
        sample=(
            "Fairly often, especially when I sit at a desk all day for study. "
            "Poor sleep nights make it worse, though a short evening park walk takes the edge off. "
            "That happens several nights a week in busy terms. "
            "I still feel drained sometimes and know I need an earlier bedtime."
        ),
        sampleZh=(
            "还挺常，尤其一整天坐着学习的时候。"
            "睡得差就更明显，傍晚公园走走能缓一缓。"
            "忙的学期一周有好几个晚上会这样。"
            "有时仍觉得透支，也知道该早点睡。"
        ),
    )
    _p(
        "Do you often get tired?",
        "light_sports_walk",
        logic="常累因缺少运动或运动过度；慢跑调节；频次感受。",
        kitHint="疲倦与运动量的关系，仍答「是否常累」。",
        words={
            "正面回答": ["Sometimes yes", "When I skip exercise", "Also after hard runs"],
            "来源或举例": ["no jog for days", "leg soreness", "catch up on sleep"],
            "频次": ["off weeks vs on weeks", "exam stress weeks"],
            "感受": ["sluggish", "jog helps routine", "listen to my body"],
        },
        sample=(
            "Sometimes yes — I feel sluggish when I skip light exercise for several days. "
            "I also feel tired the day after a hard jog if I do not sleep well. "
            "Exam stress weeks make both patterns more common. "
            "A regular slow run helps my routine, but I try to listen to my body."
        ),
        sampleZh=(
            "有时会——好几天不运动会觉得发沉。"
            "有意思的是，跑猛了再加上没睡好，第二天也会累。"
            "考试压力大的几周两种情况的更多。"
            "保持慢跑习惯有帮助，但也要听身体信号。"
        ),
    )
    _p(
        "When do you usually feel tired?",
        "nearby_park_walk",
        logic="行为习惯：点出通常何时累，原因，行为（散步前夜作息），影响。",
        kitHint="晚上学习后、周日晚间等时间点。",
        words={
            "正面回答": ["Late evenings", "After long classes", "Sunday nights"],
            "原因": ["screen time", "unfinished tasks", "mental load"],
            "时间线+行为描述": ["library till nine", "walk before bed", "skip the walk if raining"],
            "影响": ["sleep later", "calmer if I walk", "worse if I scroll"],
        },
        sample=(
            "I usually feel tired late in the evening after long classes and library study till about nine. "
            "If I keep scrolling in bed, the tired feeling turns into a heavy head. "
            "On dry nights I walk in the park first, which calms me down. "
            "Without that walk I sleep later and feel worse next morning."
        ),
        sampleZh=(
            "通常在傍晚上完课、图书馆学到九点左右会累得明显。"
            "要是躺床还刷手机，那种累会变成脑袋沉沉的。"
            "天气好我会先去公园走走平复一下。"
            "不散步就更晚睡，第二天早上更难受。"
        ),
    )
    _p(
        "When do you usually feel tired?",
        "yellow_bike_gift",
        logic="何时累：周五下午或连课后；骑车放松是疲倦后的行为，影响睡眠。",
        kitHint="时间点+骑车恢复疲劳的行为习惯。",
        words={
            "正面回答": ["Friday afternoons", "After back-to-back classes", "Before weekend"],
            "原因": ["week stress piles up", "little break", "commute by bike still"],
            "时间线+行为描述": ["ride slowly to park", "no racing", "shower and sleep early"],
            "影响": ["week ends lighter", "avoid overtraining", "sleep improves"],
        },
        sample=(
            "I usually feel most tired on Friday afternoons after back-to-back classes all week. "
            "I still commute by bike, but I ride slowly to the park without racing anyone. "
            "Then I shower and try to sleep earlier on Friday night. "
            "My weekend starts lighter and my sleep improves."
        ),
        sampleZh=(
            "一般周五下午最累，一整周连堂课堆在一起。"
            "仍骑车通勤，但去公园时慢骑，不比速度。"
            "回家洗澡，周五尽量早睡。"
            "周末起步轻松些，睡眠也会好一点。"
        ),
    )
    _p(
        "When do you usually feel tired?",
        "light_sports_walk",
        logic="何时累：午后久坐后；慢跑太晚反而兴奋，调整时间，影响。",
        kitHint="午后低能量点+运动时间选择。",
        words={
            "正面回答": ["After lunch slump", "Mid-afternoon", "Post-online class blocks"],
            "原因": ["blood sugar dip", "sitting still", "air-con rooms"],
            "时间线+行为描述": ["stand and stretch", "jog only before six", "water break"],
            "影响": ["alert again", "bad sleep if too late", "plan matters"],
        },
        sample=(
            "I often feel tired in the mid-afternoon after lunch and long online class blocks. "
            "Sitting in air-conditioned rooms makes the slump worse. "
            "I stand, stretch, or jog before six pm, not later, so I do not get too wired at night. "
            "Planning the time helps me feel alert again without ruining sleep."
        ),
        sampleZh=(
            "午后吃完午饭、连着上网课后常会困。"
            "空调房里久坐会让低谷更明显。"
            "我会站起来拉伸，或在六点前慢跑，太晚怕晚上兴奋睡不着。"
            "掐好时间能提神，又不打乱作息。"
        ),
    )
    _p(
        "What do you usually do when you feel tired?",
        "nearby_park_walk",
        logic="疲倦时步行休息是主行为；原因不想继续硬学；时间线；影响清醒。",
        kitHint="累→公园散步，核心恢复动作。",
        words={
            "正面回答": ["Take a walk", "Leave the desk", "Fresh air first"],
            "原因": ["brain fog", "eyes hurt from screens", "short break works"],
            "时间线+行为描述": ["ten-minute loop", "no music sometimes", "back to work"],
            "影响": ["clearer head", "less cranky", "finish faster after"],
        },
        sample=(
            "When I feel tired I usually leave my desk and walk in the nearby park for about ten minutes. "
            "Fresh air beats scrolling when my eyes hurt from screens. "
            "I come back without music sometimes and restart the task. "
            "My head feels clearer and I finish faster with less crankiness."
        ),
        sampleZh=(
            "累了我就离开书桌，去附近公园走十分钟左右。"
            "眼睛看屏幕发涩时，透气比刷手机管用。"
            "有时不听歌，回来接着做任务。"
            "脑子清楚些，脾气也好点，效率反而上来。"
        ),
    )
    _p(
        "What do you usually do when you feel tired?",
        "yellow_bike_gift",
        logic="累时慢骑车放松；原因而动非竞技；时间线；体力精神恢复。",
        kitHint="疲倦恢复=慢骑，不是上学冲速度。",
        words={
            "正面回答": ["Slow cycling", "Easy park loop", "No hard hills"],
            "原因": ["sitting too long", "need movement", "stress release"],
            "时间线+行为描述": ["weekend afternoon", "thirty to forty minutes", "drink water after"],
            "影响": ["looser shoulders", "sleepier in a good way", "ready for Monday"],
        },
        sample=(
            "When I feel tired I often take my yellow bike for a slow loop in the park on weekend afternoons. "
            "I avoid hard hills and treat it as movement, not a race. "
            "Thirty or forty minutes is enough before I drink water and shower. "
            "My shoulders feel looser and I get pleasantly sleepy, ready for Monday."
        ),
        sampleZh=(
            "累了的话周末下午常骑小黄车在公园慢慢转一圈。"
            "不爬陡坡，只当活动筋骨，不比速度。"
            "三四十分钟就好，然后喝水洗澡。"
            "肩膀松了，也会困得舒服，周一好接着学。"
        ),
    )
    _p(
        "What do you usually do when you feel tired?",
        "light_sports_walk",
        logic="累时慢跑或拉伸；原因促循环；时间线；影响精力。",
        kitHint="疲倦恢复=轻运动，答「做什么」。",
        words={
            "正面回答": ["Light jog", "Stretch", "Stop if dizzy"],
            "原因": ["stiff body", "need energy", "better than coffee"],
            "时间线+行为描述": ["warm up walk", "fifteen-minute jog", "cool down stretch"],
            "影响": ["more awake", "avoid injury", "steady habit"],
        },
        sample=(
            "When I feel tired I do a light jog or stretch if I am not dizzy. "
            "A stiff body after sitting makes the tired feeling worse. "
            "I warm up with a walk, jog about fifteen minutes, then cool down. "
            "I feel more awake than from another coffee, and I avoid pushing too hard."
        ),
        sampleZh=(
            "累了如果不头晕，我会慢跑或拉伸。"
            "坐久了身体僵，会更像累垮。"
            "先走几分钟热身，慢跑一刻钟左右，再放松拉伸。"
            "比再来一杯咖啡精神些，也不会练过头。"
        ),
    )
    _p(
        "Why do you think so many people feel tired these days?",
        "nearby_park_walk",
        logic="观点：先答原因屏幕久坐睡得晚，再作用影响，感受担忧。",
        kitHint="社会性疲倦原因，顺带说户外少。",
        words={
            "正面回答": ["Screens and poor sleep", "Sedentary life", "Stress culture"],
            "举例或原因": ["phones in bed", "long commutes", "skip outdoor walks"],
            "作用或影响": ["chronic low energy", "mood issues", "health risk"],
            "感受": ["worried", "need better habits", "parks help if used"],
        },
        sample=(
            "I think many people feel tired because of screens, late nights and sitting too long for study or work. "
            "They use phones in bed and skip simple outdoor walks. "
            "Over time they feel low on energy and their mood gets worse. "
            "I hope more people use parks and sleep earlier."
        ),
        sampleZh=(
            "我觉得很多人累，是因为刷屏、熬夜加上久坐学习或工作。"
            "躺床还玩手机，连散个步都省了。"
            "时间长了会没劲，情绪也容易变差。"
            "希望大家多用公园、早点睡。"
        ),
    )
    _p(
        "Why do you think so many people feel tired these days?",
        "douyin_scroll_habit",
        logic="观点：先答晚刷短视频导致睡眠差，再说白天犯困影响，最后谈习惯该改。",
        kitHint="社会疲倦原因：短视频/熬夜刷屏；不要改成骑车故事。",
        words={
            "正面回答": ["Late-night phones", "Short videos in bed", "Less sleep"],
            "举例或原因": ["scroll before sleep", "one more video", "wake up heavy"],
            "作用或影响": ["yawn in class", "slow study", "mood drops"],
            "感受": ["common now", "hard to stop", "earlier sleep would help"],
        },
        sample=(
            "I think many people feel tired because they stay on phones late and watch short videos in bed. "
            "They tell themselves one more video, then sleep less and wake up heavy. "
            "That makes class and study slower the next day. "
            "It is common now, and earlier sleep would help more than coffee."
        ),
        sampleZh=(
            "我觉得很多人累，是因为夜里还刷手机、躺着看短视频。"
            "总想再看一条，睡得少，早上昏沉。"
            "第二天上课学习都会变慢。"
            "现在很常见，早睡比多喝咖啡更管用。"
        ),
    )
    _p(
        "Why do you think so many people feel tired these days?",
        "light_sports_walk",
        logic="观点：健身焦虑却又不练；规律轻跑反而少；社会比较累人；感受。",
        kitHint="运动文化与疲倦的社会原因。",
        words={
            "正面回答": ["Gym pressure but no habit", "Irregular sleep", "Social comparison online"],
            "举例或原因": ["all-or-nothing workouts", "compare lives on apps", "skip breakfast"],
            "作用或影响": ["burnout feeling", "weaker immunity vibe", "hard to focus"],
            "感受": ["sympathetic", "gentle sport better", "balance needed"],
        },
        sample=(
            "I think people feel tired because they sit too much and sleep at irregular times. "
            "They skip simple walks or light jogs, then feel heavy by mid-week. "
            "That makes it harder to focus at school or work. "
            "Small daily movement and better sleep would help more than big gym plans."
        ),
        sampleZh=(
            "我觉得大家累，是因为坐太久、睡眠也不规律。"
            "连简单散步或慢跑都省了，一周过半就发沉。"
            "上课或工作更难集中。"
            "每天一点点活动和睡好，比冲健身房计划更管用。"
        ),
    )