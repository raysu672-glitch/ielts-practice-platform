// P3：追问链题库 + 本题答题角度（优先扣题；万能素材仅可选借用）
const P3_DATA = {
  answerFrame: {
    title: '答题结构（框架，不是内容）',
    steps: [
      '引入点题（Introduction）',
      '论点 1（Firstly + 解释/举例，必须扣本题）',
      '论点 2（Besides + 解释/举例，必须扣本题）',
      '一句话总结（Conclusion）'
    ],
    qTypes: {
      reason: { zh: '原因/重要性', tip: '给 2 个不同原因；谈重要性时可说「如果没有会怎样」。' },
      compare: { zh: '对比/选择', tip: '客观说 A / By contrast 说 B；选不出用 It depends。' },
      proscons: { zh: '利弊', tip: '优点 1–2 点 + 缺点 1–2 点，或按考官方向展开。' },
      solution: { zh: '解决/未来', tip: '就本题问题给出可操作办法；勿空谈无关政策。' }
    }
  },

  // 仅作可选句式库；默认不按题强推，避免硬套跑题
  materials: [
    {
      id: 'economy_tech',
      name: '经济与科技',
      typeHint: '仅当题目本身谈消费/科技/生活变化时可用',
      bullets: [
        { zh: '生活水平提高，经济负担更小', en: 'With the development of the economy, people have a higher living standard, so they have less financial burden.' },
        { zh: '高科技省时省力，足不出户也能办事', en: 'High-tech products make life time-saving and labor-saving; people can do things anytime without going out.' }
      ]
    },
    {
      id: 'age_groups',
      name: '年龄对比',
      typeHint: '仅当题目明确问年轻/老年/小孩差异时可用',
      bullets: [
        { zh: '年轻人接受新事物更快', en: 'Young people usually accept new things more quickly.' },
        { zh: '老年人更偏向稳妥实用', en: 'Older people often prefer practical and familiar options.' }
      ]
    },
    {
      id: 'stress_relax',
      name: '压力与放松',
      typeHint: '仅当题目谈休闲/运动/解压时可用',
      bullets: [
        { zh: '工作学习压力大', en: 'People are under great pressure from work and study.' },
        { zh: '活动能缓解疲劳、保持健康', en: 'It can help them relieve fatigue and keep fit.' }
      ]
    },
    {
      id: 'alone_social',
      name: '独处 vs 社交',
      typeHint: '仅当题目谈独自/团队时可用',
      bullets: [
        { zh: '独处可按自己节奏、少被打扰', en: 'Alone, people can follow their own schedule with fewer interruptions.' },
        { zh: '团队便于互助与交流', en: 'In a group, people can help each other and exchange ideas.' }
      ]
    },
    {
      id: 'gov_media',
      name: '政府与媒体',
      typeHint: '仅当题目问如何治理/保护/提高意识时可用',
      bullets: [
        { zh: '政府可立法并投资公共设施', en: 'The government can make rules and invest in public facilities.' },
        { zh: '媒体可提高公众意识', en: 'The media can raise public awareness through campaigns.' }
      ]
    }
  ],

  topics: [
    {
      id: 'change',
      titleZh: '改变与习惯',
      titleEn: 'Change and habits',
      relatedP2Title: '近期改变',
      heatRank: 1,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'change_1',
          q: 'Why do some people find it hard to change their habits?',
          tipZh: '紧扣“习惯难改”，别扯环保或政府。',
          qType: 'reason',
          angles: [
            { zh: '习惯已自动化：不用想就会做，改起来费脑力', en: 'Habits are automatic, so people keep doing them without thinking.' },
            { zh: '改变短期不舒服：失败恐惧 + 日常已经够累', en: 'Change feels uncomfortable at first, and busy people lack energy to restart.' }
          ],
          sampleEn: 'I think there are a few reasons. Firstly, habits are automatic, so people do them without thinking. Besides, change takes energy; when life is already busy, sticking to the old routine feels safer.'
        },
        {
          id: 'change_2',
          q: 'Do young people change their lifestyles more easily than older people?',
          tipZh: '对比两边即可，别把经济科技整段塞进来。',
          qType: 'compare',
          angles: [
            { zh: '年轻人更敢试新习惯：社交与工作环境变化快', en: 'Young people often try new routines because school or work changes fast.' },
            { zh: '年长者已有成型生活方式，改动成本更高', en: 'Older people already have a settled lifestyle, so changing it costs more effort.' }
          ],
          sampleEn: 'They are quite different. Young people usually try new routines more easily because their environment changes often. By contrast, older people may keep what already works and feel less need to reinvent daily life.'
        },
        {
          id: 'change_3',
          q: 'What are the advantages of making a positive change in life?',
          tipZh: '优点要落到“改变之后更好”，举健康/效率等与改变相关的例。',
          qType: 'proscons',
          angles: [
            { zh: '身心状态更好：睡眠、精力、情绪更稳', en: 'A positive change can improve energy, sleep, and mood.' },
            { zh: '带来新机会：新技能、新朋友或更好效率', en: 'It may bring new skills, new friends, or better daily efficiency.' }
          ],
          sampleEn: 'There are clear merits. Firstly, a healthy change can improve energy and mood. Besides, it may create new opportunities, such as meeting people through a new hobby or working more efficiently.'
        }
      ]
    },
    {
      id: 'environment',
      titleZh: '环境与法律',
      titleEn: 'Environment and laws',
      relatedP2Title: '保护环境的法律',
      heatRank: 2,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'env_1',
          q: 'Why is it important for governments to protect the environment?',
          tipZh: '谈公共健康与长期资源，勿扯“独处学习”。',
          qType: 'reason',
          angles: [
            { zh: '污染直接伤公众健康（空气、水）', en: 'Pollution harms public health through dirty air and water.' },
            { zh: '自然破坏难恢复，早治理成本更低', en: 'Damaged nature is hard to restore, so early protection saves more later.' }
          ],
          sampleEn: 'It is of vital importance. Firstly, without protection, pollution would harm public health. Besides, damaged nature is hard to restore, so early rules save money and resources later.'
        },
        {
          id: 'env_2',
          q: 'What can individuals do to help the environment?',
          tipZh: '只讲个人能做的日常行动。',
          qType: 'solution',
          angles: [
            { zh: '减塑、分类回收、少浪费食物与电', en: 'People can reduce plastic, recycle properly, and cut food or electricity waste.' },
            { zh: '多选公交/骑行，少开不必要的车', en: 'They can choose public transport or cycling instead of unnecessary car trips.' }
          ],
          sampleEn: 'Individuals can start with daily habits: reduce plastic, recycle, and save electricity. Also, choosing public transport more often can lower personal emissions.'
        },
        {
          id: 'env_3',
          q: 'Do you think fines are an effective way to stop people from harming nature?',
          tipZh: '讨论罚款是否有效，别展开成旅游题。',
          qType: 'proscons',
          angles: [
            { zh: '有效处：提高违规成本，吓阻乱扔/偷猎等', en: 'Fines raise the cost of bad behavior and can deter littering or illegal dumping.' },
            { zh: '局限：执法松或罚款太低，有人仍会无视', en: 'If enforcement is weak or fines are too low, some people still ignore the rules.' }
          ],
          sampleEn: 'Fines can work as a deterrent for obvious bad behavior. However, if enforcement is weak or the fine is tiny, some people may still ignore the rules.'
        }
      ]
    },
    {
      id: 'technology',
      titleZh: '科技与生活',
      titleEn: 'Technology in daily life',
      relatedP2Title: '遇到的科技问题',
      heatRank: 3,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'tech_1',
          q: 'How has technology changed the way people live compared with the past?',
          tipZh: '过去 vs 现在的生活方式差异。',
          qType: 'compare',
          angles: [
            { zh: '过去很多事必须出门、排队等待', en: 'In the past, many tasks required going outside and waiting in line.' },
            { zh: '现在购物、学习、沟通可随时在线完成', en: 'Today people can shop, study, and communicate online anytime.' }
          ],
          sampleEn: 'Life is quite different now. In the past, many tasks required going outside and waiting. Today, people can shop, study, and talk online without leaving home.'
        },
        {
          id: 'tech_2',
          q: 'What problems can technology cause for people?',
          tipZh: '谈科技带来的问题，如分心、隐私、久坐。',
          qType: 'proscons',
          angles: [
            { zh: '手机通知打断专注，深度工作变难', en: 'Constant notifications interrupt focus and make deep work harder.' },
            { zh: '久坐刷屏伤身体，也可能更焦虑', en: 'Sitting online for hours can harm health and increase anxiety.' }
          ],
          sampleEn: 'Technology saves time, but it also causes problems. Phones distract people from deep work, and staying online all day can harm health and increase stress.'
        },
        {
          id: 'tech_3',
          q: 'How can people solve technical problems more effectively?',
          tipZh: '解决“技术故障/不会用”的办法，别扯环保法。',
          qType: 'solution',
          angles: [
            { zh: '先看官方教程或联系客服逐步排查', en: 'People can follow official tutorials or contact customer service step by step.' },
            { zh: '向同事/论坛求助，厂商也应把界面做更清楚', en: 'They can ask colleagues or online forums, and companies should design clearer interfaces.' }
          ],
          sampleEn: 'First, people can follow tutorials or contact customer service. Besides, asking experienced friends or forums helps, and companies should make interfaces clearer.'
        }
      ]
    },
    {
      id: 'travel',
      titleZh: '旅行与地方',
      titleEn: 'Travel and places',
      relatedP2Title: '推荐旅行过的地方',
      heatRank: 4,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'travel_1',
          q: 'Why do people like to travel to natural places?',
          tipZh: '原因要连到“自然景点”，不是泛泛谈运动。',
          qType: 'reason',
          angles: [
            { zh: '风景与空气帮助从城市噪音里抽离', en: 'Natural scenery and clean air help people escape city noise.' },
            { zh: '慢节奏让人休息大脑，回来更有精力', en: 'A slower pace helps the mind rest, so people return with more energy.' }
          ],
          sampleEn: 'There are several reasons. Firstly, nature helps people escape noisy cities. Besides, quiet scenery lets them rest mentally and return with more energy.'
        },
        {
          id: 'travel_2',
          q: 'Is it better to travel alone or with friends?',
          tipZh: '只对比旅行方式，勿扯公司团队管理。',
          qType: 'compare',
          angles: [
            { zh: '独自旅行：行程自由，节奏随自己', en: 'Traveling alone means full freedom over the schedule and pace.' },
            { zh: '与朋友：更好分享体验，但可能意见不合', en: 'With friends it is more fun to share moments, but schedules can conflict.' }
          ],
          sampleEn: 'It depends. Alone travel gives freedom and a peaceful pace. With friends it is more fun to share moments, though people may disagree about plans.'
        },
        {
          id: 'travel_3',
          q: 'What should governments do to protect popular tourist sites?',
          tipZh: '聚焦景区保护措施。',
          qType: 'solution',
          angles: [
            { zh: '限流、禁乱扔，违规罚款', en: 'Set visitor limits, ban littering, and fine rule-breakers.' },
            { zh: '修步道与垃圾桶，并做游客须知宣传', en: 'Improve paths and bins, and teach visitors basic site rules.' }
          ],
          sampleEn: 'Governments can set visitor limits and punish littering. They should also improve paths and facilities, and clearly tell tourists how to protect the site.'
        }
      ]
    },
    {
      id: 'advertising',
      titleZh: '广告与名人',
      titleEn: 'Advertising and celebrities',
      relatedP2Title: '名人出演的广告',
      heatRank: 5,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'ad_1',
          q: 'Why do companies invite celebrities to advertise products?',
          tipZh: '商业动机：关注度与信任。',
          qType: 'reason',
          angles: [
            { zh: '明星自带流量，广告更容易被看到记住', en: 'Celebrities bring attention, so the ad is noticed and remembered.' },
            { zh: '粉丝对熟悉面孔更信任，转化更快', en: 'Fans often trust a familiar face, which can increase sales.' }
          ],
          sampleEn: 'Celebrities attract attention quickly. Fans trust familiar faces, and a popular star can make the brand more memorable.'
        },
        {
          id: 'ad_2',
          q: 'What are the disadvantages of celebrity advertising?',
          tipZh: '谈广告副作用，勿跑到环保。',
          qType: 'proscons',
          angles: [
            { zh: '冲动消费：不为需要，只为追星或虚荣', en: 'People may buy things they do not need just to follow a star.' },
            { zh: '夸大宣传：效果被吹高，误导消费者', en: 'Some ads exaggerate benefits and mislead consumers.' }
          ],
          sampleEn: 'One drawback is impulse buying for image, not need. Also, some celebrity ads exaggerate benefits and mislead viewers.'
        },
        {
          id: 'ad_3',
          q: 'Do young people and older people respond to ads differently?',
          tipZh: '广告反应差异，举例要与广告相关。',
          qType: 'compare',
          angles: [
            { zh: '年轻人更吃潮流、网感与明星联名', en: 'Young people react more to trends, online styles, and star collaborations.' },
            { zh: '年长者更看价格、实用性与可靠口碑', en: 'Older people focus more on price, usefulness, and trusted reviews.' }
          ],
          sampleEn: 'Yes, they often differ. Young people chase trendy ads and star collaborations. Older people usually care more about price and whether the product is useful.'
        }
      ]
    },
    {
      id: 'teamwork',
      titleZh: '团队与工作',
      titleEn: 'Teamwork and work',
      relatedP2Title: '在团队中工作',
      heatRank: 6,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'team_1',
          q: 'What are the benefits of working in a team?',
          tipZh: '工作场景的好处。',
          qType: 'proscons',
          angles: [
            { zh: '卡住时能互相补位、分担任务', en: 'Teammates can share tasks and help when someone gets stuck.' },
            { zh: '不同想法碰撞，方案更完整', en: 'Different ideas can make the final plan more complete.' }
          ],
          sampleEn: 'Teamwork has clear merits. People can share tasks and help each other when stuck. Different ideas also make the final plan stronger.'
        },
        {
          id: 'team_2',
          q: 'When is it better to work alone?',
          tipZh: '什么时候独自工作更好。',
          qType: 'compare',
          angles: [
            { zh: '需要深度专注写报告/写代码时', en: 'Deep-focus tasks like writing or coding often work better alone.' },
            { zh: '任务边界清晰、不必反复开会时', en: 'When the task is clear and needs few meetings, working alone is faster.' }
          ],
          sampleEn: 'Working alone is better for deep focus, such as writing a report. It is also faster when the task is clear and you do not need constant meetings.'
        },
        {
          id: 'team_3',
          q: 'How can companies help introverted employees work well in teams?',
          tipZh: '公司如何帮内向员工，给具体管理动作。',
          qType: 'solution',
          angles: [
            { zh: '角色清晰，可用书面更新代替只开大声会', en: 'Give clear roles and allow written updates instead of only loud meetings.' },
            { zh: '用小组讨论，减少突然当众发言压力', en: 'Use smaller discussion groups so shy people can speak with less pressure.' }
          ],
          sampleEn: 'Companies can assign clear roles and allow written updates. Smaller groups also help introverted staff contribute without too much pressure.'
        }
      ]
    },
    {
      id: 'learning',
      titleZh: '学习与语言',
      titleEn: 'Learning and languages',
      relatedP2Title: '擅长学习和说语言的人',
      heatRank: 7,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'learn_1',
          q: 'Why do some people learn languages faster than others?',
          tipZh: '语言学习速度差异。',
          qType: 'reason',
          angles: [
            { zh: '动机强：留学/工作需要，练习更勤', en: 'Strong motivation, such as study or work needs, leads to more practice.' },
            { zh: '不怕开口犯错，开口量更大', en: 'People who are not afraid of mistakes speak more and improve faster.' }
          ],
          sampleEn: 'Motivation matters a lot. People who need the language for study or work practice more. Those who dare to make mistakes also speak more and improve faster.'
        },
        {
          id: 'learn_2',
          q: 'Is it better to study alone or in a group when learning a language?',
          tipZh: '语言学习场景下的独自/小组。',
          qType: 'compare',
          angles: [
            { zh: '独自：记单词、练听力节奏可控', en: 'Alone study helps with vocabulary and listening at your own pace.' },
            { zh: '小组：真实对话与纠错，口语进步快', en: 'Group practice gives real conversation and faster speaking progress.' }
          ],
          sampleEn: 'It depends. Alone study helps concentration for vocabulary. Group practice gives real conversation, which builds fluency faster.'
        },
        {
          id: 'learn_3',
          q: 'What can schools do to help students enjoy language learning?',
          tipZh: '学校具体做法，别只说“减压”空话。',
          qType: 'solution',
          angles: [
            { zh: '用短视频、游戏、角色扮演增加趣味', en: 'Use short videos, games, and role-play to make lessons more fun.' },
            { zh: '多鼓励开口，评分不只盯语法错误', en: 'Praise speaking effort, not only perfect grammar.' }
          ],
          sampleEn: 'Schools can use games, short videos, and pair speaking so lessons feel less boring. Teachers should also praise effort, not only perfect grammar.'
        }
      ]
    },
    {
      id: 'ambition',
      titleZh: '目标与决定',
      titleEn: 'Goals and decisions',
      relatedP2Title: '长久目标/抱负',
      heatRank: 8,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'goal_1',
          q: 'Why is it important for young people to have long-term goals?',
          tipZh: '长期目标的重要性。',
          qType: 'reason',
          angles: [
            { zh: '给日常选择方向，少做无意义消耗', en: 'Goals give direction so daily choices waste less energy.' },
            { zh: '遇到困难时更愿坚持', en: 'With a clear goal, people keep going when study or work gets hard.' }
          ],
          sampleEn: 'Long-term goals give direction. Without them, people may waste energy on random tasks. Goals also help them stay disciplined when life gets hard.'
        },
        {
          id: 'goal_2',
          q: 'Do parents and children often have different goals?',
          tipZh: '代际目标差异。',
          qType: 'compare',
          angles: [
            { zh: '父母常更看重稳定工作与收入安全', en: 'Parents often focus on stable jobs and financial security.' },
            { zh: '年轻人可能更看重兴趣与成长体验', en: 'Young people may prioritize interest and personal growth first.' }
          ],
          sampleEn: 'Often yes. Parents may focus on stable jobs and income. By contrast, young people may chase interest or personal growth first.'
        },
        {
          id: 'goal_3',
          q: 'What problems can appear if someone changes plans too often?',
          tipZh: '频繁改计划的问题。',
          qType: 'proscons',
          angles: [
            { zh: '时间金钱浪费，项目总开不完', en: 'Frequent changes waste time and money because projects never finish.' },
            { zh: '自信受挫，也难获得他人信任', en: 'It can hurt confidence and make others less willing to trust you.' }
          ],
          sampleEn: 'Changing plans can show flexibility, but doing it too often wastes time and money. People may also lose confidence if nothing is finished.'
        }
      ]
    },
    {
      id: 'media_news',
      titleZh: '媒体与信息',
      titleEn: 'Media and information',
      relatedP2Title: '当地新闻',
      heatRank: 9,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'media_1',
          q: 'Why do people follow local news?',
          tipZh: '为什么看本地新闻。',
          qType: 'reason',
          angles: [
            { zh: '实用：交通、天气、社区活动直接影响生活', en: 'Local news covers traffic, weather, and events that affect daily life.' },
            { zh: '让人更了解所在城市，有归属感', en: 'It helps people feel connected to the place they live in.' }
          ],
          sampleEn: 'Local news is practical. It tells people about traffic, weather, and community events. It also helps them feel connected to their city.'
        },
        {
          id: 'media_2',
          q: 'What are the disadvantages of getting news only from social media?',
          tipZh: '只从社媒获取新闻的缺点。',
          qType: 'proscons',
          angles: [
            { zh: '谣言传播快，难辨真假', en: 'Rumors spread quickly and are hard to check.' },
            { zh: '算法推情绪化内容，容易片面理解', en: 'Algorithms push emotional clips, so people may see only one side.' }
          ],
          sampleEn: 'Social media is fast, but rumors spread easily. Short videos also push emotional content, so people may misunderstand complex issues.'
        },
        {
          id: 'media_3',
          q: 'How can the media help society solve problems?',
          tipZh: '媒体如何助力解决问题，要举例具体问题类型。',
          qType: 'solution',
          angles: [
            { zh: '曝光问题、解释原因，推动公众关注', en: 'Media can expose problems and explain causes to attract public attention.' },
            { zh: '传播正确做法与成功案例，促进行动', en: 'It can share good practices and success cases that encourage action.' }
          ],
          sampleEn: 'The media can expose social problems and explain why they matter. It can also share practical solutions so more people support helpful actions.'
        }
      ]
    },
    {
      id: 'sports',
      titleZh: '运动与健康',
      titleEn: 'Sport and health',
      relatedP2Title: '喜欢的现场体育赛事',
      heatRank: 10,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'sport_1',
          q: 'What are the benefits of children doing sports regularly?',
          tipZh: '儿童规律运动的好处。',
          qType: 'proscons',
          angles: [
            { zh: '增强体质，缓解久坐学习带来的疲劳', en: 'Regular sport improves fitness and reduces fatigue from sitting and studying.' },
            { zh: '团队项目练合作，也更容易交到朋友', en: 'Team sports teach cooperation and help kids make friends.' }
          ],
          sampleEn: 'Sports help kids keep fit and relieve study fatigue. Team games also teach cooperation and help them make friends.'
        },
        {
          id: 'sport_2',
          q: 'Do you think watching sports is as useful as playing sports?',
          tipZh: '看 vs 打，别两边都说成解压就结束。',
          qType: 'compare',
          angles: [
            { zh: '观看：娱乐、学习战术、情绪释放', en: 'Watching can entertain people and teach tactics.' },
            { zh: '参与：直接锻炼身体，健康收益更大', en: 'Playing sports trains the body directly, so health benefits are stronger.' }
          ],
          sampleEn: 'Watching sports can entertain people and teach tactics, but playing is better for fitness. Ideally people do both in balance.'
        },
        {
          id: 'sport_3',
          q: 'How can cities encourage more people to exercise?',
          tipZh: '城市如何鼓励锻炼，给可落地措施。',
          qType: 'solution',
          angles: [
            { zh: '建更多免费公园、步道和球场', en: 'Build more free parks, walking paths, and courts.' },
            { zh: '办社区活动，让上班族更容易参与', en: 'Organize community sports events that busy people can join easily.' }
          ],
          sampleEn: 'Cities can build more parks and free courts. Community events after work can also make exercise easier for busy people.'
        }
      ]
    },
    {
      id: 'business',
      titleZh: '商业与消费',
      titleEn: 'Business and shopping',
      relatedP2Title: '拥有成功商业的人',
      heatRank: 11,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'biz_1',
          q: 'Why do some small businesses become successful?',
          tipZh: '小生意成功原因。',
          qType: 'reason',
          angles: [
            { zh: '真正懂顾客需求，产品对口', en: 'They understand what customers really need and offer the right products.' },
            { zh: '质量稳定 + 服务好，带来回头客', en: 'Reliable quality and friendly service bring repeat customers.' }
          ],
          sampleEn: 'Successful shops understand real customer needs. Reliable quality and friendly service also make people come back.'
        },
        {
          id: 'biz_2',
          q: 'What are the advantages and disadvantages of online shopping?',
          tipZh: '网购利弊，别扯旅游。',
          qType: 'proscons',
          angles: [
            { zh: '优点：随时买、选择多、常更便宜', en: 'It is convenient anytime, with more choices and often lower prices.' },
            { zh: '缺点：易冲动下单，退换货麻烦，难验货', en: 'People may buy impulsively, returns are annoying, and quality is harder to check.' }
          ],
          sampleEn: 'Online shopping is convenient and often cheaper. However, people may buy things they do not need, and returning products can be annoying.'
        },
        {
          id: 'biz_3',
          q: 'How is shopping different for young people and older people?',
          tipZh: '购物习惯代际差异。',
          qType: 'compare',
          angles: [
            { zh: '年轻人更常网购、追新品与折扣活动', en: 'Young people shop online more and chase new products or sales.' },
            { zh: '年长者更信实体店，重视能摸到商品', en: 'Older people often prefer physical stores where they can check items in person.' }
          ],
          sampleEn: 'Young people enjoy online shopping and new brands. Older people often prefer physical stores where they can check quality themselves.'
        }
      ]
    },
    {
      id: 'buildings',
      titleZh: '建筑与城市',
      titleEn: 'Buildings and cities',
      relatedP2Title: '喜欢或不喜欢的高建筑',
      heatRank: 12,
      sourceNote: '当季公开回忆整理',
      questions: [
        {
          id: 'build_1',
          q: 'Why do cities build so many tall buildings nowadays?',
          tipZh: '为何多建高楼。',
          qType: 'reason',
          angles: [
            { zh: '城市土地贵、人口密，向上建更省地', en: 'Land is expensive and crowded, so building upward saves space.' },
            { zh: '公司与住宅需求集中在市中心', en: 'Companies and residents both need space in central areas.' }
          ],
          sampleEn: 'Tall buildings save land when cities are crowded. With growth, more companies and residents need space in the same central area.'
        },
        {
          id: 'build_2',
          q: 'What problems can high-rise buildings cause?',
          tipZh: '高楼带来的问题。',
          qType: 'proscons',
          angles: [
            { zh: '周边交通更堵，早晚高峰更挤', en: 'They can increase traffic and crowding around the area.' },
            { zh: '邻里互动变少，生活有压迫感', en: 'Neighbors may interact less, and dense towers can feel stressful.' }
          ],
          sampleEn: 'High-rises can increase traffic nearby. People may also feel stressed in crowded lifts, and neighbors interact less than in smaller communities.'
        },
        {
          id: 'build_3',
          q: 'How can governments make cities more livable?',
          tipZh: '宜居城市措施，要具体。',
          qType: 'solution',
          angles: [
            { zh: '加强公交与绿道，减少纯靠私家车', en: 'Improve public transport and green paths so people rely less on cars.' },
            { zh: '规划公园与限高，保留公共空间', en: 'Plan parks and height limits to protect public open space.' }
          ],
          sampleEn: 'Governments should invest in public transport and green spaces. Better planning can also reduce overcrowding and keep quiet public areas.'
        }
      ]
    }
  ]
};

if (typeof window !== 'undefined') {
  window.P3_DATA = P3_DATA;
}
