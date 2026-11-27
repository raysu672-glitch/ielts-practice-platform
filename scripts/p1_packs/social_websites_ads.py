# -*- coding: utf-8 -*-
"""Social media, Advertisements, and Websites Freestyle packs."""


def register(_p):
    # ---------- Social media ----------
    _p(
        "Which social media apps do you use most?",
        "phone_xiaohongshu_wechat",
        logic="先直接点名最常用 App，再分微信与小红书用途，补每天频率与实用感受。",
        kitHint="WeChat=通知聊天，小红书=浏览；本题答「用哪些」，不是广告或网站总览。",
        words={
            "正面回答": ["WeChat and Xiaohongshu", "Mainly those two", "WeChat for groups"],
            "来源或举例": ["class WeChat groups", "Xiaohongshu tips", "family chats"],
            "频次": ["every day after class", "most evenings", "on the subway"],
            "感受": ["practical", "stay in touch", "need limits at night"],
        },
        sample=(
            "I use WeChat and Xiaohongshu the most in daily campus life. "
            "WeChat is for chatting, class group notices and family messages, while Xiaohongshu is for short tips and videos. "
            "I open both almost every day after class and sometimes on the subway. "
            "I find them practical for staying in touch, though I try not to scroll too late."
        ),
        sampleZh=(
            "日常我最常用微信和小红书。"
            "微信聊天、看班级群通知和家里消息，小红书看短 tips 和视频。"
            "几乎每天下课后都会开，地铁上有时也会。"
            "我觉得很实用，不过也尽量别刷太晚。"
        ),
    )
    _p(
        "Which social media apps do you use most?",
        "douyin_scroll_habit",
        logic="先答抖音为主，再说明晚上浏览习惯，补频率与心情/上瘾平衡感受。",
        kitHint="抖音套装：本题只谈社交媒体 App，不展开广告主题。",
        words={
            "正面回答": ["Douyin", "Short-video apps", "Mainly Douyin"],
            "来源或举例": ["browse videos", "funny clips", "quick breaks"],
            "频次": ["every evening", "before sleep", "when bored"],
            "感受": ["relaxes me", "can be obsessive", "set a limit"],
        },
        sample=(
            "I use Douyin the most among social media apps on my phone. "
            "I browse short videos when I want a quick break after study or feel bored. "
            "That is almost every evening before sleep if I am honest. "
            "It relaxes me, but I know I can get obsessed, so I try to set a limit."
        ),
        sampleZh=(
            "手机里社交媒体我最常用抖音。"
            "学习后想歇口气或无聊时会刷短视频。"
            "说实话几乎每天睡前都会。"
            "能放松，但我也知道容易上瘾，所以会给自己设个限度。"
        ),
    )
    _p(
        "Which social media apps do you use most?",
        "comedy_hang_out",
        logic="先答微信等联络 App 为主，再说明也常通过群聊分享喜剧内容，补周末与轻松感受。",
        kitHint="喜剧素材轻挂：用最常用的聊天 App + 分享好笑内容，不是只说看电影。",
        words={
            "正面回答": ["WeChat for groups", "Also video apps", "Stay connected"],
            "来源或举例": ["share funny clips", "plan weekends", "dorm group chat"],
            "频次": ["every day", "Fridays", "at weekends"],
            "感受": ["social", "light mood", "keeps friendships"],
        },
        sample=(
            "I use WeChat the most because our class and dorm groups live there. "
            "Friends also share funny comedy clips and weekend plans in those chats. "
            "I check the groups every day, especially on Fridays. "
            "I find it social and it keeps friendships light and easy."
        ),
        sampleZh=(
            "我最常用微信，因为班级群和宿舍群都在上面。"
            "朋友也会在群里转发好笑片段、约周末。"
            "每天都会看，周五尤其多。"
            "我觉得很有社交感，也让朋友相处更轻松。"
        ),
    )
    _p(
        "How much time do you spend on social media each day?",
        "phone_xiaohongshu_wechat",
        logic="先给大致时长，再分微信与小红书各用多久，补场景与是否过多感受。",
        kitHint="估时即可：上课后微信多，碎片时间小红书。",
        words={
            "正面回答": ["About one hour", "Maybe ninety minutes", "Less on busy days"],
            "来源或举例": ["WeChat replies", "Xiaohongshu browsing", "class notices"],
            "频次": ["after each class block", "before sleep", "weekends more"],
            "感受": ["acceptable", "could be less", "useful for news"],
        },
        sample=(
            "I spend about an hour on social media on a normal study day, sometimes a bit more at weekends. "
            "Roughly half goes to WeChat for replies and notices, and the rest to Xiaohongshu browsing. "
            "Most of that happens after class blocks and before sleep. "
            "I find it acceptable for campus life, though I could cut the late-night part."
        ),
        sampleZh=(
            "平时学习日大概一小时社交媒体，周末有时更长。"
            "大约一半回微信、看通知，一半刷小红书。"
            "主要在课后和睡前。"
            "校园生活还算能接受，不过睡前那部分还能再减。"
        ),
    )
    _p(
        "How much time do you spend on social media each day?",
        "douyin_scroll_habit",
        logic="先承认抖音占时较长，再描述晚上连着刷的行为，补频率与自控感受。",
        kitHint="抖音套装可诚实答偏多，但要提到节制。",
        words={
            "正面回答": ["More than I plan", "Around an hour", "Too much sometimes"],
            "来源或举例": ["Douyin scroll", "lose track of time", "quick clips"],
            "频次": ["every evening", "before sleep", "on the subway"],
            "感受": ["relaxing but long", "need discipline", "happy short term"],
        },
        sample=(
            "On social media I probably spend around an hour a day, and Douyin takes most of it. "
            "I open one short clip after study and suddenly thirty minutes pass before sleep. "
            "That pattern is almost every evening, sometimes on the subway too. "
            "It feels relaxing short term, but I know I need more discipline."
        ),
        sampleZh=(
            "社交媒体我每天大概一小时，抖音占大头。"
            "学习后点开一条，睡前不知不觉半小时就没了。"
            "几乎每晚如此，地铁上有时也会。"
            "当下挺放松，但我也知道得更自律。"
        ),
    )
    _p(
        "How much time do you spend on social media each day?",
        "comedy_hang_out",
        logic="先答总时长不长，再说明多花在微信群聊与转喜剧，补碎片时间与社交感受。",
        kitHint="聊天+转好笑内容占时，不是长时间看剧。",
        words={
            "正面回答": ["Under an hour", "Short checks", "More on weekends"],
            "来源或举例": ["WeChat chats", "funny links", "weekend plans"],
            "频次": ["between classes", "evenings", "Fridays"],
            "感受": ["social not addictive", "light use", "enjoyable"],
        },
        sample=(
            "I spend under an hour on social media most weekdays, a bit more when friends chat a lot at weekends. "
            "I am not watching full films there — it is quick WeChat replies and shared comedy links. "
            "I check messages between classes and in the evening after dinner. "
            "I find that light social use enjoyable without feeling addictive."
        ),
        sampleZh=(
            "工作日社交媒体大概不到一小时，周末朋友聊得多会稍长。"
            "不是在上看整部电影，而是快回微信、转发好笑链接。"
            "课间和晚饭后会看。"
            "这种轻度社交我觉得开心，也不容易上瘾。"
        ),
    )
    _p(
        "What do you usually post online?",
        "phone_xiaohongshu_wechat",
        logic="先答发什么类型内容，再描述朋友圈/小红书发帖场景，补原因与影响。",
        kitHint="行为习惯四步：原因=为何发；时间线=课后拍照发笔记或动态。",
        words={
            "正面回答": ["Photos sometimes", "Rare long posts", "Study or life snaps"],
            "原因": ["share small moments", "classmates ask", "record a trip"],
            "时间线+行为描述": ["after a walk", "upload to Xiaohongshu", "brief WeChat moments"],
            "影响": ["friends comment", "light connection", "not much pressure"],
        },
        sample=(
            "I do not post a lot, usually just photos after a walk or a simple campus moment. "
            "I share them because classmates sometimes ask where a café or view is, and a short post is enough. "
            "After dinner I might upload one picture to Xiaohongshu and skip WeChat moments if I am busy. "
            "It keeps a light connection without much pressure to perform online."
        ),
        sampleZh=(
            "我不怎么发，多半是散步或校园小瞬间的照片。"
            "同学会问某地在哪，发一张就够。"
            "晚饭后可能上传一张到小红书，忙就不发朋友圈。"
            "保持轻松联系，也没什么表现压力。"
        ),
    )
    _p(
        "What do you usually post online?",
        "douyin_scroll_habit",
        logic="先答很少自己发，以看为主，再说明偶尔转发或点赞，补原因与影响。",
        kitHint="抖音套装：多数时间是消费者，发帖少也合法。",
        words={
            "正面回答": ["Mostly watch", "Rare posts", "Forward sometimes"],
            "原因": ["shy on camera", "prefer browsing", "quick share"],
            "时间线+行为描述": ["like clips", "send one to roommate", "no long editing"],
            "影响": ["dorm laughs", "stay quiet feed", "saves time"],
        },
        sample=(
            "I usually watch rather than post — I am a bit shy on camera. "
            "If a clip fits my roommate's mood I forward it instead of filming myself. "
            "Most evenings I just like videos and occasionally send one link in our dorm chat. "
            "That saves time and still creates a quick laugh without building a public feed."
        ),
        sampleZh=(
            "我多半是看，很少自己发，镜头前有点害羞。"
            "看到适合室友的会转发，不自己拍。"
            "晚上大多点赞，偶尔在宿舍群发一条链接。"
            "省时间，也能快速笑一下，不用经营公开主页。"
        ),
    )
    _p(
        "What do you usually post online?",
        "comedy_hang_out",
        logic="先答偶尔发聚会/喜剧截图或文字，再说明与朋友互动的原因与时间线，补气氛影响。",
        kitHint="发的是好笑截图或活动合照，不是严肃长文。",
        words={
            "正面回答": ["Weekend photos", "Funny screenshots", "Not daily"],
            "原因": ["share a good laugh", "remember hangouts", "invite friends"],
            "时间线+行为描述": ["after KTV or films", "post one group photo", "caption a joke"],
            "影响": ["friends reply", "plan next outing", "lighter mood"],
        },
        sample=(
            "I sometimes post a group photo or a funny screenshot after we hang out at weekends. "
            "It is usually to share a good laugh and remind friends who missed the outing. "
            "After KTV or a light comedy night I upload one picture with a short joke caption. "
            "Friends reply quickly and it keeps our weekend plans easy and light."
        ),
        sampleZh=(
            "周末聚会后偶尔会发合照或好笑截图。"
            "多半是为了分享欢乐、提醒没来的朋友。"
            "唱完 KTV 或看完轻喜剧，发一张图配短笑话。"
            "大家很快回复，下次约会也容易接着约。"
        ),
    )
    _p(
        "What do people often do on social media?",
        "phone_xiaohongshu_wechat",
        logic="先概括常见行为，再举聊天、刷短视频、看推荐，补学生日常与双面感受。",
        kitHint="描述「人们」行为，可带微信群与小红书浏览。",
        words={
            "正面回答": ["Chat and browse", "Share posts", "Shop sometimes"],
            "原因": ["stay connected", "kill time", "follow trends"],
            "时间线+行为描述": ["reply in groups", "scroll feeds", "compare products"],
            "影响": ["useful notices", "easy to overuse", "keeps friendships"],
        },
        sample=(
            "People often chat, browse short posts and share links on social media. "
            "Students use group chats for class notices while others scroll recommendation feeds to kill time. "
            "You see that every day after lessons and again late at night. "
            "It keeps friendships alive but also makes it easy to overuse phones."
        ),
        sampleZh=(
            "大家常在社交媒体上聊天、浏览短内容和转发链接。"
            "学生用群看通知，也有人刷推荐打发时间。"
            "每天下课后、深夜都很常见。"
            "能维系关系，但也容易过度用手机。"
        ),
    )
    _p(
        "What do people often do on social media?",
        "douyin_scroll_habit",
        logic="先答刷短视频最常见，再描述连刷与评论行为，补晚间场景与上瘾影响。",
        kitHint="抖音角度：刷、赞、评论、转发。",
        words={
            "正面回答": ["Watch short videos", "Like and comment", "Share clips"],
            "原因": ["quick entertainment", "algorithm keeps feeding", "stress relief"],
            "时间线+行为描述": ["open Douyin after class", "scroll in bed", "send links"],
            "影响": ["relieves stress", "sleep later", "viral trends spread"],
        },
        sample=(
            "People often watch short videos, like them and pass funny clips to friends. "
            "The algorithm keeps feeding new clips, so many students open Douyin right after class. "
            "Scrolling in bed before sleep is common, and links spread fast in dorm chats. "
            "It relieves stress short term but can push sleep later."
        ),
        sampleZh=(
            "大家常刷短视频、点赞，还把好笑片段转给朋友。"
            "算法一直推新片，很多学生下课就开抖音。"
            "睡前躺床上刷也常见，宿舍里链接传得很快。"
            "短期减压，但也容易睡得晚。"
        ),
    )
    _p(
        "What do people often do on social media?",
        "comedy_hang_out",
        logic="先答聊天和分享好笑内容最常见，再补周末聚会约饭行为链与放松影响。",
        kitHint="人们=聊天+转喜剧+约聚会，不只是观众。",
        words={
            "正面回答": ["Chat and laugh", "Plan meet-ups", "Share memes"],
            "原因": ["relieve stress", "stay close", "cheap fun"],
            "时间线+行为描述": ["Friday group chat", "pick a film", "post photos later"],
            "影响": ["stronger bonds", "less lonely", "can distract from study"],
        },
        sample=(
            "People often chat, share memes and plan simple meet-ups on social media. "
            "On Fridays our group picks a light comedy or café visit without leaving the chat app. "
            "Afterwards someone posts photos so everyone feels included. "
            "It strengthens bonds and relieves stress, though it can distract from study if chat never stops."
        ),
        sampleZh=(
            "大家常在社交媒体上聊天、发表情、约见面。"
            "周五群聊里就能定看哪部轻喜剧或去哪家咖啡馆。"
            "结束后有人发照片，没去的也觉得参与。"
            "增进感情、减压，但若聊个不停也会影响学习。"
        ),
    )
    _p(
        "How do you think social media will change in the future?",
        "phone_xiaohongshu_wechat",
        logic="先给观点，再举例 AI 推荐与购物结合，说作用与感受。",
        kitHint="观点题：可谈推荐更准、与微信生态整合，别空喊科技。",
        words={
            "正面回答": ["More personal", "Shorter content", "Closer to daily life"],
            "举例或原因": ["phone feeds", "in-app shopping", "class notices online"],
            "作用或影响": ["faster info", "less privacy", "harder to switch off"],
            "感受": ["convenient but worrying", "need balance", "still useful"],
        },
        sample=(
            "I think social media will become more personal and even harder to switch off. "
            "Apps like WeChat and Xiaohongshu may mix shopping and campus notices in one feed. "
            "That can bring faster information, but also more ads in private life. "
            "I find it convenient yet worrying unless I keep clear limits."
        ),
        sampleZh=(
            "我觉得社交媒体会更个人化，也更难放下手机。"
            "微信、小红书一类可能把购物和校园通知揉在一个信息流里。"
            "信息更快，但私生活里广告也会更多。"
            "我觉得方便，也担心，除非自己界限划清楚。"
        ),
    )
    _p(
        "How do you think social media will change in the future?",
        "douyin_scroll_habit",
        logic="先答短视频更短更快，再举例算法与直播购物，说影响与感受。",
        kitHint="从抖音习惯推未来：更短、更碎、更商业。",
        words={
            "正面回答": ["Even shorter clips", "Stronger algorithms", "More ads in feed"],
            "举例或原因": ["seconds-long videos", "live shopping", "endless scroll"],
            "作用或影响": ["quick fun", "addictive design", "young creators rise"],
            "感受": ["exciting", "need self-control", "cannot ignore trends"],
        },
        sample=(
            "I think short-video social media will get even shorter and more addictive. "
            "Algorithms may push seconds-long clips with live shopping links in the same scroll. "
            "Young creators could rise fast, but ordinary users may lose more time without noticing. "
            "I find that exciting for content but scary for self-control."
        ),
        sampleZh=(
            "我觉得短视频社交媒体会更短、更容易上瘾。"
            "算法可能在同一屏里推几秒片子加热卖链接。"
            "年轻创作者会冒头，普通用户也可能不知不觉耗掉更多时间。"
            "内容有趣，但自控方面让我担心。"
        ),
    )
    _p(
        "How do you think social media will change in the future?",
        "comedy_hang_out",
        logic="先答社交更偏轻松社区，再举小群看喜剧、线上线下活动，说影响与感受。",
        kitHint="未来=小群搞笑社区+线下聚会，不是只有大屏直播。",
        words={
            "正面回答": ["Smaller friend circles", "More event planning", "Light content wins"],
            "举例或原因": ["group chats for comedy", "campus activities", "less toxic debates"],
            "作用或影响": ["closer friends", "less public pressure", "offline meet-ups return"],
            "感受": ["hopeful", "more human", "still need moderation"],
        },
        sample=(
            "I hope social media will shift toward smaller friend circles and lighter content rather than endless arguments. "
            "People may use group chats more to plan comedy nights or campus activities, then meet offline. "
            "That could reduce public pressure while keeping humour shared. "
            "I find that future hopeful as long as we still moderate time online."
        ),
        sampleZh=(
            "我希望社交媒体更多小圈子、轻内容，少些无尽争论。"
            "大家或用群聊约喜剧夜、校园活动，再到线下见面。"
            "公开压力小一些，但好笑的东西还能分享。"
            "我觉得这种未来挺值得期待，只要仍控制上网时间。"
        ),
    )
    _p(
        "Do you think you spend too much time on social media?",
        "phone_xiaohongshu_wechat",
        logic="先有时承认偏多，再举睡前沿小红书微信，说影响与打算。",
        kitHint="诚实答 sleep 前刷太久；观点四步用作用或影响=耽误睡眠。",
        words={
            "正面回答": ["Sometimes yes", "Late night yes", "Weekdays less"],
            "举例或原因": ["Xiaohongshu before bed", "reply too many chats", "lose track"],
            "作用或影响": ["sleep later", "tired next day", "still get notices"],
            "感受": ["aware", "trying to cut", "useful but excessive"],
        },
        sample=(
            "Sometimes yes, especially when I scroll Xiaohongshu or reply WeChat chats too late. "
            "Useful group notices are fine, but recommendation feeds easily steal another twenty minutes before sleep. "
            "That makes me tired the next study day even though I stayed informed. "
            "I am aware of it and trying to cut the last half hour at night."
        ),
        sampleZh=(
            "有时是的，尤其睡前刷小红书或回太多微信。"
            "群通知有用，但推荐流很容易再吃掉二十分钟。"
            "第二天上课会困，尽管消息没落下。"
            "我有意识地在减睡前那半小时。"
        ),
    )
    _p(
        "Do you think you spend too much time on social media?",
        "douyin_scroll_habit",
        logic="先承认抖音时间常超标，再举睡前连刷，说对学习睡眠影响与感受。",
        kitHint="本题可明确说 Douyin 时间过长。",
        words={
            "正面回答": ["Yes, often", "More than planned", "Hard to stop"],
            "举例或原因": ["one clip becomes many", "algorithm", "after exams relax"],
            "作用或影响": ["less sleep", "harder to focus", "short mood boost"],
            "感受": ["guilty sometimes", "need timer", "still enjoy clips"],
        },
        sample=(
            "Yes, I often think I spend too much time, and Douyin is the main reason. "
            "One clip after study becomes twenty, and the algorithm never feels finished before sleep. "
            "I still enjoy the mood boost, but next-day focus suffers when I sleep late. "
            "I feel guilty sometimes and use a timer to force myself to stop."
        ),
        sampleZh=(
            "嗯，我常常觉得太久，主要是抖音。"
            "学习后点开一条能变成二十条，睡前算法像关不完。"
            "当下心情好些，但熬夜第二天难集中。"
            "有时会有点内疚，我会用计时器逼自己停。"
        ),
    )
    _p(
        "Do you think you spend too much time on social media?",
        "comedy_hang_out",
        logic="先答总体不算太多，再说明多为短聊天非长刷，说对学习与心情影响。",
        kitHint="喜剧/聚会素材：社交时间短、互动型，对比沉迷刷视频。",
        words={
            "正面回答": ["Not really", "Short sessions", "More talking than scrolling"],
            "举例或原因": ["plan weekends", "share jokes", "not endless feeds"],
            "作用或影响": ["relieves stress", "little study harm", "can distract if chat long"],
            "感受": ["balanced", "socially good", "watch late night less"],
        },
        sample=(
            "Not really — my social media time is more short chats than endless scrolling. "
            "I spend minutes planning a comedy night or sharing jokes, not hours on a single feed. "
            "That relieves stress without hurting study much, unless a group chat never ends. "
            "I find my use fairly balanced compared with people who binge short videos."
        ),
        sampleZh=(
            "不算吧——我更多是短聊天，不是无尽刷屏。"
            "花几分钟约喜剧夜、转笑话，不会盯一条 feed 几小时。"
            "能减压，对学习伤害不大，除非群聊聊不停。"
            "跟狂刷短视频的人比，我觉得自己的使用还算平衡。"
        ),
    )

    # ---------- Advertisements ----------
    _p(
        "Where do you see adverts most often?",
        "phone_xiaohongshu_wechat",
        logic="先答最常见广告位，再举小红书/短视频信息流广告，补刷手机频率与烦/有用感受。",
        kitHint="微信/小红书=看见广告的地方，不是回答「我最爱微信」。",
        words={
            "正面回答": ["In app feeds", "Before videos", "Sponsored posts"],
            "来源或举例": ["Xiaohongshu sponsored notes", "short video ad cards", "WeChat mini-program banners"],
            "频次": ["every day on my phone", "while browsing", "before a clip plays"],
            "感受": ["hard to ignore", "sometimes useful", "can feel noisy"],
        },
        sample=(
            "I see adverts most often inside app feeds when I browse on my phone. "
            "On Xiaohongshu sponsored notes pop up between real posts, and short-video apps show ad cards before a clip plays. "
            "That happens almost every day while I scroll after class. "
            "Some offers look useful, but the sheer number feels noisy when I only wanted to relax."
        ),
        sampleZh=(
            "我最常在手机信息流里看到广告。"
            "小红书赞助笔记夹在真帖子中间，短视频 app 播放前还有广告卡片。"
            "几乎每天课后刷手机都会遇到。"
            "有的挺有用，但只想放松时会觉得吵。"
        ),
    )
    _p(
        "Where do you see adverts most often?",
        "subway_screen_ads",
        logic="先答地铁/站台屏幕，再描述通勤盯着屏幕，补工作日频率与烦人/印象深感受。",
        kitHint="地铁广告屏套装：通勤场景，不是手机 app 主旨。",
        words={
            "正面回答": ["On subway screens", "In the station", "During my commute"],
            "来源或举例": ["carriage digital boards", "catchy slogans", "product posters"],
            "频次": ["every weekday", "twice a day", "rush hour"],
            "感受": ["hard to ignore", "sometimes catchy", "crowded and loud"],
        },
        sample=(
            "I see adverts most often on subway screens during my commute. "
            "Digital boards in the carriage play the same catchy slogans while passengers stare at their phones. "
            "I notice them every weekday, twice a day in rush hour. "
            "A clever line can stick, but repeated clips feel tiring when the train is crowded."
        ),
        sampleZh=(
            "我最常在通勤时的地铁屏幕上看广告。"
            "车厢电子屏反复播口号，乘客也会抬头扫一眼。"
            "每个工作日早晚高峰都会看到。"
            "好记的 slogan 会留下印象，但人多时重复播放挺烦。"
        ),
    )
    _p(
        "Have you ever bought something because of an advert?",
        "phone_xiaohongshu_wechat",
        logic="先承认偶尔被种草，再举小红书/直播优惠信息，补频率与实用/后悔感受。",
        kitHint="购买因广告——信息流推荐促成下单，不是夸 app 好用。",
        words={
            "正面回答": ["Yes, once or twice", "Small items only", "Not expensive things"],
            "来源或举例": ["sponsored skincare post", "coupon in feed", "snack ad before video"],
            "频次": ["a few times a year", "after exams", "when a discount appears"],
            "感受": ["convenient", "sometimes wasteful", "check reviews first"],
        },
        sample=(
            "Yes, a few times I bought small things because a feed advert pushed a discount I already wanted. "
            "Once a sponsored skincare note on Xiaohongshu matched my budget and I ordered after reading comments. "
            "That only happens a few times a year, usually when an exam ends and I browse more. "
            "It feels convenient, though I still check reviews so I do not waste money."
        ),
        sampleZh=(
            "有过几次，信息流广告推了折扣，刚好是我本来想买的小东西。"
            "有一次小红书赞助护肤笔记价位合适，看完评论就下单了。"
            "一年也就几次，多在考完试刷得多的时候。"
            "挺方便，但我还是先查评价，怕乱花钱。"
        ),
    )
    _p(
        "Have you ever bought something because of an advert?",
        "subway_screen_ads",
        logic="先答很少因地铁广告下单，再举被 slogan 记住后线上搜索，补工作日看见与影响。",
        kitHint="地铁广告影响=记住品牌后手机搜，不是当场在车厢买。",
        words={
            "正面回答": ["Rarely directly", "Remembered a brand", "Then searched online"],
            "来源或举例": ["subway snack slogan", "phone ad later", "compare prices"],
            "频次": ["noticed weekly on commute", "bought once after months", "searched on phone"],
            "感受": ["subtle influence", "not main reason", "still cautious"],
        },
        sample=(
            "I rarely buy something the second I see a subway screen advert, but one snack slogan stuck for weeks. "
            "After seeing it every weekday I searched the brand on my phone and tried it once online. "
            "That purchase only happened once, though the board repeated the clip for months. "
            "I find subway ads subtle influencers, not the main reason I shop."
        ),
        sampleZh=(
            "我很少在地铁上看到广告就立刻买，但有款零食口号念了好久。"
            "每个工作日都看见后，我在手机上搜品牌，网购尝过一次。"
            "真正下单就那一次，屏幕却播了好几个月。"
            "我觉得地铁广告是潜移默化的影响，不是购物主因。"
        ),
    )
    _p(
        "Which advert do you remember from your childhood?",
        "phone_xiaohongshu_wechat",
        logic="先答童年电视/手机屏幕广告，再举零食或饮料短片，补晚上看见与难忘旋律感受。",
        kitHint="童年记忆的广告内容，不是现在爱刷微信。",
        words={
            "正面回答": ["A snack advert", "A TV jingle", "Played before cartoons"],
            "来源或举例": ["short candy clip", "singing slogan", "family TV time"],
            "频次": ["after dinner", "most weekends", "before cartoons"],
            "感受": ["catchy", "strangely memorable", "innocent fun"],
        },
        sample=(
            "I remember a candy advert with a silly song that played before weekend cartoons on TV. "
            "The whole family watched it after dinner, and I sang the slogan without thinking. "
            "It appeared most weekends when I was a child. "
            "The tune still feels catchy, even though the product has changed."
        ),
        sampleZh=(
            "我记得小时候周末动画片前播的糖果广告，配了很傻的歌。"
            "全家晚饭后一起看，我会下意识跟着唱口号。"
            "小时候多数周末都会出现。"
            "旋律至今还洗脑，虽然产品都换代了。"
        ),
    )
    _p(
        "Which advert do you remember from your childhood?",
        "subway_screen_ads",
        logic="先答童年地铁或公交车身/站牌广告，再举某一饮料口号，补出行频率与画面感。",
        kitHint="地铁/户外屏童年版：跟父母坐车记住的大屏广告。",
        words={
            "正面回答": ["A drink poster", "Station screen", "Bus body advert"],
            "来源或举例": ["bright colours", "repeated slogan", "held mum's hand"],
            "频次": ["holiday trips", "once a month", "city visits"],
            "感受": ["vivid", "loud colours", "travel memory"],
        },
        sample=(
            "I remember a bright drink advert on a city subway screen when my parents took me downtown as a child. "
            "The slogan repeated while the train moved, and the colours looked huge to me. "
            "I only saw it on holiday trips, maybe once a month. "
            "I find that memory vivid because it mixed travel excitement with a loud advert."
        ),
        sampleZh=(
            "我记得小时候爸妈带我去市区，地铁屏上有一款很亮的饮料广告。"
            "车一开口号就重复播，颜色对我当时来说特别大。"
            "只有放假进城大概一个月一次。"
            "旅行兴奋和大屏广告叠在一起，印象特别深。"
        ),
    )
    _p(
        "What kind of adverts do you enjoy watching?",
        "phone_xiaohongshu_wechat",
        logic="先答喜欢哪类广告，再举搞笑短片或故事型信息流广告，补观看频率与轻松感受。",
        kitHint="享受看的=广告类型（短、有趣、有剧情），不是说「我爱用微信」。",
        words={
            "正面回答": ["Short funny ones", "Light story ads", "Not hard-sell"],
            "原因或时间": ["after study", "need a smile", "skip loud sales"],
            "频次": ["sometimes in feeds", "before videos", "when bored"],
            "感受": ["enjoyable", "quick", "skip if too long"],
        },
        sample=(
            "I enjoy short, funny adverts more than long hard-sell ones in my phone feeds. "
            "A fifteen-second story ad with a light joke is fine when it appears before a Xiaohongshu video. "
            "I might watch those a few times a week if I am browsing anyway. "
            "I find them enjoyable and quick, and I skip anything that shouts too much."
        ),
        sampleZh=(
            "我喜欢短、好笑的广告，不爱长篇硬推销。"
            "小红书视频前若十五秒小故事有点幽默，我能接受。"
            "本来就要刷的话，一周可能看几次。"
            "轻松又快，喊太凶的我直接划走。"
        ),
    )
    _p(
        "What kind of adverts do you enjoy watching?",
        "subway_screen_ads",
        logic="先答偏创意地铁短片广告，再说明通勤无聊时愿意看，补频率与厌烦对比感受。",
        kitHint="地铁屏上创意/幽默广告 vs 枯燥重复。",
        words={
            "正面回答": ["Creative subway clips", "Short humour", "Clear design"],
            "原因或时间": ["commute boredom", "need something to watch", "not reading homework"],
            "频次": ["weekday mornings", "same line daily", "if clip changes"],
            "感受": ["better than silence", "tired if repeated", "enjoy fresh ones"],
        },
        sample=(
            "I enjoy creative subway screen adverts when the clip actually changes, not the same loop for months. "
            "A short humorous story on the carriage board is fine while I stand during the commute. "
            "I see them on weekday mornings on the same line. "
            "Fresh ideas feel better than silence, but repeated copies make me stop looking."
        ),
        sampleZh=(
            "地铁屏要是换创意短片，我会愿意看，同一条循环好几个月就免了。"
            "通勤站着时，车厢屏上短幽默故事还行。"
            "工作日早上同一条线都会遇到。"
            "有新意比干站着好，重复我就别看。"
        ),
    )
    _p(
        "How have adverts changed over the past few years?",
        "phone_xiaohongshu_wechat",
        logic="对比题：过去电视长广告 vs 现在手机精准短视频广告，谈个人感受。",
        kitHint="对比类：手机信息流 vs 过去电视；微信只是投放渠道之一。",
        words={
            "正面回答": ["More digital", "Shorter and targeted", "Mixed change"],
            "选项1的特点与作用": ["longer TV ads", "whole family watched", "single screen"],
            "选项2的特点与作用": ["personalised feed ads", "before clips", "track shopping"],
            "个人感受": ["convenient", "more invasive", "harder to escape"],
        },
        sample=(
            "I think adverts changed from long TV clips the whole family watched to short targeted ones in phone feeds. "
            "Old adverts used one loud message on a single screen, while now Xiaohongshu and video apps push different offers to each person. "
            "That makes small purchases convenient but also feels more invasive when ads follow me online. "
            "Personally I find the new style harder to escape even if each clip is shorter."
        ),
        sampleZh=(
            "我觉得广告从全家人一起看的长电视片，变成手机里短而精准的推荐。"
            "过去一个大屏喊一句，现在小红书、短视频会给每个人不同优惠。"
            "小东西好买，但也更像被跟踪，网上躲不开。"
            "我个人觉得虽然更短，却更难躲开。"
        ),
    )
    _p(
        "How have adverts changed over the past few years?",
        "subway_screen_ads",
        logic="对比户外地铁大屏过去海报到现在动态互动屏，谈通勤感受。",
        kitHint="地铁广告：静态海报→动态屏，更亮更频。",
        words={
            "正面回答": ["More digital screens", "Less paper", "Louder commutes"],
            "选项1的特点与作用": ["paper posters", "simple photos", "easier to ignore"],
            "选项2的特点与作用": ["moving LED boards", "louder audio", "same loop issue"],
            "个人感受": ["more distracting", "sometimes clearer", "miss quiet commutes"],
        },
        sample=(
            "Compared with a few years ago, subway adverts moved from simple paper posters to bright moving screens. "
            "Old posters were easy to ignore, while LED boards now play sound and video in rush hour. "
            "The message is sometimes clearer, but the same clip loops for weeks. "
            "Personally I miss quieter commutes even if digital boards look modern."
        ),
        sampleZh=(
            "跟几年前比，地铁广告从纸质海报变成亮眼的动态屏。"
            "以前海报好忽略，现在高峰 LED 屏还带声画。"
            "信息有时更清楚，但同一条能播几周。"
            "我个人怀念安静一点的通勤，尽管新屏看着现代。"
        ),
    )

    # ---------- Websites ----------
    _p(
        "Which websites do you visit most often?",
        "study_websites_search",
        logic="先点名学习/搜索类网站，再举查作业、考研资料场景，补工作日频率与方便感受。",
        kitHint="查资料套装：必须写出具体网站用途（搜索、课程），不是社交媒体 app。",
        words={
            "正面回答": ["Search engines", "Study sites", "Online course pages"],
            "来源或举例": ["Baidu for quick search", "university library portal", "MOOC lessons"],
            "频次": ["every weekday", "before assignments", "before exams"],
            "感受": ["really convenient", "saves time", "reliable links matter"],
        },
        sample=(
            "I visit search engines and a few study websites most often for coursework. "
            "I use Baidu or the library portal to find articles, and sometimes open MOOC pages for extra examples. "
            "That happens almost every weekday before I start an assignment. "
            "I find those websites really convenient and they save me time if links are reliable."
        ),
        sampleZh=(
            "我最常打开的是搜索引擎和几个学习网站。"
            "用百度或图书馆门户找文献，有时也看网课例子。"
            "几乎每个工作日写作业前都会上。"
            "网站靠谱的话很省时间，也很方便。"
        ),
    )
    _p(
        "Which websites do you visit most often?",
        "phone_xiaohongshu_wechat",
        logic="先答常逛的网页端/小程序对应站点，再举小红书网页、购物页，补频率与休闲感受。",
        kitHint="社交套装答「网站」：小红书/电商网页版或微信内 H5，不是只说 app 聊天。",
        words={
            "正面回答": ["Xiaohongshu web", "Shopping sites", "WeChat article links"],
            "来源或举例": ["open notes on laptop", "compare prices online", "class article shares"],
            "频次": ["evenings", "when shopping", "after shared links"],
            "感受": ["easy browsing", "can distract", "useful tips"],
        },
        sample=(
            "I often visit Xiaohongshu on a laptop browser and a few shopping websites when I compare prices. "
            "Teachers sometimes share WeChat article links that open as simple web pages with campus news. "
            "I open those in the evening or right after someone sends a shopping link. "
            "I find the browsing easy and full of tips, though it can distract me from study."
        ),
        sampleZh=(
            "我常在电脑浏览器上逛小红书，也比价几家购物网站。"
            "老师还会发微信文章链接，点开是校园资讯网页。"
            "多在晚上或收到购物链接时打开。"
            "浏览方便、信息多，但也容易耽误学习。"
        ),
    )
    _p(
        "What makes a website easy to use?",
        "phone_xiaohongshu_wechat",
        logic="先答清晰导航与手机适配，再举社交/种草站加载快的例子，补使用场景感受。",
        kitHint="社交站角度：加载快、少弹窗、搜索清楚。",
        words={
            "正面回答": ["Clear layout", "Fast loading", "Simple search"],
            "来源或举例": ["Xiaohongshu filters", "clean menus", "big buttons on mobile"],
            "频次": ["every time I browse", "when shopping", "on slow networks"],
            "感受": ["less frustrating", "stay longer", "leave if slow"],
        },
        sample=(
            "A website feels easy when the layout is clear, pages load fast and search filters make sense. "
            "On Xiaohongshu web I like tags and big photos that work on both phone and laptop. "
            "If a site hangs on the dorm Wi-Fi I leave within seconds. "
            "I find speed and simple menus more important than fancy design."
        ),
        sampleZh=(
            "网站好用要布局清楚、加载快、筛选也好懂。"
            "小红书网页版标签和大图，在手机电脑上都能用。"
            "宿舍网速慢时，卡几秒我就关了。"
            "我觉得速度和简洁菜单比花哨设计更重要。"
        ),
    )
    _p(
        "What makes a website easy to use?",
        "study_websites_search",
        logic="先答搜索框与可靠分类，再举图书馆门户、学术搜索，补写作业场景。",
        kitHint="学习站：想找的信息几步到达、少广告弹窗。",
        words={
            "正面回答": ["Obvious search bar", "Reliable categories", "Less clutter"],
            "来源或举例": ["library database", "clear PDF links", "simple login"],
            "频次": ["every assignment", "before exams", "late-night study"],
            "感受": ["saves time", "less stress", "trust the source"],
        },
        sample=(
            "For study sites an obvious search bar and tidy categories matter most to me. "
            "Our library website puts journal links and PDFs in clear menus without flashy pop-ups. "
            "I use that almost every assignment week and again before exams. "
            "I find trustworthy structure saves time and lowers stress when deadlines are close."
        ),
        sampleZh=(
            "学习类网站最重要的是显眼搜索框和干净分类。"
            "图书馆站把期刊和 PDF 菜单摆得清楚，也没什么弹窗。"
            "几乎每周写作业、考前都会用。"
            "结构靠谱能省时间，临近截止日期也没那么慌。"
        ),
    )
    _p(
        "What is your favourite website?",
        "phone_xiaohongshu_wechat",
        logic="先点名最爱网站及原因，再说明浏览生活方式内容，补频率与放松感受。",
        kitHint="社交向最爱站：小红书类生活方式+购物参考，不是只说微信聊天。",
        words={
            "正面回答": ["Xiaohongshu", "A lifestyle site", "Easy tips"],
            "原因或时间": ["since university", "compare cafés", "see student life posts"],
            "频次": ["a few times a week", "before outings", "evenings"],
            "感受": ["useful", "can over-browse", "practical"],
        },
        sample=(
            "My favourite website is probably Xiaohongshu because lifestyle tips are easy to scan. "
            "I started using it more at university to compare cafés and see how other students organise notes. "
            "I open it a few times a week before outings or quiet evenings. "
            "I find it useful and practical, though I still watch the clock so I do not over-browse."
        ),
        sampleZh=(
            "我最喜欢的网站大概是小红书，生活方式信息扫一眼就有。"
            "上大学后常用它比对咖啡馆、看别人怎么整理笔记。"
            "一周打开几次，出门前或安静晚上。"
            "挺有用也实用，但我还是会看时间别刷太久。"
        ),
    )
    _p(
        "What is your favourite website?",
        "study_websites_search",
        logic="先答最爱的学习搜索站，再说明查资料效率，补工作日频率与信赖感受。",
        kitHint="最爱=学习/搜索站，与社交站明显不同。",
        words={
            "正面回答": ["The library portal", "A search engine", "MOOC site"],
            "原因或时间": ["teacher recommended", "deadline pressure", "clear examples"],
            "频次": ["most weekdays", "before essays", "revision weeks"],
            "感受": ["trust it", "efficient", "less distracted than social feeds"],
        },
        sample=(
            "My favourite website is our library portal because it gathers trusted study links in one place. "
            "A teacher recommended it when I struggled to find journal PDFs for an essay. "
            "I rely on it most weekdays and especially during revision weeks. "
            "I find it efficient and less distracting than opening random social feeds."
        ),
        sampleZh=(
            "我最喜欢的是图书馆门户，可信学习链接都集中在一处。"
            "写论文找不到期刊 PDF 时老师推荐的。"
            "工作日常用，复习周尤其依赖。"
            "效率高，也比乱开社交信息流分心少。"
        ),
    )
    _p(
        "Would you like to have your own website?",
        "phone_xiaohongshu_wechat",
        logic="先表态兴趣一般或想建生活记录站，再说明已有社交账号够用，补时间与维护感受。",
        kitHint="社交素材：可能更想用小红书等平台而非独立建站。",
        words={
            "正面回答": ["Not urgently", "Maybe a blog later", "Platforms enough"],
            "原因或时间": ["busy with study", "already post elsewhere", "after graduation maybe"],
            "频次": ["think about it sometimes", "not now", "if I have a hobby"],
            "感受": ["extra work", "creative wish", "platforms simpler"],
        },
        sample=(
            "Not urgently — I am busy with study and already share bits on Xiaohongshu when I want an audience. "
            "Running my own website would mean updates, design and hosting after every small trip. "
            "I might consider a simple blog after graduation if I pick up a hobby. "
            "For now I find existing platforms simpler even if they show more ads."
        ),
        sampleZh=(
            "不着急——学业忙，想让人看见时在小红书发一点就够了。"
            "自己建站得维护设计、服务器，旅个小游也要更新。"
            "毕业以后若有爱好也许会开简单博客。"
            "眼下我觉得平台更省事，虽然广告多些。"
        ),
    )
    _p(
        "Would you like to have your own website?",
        "study_websites_search",
        logic="先答也许想建学习笔记站，再说明整理资料动机，补未来计划感受。",
        kitHint="学习套装：个人知识库/作品集网站，与社交不同。",
        words={
            "正面回答": ["Maybe a study site", "A portfolio later", "Not now"],
            "原因或时间": ["organise notes", "apply for jobs", "after more projects"],
            "频次": ["think after each project", "maybe in final year", "not daily dream"],
            "感受": ["useful showcase", "time-consuming", "worth it for work"],
        },
        sample=(
            "Maybe one day I would like a small website to organise study notes and project samples. "
            "It could help when I apply for internships, but building it properly takes time I do not have now. "
            "I think about it after each big project, maybe in my final year. "
            "I find the idea useful as a showcase, though still time-consuming."
        ),
        sampleZh=(
            "也许以后想要个小站整理学习笔记和项目。"
            "实习申请可能用得上，但认真搭建现在没时间。"
            "每个大项目结束后会想一下，可能毕业那年再弄。"
            "当作品集挺有用，但还是费时。"
        ),
    )
    _p(
        "How have websites changed compared with ten years ago?",
        "study_websites_search",
        logic="对比过去简单静态页与现在移动适配、在线课，谈学习体验感受。",
        kitHint="学习角度：资料搜索更快、在线课程普及。",
        words={
            "正面回答": ["Much faster", "Mobile friendly", "More online courses"],
            "选项1的特点与作用": ["slow desktop pages", "few videos", "library only on campus"],
            "选项2的特点与作用": ["phone access", "MOOC libraries", "cloud homework"],
            "个人感受": ["more flexible", "still need filters", "cannot trust everything"],
        },
        sample=(
            "Websites changed from slow desktop pages to fast mobile-friendly study platforms. "
            "Ten years ago I mostly read static text in campus libraries, while now I open MOOC videos on my phone. "
            "That makes revision more flexible but also floods me with unverified links. "
            "Personally I enjoy the speed yet still filter carefully before I trust a source."
        ),
        sampleZh=(
            "网站从慢腾腾电脑页变成手机也好用的学习平台。"
            "十年前多在机房看静态文字，现在在手机也能看网课。"
            "复习灵活了，但未核实链接也更多。"
            "我喜欢这速度，但还是会筛选再信来源。"
        ),
    )
    _p(
        "How have websites changed compared with ten years ago?",
        "phone_xiaohongshu_wechat",
        logic="对比过去论坛博客与现在短视频种草站，谈社交购物网站感受。",
        kitHint="社交站变迁：从长博文到短图文+直播购物网页。",
        words={
            "正面回答": ["Shorter content", "More shopping links", "Algorithm driven"],
            "选项1的特点与作用": ["long blog posts", "simple forums", "slower uploads"],
            "选项2的特点与作用": ["Xiaohongshu notes", "live shopping pages", "personalised feeds"],
            "个人感受": ["easier discovery", "more ads", "fun but noisy"],
        },
        sample=(
            "Lifestyle websites shifted from long blogs to short notes with shopping links and live streams. "
            "Ten years ago forums felt slow, while Xiaohongshu-style pages now push tips for each person in seconds. "
            "Discovery is easier, but adverts and sponsored posts feel louder. "
            "Personally I enjoy the fun browsing yet find modern lifestyle sites noisier than old forums."
        ),
        sampleZh=(
            "生活方式网站从长博文变成短笔记加热卖和直播。"
            "十年前论坛很慢，现在小红书式页面几秒就推个性化 tips。"
            "好找，但赞助内容和广告也更吵。"
            "我觉得好玩，也比老论坛喧闹。"
        ),
    )
    _p(
        "Do you prefer getting information from websites or books?",
        "study_websites_search",
        logic="对比网站搜索快与纸质书记忆深，先表态再分述两面，谈个人偏好。",
        kitHint="学习套装：倾向网站快查，但纸质仍可补充。",
        words={
            "正面回答": ["Usually websites", "Books for deep reading", "It depends"],
            "选项1的特点与作用": ["websites", "search in seconds", "latest updates"],
            "选项2的特点与作用": ["books", "fewer distractions", "better for long chapters"],
            "个人感受": ["websites for deadlines", "books for focus", "combine both"],
        },
        sample=(
            "For deadlines I prefer websites because search is fast and articles stay updated. "
            "Books help when I need fewer pop-ups and long chapters on one topic. "
            "Websites win on speed before essays, while books win on quiet focus at night. "
            "Personally I combine both instead of choosing only one source."
        ),
        sampleZh=(
            "赶作业我更爱网站，搜索快、资料也新。"
            "想少分心、啃长章节时纸质书更好。"
            "写论文前网站胜在速度，深夜专注则书面更稳。"
            "我一般是两个一起用，不唯独一种。"
        ),
    )
    _p(
        "Do you prefer getting information from websites or books?",
        "phone_xiaohongshu_wechat",
        logic="对比生活方式类网页短贴士与书本系统知识，谈休闲 vs 深度学习偏好。",
        kitHint="社交/种草站=快 tip；书本=系统；网站偏向轻量信息。",
        words={
            "正面回答": ["Websites for quick tips", "Books for depth", "Depends on topic"],
            "选项1的特点与作用": ["lifestyle websites", "photos and comments", "fast ideas"],
            "选项2的特点与作用": ["printed guides", "less hype", "structured chapters"],
            "个人感受": ["websites for daily life", "books for serious study", "balance both"],
        },
        sample=(
            "For daily life tips I prefer websites because short posts show photos and real comments quickly. "
            "Printed books feel better when a topic needs depth without sponsored links beside every paragraph. "
            "I browse lifestyle sites before a café visit but still read a proper book for coursework. "
            "Personally I balance quick web tips with books when I need serious, quiet information."
        ),
        sampleZh=(
            "日常生活窍门我更爱网站，短文配图还有真人评论。"
            "要系统深入、旁边没赞助链接时，纸质书更好。"
            "去咖啡馆前刷生活方式站，写作业仍看书。"
            "轻量 tip 靠网，严肃安静学习靠书，我会搭配用。"
        ),
    )