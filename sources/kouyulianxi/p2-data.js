// P2 data - 6 大素材 + 56 道答题思路（2026年5-8月现行题库，含参考答案）
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
          zh: "在我大学三年级的时候，我面临着一个抉择：是继续攻读硕士学位，还是毕业后直接工作。我感到十分茫然，于是找雨萌聊了聊。那天我们在校园里边走边聊，她非常耐心地倾听。然后她建议说：「别担心找工作的压力。想想你未来一生想做什么。如果你确定想继续深造，那就全力以赴。我相信你最终会找到一份热爱的工作。」 最后，我决定申请硕士，并一步步朝着目标努力。",
          en: "When I was in my third year at university, I faced a crossroads: whether to pursue further studies for a master's degree or to start working after graduation. I felt quite at a loss, so I talked with Yumeng about it. That day we walked around the campus, and she listened very patiently. Then she suggested, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it. I believe you'll find a job you love eventually.\" In the end, I decided to apply for a master's program and worked toward that goal step by step."
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
          zh: "在我大学三年级的时候，我面临着一个抉择：是继续攻读硕士学位，还是毕业后直接工作。我感到十分茫然，于是找雨萌聊了聊。那天我们在校园里边走边聊，她非常耐心地倾听。然后她建议说：「别担心找工作的压力。想想你未来一生想做什么。如果你确定想继续深造，那就全力以赴。我相信你最终会找到一份热爱的工作。」 最后，我决定申请硕士，并一步步朝着目标努力。",
          en: "When I was in my third year at university, I faced a crossroads: whether to pursue further studies for a master's degree or to start working after graduation. I felt quite at a loss, so I talked with Yumeng about it. That day we walked around the campus, and she listened very patiently. Then she suggested, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it. I believe you'll find a job you love eventually.\" In the end, I decided to apply for a master's program and worked toward that goal step by step."
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
          en: "Recently, I have been occupied with applying for master's programs and studying English, so I always get tired and sometimes can't focus on my studies. My friends advised me to do some exercise, so I started to play badminton."
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
          en: "First there was an extremely long staircase which leads to the hilltop, we had to go up it, but at least the scenery was truly breathtaking. You can overlook the entire mountain and see the clearest blue sky you've ever seen, also, the air was extremely fresh."
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
      "id": 1,
      "title": "近期改变",
      "q": "Describe a change that you made recently",
      "cuePoints": [
        "What the change was",
        "What caused the change",
        "What you did for the change",
        "And explain how you feel about the change"
      ],
      "tag": "新增",
      "recentCount": 7994,
      "heatRank": 1,
      "heatLevel": "star3",
      "openingEn": "The change I want to talk about is something quite simple but meaningful: I started to play badminton regularly.",
      "openingZh": "我想谈的改变很简单却很有意义：我开始经常打羽毛球。",
      "materialId": "badminton",
      "materialHint": "把申请硕士与学英语的压力作为改变原因，引出开始打球、与陌生人组队、变得更外向，最后用挥拍忘压收尾。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "The change I want to talk about is something quite simple but meaningful: I started to play badminton regularly. About three months ago, I had been occupied with applying for master's programs and studying English, so I always got tired and sometimes couldn't focus on my studies. A friend noticed how stressed I looked and advised me to do some exercise, and that was what caused the change. What I did was book a court twice a week and force myself to show up even when I felt busy. At first I was awkward, but badminton is a sport that requires a partner, so I often team up with strangers at the court. Soon I made friends with people who shared the same passion for sports, and we started meeting up every weekend. I also found myself becoming more and more outgoing, which surprised me. Second, when I swing my racket, all I hear is its sound and the wind, allowing me to focus solely on my mind and body and forget the pressure from my studies for a while. Looking back, I feel genuinely positive about this change because it rebuilt both my energy and my social life.",
      "sampleZh": "近期因申请硕士和学英语压力大，朋友建议锻炼，于是开始打羽毛球；常和陌生人组队、变得外向，挥拍时能暂时忘却学业压力，我对这个改变很满意。"
    },
    {
      "id": 2,
      "title": "为家人骄傲",
      "q": "Describe a time when you felt proud of a family member",
      "cuePoints": [
        "When it happened",
        "Who the person is",
        "What the person did",
        "And explain why you felt proud of him/her"
      ],
      "tag": "沿用",
      "recentCount": 5222,
      "heatRank": 2,
      "heatLevel": "star3",
      "openingEn": "I still remember how proud I felt when my cousin turned his stress into a healthier lifestyle last year.",
      "openingZh": "我仍记得去年表弟把压力变成更健康生活方式时，我有多骄傲。",
      "materialId": "badminton",
      "materialHint": "主体换成表弟：他学习压力大后开始打羽毛球，组队交友、变得外向，挥拍忘压；你为他的坚持自豪。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "I still remember how proud I felt when my cousin turned his stress into a healthier lifestyle last year. He is two years younger than me, and around last spring he was occupied with applying for master's programs and studying English. He always got tired and sometimes couldn't focus, so the whole family was worried. What he did next really impressed me: following a friend's advice, he started to play badminton twice a week. Because badminton requires a partner, he often teams up with strangers at the court, and soon he made friends who shared the same passion for sports. They began meeting every weekend, and I found him becoming more and more outgoing. When he swings his racket, he says all he hears is its sound and the wind, which helps him forget the pressure from his studies for a while. I felt proud not only because his mood improved, but also because he chose a positive way to handle difficulty instead of complaining. Watching that change in a family member made me respect him even more.",
      "sampleZh": "表弟去年因申请压力大，后来坚持打羽毛球、与陌生人组队、变得外向；我为他用积极方式面对困难而骄傲。"
    },
    {
      "id": 3,
      "title": "擅长学习和说语言的人",
      "q": "Describe a person who is good at learning and speaking new languages",
      "cuePoints": [
        "How you got to know him/her",
        "How he/she learns a new language",
        "What languages he/she can speak",
        "And explain how you feel about him/her"
      ],
      "tag": "新增",
      "recentCount": 3178,
      "heatRank": 3,
      "heatLevel": "star2",
      "openingEn": "There's a friend of mine who picks up languages faster than anyone I know, and her name is Yumeng.",
      "openingZh": "我有个学语言比谁都快的朋友，叫雨萌。",
      "materialId": "yumeng",
      "materialHint": "雨萌为读硕士认真学英语：同街区长大、校园边走边聊；用热情驱动学习，收尾感激她的建议。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "There's a friend of mine who picks up languages faster than anyone I know, and her name is Yumeng. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so I've watched her learning style for years. She is really smart and optimistic, and English is the language she works on most because she wants to pursue a master's degree abroad. The way she learns is practical: she listens to podcasts while walking, talks to international students, and reviews vocabulary every night. When I was in my third year at university and felt lost about whether to pursue a master's degree or start working, we walked around the campus and she listened very patiently. She even practiced explaining her study plan in English to me, which showed how serious she was. She can speak fluent Mandarin and English, and she is starting basic Japanese for fun. Her words like \"Your passion is your best teacher. Just go for it.\" gave me so much strength, and I still appreciate how language learning and life advice come together in her.",
      "sampleZh": "雨萌是同街区长大的挚友，为读硕士认真学英语；校园散步时她耐心倾听并用热情鼓励我，我很佩服她。"
    },
    {
      "id": 4,
      "title": "改变重要想法",
      "q": "Describe a time when you changed an important opinion of yours",
      "cuePoints": [
        "When you changed your opinion",
        "What the original opinion was",
        "Why you changed it",
        "And explain how you felt about the experience"
      ],
      "tag": "新增",
      "recentCount": 3122,
      "heatRank": 4,
      "heatLevel": "star2",
      "openingEn": "A few years ago I changed an important opinion about what I should do after graduation, and a conversation with Yumeng was the turning point.",
      "openingZh": "几年前我改变了毕业后该做什么的重要想法，和雨萌的一次谈话是转折点。",
      "materialId": "yumeng",
      "materialHint": "原想法是赶紧工作；雨萌校园倾听后劝你想一生想做什么；你改成读硕，用她的话收尾。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "A few years ago I changed an important opinion about what I should do after graduation, and a conversation with Yumeng was the turning point. My original opinion was simple: I should start working as soon as possible to reduce financial pressure on my family. When I was in my third year at university, I faced a crossroads between a master's degree and a job, and I felt quite at a loss every night. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so I trusted her honesty. That day we walked around the campus, and she listened very patiently before she suggested, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it.\" Her calm logic made me realize I had been choosing from fear, not from passion. After that talk I changed my opinion, prepared applications carefully, and entered a master's program without regret. Looking back, the experience felt scary at first but freeing later. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "大三时我原想赶紧工作，雨萌劝我想一生想做什么；我改成读硕，至今感激她的建议。"
    },
    {
      "id": 5,
      "title": "长久目标/抱负",
      "q": "Describe a long-term goal/ambition you would like to achieve",
      "cuePoints": [
        "How long you have had this goal/ambition",
        "What it is",
        "How you will achieve it",
        "And explain why you set it"
      ],
      "tag": "新增",
      "recentCount": 2555,
      "heatRank": 5,
      "heatLevel": "star2",
      "openingEn": "The long-term ambition I keep coming back to is finishing a master's degree in a field I truly care about.",
      "openingZh": "我反复想起的长期目标是完成自己真正热爱领域的硕士学位。",
      "materialId": "yumeng",
      "materialHint": "目标源自雨萌建议：热情是最好的老师；用校园对话说明如何实现与为何设定。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "The long-term ambition I keep coming back to is finishing a master's degree in a field I truly care about. I have had this goal for about three years, ever since my third year at university, when I faced a crossroads: whether to pursue further studies or start working after graduation. At that time I felt quite at a loss, so I talked with Yumeng, one of my most important friends. We grew up in the same neighborhood and went to the same school, and she has always been willing to listen and support me. We walked around the campus, and she listened very patiently, then said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life.\" She also told me, \"Your passion is your best teacher. Just go for it.\" That is why I set this ambition: I want a career built on interest, not only on short-term salary. To achieve it, I am improving my English every week, collecting research ideas, preparing proposals, and applying to programs step by step even when progress feels slow. Some days I still feel tired, but remembering her advice keeps me steady and optimistic. Her words gave me so much strength, and that encouragement is still pushing me forward today.",
      "sampleZh": "长期目标是读完热爱领域的硕士；大三迷茫时雨萌鼓励我，我据此设定并逐步准备。"
    },
    {
      "id": 6,
      "title": "保护环境的法律",
      "q": "Describe a law on environmental protection",
      "cuePoints": [
        "What it is",
        "How you first learned about it",
        "Who benefits from it",
        "And explain how you feel about this law"
      ],
      "tag": "新增",
      "recentCount": 2513,
      "heatRank": 6,
      "heatLevel": "star2",
      "openingEn": "One environmental law I really support is the scenic-area protection rule that bans littering and unauthorized building inside national nature reserves, and I first understood why after visiting Changbai Mountain.",
      "openingZh": "我很支持禁止在国家级自然保护区乱扔垃圾与私搭乱建的景区保护法，去长白山后才真正明白原因。",
      "materialId": "tianchi",
      "materialHint": "用长白山天池景点禁扔垃圾、禁私搭乱建等具体保护区规定切入；串未开发自然、极长阶梯与清澈湖水，说明法律如何保护游客与生态，感受落在登顶值得。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "One environmental law I really support is the scenic-area protection rule that bans littering and unauthorized building inside national nature reserves, and I first understood why after visiting Changbai Mountain. In practice, visitors must carry trash out, stay on marked paths, and cannot open shops or hotels beside protected lakes. I learned about these rules when park guides explained them before we entered a remote area in the northeast part of China which is famous for its untouched nature and a lake called \"Tianchi\", the pond of heaven. First there was an extremely long staircase which leads to the hilltop; we had to go up it, but the scenery was truly breathtaking. You can overlook the entire mountain, see the clearest blue sky you've ever seen, and breathe extremely fresh air. When we finally reached the top, we saw the very Tianchi—huge and pure like jade, shining like a huge diamond under the sunlight. Locals, future visitors, and wildlife all benefit, because without the littering ban and construction limits the jade-blue water could be spoiled by plastic bottles and noisy hotels. As soon as I saw Tianchi, all the sweat from the climbing was worth it, and that feeling made me respect this concrete protection law even more.",
      "sampleZh": "我支持景区禁扔垃圾与禁私搭乱建的保护法；在长白山听讲解后更理解天池之美，登顶时一切汗水都值得。"
    },
    {
      "id": 7,
      "title": "包含动物的故事或书",
      "q": "Describe a story/book with animals in it",
      "cuePoints": [
        "What animals are in it",
        "What the story/book is about",
        "Why you read the story/book",
        "And explain what you think of this story/book"
      ],
      "tag": "新增",
      "recentCount": 2324,
      "heatRank": 7,
      "heatLevel": "star2",
      "openingEn": "The children's book I want to mention is a gentle adventure about a teddy bear, and I read it because it came with a real gift from my best friend.",
      "openingZh": "我想提的童书是关于泰迪熊的温暖冒险，我读它是因为最好的朋友把它连同礼物一起送给我。",
      "materialId": "bear",
      "materialHint": "朋友送Jellycat泰迪熊时附赠熊主角图画书；软毛红丝带、高考压力时抱熊平静；书与玩偶互相呼应。",
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "The children's book I want to mention is a gentle adventure about a teddy bear, and I read it because it came with a real gift from my best friend. When I was in primary school, my best friend gave me a stuffed teddy bear from Jellycat for my birthday, and she also slipped a small picture book into the box. The bear in the story looks almost the same: small and brown, with soft fur and a red ribbon around its neck, traveling through forests to comfort a lonely child. I read it again and again before bed, especially later when stress grew. I still remember before the college entrance exam, I was so stressed that I couldn't fall asleep; I held the bear in my arms, thought of the story's calm ending, and somehow felt calmer and managed to sleep better. Since then, whenever I feel nervous or upset, I hug the bear and reread a few pages. The book is simple, but it has been with me during many important moments, so both the story and the toy really feel like an old friend.",
      "sampleZh": "好友送Jellycat并附赠熊冒险图画书；高考前抱熊读故事更平静，它像老朋友一样陪伴我。"
    },
    {
      "id": 8,
      "title": "很久没收到回复的信息",
      "q": "Describe a time when you sent a message or an email to someone but received no reply for a long time",
      "cuePoints": [
        "Who you sent it to",
        "What the message/email was about",
        "Whether you finally received the reply",
        "And explain how you felt about the experience"
      ],
      "tag": "新增",
      "recentCount": 2093,
      "heatRank": 8,
      "heatLevel": "star2",
      "openingEn": "A few months ago I sent Yumeng a long message about my future plans and then waited far longer than I expected for a reply.",
      "openingZh": "几个月前我给雨萌发了一条关于未来计划的长消息，结果等回复比预想久得多。",
      "materialId": "yumeng",
      "materialHint": "消息内容是考研/工作纠结；她后来解释在忙申请；见面时校园倾听并给出建议；收尾感激。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "A few months ago I sent Yumeng a long message about my future plans and then waited far longer than I expected for a reply. Yumeng is one of my most important friends. We grew up in the same neighborhood, so I usually get answers quickly, which made the silence feel strange. The message was about a crossroads in my third year at university: whether to pursue a master's degree or start working after graduation. I felt quite at a loss and poured everything into that text. For nearly a week there was no reply, and I started worrying that I had bothered her. Finally she called and explained she had been buried in her own applications; then we met and walked around the campus, and she listened very patiently. She said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life,\" and \"Your passion is your best teacher. Just go for it.\" I did receive a warm reply in the end, and although the wait was uncomfortable, her words gave me so much strength. I still appreciate her wise advice to this day.",
      "sampleZh": "给雨萌发长消息久等未回；见面后她倾听并鼓励我；等待难受但最终感激她的建议。"
    },
    {
      "id": 9,
      "title": "名人出演的广告",
      "q": "Describe an advertisement with a famous person in it",
      "cuePoints": [
        "Who the person is",
        "Where you can see it",
        "What the advertisement is about",
        "And explain how you feel about the advertisement"
      ],
      "tag": "新增",
      "recentCount": 1883,
      "heatRank": 9,
      "heatLevel": "star1",
      "openingEn": "The advertisement that sticks in my mind stars the famous table tennis player Sun Yingsha promoting a sports drink.",
      "openingZh": "我印象最深的广告是乒乓球运动员孙颖莎代言的运动饮料。",
      "materialId": "sun",
      "materialHint": "孙颖莎巴黎奥运混双夺金后的热度；广告里酒窝笑容与贴纸风在社交媒体传播。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "The advertisement that sticks in my mind stars the famous table tennis player Sun Yingsha promoting a sports drink. I think she is probably the most popular one in China right now, especially after she played mixed doubles with Wang Chuqin at the Paris Olympic Games and won the gold medal under enormous pressure. You can see the ad on subway screens, short-video apps, and even on stickers people share. In the commercial she smiles with her adorable dimples and chubby cheeks, then finishes a training rally and drinks the product. What makes it clever is that fans have made lots of stickers out of her image, and people often use them on social media to lighten the mood in a conversation, so the brand spreads naturally. I like the advertisement because it feels energetic rather than fake, and it reminds me why she became extremely popular in China after the Olympics.",
      "sampleZh": "孙颖莎运动饮料广告常见于地铁与短视频；巴黎奥运夺金后她极受欢迎，酒窝与贴纸在社交媒体活跃气氛。"
    },
    {
      "id": 10,
      "title": "拥有成功商业的人",
      "q": "Describe a person you know who has a successful business",
      "cuePoints": [
        "Who this person is",
        "How you got to know him/her",
        "Why and how he/she started the business",
        "What business he/she does",
        "And explain why you think the business is successful"
      ],
      "tag": "新增",
      "recentCount": 1869,
      "heatRank": 10,
      "heatLevel": "star1",
      "openingEn": "The successful business owner I know best is my aunt, who runs a small boutique that sells carefully chosen soft toys and gifts.",
      "openingZh": "我最熟悉的成功生意人是姨妈，她经营一家精选毛绒玩具与礼品的小店。",
      "materialId": "bear",
      "materialIds": [
        "bear",
        "basketball"
      ],
      "materialHint": "姨妈开礼品店主打Jellycat泰迪熊；软毛红丝带与高考季安慰属性带来回头客。男生版可改体育用品店。",
      "materialHintById": {
        "bear": "姨妈开礼品店主打Jellycat泰迪熊；软毛红丝带、高考季安慰属性带来回头客，说明生意成功。",
        "basketball": "叔叔开体育用品店，主打手感好的篮球；高考前学生来买球投篮减压，口碑带来成功。"
      },
      "openingById": {
        "bear": {
          "en": "The successful business owner I know best is my aunt, who runs a small boutique that sells carefully chosen soft toys and gifts.",
          "zh": "我最熟悉的成功生意人是姨妈，她经营一家精选毛绒玩具与礼品的小店。"
        },
        "basketball": {
          "en": "The successful business owner I know best is my uncle, who runs a compact sports shop that sells quality balls and training gear.",
          "zh": "我最熟悉的成功生意人是叔叔，他经营一家卖优质球类与训练装备的小体育店。"
        }
      },
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "The successful business owner I know best is my aunt, who runs a small boutique that sells carefully chosen soft toys and gifts. I got to know the shop simply because she is family, and I often helped her unpack boxes during school holidays. She started the business after noticing how many young people wanted comforting gifts during stressful exam seasons. Her best-selling item is a stuffed teddy bear from Jellycat: small and brown, with very soft fur and a red ribbon around its neck. Customers tell her that before the college entrance exam they feel calmer when they hold it, and that it really feels like an old friend, which creates loyal repeat buyers. I think the business is successful because she understands emotion, not only price: the shop is tidy, advice is patient, and people leave smiling with a gift that actually matters. That mix of warmth and professionalism keeps the boutique busy every weekend.",
      "sampleZh": "姨妈开礼品店主打Jellycat小熊，高考季安慰属性带来回头客，生意成功。",
      "sampleEnById": {
        "bear": "The successful business owner I know best is my aunt, who runs a small boutique that sells carefully chosen soft toys and gifts. I got to know the shop simply because she is family, and I often helped her unpack boxes during school holidays. She started the business after noticing how many young people wanted comforting gifts during stressful exam seasons. Her best-selling item is a stuffed teddy bear from Jellycat: small and brown, with very soft fur and a red ribbon around its neck. Customers tell her that before the college entrance exam they feel calmer when they hold it, and that it really feels like an old friend, which creates loyal repeat buyers. I think the business is successful because she understands emotion, not only price: the shop is tidy, advice is patient, and people leave smiling with a gift that actually matters. That mix of warmth and professionalism keeps the boutique busy every weekend.",
        "basketball": "The successful business owner I know best is my uncle, who runs a compact sports shop that sells quality balls and training gear. I got to know the place because he is family, and I used to sweep the floor there after school. He started the business when he saw students nearby needing a healthy way to release pressure. His signature product is a solid orange basketball with a nice grip, similar to the one my father gave me years ago. Many customers say that before the college entrance exam they shot some hoops and felt calmer and their minds became much clearer, so the ball feels like an old friend. I think the business succeeds because he recommends gear patiently, prices fairly, and builds a community of regular players who keep coming back. Weekend evenings the shop is always lively with people comparing bounce and grip."
      },
      "sampleZhById": {
        "bear": "姨妈开礼品店主打Jellycat小熊，高考季安慰属性带来回头客，生意成功。",
        "basketball": "叔叔开体育店主打手感好的篮球，学生投篮减压成回头客，生意成功。"
      },
      "materialOptions": [
        "bear",
        "basketball"
      ]
    },
    {
      "id": 11,
      "title": "推荐旅行过的地方",
      "q": "Describe a place you have travelled to that you would like to recommend to others",
      "cuePoints": [
        "What it is",
        "Where it is",
        "What you saw and did there",
        "And explain why you would like to recommend it to others"
      ],
      "tag": "新增",
      "recentCount": 1813,
      "heatRank": 11,
      "heatLevel": "star1",
      "openingEn": "If I could recommend only one trip, it would be Changbai Mountain and its famous Tianchi lake.",
      "openingZh": "如果只能推荐一次旅行，我会选长白山和著名的天池。",
      "materialId": "tianchi",
      "materialHint": "按天池素材讲东北未开发自然、极长阶梯、碧玉般湖面；推荐理由落在登顶震撼。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "If I could recommend only one trip, it would be Changbai Mountain and its famous Tianchi lake. It is a remote area in the northeast part of China which is famous for its untouched nature and a lake located at the peak of a hill called Tianchi, which means the pond of heaven. When I went there, the first challenge was an extremely long staircase leading to the hilltop. The climb was tough, but the scenery was truly breathtaking: you can overlook the entire mountain, see the clearest blue sky you've ever seen, and breathe extremely fresh air. When we finally reached the top, the lake looked huge and pure like jade, shining like a huge diamond under the sunlight. I would recommend it because the view is unforgettable, and as soon as I saw Tianchi, all the sweat from the climbing was worth it. Friends who need a break from city noise would love this place.",
      "sampleZh": "推荐长白山天池：东北未开发自然、极长阶梯与清澈湖面；登顶那一刻所有汗水都值得。"
    },
    {
      "id": 12,
      "title": "去过的无聊地方",
      "q": "Describe a boring place",
      "cuePoints": [
        "Where it is",
        "Who you went there with",
        "What you did there",
        "And explain why you think it is a boring place"
      ],
      "tag": "新增",
      "recentCount": 1638,
      "heatRank": 12,
      "heatLevel": "star1",
      "openingEn": "The most boring place I visited recently was a quiet library corner where I tried to force myself to study all weekend.",
      "openingZh": "我最近去过最无聊的地方，是周末硬逼自己待着的安静图书馆角落。",
      "materialId": "badminton",
      "materialHint": "对比：图书馆枯燥闷坐 vs 后来去球场打羽毛球；组队、挥拍忘压反衬无聊。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "The most boring place I visited recently was a quiet library corner where I tried to force myself to study all weekend. I went there with a classmate because we were occupied with applying for master's programs and studying English, and we thought sitting still for ten hours would help. What we did was stare at the same pages, check phones secretly, and whisper complaints. Nothing moved, nothing changed, and I felt my brain freeze. That boredom actually pushed me to leave and start to play badminton later that afternoon. At the court I could team up with strangers, hear the sound of the racket and the wind, and suddenly feel alive again. Compared with swinging my racket and becoming more outgoing with sports friends, that library corner was painfully dull. I call it boring not because libraries are bad, but because forcing focus without movement made the pressure worse instead of helping me forget it for a while.",
      "sampleZh": "周末图书馆硬坐学习极无聊；后来去打羽毛球组队、挥拍，才感到清醒，反衬那个角落多么沉闷。"
    },
    {
      "id": 13,
      "title": "遇到的科技问题",
      "q": "Describe a challenging technological problem you faced",
      "cuePoints": [
        "What the problem was",
        "When and where you faced it",
        "How challenging it was",
        "And explain how you solved it"
      ],
      "tag": "新增",
      "recentCount": 1575,
      "heatRank": 13,
      "heatLevel": "star1",
      "openingEn": "The toughest tech problem I faced was getting my new robot vacuum to map the house properly while two cats kept confusing it.",
      "openingZh": "我遇到最棘手的科技问题，是新扫地机器人在两只猫干扰下无法正确建图。",
      "materialId": "robot",
      "materialHint": "猫毛满地买扫地机；首次连App建图失败；最终设禁区与定时清扫，省时收尾。",
      "endingTip": "它帮我节省大量时间，打扫不再是问题",
      "sampleEn": "The toughest tech problem I faced was getting my new robot vacuum to map the house properly while two cats kept confusing it. I bought the robot vacuum cleaner several years ago mainly because I have two cats at home and there is cat fur all over the place, yet I was busy with studies and had no time to tidy. The first night I tried to connect it to an app on my phone, but the mapping kept failing: the cats sat on the robot, blocked doorways, and made it restart again and again. It was more challenging than I expected because every failed loop left fur in new corners. I solved it by closing the cats in another room for twenty minutes, updating the firmware, and setting no-go zones around their bowls. After that, a few clicks in the app were enough for daily cleaning, and the device could even reach corners I could not clean by hand. Thanks to that fix, cleaning is no longer an issue and it saves me so much time.",
      "sampleZh": "因两只猫到处是毛买了扫地机，首次连App建图被猫干扰失败；隔离猫咪并设禁区后终于省下大量打扫时间。"
    },
    {
      "id": 14,
      "title": "想从事医疗行业的人",
      "q": "Describe a person you know who would like to choose a career in the medical field (e.g. a doctor, a nurse)",
      "cuePoints": [
        "When you knew him/her",
        "When he/she started to think about that",
        "What he/she would like to do",
        "And explain why he/she would like to choose this career"
      ],
      "tag": "新增",
      "recentCount": 1568,
      "heatRank": 14,
      "heatLevel": "star1",
      "openingEn": "The person closest to a future medical career in my life is my friend Yumeng, who has always been the one who cares for others first.",
      "openingZh": "我身边最接近未来医疗职业的人是雨萌，她总是最先关心别人。",
      "materialId": "yumeng",
      "materialHint": "雨萌聪明乐观、愿意倾听支持；把她对他人的耐心与“想一生做什么”的志向连到护理/医学方向。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "The person closest to a future medical career in my life is my friend Yumeng, who has always been the one who cares for others first. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so I have known her for most of my life. She started thinking seriously about nursing during our third year at university, when many of us faced crossroads about master's degrees or jobs. She is really smart and optimistic, and whether in study or personal life she is always willing to listen and support people. I still remember we walked around the campus while she listened very patiently to my worries, then told me to think about what I want to do for the rest of my life. That same empathy is why she wants to become a nurse: she believes calm words and careful care can give patients strength the way her advice gave me strength. Her passion feels genuine, and I still appreciate how wisely she connects caring with a real career path.",
      "sampleZh": "雨萌从小同街区长大，大学时认真考虑护理；她总是耐心倾听支持他人，这份共情让她想用专业照顾病人。"
    },
    {
      "id": 15,
      "title": "喜欢或不喜欢的高建筑",
      "q": "Describe a tall building you like or dislike",
      "cuePoints": [
        "What it is used for",
        "Where it is",
        "What it looks like",
        "And explain why you like/dislike it"
      ],
      "tag": "新增",
      "recentCount": 1540,
      "heatRank": 15,
      "heatLevel": "star1",
      "openingEn": "The tall building I like most is not a glass tower in a city center, but the observation structure near Tianchi on Changbai Mountain.",
      "openingZh": "我最喜欢的高建筑不是市中心玻璃楼，而是长白山天池附近的观景建筑。",
      "materialId": "tianchi",
      "materialHint": "把山顶观景台/高阶梯建筑当作tall building；登顶后俯瞰山脉与天池，解释为何喜欢。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "The tall building I like most is not a glass tower in a city center, but the observation structure near Tianchi on Changbai Mountain. It is used for visitors to rest and look out after climbing, and it sits in a remote area in the northeast part of China famous for untouched nature. From below it looks simple, almost plain, but reaching it means walking an extremely long staircase that leads toward the hilltop. When I finally stood there, the scenery was truly breathtaking: I could overlook the entire mountain, see the clearest blue sky, and feel extremely fresh air. Beyond the platform, Tianchi appeared like pure jade, shining like a huge diamond under the sunlight. I like this tall building because its height serves nature rather than blocking it, and as soon as I saw the pond of heaven, all the sweat from the climbing was worth it.",
      "sampleZh": "喜欢天池附近观景高台：需爬极长阶梯，俯瞰山脉与碧玉般天池；高度服务于自然，登顶汗水都值得。"
    },
    {
      "id": 16,
      "title": "发小",
      "q": "Describe a friend from your childhood",
      "cuePoints": [
        "Who he/she is",
        "Where and how you met each other",
        "What you often did together",
        "And explain what made you like him/her"
      ],
      "tag": "新增",
      "recentCount": 1512,
      "heatRank": 16,
      "heatLevel": "star1",
      "openingEn": "My childhood friend is still the same person I trust most today: Yumeng.",
      "openingZh": "我的发小至今仍是我最信任的人：雨萌。",
      "materialId": "yumeng",
      "materialHint": "同街区同学校长大；一起玩到大学仍倾听支持；喜欢她因聪明乐观与睿智建议。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "My childhood friend is still the same person I trust most today: Yumeng. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so we basically met by living next to each other's lives. As kids we rode bikes after class, shared snacks, and studied side by side; later we still walked around the campus when life got complicated. I like her because she is really smart and optimistic, and whether in study or personal life she is always willing to listen and support me. When I was in my third year at university and faced a crossroads about a master's degree or work, she listened very patiently and said, \"Your passion is your best teacher. Just go for it.\" Those childhood roots plus adult wisdom are rare. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "雨萌是同街区同学校的发小，一起长大到大学仍互相支持；她聪明乐观，关键建议给了我力量。"
    },
    {
      "id": 17,
      "title": "有趣视频",
      "q": "Describe an interesting video",
      "cuePoints": [
        "When and where you watched it",
        "What it is about",
        "Why you watched it",
        "And explain how you feel about it"
      ],
      "tag": "新增",
      "recentCount": 1498,
      "heatRank": 17,
      "heatLevel": "star1",
      "openingEn": "Last weekend on my phone I watched a short clip that made me laugh and then think: a highlight reel from the movie Xialuotefannao.",
      "openingZh": "上周末我在手机上看了一段又好笑又引人思考的短视频：《夏洛特烦恼》的精彩剪辑。",
      "materialId": "movie",
      "materialHint": "用夏洛特烦恼时间旅行片段作有趣视频；沈腾马丽、追秋雅、梦醒悟到爱最宝贵。",
      "endingTip": "领悟到爱才是生命中最宝贵的东西",
      "sampleEn": "Last weekend on my phone I watched a short clip that made me laugh and then think: a highlight reel from the movie Xialuotefannao. I watched it at home before sleep because a friend said the editing was hilarious. The video is about a man who can travel in time, starring Shen Teng and Ma Li, China's most famous comedians and the funniest couple on screen. In a few minutes it shows how Xialuo goes back to high school, chooses a different path to pursue his dream girl Qiuya, becomes a famous musician, and then faces a cruel twist. I watched it mainly for comedy, yet the ending still hit me: when everything turns out to be a long dream, he realizes that love was the most valuable thing in his life. That mix of jokes and meaning is why I find the video interesting, not just entertaining.",
      "sampleZh": "手机上看《夏洛特烦恼》剪辑：时间旅行、沈腾马丽搞笑；笑完仍悟到爱才是最宝贵的东西。"
    },
    {
      "id": 18,
      "title": "喜欢在家/花园种植物的人",
      "q": "Describe a person who loves to grow plants (e.g. vegetables, flowers) at home or in the garden",
      "cuePoints": [
        "Who this person is",
        "What plants he/she grows",
        "How he/she grows the plants",
        "And explain why he/she loves growing plants"
      ],
      "tag": "新增",
      "recentCount": 1484,
      "heatRank": 18,
      "heatLevel": "star1",
      "openingEn": "My uncle is the plant lover in our family, and his hobby grew even stronger after a trip to Changbai Mountain.",
      "openingZh": "叔叔是家里的植物爱好者，去长白山之后这份爱好更强了。",
      "materialId": "tianchi",
      "materialHint": "叔叔爱自然：阳台种菜养花；灵感来自天池未开发自然与清新空气；种植是把自然感带回家。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "My uncle is the plant lover in our family, and his hobby grew even stronger after a trip to Changbai Mountain. He grows herbs, tomatoes, and a few wildflowers on the balcony, watering them every morning and talking to them as if they were quiet friends. The way he grows plants is careful and patient: he checks sunlight, mixes soil himself, and refuses chemical sprays. Why does he love it? After visiting a remote area in the northeast famous for untouched nature and Tianchi, the pond of heaven, he said city air felt heavy. He still remembers the extremely long staircase, the breathtaking clear blue sky, and the lake shining like a huge diamond. Growing plants is his way of keeping a piece of that fresh world at home. Whenever the seedlings turn green, he smiles the same way he did when he said all the sweat from the climbing was worth it.",
      "sampleZh": "叔叔阳台种菜养花，灵感来自长白山未开发自然与天池清新空气；种植是把那份自然感带回家。"
    },
    {
      "id": 19,
      "title": "特别场合的食物",
      "q": "Describe a food that people eat on special occasions/events",
      "cuePoints": [
        "What it is",
        "What the special event/occasion is",
        "How it is cooked/made",
        "And explain why people eat it on that special occasion/event"
      ],
      "tag": "新增",
      "recentCount": 1309,
      "heatRank": 19,
      "heatLevel": "star1",
      "openingEn": "The special-occasion food I think of first is homemade birthday cake, especially the one we shared when I received my Jellycat bear.",
      "openingZh": "我首先想到的特别场合食物是自制生日蛋糕，尤其是收到Jellycat小熊那天一起吃的那块。",
      "materialId": "bear",
      "materialHint": "生日场合吃蛋糕；当天好友送Jellycat泰迪熊；软毛红丝带与蛋糕一起成为珍贵回忆。",
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "The special-occasion food I think of first is homemade birthday cake, especially the one we shared when I received my Jellycat bear. In my family we eat this soft cream cake on birthdays and a few graduation days. My mother bakes a simple sponge, whips cream, and lets us decorate the top with fruit. That particular birthday stands out because my best friend gave me a stuffed teddy bear from Jellycat along with the cake: it was small and brown, with soft fur and a red ribbon around its neck. We cut the cake, laughed, and I hugged the bear between bites. People eat cake on birthdays to mark care and celebration, and for me the sweetness is tied to that gift. Years later, before the college entrance exam when I felt calmer holding the bear, I still remembered the cake-and-bear birthday. The toy feels like an old friend, and the cake is the taste of that beginning.",
      "sampleZh": "生日吃自制蛋糕；那天好友还送了Jellycat小熊。蛋糕的甜蜜与这只像老朋友的熊连在一起。"
    },
    {
      "id": 20,
      "title": "喜欢的现场体育赛事",
      "q": "Describe a live sports event you watched and liked",
      "cuePoints": [
        "What it was",
        "When and where you watched it",
        "Who you watched it with",
        "And explain why you liked it"
      ],
      "tag": "新增",
      "recentCount": 1309,
      "heatRank": 20,
      "heatLevel": "star1",
      "openingEn": "The live sports event I enjoyed most was watching Sun Yingsha play on a big screen with a noisy crowd around me.",
      "openingZh": "我最喜欢的现场体育体验，是和人群一起在大屏前看孙颖莎比赛。",
      "materialId": "sun",
      "materialHint": "体育酒吧/奥运转播现场气氛；混双夺金高压表现；酒窝与欢呼说明为何喜欢。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "The live sports event I enjoyed most was watching Sun Yingsha play on a big screen with a noisy crowd around me. It was during the Paris Olympic Games period, in a sports bar downtown, and I went with two classmates. Although we were not inside the arena, the room felt live: people shouted every rally. She is a famous table tennis player and probably the most popular one in China right now. That night she played mixed doubles with Wang Chuqin and gave her best performance under enormous pressure before winning the gold medal. I liked it because the tension was real, yet when she smiled you could see her adorable dimples and chubby cheeks, and strangers high-fived like old friends. Afterward fans shared stickers of her image on social media to lighten the mood. The mix of excellence and warmth made the live atmosphere unforgettable.",
      "sampleZh": "在体育酒吧和大屏前看孙颖莎巴黎奥运混双夺金，气氛热烈；她的实力与可爱酒窝让现场难忘。"
    },
    {
      "id": 21,
      "title": "擅长做计划的人",
      "q": "Describe a person who makes plans a lot and is good at planning",
      "cuePoints": [
        "Who he/she is",
        "How you knew him/her",
        "What plans he/she makes",
        "And explain how you feel about this person"
      ],
      "tag": "沿用",
      "recentCount": 1218,
      "heatRank": 21,
      "heatLevel": "star1",
      "openingEn": "When I need a planning expert, I always think of Yumeng first.",
      "openingZh": "需要计划高手时，我总是先想到雨萌。",
      "materialId": "yumeng",
      "materialHint": "雨萌把考研/工作抉择规划清晰；校园散步倾听后给出条理建议；你佩服她的规划力。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "When I need a planning expert, I always think of Yumeng first. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so I have seen how organized she is for years. She is really smart and optimistic, and she makes plans for study timelines, internship goals, and even weekend reading lists without sounding rigid. The clearest example was when I was in my third year at university and faced a crossroads: whether to pursue a master's degree or start working after graduation. I felt quite at a loss, so we walked around the campus, she listened very patiently, then helped me map options instead of panicking. She said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life,\" and broke the decision into steps I could actually follow, from language tests to application deadlines. I feel lucky to know someone who plans with both logic and heart, because her structure turned my anxiety into action. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "雨萌从小一起长大，擅长把人生抉择拆成可执行计划；校园散步中帮我理清读硕路径，我很感激。"
    },
    {
      "id": 22,
      "title": "去过且喜欢的城市",
      "q": "Describe a city you enjoyed visiting",
      "cuePoints": [
        "Where it is",
        "When you visited it",
        "How long you stayed there",
        "What you did there",
        "And explain why you enjoyed visiting it"
      ],
      "tag": "沿用",
      "recentCount": 1218,
      "heatRank": 22,
      "heatLevel": "star1",
      "openingEn": "The city trip I enjoyed most was a short stay in Yanji as the gateway before climbing Changbai Mountain.",
      "openingZh": "我最喜欢的城市之旅，是登长白山前在延吉作门户的短暂停留。",
      "materialId": "tianchi",
      "materialHint": "延吉/长春作门户城市：停留一两天，再去天池；城市本身因通往未开发自然而难忘。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "The city trip I enjoyed most was a short stay in Yanji as the gateway before climbing Changbai Mountain. Yanji sits in the northeast, and I visited last summer for two nights with friends. We tried local food, walked lively streets, and prepared gear for the mountain the next day. What made the city special was the contrast: busy lights at night, then a journey into a remote area famous for untouched nature and Tianchi, the pond of heaven. From the city we headed to an extremely long staircase, breathed fresh air under a clear blue sky, and finally saw the lake shining like a huge diamond. I enjoyed Yanji because it was warm and practical, and it led to a view where all the sweat from the climbing was worth it. Without that city stop, the mountain adventure would have felt rushed.",
      "sampleZh": "喜欢延吉作门户城市：停留两晚尝美食，再去天池；城市因通往未开发自然而更难忘。"
    },
    {
      "id": 23,
      "title": "近期看过且享受的电影",
      "q": "Describe a movie you watched and enjoyed recently",
      "cuePoints": [
        "When and where you watched it",
        "Who you watched it with",
        "What it was about",
        "And explain why you watched this movie"
      ],
      "tag": "沿用",
      "recentCount": 1113,
      "heatRank": 23,
      "heatLevel": "star1",
      "openingEn": "I am a big fan of movies, and the most enjoyable one I watched recently is the Chinese comedy Xialuotefannao.",
      "openingZh": "我是影迷，最近最享受的是中国喜剧《夏洛特烦恼》。",
      "materialId": "movie",
      "materialHint": "直接套用夏洛特烦恼：沈腾马丽、时间旅行、追秋雅、梦醒悟爱。",
      "endingTip": "领悟到爱才是生命中最宝贵的东西",
      "sampleEn": "I am a big fan of movies, and the most enjoyable one I watched recently is the Chinese comedy Xialuotefannao. I watched it at home on a Friday night with my roommate, mainly because we needed something funny after a stressful week. Xialuotefannao is a Chinese movie about a man who can travel in time, starring Shen Teng and Ma Li, who are the funniest couple and among China's most famous comedians. In the story, Xialuo goes back to his high school days and chooses a different life path to pursue his dream girl Qiuya instead of his real wife Ma Li. After ten years he becomes a famous musician and marries Qiuya, until a cruel twist teaches him what truly matters. I watched it for laughter, but I stayed for the ending: he realizes that love was the most valuable thing in his life, and that all of this was a long dream. That balance of comedy and meaning is why I enjoyed it so much.",
      "sampleZh": "周五在家和室友看《夏洛特烦恼》：沈腾马丽时间旅行喜剧；笑完悟到爱才是最宝贵的。"
    },
    {
      "id": 24,
      "title": "喜欢拜访但不想住的家",
      "q": "Describe a home that you like to visit but do not want to live in",
      "cuePoints": [
        "Where it is",
        "What it is like",
        "Why you like to visit it",
        "And explain why you would not like to live there"
      ],
      "tag": "新增",
      "recentCount": 1085,
      "heatRank": 24,
      "heatLevel": "star1",
      "openingEn": "There is a mountain lodge near Changbai Mountain that I love to visit for a weekend but would never choose as a permanent home.",
      "openingZh": "长白山附近有一座山间小屋，我喜欢周末去，但绝不想长期住在那里。",
      "materialId": "tianchi",
      "materialHint": "山间小屋：拜访可看天池未开发自然；不想住因偏远、阶梯辛苦、生活不便。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "There is a mountain lodge near Changbai Mountain that I love to visit for a weekend but would never choose as a permanent home. It sits in a remote area in the northeast part of China, close to untouched nature and the path toward Tianchi, the pond of heaven. The lodge is wooden, quiet, and filled with fresh air; from the window you can see mist over the hills. I like to visit because after an extremely long staircase climb, the scenery is breathtaking, the sky is clear blue, and the lake shines like a huge diamond. As soon as I see Tianchi, all the sweat is worth it, and returning to the lodge for hot soup feels perfect. Still, I would not live there: shops are far, winters are harsh, and daily commuting would be exhausting. It is a wonderful guest house for nature, not a practical forever home.",
      "sampleZh": "喜欢拜访天池附近山间小屋看未开发自然，但不想住：太偏远、冬天难熬，只适合周末充电。"
    },
    {
      "id": 25,
      "title": "早起经历",
      "q": "Describe a time when you got up early",
      "cuePoints": [
        "When it was",
        "What you did",
        "Why you got up early",
        "And how you felt about it"
      ],
      "tag": "新增",
      "recentCount": 1071,
      "heatRank": 25,
      "heatLevel": "star1",
      "openingEn": "One early morning I still remember clearly was when I got up at six to claim a badminton court before the rush.",
      "openingZh": "我仍清楚记得那天六点起床，只为赶在高峰前订下羽毛球场。",
      "materialId": "badminton",
      "materialHint": "早起为打球：申请压力大需要运动；清晨组队挥拍，身心专注忘压。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "One early morning I still remember clearly was when I got up at six to claim a badminton court before the rush. It was during a month when I was occupied with applying for master's programs and studying English, so I always got tired and could not focus well. Friends advised me to exercise, and I had started to play badminton, but evening courts were always full. That is why I got up early: to practice while the hall was quiet. I met two regular partners, we warmed up, and soon I was swinging my racket with only its sound and the wind in my ears. The early start felt hard at first, yet it let me focus solely on my mind and body and forget the pressure from my studies for a while. By breakfast I felt more outgoing and awake than after any late-night cramming session.",
      "sampleZh": "申请季六点起床抢球场；清晨挥拍只听见球拍与风声，能暂时忘却学业压力，反而更清醒。"
    },
    {
      "id": 26,
      "title": "在团队中工作",
      "q": "Describe a time when you worked in a group",
      "cuePoints": [
        "What you did",
        "Who you worked with",
        "What problems you faced",
        "And explain why you worked in the group"
      ],
      "tag": "新增",
      "recentCount": 1071,
      "heatRank": 26,
      "heatLevel": "star1",
      "openingEn": "A recent group experience that taught me a lot was organizing weekend badminton matches with people I barely knew.",
      "openingZh": "最近一次很有收获的团队经历，是和不熟的人一起组织周末羽毛球局。",
      "materialId": "badminton",
      "materialHint": "球场与陌生人组队即团队工作；协调时间、水平差异；为减压与交友而合作。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "A recent group experience that taught me a lot was organizing weekend badminton matches with people I barely knew. After I started to play badminton to escape the stress of applying for master's programs and studying English, I often team up with strangers at the court. One month we formed a small group of six to book courts, rotate partners, and share shuttlecocks. The problem was obvious: different skill levels and busy schedules caused arguments about timing. We solved it by making a simple chat plan and letting stronger players coach newcomers for ten minutes first. I worked in that group because badminton requires a partner, and cooperation made practice possible. Soon we became more outgoing friends who meet every weekend. When I swing my racket there, I hear only its sound and the wind, and I can forget study pressure for a while—something I could never achieve alone at a desk.",
      "sampleZh": "为减压在球场与陌生人组队约球，协调时间与水平差异；团队合作让我更外向，挥拍时可忘却压力。"
    },
    {
      "id": 27,
      "title": "想拥有的科技产品",
      "q": "Describe a piece of technology (not a phone) that you would like to own",
      "cuePoints": [
        "What it is",
        "How much it costs",
        "How you knew it",
        "And explain why you would like to own it"
      ],
      "tag": "沿用",
      "recentCount": 1008,
      "heatRank": 27,
      "heatLevel": "star1",
      "openingEn": "The piece of technology I most want to own is a newer, quieter robot vacuum cleaner with better app control.",
      "openingZh": "我最想拥有的科技产品是一台更安静、App控制更好的新款扫地机器人。",
      "materialId": "robot",
      "materialHint": "想要更强扫地机：两只猫猫毛、连App几键搞定、省时；可提价格与熟人推荐。",
      "endingTip": "它帮我节省大量时间，打扫不再是问题",
      "sampleEn": "The piece of technology I most want to own is a newer, quieter robot vacuum cleaner with better app control. The model I am eyeing costs around three thousand yuan, which is not cheap for a student, but friends say it lasts for years. I first knew this kind of device when I bought a basic robot vacuum several years ago because I have two cats and cat fur is everywhere, while I was busy with studies. The old one already helps: I connect it to an app, tap a few clicks, and it cleans corners I cannot reach by hand. I want a better version because it maps faster, avoids cables smarter, and runs more quietly at night. With exams and part-time work, time matters. If cleaning is no longer an issue and the machine saves me so much time, that cost feels reasonable for daily peace.",
      "sampleZh": "想买更强扫地机器人：家里两只猫毛多，连App几键清理角落；虽然贵，但能节省大量时间。"
    },
    {
      "id": 28,
      "title": "想见的名人",
      "q": "Describe a famous person you would like to meet",
      "cuePoints": [
        "Who he/she is",
        "How you knew him/her",
        "How/where you would like to meet him/her",
        "And explain why you would like to meet him/her"
      ],
      "tag": "沿用",
      "recentCount": 994,
      "heatRank": 28,
      "heatLevel": "star0",
      "openingEn": "If I could meet one famous person, I would choose the table tennis star Sun Yingsha.",
      "openingZh": "如果能见一位名人，我会选乒乓球明星孙颖莎。",
      "materialId": "sun",
      "materialHint": "想见孙颖莎：巴黎奥运混双夺金、酒窝亲和力；想在赛后签名会或训练馆见面。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "If I could meet one famous person, I would choose the table tennis star Sun Yingsha. She is a famous table tennis player and probably the most popular one in China right now. I knew her through Olympic broadcasts, especially when she played mixed doubles with Wang Chuqin at the Paris Olympic Games and won gold under enormous pressure. I would love to meet her at a post-match fans' event or near the training hall, somewhere casual enough to say thank you without freezing. Why her? She is young, talented, and still approachable: people are fascinated by her adorable dimples and chubby cheeks, and fans even make stickers of her image to lighten the mood on social media. Meeting her would let me see how she stays calm under pressure, which is a skill I need in my own exams and applications.",
      "sampleZh": "想见孙颖莎：巴黎奥运混双夺金、酒窝亲和；想在赛后活动见面，学习她高压下的冷静。"
    },
    {
      "id": 29,
      "title": "当地新闻",
      "q": "Describe a piece of local news that people are interested in",
      "cuePoints": [
        "What it was about",
        "Where you saw/heard it",
        "Who was involved",
        "And explain why people were interested in it"
      ],
      "tag": "新增",
      "recentCount": 966,
      "heatRank": 29,
      "heatLevel": "star0",
      "openingEn": "The local news that got everyone talking last month was about a table tennis exhibition match featuring Sun Yingsha in our city.",
      "openingZh": "上个月全城热议的本地新闻，是孙颖莎将来我市参加乒乓球表演赛。",
      "materialId": "sun",
      "materialHint": "本地体育新闻：孙颖莎表演赛；人们因奥运金牌与可爱形象而关注。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "The local news that got everyone talking last month was about a table tennis exhibition match featuring Sun Yingsha in our city. I saw it first on a community WeChat account, then on local TV. The story involved city sports officials and the famous table tennis player Sun Yingsha, who is probably the most popular one in China right now after winning gold in mixed doubles with Wang Chuqin at the Paris Olympic Games under enormous pressure. People were interested because a world-class athlete rarely comes here, and fans love her adorable dimples and chubby cheeks as much as her skills. Overnight, stickers of her image flooded group chats to lighten the mood while tickets sold out. The news mixed pride, excitement, and a bit of celebrity gossip, which is why even classmates who never watch sports kept refreshing updates.",
      "sampleZh": "本地新闻说孙颖莎将来我市表演赛；人们因奥运金牌与可爱形象疯传，群聊贴纸刷屏。"
    },
    {
      "id": 30,
      "title": "重要决定",
      "q": "Describe an important decision that you made",
      "cuePoints": [
        "What the decision was",
        "How you made your decision",
        "What the results of the decision were",
        "And explain why it was important"
      ],
      "tag": "新增",
      "recentCount": 896,
      "heatRank": 30,
      "heatLevel": "star0",
      "openingEn": "The most important decision I made in university was to pursue a master's degree instead of rushing into a job.",
      "openingZh": "大学里我做过的最重要决定，是攻读硕士而不是匆忙工作。",
      "materialId": "yumeng",
      "materialHint": "决定过程：找雨萌聊、校园倾听、热情是最好的老师；结果读硕，决定重要因影响一生。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "The most important decision I made in university was to pursue a master's degree instead of rushing into a job. When I was in my third year, I faced that crossroads and felt quite at a loss, because family expectations and money worries pulled me toward work. I made the decision by talking with Yumeng, one of my most important friends. We grew up in the same neighborhood and went to the same school, so she knows how I think when I am scared. We walked around the campus, she listened very patiently, then said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it.\" She also reminded me, \"Your passion is your best teacher.\" The result is that I applied carefully, received offers, and now feel more aligned with my long-term goals instead of drifting. It was important because it shaped my next decade and taught me to choose with intention. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "大三决定读硕而非匆忙工作；雨萌校园倾听并鼓励我想一生想做什么；这个决定影响长远。"
    },
    {
      "id": 31,
      "title": "想颁布的新法律",
      "q": "Describe a new law you would like to introduce in your country",
      "cuePoints": [
        "What law it is",
        "What changes this law brings",
        "Whether this new law will be popular",
        "How you came up with the new law",
        "And explain how you feel about this new law"
      ],
      "tag": "新增",
      "recentCount": 868,
      "heatRank": 31,
      "heatLevel": "star0",
      "openingEn": "If I could introduce a new law, it would require stronger visitor limits and litter fines in fragile mountain reserves.",
      "openingZh": "如果能颁布新法，我会要求对脆弱山地保护区实行更严格的限流与乱扔垃圾罚款。",
      "materialId": "tianchi",
      "materialHint": "灵感来自天池：未开发自然易被破坏；法律限流禁垃圾；登顶震撼说明为何值得保护。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "If I could introduce a new law, it would require stronger visitor limits and litter fines in fragile mountain reserves. The law would change daily quotas, ban disposable plastics on trails, and fund clean-up teams. I think young travelers would support it, though some tour companies might complain at first. I came up with it after visiting Changbai Mountain, a remote area in the northeast famous for untouched nature and Tianchi, the pond of heaven. Climbing the extremely long staircase, I saw breathtaking views and a clear blue sky, but also tissues left by careless hikers. When the lake finally appeared like pure jade shining as a huge diamond, I realized places like this need legal teeth, not only slogans. I feel strongly positive about this law because as soon as I saw Tianchi, all the sweat was worth it, and that beauty should remain for the next generation.",
      "sampleZh": "想立山地保护区限流与反 litter 法；灵感来自天池未开发自然，登顶震撼让我更坚信该立法。"
    },
    {
      "id": 32,
      "title": "完美工作",
      "q": "Describe a perfect job you would like to have in the future",
      "cuePoints": [
        "What it is",
        "How you knew it",
        "What you need to learn to get this job",
        "And explain why you think it is a perfect job for you"
      ],
      "tag": "沿用",
      "recentCount": 847,
      "heatRank": 32,
      "heatLevel": "star0",
      "openingEn": "My idea of a perfect job is becoming a professional athlete, or at least working closely with elite sports teams.",
      "openingZh": "我认为的完美工作是成为职业运动员，或至少与顶尖运动队密切合作。",
      "materialId": "sun",
      "materialHint": "以孙颖莎为榜样：年轻才华、高压夺金、受欢迎；说明为何完美及需学习的抗压与技术。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "My idea of a perfect job is becoming a professional athlete, or at least working closely with elite sports teams. I knew this path by following the famous table tennis player Sun Yingsha, probably the most popular one in China right now. Just last year she played mixed doubles with Wang Chuqin at the Paris Olympic Games and gave her best performance under enormous pressure to win gold. To get near that world I would need advanced training, sports science knowledge, and mental coaching. Why is it perfect for me? I love clear goals, teamwork, and the honest feedback of winning or losing. Watching her stay sharp yet approachable—with adorable dimples that fans turn into stickers on social media to lighten the mood—shows that excellence can still feel human. That balance of grit and warmth is exactly the career energy I want.",
      "sampleZh": "完美工作是职业运动员路线；以孙颖莎高压夺金又亲和受欢迎为榜样，需要技术与心理训练。"
    },
    {
      "id": 33,
      "title": "安静的地方",
      "q": "Describe a quiet place you like to go",
      "cuePoints": [
        "Where it is",
        "How you knew it",
        "How often you go there",
        "What you do there",
        "And explain how you feel about the place"
      ],
      "tag": "沿用",
      "recentCount": 812,
      "heatRank": 33,
      "heatLevel": "star0",
      "openingEn": "When I need real quiet, I think of the trails around Tianchi rather than any cafe in town.",
      "openingZh": "需要真正安静时，我想的是天池周边步道，而不是城里任何咖啡馆。",
      "materialId": "tianchi",
      "materialHint": "天池周边：未开发自然、清新空气；偶去一次；静坐看湖，登顶值得收尾。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "When I need real quiet, I think of the trails around Tianchi rather than any cafe in town. It is in a remote area in the northeast part of China, famous for untouched nature and a lake called Tianchi, the pond of heaven. I knew it through a family trip, and I can only go there once every year or two because of the distance. What I do there is walk the extremely long staircase slowly, breathe the fresh air, and sit near the top looking at water that looks like pure jade. The scenery is breathtaking under a clear blue sky, and there is almost no traffic noise. I feel deeply restored in that quiet. As soon as I see the lake shining like a huge diamond, all the sweat from the climbing is worth it, and the silence feels richer than any city park.",
      "sampleZh": "安静之处是天池步道：一年难得去一次，爬极长阶梯后看碧玉般湖面，那份安静让一切汗水值得。"
    },
    {
      "id": 34,
      "title": "喜欢画画的孩子",
      "q": "Describe a child who loves drawing/painting",
      "cuePoints": [
        "Who he/she is",
        "How/when you knew him/her",
        "How often he/she draws/paints",
        "And explain why you think he/she loves drawing/painting"
      ],
      "tag": "沿用",
      "recentCount": 798,
      "heatRank": 34,
      "heatLevel": "star0",
      "openingEn": "My little cousin is a child who can draw for an hour without looking up, and her favorite subject is Sun Yingsha.",
      "openingZh": "我表妹是个能画一小时不抬头的孩子，最爱画的主题是孙颖莎。",
      "materialId": "sun",
      "materialHint": "表妹着迷孙颖莎酒窝与贴纸形象，天天画卡通版并做成贴纸；解释她爱画因偶像与创作乐趣。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "My little cousin is a child who can draw for an hour without looking up, and her favorite subject is Sun Yingsha. I know her well because she is family, and every Spring Festival she shows me a new sketchbook. She draws almost every evening after homework. Why does she love it? She is fascinated by the famous table tennis player who is probably the most popular one in China right now. After watching Olympic highlights of Sun Yingsha winning gold in mixed doubles with Wang Chuqin under pressure, my cousin started sketching her adorable dimples and chubby cheeks again and again. She even cuts her drawings into stickers, just like fans who use stickers on social media to lighten the mood. Drawing lets her copy what she admires and invent cute outfits for her hero. That mix of idol energy and creative play keeps her pencils busy.",
      "sampleZh": "表妹天天画孙颖莎：酒窝、脸颊和贴纸风卡通；偶像热爱加上创作乐趣让她停不下来。"
    },
    {
      "id": 35,
      "title": "爱护自然之人",
      "q": "Describe a person who likes to look after the natural world",
      "cuePoints": [
        "Who this person is",
        "What he or she does",
        "How he or she does it",
        "How often he or she does it",
        "And explain how you feel about this person"
      ],
      "tag": "沿用",
      "recentCount": 777,
      "heatRank": 35,
      "heatLevel": "star0",
      "openingEn": "The person who looks after nature most carefully in my life is a volunteer guide I met on the way to Tianchi.",
      "openingZh": "我生命中最认真爱护自然的人，是去天池路上遇到的一位志愿者向导。",
      "materialId": "tianchi",
      "materialHint": "向导在长白山捡垃圾、提醒勿破坏；每周志愿；你因天池之美而敬佩他。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "The person who looks after nature most carefully in my life is a volunteer guide I met on the way to Tianchi. He works in a remote area in the northeast famous for untouched nature and the pond of heaven. What he does is simple but tough: he picks up litter on the extremely long staircase, reminds tourists not to feed wildlife, and explains why the clear blue sky and fresh air depend on small habits. He does this almost every weekend. I feel deep respect for him because without people like him, the lake that looks like pure jade and shines like a huge diamond would be spoiled. When I finally saw Tianchi and felt that all the sweat was worth it, I also understood his quiet mission. Caring for nature is how he protects that feeling for strangers like me.",
      "sampleZh": "天池志愿者向导周末捡垃圾、劝游客；正因有他，碧玉般天池才能让攀登的汗水值得。"
    },
    {
      "id": 36,
      "title": "微笑的场合",
      "q": "Describe an occasion when many people were smiling",
      "cuePoints": [
        "When it happened",
        "Who you were with",
        "What happened",
        "And explain why most people were smiling"
      ],
      "tag": "沿用",
      "recentCount": 749,
      "heatRank": 36,
      "heatLevel": "star0",
      "openingEn": "I can still picture the moment at the top of Changbai Mountain when almost everyone around me broke into smiles.",
      "openingZh": "我仍能想起在长白山顶，周围几乎所有人突然露出微笑的那一刻。",
      "materialId": "tianchi",
      "materialHint": "登顶见天池瞬间全员微笑；与朋友同行；因湖如钻石、汗水值得。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "I can still picture the moment at the top of Changbai Mountain when almost everyone around me broke into smiles. It happened last summer after a long climb with three friends through a remote area famous for untouched nature. We had struggled up an extremely long staircase, sweating and half-complaining. Then Tianchi, the pond of heaven, appeared: huge, pure like jade, shining like a huge diamond under the sunlight against a clear blue sky. Strangers, guides, and my friends all smiled at the same time, some even laughing in relief. People were smiling because the view was breathtaking and because as soon as they saw it, all the sweat from the climbing was worth it. Shared hard work plus sudden beauty is a powerful formula for smiles.",
      "sampleZh": "去年夏天和朋友爬极长阶梯后见到天池，所有人同时微笑：湖如钻石，攀登的汗水瞬间值得。"
    },
    {
      "id": 37,
      "title": "发挥想象力",
      "q": "Describe a time you needed to use your imagination",
      "cuePoints": [
        "When it was",
        "Why you needed to use imagination",
        "How difficult or easy it was",
        "And explain how you felt about it"
      ],
      "tag": "沿用",
      "recentCount": 749,
      "heatRank": 37,
      "heatLevel": "star0",
      "openingEn": "I needed imagination most when my film club asked me to rewrite the ending of Xialuotefannao for a short stage sketch.",
      "openingZh": "最需要想象力的一次，是电影社让我为《夏洛特烦恼》短剧重写结局。",
      "materialId": "movie",
      "materialHint": "改写夏洛特烦恼结局：时间旅行、追秋雅、梦与爱；需要脑补情感转折。",
      "endingTip": "领悟到爱才是生命中最宝贵的东西",
      "sampleEn": "I needed imagination most when my film club asked me to rewrite the ending of Xialuotefannao for a short stage sketch. It was last semester, and I had to invent dialogue that kept the time-travel joke but made the theme clearer for classmates who had not seen the film. Xialuotefannao stars Shen Teng and Ma Li and follows a man who travels in time to pursue his dream girl Qiuya, becomes a famous musician, then discovers what truly matters. Imagining a new final scene was harder than I expected: I had to show that love was the most valuable thing without copying the movie line by line, and still hint that it might be a long dream. After several drafts I felt proud rather than stuck. Stretching the story helped me understand why the original ending hits so hard.",
      "sampleZh": "为电影社改写《夏洛特烦恼》结局，需想象时间旅行与情感转折，最终仍落在爱才是最宝贵的。"
    },
    {
      "id": 38,
      "title": "近期改变的计划",
      "q": "Describe a plan that you had to change recently",
      "cuePoints": [
        "When this happened",
        "What made you change the plan",
        "What the new plan was",
        "And how you felt about the change"
      ],
      "tag": "新增",
      "recentCount": 742,
      "heatRank": 38,
      "heatLevel": "star0",
      "openingEn": "Earlier this year I had to change my plan of starting work immediately after graduation.",
      "openingZh": "今年早些时候，我不得不改变毕业后立刻工作的计划。",
      "materialId": "yumeng",
      "materialHint": "原计划工作；雨萌倾听后新计划读硕；感受从忐忑到坚定。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "Earlier this year I had to change my plan of starting work immediately after graduation. This happened in my third year at university, when deadlines for both jobs and master's applications overlapped and my calendar suddenly looked impossible. What made me change was a long talk with Yumeng, one of my most important friends. We grew up in the same neighborhood, and that day we walked around the campus while she listened very patiently to my half-finished spreadsheets and fears. She said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life,\" and \"Your passion is your best teacher. Just go for it.\" The new plan was to prepare for a master's program first, delay full-time work, and treat employment as a later chapter once I felt ready. At first I felt unsettled and even guilty toward my family, but soon I felt clearer and braver because the path matched what I actually wanted. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "原计划毕业工作，雨萌劝我想一生想做什么后改为先读硕；起初忐忑，后来更坚定。"
    },
    {
      "id": 39,
      "title": "乐于助人的人",
      "q": "Describe a person who often helps others",
      "cuePoints": [
        "Who this person is",
        "How often he/she helps others",
        "How/why he/she helps others",
        "And how you feel about this person"
      ],
      "tag": "沿用",
      "recentCount": 686,
      "heatRank": 39,
      "heatLevel": "star0",
      "openingEn": "For this topic I can think of no one else but my closest friend, Yumeng.",
      "openingZh": "这个话题除了我最亲的朋友雨萌，我想不到别人。",
      "materialId": "yumeng",
      "materialHint": "雨萌常倾听支持；校园帮你做人生抉择；你感激她乐于助人。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "For this topic I can think of no one else but my closest friend, Yumeng. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school. She helps others often—classmates with notes, neighbors with errands, and me whenever I panic about the future. She helps by listening first; she is really smart and optimistic, and whether in study or personal life she is always willing to support people. When I faced a master's-or-job crossroads in my third year, we walked around the campus, she listened very patiently, and she offered clear advice instead of empty comfort: think about the rest of your life, and let passion be your teacher. I feel lucky and inspired by her. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "雨萌经常帮助别人：先倾听再给建议；大三抉择时她的话给了我巨大力量。"
    },
    {
      "id": 40,
      "title": "想从事的短期海外工作",
      "q": "Describe a short-term job you want to have in a foreign country",
      "cuePoints": [
        "Where it is",
        "How you know of it",
        "What the job is",
        "And explain why you want to do it"
      ],
      "tag": "沿用",
      "recentCount": 672,
      "heatRank": 40,
      "heatLevel": "star0",
      "openingEn": "The short-term overseas job I want is a research assistant role in the UK linked to my master's plan.",
      "openingZh": "我想要的短期海外工作，是与读硕计划相关的英国科研助理岗位。",
      "materialId": "yumeng",
      "materialHint": "岗位来自雨萌鼓励读硕之后的规划；海外短工会练英语并验证热情。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "The short-term overseas job I want is a research assistant role in the UK linked to my master's plan. I know of it through university notices and through conversations with Yumeng, one of my most important friends. We grew up in the same neighborhood, and when I was lost in my third year about studying further or working, we walked around the campus and she listened very patiently. She told me not to worry only about finding a job and to think about what I want for the rest of my life, adding that passion is the best teacher. That advice pushed me toward graduate study abroad, and a short research post would let me practice English, test the field, and earn a bit of experience. I want it because it turns her wise encouragement into a concrete next step. Her words still give me strength whenever applications feel heavy.",
      "sampleZh": "想做英国短期科研助理；灵感来自雨萌鼓励读硕与追随热情，用以练英语并验证方向。"
    },
    {
      "id": 41,
      "title": "App/程序",
      "q": "Describe a program or app on your computer or phone",
      "cuePoints": [
        "What it is",
        "How often you use it",
        "When/how you use it",
        "When/how you found it",
        "And explain how you feel about it"
      ],
      "tag": "沿用",
      "recentCount": 665,
      "heatRank": 41,
      "heatLevel": "star0",
      "openingEn": "The app I open without thinking is a social messaging app packed with stickers, including dozens of Sun Yingsha faces.",
      "openingZh": "我下意识打开的App是社交聊天软件，里面塞满贴纸，包括许多孙颖莎表情。",
      "materialId": "sun",
      "materialHint": "聊天App里用孙颖莎酒窝贴纸活跃气氛；高频使用；感受轻松有趣。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "The app I open without thinking is a social messaging app packed with stickers, including dozens of Sun Yingsha faces. I use it every day to chat with classmates and family, usually on the bus or between classes. I found it years ago because everyone in school already had it. What makes it fun for me is the sticker culture around the famous table tennis player Sun Yingsha, probably the most popular one in China right now after her Paris Olympic gold in mixed doubles with Wang Chuqin. People are fascinated by her adorable dimples and chubby cheeks, so they make stickers of her image and use them on social media to lighten the mood in a conversation. I feel the app is more than utility: those little images turn stressful group chats into something warmer and funnier.",
      "sampleZh": "最常用聊天App；孙颖莎酒窝贴纸在对话里活跃气氛，让压力群聊轻松许多。"
    },
    {
      "id": 42,
      "title": "花费超过预期的物品",
      "q": "Describe an item on which you spent more than expected",
      "cuePoints": [
        "What it is",
        "How much you spent on it",
        "Why you bought it",
        "And explain why you think you spent more than expected"
      ],
      "tag": "沿用",
      "recentCount": 651,
      "heatRank": 42,
      "heatLevel": "star0",
      "openingEn": "The item I overspent on was a limited Jellycat teddy bear that cost far more than my usual birthday budget.",
      "openingZh": "我超支买的是一只限量Jellycat泰迪熊，远超平时生日预算。",
      "materialId": "bear",
      "materialIds": [
        "bear",
        "basketball"
      ],
      "materialHint": "限量Jellycat价格超预期；为安慰与纪念而买；软毛红丝带、高考平静说明为何仍值得。",
      "materialHintById": {
        "bear": "限量Jellycat泰迪熊价格超预期；软毛红丝带，高考压力时抱着更平静，像老朋友。",
        "basketball": "专业篮球价格超预期；父亲同款手感，高考前投篮让人平静头脑清晰，像老朋友。"
      },
      "openingById": {
        "bear": {
          "en": "The item I overspent on was a limited Jellycat teddy bear that cost far more than my usual birthday budget.",
          "zh": "我超支买的是一只限量Jellycat泰迪熊，远超平时生日预算。"
        },
        "basketball": {
          "en": "The item I overspent on was a pro-quality basketball that cost more than I planned for a simple sports gift.",
          "zh": "我超支买的是一个专业手感篮球，比原计划的简单运动礼物贵不少。"
        }
      },
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "The item I overspent on was a limited Jellycat teddy bear that cost far more than my usual birthday budget. I paid nearly twice what I expected because the store only had the softest version left. I bought it after remembering how a stuffed teddy bear from Jellycat—with soft fur and a red ribbon—had once helped a friend feel calmer before exams, and I wanted the same comfort. Why more than expected? Collectors had raised demand, and I refused to leave with a cheaper stiff toy. Before my own college entrance exam period I held it when I could not sleep and somehow felt calmer. It has been with me through many tense nights, so it really feels like an old friend. Looking back, the extra money bought emotional value, not just fabric.",
      "sampleZh": "超预算买限量Jellycat小熊；软毛红丝带在压力时带来平静，像老朋友，贵得有理由。",
      "sampleEnById": {
        "bear": "The item I overspent on was a limited Jellycat teddy bear that cost far more than my usual birthday budget. I paid nearly twice what I expected because the store only had the softest version left. I bought it after remembering how a stuffed teddy bear from Jellycat—with soft fur and a red ribbon—had once helped a friend feel calmer before exams, and I wanted the same comfort. Why more than expected? Collectors had raised demand, and I refused to leave with a cheaper stiff toy. Before my own college entrance exam period I held it when I could not sleep and somehow felt calmer. It has been with me through many tense nights, so it really feels like an old friend. Looking back, the extra money bought emotional value, not just fabric.",
        "basketball": "The item I overspent on was a pro-quality basketball that cost more than I planned for a simple sports gift. The price jumped because of the grip and brand, almost double my budget. I bought it because my father once gave me a basketball that helped me a lot, and I wanted an upgrade with the same feeling. Before the college entrance exam I was so stressed I could not focus, so I went downstairs and shot some hoops; every clean shot made me feel calmer and my mind became much clearer. That is why I accepted the higher price. The ball has been with me in many tense seasons, so it really feels like an old friend rather than overpriced rubber."
      },
      "sampleZhById": {
        "bear": "超预算买限量Jellycat小熊，压力时更平静，像老朋友。",
        "basketball": "超预算买专业篮球，投篮减压头脑清晰，像老朋友。"
      },
      "materialOptions": [
        "bear",
        "basketball"
      ]
    },
    {
      "id": 43,
      "title": "想要颁布的环保法律",
      "q": "Describe an environmental law you would like your country to introduce",
      "cuePoints": [
        "What law it should be",
        "Why people should follow the law",
        "Whether the law will be popular",
        "And explain how you feel about this law"
      ],
      "tag": "新增",
      "recentCount": 637,
      "heatRank": 43,
      "heatLevel": "star0",
      "openingEn": "The environmental law I want introduced is a strict anti-litter and trail-protection rule for national mountain parks.",
      "openingZh": "我想推动的环保法，是针对国家山地公园的严格反 litter 与步道保护规则。",
      "materialId": "tianchi",
      "materialHint": "与天池体验挂钩：未开发自然需法律保护；限流罚款；登顶感受收尾。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "The environmental law I want introduced is a strict anti-litter and trail-protection rule for national mountain parks. People should follow it because untouched places disappear quickly once trash and illegal shortcuts arrive. I believe most hikers would find it popular, though a minority may call it inconvenient. My feeling comes from climbing toward Tianchi in a remote northeast area famous for untouched nature. On the extremely long staircase the air was fresh and the sky breathtakingly clear, yet I still saw bottles left behind. When the pond of heaven appeared like pure jade shining as a huge diamond, I knew beauty alone cannot protect itself. As soon as I saw Tianchi, all the sweat was worth it, and that is exactly why I want a law with real penalties and education, not only posters.",
      "sampleZh": "想立山地公园反 litter 保护法；天池未开发之美需要法律牙齿，登顶震撼让我更坚持。"
    },
    {
      "id": 44,
      "title": "自行车/摩托车/汽车旅行",
      "q": "Describe a bicycle/motorcycle/car trip you would like to go",
      "cuePoints": [
        "Who you would like to go with",
        "Where you would like to go",
        "When you would like to go",
        "And explain why you would like to go by bicycle/motorcycle/car"
      ],
      "tag": "沿用",
      "recentCount": 623,
      "heatRank": 44,
      "heatLevel": "star0",
      "openingEn": "If I could plan one road trip, I would take a car journey to Changbai Mountain with my parents.",
      "openingZh": "如果能计划一次公路旅行，我会和父母开车去长白山。",
      "materialId": "tianchi",
      "materialHint": "自驾去天池：与父母、秋天出发；开车灵活停靠，再爬阶梯看湖。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "If I could plan one road trip, I would take a car journey to Changbai Mountain with my parents. We would go in early autumn when the air is cool and clear. The destination is a remote area in the northeast famous for untouched nature and Tianchi, the pond of heaven. I prefer a car because trains cannot stop at small viewpoints, and we could rest whenever my parents feel tired before the extremely long staircase. After parking we would climb, overlook the mountain under a clear blue sky, and finally see the lake like pure jade shining as a huge diamond. I want this car trip because shared effort ends in a shared wow: as soon as we see Tianchi, all the sweat from the climbing will be worth it, and the drive itself becomes part of the memory.",
      "sampleZh": "想和父母秋天自驾去长白山天池；开车灵活停靠，登顶见湖时一切汗水都值得。"
    },
    {
      "id": 45,
      "title": "给别人建议",
      "q": "Describe a time when you gave advice to others",
      "cuePoints": [
        "When it was",
        "To whom you gave the advice",
        "What the advice was",
        "And explain why you gave the advice"
      ],
      "tag": "沿用",
      "recentCount": 616,
      "heatRank": 45,
      "heatLevel": "star0",
      "openingEn": "Last spring I found myself giving advice to Yumeng for once, reversing our usual roles.",
      "openingZh": "去年春天我难得反过来给雨萌提建议，角色对调了一次。",
      "materialId": "yumeng",
      "materialHint": "角色互换：雨萌纠结时你把“热情是最好的老师”送给她；仍用你们的友情与校园场景。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "Last spring I found myself giving advice to Yumeng for once, reversing our usual roles. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, and she usually listens to my problems with endless patience, but that week she was the one torn between a safe internship and a harder master's track. We walked around the campus as always; this time I listened first, then borrowed the wisdom she had once given me when I faced the same crossroads in my third year. I told her, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life,\" and \"Your passion is your best teacher. Just go for it.\" I gave the advice because I had lived through that fear and knew it can disguise itself as practicality. She later said my words gave her strength—the same strength her wise advice still gives me today whenever I doubt a big choice.",
      "sampleZh": "雨萌纠结实习与读硕时，我把她曾给我的话送回：想一生想做什么，热情是最好的老师。"
    },
    {
      "id": 46,
      "title": "喜欢的电视/网络节目",
      "q": "Describe a TV or online program you like to watch",
      "cuePoints": [
        "What it is",
        "What it is about",
        "Who you watch it with",
        "And explain why you like to watch it"
      ],
      "tag": "沿用",
      "recentCount": 581,
      "heatRank": 46,
      "heatLevel": "star0",
      "openingEn": "The online program I replay most is a comedy talk show that often invites actors like Shen Teng and Ma Li.",
      "openingZh": "我最常回看的网络节目，是常请沈腾、马丽这类演员的喜剧脱口秀。",
      "materialId": "movie",
      "materialHint": "节目聊夏洛特烦恼幕后：时间旅行、追梦与爱；和室友一起看，笑中有感悟。",
      "endingTip": "领悟到爱才是生命中最宝贵的东西",
      "sampleEn": "The online program I replay most is a comedy talk show that often invites actors like Shen Teng and Ma Li. It is about movie stories behind the scenes, and one episode focused on Xialuotefannao, the film where a man can travel in time. I usually watch it with my roommate on weekend nights. In that episode they joke about pursuing the dream girl Qiuya, becoming a famous musician, and then waking from a long dream. I like the program because it mixes laughter with a soft landing: even while joking, they return to the idea that love was the most valuable thing in life. After stressful study days, that blend of humor and meaning feels better than empty scrolling. It also makes me want to rewatch the movie with fresher eyes.",
      "sampleZh": "爱看请沈腾马丽的喜剧访谈；聊《夏洛特烦恼》时间旅行，笑完仍回到爱最宝贵。"
    },
    {
      "id": 47,
      "title": "机智解决问题的人",
      "q": "Describe a person who solved a problem in a smart way",
      "cuePoints": [
        "Who this person is",
        "What the problem was",
        "How he/she solved it",
        "And explain why you think he/she did it in a smart way"
      ],
      "tag": "沿用",
      "recentCount": 546,
      "heatRank": 47,
      "heatLevel": "star0",
      "openingEn": "When I think of someone who solves problems smartly, Yumeng is the first name that comes up.",
      "openingZh": "想到机智解决问题的人，我第一个会想到雨萌。",
      "materialId": "yumeng",
      "materialHint": "问题是你考研/工作迷茫；她用热情是最好的老师一句话拆开焦虑；机智在于抓住核心。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "When I think of someone who solves problems smartly, Yumeng is the first name that comes up. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, and she is really smart and optimistic without showing off. The problem was mine: in my third year at university I was stuck between a master's degree and starting work, and anxiety made every option look wrong. She solved it not by choosing for me, but by reframing the question. We walked around the campus, she listened very patiently, then said, \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life,\" and \"Your passion is your best teacher. Just go for it.\" After that, she helped me list practical next steps so the decision felt manageable instead of endless. I call it smart because she attacked the fear underneath the dilemma, not only the surface choices. Her words gave me so much strength, and I still appreciate her wise advice to this day.",
      "sampleZh": "雨萌机智化解我的读硕/工作焦虑：不替我选，而用热情与长远目标重构问题。"
    },
    {
      "id": 48,
      "title": "商店",
      "q": "Describe a shop/store you enjoy visiting",
      "cuePoints": [
        "What the shop's name is",
        "Where it is",
        "How often you visit it",
        "And explain why you like to visit it"
      ],
      "tag": "沿用",
      "recentCount": 539,
      "heatRank": 48,
      "heatLevel": "star0",
      "openingEn": "The shop I enjoy most is a soft-toy boutique in the mall where I once chose a Jellycat bear for a friend.",
      "openingZh": "我最爱逛的店是商场里的毛绒礼品店，我曾在那里为朋友挑Jellycat小熊。",
      "materialId": "bear",
      "materialIds": [
        "bear",
        "basketball"
      ],
      "materialHint": "礼品店挑Jellycat：软毛红丝带、店员耐心；喜欢因礼物有温度。男生版体育店挑篮球。",
      "materialHintById": {
        "bear": "商场毛绒店精选Jellycat泰迪熊；软毛红丝带，店员耐心，适合挑有温度的礼物。",
        "basketball": "体育用品店挑选手感好的篮球；店员讲解专业，适合买减压陪伴的“老朋友”。"
      },
      "openingById": {
        "bear": {
          "en": "The shop I enjoy most is a soft-toy boutique in the mall where I once chose a Jellycat bear for a friend.",
          "zh": "我最爱逛的店是商场里的毛绒礼品店，我曾在那里为朋友挑Jellycat小熊。"
        },
        "basketball": {
          "en": "The shop I enjoy most is a compact sports store where I once spent an afternoon choosing the right basketball.",
          "zh": "我最爱逛的店是一家小体育用品店，我曾在那里花一下午挑合适的篮球。"
        }
      },
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "The shop I enjoy most is a soft-toy boutique in the mall where I once chose a Jellycat bear for a friend. It sits on the third floor next to a bookstore, and I visit every month or whenever I need a careful gift. I like it because the staff never rush you. That day I picked a stuffed teddy bear from Jellycat with soft fur and a red ribbon around its neck, imagining how it might help someone feel calmer before exams. The shelves smell faintly clean, the lighting is warm, and other customers smile at the silly displays. Later my friend said the bear felt like an old friend during stressful weeks, which made me love the shop even more. It sells comfort, not only products.",
      "sampleZh": "爱逛商场毛绒店，曾为朋友精选Jellycat小熊；店员耐心，礼物后来成了像老朋友的安慰。",
      "sampleEnById": {
        "bear": "The shop I enjoy most is a soft-toy boutique in the mall where I once chose a Jellycat bear for a friend. It sits on the third floor next to a bookstore, and I visit every month or whenever I need a careful gift. I like it because the staff never rush you. That day I picked a stuffed teddy bear from Jellycat with soft fur and a red ribbon around its neck, imagining how it might help someone feel calmer before exams. The shelves smell faintly clean, the lighting is warm, and other customers smile at the silly displays. Later my friend said the bear felt like an old friend during stressful weeks, which made me love the shop even more. It sells comfort, not only products.",
        "basketball": "The shop I enjoy most is a compact sports store where I once spent an afternoon choosing the right basketball. It is near my school gate, and I drop in almost every other week. I like it because the owner lets you test the grip and bounce patiently. I was looking for a ball like the one my father gave me, something I could use when I need to shoot some hoops and feel calmer with a clearer mind. He explained materials without pushing the expensive option. That honesty keeps me coming back. The basketball I finally bought has been through many tense evenings and really feels like an old friend, so the shop feels like part of that story."
      },
      "sampleZhById": {
        "bear": "爱逛毛绒店精选Jellycat，礼物成了像老朋友的安慰。",
        "basketball": "爱逛体育店挑篮球，投篮减压，球像老朋友。"
      },
      "materialOptions": [
        "bear",
        "basketball"
      ]
    },
    {
      "id": 49,
      "title": "不享受的音乐活动",
      "q": "Describe an event you attended in which you didn't enjoy the music played",
      "cuePoints": [
        "What it was",
        "Who you went with",
        "Why you decided to go there",
        "And explain why you didn't enjoy it"
      ],
      "tag": "沿用",
      "recentCount": 497,
      "heatRank": 49,
      "heatLevel": "star0",
      "openingEn": "Honestly I usually like music, but a karaoke night after badminton left me wishing I had gone straight home.",
      "openingZh": "平时我挺喜欢音乐，但有一次打球后的KTV让我直想回家。",
      "materialId": "badminton",
      "materialHint": "球友拉去KTV：嘈杂跑调；对比球场挥拍专注忘压，反衬音乐活动不适。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "Honestly I usually like music, but a karaoke night after badminton left me wishing I had gone straight home. It was a weekend gathering with the people I often team up with at the court after I started to play badminton to escape application stress. I decided to go because they had become friends and I was becoming more outgoing; saying no felt rude. The music, however, was painfully loud and off-key, and the room was packed with smoke and shouted choruses. I could not hear myself think, let alone relax. What I missed was the opposite feeling I get when I swing my racket: only its sound and the wind, focusing on mind and body, forgetting study pressure for a while. That night taught me that not every social plan fits me, even with good people.",
      "sampleZh": "球友拉去KTV又吵又跑调；远不如球场挥拍时能专注身心、暂时忘却压力。"
    },
    {
      "id": 50,
      "title": "对家庭重要的东西",
      "q": "Describe something important that has been kept in your family for a long time",
      "cuePoints": [
        "What it is",
        "When your family had it",
        "How your family got it",
        "And explain why it is important to your family"
      ],
      "tag": "沿用",
      "recentCount": 469,
      "heatRank": 50,
      "heatLevel": "star0",
      "openingEn": "We do not keep jewelry as a family treasure; we keep a stuffed teddy bear that has traveled with me for years.",
      "openingZh": "家里珍藏的不是珠宝，而是一只陪伴我多年的毛绒泰迪熊。",
      "materialId": "bear",
      "materialIds": [
        "bear",
        "basketball"
      ],
      "materialHint": "小学好友送的Jellycat成家庭纪念物；高考平静；像老朋友。男生版父亲送的篮球。",
      "materialHintById": {
        "bear": "小学好友送的Jellycat泰迪熊保存多年；软毛红丝带，高考时带来平静，像老朋友。",
        "basketball": "父亲送的篮球保存多年；高考前投篮减压头脑清晰，像老朋友。"
      },
      "openingById": {
        "bear": {
          "en": "We do not keep jewelry as a family treasure; we keep a stuffed teddy bear that has traveled with me for years.",
          "zh": "家里珍藏的不是珠宝，而是一只陪伴我多年的毛绒泰迪熊。"
        },
        "basketball": {
          "en": "We do not keep antiques as a family treasure; we keep a basketball my father gave me years ago.",
          "zh": "家里珍藏的不是古董，而是父亲多年前送我的一个篮球。"
        }
      },
      "endingTip": "它真的就像一个老朋友一样",
      "sampleEn": "We do not keep jewelry as a family treasure; we keep a stuffed teddy bear that has traveled with me for years. My family has had it since primary school, when my best friend gave me a stuffed teddy bear from Jellycat for my birthday. She knew I loved soft cute things, so she chose it carefully: small and brown, with soft fur and a red ribbon around its neck. It became important because before the college entrance exam I was so stressed I could not sleep, yet holding it made me feel calmer. Mum even jokes that the bear guarded our exam season. Since then, whenever anyone at home feels nervous, we treat it as a quiet comfort object. It has been with me during many important moments, so it really feels like an old friend—and that is why the family refuses to throw it away.",
      "sampleZh": "家庭珍藏小学好友送的Jellycat小熊；高考压力时带来平静，像老朋友，谁也不肯扔。",
      "sampleEnById": {
        "bear": "We do not keep jewelry as a family treasure; we keep a stuffed teddy bear that has traveled with me for years. My family has had it since primary school, when my best friend gave me a stuffed teddy bear from Jellycat for my birthday. She knew I loved soft cute things, so she chose it carefully: small and brown, with soft fur and a red ribbon around its neck. It became important because before the college entrance exam I was so stressed I could not sleep, yet holding it made me feel calmer. Mum even jokes that the bear guarded our exam season. Since then, whenever anyone at home feels nervous, we treat it as a quiet comfort object. It has been with me during many important moments, so it really feels like an old friend—and that is why the family refuses to throw it away.",
        "basketball": "We do not keep antiques as a family treasure; we keep a basketball my father gave me years ago. He gave it to me in middle school as a birthday gift, knowing I loved sports, and chose an orange ball with a solid grip. It became important before the college entrance exam, when I was too stressed to focus at my desk. I went downstairs and shot some hoops; every time the ball went through, I felt calmer and my mind became much clearer. Dad still asks if I have been practicing. The ball has been with me during many important moments, so it really feels like an old friend, which is why it stays in our hallway instead of a dusty box."
      },
      "sampleZhById": {
        "bear": "家庭珍藏Jellycat小熊，高考平静，像老朋友。",
        "basketball": "家庭珍藏父亲送的篮球，投篮减压，像老朋友。"
      },
      "materialOptions": [
        "bear",
        "basketball"
      ]
    },
    {
      "id": 51,
      "title": "禁用手机的场合",
      "q": "Describe an occasion when you were not allowed to use your mobile phone",
      "cuePoints": [
        "When it was",
        "Where it was",
        "Why you were not allowed to use your mobile phone",
        "And how you felt about it"
      ],
      "tag": "沿用",
      "recentCount": 455,
      "heatRank": 51,
      "heatLevel": "star0",
      "openingEn": "The strictest no-phone rule I met recently was at a badminton training session my coach ran.",
      "openingZh": "我最近遇到最严的禁手机规则，是教练组织的羽毛球训练课。",
      "materialId": "badminton",
      "materialHint": "球场禁手机为专注挥拍与组队；起初不习惯，后来体会忘压好处。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "The strictest no-phone rule I met recently was at a badminton training session my coach ran. It was on a Saturday morning at the campus sports hall, during the months when I was occupied with applying for master's programs and studying English. Phones had to stay in lockers because the coach wanted us to focus and to team up with partners without scrolling between rallies. At first I felt restless, worried about messages. Then I started to play, swinging my racket until all I heard was its sound and the wind. Without the phone, I became more outgoing with strangers at the court and could forget the pressure from my studies for a while. Looking back I felt grateful for the ban: it forced the mental reset I had come for.",
      "sampleZh": "羽毛球课禁手机，起初不安；挥拍专注后反而更能忘却申请压力，后来觉得感激。"
    },
    {
      "id": 52,
      "title": "鼓励别人做不愿做的事",
      "q": "Describe a time when you encouraged someone to do something that he/she didn't want to do",
      "cuePoints": [
        "Who he or she is",
        "What you encouraged him/her to do",
        "How he/she reacted",
        "And explain why you encouraged him/her to do it"
      ],
      "tag": "沿用",
      "recentCount": 385,
      "heatRank": 52,
      "heatLevel": "star0",
      "openingEn": "I once encouraged my shy roommate to try badminton even though he insisted sports were not for him.",
      "openingZh": "我曾鼓励害羞的室友去试羽毛球，尽管他坚持运动不适合自己。",
      "materialId": "badminton",
      "materialHint": "鼓励室友打球减压：他抗拒→组队后外向；你因自身受益而鼓励。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "I once encouraged my shy roommate to try badminton even though he insisted sports were not for him. He was buried in the same stress of applications and English study that had exhausted me before I started to play badminton. At first he reacted with excuses: no talent, no time, fear of looking silly. I dragged him to the court anyway, promising just one hour. Because badminton requires a partner, we team up with strangers, and soon he was laughing between points. He became more outgoing week by week. I encouraged him because I knew how swinging a racket—hearing only its sound and the wind—helps you focus on mind and body and forget study pressure for a while. Watching his mood lift confirmed the push was worth the awkward start.",
      "sampleZh": "鼓励害羞室友试羽毛球；他从抗拒到组队变外向；因挥拍能忘压，我坚持拉他去。"
    },
    {
      "id": 53,
      "title": "朋友自学",
      "q": "Describe one of your friends who learned something without a teacher",
      "cuePoints": [
        "Who he/she is",
        "What he/she learned",
        "Why he/she learned this",
        "And explain whether it would be easier to learn from a teacher"
      ],
      "tag": "沿用",
      "recentCount": 371,
      "heatRank": 53,
      "heatLevel": "star0",
      "openingEn": "One friend taught himself badminton through videos and court practice, without ever hiring a coach.",
      "openingZh": "有个朋友完全靠视频和下场练习自学羽毛球，从未请教练。",
      "materialId": "badminton",
      "materialHint": "朋友自学打球减压：看视频、与陌生人组队；教师或许更快，但自学让他更外向。",
      "endingTip": "全神贯注于身心，暂时忘却学业压力",
      "sampleEn": "One friend taught himself badminton through videos and court practice, without ever hiring a coach. He is a classmate who was occupied with applying for master's programs and studying English, always tired and unable to focus. He learned footwork and serves from online clips, then started to play badminton at the public court. Why? He needed a cheap way to reset. He often team up with strangers, became more and more outgoing, and now meets friends every weekend. Would a teacher be easier? Probably for clean technique, yes. But self-learning forced him to observe, fail, and adjust, which built confidence. When he swings his racket he says all he hears is its sound and the wind, letting him forget study pressure for a while. That result matters more to him than perfect form from day one.",
      "sampleZh": "朋友看视频自学羽毛球来减压，与陌生人组队变外向；有教练或许更快，但自学带来自信与忘压。"
    },
    {
      "id": 54,
      "title": "有趣的建筑",
      "q": "Describe an interesting building",
      "cuePoints": [
        "Where it is",
        "What it looks like",
        "What function it has",
        "And explain why you think it is interesting"
      ],
      "tag": "沿用",
      "recentCount": 364,
      "heatRank": 54,
      "heatLevel": "star0",
      "openingEn": "An interesting building I keep describing to friends is the viewing pavilion near Tianchi after the long climb.",
      "openingZh": "我常向朋友描述的有趣建筑，是爬完长阶后天池附近的观景亭。",
      "materialId": "tianchi",
      "materialHint": "观景亭外观简朴却功能强大：休息与眺望天池；因位置与视野而有趣。",
      "endingTip": "一看到天池，攀登的所有汗水都值得了",
      "sampleEn": "An interesting building I keep describing to friends is the viewing pavilion near Tianchi after the long climb. It stands in a remote northeast area famous for untouched nature, right after an extremely long staircase. The building looks simple—wood and stone, open windows, no flashy glass—but its function is perfect: shelter from wind, a place to drink water, and a frame for the view. From there you overlook the mountain, see a clear blue sky, and then the pond of heaven appears like pure jade shining as a huge diamond. I find it interesting because architecture usually tries to impress alone, yet this pavilion becomes meaningful only with the landscape. As soon as I saw Tianchi from its edge, all the sweat from the climbing was worth it.",
      "sampleZh": "天池观景亭外观朴素，却把未开发自然与碧玉湖面框进视野；登顶后一切汗水都值得。"
    },
    {
      "id": 55,
      "title": "遇到困难终成功的人",
      "q": "Describe a person who met difficulties but succeeded",
      "cuePoints": [
        "Who this person is",
        "What difficulties he met",
        "How he overcame the difficulties",
        "And explain how you feel about him"
      ],
      "tag": "新增",
      "recentCount": 0,
      "heatRank": 55,
      "heatLevel": "star0",
      "openingEn": "A person who met huge difficulties yet succeeded is the table tennis player Sun Yingsha.",
      "openingZh": "一个遇困难终成功的人，是乒乓球运动员孙颖莎。",
      "materialId": "sun",
      "materialHint": "高压大赛、伤病或舆论困难；巴黎奥运混双夺金克服；感受敬佩与她的受欢迎。",
      "endingTip": "她在中国极其受欢迎，人们着迷于她可爱的酒窝和贴纸形象",
      "sampleEn": "A person who met huge difficulties yet succeeded is the table tennis player Sun Yingsha. She is famous and probably the most popular one in China right now, but popularity does not erase pressure. The difficulties she met include relentless competition, public expectation, and the mental weight of representing a nation in every rally. She overcame them through disciplined training and by giving her best performance under enormous pressure, especially when she played mixed doubles with Wang Chuqin at the Paris Olympic Games and won the gold medal. I feel inspired watching someone so young stay sharp without losing warmth: fans still adore her adorable dimples and chubby cheeks and make stickers to lighten the mood online. Her path shows that success can coexist with approachable humanity, which is why I respect her beyond the medals.",
      "sampleZh": "孙颖莎面对高压与期待，巴黎奥运混双夺金；年轻却亲和受欢迎，令人敬佩。"
    },
    {
      "id": 56,
      "title": "别人帮助解决问题",
      "q": "Describe a time when a person did something to help you solve a problem",
      "cuePoints": [
        "Who the person is",
        "What the problem was",
        "How he/she helped you",
        "And explain how you felt about the experience"
      ],
      "tag": "新增",
      "recentCount": 0,
      "heatRank": 56,
      "heatLevel": "star0",
      "openingEn": "The clearest time someone helped me solve a problem was when Yumeng talked me through my graduation panic.",
      "openingZh": "别人帮我解决问题最清楚的一次，是雨萌带我走出毕业恐慌。",
      "materialId": "yumeng",
      "materialHint": "问题是读硕/工作纠结；雨萌校园倾听并给建议；感受感激与力量。",
      "endingTip": "她的话给了我巨大的力量，至今仍感激她睿智的建议",
      "sampleEn": "The clearest time someone helped me solve a problem was when Yumeng talked me through my graduation panic. Yumeng is one of my most important friends. We grew up in the same neighborhood and went to the same school, so she noticed my stress before I admitted it. The problem was that in my third year at university I could not decide between a master's degree and starting work; every night felt heavier and I kept changing my mind. She helped by meeting me, walking around the campus, and listening very patiently before offering direction: \"Don't worry about the pressure of finding a job. Think about what you want to do for the rest of your life. If you are sure you want to further your studies, just go for it.\" She added that passion is the best teacher and reminded me I would find work I love eventually. I felt relief, clarity, and deep gratitude because the fog finally lifted. Her words gave me so much strength, and I still appreciate her wise advice to this day whenever a new problem appears.",
      "sampleZh": "大三读硕/工作恐慌时，雨萌校园倾听并建议追随热情；我感到解脱并至今感激。"
    }
  ]
};
