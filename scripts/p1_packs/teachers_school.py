# -*- coding: utf-8 -*-
"""Teachers and Secondary school Freestyle packs."""


def register(_p):
  # --- Teachers ---
    _p(
        "What makes someone a good teacher?",
        "patient_teacher_help",
        logic="先点耐心与讲清楚，再举课后答疑例子，说常见场景与感激感受。",
        kitHint="耐心老师：好老师=讲解+鼓励，library 料勿硬套。",
        words={
            "正面回答": ["Patience", "Clear explanations", "Encouragement"],
            "来源或举例": ["after-class help", "step by step", "no rushing"],
            "频次": ["often before exams", "when topics were hard"],
            "感受": ["less stressed", "motivated", "respected"],
        },
        sample=(
            "I think patience and clear explanations make a good teacher. "
            "In secondary school one teacher stayed after class to explain ideas step by step without rushing us. "
            "That happened often before exams when topics were hard. "
            "I felt less stressed and more motivated — I really respected that teacher."
        ),
        sampleZh=(
            "我觉得耐心和讲清楚是好老师的关键。"
            "中学有一位老师课后留下来，一步一步讲，不催我们。"
            "难题多、考前尤其常见。"
            "压力小了很多，也更有动力——我很敬重那位老师。"
        ),
    )
    _p(
        "What makes someone a good teacher?",
        "study_library_classes",
        logic="先答会引导自学与用好图书馆的老师好，再举借书、翻实体书例子，说频率与成长感受。",
        kitHint="图书馆料=好老师鼓励阅读习惯，扣老师品质非只讲自己学习。",
        words={
            "正面回答": ["Guides self-study", "Pushes good habits", "Uses real books"],
            "来源或举例": ["library tasks", "flip through books", "after-class reading lists"],
            "频次": ["weekly reading", "before essays"],
            "感受": ["more independent", "deeper thinking", "grateful"],
        },
        sample=(
            "A good teacher also guides students to study by themselves and use the library well. "
            "One lecturer gave us short reading lists and told us to flip through real books, not only slides. "
            "We did that weekly before essays. "
            "It made me more independent and I am grateful for that habit."
        ),
        sampleZh=(
            "好老师还会引导自学、用好图书馆。"
            "有一位老师开短书单，让我们翻实体书，不全靠幻灯片。"
            "写论文前每周都会这样安排。"
            "我更独立了，也很感激这习惯。"
        ),
    )
    _p(
        "Have you ever wanted to be a teacher?",
        "patient_teacher_help",
        logic="先如实答短暂想过/没坚定想过，再连受到耐心老师影响的例子，说当年情境与感受。",
        kitHint="耐心榜样：是否想过当老师=被好老师触动，非图书馆主线。",
        words={
            "正面回答": ["Briefly", "Not seriously", "Maybe when I was younger"],
            "来源或举例": ["helpful teacher", "explaining to classmates", "after-school tutoring"],
            "频次": ["once in junior high", "a short phase"],
            "感受": ["admiring", "realised it is hard work", "chose another path"],
        },
        sample=(
            "Briefly, when I was younger — not seriously long term. "
            "A patient teacher who helped after class made me think teaching could be meaningful. "
            "I even tried explaining homework to classmates for a short phase in junior high. "
            "I admired the job, but I soon realised how tiring it is and chose another path."
        ),
        sampleZh=(
            "小时候短暂想过——不是长期的坚定计划。"
            "一位课后耐心讲解的老师让我觉得教书很有意义。"
            "初中有一阵子我还给同学讲过作业。"
            "我很钦佩这职业，但很快发现很累，就走了别的路。"
        ),
    )
    _p(
        "Have you ever wanted to be a teacher?",
        "study_library_classes",
        logic="先答没特别想当，但欣赏会带学生去图书馆的老师，再举例，说频率与尊重感受。",
        kitHint="图书馆视角：不想当老师但佩服引路型老师。",
        words={
            "正面回答": ["Not really", "Respect them", "Prefer studying"],
            "来源或举例": ["library sessions", "research skills", "quiet study corners"],
            "频次": ["a few times a term", "for big projects"],
            "感受": ["good example", "still a student myself", "thankful"],
        },
        sample=(
            "Not really — I prefer being a student myself. "
            "Still, I respect teachers who lead library sessions and show us how to find sources. "
            "That happened a few times a term for big projects. "
            "They were good examples for me, and I am thankful, but I never wanted the job full time."
        ),
        sampleZh=(
            "没有特别想——我更喜欢自己当学生。"
            "但我佩服会带大家去图书馆、教查资料的老师。"
            "大作业前一学期会碰到几次。"
            "他们是榜样，我也很感激，可从没想过全职当老师。"
        ),
    )
    _p(
        "What kind of teacher do you learn best from?",
        "patient_teacher_help",
        logic="先答从耐心、愿意复述的老师学得最好，再举课堂例子，说频率与轻松感受。",
        kitHint="学习偏好=耐心讲解型老师。",
        words={
            "正面回答": ["Patient", "Repeats calmly", "Checks understanding"],
            "来源或举例": ["simple examples", "extra minutes after class", "encouraging tone"],
            "频次": ["throughout secondary school", "especially maths"],
            "感受": ["less afraid to ask", "catch up faster", "confident"],
        },
        sample=(
            "I learn best from patient teachers who repeat ideas calmly and check if we understand. "
            "My maths teacher used simple examples and waited extra minutes after class for questions. "
            "That style ran through secondary school, especially in maths. "
            "I was less afraid to ask and caught up faster — I felt more confident."
        ),
        sampleZh=(
            "我从耐心、愿意平静重复并确认听懂的老师那里学得最好。"
            "数学老师爱用简单例子，课后还多留几分钟答疑。"
            "中学阶段一直如此，数学课尤甚。"
            "敢问问题了，跟上也快——更有信心。"
        ),
    )
    _p(
        "What kind of teacher do you learn best from?",
        "study_library_classes",
        logic="先答喜欢会布置深度阅读、带队进图书馆的老师，再举例，说频率与钻研感受。",
        kitHint="学习偏好=引导查阅、自学型老师。",
        words={
            "正面回答": ["Guides research", "Library trips", "Clear reading tasks"],
            "来源或举例": ["flip books", "note-taking tips", "essay feedback"],
            "频次": ["each major essay", "before presentations"],
            "感受": ["think deeper", "skills last longer", "enjoy class more"],
        },
        sample=(
            "I learn best from teachers who guide research and actually take us to the library. "
            "They show how to flip through books, take notes, and turn reading into essay feedback. "
            "I met that style before each major essay and presentation. "
            "I think deeper and the skills last longer — I enjoy those classes more."
        ),
        sampleZh=(
            "我最适应会带查资料、真把我们带进图书馆的老师。"
            "他们教怎么翻书、做笔记，把阅读变成作文反馈。"
            "大论文、展示前常常会这样。"
            "想得深，技能也更持久——我更喜欢这类课。"
        ),
    )
    _p(
        "Who was your favourite teacher when you were at school?",
        "patient_teacher_help",
        logic="先点名喜欢的耐心老师，再说明科目与课后帮助，说相处频率与感激感受。",
        kitHint="最喜欢的老师=耐心品质主线。",
        words={
            "正面回答": ["My maths teacher", "Very patient", "Always fair"],
            "原因或时间": ["stayed after class", "simple explanations", "secondary school"],
            "频次": ["a few times a week", "near exams"],
            "感受": ["trusted her", "grades improved", "still remember"],
        },
        sample=(
            "My favourite was a very patient maths teacher in secondary school. "
            "She stayed after class with simple explanations, and she was always fair when we made mistakes. "
            "I saw her extra help a few times a week near exams. "
            "I trusted her, my grades improved, and I still remember her tone."
        ),
        sampleZh=(
            "我最喜欢的是中学一位很有耐心的数学老师。"
            "她课后留下来用简单方式讲，我们犯错她也公平对待。"
            "考前一周能见她几次额外辅导。"
            "我信她，成绩也上去了，还记得她说话的样子。"
        ),
    )
    _p(
        "Who was your favourite teacher when you were at school?",
        "study_library_classes",
        logic="先答最喜欢会带大家去图书馆的语文老师/通识老师，再举阅读任务，说频率与启发感受。",
        kitHint="最喜欢=引阅读习惯的老师，library 料作老师品质。",
        words={
            "正面回答": ["Chinese teacher", "Loved reading", "Library lover"],
            "原因或时间": ["reading lists", "quiet library hour", "wrote comments on essays"],
            "频次": ["every two weeks", "through junior high"],
            "感受": ["like reading more", "felt cared for", "warm memory"],
        },
        sample=(
            "My favourite teacher was a Chinese teacher who loved reading and took us to the library. "
            "She gave short reading lists and wrote careful comments on our essays. "
            "We had a quiet library hour every two weeks through junior high. "
            "She helped me like reading more, and I felt cared for."
        ),
        sampleZh=(
            "我最喜欢的是一位爱阅读的语文老师，常带我们进图书馆。"
            "她开短书单，作文评语写得很细。"
            "初中每两周会有一节安静阅读时间。"
            "让我更爱看书，也觉得被关心。"
        ),
    )
    _p(
        "In what way has your favourite teacher helped you?",
        "patient_teacher_help",
        logic="先答帮我在难题前保持耐心与信心，再举课后辅导例子，说持续影响。",
        kitHint="老师帮助=耐心辅导带来的信心。",
        words={
            "正面回答": ["Built confidence", "Taught patience", "Explained again"],
            "原因或时间": ["before exams", "when I fell behind", "secondary school"],
            "频次": ["weekly help", "whole semester"],
            "感受": ["less scared of maths", "study habits improved", "grateful"],
        },
        sample=(
            "My favourite teacher helped me stay patient and confident when topics were hard. "
            "Before exams, when I fell behind, she explained things again until I nodded. "
            "That support lasted a whole semester, almost weekly. "
            "I became less scared of maths and my study habits improved — I am still grateful."
        ),
        sampleZh=(
            "最喜欢的老师帮我在难题前保持耐心和信心。"
            "考前掉队时，她会一遍遍讲到点头为止。"
            "差不多一个学期，每周都有这种支持。"
            "我不那么怕数学了，学习习惯也好起来——一直很感激。"
        ),
    )
    _p(
        "In what way has your favourite teacher helped you?",
        "study_library_classes",
        logic="先答教我自学查资料与做笔记，再举图书馆任务，说对大学学习的持续影响。",
        kitHint="老师帮助=阅读习惯与方法，非主课内容复述。",
        words={
            "正面回答": ["Research skills", "Note-taking", "Independent reading"],
            "原因或时间": ["library tasks", "essay season", "after class tips"],
            "频次": ["each term", "before big assignments"],
            "感受": ["ready for university", "less reliant on slides", "thankful"],
        },
        sample=(
            "She helped me learn to find sources and take useful notes on my own. "
            "Library tasks before big assignments forced me to flip through real books, not only copy slides. "
            "That happened each term in essay season. "
            "I felt more ready for university and less reliant on PowerPoints — still thankful."
        ),
        sampleZh=(
            "她教会我自己找资料、做有用的笔记。"
            "大作业前的图书馆任务逼着我翻实体书，不能只会抄幻灯片。"
            "每个学期写论文季都会这样。"
            "感觉更适应大学学习，不那么依赖 PPT——还是很感谢她。"
        ),
    )
    _p(
        "How has the way teachers teach changed since you were a child?",
        "patient_teacher_help",
        logic="先答现在更注重互动与个别关注，再对比小时候照本宣科，说个人感受。",
        kitHint="教学法对比：过去 lecturing vs 现在耐心互动。",
        words={
            "正面回答": ["More interaction", "Less one-way lecture", "Slower pace for weak students"],
            "选项1的特点与作用": ["today: quizzes in class", "small groups", "after-class chat"],
            "选项2的特点与作用": ["childhood: chalk and listen", "fewer questions", "bigger classes"],
            "个人感受": ["less boring", "still uneven", "better for me"],
        },
        sample=(
            "Teaching feels more interactive now — teachers slow down for weak students and chat after class. "
            "Today we get in-class quizzes and small groups, not only chalk and listen. "
            "When I was a child lessons were more one-way and fewer students dared to ask. "
            "Classes are less boring for me now, though quality is still uneven."
        ),
        sampleZh=(
            "现在上课互动更多——老师会放慢照顾落后的同学，课后也聊。"
            "有课堂小测、小组，不全是对着黑板听。"
            "小时候更像单向讲授，敢提问的人少。"
            "我觉得没那么枯燥了，不过好坏老师差距还是有。"
        ),
    )
    _p(
        "How has the way teachers teach changed since you were a child?",
        "study_library_classes",
        logic="先答如今线上线下资料更多，但仍要进馆阅读；再对比童年只有纸质，说个人感受。",
        kitHint="对比：现在数字资源 vs 以前实体书，老师角色变引路人。",
        words={
            "正面回答": ["More online", "Still need libraries", "Guides instead of only talking"],
            "选项1的特点与作用": ["now: slides, videos, apps", "homework on phones"],
            "选项2的特点与作用": ["childhood: textbooks only", "copy from blackboard"],
            "个人感受": ["handy but easy to get distracted", "like teachers who still use books"],
        },
        sample=(
            "Teachers use more slides and videos now, but good ones still ask us to read real books. "
            "We often get homework on apps, while when I was a child we mostly used textbooks and copied from the board. "
            "Teachers guide us more and talk less for a whole lesson. "
            "It is handy, but easy to get distracted — I still like teachers who take us to the library."
        ),
        sampleZh=(
            "老师现在更多用幻灯片和视频，好的仍会让我们读实体书。"
            "作业常在手机应用里交，小时候多半翻教材、抄板书。"
            "老师更多是引导，而不是整节课一直讲。"
            "方便，但也容易分心——我还是喜欢会带我们去图书馆的老师。"
        ),
    )

  # --- Secondary school ---
    _p(
        "Do you still keep in touch with your classmates from secondary school?",
        "school_choir_songs",
        logic="先答还联系几位合唱过的同学，再举节日群聊/聚会例子，说频率与怀念感受。",
        kitHint="合唱班同学：保持联系=音乐课圈子。",
        words={
            "正面回答": ["A few close ones", "WeChat group", "Not everyone"],
            "来源或举例": ["choir classmates", "festival songs", "graduation photos"],
            "频次": ["a few times a year", "long holidays"],
            "感受": ["warm", "busy now", "good memories"],
        },
        sample=(
            "I still keep in touch with a few classmates from our school choir. "
            "We have a small WeChat group and sometimes meet for milk tea during long holidays. "
            "That is only a few times a year — campus life is busy now. "
            "It feels warm and brings back good memories of those festival songs."
        ),
        sampleZh=(
            "还和几位合唱团同学有联系。"
            "有个小微信群，长假有时约奶茶。"
            "一年就几次——现在校园生活忙。"
            "挺温暖，也想起当年排节日歌的日子。"
        ),
    )
    _p(
        "Do you still keep in touch with your classmates from secondary school?",
        "school_science_lab",
        logic="先答和做实验的同桌仍偶尔联系，再举讨论升学例子，说频率与友谊感受。",
        kitHint="科学课同桌：联系=实验课小伙伴。",
        words={
            "正面回答": ["Yes, my lab partner", "Sometimes online", "Not a big group"],
            "来源或举例": ["science projects", "exam revision", "university choices"],
            "频次": ["every few months", "around New Year"],
            "感受": ["supportive", "different cities", "still close"],
        },
        sample=(
            "Yes — mainly my science lab partner from secondary school. "
            "We still message about university choices and laugh about old experiments that almost failed. "
            "We chat every few months, often around New Year. "
            "We live in different cities now, but it still feels close and supportive."
        ),
        sampleZh=(
            "有——主要是中学科学实验的搭档。"
            "还会聊升学选择，也会笑差点搞砸的旧实验。"
            "几个月聊一次，过年前后常联系。"
            "现在在异地，但还是很亲近、互相打气。"
        ),
    )
    _p(
        "Do you still keep in touch with your classmates from secondary school?",
        "yellow_bike_gift",
        logic="先答会和一起骑车上学的几位同学偶尔联系，再举群发骑行照片例子，说频率与亲近感。",
        kitHint="黄自行车：联系=骑车通勤小圈子。",
        words={
            "正面回答": ["A small circle", "Still say hi", "Mainly online"],
            "来源或举例": ["rode yellow bike together", "rainy days stories", "class group chat"],
            "频次": ["a few messages a month", "summer holidays"],
            "感受": ["friendly", "busy schedules", "shared jokes"],
        },
        sample=(
            "I keep in touch with a small circle who used to ride to school with me on my yellow bike. "
            "We drop memes in the class group chat and compare busy schedules in summer. "
            "Maybe a few messages a month — not daily. "
            "It stays friendly with shared jokes about rainy rides."
        ),
        sampleZh=(
            "还和几个当年一起骑车上学的小伙伴有联系。"
            "在班级群里发梗图，暑假会比谁更忙。"
            "一个月几条消息，不是天天聊。"
            "挺友好，也还会提起雨天骑车那些事。"
        ),
    )
    _p(
        "Is there anything you miss about your secondary school?",
        "school_choir_songs",
        logic="先答想念合唱排练和齐唱氛围，再举具体场景，说怀念频率与心情。",
        kitHint="校园合唱：想念=课后排练齐心感。",
        words={
            "正面回答": ["Choir practice", "Simple songs", "Team feeling"],
            "来源或举例": ["music room", "festival performance", "classmates singing"],
            "频次": ["every week back then", "before Spring Festival"],
            "感受": ["nostalgic", "less pressure", "happy noise"],
        },
        sample=(
            "I miss choir practice and the happy noise when classmates sang together. "
            "We rehearsed simple songs every week in the music room before festivals. "
            "That rhythm is gone at university where everyone is busier. "
            "I feel nostalgic — those afternoons had less pressure."
        ),
        sampleZh=(
            "想念合唱排练和大家一齐唱的声音。"
            "音乐节目前每周在音乐教室练简单的歌。"
            "大学各忙各的，那种节奏没了。"
            "挺怀旧——那时下午没那么大压力。"
        ),
    )
    _p(
        "Is there anything you miss about your secondary school?",
        "school_science_lab",
        logic="先答想念亲手做实验的兴奋，再举有趣失败例子，说对现在学习的对比感受。",
        kitHint="科学实验：想念=动手的课堂乐趣。",
        words={
            "正面回答": ["Hands-on labs", "Curious class", "Fun failures"],
            "来源或举例": ["biology class", "colour changes", "group reports"],
            "频次": ["monthly labs", "exam terms"],
            "感受": ["more alive than slides", "simpler life", "still smile"],
        },
        sample=(
            "I miss the excitement of hands-on science labs — colour changes and messy notes felt more alive than slides. "
            "Our group reports sometimes failed in funny ways, but we laughed and fixed them. "
            "We had labs about monthly, heavier near exams. "
            "Life felt simpler then, and I still smile when I remember."
        ),
        sampleZh=(
            "想念亲手做实验的兴奋——颜色变化、乱七八糟的笔记比幻灯片生动。"
            "小组报告有时搞笑地失败，但我们笑着改。"
            "大概每月一次实验，考前更密。"
            "那时生活简单些，想起来还会笑。"
        ),
    )
    _p(
        "Is there anything you miss about your secondary school?",
        "yellow_bike_gift",
        logic="先答想念骑车上学的自由，再举黄自行车与校门口例子，说天气细节与感受。",
        kitHint="黄自行车：想念=骑车通勤的自由感。",
        words={
            "正面回答": ["Cycling freedom", "Short commute", "Fresh air"],
            "来源或举例": ["yellow bike", "school gate", "avoid traffic"],
            "频次": ["almost daily", "even light rain"],
            "感受": ["independent", "convenient", "miss that routine"],
        },
        sample=(
            "I miss the freedom of cycling to school on my small yellow bike. "
            "The ride to the gate was short, with fresh air and no rush-hour bus squeeze. "
            "I did it almost daily, even in light rain some days. "
            "It felt independent and convenient — I miss that routine now."
        ),
        sampleZh=(
            "想念骑黄色小自行车上学的自由。"
            "到校门路程短，有风、不用挤公交。"
            "差不多每天，小雨天有时也骑。"
            "觉得独立又方便——现在挺想念这节奏。"
        ),
    )
    _p(
        "What was your secondary school like?",
        "school_choir_songs",
        logic="先总体描述普通市立中学，再突出音乐课与合唱活跃，说整体氛围感受。",
        kitHint="学校画像=有合唱氛围的中学。",
        words={
            "正面回答": ["Medium-sized", "Friendly", "Active music classes"],
            "原因或时间": ["children's songs", "year shows", "normal timetable"],
            "频次": ["music once a week", "choir after lunch sometimes"],
            "感受": ["lively", "not fancy", "warm classmates"],
        },
        sample=(
            "It was a medium-sized local school — not fancy, but friendly. "
            "Music class was lively; we learned children's songs and sometimes practised after lunch for shows. "
            "We had music once a week with a normal heavy timetable besides. "
            "Classmates were warm, and the place felt lively rather than stressful."
        ),
        sampleZh=(
            "一所普通规模的市立中学——不豪华，但挺友好。"
            "音乐课很活跃，学儿歌，有时午休后排节目。"
            "每周一堂音乐课，其他课表照常很满。"
            "同学热情，整体气氛活泼，不算压抑。"
        ),
    )
    _p(
        "What was your secondary school like?",
        "school_science_lab",
        logic="先描述重视理科实验的学校，再举实验室与竞赛例子，说氛围感受。",
        kitHint="学校画像=实验条件不错的中学。",
        words={
            "正面回答": ["Science-focused", "Decent labs", "Hard-working"],
            "原因或时间": ["biology experiments", "science weeks", "exam pressure"],
            "频次": ["labs monthly", "science club Fridays"],
            "感受": ["busy", "curious crowd", "competitive but fair"],
        },
        sample=(
            "My secondary school was hard-working with decent science labs. "
            "We did biology experiments monthly and had science weeks with posters in the corridor. "
            "A small science club met on Fridays when exams allowed. "
            "It was busy and a bit competitive, but teachers were fair and students were curious."
        ),
        sampleZh=(
            "我的中学挺用功，实验条件也还可以。"
            "每月有生物实验，科学周走廊贴海报。"
            "不忙考试时有小科学社周五活动。"
            "节奏紧、有点竞争，但老师公平，同学也好奇心强。"
        ),
    )
    _p(
        "What was your secondary school like?",
        "yellow_bike_gift",
        logic="先答校门近、骑车同学多的学校，再写停车区与早晨场景，说整体感受。",
        kitHint="学校画像=骑车上学常见的校园氛围。",
        words={
            "正面回答": ["Near a main road", "Lots of cyclists", "Open gate mornings"],
            "原因或时间": ["bike racks full", "yellow bikes common", "short distance"],
            "频次": ["every morning rush", "after-school rides"],
            "感受": ["energetic", "convenient area", "less sleepy"],
        },
        sample=(
            "It sat near a main road, and lots of students cycled in every morning — bike racks were often full. "
            "The open gate at rush hour felt energetic, with yellow bikes lined up like mine. "
            "Distances were short, so riding was normal after school too. "
            "The area was convenient and mornings felt less sleepy than on a long bus ride."
        ),
        sampleZh=(
            "学校在主干道旁，早上很多人骑车来，车棚常满。"
            "高峰时校门敞开很热闹，一排排小黄车，我的也在里面。"
            "路不远，放学骑车也普遍。"
            "交通方便，早上比坐长途公交精神。"
        ),
    )
    _p(
        "What was your favourite subject at secondary school?",
        "school_choir_songs",
        logic="先答最喜欢音乐课，再说明合唱快乐与不费心的原因，说上课频率与感受。",
        kitHint="最喜欢科目=音乐/合唱，扣 secondary school Q。",
        words={
            "正面回答": ["Music", "Choir time", "Easy to enjoy"],
            "原因或时间": ["sing with friends", "festival shows", "less exam fear"],
            "频次": ["weekly lessons", "extra practice before shows"],
            "感受": ["relaxed", "confident on stage", "happy"],
        },
        sample=(
            "Music was my favourite — singing with friends felt relaxed compared with heavy exam subjects. "
            "We prepared simple choir songs for festivals, which gave me confidence on stage. "
            "Lessons were weekly, with extra practice before shows. "
            "I felt happy there, not afraid of tests."
        ),
        sampleZh=(
            "最喜欢音乐——和朋友唱歌比应试课轻松。"
            "为节日排合唱，上台也有信心。"
            "每周一堂，演出前加练。"
            "在那里很开心，不怕测验。"
        ),
    )
    _p(
        "What was your favourite subject at secondary school?",
        "school_science_lab",
        logic="先答最喜欢科学/生物，再举实验例子说明兴趣来源，说频率与好奇感受。",
        kitHint="最喜欢科目=科学实验兴趣。",
        words={
            "正面回答": ["Biology", "Science", "Hands-on class"],
            "原因或时间": ["colour experiments", "see results fast", "patient teacher"],
            "频次": ["science every week", "labs monthly"],
            "感受": ["curious", "proud of reports", "less boring"],
        },
        sample=(
            "Biology was my favourite because experiments showed results quickly — colour changes made ideas real. "
            "A patient science teacher let us retry when we failed, so labs felt less boring. "
            "We had science every week with labs about monthly. "
            "I stayed curious and proud when our group reports worked."
        ),
        sampleZh=(
            "最喜欢生物——实验很快就看到结果，颜色一变概念就活了。"
            "科学老师耐心，失败还能重做，实验不腻。"
            "每周有科学课，大概每月一次实验。"
            "保持好奇，小组报告成功时特别有成就感。"
        ),
    )
    _p(
        "What was your favourite subject at secondary school?",
        "yellow_bike_gift",
        logic="先答最喜欢体育或课外骑行情形，但用骑车上学活力说清楚对学校的喜爱，仍扣「科目/校园生活」。",
        kitHint="骑车活力：最喜欢=体育/活动课带来与骑车类似的放松（学校生活细节答 Q）。",
        words={
            "正面回答": ["PE", "Outdoor energy", "Break from desks"],
            "原因或时间": ["cycled to school", "fresh after riding", "team games"],
            "频次": ["twice a week PE", "daily bike commute"],
            "感受": ["awake", "less stiff", "fun"],
        },
        sample=(
            "PE was my favourite subject because it woke me up after cycling to school. "
            "Team games outdoors were a fun break from desks, especially after morning rides on my yellow bike. "
            "We had PE twice a week plus my daily bike commute. "
            "I felt awake, less stiff, and actually looked forward to class."
        ),
        sampleZh=(
            "最喜欢体育——骑车到学校后再上体育课特别精神。"
            "户外运动是对着课桌的调节，尤其早上骑小黄车来之后。"
            "每周两节体育，加上每天骑车通勤。"
            "人清醒、身子不僵，还挺期待上课。"
        ),
    )
    _p(
        "How did you usually spend your breaks at school?",
        "school_choir_songs",
        logic="先答课间常和同学哼歌或排练，再写走廊/音乐教室场景，说习惯影响。",
        kitHint="行为习惯：课间=哼唱排练。",
        words={
            "正面回答": ["Hummed songs", "Quick choir practice", "With close friends"],
            "原因": ["music show coming", "needed a break", "small group fun"],
            "时间线+行为描述": ["finish class", "walk to music room", "ten-minute rehearsal", "grab water"],
            "影响": ["less sleepy", "bond with classmates", "ready for shows"],
        },
        sample=(
            "I usually spent breaks humming songs or doing quick choir practice with close friends. "
            "A show was always coming, and singing woke me up more than sitting. "
            "We finished class, walked to the music room for ten minutes, then grabbed water before the bell. "
            "It bonded us and kept us ready for performances."
        ),
        sampleZh=(
            "课间常跟熟友哼歌或短排练。"
            "演出总在下一场，唱歌比干坐着醒神。"
            "下课走去音乐教室练十分钟，再抢在铃响前喝水。"
            "感情更近，演出也更跟得上。"
        ),
    )
    _p(
        "How did you usually spend your breaks at school?",
        "school_science_lab",
        logic="先答课间会讨论实验或看标本，再写走廊聊天链，说对成绩与兴趣的影响。",
        kitHint="课间=聊实验、看笔记，科学课堂延伸。",
        words={
            "正面回答": ["Talked about labs", "Checked notes", "Asked teacher quick questions"],
            "原因": ["exam soon", "curious results", "group report due"],
            "时间线+行为描述": ["open notebook", "compare colour changes", "line up at office"],
            "影响": ["clearer reports", "less panic", "science stayed fun"],
        },
        sample=(
            "I usually discussed labs or compared notes with classmates during breaks. "
            "We were curious about colour changes and nervous before group reports. "
            "We opened notebooks in the corridor, then sometimes lined up at the teacher's office with quick questions. "
            "Breaks made reports clearer and kept science fun instead of panicky."
        ),
        sampleZh=(
            "课间常跟同学聊实验、对笔记。"
            "好奇颜色变化，也怕小组报告。"
            "走廊摊开本子，有时去办公室门口排队问老师。"
            "课间把报告理清楚，科学课好玩而不是慌。"
        ),
    )
    _p(
        "How did you usually spend your breaks at school?",
        "yellow_bike_gift",
        logic="先答课间去车棚看车或和同学聊骑行，再写十分钟动线，说提神影响。",
        kitHint="课间骑车圈：行为链=车棚+短聊。",
        words={
            "正面回答": ["Bike shed", "Short walks", "Chat about rides"],
            "原因": ["needed fresh air", "rain coming", "fix a chain"],
            "时间线+行为描述": ["run downstairs", "check yellow bike", "talk at gate", "back before bell"],
            "影响": ["awake for next class", "small freedom", "closer friends"],
        },
        sample=(
            "I usually ran to the bike shed during breaks to check my yellow bike or chat about rides. "
            "Fresh air woke me up, and friends warned each other when rain was coming. "
            "Downstairs, a quick look at the chain, talk at the gate, then back before the bell — only ten minutes. "
            "I felt awake for the next class and enjoyed that small freedom with closer friends."
        ),
        sampleZh=(
            "课间常跑下车棚看小黄车，或聊骑车的事。"
            "透口气醒神，朋友也会互相提醒要下雨。"
            "下楼看一下链条，门口聊几句，铃响前赶回教室——就十分钟。"
            "下节课精神些，那点自由也拉近了朋友。"
        ),
    )
    _p(
        "How are secondary schools today different from when you were there?",
        "school_choir_songs",
        logic="先答如今更重视素质与社团但时间仍紧，再对比当年合唱机会，说个人感受。",
        kitHint="对比：现在社团资源 vs 当年简单合唱。",
        words={
            "正面回答": ["More clubs", "Still exam-heavy", "Better equipment maybe"],
            "选项1的特点与作用": ["today: maker clubs, streaming shows", "parents pay for tutors"],
            "选项2的特点与作用": ["my time: simple choir", "fewer facilities", "less homework online"],
            "个人感受": ["mixed", "kids still stressed", "music access improved"],
        },
        sample=(
            "Schools today offer more clubs and better gear for shows, but exams still dominate. "
            "Students stream performances online, while we only had a simple choir and a rusty piano. "
            "Parents pay heavily for tutors now; homework arrives on apps instead of paper. "
            "I feel mixed — music access improved, yet kids look just as stressed."
        ),
        sampleZh=(
            "现在学校社团更多、演出设备更好，但考试压力仍大。"
            "学生能把演出上网，我们只有简单合唱和老钢琴。"
            "家长砸钱补课，作业也走 App 了。"
            "感受复杂——音乐资源好了，孩子看着一样紧绷。"
        ),
    )
    _p(
        "How are secondary schools today different from when you were there?",
        "school_science_lab",
        logic="先答实验数字化更多但动手机会应保留，再对比自己当年的实验室，说看法。",
        kitHint="对比：现在虚拟实验 vs 当年动手 lab。",
        words={
            "正面回答": ["More simulations", "Safer labs", "Still need hands-on"],
            "选项1的特点与作用": ["today: VR demos", "online pre-labs", "stricter safety"],
            "选项2的特点与作用": ["my time: real flames", "handwritten logs", "smaller kits"],
            "个人感受": ["progress but balance", "hope they keep real tests", "interesting change"],
        },
        sample=(
            "Science teaching today uses more simulations and online pre-labs, with stricter safety rules. "
            "Students may watch VR demos before touching equipment. "
            "When I was there we had real flames, handwritten logs, and smaller kits but more smell and fun. "
            "Progress is clear, though I hope schools still keep real tests — the change is interesting."
        ),
        sampleZh=(
            "现在科学课更多模拟和线上预习，安全规定也更严。"
            "学生可能先戴 VR 看演示再摸器材。"
            "我那会儿是真火、手写记录、套件小但味道足、也好玩。"
            "进步明显，但希望别丢掉真做实验——这变化挺有意思。"
        ),
    )
    _p(
        "How are secondary schools today different from when you were there?",
        "yellow_bike_gift",
        logic="先答现在电动车与门禁更多，骑车入校政策变严，再对比当年自由骑车，说感受。",
        kitHint="对比：现在交通/门禁 vs 当年骑车自由。",
        words={
            "正面回答": ["Stricter gates", "More e-bikes", "Helmet rules"],
            "选项1的特点与作用": ["today: register bikes", "security cards", "shared bikes outside"],
            "选项2的特点与作用": ["my time: yellow bike at gate", "park anywhere", "shorter commutes"],
            "个人感受": ["safer maybe", "less romantic", "understand the rules"],
        },
        sample=(
            "Gates and traffic rules feel stricter now — students register bikes and wear helmets more often. "
            "Shared bikes pile up outside, while e-bikes buzz past the security card readers. "
            "When I was there I parked my yellow bike freely near the gate and commuted in minutes. "
            "It may be safer today, but less romantic — still, I understand why rules tightened."
        ),
        sampleZh=(
            "现在校门和交规更严——自行车要登记，头盔也更常见。"
            "校门口堆着共享单车，电动车嗡嗡过门禁。"
            "我那会儿小黄车随便停门口，几分钟就到。"
            "也许更安全，但没那么浪漫了——规矩变严我也理解。"
        ),
    )