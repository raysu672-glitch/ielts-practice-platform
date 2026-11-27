# -*- coding: utf-8 -*-
"""Opportunities and Work or studies Freestyle packs."""


def register(_p):
  # --- Opportunities ---
    # 童年新活动：黄自行车 + 校园通知（不要挂微信短视频）
    _p(
        "Did you have any opportunities to take part in new activities as a child?",
        "yellow_bike_gift",
        logic="①正面：有，学会自己骑车 ②举例：妈妈送黄自行车 ③频次：之后天天骑 ④感受：自由方便。",
        kitHint="童年新活动=骑车；黄自行车直接服务本题。",
        words={
            "正面回答": ["Yes, I did", "Learning to cycle", "A new outdoor activity"],
            "来源或举例": ["yellow bike from mum", "ride to school", "weekend park"],
            "频次": ["every day after that", "at weekends too"],
            "感受": ["free", "convenient", "more independent"],
        },
        sample=(
            "Yes, I did. One new activity was learning to cycle on my own. "
            "My mum bought me a small yellow bike as a birthday gift in junior high. "
            "I rode it to school every day after that, and to the park at weekends. "
            "It felt free and convenient."
        ),
        sampleZh=(
            "有的。一个新活动是学会自己骑车。"
            "初中生日妈妈送了我一辆黄色小自行车。"
            "之后我天天骑车上学，周末也去公园。"
            "觉得自由又方便。"
        ),
    )
    _p(
        "Did you have any opportunities to take part in new activities as a child?",
        "campus_opportunity_notice",
        logic="①正面：有，参加过学校活动 ②举例：老师布告栏通知 ③频次：初中一次夏令营 ④感受：紧张后开心。",
        kitHint="童年新活动=学校通知带来的营队/比赛。",
        words={
            "正面回答": ["Yes, I did", "A school camp", "A teacher notice"],
            "来源或举例": ["notice on the board", "short essay", "summer camp"],
            "频次": ["once in junior high", "one full week"],
            "感受": ["nervous then happy", "proud", "glad I tried"],
        },
        sample=(
            "Yes, I did. I joined a summer camp after a teacher put a notice on the board. "
            "I wrote a short essay and handed it in with my classmates. "
            "It happened once in junior high and lasted a full week. "
            "I felt nervous at first, then happy I tried."
        ),
        sampleZh=(
            "有的。老师在布告栏贴通知后，我参加了一次夏令营。"
            "我和同学一起交了小短文报名。"
            "初中就那一次，营队有一整周。"
            "先紧张，后来很高兴自己试了。"
        ),
    )
    _p(
        "How do you find out about new opportunities?",
        "business_major_path",
        logic="先答通过学院通知、学长和商科群，再举例实习帖，说查看频率与实用感受。",
        kitHint="商科线：找机会=专业相关通知与学长渠道。",
        words={
            "正面回答": ["School notices", "Senior students", "Major group chats"],
            "来源或举例": ["internship posts", "business club", "career office email"],
            "频次": ["a few times a week", "before holiday hiring"],
            "感受": ["relevant", "trustworthy", "worth checking"],
        },
        sample=(
            "I find out through school notices and chats with senior business majors. "
            "Our career office emails internship posts, and classmates forward useful links in the major group. "
            "I check that a few times a week, especially before holiday hiring season. "
            "It feels relevant and trustworthy enough to act on."
        ),
        sampleZh=(
            "主要靠学院通知和学长学姐、专业群。"
            "就业办发实习帖，群里也会转链接。"
            "一周看几次，假期招聘前更勤。"
            "跟专业相关，可信度也够，值得点进去。"
        ),
    )
    _p(
        "How do you find out about new opportunities?",
        "phone_xiaohongshu_wechat",
        logic="先答微信班群与小红书种草帖，再说明筛选信息习惯，说每天刷的频率。",
        kitHint="社媒渠道：机会=微信群+小红书，但要说如何甄别。",
        words={
            "正面回答": ["WeChat groups", "Xiaohongshu posts", "Douyin clips"],
            "来源或举例": ["class chat", "event ads", "student bloggers"],
            "频次": ["daily quick scroll", "before weekends"],
            "感受": ["noisy but fast", "double-check", "handy"],
        },
        sample=(
            "I find new opportunities mostly through WeChat class groups and Xiaohongshu posts students share. "
            "People forward competition ads or part-time jobs, and short Douyin clips pop up too. "
            "I do a quick scroll daily but double-check on official sites before signing up. "
            "It is noisy yet fast — handy if you verify."
        ),
        sampleZh=(
            "新机会主要靠微信班群和同学转的小红书帖。"
            "竞赛、兼职广告很多，抖音短片也会刷到。"
            "我每天快扫一遍，但报名前会去官网核实。"
            "信息吵但快——核实了就挺省事。"
        ),
    )
    _p(
        "How do you find out about new opportunities?",
        "study_websites_search",
        logic="先答主动搜索官网与论坛，再举留学实习关键词例子，说需要时的频率。",
        kitHint="查资料网站：找机会=主动 search，不全靠推送。",
        words={
            "正面回答": ["Search online", "Official sites", "Forums"],
            "来源或举例": ["career keywords", "government youth pages", "university portals"],
            "频次": ["when planning", "once or twice a month"],
            "感受": ["slower but clear", "less spam", "reliable"],
        },
        sample=(
            "I search official sites and forums when I actively plan next steps. "
            "I type career keywords on university portals or government youth pages for internships. "
            "That is slower than group chats, so I do it once or twice a month when planning. "
            "It feels clearer, with less spam and more reliable details."
        ),
        sampleZh=(
            "主动规划时会去搜官网和论坛。"
            "在学校门户、青年政策站打实习之类关键词。"
            "比群聊慢，一般一个月一两次在规划时做。"
            "更清楚，广告少，信息也更靠谱。"
        ),
    )
    _p(
        "What is one good opportunity you had when you were younger?",
        "campus_opportunity_notice",
        logic="先答中学时参加过一次竞赛/夏令营通知带来的机会，再写报名过程与频率感受。",
        kitHint="校园通知：童年/少年好机会=老师发的活动帖。",
        words={
            "正面回答": ["A summer camp", "Notice on the board", "Teacher pushed us"],
            "来源或举例": ["class bulletin", "application form", "short essay"],
            "频次": ["once in junior high", "a full week camp"],
            "感受": ["nervous then proud", "opened doors", "grateful"],
        },
        sample=(
            "One good opportunity was a summer science camp I joined in junior high after a teacher pinned the notice on our board. "
            "She pushed quiet students like me to hand in a short essay and apply. "
            "It happened once, but the camp lasted a full week. "
            "I was nervous then proud — it opened doors and I am still grateful."
        ),
        sampleZh=(
            "初中参加过一次暑期科学营，老师在布告栏贴了通知。"
            "她鼓励像我这样内向的同学写小短文报名。"
            "就这么一次，但营队有一整周。"
            "先紧张后骄傲——开了眼界，一直很感激。"
        ),
    )
    _p(
        "What is one good opportunity you had when you were younger?",
        "yellow_bike_gift",
        logic="先答妈妈送黄自行车让我开始独立骑行的新活动机会，再写骑车频率与自由感受。",
        kitHint="黄自行车=童年新活动机会（硬规则5）。",
        words={
            "正面回答": ["Learning to cycle alone", "Birthday gift", "New freedom"],
            "来源或举例": ["small yellow bike", "ride to school", "weekend park"],
            "频次": ["every day after that", "weekends about an hour"],
            "感受": ["convenient", "exciting", "more independent"],
        },
        sample=(
            "A great opportunity was when my mum bought me a small yellow bike as a birthday gift in junior high. "
            "That was the first time I really cycled on my own to school and later to the park at weekends. "
            "I rode almost every day after that, about an hour at weekends. "
            "It felt exciting, convenient, and much more independent."
        ),
        sampleZh=(
            "很好的机会是初中生日妈妈送我一辆黄色小自行车。"
            "那是我第一次真能自己骑车上学，周末也去公园。"
            "之后几乎每天骑，周末大约一小时。"
            "又兴奋又方便，也独立了很多。"
        ),
    )
    _p(
        "What is one good opportunity you had when you were younger?",
        "business_major_path",
        logic="先答高中时参加商业社团/集市活动雏形，再连现在读商科的兴趣线，说频率与影响。",
        kitHint="商科线：少年机会=商业相关活动，衔接到专业兴趣。",
        words={
            "正面回答": ["Business club fair", "Sold simple snacks", "Teamwork"],
            "来源或举例": ["school market day", "price tags", "counting money"],
            "频次": ["once a year", "two afternoons"],
            "感受": ["fun", "sparked interest", "led to my major"],
        },
        sample=(
            "One good opportunity was our school market day — I joined a tiny business team selling snacks, with price tags, teamwork and counting money. "
            "It was only two afternoons once a year, but it felt real. "
            "That fun sparked interest in how companies work and later nudged me toward a business major. "
            "I still think that small fair shaped my path."
        ),
        sampleZh=(
            "一次好机会是学校集市日——我加入卖零食的小组，标价、分工、数钱。"
            "一年就两个下午，但像真做生意。"
            "好玩，也让我对公司运作感兴趣，后来读了商科。"
            "那次小集市仍影响我的选择。"
        ),
    )
    _p(
        "Why do some people miss good opportunities?",
        "business_major_path",
        logic="先答太忙备考或犹豫实习，再举同学因怕失败不投简历例子，说观察频率与个人警示。",
        kitHint="商科视角：错过=忙碌+怕试错，联系到求职。",
        words={
            "正面回答": ["Too busy", "Fear failure", "Wait too long"],
            "来源或举例": ["exam season", "unread emails", "perfect résumé"],
            "频次": ["every term", "before deadlines"],
            "感受": ["understandable", "regret later", "need reminders"],
        },
        sample=(
            "Some people miss chances because they are buried in exams or afraid a résumé is not perfect. "
            "Classmates leave career emails unread until internships close. "
            "I see that every term right before deadlines. "
            "It is understandable, but many regret it later — reminders help."
        ),
        sampleZh=(
            "有人因为埋头考试或怕简历不够完美而错过。"
            "同学常把就业邮件搁到实习截止才看。"
            "每学期截止前都能看到。"
            "能理解，但不少人后来后悔——提醒很重要。"
        ),
    )
    _p(
        "Why do some people miss good opportunities?",
        "phone_xiaohongshu_wechat",
        logic="先答信息太多反而忽略，再举群消息刷屏例子，说每天现象与个人对策。",
        kitHint="社媒噪音：错过=刷太快没细看官方信息。",
        words={
            "正面回答": ["Too many posts", "Scroll past", "Trust wrong links"],
            "来源或举例": ["chat flood", "fake ads", "clickbait titles"],
            "频次": ["daily on phones", "peak at night"],
            "感受": ["overwhelmed", "need filters", "easy to ignore real ones"],
        },
        sample=(
            "Feeds move so fast that real opportunities get lost in jokes and ads. "
            "A useful WeChat notice sinks under hundreds of stickers, or a Xiaohongshu post looks like clickbait. "
            "That happens daily, especially at night when people scroll lazily. "
            "People feel overwhelmed and ignore the good ones unless they pin or verify."
        ),
        sampleZh=(
            "信息流太快，真机会淹没在段子和广告里。"
            "有用的微信通知被表情包顶走，小红书标题也像钓鱼。"
            "天天如此，晚上躺刷更严重。"
            "信息过载就容易错过，除非置顶或核实。"
        ),
    )
    _p(
        "Why do some people miss good opportunities?",
        "study_websites_search",
        logic="先答懒得查官网、只等别人转发，再举搜索关键词就能找到却没人做，说反思感受。",
        kitHint="主动搜索：错过=不主动查，只被动等。",
        words={
            "正面回答": ["Passive", "Do not search", "Assume it is too late"],
            "来源或举例": ["official portal", "clear deadlines online", "PDF guide"],
            "频次": ["each intake season", "when news breaks"],
            "感受": ["frustrating", "avoidable", "need habit"],
        },
        sample=(
            "Some miss opportunities simply because they never search official pages — they wait for someone else to forward links. "
            "Deadlines and PDF guides are often clear online if you type two keywords. "
            "Each intake season I watch friends assume it is too late without checking. "
            "It is frustrating but avoidable with a small search habit."
        ),
        sampleZh=(
            "有人从不查官网，只等别人转链接就错过了。"
            "打两个关键词，截止日和 PDF 指南网上常有。"
            "每季招生都有人没点开就以为来不及。"
            "挺懊恼，其实养成搜一下就能避免。"
        ),
    )
    _p(
        "What kind of opportunity would you like to have in the next few years?",
        "campus_opportunity_notice",
        logic="先答想要优质实习或交换项目，再说明通过学校通知争取，说期待频率与生涯影响。",
        kitHint="校园机会：未来想要=实习/交换，扣 notice 渠道。",
        words={
            "正面回答": ["Solid internship", "Exchange term", "Mentor access"],
            "原因或时间": ["career office", "third year", "before graduation"],
            "频次": ["hope once", "maybe twice if lucky"],
            "感受": ["excited", "nervous", "ready to apply early"],
        },
        sample=(
            "I would like a solid internship or maybe a short exchange term in the next few years. "
            "Campus notices usually list those with mentor access, and I want to apply early in third year. "
            "Even one placement would help, twice if lucky. "
            "I feel excited and a bit nervous, but ready to watch the board."
        ),
        sampleZh=(
            "接下来几年想要像样的实习，或者短期交换。"
            "校园通知常列这类项目、也有导师，我打算大三提早申。"
            "有一次就很好，运气好两次也行。"
            "兴奋也有点紧，但会盯着通知。"
        ),
    )
    _p(
        "What kind of opportunity would you like to have in the next few years?",
        "business_major_path",
        logic="先答希望进相关企业实习并接触真实项目，再连商科就业路径，说时间与职业规划感受。",
        kitHint="商科未来机会=实习+就业路径语言（硬规则2预热）。",
        words={
            "正面回答": ["Industry internship", "Real projects", "Path to a job"],
            "原因或时间": ["after core courses", "summer breaks", "before thesis"],
            "频次": ["target one per year", "two months each"],
            "感受": ["motivated", "build CV", "test the field"],
        },
        sample=(
            "I hope for an industry internship with real projects, not only classroom cases. "
            "As a business major I want to test marketing or operations after core courses, maybe each summer. "
            "One placement a year, two months each, would build my CV before graduation. "
            "I feel motivated to see if that career path fits."
        ),
        sampleZh=(
            "希望进企业实习做真项目，不只课堂案例。"
            "商科读完核心课想在营销或运营试试，可能每个暑假。"
            "一年一段、每段两月，毕业前把简历做起来。"
            "很有动力，看这职业路线适不适合我。"
        ),
    )
    _p(
        "What kind of opportunity would you like to have in the next few years?",
        "phone_xiaohongshu_wechat",
        logic="先答想通过线上社群认识跨校活动或副业，再举例靠谱 KOL 推送，说筛选频率与开放心态。",
        kitHint="社媒机会=线上活动/合作，但要提甄别。",
        words={
            "正面回答": ["Cross-campus events", "Online collabs", "Trusted creators"],
            "原因或时间": ["follow reliable bloggers", "classmate invites", "holiday time"],
            "频次": ["when spare time", "a few tries a year"],
            "感受": ["open but careful", "networking", "fun if real"],
        },
        sample=(
            "I would like cross-campus events or small online collabs found through trusted creators on Xiaohongshu or WeChat circles. "
            "Holiday spare time is when classmates invite short projects or competitions. "
            "I might try a few a year after checking organisers. "
            "I am open but careful — real ones are fun for networking."
        ),
        sampleZh=(
            "想通过靠谱博主、微信圈子找跨校活动或小合作。"
            "假期空档同学会叫一起参加比赛、短项目。"
            "核实主办方后一年试几次。"
            "心态开放也谨慎——真的话挺好拓展人脉。"
        ),
    )
    _p(
        "Do you usually take an opportunity when it comes along?",
        "campus_opportunity_notice",
        logic="先答官方通知且时间允许就会尝试，再写报名小动作链，说习惯影响。",
        kitHint="行为习惯：有好通知+匹配就行动。",
        words={
            "正面回答": ["Often yes", "If it fits", "If deadline allows"],
            "原因": ["trust official source", "fear missing once", "low cost to try"],
            "时间线+行为描述": ["read notice", "ask teacher", "submit form", "prepare interview"],
            "影响": ["more experiences", "less regret", "busy schedule"],
        },
        sample=(
            "Often yes — I usually take an opportunity if the campus notice fits my level and the deadline still allows. "
            "I trust official sources, read carefully, ask a teacher one question, then submit the form. "
            "Sometimes I prep a short interview the same week. "
            "It adds experiences and leaves less regret, though my schedule gets busier."
        ),
        sampleZh=(
            "多半会——校内通知对得上、截止还来得及，我就会抓住这个机会。"
            "信官方渠道，细读、问老师一句，就交表。"
            "同一周也许准备个小面试。"
            "经历多了、后悔少，就是日程更满。"
        ),
    )
    _p(
        "Do you usually take an opportunity when it comes along?",
        "business_major_path",
        logic="先答会衡量是否利职业规划，匹配实习就投，再写筛选步骤与影响。",
        kitHint="商科生：抓机会=看 career 匹配度。",
        words={
            "正面回答": ["If it matches", "Internships yes", "Skip random"],
            "原因": ["build CV", "learn industry", "time limited"],
            "时间线+行为描述": ["check job description", "tailor résumé", "email career office", "wait reply"],
            "影响": ["clearer path", "miss fun events sometimes", "worth it"],
        },
        sample=(
            "I usually take it when it matches my business major and career plan — internships yes, random gigs no. "
            "I read the job description, tailor my résumé, email the career office, then wait. "
            "That filter takes an evening, but it saves time later. "
            "My path looks clearer even if I miss some fun side events."
        ),
        sampleZh=(
            "跟商科规划和职业相关我就上——实习行，乱杂兼职一般不接。"
            "看岗位说明、改简历、发就业办，等回复。"
            "筛选要花一个晚上，但能省后面时间。"
            "路线更清楚，就算错过些好玩的也值得。"
        ),
    )
    _p(
        "Do you usually take an opportunity when it comes along?",
        "phone_xiaohongshu_wechat",
        logic="先答先核实再决定，再写看到群帖后的核对步骤，说被坑教训影响。",
        kitHint="社媒机会：行为=先 verify 再报名。",
        words={
            "正面回答": ["Depends", "Verify first", "Sometimes skip"],
            "原因": ["fake ads", "scam fear", "limited time"],
            "时间线+行为描述": ["see post", "search organiser", "ask friend", "sign or ignore"],
            "影响": ["fewer mistakes", "slower but safer", "peace of mind"],
        },
        sample=(
            "It depends — I verify before I act on a WeChat or Xiaohongshu post. "
            "I search the organiser, ask a friend who joined last year, then sign or ignore. "
            "Fake ads taught me that one scam wastes more time than checking. "
            "I move slower but feel safer and make fewer mistakes."
        ),
        sampleZh=(
            "看情况——微信小红书上的帖我会先核实再动。"
            "搜主办方、问去年参加的朋友，再决定报不报。"
            "假广告教会我：被骗一次比核查更费时。"
            "慢一点但安心，踩坑也少。"
        ),
    )
    _p(
        "Is it important to seize opportunities when they come?",
        "business_major_path",
        logic="先正面肯定，再从实习与学位规划举因，说错失的代价与干劲感受。",
        kitHint="观点：抓住机会=career 硬规则，degree/internship 语言。",
        words={
            "正面回答": ["Yes", "Especially early career", "Degrees have windows"],
            "举例或原因": ["internship slots", "competition deadlines", "limited places"],
            "作用或影响": ["build experience", "network", "graduate jobs"],
            "感受": ["motivated", "a bit anxious", "worth the effort"],
        },
        sample=(
            "Yes — especially when you are still studying for a degree. "
            "Internship places and competition places close fast, and they help with later jobs. "
            "If you take them, you learn skills you cannot easily get later. "
            "It makes me motivated and a bit nervous, but it is worth it."
        ),
        sampleZh=(
            "重要——尤其还在读书的时候。"
            "实习和比赛名额关得快，对以后找工作也有帮助。"
            "抓住了能学到后面不容易补的本事。"
            "让我有干劲也有点紧张，但值得。"
        ),
    )
    _p(
        "Is it important to seize opportunities when they come?",
        "phone_xiaohongshu_wechat",
        logic="先答重要但别盲目，再举社媒真假混杂例子，说甄别后的正面影响与感受。",
        kitHint="观点：抓机会+社媒甄别并行。",
        words={
            "正面回答": ["Yes, but carefully", "Check online posts", "Balance time"],
            "举例或原因": ["scam posts", "real free lectures", "time on phone"],
            "作用或影响": ["avoid traps", "catch good events", "safer feed"],
            "感受": ["careful but hopeful", "less worried", "still try"],
        },
        sample=(
            "Yes, it is important to take opportunities — but carefully, because not every WeChat link is safe. "
            "Some posts are scams, others are real free lectures worth one evening. "
            "Checking first helps me avoid traps and still catch good chances. "
            "I feel careful but hopeful, and I still try when it looks real."
        ),
        sampleZh=(
            "抓住机会很重要，但要小心——微信上不是每个链接都安全。"
            "有诈骗帖，也有值得花一晚上的免费讲座。"
            "先核实能避陷阱，也不错过好机会。"
            "我会小心，但也抱希望，看着真就会试试。"
        ),
    )
    _p(
        "Is it important to seize opportunities when they come?",
        "study_websites_search",
        logic="先肯定主动查信息再行动，再举官网信息易错过例子，说作用与踏实感受。",
        kitHint="观点：抓机会=先 search 再决定。",
        words={
            "正面回答": ["Yes", "Information is online", "Plan ahead"],
            "举例或原因": ["scholarship pages", "hidden deadlines", "quiet programs"],
            "作用或影响": ["fairer access", "less about luck", "better choices"],
            "感受": ["more in control", "less regret", "needs effort"],
        },
        sample=(
            "Yes — taking opportunities matters because clear information is already online if you search. "
            "Scholarships and exchange programs hide on pages people never open. "
            "Planning ahead makes things fairer and less about luck. "
            "I feel more in control and have less regret, though it needs effort."
        ),
        sampleZh=(
            "重要——抓住机会有用，很多信息网上查得到。"
            "奖学金、交换项目躲在没人打开的页面里。"
            "提早规划更公平，少靠运气。"
            "觉得更有掌控、后悔也少，但要花功夫。"
        ),
    )

  # --- Work or studies ---
    # Band 6 口语：四步各一句，用词简单能开口；忌 purposeful/ambitious/graduate hire 等书面词。

    # 1) Do you work or are you a student?
    _p(
        "Do you work or are you a student?",
        "study_library_classes",
        logic="①正面：我是学生 ②举例：上课+图书馆 ③频次：工作日 ④感受：忙有时累。",
        kitHint="身份题只答学生；图书馆是日常学习场景。",
        words={
            "正面回答": ["I'm a student", "I study on campus", "Not working yet"],
            "来源或举例": ["go to classes", "study in the library", "with classmates"],
            "频次": ["most weekdays", "Monday to Friday"],
            "感受": ["busy", "a bit tired", "OK overall"],
        },
        sample=(
            "I'm a student. I don't have a job yet. "
            "I go to classes in the day and study in the library with friends in the evening. "
            "I do that most weekdays, from Monday to Friday. "
            "I feel busy, and sometimes a bit tired."
        ),
        sampleZh=(
            "我是学生，还没有工作。"
            "白天上课，晚上和朋友在图书馆学。"
            "多数周一到周五都这样。"
            "觉得忙，有时也有点累。"
        ),
    )
    _p(
        "Do you work or are you a student?",
        "business_major_path",
        logic="①正面：商科学生 ②举例：上课和小组作业 ③频次：每周 ④感受：有时难但还行。",
        kitHint="身份=商科在读；课表细节服务「学生」。",
        words={
            "正面回答": ["I'm a student", "I study business", "On campus"],
            "来源或举例": ["business classes", "group projects", "homework"],
            "频次": ["every week", "most days in term"],
            "感受": ["busy", "a bit hard", "still OK"],
        },
        sample=(
            "I'm a student. I study business on campus. "
            "My week is mostly classes and group projects. "
            "That happens every week in term time. "
            "It feels busy and a bit hard, but I'm OK with it."
        ),
        sampleZh=(
            "我是学生，在学校读商科。"
            "一周主要是上课和小组作业。"
            "学期里每周都这样。"
            "忙，有点难，但还能接受。"
        ),
    )
    # 2) Why did you choose that job or that subject?
    _p(
        "Why did you choose that job or that subject?",
        "business_major_path",
        logic="①正面：好找工作、自己也喜欢 ②举例：实习机会、学长说法 ③频次：填志愿时定 ④感受：不后悔。",
        kitHint="选专业主因=工作机会+兴趣。",
        words={
            "正面回答": ["More job choices", "I liked business", "Clearer path"],
            "来源或举例": ["internship chances", "case classes", "seniors' advice"],
            "频次": ["before I applied", "still the same now"],
            "感受": ["happy with it", "no regret", "useful"],
        },
        sample=(
            "I chose business because there are more job choices later. "
            "I also liked the classes, and seniors said it was a good path. "
            "I decided that before I applied, and I still feel the same. "
            "I'm happy with it and I have no regret."
        ),
        sampleZh=(
            "选商科是因为以后工作选择更多。"
            "我也喜欢这些课，学长说这条路不错。"
            "填志愿前就定了，现在想法还一样。"
            "挺满意，也不后悔。"
        ),
    )
    _p(
        "Why did you choose that job or that subject?",
        "study_library_classes",
        logic="①正面：喜欢慢慢学、查资料 ②举例：图书馆看书比只看幻灯片 ③频次：大一定 ④感受：现在还喜欢。",
        kitHint="主因是喜欢这种学法；图书馆是举例。",
        words={
            "正面回答": ["I like reading", "It fits me", "Not a random choice"],
            "来源或举例": ["books in the library", "not only slides", "quiet study"],
            "频次": ["in year one", "I still think so"],
            "感受": ["sure about it", "still enjoy it", "comfortable"],
        },
        sample=(
            "I chose this subject because it fits me — I like reading and learning slowly. "
            "Books in the library help me more than only slides. "
            "I decided in year one, and I still think so. "
            "I feel sure about this course, and I still enjoy it."
        ),
        sampleZh=(
            "选这个专业因为适合我——我喜欢看书、慢慢学。"
            "图书馆的书比只看幻灯片更帮得上我。"
            "大一定的，现在还这么想。"
            "对这门课觉得确定，也还喜欢。"
        ),
    )
    # 3) What do you find most challenging...?
    _p(
        "What do you find most challenging about your work or your studies?",
        "study_library_classes",
        logic="①正面：阅读最难 ②举例：厚书要在图书馆看很久 ③频次：考试周 ④感受：累但值得。",
        kitHint="挑战=阅读多；图书馆是学习地点。",
        words={
            "正面回答": ["Heavy reading", "Too many pages", "Hard before exams"],
            "来源或举例": ["thick books", "long time in the library", "taking notes"],
            "频次": ["before exams", "essay weeks"],
            "感受": ["tired", "stressed", "worth it"],
        },
        sample=(
            "Heavy reading is the hardest part for me. "
            "The books are thick, so I stay in the library for a long time and take notes. "
            "It is worse before exams and in essay weeks. "
            "I feel tired and stressed, but it is worth it when I understand."
        ),
        sampleZh=(
            "对我来说最难的是阅读量大。"
            "书很厚，我要在图书馆待很久、做笔记。"
            "考前和写论文周更明显。"
            "又累又有压力，但看懂了就觉得值得。"
        ),
    )
    _p(
        "What do you find most challenging about your work or your studies?",
        "business_major_path",
        logic="①正面：小组作业最难 ②举例：分工、英语词、赶PPT ③频次：每学期 ④感受：有压力但在进步。",
        kitHint="挑战落在商科小组作业。",
        words={
            "正面回答": ["Group projects", "Case work", "Presentations"],
            "来源或举例": ["share the work", "English words", "finish the slides"],
            "频次": ["each term", "around midterm"],
            "感受": ["stressed", "getting better", "still hard"],
        },
        sample=(
            "Group projects are the hardest part. "
            "We have to share the work, learn English words, and finish the slides on time. "
            "That happens each term, especially around midterm. "
            "I feel stressed, but I am getting a bit better."
        ),
        sampleZh=(
            "最难的是小组作业。"
            "要分工、学英语词，还要按时做完幻灯片。"
            "每学期都有，期中更忙。"
            "有压力，但慢慢好一点。"
        ),
    )
    # 4) What do you like most...?
    _p(
        "What do you like most about your job or your studies?",
        "study_library_classes",
        logic="①正面：最喜欢图书馆安静看书 ②原因：比宿舍安静 ③频次：一周两次 ④感受：平静。",
        kitHint="先答喜欢什么；图书馆是场景。",
        words={
            "正面回答": ["Quiet library time", "Reading real books", "A quiet place"],
            "原因或时间": ["quieter than the dorm", "easy to focus", "after class"],
            "频次": ["twice a week", "more before exams"],
            "感受": ["peaceful", "relaxed", "happy"],
        },
        sample=(
            "I like quiet time in the library the most. "
            "It is quieter than the dorm, so I can focus better. "
            "I go about twice a week, and more before exams. "
            "I find it peaceful and I feel happier there."
        ),
        sampleZh=(
            "我最喜欢在图书馆安静待着。"
            "比宿舍安静，更容易专心。"
            "大概一周两次，考前会更多。"
            "我觉得平静，待在那儿更开心。"
        ),
    )
    _p(
        "What do you like most about your job or your studies?",
        "business_major_path",
        logic="①正面：最喜欢课堂讨论 ②原因：能听到真实工作例子 ③频次：每周 ④感受：有意思。",
        kitHint="喜好落在商科课堂讨论。",
        words={
            "正面回答": ["Class discussions", "Talking about real jobs", "Group talk"],
            "原因或时间": ["teachers share job stories", "we share ideas", "in class"],
            "频次": ["every week", "most terms"],
            "感受": ["interesting", "useful", "more confident"],
        },
        sample=(
            "I like class discussions the most. "
            "Teachers share real job stories, and we can share our ideas. "
            "That happens every week. "
            "I find it interesting and useful."
        ),
        sampleZh=(
            "我最喜欢课堂讨论。"
            "老师会讲真实工作故事，我们也能说想法。"
            "每周都有。"
            "我觉得有意思，也有用。"
        ),
    )
    # 5) What is a typical day like...?
    _p(
        "What is a typical day like for you at work or at school?",
        "study_library_classes",
        logic="①正面：早上上课下午图书馆 ②时间：午饭后去 ③频次：多数工作日 ④感受：忙但还行。",
        kitHint="先描一天；图书馆是一环。",
        words={
            "正面回答": ["Morning classes", "Afternoon library", "Back in the evening"],
            "原因或时间": ["after lunch", "until about nine", "same most days"],
            "频次": ["most weekdays", "Friday shorter"],
            "感受": ["busy", "a bit tiring", "OK"],
        },
        sample=(
            "A typical school day is morning classes and afternoon library time. "
            "I go after lunch and often stay until about nine. "
            "Most weekdays look like that; Friday is shorter. "
            "It feels busy and a bit tiring, but it's OK."
        ),
        sampleZh=(
            "典型上学日是早上上课、下午去图书馆。"
            "午饭后过去，常常待到九点左右。"
            "多数工作日这样，周五短一点。"
            "忙，有点累，但还行。"
        ),
    )
    _p(
        "What is a typical day like for you at work or at school?",
        "business_major_path",
        logic="①正面：上课+小组讨论 ②时间：午饭改PPT、车上回邮件 ③频次：周一到周五 ④感受：忙。",
        kitHint="典型一天扣商科日程。",
        words={
            "正面回答": ["Business classes", "Group talks", "Some homework"],
            "原因或时间": ["between classes", "at lunch", "on the bus"],
            "频次": ["Monday to Friday", "sometimes Saturday"],
            "感受": ["busy", "a bit rushed", "still fine"],
        },
        sample=(
            "A typical day is business classes and short group talks between classes. "
            "At lunch we work on slides, and on the bus I check emails about internships. "
            "That is Monday to Friday, and sometimes Saturday too. "
            "It feels busy and a bit rushed, but still fine."
        ),
        sampleZh=(
            "典型一天是商科课，课间还有短小组讨论。"
            "午饭做幻灯片，公交上会看实习邮件。"
            "周一到周五这样，有时周六也有。"
            "忙，有点赶，但还行。"
        ),
    )
    # 6) What would you like to be doing... in a few years?
    _p(
        "What would you like to be doing in your career or studies in a few years?",
        "business_major_path",
        logic="①正面：毕业后找工作 ②原因：先实习再找全职 ③频次：暑假实习、大四找工作 ④感受：有点紧张但清楚。",
        kitHint="未来先答工作目标；用简单词。",
        words={
            "正面回答": ["Finish my degree", "Find a job", "Maybe start with an internship"],
            "原因或时间": ["after I graduate", "get some experience first", "in my final year"],
            "频次": ["internship in summer", "job hunt in the last year"],
            "感受": ["a bit nervous", "hopeful", "clear enough"],
        },
        sample=(
            "In a few years I want to finish my business degree and find a job. "
            "I may do a summer internship first to get some experience. "
            "I plan one internship in summer, and look for jobs in my final year. "
            "I feel a bit nervous, but the plan is clear enough."
        ),
        sampleZh=(
            "几年后想拿完商科学位，然后找工作。"
            "可能先做暑假实习，攒点经验。"
            "打算暑假实习一次，大四再找工作。"
            "有点紧张，但计划够清楚。"
        ),
    )
    _p(
        "What would you like to be doing in your career or studies in a few years?",
        "campus_opportunity_notice",
        logic="①正面：毕业后实习再工作 ②原因：看校园通知、问老师 ③频次：大三起常看 ④感受：踏实有盼头。",
        kitHint="未来=工作路径；校园通知是找机会的方式。",
        words={
            "正面回答": ["Finish my degree", "Do an internship", "Then a full-time job"],
            "原因或时间": ["campus notices", "ask teachers", "apply early"],
            "频次": ["check notices often from year three", "apply a few times each term"],
            "感受": ["practical", "hopeful", "less worried"],
        },
        sample=(
            "In a few years I want to finish my degree, do an internship, and then find a full-time job. "
            "I will check campus notices and ask teachers, so I can apply early. "
            "From year three I plan to check notices often and apply a few times each term. "
            "It feels practical and hopeful."
        ),
        sampleZh=(
            "几年后想先拿完学位，再实习，然后找全职工作。"
            "会看校园通知、问老师，好早点申请。"
            "从大三起打算常看通知，每学期投几次。"
            "觉得务实，也有盼头。"
        ),
    )