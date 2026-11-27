# -*- coding: utf-8 -*-
"""Politeness and Name Freestyle packs."""


def register(_p):
    # ---- Politeness ----
    _p(
        "How do people in your country show politeness?",
        "polite_thank_you",
        logic="先概括本国常见礼貌方式，再举说谢谢、扶门等例子，补日常频率与自然感受。",
        kitHint="素材=家人教的谢谢与小事；答社会习惯，不是只讲自己家规。",
        words={
            "正面回答": ["Say thank you", "Use polite words", "Small respectful acts"],
            "来源或举例": ["saying thank you", "holding the door", "queueing patiently"],
            "频次": ["every day in shops", "on campus", "on public transport"],
            "感受": ["respectful", "natural", "smoother interactions"],
        },
        sample=(
            "People in my country usually show politeness with small words and gestures. "
            "They say thank you in shops, hold the door for the next person and queue patiently on the bus. "
            "You notice that every day in public and on campus. "
            "I find these habits respectful and they make ordinary interactions smoother."
        ),
        sampleZh=(
            "我们国家的人常用小话语和小动作表示礼貌。"
            "在店里说谢谢、帮后面的人扶门、在公车上耐心排队都很常见。"
            "在公共场合和校园里每天都能见到。"
            "我觉得这些习惯很尊重人，也让日常相处更顺畅。"
        ),
    )
    _p(
        "How do people in your country show politeness?",
        "patient_teacher_help",
        logic="先答礼貌表现，再举老师学生互敬例子，补校园频率与尊重感受。",
        kitHint="老师耐心线：校园礼貌=问好、举手、课后道谢，不硬扯昵称。",
        words={
            "正面回答": ["Greet teachers", "Say please and thank you", "Wait your turn"],
            "来源或举例": ["raise a hand in class", "thank teachers after help", "queue at the canteen"],
            "频次": ["every school day", "in class", "after lessons"],
            "感受": ["respectful", "natural at school", "keeps class calm"],
        },
        sample=(
            "People show politeness by greeting teachers and saying please and thank you. "
            "In class students raise a hand, and after lessons they thank teachers who stayed to help. "
            "That happens every school day on campus. "
            "I find it respectful, and it keeps class life calmer."
        ),
        sampleZh=(
            "大家通过向老师问好、说请和谢谢来表现礼貌。"
            "上课举手，课后向留下来辅导的老师道谢。"
            "校园里每个上学日都这样。"
            "我觉得这是尊重，课堂也更安静。"
        ),
    )
    _p(
        "Who taught you to be polite when you were a child?",
        "polite_thank_you",
        logic="先答父母为主，再举说谢谢、商场纠错为例，补每天纠正与自然习惯感受。",
        kitHint="谁教你礼貌：父母是主线，老师可作补充。",
        words={
            "正面回答": ["My parents", "Mainly my mum and dad", "Family first"],
            "来源或举例": ["say thank you", "please in shops", "correct me in public"],
            "频次": ["every day", "whenever I forgot", "on the bus and in shops"],
            "感受": ["automatic now", "respectful", "grateful"],
        },
        sample=(
            "My parents taught me to be polite when I was a child at home and in public. "
            "They reminded me to say thank you and please in shops and on the bus. "
            "They corrected me almost every day whenever I forgot those small words. "
            "I find those manners automatic now and still feel respectful in ordinary life."
        ),
        sampleZh=(
            "小时候主要是父母在家和外面教我有礼貌。"
            "他们提醒我在店里和公车上说谢谢、请。"
            "我一忘他们就纠正，几乎每天都在练。"
            "现在这些礼节已成习惯，日常也仍觉得这是尊重别人。"
        ),
    )
    _p(
        "Who taught you to be polite when you were a child?",
        "patient_teacher_help",
        logic="先答老师也教礼貌，再举课后耐心纠正例子，补学校频率与习惯感受。",
        kitHint="耐心老师：谁教礼貌=老师强化请、谢谢与排队。",
        words={
            "正面回答": ["My teachers", "School and home", "A patient teacher helped"],
            "来源或举例": ["say please in class", "thank after questions", "wait before speaking"],
            "频次": ["every school day", "before exams more", "in the classroom"],
            "感受": ["natural habits", "grateful", "respectful"],
        },
        sample=(
            "My teachers also taught me to be polite when I was a child at school. "
            "One patient teacher reminded us to say please, thank you and wait before speaking. "
            "That was part of every school day, especially before exams when we asked for extra help. "
            "I am grateful — those school habits still feel natural."
        ),
        sampleZh=(
            "小时候老师在学校也教我有礼貌。"
            "有一位很有耐心的老师常提醒我们说请、谢谢，说话前先等一等。"
            "每个上学日都这样，考前多问问题时尤其明显。"
            "我很感激——这些校园习惯现在仍很自然。"
        ),
    )
    _p(
        "What kind of behaviour do you find rude?",
        "polite_thank_you",
        logic="先点出不礼貌行为，再对照自己重视的谢谢/排队等，补常见场景与不适感。",
        kitHint="从「说谢谢」价值观出发：打断、推搡、不讲谢谢都算无礼。",
        words={
            "正面回答": ["Not saying thank you", "Interrupting", "Pushing in lines"],
            "来源或举例": ["loud phone calls", "ignoring queue rules", "no please or thanks"],
            "频次": ["often in rush hour", "in the canteen", "on public transport"],
            "感受": ["bothers me", "disrespectful", "awkward"],
        },
        sample=(
            "I find not saying thank you and interrupting others quite rude in daily life. "
            "Pushing in lines or speaking loudly on the phone in quiet places also bothers me. "
            "You see that sometimes in rush hour on the bus or in the canteen. "
            "I feel those moments disrespectful and a bit awkward for everyone nearby."
        ),
        sampleZh=(
            "我觉得不打招呼道谢、打断别人说话挺没礼貌。"
            "插队或在安静地方大声打电话也让我反感。"
            "高峰期的公车或食堂里有时会碰到。"
            "我觉得那样不尊重人，周围的人也会尴尬。"
        ),
    )
    _p(
        "What kind of behaviour do you find rude?",
        "patient_teacher_help",
        logic="先答无礼行为，再举打断老师、不道谢，补课堂场景与不适感。",
        kitHint="老师线：无礼=打断讲解、无视老师问好。",
        words={
            "正面回答": ["Interrupting teachers", "Ignoring greetings", "Talking over others"],
            "来源或举例": ["cut off explanations", "no thank you after help", "loud chat in class"],
            "频次": ["sometimes in busy classes", "near exams", "in crowded halls"],
            "感受": ["disrespectful", "awkward", "unfair to patient teachers"],
        },
        sample=(
            "I find it rude when people interrupt teachers or talk over classmates. "
            "Ignoring a teacher's hello or forgetting thank you after extra help also bothers me. "
            "That sometimes happens in busy classes near exams. "
            "It feels disrespectful, especially to patient teachers."
        ),
        sampleZh=(
            "我觉得打断老师、盖过同学说话很没礼貌。"
            "对老师打招呼装作没听见，或者辅导后不道谢，也让我反感。"
            "考前忙的时候课堂里偶尔会有。"
            "特别对耐心的老师，这样很不尊重。"
        ),
    )
    _p(
        "Why is it important to be polite to strangers?",
        "polite_thank_you",
        logic="先给观点，再举陌生人场合说谢谢的作用，说明影响与个人感受。",
        kitHint="观点题：陌生人礼貌能减少摩擦，例子用商店、公车。",
        words={
            "正面回答": ["It builds trust", "It reduces conflict", "Basic respect matters"],
            "举例或原因": ["say thank you to staff", "queue on the bus", "first impressions"],
            "作用或影响": ["smoother service", "less awkward tension", "safer public space"],
            "感受": ["important", "natural duty", "calmer"],
        },
        sample=(
            "I think being polite to strangers matters because it shows basic respect and reduces small conflicts. "
            "Saying thank you to shop staff or waiting calmly in a queue sets a calm tone. "
            "That makes everyday service smoother and public spaces feel safer. "
            "I find it an important habit that keeps ordinary life calmer."
        ),
        sampleZh=(
            "我觉得对陌生人礼貌很重要，因为这是基本尊重，也能减少小摩擦。"
            "对店员说谢谢、耐心排队，能让气氛平和。"
            "日常服务更顺畅，公共场所也更安心。"
            "我觉得这是重要习惯，让生活更平静。"
        ),
    )
    _p(
        "Why is it important to be polite to strangers?",
        "patient_teacher_help",
        logic="先答重要性，再举对新老师或校外人员仍要礼貌，说作用与感受。",
        kitHint="老师线推到陌生人：第一次见面也要问好道谢。",
        words={
            "正面回答": ["First impressions matter", "Shows basic respect", "Reduces awkwardness"],
            "举例或原因": ["new teachers", "guest speakers", "staff you do not know"],
            "作用或影响": ["smoother talk", "better help later", "calmer public places"],
            "感受": ["important", "grown-up", "natural duty"],
        },
        sample=(
            "Being polite to strangers matters because first impressions form quickly. "
            "Even with a new teacher or guest speaker, a hello and thank you show basic respect. "
            "That makes later help smoother and public places calmer. "
            "I find it important and grown-up outside my close friends."
        ),
        sampleZh=(
            "对陌生人礼貌很重要，因为第一印象来得很快。"
            "即便对新老师或来访嘉宾，问好和道谢也是基本尊重。"
            "以后求助更顺，公共场合也更平静。"
            "出了熟人圈我觉得这很重要，也很成熟。"
        ),
    )
    _p(
        "On what occasions should we be polite?",
        "polite_thank_you",
        logic="先列举该礼貌的场合，再举购物、就餐、乘车例子，说作用与感受。",
        kitHint="全家教的场景：商店、食堂、公共交通、别人家做客。",
        words={
            "正面回答": ["In shops", "When eating out", "On public transport"],
            "举例或原因": ["thank staff", "hold the door", "wait in line"],
            "作用或影响": ["smooth service", "show respect", "avoid arguments"],
            "感受": ["natural", "expected", "comfortable"],
        },
        sample=(
            "We should be polite in shops, restaurants, public transport and other people's homes. "
            "Those are the places where saying thank you and waiting in line really matters. "
            "Small manners there keep service smooth and stop pointless arguments. "
            "I find that expected and comfortable in daily life."
        ),
        sampleZh=(
            "在商店、餐馆、公共交通和别人家里都应该有礼貌。"
            "这些地方说谢谢、排队特别重要。"
            "小事到位，服务更顺，也少了无谓争吵。"
            "我觉得这是日常里理所应当、也让人舒服的。"
        ),
    )
    _p(
        "On what occasions should we be polite?",
        "patient_teacher_help",
        logic="先答上课与见老师等场合，再举问好道谢，说作用与感受。",
        kitHint="老师线：课堂、答疑、食堂都是该礼貌的场合。",
        words={
            "正面回答": ["In class", "When asking for help", "In the canteen"],
            "举例或原因": ["greet teachers", "thank after questions", "wait your turn"],
            "作用或影响": ["respectful classroom", "easier to get help", "clear boundaries"],
            "感受": ["necessary", "still friendly", "comfortable"],
        },
        sample=(
            "We should be polite in class, when asking teachers for help, and in the canteen. "
            "Greeting teachers and thanking them after questions shows respect in those moments. "
            "That keeps the classroom calm and makes help easier next time. "
            "I find it necessary, and it can still feel friendly."
        ),
        sampleZh=(
            "上课、向老师提问、在食堂都要有礼貌。"
            "问好，以及答疑后说谢谢，这些场合特别重要。"
            "课堂更安静，下次求助也更容易。"
            "我觉得有必要，也可以很友善。"
        ),
    )
    _p(
        "How have people's manners changed compared with the past?",
        "polite_thank_you",
        logic="对比题先总评变化，再分线上急躁与线下仍重礼貌两面，补个人感受。",
        kitHint="对比类四步：过去更当面致谢 vs 现在手机快消息；感受平衡答。",
        words={
            "正面回答": ["Some things improved", "Some feel worse online", "It is mixed"],
            "选项1的特点与作用": ["past face-to-face thanks", "neighbours knew each other", "slower but warm"],
            "选项2的特点与作用": ["fast online chat", "less patience in queues", "still care in shops"],
            "个人感受": ["mixed", "hope we keep basics", "still value thank you"],
        },
        sample=(
            "I think manners are mixed compared with the past. "
            "In the past neighbours knew each other and thanked people face to face more often. "
            "Now online chat is faster, so some people sound impatient in queues or messages. "
            "Personally I still value saying thank you and hope we keep those basics."
        ),
        sampleZh=(
            "我觉得跟过去比，礼貌有好有坏。"
            "以前邻居更熟，当面道谢也更常见。"
            "现在线上交流快，有些人在排队或消息里显得急躁。"
            "我个人仍重视说谢谢，也希望这些基本礼节能保留。"
        ),
    )
    _p(
        "How have people's manners changed compared with the past?",
        "patient_teacher_help",
        logic="对比过去课堂更严与现在更互动但仍要礼貌，分述后谈感受。",
        kitHint="老师线对比：过去单向听讲 vs 现在可提问，礼貌底线仍在。",
        words={
            "正面回答": ["Classrooms feel more open", "Respect still matters", "Mixed change"],
            "选项1的特点与作用": ["past: quiet listening", "stricter distance", "less chat with teachers"],
            "选项2的特点与作用": ["now: more questions", "after-class help", "still say please and thanks"],
            "个人感受": ["more relaxed", "still need respect", "mostly fine"],
        },
        sample=(
            "Compared with the past, classrooms feel more open now. "
            "Before, students mostly listened quietly and kept more distance from teachers. "
            "Today we ask more questions and get after-class help, but please and thank you still matter. "
            "Personally I find the change mostly fine as long as respect stays."
        ),
        sampleZh=(
            "跟过去比，现在课堂更开放。"
            "以前学生多半安静听讲，跟老师距离也更远。"
            "现在提问更多、也有课后辅导，但请和谢谢仍重要。"
            "我觉得只要尊重还在，这种变化大体是好的。"
        ),
    )

    # ---- Name ----
    _p(
        "Who chose your name?",
        "name_parents_choice",
        logic="先答父母选择，再略提含义或好叫，补日常被称呼与亲近感受。",
        kitHint="谁取名=父母；可轻带含义，但本题不展开长篇寓意。",
        words={
            "正面回答": ["My parents", "They chose it", "When I was born"],
            "来源或举例": ["positive meaning", "easy for relatives", "family discussion"],
            "频次": ["every day when people call me", "since childhood"],
            "感受": ["natural", "connected to family", "used to it"],
        },
        sample=(
            "My parents chose my name when I was born. "
            "They picked it for a simple positive meaning and because relatives could say it easily. "
            "People have called me that every day since I was a child. "
            "I find their choice natural and I feel connected to my family."
        ),
        sampleZh=(
            "我的名字是父母在我出生时取的。"
            "他们看重寓意简单正面，也希望亲戚好叫。"
            "从小每天有人这样叫我。"
            "我觉得很自然，也和家里更有联系。"
        ),
    )
    _p(
        "Who chose your name?",
        "name_nickname_school",
        logic="先答父母取正式名，再说明同学后来起外号，补校园场景与两种称呼感受。",
        kitHint="正式名来自父母；昵称是同学起的，别颠倒主体。",
        words={
            "正面回答": ["My parents chose it", "Friends added a nickname", "Both matter"],
            "来源或举例": ["formal name at birth", "short nickname at school", "playground shout"],
            "频次": ["parents' name every day", "nickname after class"],
            "感受": ["warm", "two layers", "friendly"],
        },
        sample=(
            "My parents chose my formal name, though classmates later gave me a short nickname at school. "
            "The nickname was easier to shout across the playground after class. "
            "My family still use the formal name every day at home. "
            "I find both warm — one from parents and one from friends."
        ),
        sampleZh=(
            "正式名字是父母取的，同学后来在学校给我起了短外号。"
            "外号下课后在操场喊起来更方便。"
            "家里每天还是用父母取的名字。"
            "我觉得两种称呼都暖：一个来自家人，一个来自朋友。"
        ),
    )
    _p(
        "Does your name have a special meaning?",
        "name_parents_choice",
        logic="先答有无意涵，再说明父母选字寓意，补被介绍时的感受。",
        kitHint="含义题可对 parents 套装展开寓意。",
        words={
            "正面回答": ["Yes, it does", "A positive meaning", "Parents planned it"],
            "来源或举例": ["Chinese characters", "hope for health or study", "family wishes"],
            "频次": ["when I introduce myself", "at festivals with relatives"],
            "感受": ["positive", "appreciated", "part of identity"],
        },
        sample=(
            "Yes, it does. My parents chose characters with a positive meaning about study and health. "
            "They told me the story when I was old enough to understand family wishes. "
            "I mention it sometimes when relatives ask during festivals. "
            "I feel appreciated and it is part of how I see my identity."
        ),
        sampleZh=(
            "有的。父母选的字寓意学习和健康。"
            "我大一点能懂家里期盼时，他们跟我讲过。"
            "过年亲戚问起时我偶尔会提。"
            "我觉得被重视，这也是自我认同的一部分。"
        ),
    )
    _p(
        "Does your name have a special meaning?",
        "name_nickname_school",
        logic="先答正式名有含义，再对比昵称只是方便叫，补使用场景感受。",
        kitHint="含义挂在父母取的正式名；昵称通常无深层含义。",
        words={
            "正面回答": ["The formal name does", "The nickname does not", "Two different things"],
            "来源或举例": ["parents' meaning", "short form for friends", "easier pronunciation"],
            "频次": ["formal name at home", "nickname with classmates"],
            "感受": ["meaningful vs casual", "both fine", "friendly"],
        },
        sample=(
            "My formal name has a special meaning my parents chose, but my school nickname is just a short form. "
            "Friends use the nickname because it is quick to say in class chat. "
            "At home relatives still use the full name with its meaning. "
            "I find the formal name meaningful and the nickname friendly and casual."
        ),
        sampleZh=(
            "正式名字有父母选的寓意，学校外号只是简称。"
            "同学用外号是因为上课聊天说起来快。"
            "家里亲戚还是用有含义的全名。"
            "我觉得全名有意义，外号则亲切随意。"
        ),
    )
    _p(
        "How do you feel about your name?",
        "name_parents_choice",
        logic="先表态喜欢或习惯，再连到父母选择与含义，补日常感受。",
        kitHint="感受可连家庭选择与名字含义。",
        words={
            "正面回答": ["I like it", "Completely used to it", "Positive feeling"],
            "来源或举例": ["parents' choice", "easy to remember", "good meaning"],
            "频次": ["every day", "when I sign forms", "meeting new people"],
            "感受": ["comfortable", "connected", "natural"],
        },
        sample=(
            "I feel quite positive about my name. "
            "My parents chose it carefully and it is easy for teachers and friends to remember. "
            "I use it every day on forms and when I meet new people. "
            "I find it comfortable and natural, and it connects me to my family."
        ),
        sampleZh=(
            "我对自己的名字感觉挺好。"
            "父母认真取的，老师和同学也好记。"
            "填表、认识新人时每天都用。"
            "我觉得顺口自然，也和家里更有联结。"
        ),
    )
    _p(
        "How do you feel about your name?",
        "name_nickname_school",
        logic="先谈对正式名感受，再谈朋友外号的亲切，补不同场合频率。",
        kitHint="两套称呼：正式名认同 + 外号亲切。",
        words={
            "正面回答": ["Fine with both", "Formal name serious", "Nickname fun"],
            "来源或举例": ["parents' full name", "classmates' short form", "group chat"],
            "频次": ["formal at home", "nickname with friends"],
            "感受": ["flexible", "warm with friends", "respectful when needed"],
        },
        sample=(
            "I feel fine with both my formal name and my school nickname. "
            "The full name feels proper when I am with family or meet teachers. "
            "Friends still use the short nickname in group chats after class. "
            "I find that flexible — warm with friends but respectful when the situation needs it."
        ),
        sampleZh=(
            "正式名和外号我都能接受。"
            "和家人见面、见老师时全名更得体。"
            "朋友下课后在群里仍叫我短外号。"
            "我觉得挺灵活：朋友间亲切，需要时也尊重场合。"
        ),
    )
    _p(
        "What did your friends call you when you were a child?",
        "name_nickname_school",
        logic="先答童年朋友称呼，再举学校外号由来，补操场场景与温暖回忆。",
        kitHint="本题主轴=朋友叫你的外号，不是父母取名含义。",
        words={
            "正面回答": ["A short nickname", "Mostly my given name", "Playground name"],
            "来源或举例": ["classmates shortened it", "easier to shout", "nothing fancy"],
            "频次": ["every school day", "after class", "at breaks"],
            "感受": ["warm", "fun memories", "close friends"],
        },
        sample=(
            "My friends mostly called me a short nickname when I was a child at school. "
            "Classmates shortened my name because it was quicker to shout across the playground after class. "
            "They used it every school day at breaks, not something fancy. "
            "I find those memories warm and they remind me of close friends."
        ),
        sampleZh=(
            "小时候同学在学校多半叫我短外号。"
            "大家把名字缩短，下课后在操场喊起来更快。"
            "课间每天都会这样叫，也没什么花样。"
            "我觉得那些回忆很暖，也让我想起好朋友。"
        ),
    )
    _p(
        "What did your friends call you when you were a child?",
        "name_parents_choice",
        logic="先答朋友多叫全名或小名，再对比父母坚持正式名，补家庭与学校场景。",
        kitHint="父母套装：朋友叫法可能接近全名小名，不是大段寓意。",
        words={
            "正面回答": ["My given name", "A softer little name", "Not a joke name"],
            "来源或举例": ["close neighbours", "family friends", "simple pronunciation"],
            "频次": ["after school", "on holidays", "in the neighbourhood"],
            "感受": ["friendly", "respectful", "childhood memories"],
        },
        sample=(
            "When I was a child my friends usually called me my given name or a softer little name. "
            "Neighbours and family friends preferred the full name because my parents liked it clear. "
            "That was common after school in the neighbourhood and on holidays. "
            "I find those childhood memories friendly and respectful."
        ),
        sampleZh=(
            "小时候朋友通常叫我的大名或稍软一点的小名。"
            "街坊和爸妈的朋友更爱叫全名，因为我父母希望清晰好认。"
            "放学后小区里、放假时都很常见。"
            "我觉得那些童年记忆亲切又有礼貌感。"
        ),
    )
    _p(
        "Do you often forget people's names?",
        "name_parents_choice",
        logic="先承认会忘别人名字，再举新生/偶尔见面场景，补频率与尴尬及补救。",
        kitHint="忘记=别人的名字；绝不把「自己名字含义」当本题答案。",
        words={
            "正面回答": ["Sometimes", "Yes, after first meetings", "Especially new classmates"],
            "来源或举例": ["forget after one hello", "need to ask again", "apologise politely"],
            "频次": ["at term start", "after big events", "once a month maybe"],
            "感受": ["a bit embarrassed", "try to remember", "polite if I ask again"],
        },
        sample=(
            "Sometimes I forget people's names, especially right after a busy term starts. "
            "If I only meet someone once at an event, the name slips away though the face stays clear. "
            "That might happen once a month when many new faces appear. "
            "I feel a bit embarrassed, so I apologise and ask again politely."
        ),
        sampleZh=(
            "有时我会忘别人的名字，开学忙的时候尤其明显。"
            "活动上只见过一次的人，脸记得名字却跑了。"
            "人多的时候大概一个月会碰到几次。"
            "有点尴尬，所以会礼貌道歉再问一遍。"
        ),
    )
    _p(
        "Do you often forget people's names?",
        "name_nickname_school",
        logic="先答会混淆同学外号与真名，再举群聊多人场景，补频率与应对。",
        kitHint="忘的是别人的名/外号对应谁；不是讲自己名字好不好听。",
        words={
            "正面回答": ["Yes, sometimes", "Mix up nicknames", "After big class changes"],
            "来源或举例": ["too many nicknames", "group chats", "ask which name they prefer"],
            "频次": ["after class reshuffles", "in new clubs", "first weeks"],
            "感受": ["awkward but normal", "try nicknames carefully", "friendly correction"],
        },
        sample=(
            "Yes, sometimes I forget people's names when a class uses many nicknames. "
            "After a reshuffle I mix up who owns which short name in group chats. "
            "That happens most in the first weeks of a new term or club. "
            "I find it awkward but normal, and I politely ask which name they prefer."
        ),
        sampleZh=(
            "会的，班里外号多的时候我会搞混谁是谁。"
            "换班后群里短称呼一多，我就对不上人。"
            "新学期或刚加社团的头几周最常见。"
            "有点尴尬但也正常，我会礼貌问他们希望我怎么叫。"
        ),
    )
    _p(
        "How have popular names for babies changed in your country?",
        "name_parents_choice",
        logic="对比题先总评变化，再分过去传统字与现在时尚/独特名，补个人感受。",
        kitHint="从父母取名经验谈趋势：寓意字 vs 新潮组合。",
        words={
            "正面回答": ["More variety now", "Less repetitive", "Still care about meaning"],
            "选项1的特点与作用": ["traditional characters", "family generation names", "safe and familiar"],
            "选项2的特点与作用": ["unique combinations", "influenced by media", "still sound modern"],
            "个人感受": ["interesting trend", "parents think harder", "balance matters"],
        },
        sample=(
            "I think baby names in my country show more variety than in the past. "
            "Older generations often reused traditional characters or family patterns that felt safe. "
            "Now parents pick more unique combinations, sometimes influenced by books or shows, but many still want a good meaning. "
            "Personally I find the trend interesting as long as the name is easy to use every day."
        ),
        sampleZh=(
            "我觉得国内婴儿名字比过去更多样了。"
            "老一辈常用传统字或家族辈分，求稳求熟。"
            "现在父母更爱独特组合，有时会受书影音影响，但仍要寓意好。"
            "我个人觉得挺有意思，只要日常叫着顺口就好。"
        ),
    )
    _p(
        "How have popular names for babies changed in your country?",
        "name_nickname_school",
        logic="对比过去偏长或辈分名与现在更短好叫的名，分述后谈感受。",
        kitHint="婴儿名趋势第二套：更短、更好叫；外号只作日常简称轻提。",
        words={
            "正面回答": ["Shorter names now", "Easier to call", "Still need meaning"],
            "选项1的特点与作用": ["past: longer or generation names", "harder for kids to say"],
            "选项2的特点与作用": ["now: shorter given names", "easy short forms at school"],
            "个人感受": ["more practical", "still need respect", "fine for daily life"],
        },
        sample=(
            "Baby names feel shorter and easier to call than in the past. "
            "Older names were often longer or followed family patterns that kids found hard to say. "
            "Now many parents pick short given names, so school short forms come naturally. "
            "Personally I find it practical, as long as people still respect the formal name when needed."
        ),
        sampleZh=(
            "现在的婴儿名感觉更短、更好叫。"
            "以前名字偏长，或按辈分取，小孩也不好念。"
            "现在很多父母选短一点的大名，学校里简称也自然。"
            "我觉得实用，只要该用正式名时仍尊重就好。"
        ),
    )