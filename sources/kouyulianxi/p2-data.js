// P2 data - 6 大素材 + 33 道答题思路
const P2_DATA = {
  materials: [
    {
      id: "yumeng",
      name: "朋友·雨萌",
      type: "人物",
      summary: "给出关键建议的挚友，两种主体段可按考题选用",
      steps: [
        {
          label: "背景介绍",
          zh: "雨萌是我最重要的朋友之一。我们从小在同一个街区长大，上同一所学校。她非常聪明乐观，她的生活态度总是激励着我。无论是在学习还是个人生活中，她总是愿意倾听并支持我。",
          en: "Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school. She is really smart and optimistic, and her attitude towards life always inspires me. Whether in study or personal life, she is always willing to listen and support me."
        },
        {
          label: "主体事件（默认情况A·大学考研；亦可选情况B·高考选专业，见 variants）",
          zh: "在我大学三年级的时候，我面临着一个抉择：是继续攻读硕士学位，还是毕业后直接工作。我感到十分茫然，于是找雨萌聊了聊。那天我们在校园里边走边聊，她非常耐心地倾听。然后她建议说：「别担心找工作的压力。想想你未来一生想做什么。如果你确定想继续深造，那就全力以赴。我相信你最终会找到一份热爱的工作。」 最后，。。。",
          en: "When I was in my third year at university, I faced a crossroads: whether to pursue further studies for a master's degree or to start working after graduation. I felt quite at a loss, so I talked with Yumeng about it. That day we walked around the campus, and she listened very patiently. Then she suggested, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it. I believe you'll find a job you love eventually.\" In the end, ...."
        },
        {
          label: "感受与升华",
          zh: "她的话给了我巨大的力量。直到今天我仍然感激她睿智的建议。",
          en: "Her words gave me so much strength. I still appreciate her wise advice to this day."
        }
      ],
      variants: [
        {
          id: "a",
          label: "情况A·大学考研",
          zh: "在我大学三年级的时候，我面临着一个抉择：是继续攻读硕士学位，还是毕业后直接工作。我感到十分茫然，于是找雨萌聊了聊。那天我们在校园里边走边聊，她非常耐心地倾听。然后她建议说：「别担心找工作的压力。想想你未来一生想做什么。如果你确定想继续深造，那就全力以赴。我相信你最终会找到一份热爱的工作。」 最后，。。。",
          en: "When I was in my third year at university, I faced a crossroads: whether to pursue further studies for a master's degree or to start working after graduation. I felt quite at a loss, so I talked with Yumeng about it. That day we walked around the campus, and she listened very patiently. Then she suggested, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it. I believe you'll find a job you love eventually.\" In the end, ...."
        },
        {
          id: "b",
          label: "情况B·高考选专业",
          zh: "高中毕业那年，我面临了人生中最艰难的选择。由于我在大学入学考试中没有发挥出最佳水平，我的计划被完全打乱了。我左右为难：一边是梦想的大学却配着一个我毫无兴趣的专业，另一边是梦想的专业却在一所相当普通的大学。我当时非常沮丧。那时，她告诉我：「你的热情是你最好的老师。尽管去做吧。」大学的排名什么也不是。我知道你未来一定会发光。",
          en: "The year I graduated from high school, I faced the most difficult choice in my life. Because I didn't give my best performance in the university entrance exam, my plans were completely disrupted. I was torn between, on the one hand, my dream university with a major I wasn't interested in at all, and on the other hand, my dream major at a rather mediocre university. I was so depressed. At that time, she told me, \"Your passion is your best teacher. Just go for it. The ranking of a university means nothing. I know you're going to shine in the future.\""
        }
      ],
      endingTip: "她的话给了我巨大的力量，至今仍感激她睿智的建议"
    },
    {
      id: "sun",
      name: "明星·孙颖莎",
      type: "人物",
      summary: "当下最受欢迎的乒乓球运动员，巴黎奥运混双夺金",
      steps: [
        {
          label: "背景介绍",
          zh: "我想聊的人是著名的乒乓球运动员孙颖莎。我认为她很可能就是当下中国最受欢迎的乒乓球选手。她非常年轻但才华横溢，刚过20岁就已经几乎赢得了国内外所有顶级赛事的奖项。",
          en: "Well, the person I want to talk about is the famous table tennis player Sun Yingsha, and I think she is probably the most popular one in China right now. She is very young but incredibly talented, and she's just over 20 but has already won almost all the top prizes in both domestic and international competitions."
        },
        {
          label: "主体事件",
          zh: "就在去年，她在巴黎奥运会上与王楚钦搭档混双，在巨大压力下发挥出最佳水平，击败强敌并赢得了金牌。",
          en: "Just last year, she played mixed doubles with Wang Chuqin at the Paris Olympic Games and gave her best performance under enormous pressure to beat strong opponents and win the gold medal."
        },
        {
          label: "社会影响与感受",
          zh: "此后，她在中国变得极其受欢迎，人们如此着迷于她可爱的酒窝和肉肉的脸颊，甚至用她的形象制作了许多贴纸。有些贴纸是她的脸配上可爱装饰，而另一些则是她和搭档的可爱情侣虚拟形象。人们经常在社交媒体上使用它们来活跃对话气氛。",
          en: "After that, she became extremely popular in China, and people are so fascinated by her adorable dimples and chubby cheeks that they've even made lots of stickers out of her image. Some stickers feature her face with cute additions, while others portray her and her partner as a lovely couple, and people often use them on social media to lighten the mood in a conversation."
        }
      ],
      endingTip: "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象"
    },
    {
      id: "movie",
      name: "影视·夏洛特烦恼",
      type: "影视",
      summary: "沈腾马丽主演的时间旅行喜剧，领悟爱的珍贵",
      steps: [
        {
          label: "背景介绍",
          zh: "《夏洛特烦恼》是一部关于时间旅行的中国电影，由沈腾和马丽这两位中国最著名的喜剧演员主演，他们这对极其有趣的搭档让我非常喜欢这部电影。",
          en: "Xialuotefannao is a Chinese movie about a man who can travel in time. This movie stars China's most famous comedians, Shen Teng and Ma Li, who are the funniest couple, so I am really a big fan of this film."
        },
        {
          label: "主体情节",
          zh: "在故事中，夏洛发现自己能穿越回高中时代，并选择了一条不同的人生道路去追求他梦想的女孩秋雅，而不是他真正的妻子马丽。十年后，他成为著名音乐家并与秋雅结婚，梦想成真，却随后接到医生通知说他已处于癌症二期。",
          en: "In the story, Xialuo found he could travel in time and went back to his high school days, and he chose a different life path to pursue his dream girl, Qiuya, instead of his real wife, Ma Li. After 10 years, he became a famous musician and married Qiuya. All of his dreams came true until he got a note from his doctor saying that he was already in the second stage of cancer."
        },
        {
          label: "感受与反转",
          zh: "在这段艰难时期，秋雅不仅离开了他，还骗走了他所有的钱；然而，马丽却出现并照顾他，这让他意识到爱才是生命中最宝贵的东西。最终，他发现这一切不过是一场长长的梦。",
          en: "In this critical period, to his surprise, Qiuya gave up on him and even tricked him out of all his money. However, Ma Li showed up to take care of him, and he realized that love was the most valuable thing in his life. In the end, he found that all of this was a long dream."
        }
      ],
      endingTip: "领悟到爱才是生命中最宝贵的东西"
    },
    {
      id: "badminton",
      name: "事件·羽毛球",
      type: "事件",
      summary: "缓解申请压力、结交球友、改善心理健康的运动",
      steps: [
        {
          label: "起因背景",
          zh: "最近，我忙于申请硕士项目和学英语，所以总是很累，有时无法专注学习；朋友建议我锻炼身体，于是我开始打羽毛球。",
          en: "Recently, I have been occupied by applying for master's programs and studying English, so I always get tired and sometimes can't focus on my studies. My friends advised me to do some exercise, so I started to play badminton."
        },
        {
          label: "主体益处·社交",
          zh: "羽毛球对我有很多积极影响。首先，众所周知，羽毛球是一项需要搭档的运动，所以我常在球场和陌生人组队。很快，我与一些同样热爱运动的人成为了朋友，我们开始每周末约着一起打球，我也发现自己变得越来越外向。",
          en: "Badminton has had a lot of positive impacts on me. First, as you know, badminton is a sport that requires a partner, so I often team up with strangers at the court. Soon, I made friends with some people who shared the same passion for sports, and we started meeting up every weekend to play together. I also found myself becoming more and more outgoing."
        },
        {
          label: "感受升华·心理健康",
          zh: "其次，它对心理健康也极有益处。当我挥动球拍时，耳边只有球拍与风声，这让我能全神贯注于身心，暂时忘却学业压力。",
          en: "Second, it's been great for my mental health too. When I swing my racket, all I hear is its sound and the wind, allowing me to focus solely on my mind and body and forget the pressure from my studies for a while."
        }
      ],
      endingTip: "全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: "bear",
      name: "物品·小熊玩偶（女生向）",
      type: "物品",
      audience: "girl",
      summary: "Jellycat 泰迪熊，高考压力下带来平静的老朋友；女生优先",
      steps: [
        {
          label: "来源与外观",
          zh: "当我上小学时，我最好的朋友送了我一只 Jellycat 的毛绒泰迪熊作为生日礼物。她知道我特别喜欢柔软可爱的东西，所以特地为我精心挑选了这只小熊。这只泰迪熊是棕色的，小小的，毛非常柔软，脖子上还系着一个红色蝴蝶结。",
          en: "When I was in primary school, my best friend gave me a stuffed teddy bear from Jellycat for my birthday. She knew I was crazy about soft and cute things, so she picked this bear carefully just for me. The teddy bear is small and brown, with very soft fur and a red ribbon around its neck."
        },
        {
          label: "主体事件·缓解压力",
          zh: "我记得在高考前，我压力大到睡不着觉。抱着它，就感觉平静了些，也能睡得更好一些了。",
          en: "I still remember before the college entrance exam, I was so stressed that I couldn't fall asleep. I held the bear in my arms, and somehow I felt calmer and managed to sleep better."
        },
        {
          label: "长远意义与感受",
          zh: "从那时起，每当我感到紧张或难过，我都会抱着它一会儿。它陪伴我度过了很多重要时刻，真的就像一个老朋友一样。",
          en: "Since then, whenever I feel nervous or upset, I would hug it for a while. It has been with me during many important moments, so it really feels like an old friend."
        }
      ],
      endingTip: "它真的就像一个老朋友一样"
    },
    {
      id: "basketball",
      name: "物品·篮球（男生向）",
      type: "物品",
      audience: "boy",
      summary: "父亲送的篮球，与小熊并列；男生优先选用，结构情感线一致",
      steps: [
        {
          label: "来源与外观",
          zh: "当我上初中时，父亲送给我一个篮球作为生日礼物。他知道我特别喜欢运动，所以特地为我挑选了这个球。这个篮球是橙色的，手感很好，上面还有清晰的黑色线条，看起来既结实又专业。",
          en: "When I was in middle school, my father gave me a basketball for my birthday. He knew I was crazy about sports, so he picked this ball carefully just for me. The basketball is orange, with a really nice grip and clear black lines on it. It looks both solid and professional."
        },
        {
          label: "主体事件·缓解压力",
          zh: "我记得在高考前，我压力大到坐在书桌前根本学不进去。于是我下楼到空地上投篮。每当球进筐的那一刻，我就感觉平静了些，脑子也清醒了不少。",
          en: "I still remember before the college entrance exam, I was so stressed that I couldn't focus at my desk at all. So I went downstairs and shot some hoops in an open area. Every time the ball went through the hoop, I somehow felt calmer and my mind became much clearer."
        },
        {
          label: "长远意义与感受",
          zh: "从那时起，每当我感到紧张或烦躁，我都会拿着它出去投一会儿篮。它陪伴我度过了很多重要时刻，真的就像一个老朋友一样。",
          en: "Since then, whenever I feel nervous or upset, I would take it outside and shoot for a while. It has been with me during many important moments, so it really feels like an old friend."
        }
      ],
      endingTip: "它真的就像一个老朋友一样"
    },
    {
      id: "tianchi",
      name: "地点·长白山天池",
      type: "地点",
      summary: "东北未经雕琢的自然风光，登顶天池的震撼之旅",
      steps: [
        {
          label: "地点简介",
          zh: "长白山是中国东北部的一个偏远地区，以未经雕琢的自然风光和一座位于山顶的「天池」而闻名。",
          en: "It's a remote area in the northeast part of China which is famous for its untouched nature and a lake located at the peak of a hill called \"天池\", it means the pond of heaven."
        },
        {
          label: "攀登过程",
          zh: "首先是一段通往山顶的极长阶梯，我们必须爬上去，但至少景色确实令人叹为观止。你可以俯瞰整片山脉，看到前所未见的湛蓝天空，而且空气也格外清新。",
          en: "First there was an extremely long staircase which leads to the hilltop, we had to go up it, but at least the scenery was truly breathtaking. You can overlook the entire mountain and see the most clear blue sky you've ever seen, also, the air was extremely fresh."
        },
        {
          label: "登顶震撼与感受",
          zh: "当我们终于到达山顶，我们看到了那个真正的「天池」。这个湖巨大无比，纯净如碧玉。在阳光下像一颗巨大的钻石一样闪耀，我的天啊，一看到它，攀登时流的所有汗水都值得了。",
          en: "When we finally reached the top, we saw the very \"天池\". The lake is huge and pure jade. Shining like a huge diamond under the sunlight, oh my god, as soon as I saw it, all the sweat from the climbing was all worth it."
        }
      ],
      endingTip: "一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: "robot",
      name: "物品·扫地机器人",
      type: "物品",
      summary: "（补充素材）养猫家庭省时省力的清洁帮手",
      optional: true,
      steps: [
        {
          label: "购买背景",
          zh: "我想聊聊扫地机器人。几年前我买了它，主要是因为家里养了两只猫，到处都是猫毛，而那时我又忙于学业没时间收拾。",
          en: "I'd like to talk about a robot vacuum cleaner. I bought it several years ago, and the main reason was that I have two cats at home. As you can imagine, there's cat fur all over my home all the time. Meanwhile, I was always busy with my studies back then and didn't have time to tidy my home. That's the time when I decided to get one."
        },
        {
          label: "功能与便利",
          zh: "这个小设备极其方便。以前我得自己处理猫毛和灰尘，非常累；现在只需在手机上连上应用，点几下就能搞定。它有多种模式，可以设日常清扫，也可以切换扫地模式；而且它能清洁到人手够不到的角落，打扫完还能自清洁。",
          en: "This little device is extremely handy. In the past, I had to deal with all the fur and dust, which was quite tiring/a lot of work. But now, I just need to connect it to an app on my phone, and get everything done with just a few clicks. It offers different modes. For example, I can set it for regular cleaning on a daily basis, or switch to sweep mode when I need it to mop the floor. And what's really impressive is that it can reach corners that it's impossible for me to clean by hand. After it finishes cleaning, it can even self-clean."
        },
        {
          label: "感受",
          zh: "多亏了扫地机器人，打扫不再是问题，它帮我节省大量时间，也让家里保持整洁。",
          en: "Thanks to this robot vacuum, cleaning is no longer an issue for me. It saves me so much time and keeps my home clean."
        }
      ],
      endingTip: "它帮我节省大量时间，打扫不再是问题"
    }
  ],
  questions: [
    {
      id: 1,
      title: "完美工作",
      q: "Perfect job",
      openingEn: "Speaking of a perfect job, being a professional athlete is the first thing that jumps into my mind.",
      openingZh: "谈到完美工作，成为职业运动员是我脑海中跳出的第一件事。",
      materialId: "sun",
      materialHint: "就像她一样年纪轻轻才华横溢，在巨大压力下赢得金牌，广受欢迎。",
      endingTip: "她是中国最受欢迎的乒乓球选手，这便是我梦想的完美状态"
    },
    {
      id: 2,
      title: "想见的名人",
      q: "A famous person you would like to meet",
      openingEn: "When it comes to a famous person I'd like to meet, I would definitely choose a sports star.",
      openingZh: "谈到想见的名人，我绝对会选一位体育明星。",
      materialId: "sun",
      materialHint: "想见这位20出头就包揽顶级赛事奖项的乒乓球冠军，看看她可爱的酒窝。",
      endingTip: "用素材第三步感受收尾：她极其受欢迎，人们着迷于她可爱的酒窝"
    },
    {
      id: 3,
      title: "禁用手机的场合",
      q: "Occasion not allowed to use mobile phone",
      openingEn: "This topic reminds me of a strict sports training session I had recently.",
      openingZh: "这个话题让我想起了最近一次严格的运动训练课。",
      materialId: "badminton",
      materialHint: "因为我忙于申请硕士压力大，去打羽毛球时，教练为了让我能全神贯注于身心，禁止带手机进球场。",
      endingTip: "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: 4,
      title: "给别人建议",
      q: "Time you gave advice to others",
      openingEn: "Talking about giving advice, I'd like to share an experience where I helped my best friend through a hard time.",
      openingZh: "谈到给建议，我想分享一次帮好朋友度过难关的经历。",
      materialId: "yumeng",
      materialHint: "（角色互换）雨萌在考研和工作之间面临抉择，我把「你的热情是你最好的老师」这番话送给了她，鼓励她全力以赴。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 5,
      title: "外国的短期停留",
      q: "Foreign country to stay/work for a short period",
      openingEn: "If I had the chance to stay abroad for a short time, I would choose to go to the UK for a short study program.",
      openingZh: "如果能在国外短期停留，我会选择去英国进行短期学习。",
      materialId: "yumeng",
      materialHint: "这正是因为在我对未来茫然时，雨萌耐心倾听并鼓励我继续攻读硕士学位，让我做出了出国深造的决定。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 6,
      title: "想拥有的科技产品",
      q: "Piece of technology you would like to own",
      openingEn: "Speaking of a piece of technology I really desire to own, it would be an advanced digital camera.",
      openingZh: "谈到我极其渴望拥有的科技产品，那是一台高级数码相机。",
      materialId: "tianchi",
      materialHint: "因为我想带它去记录长白山天池未经雕琢的自然风光，拍下它在阳光下像钻石一样闪耀的绝美画面。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: 7,
      title: "擅长做计划的人",
      q: "Person good at planning",
      openingEn: "When reading this prompt, my bestie immediately came to my mind. She is a master of planning.",
      openingZh: "看到这个题目，我立马想到了我闺蜜，她是个计划大师。",
      materialId: "yumeng",
      materialHint: "她非常聪明乐观，把人生的抉择（考研还是工作）规划得极其清晰，并用她的态度激励了我。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 8,
      title: "喜欢画画的孩子",
      q: "Child who loves drawing/painting",
      openingEn: "This topic reminds me of my little cousin. She has a huge passion for drawing characters.",
      openingZh: "这让我想起我的小表妹，她对画人物充满热情。",
      materialId: "sun",
      materialHint: "表妹非常着迷于乒乓球运动员孙颖莎，经常画她可爱的酒窝和肉肉的脸颊，还自己动手做成贴纸。",
      endingTip: "用素材第三步感受收尾：她极其受欢迎，人们着迷于她可爱的酒窝和贴纸"
    },
    {
      id: 9,
      title: "App/程序",
      q: "Program or app",
      openingEn: "To be honest, the app I use most frequently is a social media chat app.",
      openingZh: "老实说，我最常用的 App 是一个社交聊天软件。",
      materialId: "sun",
      materialHint: "在这个 App 上，人们经常使用孙颖莎的贴纸（可爱的酒窝和情侣虚拟形象）来活跃对话气氛。",
      endingTip: "用素材第三步感受收尾：人们用她的贴纸活跃对话气氛"
    },
    {
      id: 10,
      title: "最近读过的故事",
      q: "Story you have read recently",
      openingEn: "Recently, I read a fascinating story about time travel, which was also adapted into a famous movie.",
      openingZh: "最近我读了一个关于时间旅行的奇妙故事，它还被拍成了著名电影。",
      materialId: "movie",
      materialHint: "讲述夏洛穿越回高中重新选择人生，最终意识到爱才是生命中最宝贵的东西的故事。",
      endingTip: "用素材第三步感受收尾：领悟到爱才是生命中最宝贵的东西"
    },
    {
      id: 11,
      title: "微笑的场合",
      q: "Occasion when many people were smiling",
      openingEn: "Thinking about an occasion filled with smiles, a remarkable mountain trip with my friends pops up in my head.",
      openingZh: "想到充满微笑的场合，我脑海中浮现出一次非凡的爬山之旅。",
      materialId: "tianchi",
      materialHint: "当我们爬上极长的阶梯，终于在山顶看到像巨大钻石一样的天池时，所有人都开心地笑了，攀登的汗水都值得了。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: 12,
      title: "为家人骄傲",
      q: "Time you felt proud of a family member",
      openingEn: "Speaking of a proud moment, I want to talk about my cousin and his amazing changes.",
      openingZh: "谈到骄傲的时刻，我想讲讲我表弟和他惊人的改变。",
      materialId: "badminton",
      materialHint: "他之前压力大无法专注，后来开始打羽毛球，不仅交到了热爱运动的朋友，还变得越来越外向，我为他深感自豪。",
      endingTip: "用素材第三步感受收尾：变得外向，全神贯注于身心"
    },
    {
      id: 13,
      title: "对家庭重要的东西",
      q: "Important thing kept in family",
      openingEn: "We don't have expensive antiques, but we do have a stuffed toy that has been kept for a long time and is incredibly precious.",
      openingZh: "我们没有昂贵古董，但有一个保存了很久且无比珍贵的毛绒玩具。",
      materialId: "bear",
      materialOptions: ["bear", "basketball"],
      materialHint: "小学时朋友送的 Jellycat 泰迪熊，非常柔软，陪伴我度过了高考前无数个压力山大的夜晚，像个老朋友。",
      materialHintById: {
        bear: "小学时朋友送的 Jellycat 泰迪熊，非常柔软，陪伴我度过了高考前无数个压力山大的夜晚，像个老朋友。",
        basketball: "父亲送的篮球，保存多年；高考前下楼投篮减压，像个老朋友。"
      },
      openingById: {
        bear: {
          en: "We don't have expensive antiques, but we do have a stuffed toy that has been kept for a long time and is incredibly precious.",
          zh: "我们没有昂贵古董，但有一个保存了很久且无比珍贵的毛绒玩具。"
        },
        basketball: {
          en: "We don't have expensive antiques, but we do have a basketball that has been kept for a long time and is incredibly precious.",
          zh: "我们没有昂贵古董，但有一个保存了很久且无比珍贵的篮球。"
        }
      },
      endingTip: "用素材第三步感受收尾：它真的就像一个老朋友一样"
    },
    {
      id: 14,
      title: "商场",
      q: "Shopping mall",
      openingEn: "Well, I'm not a shopaholic, but there is a shopping mall I visited to buy a special gift.",
      openingZh: "我不是购物狂，但我去过一家商场买一份特别的礼物。",
      materialId: "bear",
      materialOptions: ["bear", "basketball"],
      materialHint: "去商场里是为了给好朋友精心挑选一只 Jellycat 小熊玩偶作为生日礼物，因为她喜欢柔软可爱的东西。",
      materialHintById: {
        bear: "去商场里是为了给好朋友精心挑选一只 Jellycat 小熊玩偶作为生日礼物，因为她喜欢柔软可爱的东西。",
        basketball: "去商场或体育用品店，为朋友（或自己）精心挑选一个手感好的篮球作为生日礼物。"
      },
      endingTip: "用素材第三步感受收尾：它真的就像一个老朋友一样"
    },
    {
      id: 15,
      title: "自行车/摩托车/汽车旅行",
      q: "Bicycle/motorcycle/car trip",
      openingEn: "If I could plan a road trip right now, I would definitely go for a car trip to Northeast China.",
      openingZh: "如果现在能计划一次公路旅行，我肯定会选自驾去中国东北。",
      materialId: "tianchi",
      materialHint: "开车去欣赏长白山未经雕琢的自然风光，爬阶梯去看纯净如碧玉的天池。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: 16,
      title: "鼓励你保护自然的人",
      q: "Person who encouraged you to protect nature",
      openingEn: "This topic brings my best friend Yumeng to my mind. She always cares about the environment.",
      openingZh: "这个话题让我想到了我最好的朋友雨萌。她总是关心环境。",
      materialId: "yumeng",
      materialIds: ["yumeng", "tianchi"],
      materialHint: "她不仅在我人生的十字路口给我建议，还鼓励我一起去长白山旅行，去见证并保护那里未经雕琢的自然风光。",
      endingTip: "用素材第三步感受收尾：天池之美让保护自然变得有意义"
    },
    {
      id: 17,
      title: "机智解决问题的人",
      q: "Person who solved a problem in a smart way",
      openingEn: "When thinking of someone who solves problems smartly, my best friend is the first one I want to talk about.",
      openingZh: "想到能机智解决问题的人，我第一个想谈我的好朋友。",
      materialId: "yumeng",
      materialHint: "在我面临考研还是工作的艰难抉择时，她机智地用「热情是你最好的老师」化解了我的茫然。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 18,
      title: "朋友所学",
      q: "Friend who learned something new",
      openingEn: "Speaking of a friend picking up a new skill, I have to mention my homie's recent sports journey.",
      openingZh: "谈到朋友学新技能，我得提提我哥们的近期运动之旅。",
      materialId: "badminton",
      materialHint: "朋友忙于申请硕士压力大，去学了打羽毛球，在球场上结交陌生人，变得外向且全神贯注于身心。",
      endingTip: "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: 19,
      title: "不享受的音乐活动",
      q: "Music event you didn't enjoy",
      openingEn: "Honestly, I usually enjoy music, but there was one noisy concert that was a total disaster for me.",
      openingZh: "说实话我通常很享受音乐，但有一次吵闹的音乐会对我是个灾难。",
      materialId: "badminton",
      materialHint: "因为我当时正忙于申请硕士，极其疲惫无法专注。比起吵闹的音乐，我更想去打羽毛球，只听风声和球拍声来放松身心。",
      endingTip: "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: 20,
      title: "近期观影",
      q: "Movie you watched and enjoyed recently",
      openingEn: "I am a big fan of movies, and the most intriguing one I watched recently is a Chinese comedy.",
      openingZh: "我是个超级影迷，最近看的最好玩的是一部中国喜剧。",
      materialId: "movie",
      materialHint: "沈腾和马丽主演，讲述时间旅行，最终让人领悟爱才是生命中最宝贵的东西。",
      endingTip: "用素材第三步感受收尾：领悟到爱才是生命中最宝贵的东西"
    },
    {
      id: 21,
      title: "有趣的建筑",
      q: "Interesting building",
      openingEn: "Talking about an interesting building, I want to describe a unique observation deck I visited.",
      openingZh: "谈到有趣的建筑，我想描述我参观过的一个独特的观景台。",
      materialId: "tianchi",
      materialHint: "它建在长白山的极长阶梯顶端，站在那里可以俯瞰整片山脉和纯净如碧玉的天池。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: 22,
      title: "发挥想象力",
      q: "Time you needed to use your imagination",
      openingEn: "When it comes to using imagination, nothing beats the experience of watching a fantastic movie.",
      openingZh: "谈到发挥想象力，没有什么比看一部奇幻电影更贴切了。",
      materialId: "movie",
      materialHint: "看电影时，我跟着主角发挥想象力，想象如果自己也能穿越回高中时代，去选择不同的人生道路会怎样。",
      endingTip: "用素材第三步感受收尾：领悟到爱才是生命中最宝贵的东西"
    },
    {
      id: 23,
      title: "乐于助人的人",
      q: "Person who often helps others",
      openingEn: "For this topic, I can think of no one else but my closest friend, Yumeng.",
      openingZh: "对于这个话题，除了我最亲密的朋友雨萌，我想不到别人。",
      materialId: "yumeng",
      materialHint: "她聪明乐观，总愿意耐心倾听。在我面临人生十字路口时，给了我「全力以赴」的巨大力量。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 24,
      title: "花费超过预期的物品",
      q: "Item on which you spent more than expected",
      openingEn: "Speaking of spending a fortune, I have to admit I paid a lot for a specific toy.",
      openingZh: "谈到花大价钱，我承认我曾为一个特定玩具花超了预算。",
      materialId: "bear",
      materialOptions: ["bear", "basketball"],
      materialHint: "为了给朋友送生日礼物，精心挑选了一只 Jellycat 的棕色小熊，虽然很贵，但它能在高压下带来平静，物超所值。",
      materialHintById: {
        bear: "为了给朋友送生日礼物，精心挑选了一只 Jellycat 的棕色小熊，虽然很贵，但它能在高压下带来平静，物超所值。",
        basketball: "为了买手感更好、更专业的篮球花超了预算，但高压时投篮能让自己冷静，物超所值。"
      },
      openingById: {
        bear: {
          en: "Speaking of spending a fortune, I have to admit I paid a lot for a specific toy.",
          zh: "谈到花大价钱，我承认我曾为一个特定玩具花超了预算。"
        },
        basketball: {
          en: "Speaking of spending a fortune, I have to admit I paid a lot for a specific sports item.",
          zh: "谈到花大价钱，我承认我曾为一个运动用品花超了预算。"
        }
      },
      endingTip: "用素材第三步感受收尾：它真的就像一个老朋友一样"
    },
    {
      id: 25,
      title: "鼓励别人做不愿做的事",
      q: "Encouraged someone to do something they didn't want to do",
      openingEn: "This reminds me of the time I encouraged my friend to do some sports.",
      openingZh: "这让我想起我鼓励朋友去做运动的的经历。",
      materialId: "badminton",
      materialHint: "朋友因为申请硕士压力大且疲惫，不愿出门。我鼓励他去打羽毛球，最终他交到了朋友并释放了压力。",
      endingTip: "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: 26,
      title: "想多了解的野生动物",
      q: "Wild animal you want to learn more about",
      openingEn: "After a mountain trip, I became completely fascinated by the wild animals living there.",
      openingZh: "一次爬山旅行后，我完全迷上了那里的野生动物。",
      materialId: "tianchi",
      materialHint: "在长白山未经雕琢的自然风光里，我感受到了清新的空气，也激发了我对生存在这片纯净土地上的野生动物的好奇心。",
      endingTip: "用素材第三步感受收尾：天池之美激发对自然与野生动物的好奇"
    },
    {
      id: 27,
      title: "擅长音乐的朋友",
      q: "Friend good at music/singing",
      openingEn: "Speaking of a friend with musical talent, I immediately think of my bestie.",
      openingZh: "谈到有音乐天赋的朋友，我立马想到了我闺蜜。",
      materialId: "movie",
      materialHint: "她唱歌像天籁，梦想成为像电影里夏洛那样的著名音乐家，通过努力追求她的音乐梦想。",
      endingTip: "用素材第三步感受收尾：领悟到爱才是生命中最宝贵的东西"
    },
    {
      id: 28,
      title: "重要的好朋友",
      q: "Good friend important to you",
      openingEn: "When talking about a vital friend in my life, Yumeng is the name that pops up.",
      openingZh: "谈论生命中重要的朋友，雨萌的名字立刻浮现。",
      materialId: "yumeng",
      materialHint: "同个街区长大，在我面临高考志愿/考研最茫然时给我睿智的建议。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 29,
      title: "迷路",
      q: "Occasion when you lost your way",
      openingEn: "I have a terrible sense of direction, and getting lost during a mountain trip was unforgettable.",
      openingZh: "我方向感极差，一次爬山时迷路让我终生难忘。",
      materialId: "tianchi",
      materialHint: "在爬通往天池的极长阶梯时，大雾让我一度走错路，但最终登顶看到钻石般的天池那一刻，一切都值得了。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    },
    {
      id: 30,
      title: "在家族企业工作的人",
      q: "Person working for a family business",
      openingEn: "This topic perfectly describes my friend, who helps run her family's toy shop.",
      openingZh: "这题完美描述了我朋友，她帮忙经营她家的玩具店。",
      materialId: "bear",
      materialOptions: ["bear", "basketball"],
      materialHint: "她家的店专门卖各种毛绒玩具，我正是在那里精心挑选了那只柔软的 Jellycat 小熊玩偶。",
      materialHintById: {
        bear: "她家的店专门卖各种毛绒玩具，我正是在那里精心挑选了那只柔软的 Jellycat 小熊玩偶。",
        basketball: "朋友帮忙经营家里的体育用品店；我正是在那里精心挑选了那只手感很好的篮球。"
      },
      openingById: {
        bear: {
          en: "This topic perfectly describes my friend, who helps run her family's toy shop.",
          zh: "这题完美描述了我朋友，她帮忙经营她家的玩具店。"
        },
        basketball: {
          en: "This topic perfectly describes my friend, who helps run his family's sports shop.",
          zh: "这题完美描述了我朋友，他帮忙经营家里的体育用品店。"
        }
      },
      endingTip: "用素材第三步感受收尾：它真的就像一个老朋友一样"
    },
    {
      id: 31,
      title: "想提升的天赋",
      q: "Natural talent you want to improve",
      openingEn: "If I could improve any natural talent, I would focus on my athletic abilities.",
      openingZh: "如果能提升天赋，我会专注于我的运动能力。",
      materialId: "badminton",
      materialHint: "我开始打羽毛球来缓解申请硕士的压力，我希望提升挥拍的技巧，让自己能更好地在球场上全神贯注于身心。",
      endingTip: "用素材第三步感受收尾：全神贯注于身心，暂时忘却学业压力"
    },
    {
      id: 32,
      title: "和亲友享受的晚餐",
      q: "Great dinner enjoyed with friends/family",
      openingEn: "Speaking of a memorable dinner, a meal I had with my best friend comes to mind.",
      openingZh: "谈到难忘的晚餐，我想起和最好朋友共进的一餐。",
      materialId: "yumeng",
      materialHint: "那次晚餐我正面临人生的十字路口，我们在餐桌上长谈，她耐心地倾听并给了我受用一生的建议。",
      endingTip: "用素材第三步感受收尾：她的话给了我巨大力量，至今仍感激她的睿智建议"
    },
    {
      id: 33,
      title: "想再去一次的远行",
      q: "Long journey you would like to take again",
      openingEn: "Among all the places I've visited, the journey to northeastern China is the one I want to repeat most.",
      openingZh: "在我去过的地方里，去中国东北的旅行是我最想重温的。",
      materialId: "tianchi",
      materialHint: "长白山天池那次远行让我难忘——未经雕琢的自然风光、极长阶梯和登顶看到钻石般天池的震撼，让我最想重温。",
      endingTip: "用素材第三步感受收尾：一看到天池，攀登的所有汗水都值得了"
    }
  ]
};
