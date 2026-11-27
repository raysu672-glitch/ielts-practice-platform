# -*- coding: utf-8 -*-
"""Outer space and stars Freestyle packs."""


def register(_p):
    _p(
        "What did you learn about space when you were a child?",
        "space_docs_night",
        logic="先答童年学过基础太空知识，再举夜里看航天纪录片例子，补观看频率与好奇感受。",
        kitHint="航天纪录片主线：童年太空学习来自科普片，非硬套实验课。",
        words={
            "正面回答": ["Basic ideas", "Planets and stars", "From TV at home"],
            "来源或举例": ["space documentaries", "rockets", "the solar system"],
            "频次": ["a few nights a week", "after homework", "with my parents sometimes"],
            "感受": ["exciting", "made space real", "still curious"],
        },
        sample=(
            "I learned basic ideas about planets, stars, and rockets, mostly from TV at home. "
            "My parents sometimes put on short space documentaries at night, and that made the topic feel real. "
            "I watched them a few nights a week after homework. "
            "I found it exciting and I am still curious about space."
        ),
        sampleZh=(
            "小时候学过行星、星星、火箭这些基础知识，多半在家看电视。"
            "父母有时晚上放短一点的航天纪录片，让太空变得具体。"
            "一周会看几个晚上，写完作业后。"
            "我觉得很有意思，到现在还对太空好奇。"
        ),
    )
    _p(
        "What did you learn about space when you were a child?",
        "school_science_lab",
        logic="先答学校科学课入门，再借课堂实验过渡到认识地球与太空，强调课上频率。",
        kitHint="学校科学课：太空童年学习=课堂概念+简单实验，纪录片仅弱提及。",
        words={
            "正面回答": ["In science class", "Simple facts", "Earth and moon"],
            "来源或举例": ["science lessons", "a model of planets", "basic experiments"],
            "频次": ["every week at school", "in junior-high years"],
            "感受": ["clearer than TV alone", "interesting", "sparked interest"],
        },
        sample=(
            "I learned about space mainly in school science lessons as a child. "
            "We used a simple model of planets and did easy experiments that linked to the Earth and the moon. "
            "That was every week in junior-high years. "
            "It was clearer than only watching TV, and it sparked my interest."
        ),
        sampleZh=(
            "小时候主要是在学校科学课里接触太空。"
            "用过简易行星模型，也做过和地球、月亮有关的小实验。"
            "初中那几年每周都有。"
            "比光看电视清楚，也激起兴趣。"
        ),
    )
    _p(
        "Have you ever learnt about outer space and stars?",
        "space_docs_night",
        logic="先肯定学过，再说明纪录片与短视频来源，补晚上学习频率与兴趣感受。",
        kitHint="夜里科普：已学过太空=纪录片+自学短片。",
        words={
            "正面回答": ["Yes, I have", "Quite a bit", "Mostly on my own"],
            "来源或举例": ["space documentaries", "videos about stars", "news about missions"],
            "频次": ["a few nights a week", "when I need a break"],
            "感受": ["fascinating", "relaxing", "keeps me interested"],
        },
        sample=(
            "Yes, I have learnt quite a bit about outer space and stars. "
            "I mainly watched short documentaries and clips about stars and space missions when I wanted a calm break. "
            "I do that a few nights a week after study. "
            "I find it interesting and quite relaxing."
        ),
        sampleZh=(
            "学过，了解还不少。"
            "主要是想放松时看关于星星和任务的短纪录片、短片。"
            "学习后一周有好几个晚上会看。"
            "我觉得很吸引人，也挺解压。"
        ),
    )
    _p(
        "Have you ever learnt about outer space and stars?",
        "school_science_lab",
        logic="先肯定学校有系统接触，再举科学课与测验例子，说课余是否会再查资料。",
        kitHint="科学课主线：学过太空=课堂+作业，可轻提课外搜索。",
        words={
            "正面回答": ["Yes, at school", "In exams too", "Still reading sometimes"],
            "来源或举例": ["science textbooks", "class quizzes", "teacher slides"],
            "频次": ["through secondary school", "before tests"],
            "感受": ["useful basics", "not expert", "want to learn more"],
        },
        sample=(
            "Yes — at school we covered outer space and stars in science class and even in exams. "
            "Textbooks and teacher slides gave me useful basics about orbits and constellations. "
            "That ran through secondary school, especially before tests. "
            "I am not an expert, but it made me want to learn more."
        ),
        sampleZh=(
            "学过——学校科学课讲过太空和星星，考试也考过。"
            "课本和老师幻灯片让我知道轨道、星座这些基础。"
            "整个中学阶段都有，考前尤其多。"
            "不算专家，但让我想继续了解。"
        ),
    )
    _p(
        "Do you like looking at the stars?",
        "space_docs_night",
        logic="先答喜欢，再解释夜里看天空或纪录片联想星星，补频率与平静感受。",
        kitHint="星空/纪录片：喜欢看星星=实地或片里都会兴奋。",
        words={
            "正面回答": ["Yes, I do", "When the sky is clear", "Especially at night"],
            "原因或时间": ["space videos", "quiet nights", "since childhood"],
            "频次": ["a few times a month", "holidays at home"],
            "感受": ["calming", "amazing", "makes me think big"],
        },
        sample=(
            "Yes, I do, especially when the sky is clear at night. "
            "Watching space programmes made me pay more attention to real stars when I go back home on holidays. "
            "I might look up a few times a month if the weather is good. "
            "It feels calming and a bit amazing — it makes me think big."
        ),
        sampleZh=(
            "喜欢，尤其夜里天晴的时候。"
            "看航天节目后，放假回家会更注意天上的星星。"
            "天气好一个月会看几次。"
            "很平静，也有点震撼，让人想得远一些。"
        ),
    )
    _p(
        "Do you like looking at the stars?",
        "school_science_lab",
        logic="先答喜欢但更偏理解原理，再连中学科学课认星座，说偶尔上楼顶看夜空。",
        kitHint="科学兴趣：喜欢星星=认星座+懂得一点科学，纪录片不当主角。",
        words={
            "正面回答": ["Yes", "With some knowledge", "Not every night"],
            "原因或时间": ["science class", "learned constellations", "curious mind"],
            "频次": ["sometimes on clear evenings", "after exams"],
            "感受": ["quieter", "interesting", "worth the cold"],
        },
        sample=(
            "Yes, I like looking at the stars, especially when I can name a few constellations from school. "
            "Science lessons gave me curiosity, so on clear evenings I sometimes go upstairs for a quick look. "
            "It is not every night — maybe a few times a month after busy weeks. "
            "It feels quiet and interesting, even if it is a bit cold."
        ),
        sampleZh=(
            "喜欢，尤其能叫出学校教过的几个星座时。"
            "科学课让我好奇，天晴的晚上有时上楼顶看一会儿。"
            "不是每天，忙完一周大概一个月几次。"
            "很安静也有意思，冷一点也值得。"
        ),
    )
    _p(
        "What would you most like to know about outer space?",
        "space_docs_night",
        logic="先点最想搞懂的问题（人能否长期住太空等），再举例纪录片里提过的方向，说持续关注意愿。",
        kitHint="纪录片启发：最想知道=看完片后仍好奇的点。",
        words={
            "正面回答": ["Life beyond Earth", "How Mars trips work", "Deep space"],
            "原因或时间": ["documentaries raised it", "recent missions", "since I was young"],
            "频次": ["whenever news appears", "a few times a year"],
            "感受": ["exciting", "hard to imagine", "worth following"],
        },
        sample=(
            "I would most like to know whether people can really live in space long term, not just visit. "
            "Documentaries about Mars missions and space stations made me think about food, gravity, and health. "
            "I follow that kind of news whenever it appears, maybe a few times a year. "
            "It feels exciting and hard to imagine, but worth following."
        ),
        sampleZh=(
            "我最想知道人能不能长期在太空生活，而不只是短暂访问。"
            "火星任务、空间站的片子让我想到食物、重力、健康这些问题。"
            "有新闻我就会看看，一年大概几次。"
            "又兴奋又难以想象，但值得继续关注。"
        ),
    )
    _p(
        "What would you most like to know about outer space?",
        "school_science_lab",
        logic="先答想知道黑洞或星系形成等科学问题，再连课堂引发的好奇，说仍会查资料。",
        kitHint="科学课好奇心：最想知道=课堂留下的硬核问题。",
        words={
            "正面回答": ["Black holes", "How galaxies form", "More physics"],
            "原因或时间": ["a tough science question", "teacher mentioned it", "still unsolved"],
            "频次": ["when I study", "occasionally online"],
            "感受": ["mind-blowing", "motivating", "bigger than homework"],
        },
        sample=(
            "I would most like to know how black holes really work — our teacher mentioned them once and I got stuck on the idea. "
            "Science class showed how much we still do not understand about galaxies and gravity. "
            "I sometimes search online when I study, though not every week. "
            "It feels mind-blowing and bigger than normal homework."
        ),
        sampleZh=(
            "我最想弄清黑洞到底是怎么回事——老师提过一句我就一直想。"
            "科学课让我看到星系、引力还有很多未解之谜。"
            "学习时偶尔会上网查，但不是每周都查。"
            "很震撼，比平常作业「大」很多。"
        ),
    )
    _p(
        "How often can you see stars where you live?",
        "space_docs_night",
        logic="先如实答城市里不常看清，再写放假回家或城郊能看到时要做何，说观星频率与可惜感受。",
        kitHint="观星频率：先答居住地光污染，再写何时真能看见星星。",
        words={
            "正面回答": ["Not often in the city", "Sometimes on trips", "Depends on weather"],
            "原因": ["light pollution", "tall buildings", "busy campus"],
            "时间线+行为描述": ["check weather app", "go to a darker spot", "look up briefly"],
            "影响": ["appreciate clear nights", "miss the view", "watch docs instead"],
        },
        sample=(
            "Honestly, not very often — light pollution near campus hides most stars. "
            "I care about a clear sky, so on holidays back home I walk to a darker street and look up for a minute. "
            "That might happen a few times a year when weather cooperates. "
            "I appreciate those nights, and otherwise I watch space docs instead."
        ),
        sampleZh=(
            "说实话不多——学校附近光污染重，星星大多看不见。"
            "我挺在意晴空，放假回家会走去暗一点的路口抬头看一分钟。"
            "天气配合的话一年大概几次。"
            "那种夜晚很珍惜，平时就看航天片代替。"
        ),
    )
    _p(
        "How often can you see stars where you live?",
        "school_science_lab",
        logic="先答城里少见、晴夜偶尔可见，再写会认几颗星才觉得值，说明频率与影响。",
        kitHint="科学视角：可见频率+是否会辨认星座。",
        words={
            "正面回答": ["Rarely", "Clear winter nights", "Almost never in summer haze"],
            "原因": ["city smog", "exam stress keeps me indoors", "late nights on campus"],
            "时间线+行为描述": ["finish study", "step outside", "spot Orion if lucky"],
            "影响": ["reminds me of science class", "small reward", "short break"],
        },
        sample=(
            "Rarely — in the city I might see a few bright stars on clear winter nights, almost never in summer haze. "
            "Late study keeps me indoors, but if I finish early I step outside and try to spot Orion. "
            "That lucky moment comes a few times a winter. "
            "It reminds me of science class and feels like a small reward."
        ),
        sampleZh=(
            "很少——城里只有冬天天晴时能看到几颗亮的，夏天雾霾几乎看不到。"
            "学习常弄到很晚，但提早结束我会出门试着找猎户座。"
            "冬天运气好才有几次。"
            "让我想起科学课，像一点小奖励。"
        ),
    )
    _p(
        "How do you think space travel will change in the future?",
        "space_docs_night",
        logic="先正面谈未来更商业、更频繁，再举纪录片里私人公司的例子，说个人期待感受。",
        kitHint="航天片观点：未来旅行=更多平民参与与成本下降。",
        words={
            "正面回答": ["More normal", "Cheaper maybe", "More countries involved"],
            "举例或原因": ["private rockets", "space tourism news", "reusable boosters"],
            "作用或影响": ["science faster", "jobs in tech", "inspire students"],
            "感受": ["hopeful", "a bit worried about cost", "exciting era"],
        },
        sample=(
            "I think space travel will become more normal, not only for a few astronauts. "
            "Documentaries about private rockets and tourism made me believe tickets could get cheaper one day. "
            "That could speed up science and create tech jobs that inspire students like me. "
            "I feel hopeful about the era, though costs still worry me a bit."
        ),
        sampleZh=(
            "我觉得太空旅行会越来越平常，不只有极少数宇航员。"
            "私人火箭、太空旅游的片子让我觉得票价也许有一天会降下来。"
            "这也可能加快科研、带来科技工作，激励像我这样的学生。"
            "我对这个时代挺乐观，不过成本仍有点担心。"
        ),
    )
    _p(
        "How do you think space travel will change in the future?",
        "school_science_lab",
        logic="先答未来更依赖国际合作与自动化，再从课堂科学素养谈影响，收束感受。",
        kitHint="科学课观点：未来旅行=技术+合作，不单靠娱乐片想象。",
        words={
            "正面回答": ["Safer trips", "More technology", "More teamwork"],
            "举例或原因": ["new materials from science class", "better machines", "countries work together"],
            "作用或影响": ["help medicine", "better weather satellites", "more science at school"],
            "感受": ["hopeful", "takes time", "worth studying"],
        },
        sample=(
            "I think space travel will get safer and use more technology than in the past. "
            "Science class showed how new materials and better machines could support longer trips and teamwork across countries. "
            "That may help medicine and weather satellites, and push schools to teach more science. "
            "I feel hopeful — it takes time, but it is worth studying for."
        ),
        sampleZh=(
            "我觉得太空旅行会更安全，也更靠新技术。"
            "科学课讲过新材料和更好的机器，能支持更长任务和跨国合作。"
            "这可能帮到医药和气象卫星，也推动学校多教科学。"
            "我觉得有希望——要时间，但值得学。"
        ),
    )