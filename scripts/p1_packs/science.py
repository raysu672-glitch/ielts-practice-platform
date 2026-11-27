# -*- coding: utf-8 -*-
"""Science topic Freestyle packs."""


def register(_p):
    _p(
        "How does science affect your daily life?",
        "daily_tech_science",
        logic="先正面说会影响日常生活，再举手机地图/天气/地铁，补工作日频率与方便感受。",
        kitHint="本题切「出行与手机科技」：地图、天气、地铁系统，直接回答科学如何影响生活。",
        words={
            "正面回答": ["It affects me every day", "In small daily ways", "Through my phone and transport"],
            "来源或举例": ["phone maps", "weather apps", "subway systems", "online classes"],
            "频次": ["every weekday", "whenever I go out", "most mornings"],
            "感受": ["really convenient", "practical", "makes tasks faster"],
        },
        sample=(
            "It affects me every day through my phone and the subway. "
            "I use maps and weather apps before I go out, and trains also need modern systems. "
            "I notice this every weekday on campus. "
            "I find it really convenient in ordinary life."
        ),
        sampleZh=(
            "它每天都影响我，主要体现在手机和地铁上。"
            "出门前我会用地图和天气软件，火车也靠现代系统运行。"
            "上学的工作日我都能感觉到。"
            "我觉得这在日常生活里很方便。"
        ),
    )
    _p(
        "How does science affect your daily life?",
        "weather_search_tools",
        logic="先扣「影响生活」，再举查天气、搜索引擎、在线课等家里常用工具，补晚上/学习时频率与实用感受。",
        kitHint="本题切「家里常用小工具」：天气、搜索、在线课；和出行科技形成第二套答法，仍紧扣日常生活。",
        words={
            "正面回答": ["Yes, in small ways", "It helps at home and in study", "Through simple online tools"],
            "来源或举例": ["check the weather", "a search engine", "online classes", "look things up quickly"],
            "频次": ["most evenings", "when I do homework", "almost every day"],
            "感受": ["practical", "saves time", "really useful"],
        },
        sample=(
            "It affects my daily life in small but clear ways at home. "
            "I check the weather on my phone, use a search engine for homework, and take online classes when I need to. "
            "I do this most evenings after study. "
            "I find these simple tools practical and time-saving."
        ),
        sampleZh=(
            "它在家里也一点点影响着我的日常生活。"
            "我会查天气、用搜索引擎写作业，需要时也上网课。"
            "多数在学习后的晚上。"
            "我觉得这些小工具实用又省时间。"
        ),
    )
    _p(
        "When did you start to learn about science?",
        "school_science_lab",
        logic="先正面说小学/中学开始，再举科学课实验例子，补上课频率与好奇感受。",
        kitHint="本题切「学校实验课」：回答何时开始学科学，实验课是合法来源，不是硬套到生活影响题。",
        words={
            "正面回答": ["In primary school", "In secondary school", "Quite early"],
            "来源或举例": ["biology experiments", "science class", "simple school labs"],
            "频次": ["in science lessons every week", "when we had lab sessions"],
            "感受": ["keeps me curious", "feels practical", "interesting"],
        },
        sample=(
            "I started to learn about science in primary school. "
            "Later in secondary school we did simple biology experiments, which made the subject feel real. "
            "We had science lessons every week. "
            "I find those classes still keep me curious."
        ),
        sampleZh=(
            "我小学就开始学科学了。"
            "后来中学时我们做了简单的生物实验，让这门课变得具体。"
            "每周都有科学课。"
            "我觉得那些课现在仍让我保持好奇。"
        ),
    )
    _p(
        "When did you start to learn about science?",
        "space_docs_night",
        logic="先说学校入门时间，再补夜里看科普视频加深兴趣，说明晚上频率与轻松感受。",
        kitHint="本题切「课后科普视频」：开始学科学仍从学校说起，视频是第二套加深兴趣的细节。",
        words={
            "正面回答": ["In primary school", "From school, then videos", "Quite early"],
            "来源或举例": ["science class first", "space documentaries", "short science videos"],
            "频次": ["a few nights a week", "after homework"],
            "感受": ["interesting", "helps me chill out", "curious"],
        },
        sample=(
            "I started in primary school with simple science lessons. "
            "Later I also watched short space documentaries at night, which made me more curious. "
            "I do that a few nights a week after homework. "
            "I find it interesting and a soft break from study."
        ),
        sampleZh=(
            "我小学就在科学课里入门了。"
            "后来晚上也会看短一点的航天纪录片，让我更好奇。"
            "一周会看几个晚上，写完作业后。"
            "我觉得有意思，也是学习后的轻松休息。"
        ),
    )
    _p(
        "Which area of science interests you the most?",
        "school_science_lab",
        logic="先直接点出生物/实验，再说明课堂实验为何有趣，补上课场景与感受。",
        kitHint="本题切「生物实验」：回答最感兴趣的科学领域，课堂实验是正面例子。",
        words={
            "正面回答": ["Biology", "Hands-on experiments", "School lab science"],
            "来源或举例": ["biology experiments", "science class", "lab work"],
            "频次": ["in secondary-school lessons", "when we had labs"],
            "感受": ["keeps me curious", "clearer than pure theory"],
        },
        sample=(
            "Biology interests me the most. "
            "I liked simple experiments in science class because they made ideas easier to see. "
            "We did that in secondary-school lessons. "
            "I find hands-on science clearer than only reading theory."
        ),
        sampleZh=(
            "我对生物最感兴趣。"
            "我喜欢科学课里的简单实验，因为能把概念看得更清楚。"
            "中学课上常做。"
            "我觉得动手学科学比只读理论更清楚。"
        ),
    )
    _p(
        "Which area of science interests you the most?",
        "space_docs_night",
        logic="先点出太空/航天，再说明靠纪录片了解，补晚上观看频率与好奇感受。",
        kitHint="本题切「太空科普」：最感兴趣的领域是太空，用纪录片举例，不扯课堂实验。",
        words={
            "正面回答": ["Space science", "Astronomy", "Outer space"],
            "来源或举例": ["space documentaries", "videos about planets", "night-sky clips"],
            "频次": ["a few nights a week", "before I sleep"],
            "感受": ["exciting", "curious", "calming"],
        },
        sample=(
            "Space science interests me the most. "
            "I watch short documentaries about planets and stars when I want a calm break. "
            "I usually do this a few nights a week before sleep. "
            "I find it exciting and it keeps me curious."
        ),
        sampleZh=(
            "我对太空科学最感兴趣。"
            "想放松时会看行星、星星的短纪录片。"
            "一周大概几个晚上，睡前看。"
            "我觉得很有意思，也能保持好奇。"
        ),
    )
    _p(
        "Did you like science at school?",
        "school_science_lab",
        logic="先正面说喜欢，再举实验课例子，补上课频率与清晰/有趣感受。",
        kitHint="本题切「学校实验」：直接回答是否喜欢学校科学课。",
        words={
            "正面回答": ["Yes, I did", "Especially experiments", "I liked biology most"],
            "来源或举例": ["biology experiments", "science class", "lab sessions"],
            "频次": ["every week in secondary school", "when we had labs"],
            "感受": ["interesting", "keeps me curious", "clearer"],
        },
        sample=(
            "Yes, I did. I liked science at school, especially when we did simple biology experiments. "
            "Those classes happened every week in secondary school. "
            "I find experiments clearer and more interesting than only reading the book."
        ),
        sampleZh=(
            "喜欢。我喜欢学校的科学课，尤其是做简单生物实验的时候。"
            "中学每周都有。"
            "我觉得实验比只看书更清楚、更好玩。"
        ),
    )
    _p(
        "Did you like science at school?",
        "space_docs_night",
        logic="先说喜欢，再说明课堂之外还看科普视频，补晚上频率与好奇感受。",
        kitHint="本题切「课后科普」：喜欢学校科学，并用纪录片说明兴趣延续。",
        words={
            "正面回答": ["Yes, I did", "I liked it", "Science was interesting"],
            "来源或举例": ["science class", "space documentaries", "short science videos"],
            "频次": ["in school, then a few nights a week", "after homework"],
            "感受": ["curious", "interesting", "calming"],
        },
        sample=(
            "Yes, I liked science at school. "
            "After class I also watched short space documentaries, which kept me curious. "
            "I still watch them a few nights a week after homework. "
            "I find science interesting both in class and at home."
        ),
        sampleZh=(
            "喜欢。我喜欢学校的科学课。"
            "课后我还会看短一点的航天纪录片，保持好奇。"
            "现在一周还会看几个晚上。"
            "我觉得课堂和家里的科学都很有意思。"
        ),
    )
    _p(
        "What science programmes or videos do you enjoy?",
        "space_docs_night",
        logic="先点出航天/星空纪录片，再说明为何喜欢，补晚上观看频率与放松感受。",
        kitHint="本题切「航天纪录片」：直接回答喜欢的科学节目类型。",
        words={
            "正面回答": ["Space documentaries", "Short science videos", "Programmes about planets"],
            "来源或举例": ["space documentaries", "night-sky clips", "videos about stars"],
            "频次": ["a few nights a week", "before I sleep"],
            "感受": ["calming", "interesting", "helps me chill out"],
        },
        sample=(
            "I enjoy short space documentaries and videos about planets. "
            "They are easy to watch after study and still teach me something new. "
            "I usually watch them a few nights a week before sleep. "
            "I find them calming and interesting."
        ),
        sampleZh=(
            "我喜欢短一点的航天纪录片和行星视频。"
            "学习后也好看，还能学到一点新东西。"
            "一周大概几个晚上，睡前看。"
            "我觉得平静又有意思。"
        ),
    )
    _p(
        "What science programmes or videos do you enjoy?",
        "school_science_lab",
        logic="先说喜欢实验/生物类科普短片，再连到学校兴趣，补观看频率与清晰感受。",
        kitHint="本题切「实验类科普」：节目内容贴近课堂实验兴趣，仍回答「喜欢什么科学节目」。",
        words={
            "正面回答": ["Videos about experiments", "Biology clips", "Simple lab science videos"],
            "来源或举例": ["experiment videos", "biology clips", "school-style science shows"],
            "频次": ["at weekends", "when I revise science"],
            "感受": ["clear", "practical", "keeps me curious"],
        },
        sample=(
            "I enjoy short videos about experiments and biology. "
            "They remind me of science class and make ideas easier to understand. "
            "I watch them at weekends when I revise. "
            "I find them clear and practical."
        ),
        sampleZh=(
            "我喜欢实验和生物类的短视频。"
            "会让我想起科学课，也更容易懂。"
            "周末复习时会看。"
            "我觉得清楚又实用。"
        ),
    )
    _p(
        "What scientific discovery would you like to see in the future?",
        "space_docs_night",
        logic="先点出希望的太空/探索类发现，再说明为何关心，补平时关注方式与期待感受。",
        kitHint="本题切「太空探索」：未来想看到的科学发现与航天兴趣一致。",
        words={
            "正面回答": ["Safer space travel", "New planet discoveries", "Clearer space research"],
            "来源或举例": ["space documentaries", "news about planets", "research videos"],
            "频次": ["when I watch science videos", "a few times a month"],
            "感受": ["exciting", "hopeful", "curious"],
        },
        sample=(
            "I would like to see safer space travel and clearer discoveries about other planets. "
            "I already watch space documentaries, so this future feels exciting to me. "
            "I follow this kind of news a few times a month. "
            "I find it hopeful and curious."
        ),
        sampleZh=(
            "我希望看到更安全的太空旅行，以及对其他星球更清楚的发现。"
            "我本来就看航天纪录片，所以对这种未来很期待。"
            "一个月会关注几次相关新闻。"
            "我觉得充满希望，也很好奇。"
        ),
    )
    _p(
        "What scientific discovery would you like to see in the future?",
        "school_science_lab",
        logic="先点出医学/生物类发现，再连到学校兴趣，补关注频率与实用期待。",
        kitHint="本题切「生物/医学」：未来发现与课堂生物兴趣相关，仍直接回答题干。",
        words={
            "正面回答": ["Better medical discoveries", "Useful biology research", "Health science progress"],
            "来源或举例": ["biology lessons", "health science videos", "simple lab ideas"],
            "频次": ["when I read science news", "from time to time"],
            "感受": ["useful", "hopeful", "practical"],
        },
        sample=(
            "I would like to see better medical discoveries from biology research. "
            "Since I liked biology experiments at school, health science feels meaningful to me. "
            "I read this kind of news from time to time. "
            "I find that future useful and hopeful."
        ),
        sampleZh=(
            "我希望看到更多来自生物研究的医学发现。"
            "我以前喜欢学校生物实验，所以健康科学对我很有意义。"
            "我会偶尔看这类新闻。"
            "我觉得那种未来实用又有希望。"
        ),
    )
    _p(
        "What scientific discovery would you like to see in the future?",
        "daily_tech_science",
        logic="先点出清洁能源/日常科技类发现，再说明对生活的影响，补关注频率与方便期待。",
        kitHint="本题切「日常科技」：未来发现要能改善出行/手机生活，紧扣日常生活。",
        words={
            "正面回答": ["Cleaner energy tech", "Smarter daily tools", "Better transport systems"],
            "来源或举例": ["phone tools", "subway systems", "everyday technology"],
            "频次": ["in daily news", "when I use my phone"],
            "感受": ["convenient", "practical", "useful"],
        },
        sample=(
            "I would like to see cleaner energy and smarter daily tools for transport and phones. "
            "Science already affects my weekday maps and subway trips, so better tech would help a lot. "
            "I notice this topic in daily news. "
            "I find that kind of discovery practical and useful."
        ),
        sampleZh=(
            "我希望看到更清洁的能源，以及更聪明的出行和手机工具。"
            "科学已经影响我工作日的地图和地铁，更好的科技会很有帮助。"
            "日常新闻里常能看到这类话题。"
            "我觉得这种发现实用又有用。"
        ),
    )
