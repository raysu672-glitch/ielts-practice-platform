# -*- coding: utf-8 -*-
"""Paper and Rubbish and Recycling Freestyle packs."""


def register(_p):
  # --- Paper ---
    _p(
        "What did you use paper for most when you were at school?",
        "handwritten_notes_paper",
        logic="先答纸质笔记和作业为主，再举课堂笔记本与翻阅课本例子，说几乎每天用与顺手感受。",
        kitHint="手写笔记：学校用纸=记笔记写作业，不是垃圾分类题硬套。",
        words={
            "正面回答": ["Notes and homework", "Worksheets", "Real books"],
            "来源或举例": ["notebooks", "flip through textbooks", "exam papers"],
            "频次": ["almost every lesson", "every evening for homework"],
            "感受": ["helps me remember", "tangible", "still useful"],
        },
        sample=(
            "I used paper most for notes and homework at school. "
            "I kept notebooks for each subject and liked to flip through real textbooks after class. "
            "That was almost every lesson, and every evening for homework. "
            "Writing on paper helped me remember and still feels useful."
        ),
        sampleZh=(
            "上学时纸用得最多的是笔记和作业。"
            "每科有笔记本，课后我也爱翻纸质课本。"
            "几乎每节课都用，晚上写作业也用。"
            "手写帮我记得牢，现在也觉得有用。"
        ),
    )
    _p(
        "What did you use paper for most when you were at school?",
        "recycle_bins_floor",
        logic="先答练习卷、草稿纸用量大，再说明打草稿后分类处理习惯，强调学校日常频率。",
        kitHint="草稿+分类：学校用纸侧重试卷草稿，顺带提课后整理。",
        words={
            "正面回答": ["Drafts and tests", "Printouts", "Old worksheets"],
            "来源或举例": ["rough paper", "weekly quizzes", "sorted after class"],
            "频次": ["every week", "before exams more"],
            "感受": ["wasteful if messy", "better when recycled"],
        },
        sample=(
            "I used paper most for drafts and tests — weekly quizzes and rough workings took a lot of sheets. "
            "After class I stacked printouts and threw away the messy drafts once I copied the neat version. "
            "That happened every week, more before exams. "
            "It felt wasteful if I left piles lying around, so sorting helped."
        ),
        sampleZh=(
            "上学时纸最多的是草稿和测验——周测、演算很费纸。"
            "下课后我会把讲义摞好，乱七八糟的草稿誊完就清掉。"
            "每周都有，考前更多。"
            "堆着很浪费，分一下会好一些。"
        ),
    )
    _p(
        "What do you do with paper you no longer need?",
        "handwritten_notes_paper",
        logic="先答旧笔记保留有用的、其余回收，再描述期末整理步骤与频率。",
        kitHint="笔记整理：不再需要的纸=留精华、丢草稿。",
        words={
            "正面回答": ["Keep key notes", "Recycle the rest", "Clear old drafts"],
            "来源或举例": ["notebooks", "exam term folders", "soft recycle bin"],
            "频次": ["each term end", "before moving dorm"],
            "感受": ["less clutter", "responsible", "fresh start"],
        },
        sample=(
            "I keep useful notes and recycle paper I no longer need. "
            "At the end of each term I tear out loose drafts and put clean sheets in the recycle bin. "
            "I do that each term end, and again before moving dorm. "
            "It reduces clutter and feels like a responsible fresh start."
        ),
        sampleZh=(
            "有用的笔记留着，不要的纸拿去回收。"
            "每学期末我会撕掉零散草稿，干净些的投进可回收桶。"
            "每学期一次，换宿舍前也会整理。"
            "少占地方，也觉得是对的起的一次新开始。"
        ),
    )
    _p(
        "What do you do with paper you no longer need?",
        "recycle_bins_floor",
        logic="先答分类扔楼层回收桶，再写纸壳讲义与塑料包装袋分开动作，说每天习惯影响。",
        kitHint="楼层分类：处理废纸=投进楼层可回收，扣 recycle 题。",
        words={
            "正面回答": ["Sort and recycle", "Flatten boxes", "Use floor bins"],
            "来源或举例": ["cardboard", "plastic wrapping", "dorm recycling bins"],
            "频次": ["every few days", "when parcels arrive"],
            "感受": ["quick habit", "cleaner hallway", "feel better"],
        },
        sample=(
            "I sort paper I do not need and put it in the recycling bins on our dorm floor. "
            "I flatten delivery boxes, keep worksheets in the paper side, and plastic mailers separate. "
            "I do that every few days, especially when parcels arrive. "
            "It is a quick habit and keeps the hallway cleaner — I feel better doing it."
        ),
        sampleZh=(
            "不要的纸我会分类，投进宿舍楼层的回收桶。"
            "快递箱压扁，讲义进纸质那边，塑料包装另放。"
            "几天做一次，有快递时更多。"
            "习惯很快，走廊也更干净，心里踏实。"
        ),
    )
    _p(
        "What did you like to do with paper as a child?",
        "handwritten_notes_paper",
        logic="先答喜欢折便签、贴装饰或工整抄写，再举课外活动练字的例子，说课余频率。",
        kitHint="童年用纸喜好=折纸便签、练字，非环保题主角度。",
        words={
            "正面回答": ["Coloured notes", "Practice handwriting", "Stickers on books"],
            "原因或时间": ["primary school", "after class", "neat pens"],
            "频次": ["a few afternoons a week", "before homework"],
            "感受": ["fun", "proud of neat pages", "relaxing"],
        },
        sample=(
            "As a child I liked making neat notes on coloured paper and practising handwriting. "
            "Sometimes I stuck small stickers on book covers or folded corner bookmarks after class. "
            "I did that a few afternoons a week before homework. "
            "It was fun and I felt proud when the pages looked tidy."
        ),
        sampleZh=(
            "小时候喜欢在彩纸上做整齐的笔记、练字。"
            "有时课后在封面上贴小贴纸，或折个书角书签。"
            "一周好几个下午，写作业前玩一下。"
            "好玩，页面整齐时还挺有成就感。"
        ),
    )
    _p(
        "What did you like to do with paper as a child?",
        "recycle_bins_floor",
        logic="先答喜欢把废纸折成小飞机或收纳盒（用后仍回收），再写与同学玩耍场景，说童年频率与开心感受。",
        kitHint="童年折纸玩乐：喜欢「用纸做什么」=手工玩，用完可分类。",
        words={
            "正面回答": ["Simple crafts", "Paper planes", "Small boxes"],
            "原因或时间": ["break time", "with classmates", "cheap fun"],
            "频次": ["at lunch breaks", "rainy days indoors"],
            "感受": ["creative", "then recycle later", "good memories"],
        },
        sample=(
            "I liked simple paper crafts — folding planes or little boxes with classmates at lunch. "
            "It was cheap fun on rainy days when we stayed indoors. "
            "We did that pretty often in primary school breaks. "
            "It was fun, and teachers later told us to put the scraps in the recycle bin."
        ),
        sampleZh=(
            "喜欢用纸做简单手工——午休和同学折飞机、小盒子。"
            "雨天待在室内时特别常见，花钱少也好玩。"
            "小学课间挺经常这么玩。"
            "很好玩，后来老师会提醒我们把边角料放进回收箱。"
        ),
    )
    _p(
        "How often do you use paper in your daily life?",
        "handwritten_notes_paper",
        logic="先答仍较常用手写笔记，再写图书馆查书做摘录流程，说每周频率与安心感受。",
        kitHint="日常用纸频率=笔记摘录，偏学习用途。",
        words={
            "正面回答": ["Several times a week", "Not every hour", "For key tasks"],
            "原因": ["remember better", "exams", "library reading"],
            "时间线+行为描述": ["carry a notebook", "jot in the library", "rewrite summaries"],
            "影响": ["less phone distraction", "clearer review", "worth the weight"],
        },
        sample=(
            "I still use paper several times a week, though not every hour. "
            "Handwriting helps me remember for exams, so I carry a thin notebook. "
            "In the library I jot points from real books and rewrite summaries at night. "
            "It keeps my phone away and makes review clearer — worth the extra weight."
        ),
        sampleZh=(
            "一周还是会用好几次纸，当然不是每小时。"
            "手写备考记得牢，我会带薄笔记本。"
            "在图书馆翻实体书做摘录，晚上再整理摘要。"
            "手机少分心，复习更清楚，多带点重量也值得。"
        ),
    )
    _p(
        "How often do you use paper in your daily life?",
        "recycle_bins_floor",
        logic="先答包裹纸盒让用纸变频繁，再写拆包分类步骤，说频率与环保习惯影响。",
        kitHint="快递纸盒：日常用纸=网购包装+分类处理频率。",
        words={
            "正面回答": ["More than before", "Mainly packaging", "Still less than digital"],
            "原因": ["online shopping", "dorm deliveries", "floor recycling rules"],
            "时间线+行为描述": ["open parcel", "flatten cardboard", "carry to floor bin"],
            "影响": ["hallway stays tidy", "fewer mixed bags", "quick routine"],
        },
        sample=(
            "I use paper more than before, mainly packing paper and parcel boxes from online shopping. "
            "Dorm deliveries mean cardboard nearly every week. "
            "I open the parcel, flatten the box, and carry it to the floor recycle bin the same day. "
            "That quick routine keeps mixed rubbish down and the hallway tidy."
        ),
        sampleZh=(
            "用纸比以前多了，主要是网购的包装纸和纸盒。"
            "宿舍快递差不多每周都有。"
            "当天拆开、压扁，送到楼层回收桶。"
            "流程快，混杂垃圾少，走廊也干净。"
        ),
    )
    _p(
        "How do you think our use of paper will change in the future?",
        "handwritten_notes_paper",
        logic="先答总量会减少但笔记不会归零，再对比屏幕与纸质各自作用，说个人感受。",
        kitHint="观点：未来用纸=数字化减量化，手写仍留一席之地。",
        words={
            "正面回答": ["Less overall", "Not zero", "More digital forms"],
            "举例或原因": ["e-textbooks", "still like handwriting", "exam habits"],
            "作用或影响": ["save trees", "faster sharing online", "keep focus on paper"],
            "感受": ["mixed but practical", "hopeful", "still choose paper sometimes"],
        },
        sample=(
            "I think we will use less paper overall, but not zero. "
            "More classes may move to e-textbooks, yet many students still like handwriting for focus in exams. "
            "That should save trees while making sharing online faster. "
            "I feel mixed but practical — I will still choose paper sometimes."
        ),
        sampleZh=(
            "我觉得总量会变少，但不会完全没有。"
            "更多课可能用电子书，但考试前很多人还是靠手写集中注意力。"
            "能省树，也让线上分享更快。"
            "我有点矛盾但很现实——有时还是会选纸。"
        ),
    )
    _p(
        "How do you think our use of paper will change in the future?",
        "recycle_bins_floor",
        logic="先答未来更强调循环与分类，再举楼层桶推广例子，说社区影响与乐观感受。",
        kitHint="环保观点：未来=更严分类与循环用纸。",
        words={
            "正面回答": ["More recycling", "Less mixed waste", "Clearer rules"],
            "举例或原因": ["floor bins everywhere", "apps for pickup", "habits from school"],
            "作用或影响": ["cleaner blocks", "lower landfill", "easier for students"],
            "感受": ["hopeful", "needs everyone", "worth keeping"],
        },
        sample=(
            "I think we will recycle more paper in the future, instead of throwing mixed rubbish away. "
            "Floor bins and clearer labels already help students separate cardboard and worksheets. "
            "That should make the building cleaner over time. "
            "I feel hopeful, though it needs everyone — still worth keeping the habit."
        ),
        sampleZh=(
            "我觉得以后大家会回收更多纸，而不是混着扔。"
            "楼层分类桶和更清楚的标识已经帮同学把纸盒、讲义分开。"
            "时间长了楼会更干净。"
            "我觉得有希望，但要靠大家——这习惯值得坚持。"
        ),
    )
    _p(
        "Do you prefer reading on paper or on a screen?",
        "handwritten_notes_paper",
        logic="先表明更偏纸质深度阅读，再对比屏幕轻便与纸质翻页沉浸，收束个人感受。",
        kitHint="对比：纸质书翻阅 vs 屏幕，扣 paper 题。",
        words={
            "正面回答": ["Paper for deep reading", "Screen for quick stuff", "Depends on task"],
            "选项1的特点与作用": ["real pages", "flip back easily", "less eye strain at night"],
            "选项2的特点与作用": ["light tablet", "search keywords", "carry many files"],
            "个人感受": ["choose paper for exams", "screen for news", "comfort matters"],
        },
        sample=(
            "For deep reading I prefer paper, but screens win for quick news. "
            "Real pages let me flip back easily and stay focused when exams are close. "
            "A tablet is lighter and good for searching keywords on the bus. "
            "Personally I choose paper for serious study and a screen when I only need a fast scan."
        ),
        sampleZh=(
            "深度阅读我更喜欢纸，快讯就还是屏幕。"
            "纸质能随手翻回，考前也更专注。"
            "平板轻，公交车上搜关键词方便。"
            "Personally我会正经学习用纸，随便看看就用屏。"
        ),
    )
    _p(
        "Do you prefer reading on paper or on a screen?",
        "recycle_bins_floor",
        logic="先答日常更常用屏幕但愿为重要材料打印，再对比环保与方便，说个人取舍。",
        kitHint="对比：电子为主+可回收纸打印，体现 paper 使用态度。",
        words={
            "正面回答": ["Mostly screen", "Print when it matters", "Recycle after"],
            "选项1的特点与作用": ["phone and laptop", "always there", "less physical waste"],
            "选项2的特点与作用": ["print key pages", "mark with pen", "put in recycle bin"],
            "个人感受": ["balanced", "care about sorting", "flexible"],
        },
        sample=(
            "I mostly read on a screen, but I print key pages when I need to mark them. "
            "Phones and laptops are always there and cut down physical waste day to day. "
            "Printing lets me underline, then I put used sheets in the floor recycle bin. "
            "I feel balanced — digital first, paper when it really helps, and I care about sorting after."
        ),
        sampleZh=(
            "平时多用屏幕，但要批注时会打印重点页。"
            "手机电脑随身带，日常物理废纸也少。"
            "纸质的方便划线，用完投进楼层回收桶。"
            "我觉得挺平衡——先电子，真需要再纸，之后认真分类。"
        ),
    )

  # --- Rubbish and Recycling ---
    _p(
        "Do you recycle at home?",
        "recycle_bins_floor",
        logic="先肯定在宿舍/家里分类，再举楼层桶与纸塑分开例子，说每天习惯感受。",
        kitHint="楼层分类桶：在家/宿舍是否回收=肯定+具体动作。",
        words={
            "正面回答": ["Yes, I try", "At the dorm", "Paper and plastic"],
            "来源或举例": ["floor recycling bins", "labels on the wall", "separate bags"],
            "频次": ["almost every day", "when I take rubbish out"],
            "感受": ["normal now", "responsible", "quick"],
        },
        sample=(
            "Yes, I recycle at the dorm — we have labelled bins on each floor. "
            "I separate paper, bottles, and other rubbish before I take the bag downstairs. "
            "I do that almost every day when I go out. "
            "It feels normal now and pretty quick."
        ),
        sampleZh=(
            "会的，宿舍里每层都有贴好标签的桶。"
            "下楼前我会把纸、瓶子和其他垃圾分开。"
            "几乎每天出门时都会做。"
            "现在像日常习惯，也很快。"
        ),
    )
    _p(
        "Do you recycle at home?",
        "handwritten_notes_paper",
        logic="先答会回收讲义和草稿，再写期末整理进回收的步骤，说频率与整洁影响。",
        kitHint="笔记回收角：在家回收=旧笔记纸张进可回收。",
        words={
            "正面回答": ["Yes", "Mainly paper", "Old notes too"],
            "来源或举例": ["used worksheets", "notebooks", "campus recycle points"],
            "频次": ["each term", "when drawers get full"],
            "感受": ["lighter bag", "less guilt", "easier to study"],
        },
        sample=(
            "Yes, especially paper from study. "
            "When notebooks fill up I tear out useless drafts and bring the clean stack to the campus recycle point. "
            "That is each term, or when my drawer gets too full. "
            "My bag feels lighter and it is easier to study in a tidy space."
        ),
        sampleZh=(
            "会，尤其是学习用的纸。"
            "本子写满时我会撕掉无用草稿，把整齐的送去校园回收点。"
            "每学期一次，抽屉太满也会整理。"
            "包轻了，书桌清爽也更方便学。"
        ),
    )
    _p(
        "What kinds of things do you throw away most often?",
        "recycle_bins_floor",
        logic="先答外卖盒、塑料瓶、快递包装最多，再说明如何尽量分类，说每周频率。",
        kitHint="宿舍日常垃圾：最常扔=餐饮快递包装。",
        words={
            "正面回答": ["Takeaway boxes", "Plastic bottles", "Delivery packaging"],
            "来源或举例": ["canteen meals", "milk tea cups", "cardboard mailers"],
            "频次": ["several times a week", "after dinners"],
            "感受": ["wish there were less", "sorting helps"],
        },
        sample=(
            "I throw away takeaway boxes, plastic bottles, and delivery packaging most often. "
            "Canteen meals and milk tea cups pile up during busy weeks, plus cardboard from online orders. "
            "That is several times a week, especially after dinners. "
            "I wish there were less waste, but sorting at least helps."
        ),
        sampleZh=(
            "最常扔的是外卖盒、塑料瓶和快递包装。"
            "食堂、奶茶忙的时候堆得快，网购也会来纸盒。"
            "一周好几次，晚饭后尤其多。"
            "希望少点浪费，但至少分类有帮助。"
        ),
    )
    _p(
        "What kinds of things do you throw away most often?",
        "handwritten_notes_paper",
        logic="先答草稿纸、过期的打印材料最多，再写誊抄后清理习惯，说学期频率。",
        kitHint="学习废纸：最常扔=草稿与过期讲义。",
        words={
            "正面回答": ["Rough drafts", "Old printouts", "Broken pens"],
            "来源或举例": ["homework mistakes", "outdated slides", "exam week"],
            "频次": ["each month", "heavier each term end"],
            "感受": ["normal for students", "better when recycled"],
        },
        sample=(
            "Rough drafts and old printouts are what I throw away most as a student. "
            "Homework mistakes and outdated lecture slides stack up, especially near exams. "
            "I clear them each month, more heavily at term end. "
            "It feels normal, and better when the paper goes to recycle."
        ),
        sampleZh=(
            "当学生最常扔的是草稿和过期打印资料。"
            "作业涂改、过时的课件堆起来，考前更明显。"
            "每月清一次，学期末更彻底。"
            "挺正常，纸能回收更好。"
        ),
    )
    _p(
        "How do people in your area sort their rubbish?",
        "recycle_bins_floor",
        logic="先概述楼层分桶+四类标签，再写邻居普遍遵守程度，说常见频次与观感。",
        kitHint="社区分类：描述本区域=宿舍楼层桶+居民习惯。",
        words={
            "正面回答": ["Four bins", "Clear signs", "Most students follow"],
            "来源或举例": ["paper", "plastic", "food waste", "other"],
            "频次": ["daily", "when taking rubbish out"],
            "感受": ["improved recently", "still not perfect", "better than before"],
        },
        sample=(
            "Near campus people sort rubbish into about four types with clear signs — paper, plastic, kitchen waste, and other. "
            "Dorm buildings put matching bins on each floor, and most students follow the labels. "
            "You see that daily when people take bags downstairs. "
            "It improved recently, though habits are still not perfect."
        ),
        sampleZh=(
            "学校附近 roughly 分四类，标牌清楚——纸、塑料、厨余、其他。"
            "宿舍楼每层有对应桶，多数同学会看标签。"
            "每天有人拎垃圾下楼时都能看到。"
            "这两年好多了，但习惯还不算完美。"
        ),
    )
    _p(
        "How do people in your area sort their rubbish?",
        "handwritten_notes_paper",
        logic="先答纸类常单独丢回收点，再补充塑料等其他类别由物业统一，说观察频率。",
        kitHint="第二角度：区域分类强调学习纸类回收点。",
        words={
            "正面回答": ["Paper bins near library", "Mixed points too", "Volunteers sometimes"],
            "来源或举例": ["old notes", "cardboard", "green staff"],
            "频次": ["during term", "after big deliveries"],
            "感受": ["organized", "students cooperate", "could be stricter"],
        },
        sample=(
            "In my area students often take paper to separate bins near the library, while plastic goes to the floor points. "
            "After big deliveries you see piles of cardboard waiting for pickup. "
            "That happens during term, especially post-shopping weeks. "
            "It looks organized and students usually cooperate, though rules could be stricter."
        ),
        sampleZh=(
            "我们这片区同学常把纸送到图书馆旁的专用桶，塑料则去楼层点。"
            "大量快递后能看到一摞摞纸盒等着收。"
            "学期里都会这样，购物周更明显。"
            "整体挺有序，大家配合，但规则还能更严一点。"
        ),
    )
    _p(
        "How do you recycle things like paper and plastic?",
        "handwritten_notes_paper",
        logic="先答纸类先整理再送回收，塑料瓶冲洗后归类，说固定习惯与方便感受。",
        kitHint="纸塑回收步骤：先答怎么回收，再写具体动作。",
        words={
            "正面回答": ["Sort first", "Flatten paper", "Rinse bottles"],
            "原因或时间": ["campus rules", "before taking rubbish down", "exam clutter"],
            "频次": ["twice a week", "more when busy"],
            "感受": ["quick once you learn", "cleaner room"],
        },
        sample=(
            "I recycle paper and plastic by sorting them first. "
            "I flatten worksheets and cardboard, and rinse milk tea bottles before they go in the plastic side. "
            "I usually do that twice a week before I take rubbish downstairs. "
            "Once you learn the steps it is quick, and my room stays cleaner."
        ),
        sampleZh=(
            "纸和塑料我会先分好类再回收。"
            "讲义和纸盒压扁，奶茶瓶冲一下再进塑料那边。"
            "一般一周两次，下楼丢垃圾前做。"
            "熟了很快，房间也干净。"
        ),
    )
    _p(
        "How do you recycle things like paper and plastic?",
        "recycle_bins_floor",
        logic="先答利用楼层四色桶，再描述纸塑分袋动线，说每天下楼顺手做。",
        kitHint="楼层动线：回收=分袋→楼层桶。",
        words={
            "正面回答": ["Use floor bins", "Two small bags", "Same routine"],
            "原因或时间": ["signs remind me", "roommates do too", "since first year"],
            "频次": ["almost daily", "after meals"],
            "感受": ["team habit", "no smell if rinsed", "easy"],
        },
        sample=(
            "I recycle paper and plastic with two small bags and the colour-coded bins on our floor. "
            "Signs on the wall remind me, and roommates follow the same routine since first year. "
            "I drop them off almost daily after meals. "
            "If bottles are rinsed there is no smell — the team habit feels easy."
        ),
        sampleZh=(
            "纸和塑料我用两个小袋，投进楼层色标桶。"
            "墙上的说明会一直提醒，室友从大一起也这么干。"
            "饭后几乎每天顺路扔下去。"
            "瓶子冲干净就没味——全宿舍习惯挺轻松。"
        ),
    )
    _p(
        "What do you do when you see rubbish on the street?",
        "recycle_bins_floor",
        logic="先答不太脏会捡起投桶，再写上路→最近垃圾桶动线，说习惯影响。",
        kitHint="行为习惯：街上垃圾=捡起/入桶，硬规则第7条。",
        words={
            "正面回答": ["Pick it up if I can", "Use the nearest bin", "Not if it is too dirty"],
            "原因": ["messy streets annoy me", "set a small example", "near home"],
            "时间线+行为描述": ["notice bottle", "pick with tissue", "walk to recycle bin"],
            "影响": ["area looks nicer", "takes one minute", "feel responsible"],
        },
        sample=(
            "I usually pick up rubbish on the street if it is not too dirty. "
            "Messy pavements annoy me, especially near the dorm. "
            "If I see a bottle or paper, I grab it with a tissue and put it in the nearest bin on my way. "
            "It takes about a minute and the area looks nicer — I feel more responsible."
        ),
        sampleZh=(
            "不太脏的话我会把街上的垃圾捡起来。"
            "尤其是宿舍附近，路面乱我看着难受。"
            "看到瓶子或纸片，用纸垫着拿起，顺路扔进最近的桶。"
            "一分钟不到，环境好看点，自己也比较踏实。"
        ),
    )
    _p(
        "What do you do when you see rubbish on the street?",
        "handwritten_notes_paper",
        logic="先答会捡纸张类垃圾（熟动作），再写送去可回收桶，说对环境与心情影响。",
        kitHint="捡纸张：街上垃圾偏纸类捡起→回收桶。",
        words={
            "正面回答": ["Often pick paper", "Avoid sticky food waste", "Quick check around"],
            "原因": ["study waste floats around campus", "easy to carry", "paper recyclables"],
            "时间线+行为描述": ["spot handout", "fold it", "nearest recycle bin"],
            "影响": ["less litter near bus stop", "sets quiet example", "feels right"],
        },
        sample=(
            "When I see rubbish on the street I often pick up loose paper — flyers and handouts float around campus. "
            "I avoid sticky food waste, but flat paper is easy to carry. "
            "I fold it and drop it in the nearest recycle bin on my walk. "
            "The bus stop looks less messy, and it quietly feels like the right thing to do."
        ),
        sampleZh=(
            "街上看到垃圾我常捡纸张——校园周围传单、讲义随风跑。"
            "黏糊糊的厨余我不碰，平整的纸好拿。"
            "折一下，走路时扔进最近的可回收桶。"
            "公交站台没那么乱，心里也觉得该这么做。"
        ),
    )
    _p(
        "How have people's attitudes to rubbish changed in recent years?",
        "recycle_bins_floor",
        logic="先答更重视分类与环保宣传，再对比以前混扔，说社区变化与个人感受。",
        kitHint="对比态度变化：楼层桶与宣传推动观念更新。",
        words={
            "正面回答": ["More serious", "Less excuses", "Younger people lead"],
            "选项1的特点与作用": ["today: bins, signs, apps", "social posts", "fines in some cities"],
            "选项2的特点与作用": ["before: mix everything", "less talk", "fewer facilities"],
            "个人感受": ["clear improvement", "still lazy sometimes", "worth keeping"],
        },
        sample=(
            "People take rubbish more seriously now than a few years ago. "
            "Today we have floor bins, campus posters, and even apps reminding students to sort waste. "
            "In the past many rooms just mixed everything in one bag because facilities were poor. "
            "I see clear improvement, though some people are still lazy — the habit is worth keeping."
        ),
        sampleZh=(
            "这几年大家对垃圾明显更认真了。"
            "现在有楼层桶、校园海报，还有 App 提醒分类。"
            "以前设施少，不少人一袋混装就扔了。"
            "进步很清楚，也有人偷懒——但这习惯值得坚持。"
        ),
    )
    _p(
        "How have people's attitudes to rubbish changed in recent years?",
        "handwritten_notes_paper",
        logic="先答学生更愿回收学习用纸，再对比过去随意丢弃讲义，说变化原因与感受。",
        kitHint="学习场景态度：纸张回收意识提升。",
        words={
            "正面回答": ["More recycling mindset", "Less throwing notes away", "Teachers mention it"],
            "选项1的特点与作用": ["now: term-end paper drives", "library recycle boxes", "saving drafts digitally"],
            "选项2的特点与作用": ["before: bins full of worksheets", "less awareness", "no sorting"],
            "个人感受": ["healthier habit", "not perfect", "glad for the shift"],
        },
        sample=(
            "Attitudes changed a lot among students — more people think before they toss paper. "
            "Now we get term-end reminders to recycle notes, and there are boxes near the library. "
            "Years ago bins were stuffed with worksheets and nobody sorted. "
            "The shift is not perfect, but I am glad the recycling mindset is healthier."
        ),
        sampleZh=(
            "同学对垃圾的态度变了很多——扔纸前会先想一圈。"
            "现在有期末回收提醒，图书馆旁也有箱子。"
            "早年桶里塞满讲义，也没人说要分类。"
            "还不完美，但回收意识好不少，我挺高兴这变化。"
        ),
    )