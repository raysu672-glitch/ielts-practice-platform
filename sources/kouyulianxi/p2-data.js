// P2 data - 6 大素材 + 56 道答题思路（2026年5-8月现行题库，含参考答案）
const P2_DATA = {
  materials: [
            {
      id: "yumeng",
      name: "朋友·雨萌",
      type: "人物",
      summary: "遇大事找她商量的挚友。扩句=解释钩子：说白了 → 比如（考研/选专业两版）",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "为什么是她",
          zhOutline: [
            "雨萌是我从小一起长大的朋友",
            "她乐观，也特别肯听人说话",
            "所以一遇到大事，我第一个会找她"
          ],
          hooks: [
            {
              hook: "雨萌是我从小一起长大的朋友",
              pattern: "explain",
              s1: "我们很熟，不是普通同学那种关系",
              s2: "我们以前住得很近，后来又上了同一所学校"
            },
            {
              hook: "她乐观，也特别肯听人说话",
              pattern: "explain",
              s1: "她不急着打断你，也不先下判断",
              s2: "跟她说话我会更敢讲真心话"
            },
            {
              hook: "所以一遇到大事，我第一个会找她",
              pattern: "explain",
              s1: "因为她靠得住，也听得进我说的话",
              s2: "学习或生活里一有难事，我会先想到她"
            }
          ],
          zh: "雨萌是我从小一起长大的朋友。我们很熟，不是普通同学那种关系，比如我们以前住得很近，后来又上了同一所学校。她乐观，也特别肯听人说话。说白了，她不急着打断你，也不先下判断，比如跟她说话我会更敢讲真心话。所以一遇到大事，我第一个会找她。说白了是她靠得住，也听得进我说的话，比如学习或生活里一有难事，我会先想到她。",
          en: "Yumeng is a friend I grew up with. In plain words, we know each other well—not just ordinary classmates. For example, we lived close by and later went to the same school. She's optimistic and really listens. In plain words, she doesn't cut you off or judge too quickly—for example, I dare to tell her what I really think. So when something big happens, she's the first person I go to. That means she's reliable and actually listens—for example, I think of her first whenever study or life gets hard."
        },
        {
          label: "主体事件（默认情况A·大学考研；亦可选情况B·高考选专业，见 variants）",
          zhOutline: [
            "大三那年，我不知道该读研还是工作",
            "我找雨萌在学校边走边说",
            "她让我先想清楚自己更想做什么",
            "后来我决定申请读研"
          ],
          hooks: [
            {
              hook: "大三那年，我不知道该读研还是工作",
              pattern: "explain",
              s1: "两边都有道理，我自己选不出来",
              s2: "一边想继续上学，一边又有人劝我先找工作"
            },
            {
              hook: "我找雨萌在学校边走边说",
              pattern: "explain",
              s1: "这件事一直压着我，心里很乱，想找人聊聊",
              s2: "我们慢慢走，我把两边的担心都说了，她先听完"
            },
            {
              hook: "她让我先想清楚自己更想做什么",
              pattern: "explain",
              s1: "别先被找工作吓到，先问自己想过什么样的生活",
              s2: "如果确定想继续读，就认真去准备"
            },
            {
              hook: "后来我决定申请读研",
              pattern: "explain",
              s1: "听完以后我清楚多了",
              s2: "我开始准备申请，一步一步往前走"
            }
          ],
          zh: "大三那年，我不知道该读研还是工作。说白了，两边都有道理，我自己选不出来，比如一边想继续上学，一边又有人劝我先找工作。我找雨萌在学校边走边说。说白了，这件事一直压着我，心里很乱，想找人聊聊，比如我们慢慢走，我把两边的担心都说了，她先听完。她让我先想清楚自己更想做什么。说白了，就是别先被找工作吓到，先问自己想过什么样的生活，比如如果确定想继续读，就认真去准备。后来我决定申请读研。说白了，听完以后我清楚多了，比如我开始准备申请，一步一步往前走。",
          en: "In my third year, I didn't know whether to do a master's or get a job. In plain words, both sides made sense and I couldn't choose—for example, I wanted to keep studying, but some people told me to work first. I asked Yumeng to walk and talk on campus. In plain words, it kept weighing on me and I felt mixed up, so I needed to talk—for example, we walked slowly, I told her both sides, and she listened first. She told me to figure out what I really wanted. In plain words, don't let finding a job scare you first; ask what kind of life you want—for example, if you're sure about further study, prepare seriously. Later I decided to apply for a master's. In plain words, I felt much clearer after that talk—for example, I started getting the application ready step by step."
        },
        {
          label: "结果与感受",
          zhOutline: [
            "她的话让我有了方向",
            "到现在我还很感激那次建议"
          ],
          hooks: [
            {
              hook: "她的话让我有了方向",
              pattern: "explain",
              s1: "不是给我一个标准答案，而是让我知道先问自己想要什么",
              s2: "从那以后，我做选择不那么容易被别人的焦虑带着走"
            },
            {
              hook: "到现在我还很感激那次建议",
              pattern: "explain",
              s1: "她说得很清楚，也很真心",
              s2: "这也让我更明白，为什么大事我会先找她"
            }
          ],
          zh: "她的话让我有了方向。说白了，不是给我一个标准答案，而是让我知道先问自己想要什么，比如从那以后，我做选择不那么容易被别人的焦虑带着走。到现在我还很感激那次建议。说白了，她说得很清楚，也很真心，比如这也让我更明白，为什么大事我会先找她。",
          en: "Her words gave me direction. In plain words, it wasn't a perfect answer—it showed me I should first ask what I really want. For example, since then I'm less easily pushed around by other people's worry when I choose. Even now I'm still grateful for that advice. In plain words, she spoke clearly and sincerely—for example, that also helps me understand why I go to her first when something big happens."
        }
      ],
      variants: [
        {
          id: "a",
          label: "情况A·大学考研",
          zhOutline: [
            "大三那年，我不知道该读研还是工作",
            "我找雨萌在学校边走边说",
            "她让我先想清楚自己更想做什么",
            "后来我决定申请读研"
          ],
          hooks: [
            {
              hook: "大三那年，我不知道该读研还是工作",
              pattern: "explain",
              s1: "两边都有道理，我自己选不出来",
              s2: "一边想继续上学，一边又有人劝我先找工作"
            },
            {
              hook: "我找雨萌在学校边走边说",
              pattern: "explain",
              s1: "这件事一直压着我，心里很乱，想找人聊聊",
              s2: "我们慢慢走，我把两边的担心都说了，她先听完"
            },
            {
              hook: "她让我先想清楚自己更想做什么",
              pattern: "explain",
              s1: "别先被找工作吓到，先问自己想过什么样的生活",
              s2: "如果确定想继续读，就认真去准备"
            },
            {
              hook: "后来我决定申请读研",
              pattern: "explain",
              s1: "听完以后我清楚多了",
              s2: "我开始准备申请，一步一步往前走"
            }
          ],
          zh: "大三那年，我不知道该读研还是工作。说白了，两边都有道理，我自己选不出来，比如一边想继续上学，一边又有人劝我先找工作。我找雨萌在学校边走边说。说白了，这件事一直压着我，心里很乱，想找人聊聊，比如我们慢慢走，我把两边的担心都说了，她先听完。她让我先想清楚自己更想做什么。说白了，就是别先被找工作吓到，先问自己想过什么样的生活，比如如果确定想继续读，就认真去准备。后来我决定申请读研。说白了，听完以后我清楚多了，比如我开始准备申请，一步一步往前走。",
          en: "In my third year, I didn't know whether to do a master's or get a job. In plain words, both sides made sense and I couldn't choose—for example, I wanted to keep studying, but some people told me to work first. I asked Yumeng to walk and talk on campus. In plain words, it kept weighing on me and I felt mixed up, so I needed to talk—for example, we walked slowly, I told her both sides, and she listened first. She told me to figure out what I really wanted. In plain words, don't let finding a job scare you first; ask what kind of life you want—for example, if you're sure about further study, prepare seriously. Later I decided to apply for a master's. In plain words, I felt much clearer after that talk—for example, I started getting the application ready step by step."
        },
        {
          id: "b",
          label: "情况B·高考选专业",
          zhOutline: [
            "高中毕业后，我的计划全乱了",
            "我在名校冷专业和普通学校热专业之间很难选",
            "雨萌让我跟着自己真正喜欢的走",
            "后来我选了喜欢的专业，也证明这样更好"
          ],
          hooks: [
            {
              hook: "高中毕业后，我的计划全乱了",
              pattern: "explain",
              s1: "高考没考好，原来想走的路走不通了",
              s2: "我很着急，也很丧"
            },
            {
              hook: "我在名校冷专业和普通学校热专业之间很难选",
              pattern: "explain",
              s1: "一边学校更好但我不喜欢，一边学校普通但我真想学",
              s2: "怎么选都像在放弃一点东西"
            },
            {
              hook: "雨萌让我跟着自己真正喜欢的走",
              pattern: "explain",
              s1: "喜欢比学校排名更重要",
              s2: "她要我去做真正想做的事"
            },
            {
              hook: "后来我选了喜欢的专业，也证明这样更好",
              pattern: "explain",
              s1: "我最后选了自己喜欢的专业",
              s2: "后来上课更有劲，也说明这个决定是对的"
            }
          ],
          zh: "高中毕业后，我的计划全乱了。说白了，高考没考好，原来想走的路走不通了，比如我很着急，也很丧。我在名校冷专业和普通学校热专业之间很难选。说白了，一边学校更好但我不喜欢，一边学校普通但我真想学，比如怎么选都像在放弃一点东西。雨萌让我跟着自己真正喜欢的走。说白了，喜欢比学校排名更重要，比如她要我去做真正想做的事。后来我选了喜欢的专业，也证明这样更好。说白了，我最后选了自己喜欢的专业，比如后来上课更有劲，也说明这个决定是对的。",
          en: "After high school, my plan fell apart. In plain words, I didn't do well enough in the exam, so the path I wanted was gone—for example, I felt anxious and low. I had a hard choice between a better university with a major I didn't like and an ordinary university with a major I really wanted. In plain words, either way felt like giving something up. Yumeng told me to follow what I truly enjoy. In plain words, liking the subject matters more than the ranking—for example, she told me to do what I really want. Later I chose the major I liked, and it proved better. In plain words, I picked what I liked—for example, I studied with more energy later, and that showed the decision was right."
        }
      ],
      endingTip: "她的话给了我方向，我现在还很感激"
    },
    {
      id: "sun",
      name: "明星·孙颖莎",
      type: "人物",
      summary: "年轻顶尖的乒乓球选手。扩句=解释钩子：说白了 → 比如（身份→夺金→爆红与感受）",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "她是谁",
          zhOutline: [
            "我想说的人是乒乓球选手孙颖莎",
            "她很年轻，但成绩已经很顶尖"
          ],
          hooks: [
            {
              hook: "我想说的人是乒乓球选手孙颖莎",
              pattern: "explain",
              s1: "中国队很出名的那个运动员",
              s2: "很多人一提乒乓球就会想到她"
            },
            {
              hook: "她很年轻，但成绩已经很顶尖",
              pattern: "explain",
              s1: "年纪不大，但已经赢过很多重要比赛",
              s2: "国内外大赛里常能看到她打得很拼"
            }
          ],
          zh: "我想说的人是乒乓球选手孙颖莎。说白了，就是中国队很出名的那个运动员，比如很多人一提乒乓球就会想到她。她很年轻，但成绩已经很顶尖。说白了，年纪不大，但已经赢过很多重要比赛，比如国内外大赛里常能看到她打得很拼。",
          en: "The person I want to talk about is the table tennis player Sun Yingsha. In plain words, she's a well-known athlete on the Chinese team—for example, a lot of people think of her when table tennis comes up. She's still young, but her results are already top-level. In plain words, she isn't that old, yet she's already won many big matches—for example, you often see her fighting hard in major events."
        },
        {
          label: "高光时刻",
          zhOutline: [
            "去年巴黎奥运，她和王楚钦打混双",
            "压力很大，但他们还是拿下了金牌"
          ],
          hooks: [
            {
              hook: "去年巴黎奥运，她和王楚钦打混双",
              pattern: "explain",
              s1: "那是很大的舞台，混双又特别需要两个人配合",
              s2: "我看的时候也很紧张，觉得每一分都很关键"
            },
            {
              hook: "压力很大，但他们还是拿下了金牌",
              pattern: "explain",
              s1: "中间也有不好打的时候，但关键分他们打得很稳",
              s2: "最后赢了强队，拿到金牌"
            }
          ],
          zh: "最让我记得的，是去年巴黎奥运。她和王楚钦打混双。说白了，那是很大的舞台，混双又特别需要两个人配合，比如我看的时候也很紧张，觉得每一分都很关键。压力很大，但他们还是拿下了金牌。说白了，中间也有不好打的时候，但关键分他们打得很稳，比如最后赢了强队，拿到金牌。",
          en: "What I remember most is last year's Paris Olympics, when she played mixed doubles with Wang Chuqin. In plain words, it was a huge stage and mixed doubles needs real teamwork—for example, I was nervous watching and every point felt important. The pressure was high, but they still won gold. In plain words, there were hard moments, but they stayed steady on the key points—for example, they beat a strong team and took the gold medal."
        },
        {
          label: "爆红之后与我的感受",
          zhOutline: [
            "夺金之后，她一下子更红了",
            "大家特别喜欢她的酒窝，还做成贴纸",
            "我更佩服她抗压拿金的能力"
          ],
          hooks: [
            {
              hook: "夺金之后，她一下子更红了",
              pattern: "explain",
              s1: "关注她的人变多了，不只是球迷",
              s2: "手机上、街上到处都能看到她"
            },
            {
              hook: "大家特别喜欢她的酒窝，还做成贴纸",
              pattern: "explain",
              s1: "大家喜欢她可爱、好亲近的一面",
              s2: "聊天软件里常有她的贴纸，气氛一下子轻松"
            },
            {
              hook: "我更佩服她抗压拿金的能力",
              pattern: "explain",
              s1: "贴纸很好玩，但我更看重她高压下还能打好",
              s2: "我考试或当众说话紧张时，也会想起要把该做的做好"
            }
          ],
          zh: "夺金之后，她一下子更红了。说白了，关注她的人变多了，不只是球迷，比如手机上、街上到处都能看到她。大家特别喜欢她的酒窝，还做成贴纸。说白了，大家喜欢她可爱、好亲近的一面，比如聊天软件里常有她的贴纸，气氛一下子轻松。我更佩服她抗压拿金的能力。说白了，贴纸很好玩，但我更看重她高压下还能打好，比如我考试或当众说话紧张时，也会想起要把该做的做好。",
          en: "After the gold medal, she became even more popular. In plain words, more people followed her, not only sports fans—for example, you could see her everywhere on phones and in the streets. People especially like her dimples and made stickers of her. In plain words, they like how cute and approachable she feels—for example, her stickers in chat apps lighten the mood fast. I admire more how she won gold under pressure. In plain words, stickers are fun, but what matters more is that she could still play well under pressure—for example, when I get nervous before an exam or speaking in public, I also remind myself to do what I need to do."
        }
      ],
      endingTip: "夺金后更红；我更佩服她压力下还能打好"
    },
    {
      id: "movie",
      name: "影视·夏洛特烦恼",
      type: "影视",
      summary: "沈腾马丽的时间旅行喜剧。扩句=解释钩子：说白了 → 比如",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "这是什么电影",
          zhOutline: [
            "我想说的是电影《夏洛特烦恼》",
            "沈腾和马丽演的，特别好笑"
          ],
          hooks: [
            {
              hook: "我想说的是电影《夏洛特烦恼》",
              pattern: "explain",
              s1: "一部中国喜剧，讲的是时间旅行",
              s2: "主角能回到高中，重新选人生"
            },
            {
              hook: "沈腾和马丽演的，特别好笑",
              pattern: "explain",
              s1: "他们是很有名的喜剧搭档",
              s2: "两个人一搭档，很多桥段我都想笑"
            }
          ],
          zh: "我想说的是电影《夏洛特烦恼》。说白了，一部中国喜剧，讲的是时间旅行，比如主角能回到高中，重新选人生。沈腾和马丽演的，特别好笑。说白了，他们是很有名的喜剧搭档，比如两个人一搭档，很多桥段我都想笑。",
          en: "I'd like to talk about the movie Xialuotefannao. In plain words, it's a Chinese comedy about time travel—for example, the main character can go back to high school and choose life again. It stars Shen Teng and Ma Li, and it's really funny. In plain words, they're a famous comedy pair—for example, once they team up, a lot of scenes make me want to laugh."
        },
        {
          label: "主要情节",
          zhOutline: [
            "夏洛穿越回高中，去追梦中女孩秋雅",
            "十年后他成功了，却查出得了重病"
          ],
          hooks: [
            {
              hook: "夏洛穿越回高中，去追梦中女孩秋雅",
              pattern: "explain",
              s1: "他没再选现在的妻子马丽，而是换了一条路",
              s2: "他想弥补年轻时的遗憾，把梦想女孩追到手"
            },
            {
              hook: "十年后他成功了，却查出得了重病",
              pattern: "explain",
              s1: "表面上看，名利爱情都有了",
              s2: "医生告诉他已经病得很重，好运一下子翻了"
            }
          ],
          zh: "夏洛穿越回高中，去追梦中女孩秋雅。说白了，他没再选现在的妻子马丽，而是换了一条路，比如他想弥补年轻时的遗憾，把梦想女孩追到手。十年后他成功了，却查出得了重病。说白了，表面上看名利爱情都有了，比如医生告诉他已经病得很重，好运一下子翻了。",
          en: "Xialuo goes back to high school and chases his dream girl, Qiuya. In plain words, he doesn't choose his real wife Ma Li again—he takes another path. For example, he wants to fix young regrets and win the girl he dreamed of. Ten years later he succeeds, but then finds out he's seriously ill. In plain words, it looks like he has fame, money and love—for example, the doctor says he's already very sick, and his luck turns over at once."
        },
        {
          label: "结局与感受",
          zhOutline: [
            "秋雅离开他，马丽却来照顾他",
            "他明白爱最重要，最后发现是一场梦"
          ],
          hooks: [
            {
              hook: "秋雅离开他，马丽却来照顾他",
              pattern: "explain",
              s1: "困难时刻，谁真的在身边就看出来了",
              s2: "秋雅不只离开，还骗走他的钱；马丽反而出现帮忙"
            },
            {
              hook: "他明白爱最重要，最后发现是一场梦",
              pattern: "explain",
              s1: "他终于懂了，真正宝贵的不是名气",
              s2: "梦醒之后，这份感悟还留着，我也觉得很触动"
            }
          ],
          zh: "秋雅离开他，马丽却来照顾他。说白了，困难时刻谁真的在身边就看出来了，比如秋雅不只离开，还骗走他的钱，马丽反而出现帮忙。他明白爱最重要，最后发现是一场梦。说白了，他终于懂了真正宝贵的不是名气，比如梦醒之后这份感悟还留着，我也觉得很触动。",
          en: "Qiuya leaves him, but Ma Li comes to take care of him. In plain words, hard times show who really stays—for example, Qiuya not only leaves but also tricks him out of his money, while Ma Li shows up to help. He realizes love matters most, and in the end it was all a dream. In plain words, he finally understands fame isn't the real treasure—for example, after he wakes up, that feeling stays, and I find it touching too."
        }
      ],
      endingTip: "他明白爱最重要；梦醒后这份感悟还在"
    },
    {
      id: "badminton",
      name: "事件·羽毛球",
      type: "事件",
      summary: "压力大开始打球：交友、变外向、暂时忘掉学业压力。扩句=说白了→比如",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "为什么开始打",
          zhOutline: [
            "那段时间申请和学英语把我累坏了",
            "朋友建议我运动，我就开始打羽毛球"
          ],
          hooks: [
            {
              hook: "那段时间申请和学英语把我累坏了",
              pattern: "explain",
              s1: "事情太多，人又累又难集中",
              s2: "有时坐在书桌前，脑子转不动"
            },
            {
              hook: "朋友建议我运动，我就开始打羽毛球",
              pattern: "explain",
              s1: "他们觉得我该出门出出汗",
              s2: "我听了建议，约场去打球"
            }
          ],
          zh: "那段时间申请和学英语把我累坏了。说白了，事情太多，人又累又难集中，比如有时坐在书桌前，脑子转不动。朋友建议我运动，我就开始打羽毛球。说白了，他们觉得我该出门出出汗，比如我听了建议，约场去打球。",
          en: "For a while, applying for programs and studying English wore me out. In plain words, there was too much to do—I was tired and couldn't focus. For example, sometimes I sat at my desk and my mind just wouldn't work. Friends suggested exercise, so I started playing badminton. In plain words, they thought I should go out and sweat a bit—for example, I took the advice and booked a court."
        },
        {
          label: "打球带来的变化",
          zhOutline: [
            "羽毛球常要找搭档，我认识了新朋友",
            "我也变得更外向了"
          ],
          hooks: [
            {
              hook: "羽毛球常要找搭档，我认识了新朋友",
              pattern: "explain",
              s1: "球场上经常和不太熟的人一组",
              s2: "后来我们周末常约着一起打"
            },
            {
              hook: "我也变得更外向了",
              pattern: "explain",
              s1: "以前我不太主动跟人说话",
              s2: "打球之后更敢打招呼、更敢约人了"
            }
          ],
          zh: "羽毛球常要找搭档，我认识了新朋友。说白了，球场上经常和不太熟的人一组，比如后来我们周末常约着一起打。我也变得更外向了。说白了，以前我不太主动跟人说话，比如打球之后更敢打招呼、更敢约人了。",
          en: "Badminton often needs a partner, so I met new friends. In plain words, I often team up with people I don't know well at the court—for example, later we started meeting on weekends to play. I also became more outgoing. In plain words, I used to be slow to talk to people—for example, after playing I dare to say hi and make plans more."
        },
        {
          label: "对我心情的帮助",
          zhOutline: [
            "打球时我能暂时忘掉学习压力",
            "挥拍的时候脑子会清一点"
          ],
          hooks: [
            {
              hook: "打球时我能暂时忘掉学习压力",
              pattern: "explain",
              s1: "那一会儿我只管眼前的球",
              s2: "申请和英语的烦心事先放一边"
            },
            {
              hook: "挥拍的时候脑子会清一点",
              pattern: "explain",
              s1: "耳朵里差不多只有球拍和风声",
              s2: "打完再回去学，状态会好一些"
            }
          ],
          zh: "打球时我能暂时忘掉学习压力。说白了，那一会儿我只管眼前的球，比如申请和英语的烦心事先放一边。挥拍的时候脑子会清一点。说白了，耳朵里差不多只有球拍和风声，比如打完再回去学，状态会好一些。",
          en: "When I play, I can forget study pressure for a while. In plain words, for that moment I only watch the shuttle—for example, worries about applications and English are put aside. When I swing the racket, my mind feels clearer. In plain words, I mostly hear the racket and the wind—for example, when I go back to study after that, I feel better."
        }
      ],
      endingTip: "打球时能暂时忘掉压力，脑子也会清一点"
    },
    {
      id: "bear",
      name: "物品·小熊玩偶（女生向）",
      type: "物品",
      audience: "girl",
      summary: "好友送的小熊：软、可爱，高考压力时能让人平静。扩句=说白了→比如",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "它怎么来的",
          zhOutline: [
            "小学时好友送给我一只小熊",
            "它小小的，毛很软，还系着红蝴蝶结"
          ],
          hooks: [
            {
              hook: "小学时好友送给我一只小熊",
              pattern: "explain",
              s1: "生日礼物，她知道我喜欢软软可爱的东西",
              s2: "是 Jellycat 的泰迪熊，她特意挑的"
            },
            {
              hook: "它小小的，毛很软，还系着红蝴蝶结",
              pattern: "explain",
              s1: "看起来很治愈，抱着也舒服",
              s2: "棕色的身子，脖子上那条红丝带特别好看"
            }
          ],
          zh: "小学时好友送给我一只小熊。说白了，生日礼物，她知道我喜欢软软可爱的东西，比如是 Jellycat 的泰迪熊，她特意挑的。它小小的，毛很软，还系着红蝴蝶结。说白了，看起来很治愈，抱着也舒服，比如棕色的身子，脖子上那条红丝带特别好看。",
          en: "In primary school, my best friend gave me a little bear. In plain words, it was a birthday gift—she knew I loved soft cute things. For example, it was a Jellycat teddy she picked carefully. It's small, with very soft fur and a red bow. In plain words, it looks comforting and feels nice to hold—for example, it's brown, and the red ribbon around its neck looks lovely."
        },
        {
          label: "它怎么帮到我",
          zhOutline: [
            "高考前我压力大到睡不着",
            "抱着它，会平静一些，也更容易睡着"
          ],
          hooks: [
            {
              hook: "高考前我压力大到睡不着",
              pattern: "explain",
              s1: "白天学，晚上脑子还在转",
              s2: "躺下很久也进不了睡眠"
            },
            {
              hook: "抱着它，会平静一些，也更容易睡着",
              pattern: "explain",
              s1: "手上有个软东西，心会定一点",
              s2: "那几周它几乎天天陪我入睡"
            }
          ],
          zh: "高考前我压力大到睡不着。说白了，白天学，晚上脑子还在转，比如躺下很久也进不了睡眠。抱着它，会平静一些，也更容易睡着。说白了，手上有个软东西，心会定一点，比如那几周它几乎天天陪我入睡。",
          en: "Before the college entrance exam, I was so stressed I couldn't sleep. In plain words, I studied all day and my mind kept running at night—for example, I'd lie down for a long time and still not fall asleep. Holding the bear made me calmer and helped me sleep. In plain words, having something soft in my arms settled me a bit—for example, for those weeks it almost went to bed with me every night."
        },
        {
          label: "它现在对我意味着什么",
          zhOutline: [
            "后来一紧张或难过，我还会抱一抱它",
            "它像一个老朋友，陪我过了很多重要时刻"
          ],
          hooks: [
            {
              hook: "后来一紧张或难过，我还会抱一抱它",
              pattern: "explain",
              s1: "不一定解决问题，但能让我缓一下",
              s2: "考试前、心情差的时候我会拿出来"
            },
            {
              hook: "它像一个老朋友，陪我过了很多重要时刻",
              pattern: "explain",
              s1: "从小学到现在，它一直在",
              s2: "所以它对我不只是玩具，更像陪伴"
            }
          ],
          zh: "后来一紧张或难过，我还会抱一抱它。说白了，不一定解决问题，但能让我缓一下，比如考试前、心情差的时候我会拿出来。它像一个老朋友，陪我过了很多重要时刻。说白了，从小学到现在它一直在，比如所以它对我不只是玩具，更像陪伴。",
          en: "Later, whenever I feel nervous or upset, I still hug it for a while. In plain words, it may not fix the problem, but it helps me slow down—for example, before exams or on low days I take it out. It feels like an old friend that has been with me through many important moments. In plain words, it's been there since primary school—for example, so to me it isn't just a toy; it's company."
        }
      ],
      endingTip: "它像老朋友，陪我过了很多重要时刻"
    },
    {
      id: "basketball",
      name: "物品·篮球（男生向）",
      type: "物品",
      audience: "boy",
      summary: "父亲送的篮球：高考压力时投篮能让人清醒。扩句=说白了→比如",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "它怎么来的",
          zhOutline: [
            "初中时父亲送给我一个篮球",
            "球是橙色的，手感很好，看起来很专业"
          ],
          hooks: [
            {
              hook: "初中时父亲送给我一个篮球",
              pattern: "explain",
              s1: "生日礼物，他知道我喜欢运动",
              s2: "他特意挑了这个球送给我"
            },
            {
              hook: "球是橙色的，手感很好，看起来很专业",
              pattern: "explain",
              s1: "摸着结实，线条也很清楚",
              s2: "拿到手里就想下场投两下"
            }
          ],
          zh: "初中时父亲送给我一个篮球。说白了，生日礼物，他知道我喜欢运动，比如他特意挑了这个球送给我。球是橙色的，手感很好，看起来很专业。说白了，摸着结实，线条也很清楚，比如拿到手里就想下场投两下。",
          en: "In middle school, my father gave me a basketball. In plain words, it was a birthday gift—he knew I loved sports. For example, he picked this ball carefully for me. It's orange, feels good in the hand, and looks professional. In plain words, it feels solid and the lines are clear—for example, once I hold it I want to go shoot a few."
        },
        {
          label: "它怎么帮到我",
          zhOutline: [
            "高考前我压力大到学不进去",
            "下楼投篮后，我会平静一些，脑子也更清醒"
          ],
          hooks: [
            {
              hook: "高考前我压力大到学不进去",
              pattern: "explain",
              s1: "坐在书桌前，眼睛看着书，心不在焉",
              s2: "越急越看不进去"
            },
            {
              hook: "下楼投篮后，我会平静一些，脑子也更清醒",
              pattern: "explain",
              s1: "球进筐的那一下，烦心事会轻一点",
              s2: "活动一会儿再回去，状态会好很多"
            }
          ],
          zh: "高考前我压力大到学不进去。说白了，坐在书桌前眼睛看着书，心不在焉，比如越急越看不进去。下楼投篮后，我会平静一些，脑子也更清醒。说白了，球进筐的那一下烦心事会轻一点，比如活动一会儿再回去，状态会好很多。",
          en: "Before the college entrance exam, I was so stressed I couldn't study. In plain words, I sat at my desk looking at the book but my mind wasn't there—for example, the more anxious I got, the less I could take in. After I went downstairs to shoot, I felt calmer and clearer. In plain words, when the ball went through the hoop, the worry felt lighter—for example, after moving a bit I studied in a better state."
        },
        {
          label: "它现在对我意味着什么",
          zhOutline: [
            "后来一紧张或烦躁，我还会拿它去投一会儿",
            "它像一个老朋友，陪我过了很多重要时刻"
          ],
          hooks: [
            {
              hook: "后来一紧张或烦躁，我还会拿它去投一会儿",
              pattern: "explain",
              s1: "不一定马上解决问题，但能让我换口气",
              s2: "空地或球场投十几分钟，人会松一点"
            },
            {
              hook: "它像一个老朋友，陪我过了很多重要时刻",
              pattern: "explain",
              s1: "从初中到现在，这个球一直在",
              s2: "所以它对我不只是器材，更像陪伴"
            }
          ],
          zh: "后来一紧张或烦躁，我还会拿它去投一会儿。说白了，不一定马上解决问题，但能让我换口气，比如空地或球场投十几分钟，人会松一点。它像一个老朋友，陪我过了很多重要时刻。说白了，从初中到现在这个球一直在，比如所以它对我不只是器材，更像陪伴。",
          en: "Later, whenever I feel nervous or restless, I still take it out and shoot for a while. In plain words, it may not fix things at once, but it lets me breathe—for example, ten-odd minutes on an open court and I loosen up. It feels like an old friend that has been with me through many important moments. In plain words, the ball has been there since middle school—for example, so to me it isn't just gear; it's company."
        }
      ],
      endingTip: "它像老朋友，陪我过了很多重要时刻"
    },
    {
      id: "tianchi",
      name: "地点·长白山天池",
      type: "地点",
      summary: "东北长白山天池：爬很长的阶梯，登顶看到湖面很震撼。扩句=说白了→比如",

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "这是什么地方",
          zhOutline: [
            "我想说的是长白山的天池",
            "在东北，自然风景很原始，湖在山顶"
          ],
          hooks: [
            {
              hook: "我想说的是长白山的天池",
              pattern: "explain",
              s1: "中国东北很有名的景点",
              s2: "很多人专门跑去看那个山顶上的湖"
            },
            {
              hook: "在东北，自然风景很原始，湖在山顶",
              pattern: "explain",
              s1: "不是城市公园那种修得很整齐的感觉",
              s2: "天池的意思差不多就是“天上的池子”"
            }
          ],
          zh: "我想说的是长白山的天池。说白了，中国东北很有名的景点，比如很多人专门跑去看那个山顶上的湖。在东北，自然风景很原始，湖在山顶。说白了，不是城市公园那种修得很整齐的感觉，比如天池的意思差不多就是“天上的池子”。",
          en: "I'd like to talk about Tianchi on Changbai Mountain. In plain words, it's a famous place in northeast China—for example, many people travel just to see that lake on the mountain top. It's in the northeast, the nature feels raw, and the lake sits up high. In plain words, it isn't a neat city park—for example, Tianchi basically means “the pond of heaven.”"
        },
        {
          label: "怎么上去的",
          zhOutline: [
            "要先爬很长很长的阶梯",
            "路上风景很好，空气也很新"
          ],
          hooks: [
            {
              hook: "要先爬很长很长的阶梯",
              pattern: "explain",
              s1: "腿会酸，人也容易喘",
              s2: "我们一边爬一边停，花了不少时间"
            },
            {
              hook: "路上风景很好，空气也很新",
              pattern: "explain",
              s1: "往下看是山，往上看是很蓝的天",
              s2: "就算累，也不太想抱怨"
            }
          ],
          zh: "要先爬很长很长的阶梯。说白了，腿会酸，人也容易喘，比如我们一边爬一边停，花了不少时间。路上风景很好，空气也很新。说白了，往下看是山，往上看是很蓝的天，比如就算累，也不太想抱怨。",
          en: "First you have to climb a very long staircase. In plain words, your legs get sore and you get out of breath—for example, we climbed and stopped again and again, and it took a long time. The views on the way are great, and the air feels fresh. In plain words, you look down at mountains and up at a very blue sky—for example, even when you're tired, you don't really want to complain."
        },
        {
          label: "登顶之后",
          zhOutline: [
            "到山顶终于看到天池",
            "湖又大又干净，一看就觉得值了"
          ],
          hooks: [
            {
              hook: "到山顶终于看到天池",
              pattern: "explain",
              s1: "那一刻前面的累突然有了回报",
              s2: "大家都会停下来盯着看一会儿"
            },
            {
              hook: "湖又大又干净，一看就觉得值了",
              pattern: "explain",
              s1: "阳光下亮得像一块大宝石",
              s2: "爬阶梯流的汗，我觉得都值了"
            }
          ],
          zh: "到山顶终于看到天池。说白了，那一刻前面的累突然有了回报，比如大家都会停下来盯着看一会儿。湖又大又干净，一看就觉得值了。说白了，阳光下亮得像一块大宝石，比如爬阶梯流的汗，我觉得都值了。",
          en: "At the top we finally saw Tianchi. In plain words, at that moment all the tiredness suddenly felt worth it—for example, everyone stops and stares for a while. The lake is huge and clean, and one look makes it feel worth the climb. In plain words, under the sun it shines like a big jewel—for example, I felt all the sweat from the stairs was worth it."
        }
      ],
      endingTip: "一看到天池，爬阶梯的汗都值了"
    },
    {
      id: "robot",
      name: "物品·扫地机器人",
      type: "物品",
      summary: "（补充）养猫后买扫地机：连手机、省时间。扩句=说白了→比如",
      optional: true,

  expandPatterns: {
    explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
  },

      steps: [
        {
          label: "为什么买",
          zhOutline: [
            "我想说的是家里的扫地机器人",
            "因为养了两只猫，猫毛太多，我又忙"
          ],
          hooks: [
            {
              hook: "我想说的是家里的扫地机器人",
              pattern: "explain",
              s1: "几年前买的，专门帮打扫",
              s2: "现在几乎每天都会用到"
            },
            {
              hook: "因为养了两只猫，猫毛太多，我又忙",
              pattern: "explain",
              s1: "地上老是一层毛，自己扫很累",
              s2: "那时学业也紧，没时间天天收拾"
            }
          ],
          zh: "我想说的是家里的扫地机器人。说白了，几年前买的，专门帮打扫，比如现在几乎每天都会用到。因为养了两只猫，猫毛太多，我又忙。说白了，地上老是一层毛，自己扫很累，比如那时学业也紧，没时间天天收拾。",
          en: "I'd like to talk about our robot vacuum. In plain words, I bought it a few years ago to help with cleaning—for example, we use it almost every day now. I got it because we have two cats, there's too much fur, and I was busy. In plain words, the floor was always covered in fur and sweeping by hand was tiring—for example, I was also busy with study and had no time to tidy every day."
        },
        {
          label: "它怎么好用",
          zhOutline: [
            "连上手机点几下就能扫",
            "还能扫到边角，扫完会自己回充"
          ],
          hooks: [
            {
              hook: "连上手机点几下就能扫",
              pattern: "explain",
              s1: "不用自己拖着机器满屋跑",
              s2: "可以设每天定时，也可以临时开一下"
            },
            {
              hook: "还能扫到边角，扫完会自己回充",
              pattern: "explain",
              s1: "有些地方人手不好够，它能进去",
              s2: "弄完自己回底座，我几乎不用管"
            }
          ],
          zh: "连上手机点几下就能扫。说白了，不用自己拖着机器满屋跑，比如可以设每天定时，也可以临时开一下。还能扫到边角，扫完会自己回充。说白了，有些地方人手不好够，它能进去，比如弄完自己回底座，我几乎不用管。",
          en: "I connect it to my phone and start cleaning with a few taps. In plain words, I don't have to drag a machine around the house—for example, I can set a daily schedule or start it when I need. It can also reach corners and goes back to charge by itself. In plain words, it gets into places that are hard to clean by hand—for example, when it's done it returns to the base and I barely need to watch it."
        },
        {
          label: "用完什么感受",
          zhOutline: [
            "打扫不再是大事",
            "它帮我省了很多时间，家里也更整洁"
          ],
          hooks: [
            {
              hook: "打扫不再是大事",
              pattern: "explain",
              s1: "以前猫毛一多我就头疼",
              s2: "现在基本交给它就行"
            },
            {
              hook: "它帮我省了很多时间，家里也更整洁",
              pattern: "explain",
              s1: "省下的时间能用来学习或休息",
              s2: "进门也不容易看到到处是毛"
            }
          ],
          zh: "打扫不再是大事。说白了，以前猫毛一多我就头疼，比如现在基本交给它就行。它帮我省了很多时间，家里也更整洁。说白了，省下的时间能用来学习或休息，比如进门也不容易看到到处是毛。",
          en: "Cleaning is no longer a big deal. In plain words, too much cat fur used to give me a headache—for example, now I mostly leave it to the robot. It saves me a lot of time and keeps the home cleaner. In plain words, the time saved can go to study or rest—for example, when I walk in I'm less likely to see fur everywhere."
        }
      ],
      endingTip: "打扫不再是大事，它帮我省时间"
    },
    {
      id: "linlin",
      name: "人物·表妹琳琳",
      type: "人物",
      summary: "（补充）想当护士的表妹：医院志愿后动念，耐心适合照顾人。扩句=说白了→比如",
      optional: true,
      expandPatterns: {
        explain: { id: "explain", slogan: "说白了 → 比如", q1: "说白了？", q2: "比如？" }
      },
      steps: [
        {
          label: "她是谁",
          zhOutline: [
            "我想说的是表妹琳琳",
            "我们从小亲戚聚会就熟",
            "她性格耐心，也愿意照顾人"
          ],
          hooks: [
            {
              hook: "我想说的是表妹琳琳",
              pattern: "explain",
              s1: "她比我小几岁，是家里最小的一辈之一",
              s2: "过年过节总能见到，后来也常视频"
            },
            {
              hook: "她性格耐心，也愿意照顾人",
              pattern: "explain",
              s1: "别人讲麻烦事她不急着打断",
              s2: "家里有人生病，她也爱跟着跑前跑后"
            }
          ],
          zh: "我想说的是表妹琳琳。说白了，她比我小几岁，是家里最小的一辈之一，比如过年过节总能见到，后来也常视频。我们从小亲戚聚会就熟。她性格耐心，也愿意照顾人。说白了，别人讲麻烦事她不急着打断，比如家里有人生病，她也爱跟着跑前跑后。",
          en: "I'd like to talk about my cousin Linlin. In plain words, she's a few years younger and one of the youngest in the family—for example, we always meet at festivals and later often video-call. We've known each other since family gatherings as kids. She's patient and willing to look after people. In plain words, she doesn't rush to interrupt when someone talks about troubles—for example, when someone at home is ill she likes to help."
        },
        {
          label: "为什么想学医/护理",
          zhOutline: [
            "高中时她去医院做志愿者",
            "看到护士把病人照料好，她觉得很有意义",
            "从那时起她想正式走护理方向"
          ],
          hooks: [
            {
              hook: "高中时她去医院做志愿者",
              pattern: "explain",
              s1: "学校组织的短期志愿",
              s2: "她负责指路、陪老人聊天这类小事"
            },
            {
              hook: "从那时起她想正式走护理方向",
              pattern: "explain",
              s1: "不是一时冲动，回家后还查专业和学校",
              s2: "跟父母说以后想考护理相关专业"
            }
          ],
          zh: "高中时她去医院做志愿者。说白了，那是学校组织的短期志愿，比如她负责指路、陪老人聊天这类小事。看到护士把病人照料好，她觉得很有意义。从那时起她想正式走护理方向。说白了，不是一时冲动，回家后还查专业和学校，比如跟父母说以后想考护理相关专业。",
          en: "In high school she volunteered at a hospital. In plain words, it was a short school programme—for example, she helped with directions and chatting with elderly patients. Seeing nurses look after patients well made her feel the work was meaningful. From then on she wanted to pursue nursing properly. In plain words, it wasn't a sudden whim—she researched programmes at home—for example, she told her parents she wanted to apply for nursing-related studies."
        },
        {
          label: "计划和我的看法",
          zhOutline: [
            "她计划先读护理，再进病房工作",
            "以后再决定要不要深造",
            "我支持她，觉得她真的适合"
          ],
          hooks: [
            {
              hook: "她计划先读护理，再进病房工作",
              pattern: "explain",
              s1: "先把基础技能学扎实",
              s2: "想从最贴近病人的岗位做起"
            },
            {
              hook: "我支持她，觉得她真的适合",
              pattern: "explain",
              s1: "她不怕琐碎，也有耐心",
              s2: "看到别人被照顾好，她会特别有成就感"
            }
          ],
          zh: "她计划先读护理，再进病房工作。说白了，先把基础技能学扎实，比如想从最贴近病人的岗位做起。以后再决定要不要深造。我支持她，觉得她真的适合。说白了，她不怕琐碎，也有耐心，比如看到别人被照顾好，她会特别有成就感。",
          en: "She plans to study nursing first, then work on a ward. In plain words, she wants solid basic skills—for example, starting in a role closest to patients. Later she can decide whether to study further. I support her and think she truly fits. In plain words, she isn't afraid of small tasks and has patience—for example, she feels proud when people are well looked after."
        }
      ],
      endingTip: "我支持她：耐心、适合照顾人"
    }
  ],

  questions:       [
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
      "materialHint": "主体换成表弟：压力大→开始打球→交友变外向。你的骄傲来自他的坚持，不要用「我忘却学业压力」收尾。",
      "endingTip": "看到他用运动把自己拉出低谷，我真的为他骄傲。",
      "sampleEn": "I still remember how proud I felt when my cousin turned his stress into a healthier lifestyle last year. He is two years younger than me, and around last spring he was occupied with applying for master's programs and studying English. He always got tired and sometimes couldn't focus, so the whole family was worried. What he did next really impressed me: following a friend's advice, he started to play badminton twice a week. Because badminton requires a partner, he often teams up with strangers at the court, and soon he made friends who shared the same passion for sports. They began meeting every weekend, and I found him becoming more and more outgoing. When he swings his racket, he says all he hears is its sound and the wind, which helps him forget the pressure from his studies for a while. I felt proud not only because his mood improved, but also because he chose a positive way to handle difficulty instead of complaining. Watching that change in a family member made me respect him even more.",
      "sampleZh": "表弟去年因申请压力大，后来坚持打羽毛球、与陌生人组队、变得外向；我为他用积极方式面对困难而骄傲。",
      "applyOutline": [
        {
          "label": "何时",
          "line": "去年备考最难的阶段"
        },
        {
          "label": "是谁",
          "line": "表弟，比我小几岁"
        },
        {
          "label": "他做了什么",
          "line": "主动约球、跟陌生人组队，把羽毛球坚持下来"
        },
        {
          "label": "为何骄傲",
          "line": "他没有被压力压垮，还变得更开朗，全家都松了口气"
        }
      ]
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
      "openingEn": "The person I want to talk about is Yumeng — she picks up new languages really fast, especially English.",
      "openingZh": "我想说的人是雨萌：她学新语言特别快，尤其是英语。",
      "materialId": "yumeng",
      "materialHint": "人用雨萌（发小、乐观肯听）。本题主线是她怎么学语言，不要整段讲考研建议。",
      "endingTip": "我佩服她学语言的劲头，也喜欢她那种不慌不忙的耐心。",
      "sampleEn": "There's a friend of mine who picks up languages faster than anyone I know, and her name is Yumeng. We grew up in the same neighbourhood and still talk often. When she prepared graduate applications she practised English every day — podcasts, shadowing, and forcing herself to explain ideas in English. Her mother tongue is Chinese, and her English is already smooth enough for study and daily life. What I admire is not magic talent but her patience: she keeps practising and she isn't afraid to open her mouth.",
      "sampleZh": "雨萌从小一起长大；为读研每天练英语；佩服她敢开口、肯坚持。",
      "applyOutline": [
        {
          "label": "怎么认识",
          "line": "我们从小一起长大，现在仍常聊天"
        },
        {
          "label": "怎么学语言",
          "line": "为了读研申请，她每天练英语：听播客、跟读、逼自己用英语解释想法"
        },
        {
          "label": "会说什么",
          "line": "中文母语，英语已经能比较顺地讨论学习和生活"
        },
        {
          "label": "我的感受",
          "line": "她学得快，是因为肯练、也敢开口；跟她聊天我会更敢说英语"
        }
      ]
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
      "materialHint": "法律是「保护区禁乱扔/禁私搭」。天池经历用来解释你为何在意，爬山细节点到为止。",
      "endingTip": "有了这类规定，像天池这样的地方才更能留给后来的人。",
      "sampleEn": "One environmental law I really support is the scenic-area protection rule that bans littering and unauthorized building inside national nature reserves, and I first understood why after visiting Changbai Mountain. In practice, visitors must carry trash out, stay on marked paths, and cannot open shops or hotels beside protected lakes. I learned about these rules when park guides explained them before we entered a remote area in the northeast part of China which is famous for its untouched nature and a lake called \"Tianchi\", the pond of heaven. First there was an extremely long staircase which leads to the hilltop; we had to go up it, but the scenery was truly breathtaking. You can overlook the entire mountain, see the clearest blue sky you've ever seen, and breathe extremely fresh air. When we finally reached the top, we saw the very Tianchi—huge and pure like jade, shining like a huge diamond under the sunlight. Locals, future visitors, and wildlife all benefit, because without the littering ban and construction limits the jade-blue water could be spoiled by plastic bottles and noisy hotels. As soon as I saw Tianchi, all the sweat from the climbing was worth it, and that feeling made me respect this concrete protection law even more.",
      "sampleZh": "我支持景区禁扔垃圾与禁私搭乱建的保护法；在长白山听讲解后更理解天池之美，登顶时一切汗水都值得。",
      "applyOutline": [
        {
          "label": "什么法",
          "line": "国家级自然保护区里禁乱扔垃圾、禁私搭乱建一类的景区保护规定"
        },
        {
          "label": "怎么知道",
          "line": "去长白山天池时入口和步道反复看到警示与罚款提示"
        },
        {
          "label": "谁受益",
          "line": "游客能看到更干净的湖景，生态也不被一点点啃坏"
        },
        {
          "label": "我的感受",
          "line": "爬那么久才看到湖，更觉得这些规矩不是扫兴，是在护住那份震撼"
        }
      ]
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
      "openingEn": "I'd like to talk about a children's storybook about a little bear — a friend gave it to me together with a gift.",
      "openingZh": "我想谈的是一本关于小熊的儿童故事书，朋友把书连同礼物一起送给我。",
      "materialId": "bear",
      "materialHint": "主线是「书」：熊是主角。小熊玩偶只作送礼场景里的关联细节，不要把玩偶软毛当故事本身。",
      "endingTip": "这本书现在仍会让我想起那份友情，也觉得故事很暖。",
      "sampleEn": "I'd like to talk about a children's storybook about a little bear that a friend gave me together with a gift. The main animal is a talking teddy who helps a nervous child through a hard time by teaching slow breathing and saying fears out loud. I read it often before the college entrance exam because it came with a Jellycat bear from my best friend. The plot is simple but warm — it feels like someone gently tapping your shoulder and saying you'll be fine.",
      "sampleZh": "谈熊主角童书；好友送礼时附上；高考前常翻，故事很暖。",
      "applyOutline": [
        {
          "label": "什么动物",
          "line": "主角是一只会说话的小熊"
        },
        {
          "label": "故事讲什么",
          "line": "小熊陪一个紧张的孩子度过难关，教他慢慢呼吸、把害怕说出来"
        },
        {
          "label": "为什么读",
          "line": "好友送Jellycat小熊时附上这本书，高考前我常翻几页"
        },
        {
          "label": "我觉得怎样",
          "line": "情节简单但很暖，像有人轻轻拍拍你说没事的"
        }
      ]
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
      "openingEn": "A few months ago I sent Yumeng a long message, and then I waited much longer than I expected for her reply.",
      "openingZh": "几个月前我给雨萌发了一条很长的消息，结果等她回复等了好久。",
      "materialId": "yumeng",
      "materialHint": "主线必须是「发消息→久等→终于回复→当下感受」。雨萌身份可借；校园长谈/考研建议最多一句带过，别喧宾夺主。",
      "endingTip": "等回复的那几天我挺焦虑，但后来明白她不是冷落我，只是真的忙。",
      "sampleEn": "A few months ago I sent Yumeng a long message, and then I waited much longer than I expected for her reply. Yumeng is my childhood friend, so I usually hear back quickly, which made the silence feel strange. The message was about whether I should do a master's after graduation or start working — I poured everything into that text. For several days there was no reply, and I started overthinking. Finally she messaged that she had been buried in her own applications and barely checked her phone; she suggested we talk at the weekend. When we met I felt relieved. The wait was uncomfortable, but I realised she wasn't ignoring me — she was simply busy, and I learned not to stare at 'read' receipts when something matters.",
      "sampleZh": "给雨萌发长消息久等未回；她忙申请后解释并约见面；等待焦虑但后来释然。",
      "applyOutline": [
        {
          "label": "发给谁",
          "line": "发给雨萌——从小一起长大的朋友"
        },
        {
          "label": "消息说什么",
          "line": "我纠结毕业后读研还是工作，把心里话写成一条很长的消息"
        },
        {
          "label": "有没有回复",
          "line": "她隔了好几天才回：正在赶申请材料，手机几乎没看；约我周末当面说"
        },
        {
          "label": "我的感受",
          "line": "等的时候会胡思乱想，见面后释然；也学到急事别只盯已读不回"
        }
      ]
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
      "openingEn": "The most successful businessperson I know well is my aunt — she runs a small shop selling selected plush toys and gifts.",
      "openingZh": "我最熟悉的成功生意人是姨妈：她开了一家卖精选毛绒玩具和礼物的小店。",
      "materialId": "bear",
      "materialIds": [
        "bear",
        "basketball"
      ],
      "materialHint": "主线是姨妈的店怎么开、为何成功。Jellycat小熊是店里明星货，不是把「我抱熊减压」讲成生意故事。男生版可换成体育用品店卖篮球。",
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
      "endingTip": "我觉得她成功，是因为货靠谱，也懂客人真正想要什么安慰感。",
      "sampleEn": "The successful businessperson I know best is my aunt, who runs a small shop selling selected plush toys and gifts. She's a relative, and I often help in the shop at weekends. She started online, noticed strong demand for comforting gifts during exam season, then rented a mall counter. The shop does well because quality is reliable and she understands what comfort customers want — popular bears sell out in peak months and people come back.",
      "sampleZh": "姨妈开毛绒礼品店；网上试卖后开柜；考季安慰礼物回头客多。",
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
      ],
      "applyOutline": [
        {
          "label": "是谁",
          "line": "姨妈，家里亲戚，我周末常去店里帮忙"
        },
        {
          "label": "做什么生意",
          "line": "商场里一间毛绒礼品店，主打质量好的泰迪熊（含Jellycat）"
        },
        {
          "label": "怎么起步",
          "line": "她先在网上试卖，发现高考季「安慰礼物」需求大，才敢租柜台"
        },
        {
          "label": "为何算成功",
          "line": "回头客多，考季常卖断货；她把服务做细，客人愿意复购"
        }
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
      "materialHint": "主体是无聊的图书馆角落：做什么、为何闷。羽毛球只作对比一句，别把打球经历讲成主线。",
      "endingTip": "正因为太闷，我后来才更珍惜能真正活动起来的地方。",
      "sampleEn": "The most boring place I visited recently was a quiet library corner where I tried to force myself to study all weekend. I went there with a classmate because we were occupied with applying for master's programs and studying English, and we thought sitting still for ten hours would help. What we did was stare at the same pages, check phones secretly, and whisper complaints. Nothing moved, nothing changed, and I felt my brain freeze. That boredom actually pushed me to leave and start to play badminton later that afternoon. At the court I could team up with strangers, hear the sound of the racket and the wind, and suddenly feel alive again. Compared with swinging my racket and becoming more outgoing with sports friends, that library corner was painfully dull. I call it boring not because libraries are bad, but because forcing focus without movement made the pressure worse instead of helping me forget it for a while.",
      "sampleZh": "周末图书馆硬坐学习极无聊；后来去打羽毛球组队、挥拍，才感到清醒，反衬那个角落多么沉闷。",
      "applyOutline": [
        {
          "label": "在哪",
          "line": "学校图书馆最里侧靠窗的角落"
        },
        {
          "label": "和谁",
          "line": "多半自己一人，有时室友也闷坐旁边"
        },
        {
          "label": "做什么",
          "line": "假装复习，实际刷题刷不进去，只听得到翻书声"
        },
        {
          "label": "为何无聊",
          "line": "空气沉、不能大声说话，越坐越困；后来去打球才觉得人活过来了"
        }
      ]
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
      "openingEn": "I'd like to talk about my cousin Linlin — she's clear she wants a career in the medical field, as a nurse or something related.",
      "openingZh": "我想说的是表妹琳琳：她很明确想走医疗方向，以后做护士或相关工作。",
      "materialId": "linlin",
      "materialHint": "主线就是表妹琳琳想当护士。去背补充素材「琳琳」即可；不要再套雨萌考研故事。",
      "endingTip": "我支持她：她真的适合照顾人，也愿意为这事长期投入。",
      "sampleEn": "I'd like to talk about my cousin Linlin, who is clear she wants a career in the medical field as a nurse. We've known each other since family gatherings when we were kids. After high-school volunteering at a hospital she said she wanted to study nursing properly. Her plan is to enter a nursing programme first, work on a ward, and later decide whether to study further. I support her because she is patient with small tasks and feels proud when patients are well looked after.",
      "sampleZh": "表妹琳琳想当护士；高中医院志愿后动念；耐心适合照顾人。",
      "applyOutline": [
        {
          "label": "何时认识",
          "line": "她是表妹，从小亲戚聚会就熟"
        },
        {
          "label": "何时动念",
          "line": "高中志愿者去医院帮忙后，她说想正式学护理"
        },
        {
          "label": "想做什么",
          "line": "先考护理相关专业，以后做病房护士，再慢慢看要不要深造"
        },
        {
          "label": "为什么",
          "line": "她耐心、不怕琐碎，看到病人被好好照顾会特别有成就感"
        }
      ]
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
      "materialHint": "把天池附近观景台/高阶建筑当作 tall building：用途、外观、为何喜欢。不要只讲爬山不讲建筑。",
      "endingTip": "站在那座观景建筑往下看，山脉和天池一起进来，我反而喜欢这种「高」。",
      "sampleEn": "The tall building I like most is not a glass tower in a city center, but the observation structure near Tianchi on Changbai Mountain. It is used for visitors to rest and look out after climbing, and it sits in a remote area in the northeast part of China famous for untouched nature. From below it looks simple, almost plain, but reaching it means walking an extremely long staircase that leads toward the hilltop. When I finally stood there, the scenery was truly breathtaking: I could overlook the entire mountain, see the clearest blue sky, and feel extremely fresh air. Beyond the platform, Tianchi appeared like pure jade, shining like a huge diamond under the sunlight. I like this tall building because its height serves nature rather than blocking it, and as soon as I saw the pond of heaven, all the sweat from the climbing was worth it.",
      "sampleZh": "喜欢天池附近观景高台：需爬极长阶梯，俯瞰山脉与碧玉般天池；高度服务于自然，登顶汗水都值得。",
      "applyOutline": [
        {
          "label": "用途",
          "line": "观景与休息，方便游客登高看天池方向"
        },
        {
          "label": "在哪",
          "line": "长白山景区靠近天池一侧的观景建筑"
        },
        {
          "label": "长什么样",
          "line": "挑高、大玻璃或开阔平台，风很大，阶梯连着上去"
        },
        {
          "label": "为何喜欢",
          "line": "高度带来视野，让未开发的山湖一眼看清，比城里玻璃楼有意思"
        }
      ]
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
      "openingEn": "My uncle is the biggest plant lover in our family — his balcony and yard are almost fully occupied by what he grows.",
      "openingZh": "叔叔是家里最爱种植物的人，阳台和院子几乎被他占满了。",
      "materialId": "tianchi",
      "materialHint": "主线是叔叔种菜养花。长白山天池只作「他为何更爱自然」的一次触发，不要整段爬山阶梯当主体。",
      "endingTip": "看他侍弄植物很安心，也让我觉得把一点自然带回家很值得。",
      "sampleEn": "My uncle is the plant lover in our family, and his hobby grew even stronger after a trip to Changbai Mountain. He grows herbs, tomatoes, and a few wildflowers on the balcony, watering them every morning and talking to them as if they were quiet friends. The way he grows plants is careful and patient: he checks sunlight, mixes soil himself, and refuses chemical sprays. Why does he love it? After visiting a remote area in the northeast famous for untouched nature and Tianchi, the pond of heaven, he said city air felt heavy. He still remembers the extremely long staircase, the breathtaking clear blue sky, and the lake shining like a huge diamond. Growing plants is his way of keeping a piece of that fresh world at home. Whenever the seedlings turn green, he smiles the same way he did when he said all the sweat from the climbing was worth it.",
      "sampleZh": "叔叔阳台种菜养花，灵感来自长白山未开发自然与天池清新空气；种植是把那份自然感带回家。",
      "applyOutline": [
        {
          "label": "是谁",
          "line": "叔叔，退休后时间更多，整天围着花草转"
        },
        {
          "label": "种什么",
          "line": "阳台番茄、香菜，院子里月季和一点小葱"
        },
        {
          "label": "怎么种",
          "line": "自己配土、看天气预报浇水，还用手机记浇水周期"
        },
        {
          "label": "为何热爱",
          "line": "去长白山看过未开发的自然后更上瘾；种植是把那份清新感带回家"
        }
      ]
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
      "openingEn": "The special-occasion food that comes to mind is birthday cake — we almost always have it for birthdays at home.",
      "openingZh": "我想到的特别场合食物是生日蛋糕——家里过生日几乎必有。",
      "materialId": "bear",
      "materialHint": "主线是生日蛋糕（场合、怎么来的、为什么吃）。小熊只是「某次生日顺带收到的礼物」，别把玩偶讲成食物。",
      "endingTip": "蛋糕本身不复杂，但切开分享的那一刻，场合就有了仪式感。",
      "sampleEn": "The special-occasion food that comes to mind is birthday cake — we almost always have it for birthdays at home. It is usually a cream cake with strawberry or chocolate. Mum orders it or decorates a simple one; on one birthday a friend also brought a small bear as a gift. We eat it then because candles, wishes and sharing slices mark growing another year together.",
      "sampleZh": "特别场合吃生日蛋糕；蜡烛许愿一起分；礼物可带过一句。",
      "applyOutline": [
        {
          "label": "是什么",
          "line": "奶油生日蛋糕，通常是草莓或巧克力口味"
        },
        {
          "label": "什么场合",
          "line": "家人过生日，尤其是我高考前夕那次"
        },
        {
          "label": "怎么来的",
          "line": "妈妈预订或自己简单裱花；好友那天还带来礼物（一只小熊）"
        },
        {
          "label": "为何这时吃",
          "line": "蜡烛、许愿、一起分着吃，是我们标记「又长大一岁」的方式"
        }
      ]
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
      "materialHint": "城市主线（延吉/长春门户）：住几天、吃什么、再出发。天池是行程高潮，但题面要先把城市说够。",
      "endingTip": "这座城本身不夸张，但作为去天池的门户，它留给我很清晰的旅行记忆。",
      "sampleEn": "The city trip I enjoyed most was a short stay in Yanji as the gateway before climbing Changbai Mountain. Yanji sits in the northeast, and I visited last summer for two nights with friends. We tried local food, walked lively streets, and prepared gear for the mountain the next day. What made the city special was the contrast: busy lights at night, then a journey into a remote area famous for untouched nature and Tianchi, the pond of heaven. From the city we headed to an extremely long staircase, breathed fresh air under a clear blue sky, and finally saw the lake shining like a huge diamond. I enjoyed Yanji because it was warm and practical, and it led to a view where all the sweat from the climbing was worth it. Without that city stop, the mountain adventure would have felt rushed.",
      "sampleZh": "喜欢延吉作门户城市：停留两晚尝美食，再去天池；城市因通往未开发自然而更难忘。",
      "applyOutline": [
        {
          "label": "在哪",
          "line": "东北，去长白山前停留的门户城市（如延吉）"
        },
        {
          "label": "何时多久",
          "line": "秋天去，城里住一到两晚再进山"
        },
        {
          "label": "做了什么",
          "line": "吃当地餐、逛不太商业的街区，为爬山养足精神"
        },
        {
          "label": "为何喜欢",
          "line": "节奏慢、离自然近；它让整个天池行程不那么赶"
        }
      ]
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
      "materialHint": "主线是「山间小屋」：什么样、为何爱拜访、为何不想住。天池风景是加分项，不是把整段登山当住房描述。",
      "endingTip": "拜访很爽，但长期住太偏、生活不便，我还是更适合城里。",
      "sampleEn": "There is a mountain lodge near Changbai Mountain that I love to visit for a weekend but would never choose as a permanent home. It sits in a remote area in the northeast part of China, close to untouched nature and the path toward Tianchi, the pond of heaven. The lodge is wooden, quiet, and filled with fresh air; from the window you can see mist over the hills. I like to visit because after an extremely long staircase climb, the scenery is breathtaking, the sky is clear blue, and the lake shines like a huge diamond. As soon as I see Tianchi, all the sweat is worth it, and returning to the lodge for hot soup feels perfect. Still, I would not live there: shops are far, winters are harsh, and daily commuting would be exhausting. It is a wonderful guest house for nature, not a practical forever home.",
      "sampleZh": "喜欢拜访天池附近山间小屋看未开发自然，但不想住：太偏远、冬天难熬，只适合周末充电。",
      "applyOutline": [
        {
          "label": "在哪",
          "line": "长白山附近一间亲戚能借用的山间小屋"
        },
        {
          "label": "什么样",
          "line": "木结构、窗景好，晚上很静，离景区车程不远"
        },
        {
          "label": "为何爱去",
          "line": "周末能喘气，清晨出门就能靠近未开发的自然"
        },
        {
          "label": "为何不想住",
          "line": "买菜就医不方便，冬天更难；适合短住不适适合家"
        }
      ]
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
      "endingTip": "我希望新法能少争议、多执行，别等景致坏了再补救。",
      "sampleEn": "If I could introduce a new law, it would require stronger visitor limits and litter fines in fragile mountain reserves. The law would change daily quotas, ban disposable plastics on trails, and fund clean-up teams. I think young travelers would support it, though some tour companies might complain at first. I came up with it after visiting Changbai Mountain, a remote area in the northeast famous for untouched nature and Tianchi, the pond of heaven. Climbing the extremely long staircase, I saw breathtaking views and a clear blue sky, but also tissues left by careless hikers. When the lake finally appeared like pure jade shining as a huge diamond, I realized places like this need legal teeth, not only slogans. I feel strongly positive about this law because as soon as I saw Tianchi, all the sweat was worth it, and that beauty should remain for the next generation.",
      "sampleZh": "想立山地保护区限流与反 litter 法；灵感来自天池未开发自然，登顶震撼让我更坚信该立法。",
      "applyOutline": [
        {
          "label": "什么法",
          "line": "对脆弱山地保护区更严的限流 + 乱扔垃圾重罚"
        },
        {
          "label": "带来什么变化",
          "line": "高峰少拥挤，步道更干净，生态压力下降"
        },
        {
          "label": "会不会受欢迎",
          "line": "当地商户可能嫌限流，但多数游客其实吃过「人挤人」的亏"
        },
        {
          "label": "灵感与感受",
          "line": "灵感来自登天池：那么美更该护住；我觉得严一点是值得的"
        }
      ]
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
      "openingEn": "The child I want to talk about is my younger cousin — she loves drawing and can stay focused for a whole hour.",
      "openingZh": "我想说的孩子是表妹，她超爱画画，能安静画上一小时。",
      "materialId": "sun",
      "materialHint": "主线是「爱画画的孩子」。孙颖莎只是她常画的主题之一，不要把奥运夺金故事当成主体。",
      "endingTip": "我喜欢看她画：认真、开心，画完还主动送我一张。",
      "sampleEn": "The child I want to talk about is my younger cousin — she loves drawing and can stay focused for a whole hour. We meet at Spring Festival and she often shows new drawings on video calls. After school she draws almost every day; her desk drawer is full of pencils and stickers. She loves it because finishing a picture of someone she likes feels satisfying — lately she often draws smiling faces of table-tennis star Sun Yingsha in a sticker style.",
      "sampleZh": "表妹爱画画；几乎每天画；常画孙颖莎笑脸贴纸风。",
      "applyOutline": [
        {
          "label": "是谁",
          "line": "表妹，小学中年级，亲戚里最小的"
        },
        {
          "label": "怎么认识",
          "line": "每年过年见面，后来视频里也常展示新画"
        },
        {
          "label": "画得有多勤",
          "line": "放学后几乎每天画；书桌抽屉里塞满彩铅和贴纸"
        },
        {
          "label": "为何爱画",
          "line": "她觉得把喜欢的人画出来很满足，最近常画乒乓球运动员孙颖莎的笑脸和贴纸风"
        }
      ]
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
      "materialHint": "人物是天池路上的志愿者向导：做什么、多频繁。景色只用来解释你为何敬佩他。",
      "endingTip": "有他这种人在，景点才不只是打卡，而是真的被照看。",
      "sampleEn": "The person who looks after nature most carefully in my life is a volunteer guide I met on the way to Tianchi. He works in a remote area in the northeast famous for untouched nature and the pond of heaven. What he does is simple but tough: he picks up litter on the extremely long staircase, reminds tourists not to feed wildlife, and explains why the clear blue sky and fresh air depend on small habits. He does this almost every weekend. I feel deep respect for him because without people like him, the lake that looks like pure jade and shines like a huge diamond would be spoiled. When I finally saw Tianchi and felt that all the sweat was worth it, I also understood his quiet mission. Caring for nature is how he protects that feeling for strangers like me.",
      "sampleZh": "天池志愿者向导周末捡垃圾、劝游客；正因有他，碧玉般天池才能让攀登的汗水值得。",
      "applyOutline": [
        {
          "label": "是谁",
          "line": "去天池路上遇到的志愿者向导"
        },
        {
          "label": "做什么",
          "line": "捡垃圾、提醒别抄近路踩植被、给游客讲保护规矩"
        },
        {
          "label": "怎么做/多常",
          "line": "穿志愿马甲、边走边劝；他说几乎每周末都来"
        },
        {
          "label": "我的感受",
          "line": "辛苦却不抱怨，让我觉得爱护自然是具体行动，不是口号"
        }
      ]
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
      "materialHint": "主线是海外短工本身（地点、岗位、为何想做）。雨萌建议读研只作「你如何知道这个方向」的一句背景。",
      "endingTip": "我想用短期海外工作练英语、验证自己是不是真喜欢这个方向。",
      "sampleEn": "The short-term overseas job I want is a research assistant role in the UK linked to my master's plan. I know of it through university notices and through conversations with Yumeng, one of my most important friends. We grew up in the same neighborhood, and when I was lost in my third year about studying further or working, we walked around the campus and she listened very patiently. She told me not to worry only about finding a job and to think about what I want for the rest of my life, adding that passion is the best teacher. That advice pushed me toward graduate study abroad, and a short research post would let me practice English, test the field, and earn a bit of experience. I want it because it turns her wise encouragement into a concrete next step. Her words still give me strength whenever applications feel heavy.",
      "sampleZh": "想做英国短期科研助理；灵感来自雨萌鼓励读硕与追随热情，用以练英语并验证方向。",
      "applyOutline": [
        {
          "label": "在哪",
          "line": "英国（或英语国家）高校/实验室的短期科研助理"
        },
        {
          "label": "怎么知道",
          "line": "和雨萌聊读研方向时搜到相关项目，她鼓励我先短试"
        },
        {
          "label": "工作内容",
          "line": "帮忙整理数据、参与组会、用英语写简单报告"
        },
        {
          "label": "为何想做",
          "line": "短、能练英语，也检验热情是不是真的，再决定要不要长读"
        }
      ]
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
      "endingTip": "规则严一点没关系，关键是山和湖还在。",
      "sampleEn": "The environmental law I want introduced is a strict anti-litter and trail-protection rule for national mountain parks. People should follow it because untouched places disappear quickly once trash and illegal shortcuts arrive. I believe most hikers would find it popular, though a minority may call it inconvenient. My feeling comes from climbing toward Tianchi in a remote northeast area famous for untouched nature. On the extremely long staircase the air was fresh and the sky breathtakingly clear, yet I still saw bottles left behind. When the pond of heaven appeared like pure jade shining as a huge diamond, I knew beauty alone cannot protect itself. As soon as I saw Tianchi, all the sweat was worth it, and that is exactly why I want a law with real penalties and education, not only posters.",
      "sampleZh": "想立山地公园反 litter 保护法；天池未开发之美需要法律牙齿，登顶震撼让我更坚持。",
      "applyOutline": [
        {
          "label": "什么法",
          "line": "国家山地公园反 litter + 步道保护的专门环保规则"
        },
        {
          "label": "为何遵守",
          "line": "垃圾和抄近道会一点点毁掉未开发自然"
        },
        {
          "label": "是否受欢迎",
          "line": "年轻人多半支持；关键是罚款要执行、标识要清楚"
        },
        {
          "label": "感受",
          "line": "登过天池后更坚定：美景配得上被认真保护"
        }
      ]
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
      "openingEn": "Last spring the roles were reversed for once — Yumeng was stuck, and I was the one who gave her advice.",
      "openingZh": "去年春天有一次角色对调：雨萌卡住了，反而是我给她提了建议。",
      "materialId": "yumeng",
      "materialHint": "主线是「你建议她」。场景仍可用校园散步；内容可借用「先想清楚自己真正想要什么」，但主语必须是你在帮她。",
      "endingTip": "能帮到她我挺高兴，也更明白倾听本身就是一种帮助。",
      "sampleEn": "Last spring the roles were reversed for once — Yumeng was stuck, and I gave her advice. We walked around campus in our third year. Usually she listens to me, but that day she couldn't choose an internship city. I asked her to write down what she wanted to become in a year, then work backwards to pick the city. I gave that advice because too many opinions had made her messy; I simply returned a method she often used on me. Helping her felt good, and I realised listening and clarifying can be help too.",
      "sampleZh": "角色对调：你帮雨萌选实习城市；先定一年目标再倒推；高兴能帮到她。",
      "applyOutline": [
        {
          "label": "何时",
          "line": "大三下学期，春暖时我们在校园边走边聊"
        },
        {
          "label": "建议给谁",
          "line": "给雨萌——平时总是她听我讲"
        },
        {
          "label": "建议是什么",
          "line": "她纠结实习城市；我让她先列「一年后想变成什么样」，再倒推选哪座城"
        },
        {
          "label": "为何提这建议",
          "line": "她听别人太多反而乱；我用她常对我说的办法还给她，帮她抓重点"
        }
      ]
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
      "materialHint": "主体是不喜欢的KTV/音乐活动。羽毛球局只是「为何会去」的前因，别把打球讲成主线。",
      "endingTip": "那晚的音乐让我更确认：我放松的方式是挥拍，不是硬嗨。",
      "sampleEn": "Honestly I usually like music, but a karaoke night after badminton left me wishing I had gone straight home. It was a weekend gathering with the people I often team up with at the court after I started to play badminton to escape application stress. I decided to go because they had become friends and I was becoming more outgoing; saying no felt rude. The music, however, was painfully loud and off-key, and the room was packed with smoke and shouted choruses. I could not hear myself think, let alone relax. What I missed was the opposite feeling I get when I swing my racket: only its sound and the wind, focusing on mind and body, forgetting study pressure for a while. That night taught me that not every social plan fits me, even with good people.",
      "sampleZh": "球友拉去KTV又吵又跑调；远不如球场挥拍时能专注身心、暂时忘却压力。",
      "applyOutline": [
        {
          "label": "什么活动",
          "line": "打球结束后队友拉去的KTV"
        },
        {
          "label": "和谁去",
          "line": "球友几人，我不太好意思拒绝"
        },
        {
          "label": "为何去",
          "line": "大家说庆祝打得开心，顺路聚一下"
        },
        {
          "label": "为何不喜欢",
          "line": "歌单吵、跑调起哄，我听着更累；对比球场专注，这里完全放松不了"
        }
      ]
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
