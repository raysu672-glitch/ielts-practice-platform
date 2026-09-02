// P1 data - 2026年5-8月在考题（五类按热度）+ 逐题词块
const P1_DATA = {
  "meta": {
    "season": "2026年5-8月",
    "heatSource": "雅思哥 2026-08-25",
    "note": "仅保留大陆考区当季在考小题；同类内按近期考过人数排序",
    "totalQuestions": 231,
    "wordSourceStats": {
      "explicit": 119,
      "clue-alias": 30,
      "clue": 82
    },
    "sampleLogicFail": 0
  },
  "categories": [
    {
      "id": "shishi",
      "name": "事实陈述类",
      "steps": [
        "正面回答",
        "来源或举例",
        "频次",
        "感受"
      ],
      "questions": [
        {
          "id": 1,
          "title": "Have you ever got a watch as a gift",
          "q": "Have you ever got a watch as a gift?",
          "topicEn": "Watch",
          "topicZh": "手表",
          "tag": "新增",
          "recentCount": 39172,
          "heatRank": 1,
          "tip": "【新增·热度#1·近39172人】事实：收到手表礼物→谁送的+实用；别聊名牌。 本题按「事实陈述类」四步答；素材：物品·手表（实用计时）。",
          "logic": "事实：收到手表礼物→谁送的+实用；别聊名牌。",
          "material": "物品·手表（实用计时）",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "Sure"
            ],
            "来源或举例": [
              "from my parents",
              "birthday gift",
              "smartwatch"
            ],
            "频次": [
              "on special occasions",
              "last year",
              "once"
            ],
            "感受": [
              "really convenient",
              "practical",
              "a useful gift"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. I got a smartwatch from my parents as a birthday gift last year, which helps me check the time quickly. On special occasions I still remember that day. I find it really convenient and practical.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 2,
          "title": "What subjects are you studying",
          "q": "What subjects are you studying?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I'm majoring in",
              "Yes",
              "Several subjects"
            ],
            "来源或举例": [
              "business",
              "economics",
              "related courses"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I'm majoring in business, and I also take related courses like economics. I attend classes every weekday to build a solid foundation, which will be useful for my future career. I find this field quite practical.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "clue-alias",
          "clueId": "20"
        },
        {
          "id": 3,
          "title": "Why did you choose to study that subject",
          "q": "Why did you choose to study that subject?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "Because I'm interested in it",
              "Definitely",
              "Passion"
            ],
            "来源或举例": [
              "passion for the subject",
              "future career",
              "my strengths"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since",
              "pattern": "I chose it for the reason that / since ______.",
              "tip": "第2步：Why 题直接给原因状语"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I chose it for the reason that I have a passion for the subject and it matches my strengths. Since I want a clear future career path, I study related courses every weekday. I find it practical and quite useful.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "clue-alias",
          "clueId": "20"
        },
        {
          "id": 4,
          "title": "What work do you do",
          "q": "What work do you do?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I'm a student",
              "I work part-time",
              "Internship"
            ],
            "来源或举例": [
              "internship",
              "tutor",
              "on campus"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I'm a student, and I also do a part-time internship on campus. I work as a tutor from time to time, which helps me practice communication. I find this experience really useful for my future career.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "clue-alias",
          "clueId": "20"
        },
        {
          "id": 5,
          "title": "Why did you choose to do that type of work (or that job)",
          "q": "Why did you choose to do that type of work (or that job)?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I am a student majoring in",
              "Yes",
              "Definitely",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "Study",
              "attend classes",
              "listen to a lecture"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since",
              "pattern": "I chose it for the reason that / since ______.",
              "tip": "第2步：Why 题直接给原因状语"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I chose it since it matches my major. For example, I can talk about Study and attend classes, which is quite typical for me. I notice this every weekday, so it is easy to keep the answer concrete. I find it useful, and it will be useful for my future career is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 6,
          "title": "What requirements did you need to meet to get your current job",
          "q": "What requirements did you need to meet to get your current job?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "Several requirements",
              "Yes",
              "Quite a few"
            ],
            "来源或举例": [
              "a degree",
              "relevant experience",
              "good communication skills"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "There were several requirements. To be specific, I would mention a degree and relevant experience, which matters in my daily routine. I usually talk about this every weekday, and I can give a short example if needed. I find it useful, so it will be useful for my future career is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "20"
        },
        {
          "id": 7,
          "title": "Who helps you the most? And how",
          "q": "Who helps you the most? And how?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「事实陈述类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "事实：直接 Yes/No + 具体细节；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "My parents",
              "My close friends",
              "Definitely"
            ],
            "来源或举例": [
              "give me advice",
              "encourage me",
              "help with planning"
            ],
            "频次": [
              "every weekday",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it will be useful for my future career",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 who + which",
              "pattern": "______ helps me the most, which ______.",
              "tip": "第2步：人物题用 who + which 补具体帮助"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "My parents help me the most. They give me advice and encourage me, which helps with planning. Whenever I feel stuck with study or life choices, they support me patiently. I find their help really practical, and I rely on it a lot.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "clue-alias",
          "clueId": "20"
        },
        {
          "id": 8,
          "title": "Are there any changes to the websites you often visit",
          "q": "Are there any changes to the websites you often visit?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 3,
          "tip": "【新增·热度#3·近8064人】事实：常用站改版/新功能，如学习网站或小红书。 本题按「事实陈述类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "事实：常用站改版/新功能，如学习网站或小红书。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Quite a few",
              "Recently yes"
            ],
            "来源或举例": [
              "new layout",
              "more short videos",
              "updated design"
            ],
            "频次": [
              "recently",
              "in the past year",
              "from time to time"
            ],
            "感受": [
              "takes time to get used to",
              "mostly positive",
              "still useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, there is a new layout and more short videos, which take time to get used to. I have noticed these updates in the past year. I find the changes mostly positive and still useful.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 9,
          "title": "What have you learned from websites that help with your life or studies",
          "q": "What have you learned from websites that help with your life or studies?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 3,
          "tip": "【新增·热度#3·近8064人】事实：从B站/知乎学技能、查资料。 本题按「事实陈述类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "事实：从B站/知乎学技能、查资料。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Quite a lot",
              "A fair amount",
              "Definitely"
            ],
            "来源或举例": [
              "study skills",
              "cooking tips",
              "search information"
            ],
            "频次": [
              "when I need help",
              "almost every day",
              "before exams"
            ],
            "感受": [
              "really useful",
              "save me time",
              "practical"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Quite a lot. I learn study skills and cooking tips online, which helps me search information quickly. Whenever I need help before exams, I use these sites almost every day. I find them really useful and practical, so I keep going back to them.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 10,
          "title": "Do you have a teacher from your past that you still remember",
          "q": "Do you have a teacher from your past that you still remember?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】事实：一位耐心老师+具体帮助。 本题按「事实陈述类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "事实：一位耐心老师+具体帮助。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "Yes",
              "clearly",
              "Definitely",
              "One in particular"
            ],
            "来源或举例": [
              "my high school English teacher",
              "very patient",
              "explained clearly"
            ],
            "频次": [
              "years ago",
              "in high school",
              "still remember"
            ],
            "感受": [
              "left a deep impression",
              "really grateful",
              "changed my attitude"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about my high school English teacher and very patient, which is quite typical for me. I notice this years ago, so it is easy to keep the answer concrete. I find it grateful, and left a deep impression is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 11,
          "title": "Are you still in touch with your primary school teachers",
          "q": "Are you still in touch with your primary school teachers?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】事实：偶尔联系/节日问候，或坦诚很少联系。 本题按「事实陈述类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "事实：偶尔联系/节日问候，或坦诚很少联系。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "Not really",
              "Occasionally",
              "Rarely"
            ],
            "来源或举例": [
              "WeChat messages",
              "during festivals",
              "through my parents"
            ],
            "频次": [
              "from time to time",
              "once a year",
              "almost never"
            ],
            "感受": [
              "still grateful",
              "fond memories",
              "they were caring"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Not really, only sometimes. For example, I can talk about WeChat messages and during festivals, which is quite typical for me. I notice this from time to time, so it is easy to keep the answer concrete. I find it practical, and still grateful is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 12,
          "title": "In what way has your favourite teacher helped you",
          "q": "In what way has your favourite teacher helped you?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】事实：鼓励+讲题+树立信心。 本题按「事实陈述类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "事实：鼓励+讲题+树立信心。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "In many ways",
              "Quite a lot",
              "Several ways"
            ],
            "来源或举例": [
              "encouraged me",
              "explained concepts clearly",
              "gave feedback"
            ],
            "频次": [
              "when I struggled",
              "during exams",
              "through university prep"
            ],
            "感受": [
              "gave me confidence",
              "made me believe in myself",
              "really supportive"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 who + which",
              "pattern": "______ helps me the most, which ______.",
              "tip": "第2步：人物题用 who + which 补具体帮助"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Quite a lot. For example, I can talk about encouraged me and explained concepts clearly, which is quite typical for me. I notice this during exams, so it is easy to keep the answer concrete. I find it supportive, and gave me confidence is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 13,
          "title": "Do you know any famous people in your area",
          "q": "Do you know any famous people in your area?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 5,
          "tip": "【万年·热度#5·近4473人】事实：当地名人/网红或坦诚不认识。 本题按「事实陈述类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "事实：当地名人/网红或坦诚不认识。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "Not personally",
              "One or two",
              "On TV only"
            ],
            "来源或举例": [
              "a local influencer",
              "historical figure",
              "community leader"
            ],
            "频次": [
              "in the news",
              "heard from neighbours",
              "rarely"
            ],
            "感受": [
              "interesting stories",
              "not that famous",
              "part of local culture"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Not personally. For example, I can talk about a local influencer and historical figure, which is quite typical for me. I notice this rarely, so it is easy to keep the answer concrete. I find it practical, and interesting stories is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 14,
          "title": "What are some changes in the area recently",
          "q": "What are some changes in the area recently?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 5,
          "tip": "【万年·热度#5·近4473人】事实：新建商场/地铁/环境变化。 本题按「事实陈述类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "事实：新建商场/地铁/环境变化。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "Quite a few",
              "Several changes",
              "Definitely"
            ],
            "来源或举例": [
              "new shopping malls",
              "subway extension",
              "more cafes"
            ],
            "频次": [
              "recently",
              "in the past few years",
              "ever ever ever ever since I moved here"
            ],
            "感受": [
              "more convenient",
              "busier now",
              "better facilities"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Quite a few. To be specific, I would mention new shopping malls and subway extension, which matters in my daily routine. I usually talk about this recently, and I can give a short example if needed. I find it convenient, so more convenient is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 15,
          "title": "Do you know any of your neighbors",
          "q": "Do you know any of your neighbors?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 5,
          "tip": "【万年·热度#5·近4473人】事实：认识几位邻居/偶尔打招呼。 本题按「事实陈述类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "事实：认识几位邻居/偶尔打招呼。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "A few of them",
              "Some neighbours",
              "Not many"
            ],
            "来源或举例": [
              "say hello",
              "elderly couple",
              "same building"
            ],
            "频次": [
              "when we meet",
              "in the elevator",
              "from time to time"
            ],
            "感受": [
              "friendly enough",
              "peaceful community",
              "feel safe"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, a few of them. For example, I can talk about say hello and elderly couple, which is quite typical for me. I notice this from time to time, so it is easy to keep the answer concrete. I find it practical, and friendly enough is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 16,
          "title": "Are the people in your neighborhood nice and friendly",
          "q": "Are the people in your neighborhood nice and friendly?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 5,
          "tip": "【万年·热度#5·近4473人】事实：邻居友善互助或一般。 本题按「事实陈述类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "事实：邻居友善互助或一般。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "Yes",
              "quite friendly",
              "Most are nice",
              "Generally yes"
            ],
            "来源或举例": [
              "help each other",
              "say hello",
              "quiet community"
            ],
            "频次": [
              "when needed",
              "always",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel safe",
              "warm atmosphere",
              "comfortable living here"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about help each other and say hello, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it comfortable, and feel safe is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 17,
          "title": "Do you live in a noisy or a quiet area",
          "q": "Do you live in a noisy or a quiet area?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 5,
          "tip": "【万年·热度#5·近4473人】事实：安静住宅区或临街略吵。 本题按「事实陈述类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "事实：安静住宅区或临街略吵。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "Quite quiet",
              "Mostly quiet",
              "A bit noisy"
            ],
            "来源或举例": [
              "residential area",
              "away from main road",
              "near a market"
            ],
            "频次": [
              "at night",
              "during rush hour",
              "on weekdays"
            ],
            "感受": [
              "peaceful at night",
              "can sleep well",
              "busy in the morning"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "It is quite quiet. In my case, residential area and away from main road is the better description, which fits where I live. I notice this at night, especially when I compare different areas. I find it practical, and peaceful at night is my honest reaction.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 18,
          "title": "Have you ever returned anything you bought online",
          "q": "Have you ever returned anything you bought online?",
          "topicEn": "Shopping",
          "topicZh": "购物",
          "tag": "新增",
          "recentCount": 4312,
          "heatRank": 6,
          "tip": "【新增·热度#6·近4312人】事实：网购退货经历+原因尺码/质量。 本题按「事实陈述类」四步答；素材：购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。。",
          "logic": "事实：网购退货经历+原因尺码/质量。",
          "material": "购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。",
          "words": {
            "正面回答": [
              "Yes",
              "once",
              "A couple of times",
              "Definitely"
            ],
            "来源或举例": [
              "wrong size",
              "quality issue",
              "through online shopping"
            ],
            "频次": [
              "last month",
              "from time to time",
              "rarely"
            ],
            "感受": [
              "the process was easy",
              "a bit annoying",
              "sellers were helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with wrong size and quality issue, which left a clear impression on me. That happened last month, so I still remember the details. Overall, I find it helpful, and the process was easy is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 19,
          "title": "Have you ever bought mirrors",
          "q": "Have you ever bought mirrors?",
          "topicEn": "Mirrors",
          "topicZh": "镜子",
          "tag": "新增",
          "recentCount": 4116,
          "heatRank": 7,
          "tip": "【新增·热度#7·近4116人】事实：买过镜子装饰/化妆镜。 本题按「事实陈述类」四步答；素材：镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。。",
          "logic": "事实：买过镜子装饰/化妆镜。",
          "material": "镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。",
          "words": {
            "正面回答": [
              "Yes",
              "once",
              "A few times",
              "Not really"
            ],
            "来源或举例": [
              "a small mirror",
              "for my desk",
              "decorative mirror"
            ],
            "频次": [
              "last year",
              "when I moved",
              "rarely"
            ],
            "感受": [
              "practical and cheap",
              "looks nice",
              "useful daily"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with a small mirror and for my desk, which left a clear impression on me. That happened last year, so I still remember the details. Overall, I find it practical, and practical and cheap is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 20,
          "title": "Have you taken any music classes",
          "q": "Have you taken any music classes?",
          "topicEn": "Music",
          "topicZh": "音乐",
          "tag": "新增",
          "recentCount": 3997,
          "heatRank": 8,
          "tip": "【新增·热度#8·近3997人】事实：学过音乐课/乐器经历。 本题按「事实陈述类」四步答；素材：音乐=listen to music 解压。",
          "logic": "事实：学过音乐课/乐器经历。",
          "material": "音乐=listen to music 解压",
          "words": {
            "正面回答": [
              "Yes",
              "in school",
              "A short course",
              "Not really"
            ],
            "来源或举例": [
              "music class",
              "learned guitar",
              "in primary school"
            ],
            "频次": [
              "years ago",
              "for one semester",
              "when I was young"
            ],
            "感受": [
              "was fun",
              "basic skills",
              "wish I continued"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about music class and learned guitar, which is quite typical for me. I notice this years ago, so it is easy to keep the answer concrete. I find it fun, and was fun is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 21,
          "title": "Are the transport facilities to your home very good",
          "q": "Are the transport facilities to your home very good?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：地铁公交方便/离家近。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：地铁公交方便/离家近。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "Yes",
              "quite good",
              "Very convenient",
              "Pretty decent"
            ],
            "来源或举例": [
              "near the subway",
              "bus stops nearby",
              "easy to get around"
            ],
            "频次": [
              "every day",
              "when commuting",
              "to university"
            ],
            "感受": [
              "save a lot of time",
              "really convenient",
              "rarely late"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about near the subway and bus stops nearby, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it convenient, and save a lot of time is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 22,
          "title": "Please describe the room you live in",
          "q": "Please describe the room you live in?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "my bedroom",
              "small but cosy",
              "desk and wardrobe"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 描述细节",
              "pattern": "It is ______, which ______.",
              "tip": "第2步：Describe 题用 which 补一句细节"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "My room is small but cosy. The key details are my bedroom and small but cosy, which are easy to notice in real life. I experience this every day, so I can describe it without making things up. I find this place relaxed, and feel relaxed and at ease is how I feel about it.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 23,
          "title": "How long have you lived there",
          "q": "How long have you lived there?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "with easy access to the subway"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I have lived there for several years. The main point is surrounded by convenience stores and shopping malls, which shapes my answer clearly. This has been true every day, so I do not need a complicated story. I find it relaxed, and feel relaxed and at ease is the feeling I want to share.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 24,
          "title": "Can you describe the place where you live",
          "q": "Can you describe the place where you live?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "a residential area",
              "convenience stores nearby",
              "quiet street"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 描述细节",
              "pattern": "It is ______, which ______.",
              "tip": "第2步：Describe 题用 which 补一句细节"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Sure, I can give a short description. The key details are a residential area and convenience stores nearby, which are easy to notice in real life. I experience this every day, so I can describe it without making things up. I find this place relaxed, and feel relaxed and at ease is how I feel about it.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 25,
          "title": "Do you live in an apartment or a house",
          "q": "Do you live in an apartment or a house?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "an apartment",
              "with my family",
              "in a high-rise"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I live in an apartment. In my case, an apartment and with my family is the better description, which fits where I live. I notice this every day, especially when I compare different areas. I find it relaxed, and feel relaxed and at ease is my honest reaction.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 26,
          "title": "Who do you live with",
          "q": "Who do you live with?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "my parents",
              "roommates",
              "my family"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I live in a big city. To be specific, I would mention my parents and roommates, which matters in my daily routine. I usually talk about this every day, and I can give a short example if needed. I find it relaxed, so feel relaxed and at ease is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 27,
          "title": "What kinds of accommodation do you live in",
          "q": "What kinds of accommodation do you live in?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「事实陈述类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "事实：直接 Yes/No + 具体细节；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "student dorms",
              "rented apartment",
              "shared flat"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型2 I prefer / am keen on",
              "pattern": "I prefer / am keen on ______ because ______.",
              "tip": "第2步：类型题用 prefer / keen on + 简短原因"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I live in a big city. To be specific, I would mention student dorms and rented apartment, which matters in my daily routine. I usually talk about this every day, and I can give a short example if needed. I find it relaxed, so feel relaxed and at ease is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 28,
          "title": "Where is your hometown",
          "q": "Where is your hometown?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "in the south",
              "a coastal city",
              "central China"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "My hometown is in the south. The key details are in the south and a coastal city, which are easy to notice in real life. I experience this every day, so I can describe it without making things up. I find this place relaxed, and feel relaxed and at ease is how I feel about it.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 29,
          "title": "Is that a big city or a small place",
          "q": "Is that a big city or a small place?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "a medium-sized city",
              "not too big",
              "manageable size"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "It is a medium-sized city. In my case, a medium-sized city and not too big is the better description, which fits where I live. I notice this every day, especially when I compare different areas. I find it relaxed, and feel relaxed and at ease is my honest reaction.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 30,
          "title": "Please describe your hometown a little",
          "q": "Please describe your hometown a little?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "local food",
              "friendly people",
              "nice scenery"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 描述细节",
              "pattern": "It is ______, which ______.",
              "tip": "第2步：Describe 题用 which 补一句细节"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Sure, I can give a short description. The key details are local food and friendly people, which are easy to notice in real life. I experience this every day, so I can describe it without making things up. I find this place relaxed, and feel relaxed and at ease is how I feel about it.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 31,
          "title": "How long have you been living there",
          "q": "How long have you been living there?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "with easy access to the subway"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I have lived there for several years. The main point is surrounded by convenience stores and shopping malls, which shapes my answer clearly. This has been true every day, so I do not need a complicated story. I find it relaxed, and feel relaxed and at ease is the feeling I want to share.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 32,
          "title": "What's your hometown famous for",
          "q": "What's your hometown famous for?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：直接 Yes/No + 具体细节；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "local cuisine",
              "historical sites",
              "natural scenery"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "It is mainly famous for local food. For example, I can talk about local cuisine and historical sites, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it relaxed, and feel relaxed and at ease is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 33,
          "title": "Did you learn about the history of your hometown at school",
          "q": "Did you learn about the history of your hometown at school?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：学校历史课讲过家乡。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：学校历史课讲过家乡。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "Yes",
              "briefly",
              "In history class",
              "A little"
            ],
            "来源或举例": [
              "local history",
              "famous events",
              "in textbooks"
            ],
            "频次": [
              "in middle school",
              "years ago",
              "one chapter"
            ],
            "感受": [
              "interesting",
              "proud of my hometown",
              "basic knowledge"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about local history and famous events, which is quite typical for me. I notice this years ago, so it is easy to keep the answer concrete. I find it practical, and interesting is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 34,
          "title": "Are there many young people in your hometown",
          "q": "Are there many young people in your hometown?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：年轻人多/少+就业吸引力。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：年轻人多/少+就业吸引力。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "Yes",
              "quite a few",
              "A good number",
              "Not that many"
            ],
            "来源或举例": [
              "university students",
              "young workers",
              "start-up scene"
            ],
            "频次": [
              "nowadays",
              "in the city centre",
              "compared to before"
            ],
            "感受": [
              "lively atmosphere",
              "more opportunities",
              "some moved away"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about university students and young workers, which is quite typical for me. I notice this nowadays, so it is easy to keep the answer concrete. I find it practical, and lively atmosphere is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 35,
          "title": "Have you learned anything about the history of your hometown",
          "q": "Have you learned anything about the history of your hometown?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：博物馆/家人讲述了解历史。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：博物馆/家人讲述了解历史。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "Yes",
              "some things",
              "A fair amount",
              "From family"
            ],
            "来源或举例": [
              "local museum",
              "grandparents' stories",
              "history books"
            ],
            "频次": [
              "during the holidays",
              "when I was young",
              "from time to time"
            ],
            "感受": [
              "proud heritage",
              "know my roots",
              "interesting past"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about local museum and grandparents' stories, which is quite typical for me. I notice this during the holidays, so it is easy to keep the answer concrete. I find it practical, and proud heritage is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 36,
          "title": "Did you learn about the culture of your hometown in your childhood",
          "q": "Did you learn about the culture of your hometown in your childhood?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 10,
          "tip": "【万年·热度#10·近2912人】事实：童年节日习俗/地方美食文化。 本题按「事实陈述类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "事实：童年节日习俗/地方美食文化。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "Yes",
              "through festivals",
              "From my family",
              "Quite a lot"
            ],
            "来源或举例": [
              "local festivals",
              "traditional food",
              "folk customs"
            ],
            "频次": [
              "during childhood",
              "every spring festival",
              "with grandparents"
            ],
            "感受": [
              "warm memories",
              "part of who I am",
              "still practise some"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about local festivals and traditional food, which is quite typical for me. I notice this during childhood, so it is easy to keep the answer concrete. I find it practical, and warm memories is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 37,
          "title": "What type of headphones do you use",
          "q": "What type of headphones do you use?",
          "topicEn": "Headphones",
          "topicZh": "耳机",
          "tag": "新增",
          "recentCount": 2597,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2597人】事实：无线/入耳式耳机+主要用途。 本题按「事实陈述类」四步答；素材：耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。。",
          "logic": "事实：无线/入耳式耳机+主要用途。",
          "material": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
          "words": {
            "正面回答": [
              "Wireless earbuds",
              "Over-ear headphones",
              "Bluetooth ones"
            ],
            "来源或举例": [
              "listen to music",
              "on the subway",
              "while studying"
            ],
            "频次": [
              "every day",
              "when commuting",
              "in my free time"
            ],
            "感受": [
              "block noise",
              "really convenient",
              "good sound quality"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I usually use wireless earbuds. To be specific, I would mention listen to music and on the subway, which matters in my daily routine. I usually talk about this every day, and I can give a short example if needed. I find it convenient, so block noise is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 38,
          "title": "Have you ever posted anything on social media",
          "q": "Have you ever posted anything on social media?",
          "topicEn": "Social media",
          "topicZh": "社交媒体",
          "tag": "新增",
          "recentCount": 2310,
          "heatRank": 12,
          "tip": "【新增·热度#12·近2310人】事实：发过照片/动态的经历。 本题按「事实陈述类」四步答；素材：社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。。",
          "logic": "事实：发过照片/动态的经历。",
          "material": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
          "words": {
            "正面回答": [
              "Yes",
              "many times",
              "Occasionally",
              "A few times"
            ],
            "来源或举例": [
              "post photos",
              "share daily life",
              "on WeChat"
            ],
            "频次": [
              "at weekends",
              "during the holidays",
              "from time to time"
            ],
            "感受": [
              "keep in touch",
              "fun to share",
              "get reactions from friends"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with post photos and share daily life, which left a clear impression on me. That happened at weekends, so I still remember the details. Overall, I find it fun, and keep in touch is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 39,
          "title": "When did you start using social media",
          "q": "When did you start using social media?",
          "topicEn": "Social media",
          "topicZh": "社交媒体",
          "tag": "新增",
          "recentCount": 2310,
          "heatRank": 12,
          "tip": "【新增·热度#12·近2310人】事实：初中/高中开始用微信等。 本题按「事实陈述类」四步答；素材：社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。。",
          "logic": "事实：初中/高中开始用微信等。",
          "material": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
          "words": {
            "正面回答": [
              "In high school",
              "Years ago",
              "Around age 15"
            ],
            "来源或举例": [
              "WeChat",
              "Xiaohongshu",
              "with my classmates"
            ],
            "频次": [
              "since high school",
              "for many years",
              "early teens"
            ],
            "感受": [
              "part of daily life",
              "hard to imagine without it",
              "very common"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I started in high school. For example, I can talk about WeChat and Xiaohongshu, which is quite typical for me. I notice this for many years, so it is easy to keep the answer concrete. I find it common, and part of daily life is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 40,
          "title": "Do your friends use social media",
          "q": "Do your friends use social media?",
          "topicEn": "Social media",
          "topicZh": "社交媒体",
          "tag": "新增",
          "recentCount": 2310,
          "heatRank": 12,
          "tip": "【新增·热度#12·近2310人】事实：朋友都用社媒聊天发动态。 本题按「事实陈述类」四步答；素材：社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。。",
          "logic": "事实：朋友都用社媒聊天发动态。",
          "material": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
          "words": {
            "正面回答": [
              "Yes",
              "all of them",
              "Almost everyone",
              "Definitely"
            ],
            "来源或举例": [
              "WeChat",
              "post photos",
              "chat every day"
            ],
            "频次": [
              "every day",
              "constantly",
              "all the time"
            ],
            "感受": [
              "easy to connect",
              "share moments",
              "stay updated"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about WeChat and post photos, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it practical, and easy to connect is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 41,
          "title": "Have you ever learnt how to sing",
          "q": "Have you ever learnt how to sing?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 13,
          "tip": "【新增·热度#13·近2135人】事实：学过唱歌/KTV经历。 本题按「事实陈述类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "事实：学过唱歌/KTV经历。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "Yes",
              "a little",
              "In music class",
              "Self-taught"
            ],
            "来源或举例": [
              "sing a song",
              "at KTV",
              "with friends"
            ],
            "频次": [
              "years ago",
              "during the holidays",
              "occasionally"
            ],
            "感受": [
              "was fun",
              "not very skilled",
              "enjoyed it"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with sing a song and at KTV, which left a clear impression on me. That happened years ago, so I still remember the details. Overall, I find it fun, and was fun is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 42,
          "title": "Have you ever taken a singing class",
          "q": "Have you ever taken a singing class?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 13,
          "tip": "【新增·热度#13·近2135人】事实：是否上过声乐课。 本题按「事实陈述类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "事实：是否上过声乐课。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "Yes",
              "briefly",
              "In school",
              "Not really"
            ],
            "来源或举例": [
              "music class",
              "learned basics",
              "school choir"
            ],
            "频次": [
              "in primary school",
              "one semester",
              "years ago"
            ],
            "感受": [
              "interesting experience",
              "built confidence",
              "was nervous"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with music class and learned basics, which left a clear impression on me. That happened years ago, so I still remember the details. Overall, I find it practical, and interesting experience is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 43,
          "title": "Have you ever learnt about outer space and stars",
          "q": "Have you ever learnt about outer space and stars?",
          "topicEn": "Outer space and stars",
          "topicZh": "外太空与星星",
          "tag": "新增",
          "recentCount": 1988,
          "heatRank": 14,
          "tip": "【新增·热度#14·近1988人】事实：学校科学课/纪录片了解太空。 本题按「事实陈述类」四步答；素材：太空题用 science fiction movies / documentaries，别装专业天文。。",
          "logic": "事实：学校科学课/纪录片了解太空。",
          "material": "太空题用 science fiction movies / documentaries，别装专业天文。",
          "words": {
            "正面回答": [
              "Yes",
              "in school",
              "Through documentaries",
              "A bit"
            ],
            "来源或举例": [
              "science class",
              "documentaries",
              "science fiction movies"
            ],
            "频次": [
              "in primary school",
              "years ago",
              "from time to time"
            ],
            "感受": [
              "found it fascinating",
              "sparked curiosity",
              "still curious"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with science class and documentaries, which left a clear impression on me. That happened years ago, so I still remember the details. Overall, I find it practical, and found it fascinating is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 44,
          "title": "What city do you live in",
          "q": "What city do you live in?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "a major city",
              "university town",
              "where I study"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I live in a big city. To be specific, I would mention a major city and university town, which matters in my daily routine. I usually talk about this every day, and I can give a short example if needed. I find it relaxed, so feel relaxed and at ease is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 45,
          "title": "How long have you lived in this city",
          "q": "How long have you lived in this city?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "with easy access to the subway"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I have lived there for several years. The main point is surrounded by convenience stores and shopping malls, which shapes my answer clearly. This has been true every day, so I do not need a complicated story. I find it relaxed, and feel relaxed and at ease is the feeling I want to share.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 46,
          "title": "Is this city your permanent residence",
          "q": "Is this city your permanent residence?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "for now yes",
              "while studying",
              "not sure long-term"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "For now, yes. For example, I can talk about for now yes and while studying, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it relaxed, and feel relaxed and at ease is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 47,
          "title": "Are there big changes in this city",
          "q": "Are there big changes in this city?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：城市变化：新建筑/交通发展。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：城市变化：新建筑/交通发展。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "Yes",
              "huge changes",
              "Definitely",
              "Many changes"
            ],
            "来源或举例": [
              "new skyscrapers",
              "expanded subway",
              "more parks"
            ],
            "频次": [
              "in recent years",
              "since I arrived",
              "constantly"
            ],
            "感受": [
              "more modern",
              "more convenient",
              "hard to recognise some areas"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about new skyscrapers and expanded subway, which is quite typical for me. I notice this in recent years, so it is easy to keep the answer concrete. I find it convenient, and more modern is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 48,
          "title": "Are there people of different ages living in this city",
          "q": "Are there people of different ages living in this city?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：各年龄段都有，老少皆宜。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：各年龄段都有，老少皆宜。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "Yes",
              "all ages",
              "Definitely",
              "Very diverse"
            ],
            "来源或举例": [
              "young professionals",
              "families with kids",
              "elderly residents"
            ],
            "频次": [
              "everywhere",
              "in every district",
              "in my neighbourhood"
            ],
            "感受": [
              "vibrant mix",
              "balanced community",
              "feel inclusive"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about young professionals and families with kids, which is quite typical for me. I notice this everywhere, so it is easy to keep the answer concrete. I find it practical, and vibrant mix is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 49,
          "title": "Are the people friendly in the city",
          "q": "Are the people friendly in the city?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：城市人友善/忙碌但乐于助人。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：城市人友善/忙碌但乐于助人。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "Yes",
              "quite friendly",
              "Most are helpful",
              "Generally yes"
            ],
            "来源或举例": [
              "give directions",
              "help strangers",
              "polite in shops"
            ],
            "频次": [
              "when you need help",
              "in daily interactions",
              "often"
            ],
            "感受": [
              "feel welcome",
              "warm despite busy life",
              "positive impression"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about give directions and help strangers, which is quite typical for me. I notice this often, so it is easy to keep the answer concrete. I find it positive, and feel welcome is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "21"
        },
        {
          "id": 50,
          "title": "What's the weather like where you live",
          "q": "What's the weather like where you live?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「事实陈述类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "事实：直接 Yes/No + 具体细节；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since I was a child",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "hot summers",
              "mild winters",
              "four seasons"
            ],
            "频次": [
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit back and relax",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "I live in a big city. For example, I can talk about hot summers and mild winters, which is quite typical for me. I notice this every day, so it is easy to keep the answer concrete. I find it relaxed, and feel relaxed and at ease is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "21"
        },
        {
          "id": 51,
          "title": "When did you start to learn about science",
          "q": "When did you start to learn about science?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 16,
          "tip": "【新增·热度#16·近1834人】事实：小学科学课开始接触。 本题按「事实陈述类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "事实：小学科学课开始接触。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "In primary school",
              "Around age 7",
              "Early years"
            ],
            "来源或举例": [
              "science class",
              "simple experiments",
              "with my teacher"
            ],
            "频次": [
              "years ago",
              "through school",
              "step by step"
            ],
            "感受": [
              "was interesting",
              "built curiosity",
              "foundation for later"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "In primary school. For example, I can talk about science class and simple experiments, which is quite typical for me. I notice this years ago, so it is easy to keep the answer concrete. I find it practical, and was interesting is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 52,
          "title": "What kinds of interesting things have you done with science",
          "q": "What kinds of interesting things have you done with science?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 16,
          "tip": "【新增·热度#16·近1834人】事实：实验课/参观科技馆经历。 本题按「事实陈述类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "事实：实验课/参观科技馆经历。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "Several things",
              "A few experiments",
              "Quite a few"
            ],
            "来源或举例": [
              "science museum",
              "lab experiments",
              "biology projects"
            ],
            "频次": [
              "in school",
              "during the holidays",
              "years ago"
            ],
            "感受": [
              "really fun",
              "hands-on learning",
              "memorable experiences"
            ]
          },
          "frames": {
            "1": {
              "name": "句型2 I prefer / am keen on",
              "pattern": "I prefer / am keen on ______ because ______.",
              "tip": "第2步：类型题用 prefer / keen on + 简短原因"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Several things. To be specific, I would mention science museum and lab experiments, which matters in my daily routine. I usually talk about this during the holidays, and I can give a short example if needed. I find it fun, so really fun is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 53,
          "title": "Have you seen an unforgettable and beautiful view or scenery",
          "q": "Have you seen an unforgettable and beautiful view or scenery?",
          "topicEn": "Views",
          "topicZh": "风景/取景",
          "tag": "沿用",
          "recentCount": 1743,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近1743人】事实：旅行见过的山海/城市夜景。 本题按「事实陈述类」四步答；素材：与 scenery 共用 take photos of views，城乡对比即可。。",
          "logic": "事实：旅行见过的山海/城市夜景。",
          "material": "与 scenery 共用 take photos of views，城乡对比即可。",
          "words": {
            "正面回答": [
              "Yes",
              "absolutely",
              "Several times",
              "One stands out"
            ],
            "来源或举例": [
              "mountain sunrise",
              "sea at sunset",
              "city night view"
            ],
            "频次": [
              "while travelling",
              "last summer",
              "on vacation"
            ],
            "感受": [
              "unforgettable",
              "took many photos",
              "still remember clearly"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about mountain sunrise and sea at sunset, which is quite typical for me. I notice this last summer, so it is easy to keep the answer concrete. I find it practical, and unforgettable is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 54,
          "title": "Are you good at telling jokes",
          "q": "Are you good at telling jokes?",
          "topicEn": "Jokes & Comedies",
          "topicZh": "笑话与喜剧",
          "tag": "新增",
          "recentCount": 1680,
          "heatRank": 18,
          "tip": "【新增·热度#18·近1680人】事实：坦诚不太会/偶尔讲冷笑话。 本题按「事实陈述类」四步答；素材：笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。。",
          "logic": "事实：坦诚不太会/偶尔讲冷笑话。",
          "material": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
          "words": {
            "正面回答": [
              "Not really",
              "A little",
              "Sometimes"
            ],
            "来源或举例": [
              "forget the punchline",
              "only simple jokes",
              "with close friends"
            ],
            "频次": [
              "rarely",
              "at gatherings",
              "when mood is right"
            ],
            "感受": [
              "others laugh more",
              "still fun",
              "not my strength"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Not really. For example, I can talk about forget the punchline and only simple jokes, which is quite typical for me. I notice this rarely, so it is easy to keep the answer concrete. I find it fun, and others laugh more is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 55,
          "title": "Do your friends like to tell jokes",
          "q": "Do your friends like to tell jokes?",
          "topicEn": "Jokes & Comedies",
          "topicZh": "笑话与喜剧",
          "tag": "新增",
          "recentCount": 1680,
          "heatRank": 18,
          "tip": "【新增·热度#18·近1680人】事实：朋友爱讲笑话活跃气氛。 本题按「事实陈述类」四步答；素材：笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。。",
          "logic": "事实：朋友爱讲笑话活跃气氛。",
          "material": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
          "words": {
            "正面回答": [
              "Yes",
              "some do",
              "Quite a few",
              "Especially one friend"
            ],
            "来源或举例": [
              "make people laugh",
              "at parties",
              "on WeChat"
            ],
            "频次": [
              "when we hang out",
              "quite often",
              "to lighten the mood"
            ],
            "感受": [
              "great atmosphere",
              "have a good laugh",
              "feel closer"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about make people laugh and at parties, which is quite typical for me. I notice this quite often, so it is easy to keep the answer concrete. I find it practical, and great atmosphere is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 56,
          "title": "Have you ever watched a live show",
          "q": "Have you ever watched a live show?",
          "topicEn": "Jokes & Comedies",
          "topicZh": "笑话与喜剧",
          "tag": "新增",
          "recentCount": 1680,
          "heatRank": 18,
          "tip": "【新增·热度#18·近1680人】事实：看过脱口秀/相声现场演出。 本题按「事实陈述类」四步答；素材：笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。。",
          "logic": "事实：看过脱口秀/相声现场演出。",
          "material": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
          "words": {
            "正面回答": [
              "Yes",
              "once",
              "A couple of times",
              "Not yet"
            ],
            "来源或举例": [
              "stand-up comedy",
              "live show",
              "with friends"
            ],
            "频次": [
              "last year",
              "during a festival",
              "rarely"
            ],
            "感受": [
              "have a good laugh",
              "great atmosphere",
              "unforgettable night"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with stand-up comedy and live show, which left a clear impression on me. That happened last year, so I still remember the details. Overall, I find it practical, and have a good laugh is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 57,
          "title": "Are there tall buildings near your home",
          "q": "Are there tall buildings near your home?",
          "topicEn": "Building",
          "topicZh": "建筑",
          "tag": "沿用",
          "recentCount": 1400,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1400人】事实：直接 Yes/No + 具体细节；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。 本题按「事实陈述类」四步答；素材：建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。。",
          "logic": "事实：直接 Yes/No + 具体细节；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "material": "建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "words": {
            "正面回答": [
              "Yes",
              "lots of them",
              "Definitely",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "like shopping malls and hotels",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "go there regularly",
              "in my free time",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "super convenient",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about like shopping malls and hotels and such as, which is quite typical for me. I notice this in my free time, so it is easy to keep the answer concrete. I find it convenient, and super convenient is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue",
          "clueId": "7"
        },
        {
          "id": 58,
          "title": "Have you ever sent handmade gifts to others",
          "q": "Have you ever sent handmade gifts to others?",
          "topicEn": "Gifts",
          "topicZh": "礼物",
          "tag": "沿用",
          "recentCount": 1386,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近1386人】事实：送过手工礼物→具体做了什么+对方反应。 本题按「事实陈述类」四步答；素材：礼物=handmade / thoughtful gift，选择看 receiver's preference。。",
          "logic": "事实：送过手工礼物→具体做了什么+对方反应。",
          "material": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "words": {
            "正面回答": [
              "Yes",
              "I have",
              "A few times",
              "Definitely"
            ],
            "来源或举例": [
              "a handmade card",
              "knitted scarf",
              "DIY gift"
            ],
            "频次": [
              "on birthdays",
              "for close friends",
              "from time to time"
            ],
            "感受": [
              "they were touched",
              "meaningful",
              "worth the effort"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, I have. I once made a handmade card and a DIY gift for a close friend, which they really liked. I do this on birthdays from time to time. I find it meaningful and worth the effort.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit",
          "clueId": "3"
        },
        {
          "id": 59,
          "title": "Have you ever received a great gift",
          "q": "Have you ever received a great gift?",
          "topicEn": "Gifts",
          "topicZh": "礼物",
          "tag": "沿用",
          "recentCount": 1386,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近1386人】事实：收到好礼物→谁送的+为什么感动。 本题按「事实陈述类」四步答；素材：礼物=handmade / thoughtful gift，选择看 receiver's preference。。",
          "logic": "事实：收到好礼物→谁送的+为什么感动。",
          "material": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "Sure"
            ],
            "来源或举例": [
              "a thoughtful gift",
              "from my best friend",
              "last month"
            ],
            "频次": [
              "on my birthday",
              "last year",
              "once in a while"
            ],
            "感受": [
              "really surprised",
              "made me happy",
              "unexpected surprise"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. I received a thoughtful gift from my best friend last month, which really surprised me. It was on my birthday, and I still remember how excited I felt. I find such gifts really make me happy, and they mean more than expensive things.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit",
          "clueId": "3"
        },
        {
          "id": 60,
          "title": "What gift have you received recently",
          "q": "What gift have you received recently?",
          "topicEn": "Gifts",
          "topicZh": "礼物",
          "tag": "沿用",
          "recentCount": 1386,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近1386人】事实：最近礼物→物品+场合+一句感受。 本题按「事实陈述类」四步答；素材：礼物=handmade / thoughtful gift，选择看 receiver's preference。。",
          "logic": "事实：最近礼物→物品+场合+一句感受。",
          "material": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "words": {
            "正面回答": [
              "Yes",
              "recently",
              "Just last month",
              "A small gift"
            ],
            "来源或举例": [
              "a book",
              "from my parents",
              "birthday present"
            ],
            "频次": [
              "last month",
              "this year",
              "not long ago"
            ],
            "感受": [
              "really thoughtful",
              "practical",
              "I loved it"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. To be specific, I would mention a book and from my parents, which matters in my daily routine. I usually talk about this last month, and I can give a short example if needed. I find it thoughtful, so really thoughtful is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "3"
        },
        {
          "id": 61,
          "title": "Have you ever had a pet before",
          "q": "Have you ever had a pet before?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 21,
          "tip": "【沿用·热度#21·近1330人】事实：宠物=puppy at home 本题按「事实陈述类」四步答；素材：宠物=puppy at home。",
          "logic": "事实：宠物=puppy at home",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "Yes",
              "absolutely",
              "used to"
            ],
            "来源或举例": [
              "a puppy",
              "dorms",
              "home"
            ],
            "频次": [
              "every day",
              "the park",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "unwind",
              "really lifts my mood",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with a puppy and dorms, which left a clear impression on me. That happened every day, so I still remember the details. Overall, I find it lifts my mood, and unwind is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue",
          "clueId": "1"
        },
        {
          "id": 62,
          "title": "Have you ever visited a zoo",
          "q": "Have you ever visited a zoo?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 21,
          "tip": "【沿用·热度#21·近1330人】事实：宠物=puppy at home 本题按「事实陈述类」四步答；素材：宠物=puppy at home。",
          "logic": "事实：宠物=puppy at home",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "Yes",
              "absolutely",
              "used to"
            ],
            "来源或举例": [
              "a puppy",
              "dorms",
              "home"
            ],
            "频次": [
              "every day",
              "the park",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "unwind",
              "really lifts my mood",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with a puppy and dorms, which left a clear impression on me. That happened every day, so I still remember the details. Overall, I find it lifts my mood, and unwind is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 63,
          "title": "When did you learn how to type on a keyboard",
          "q": "When did you learn how to type on a keyboard?",
          "topicEn": "Typing",
          "topicZh": "打字",
          "tag": "沿用",
          "recentCount": 1260,
          "heatRank": 22,
          "tip": "【沿用·热度#22·近1260人】事实：直接 Yes/No + 具体细节；打字=daily laptop + practice speed，对比 handwriting 强调 faster。 本题按「事实陈述类」四步答；素材：打字=daily laptop + practice speed，对比 handwriting 强调 faster。。",
          "logic": "事实：直接 Yes/No + 具体细节；打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "material": "打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "words": {
            "正面回答": [
              "In my childhood",
              "in primary school",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "through online shopping",
              "play video games",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "regularly",
              "as often as I can",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "practical",
              "time-saving",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about through online shopping and play video games, which is quite typical for me. I notice this as often as I can, so it is easy to keep the answer concrete. I find it practical, and practical is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "5"
        },
        {
          "id": 64,
          "title": "How do you improve your typing",
          "q": "How do you improve your typing?",
          "topicEn": "Typing",
          "topicZh": "打字",
          "tag": "沿用",
          "recentCount": 1260,
          "heatRank": 22,
          "tip": "【沿用·热度#22·近1260人】事实：直接 Yes/No + 具体细节；打字=daily laptop + practice speed，对比 handwriting 强调 faster。 本题按「事实陈述类」四步答；素材：打字=daily laptop + practice speed，对比 handwriting 强调 faster。。",
          "logic": "事实：直接 Yes/No + 具体细节；打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "material": "打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "words": {
            "正面回答": [
              "In my childhood",
              "in primary school",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "through online shopping",
              "play video games",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "regularly",
              "as often as I can",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "practical",
              "time-saving",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. The main point is through online shopping and play video games, which shapes my answer clearly. This has been true as often as I can, so I do not need a complicated story. I find it practical, and practical is the feeling I want to share.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "5"
        },
        {
          "id": 65,
          "title": "Are you good at memorising things",
          "q": "Are you good at memorising things?",
          "topicEn": "Memory",
          "topicZh": "记忆",
          "tag": "沿用",
          "recentCount": 1218,
          "heatRank": 23,
          "tip": "【沿用·热度#23·近1218人】事实：记忆力好/一般+用手机备忘。 本题按「事实陈述类」四步答；素材：记忆=phone notes / to-do list，忘事承认 once forgot + lesson。。",
          "logic": "事实：记忆力好/一般+用手机备忘。",
          "material": "记忆=phone notes / to-do list，忘事承认 once forgot + lesson。",
          "words": {
            "正面回答": [
              "Average",
              "Pretty good",
              "Depends on the topic"
            ],
            "来源或举例": [
              "phone notes",
              "to-do list",
              "repeat out loud"
            ],
            "频次": [
              "for exams",
              "daily reminders",
              "important dates"
            ],
            "感受": [
              "works for me",
              "still forget sometimes",
              "need reminders"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Average. For example, I can talk about phone notes and to-do list, which is quite typical for me. I notice this for exams, so it is easy to keep the answer concrete. I find it practical, and works for me is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 66,
          "title": "Have you ever forgotten something important",
          "q": "Have you ever forgotten something important?",
          "topicEn": "Memory",
          "topicZh": "记忆",
          "tag": "沿用",
          "recentCount": 1218,
          "heatRank": 23,
          "tip": "【沿用·热度#23·近1218人】事实：忘带钥匙/证件经历+教训。 本题按「事实陈述类」四步答；素材：记忆=phone notes / to-do list，忘事承认 once forgot + lesson。。",
          "logic": "事实：忘带钥匙/证件经历+教训。",
          "material": "记忆=phone notes / to-do list，忘事承认 once forgot + lesson。",
          "words": {
            "正面回答": [
              "Yes",
              "unfortunately",
              "Once or twice",
              "More than once"
            ],
            "来源或举例": [
              "forgot my keys",
              "missed a deadline",
              "left my ID at home"
            ],
            "频次": [
              "last semester",
              "years ago",
              "recently"
            ],
            "感受": [
              "it taught me to be more careful",
              "really stressful",
              "learned a lesson"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with forgot my keys and missed a deadline, which left a clear impression on me. That happened last semester, so I still remember the details. Overall, I find it stressful, and it taught me to be more careful is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 67,
          "title": "What do you need to remember in your daily life",
          "q": "What do you need to remember in your daily life?",
          "topicEn": "Memory",
          "topicZh": "记忆",
          "tag": "沿用",
          "recentCount": 1218,
          "heatRank": 23,
          "tip": "【沿用·热度#23·近1218人】事实：课程表/作业/约会日程。 本题按「事实陈述类」四步答；素材：记忆=phone notes / to-do list，忘事承认 once forgot + lesson。。",
          "logic": "事实：课程表/作业/约会日程。",
          "material": "记忆=phone notes / to-do list，忘事承认 once forgot + lesson。",
          "words": {
            "正面回答": [
              "Many things",
              "Quite a lot",
              "A long list"
            ],
            "来源或举例": [
              "class schedule",
              "assignments",
              "friends' birthdays"
            ],
            "频次": [
              "every day",
              "every morning",
              "before leaving home"
            ],
            "感受": [
              "phone reminders help",
              "sometimes stressful",
              "part of student life"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Quite a lot. To be specific, I would mention class schedule and assignments, which matters in my daily routine. I usually talk about this every day, and I can give a short example if needed. I find it practical, so phone reminders help is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 68,
          "title": "Have you ever been part of a sports team",
          "q": "Have you ever been part of a sports team?",
          "topicEn": "Sports team",
          "topicZh": "运动队",
          "tag": "沿用",
          "recentCount": 1022,
          "heatRank": 24,
          "tip": "【沿用·热度#24·近1022人】事实：运动队=basketball/volleyball + teamwork，观看与参与同一套。 本题按「事实陈述类」四步答；素材：运动队=basketball/volleyball + teamwork，观看与参与同一套。。",
          "logic": "事实：运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "material": "运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "words": {
            "正面回答": [
              "Definitely",
              "Yes",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "play basketball",
              "volleyball in the sports centre",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "at weekends",
              "in my free time",
              "every day",
              "from time to time"
            ],
            "感受": [
              "sense of teamwork",
              "practical",
              "really convenient",
              "quite useful",
              "helpful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which 经历举例",
              "pattern": "Yes, I ______, which ______.",
              "tip": "第2步：Have you ever 用经历 + which 补感受"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I once dealt with play basketball and volleyball in the sports centre, which left a clear impression on me. That happened at weekends, so I still remember the details. Overall, I find it practical, and sense of teamwork is what I would emphasise.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue",
          "clueId": "2"
        },
        {
          "id": 69,
          "title": "What did you often do with your friends in your childhood",
          "q": "What did you often do with your friends in your childhood?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 25,
          "tip": "【沿用·热度#25·近959人】事实：童年和朋友户外玩/骑车。 本题按「事实陈述类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "事实：童年和朋友户外玩/骑车。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "Many things",
              "Quite a lot",
              "Played outside"
            ],
            "来源或举例": [
              "play outside",
              "ride bikes",
              "play video games"
            ],
            "频次": [
              "after school",
              "at weekends",
              "almost every day"
            ],
            "感受": [
              "carefree days",
              "great memories",
              "still close friends"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Quite a lot. To be specific, I would mention play outside and ride bikes, which matters in my daily routine. I usually talk about this after school, and I can give a short example if needed. I find it practical, so carefree days is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "m1"
        },
        {
          "id": 70,
          "title": "Do you have any plans for the next five years",
          "q": "Do you have any plans for the next five years?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 25,
          "tip": "【沿用·热度#25·近959人】事实：五年计划：毕业/工作/提升。 本题按「事实陈述类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "事实：五年计划：毕业/工作/提升。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "A rough plan",
              "Several goals"
            ],
            "来源或举例": [
              "graduate",
              "find a good job",
              "improve my skills"
            ],
            "频次": [
              "after university",
              "step by step",
              "in the next few years"
            ],
            "感受": [
              "excited about the future",
              "need to work hard",
              "clear direction"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about graduate and find a good job, which is quite typical for me. I notice this after university, so it is easy to keep the answer concrete. I find it practical, and excited about the future is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit",
          "clueId": "m2"
        },
        {
          "id": 71,
          "title": "Where did you go for a walk lately",
          "q": "Where did you go for a walk lately?",
          "topicEn": "Walking",
          "topicZh": "走路",
          "tag": "沿用",
          "recentCount": 854,
          "heatRank": 26,
          "tip": "【沿用·热度#26·近854人】事实：直接 Yes/No + 具体细节；走路=go for a walk in the park，解压+景色一笔带过。 本题按「事实陈述类」四步答；素材：走路=go for a walk in the park，解压+景色一笔带过。。",
          "logic": "事实：直接 Yes/No + 具体细节；走路=go for a walk in the park，解压+景色一笔带过。",
          "material": "走路=go for a walk in the park，解压+景色一笔带过。",
          "words": {
            "正面回答": [
              "Recently",
              "just a few days ago",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "the local park",
              "city centre",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "after dinner",
              "feel bored",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "feel relaxed and at ease",
              "clear my mind",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. The key details are the local park and city centre, which are easy to notice in real life. I experience this after dinner, so I can describe it without making things up. I find this place relaxed, and feel relaxed and at ease is how I feel about it.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue",
          "clueId": "4"
        },
        {
          "id": 72,
          "title": "What are the most beautiful sights you have seen while traveling",
          "q": "What are the most beautiful sights you have seen while traveling?",
          "topicEn": "Scenery",
          "topicZh": "景色",
          "tag": "沿用",
          "recentCount": 777,
          "heatRank": 27,
          "tip": "【沿用·热度#27·近777人】事实：直接 Yes/No + 具体细节；景色=travel + take photos，山/海对比用 mountains vs sea。 本题按「事实陈述类」四步答；素材：景色=travel + take photos，山/海对比用 mountains vs sea。。",
          "logic": "事实：直接 Yes/No + 具体细节；景色=travel + take photos，山/海对比用 mountains vs sea。",
          "material": "景色=travel + take photos，山/海对比用 mountains vs sea。",
          "words": {
            "正面回答": [
              "To be honest",
              "the seaside",
              "Yes",
              "Definitely",
              "Not really"
            ],
            "来源或举例": [
              "take photos of the stunning views",
              "such as",
              "in particular",
              "for instance"
            ],
            "频次": [
              "during the holidays",
              "when I have time off",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "It",
              "s something I",
              "ll never forget"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. To be specific, I would mention take photos of the stunning views and such as, which matters in my daily routine. I usually talk about this during the holidays, and I can give a short example if needed. I find it practical, so It is a fair summary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue",
          "clueId": "6"
        },
        {
          "id": 73,
          "title": "Is the city where you live crowded",
          "q": "Is the city where you live crowded?",
          "topicEn": "Crowded place",
          "topicZh": "拥挤的地方",
          "tag": "沿用",
          "recentCount": 728,
          "heatRank": 28,
          "tip": "【沿用·热度#28·近728人】事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。 本题按「事实陈述类」四步答；素材：拥挤=city centre / rush hour / shopping malls，喜好偏 not really。。",
          "logic": "事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "material": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "words": {
            "正面回答": [
              "Honestly",
              "yes",
              "Definitely",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "downtown",
              "rush hour",
              "shopping malls"
            ],
            "频次": [
              "every single day",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it really gets to me",
              "feel awful",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about downtown and rush hour, which is quite typical for me. I notice this every single day, so it is easy to keep the answer concrete. I find it practical, and it really gets to me is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "13"
        },
        {
          "id": 74,
          "title": "Is there a crowded place near where you live",
          "q": "Is there a crowded place near where you live?",
          "topicEn": "Crowded place",
          "topicZh": "拥挤的地方",
          "tag": "沿用",
          "recentCount": 728,
          "heatRank": 28,
          "tip": "【沿用·热度#28·近728人】事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。 本题按「事实陈述类」四步答；素材：拥挤=city centre / rush hour / shopping malls，喜好偏 not really。。",
          "logic": "事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "material": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "words": {
            "正面回答": [
              "Honestly",
              "yes",
              "Definitely",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "the city centre",
              "near the subway station",
              "weekend markets"
            ],
            "频次": [
              "every single day",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it really gets to me",
              "feel awful",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about the city centre and near the subway station, which is quite typical for me. I notice this every single day, so it is easy to keep the answer concrete. I find it practical, and it really gets to me is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "13"
        },
        {
          "id": 75,
          "title": "When was the last time you were in a crowded place",
          "q": "When was the last time you were in a crowded place?",
          "topicEn": "Crowded place",
          "topicZh": "拥挤的地方",
          "tag": "沿用",
          "recentCount": 728,
          "heatRank": 28,
          "tip": "【沿用·热度#28·近728人】事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。 本题按「事实陈述类」四步答；素材：拥挤=city centre / rush hour / shopping malls，喜好偏 not really。。",
          "logic": "事实：直接 Yes/No + 具体细节；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "material": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "words": {
            "正面回答": [
              "Honestly",
              "yes",
              "Definitely",
              "Not really",
              "Sometimes"
            ],
            "来源或举例": [
              "the shopping mall",
              "during a holiday",
              "last weekend"
            ],
            "频次": [
              "every single day",
              "every day",
              "from time to time",
              "at weekends"
            ],
            "感受": [
              "it really gets to me",
              "feel awful",
              "practical",
              "really convenient",
              "quite useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型4 which / 句型5 to do",
              "pattern": "I ______ (举例/地点), which ______. / I ______ to ______.",
              "tip": "第2步：举例后用 which 补结果，或用 to do 交代目的"
            },
            "2": {
              "name": "句型6 Whenever / As long as",
              "pattern": "Whenever / As long as I ______, I ______.",
              "tip": "第3步：时间/条件状语，交代什么时候会做"
            },
            "3": {
              "name": "句型1B / 句型2 I find",
              "pattern": "I find it ______ to ______. / I find this ______.",
              "tip": "第4步：形式宾语或宾补，收束感受"
            }
          },
          "sample": "Yes, definitely. For example, I can talk about the shopping mall and during a holiday, which is quite typical for me. I notice this every single day, so it is easy to keep the answer concrete. I find it practical, and it really gets to me is what I would say at the end.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias",
          "clueId": "13"
        }
      ]
    },
    {
      "id": "xihao",
      "name": "喜好类",
      "steps": [
        "正面回答",
        "原因或时间",
        "频次",
        "感受"
      ],
      "questions": [
        {
          "id": 1,
          "title": "Did you enjoy traveling by car when you were a kid",
          "q": "Did you enjoy traveling by car when you were a kid?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 1,
          "tip": "【新增·热度#1·近12327人】喜好：童年坐车出游开心，去郊区/回老家。 本题按「喜好类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "喜好：童年坐车出游开心，去郊区/回老家。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "Yes",
              "I loved it",
              "Definitely",
              "So much fun"
            ],
            "原因或时间": [
              "family road trips",
              "when I was a child",
              "during the holidays"
            ],
            "频次": [
              "during the holidays",
              "a few times a year",
              "often"
            ],
            "感受": [
              "feel relaxed and at ease",
              "great memories",
              "so much fun"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, I loved it. When I was a child, we often went on family road trips during the holidays, which created great memories. Back then I felt relaxed and at ease in the car. I find those trips so much fun even now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 2,
          "title": "What types of cars do you like",
          "q": "What types of cars do you like?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 1,
          "tip": "【新增·热度#1·近12327人】喜好：SUV/舒适轿车，理由=空间/安全，别背参数。 本题按「喜好类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "喜好：SUV/舒适轿车，理由=空间/安全，别背参数。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "I prefer SUVs",
              "Comfortable sedans",
              "Electric cars"
            ],
            "原因或时间": [
              "more space",
              "comfortable seats",
              "feel safer"
            ],
            "频次": [
              "for long trips",
              "with my family",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "feel safer",
              "more comfortable",
              "practical"
            ]
          },
          "frames": {
            "1": {
              "name": "句型2 I prefer / am keen on",
              "pattern": "I prefer / am keen on ______ because ______.",
              "tip": "第2步：类型题用 prefer / keen on + 简短原因"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I prefer SUVs for the reason that they have more space and comfortable seats. I am keen on them for long trips with my family to feel safer. I find this type more comfortable and practical.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 3,
          "title": "Will you buy an expensive car in the future",
          "q": "Will you buy an expensive car in the future?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 1,
          "tip": "【新增·热度#1·近12327人】喜好：务实→先实用再考虑，或说毕业后努力买。 本题按「喜好类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "喜好：务实→先实用再考虑，或说毕业后努力买。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "Maybe in the future",
              "Not sure yet",
              "Perhaps"
            ],
            "原因或时间": [
              "after I graduate",
              "when I can afford it",
              "a practical car first"
            ],
            "频次": [
              "not at the moment",
              "in a few years",
              "after I start working"
            ],
            "感受": [
              "practical matters more",
              "quality over price",
              "it depends"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Maybe in the future. I plan to buy a practical car first after I graduate, when I can afford it. In a few years, after I start working, I might reconsider. For now, practical matters more than price.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 4,
          "title": "Do you like your subject",
          "q": "Do you like your subject?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I'm passionate about it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "really convenient",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "attend classes",
              "listen to a lecture",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "self-motivated",
              "strive in one",
              "s studies"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm passionate about it. I am keen on this for the reason that really convenient and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity practical, which helps me unwind, and self-motivated.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 5,
          "title": "Do you want to change your major",
          "q": "Do you want to change your major?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "absolutely not",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "I'm passionate about it",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "study at the library",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it will be useful for my future career",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on I'm passionate about it and because for the reason that it fits my long-term plan. I may do this quite often, after I have more time and money. I find the idea useful, and it will be useful for my future career is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 6,
          "title": "Are you looking forward to working",
          "q": "Are you looking forward to working?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "Definitely",
              "Yes",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "after graduation",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "no longer rely on my parents",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "stand on my own two feet",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that after graduation and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and stand on my own two feet.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 7,
          "title": "Do you like your job",
          "q": "Do you like your job?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "yes",
              "I do",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "a great atmosphere",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "exchange ideas",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "both practical and fulfilling",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that a great atmosphere and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity practical, which helps me unwind, and both practical and fulfilling.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 8,
          "title": "Do you want to change to another job",
          "q": "Do you want to change to another job?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "not at the moment",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "at this stage of my life of my life of my life of my life of my life",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "focus on my current work",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "feel relaxed and at ease",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on at this stage of my life of my life of my life of my life of my life and because for the reason that it fits my long-term plan. I may do this quite often, after I have more time and money. I find the idea relaxed, and feel relaxed and at ease is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 9,
          "title": "Do you miss being a student",
          "q": "Do you miss being a student?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I absolutely miss it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when work gets tiring",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "the school canteen and the classrooms",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "holds a lot of precious memories",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I absolutely miss it. I am keen on this for the reason that when work gets tiring and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and holds a lot of precious memories.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 10,
          "title": "What changes would you like to see in your school",
          "q": "What changes would you like to see in your school?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「喜好类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "喜好：说清喜欢什么+原因；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I'd improve the food in the canteen",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "have a good laugh",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'd improve the food in the canteen. I hope to focus on because and when I for the reason that it fits my long-term plan. I may do this quite often, after I have more time and money. I find the idea relaxed, and have a good laugh is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 11,
          "title": "What is your favourite website",
          "q": "What is your favourite website?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 3,
          "tip": "【新增·热度#3·近8064人】喜好：B站/小红书/学校平台，说清用途。 本题按「喜好类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "喜好：B站/小红书/学校平台，说清用途。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Bilibili",
              "Xiaohongshu",
              "Definitely Bilibili"
            ],
            "原因或时间": [
              "watch tutorials",
              "relax",
              "learn new skills"
            ],
            "频次": [
              "almost every day",
              "in my free time",
              "at night"
            ],
            "感受": [
              "it always cheers me up",
              "really fun",
              "very useful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "My favourite is Bilibili. I am keen on it for the reason that I can watch tutorials and learn new skills. I visit it almost every day in my free time to relax. I find it really fun and very useful.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 12,
          "title": "Would you like to have your own website",
          "q": "Would you like to have your own website?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 3,
          "tip": "【新增·热度#3·近8064人】喜好：想有个人博客/作品集，毕业后。 本题按「喜好类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "喜好：想有个人博客/作品集，毕业后。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Yes",
              "I'd love to",
              "Maybe someday",
              "Sounds cool"
            ],
            "原因或时间": [
              "share my portfolio",
              "write blog posts",
              "in the future"
            ],
            "频次": [
              "not right now",
              "after graduation",
              "when I have time"
            ],
            "感受": [
              "sounds cool",
              "a good idea",
              "would be fun"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on share my portfolio and write blog posts for the reason that it fits my long-term plan. I may do this after graduation, after I have more time and money. I find the idea fun, and sounds cool is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 13,
          "title": "Do you have a favorite teacher",
          "q": "Do you have a favorite teacher?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】喜好：最喜欢某科老师，原因耐心有趣。 本题按「喜好类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "喜好：最喜欢某科老师，原因耐心有趣。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "One favourite"
            ],
            "原因或时间": [
              "patient and humorous",
              "makes class engaging",
              "explains clearly"
            ],
            "频次": [
              "every week",
              "in every class",
              "through the semester"
            ],
            "感受": [
              "I enjoy their classes",
              "never boring",
              "learn a lot"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that patient and humorous and makes class engaging matters to me. Whenever I have time, I enjoy it every week to stay positive. I find this activity practical, which helps me unwind, and I enjoy their classes.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 14,
          "title": "Do you want to be a teacher in the future",
          "q": "Do you want to be a teacher in the future?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】喜好：想当/不想当+原因（分享知识/压力大）。 本题按「喜好类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "喜好：想当/不想当+原因（分享知识/压力大）。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "Not really",
              "Maybe",
              "Haven't decided"
            ],
            "原因或时间": [
              "too much pressure",
              "love sharing knowledge",
              "respect the job"
            ],
            "频次": [
              "haven't decided",
              "maybe later",
              "not my plan now"
            ],
            "感受": [
              "it depends",
              "could be rewarding",
              "admire teachers"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Not really. I hope to focus on too much pressure and love sharing knowledge for the reason that it fits my long-term plan. I may do this haven't decided, after I have more time and money. I find the idea practical, and it depends is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 15,
          "title": "Did you like going to parks as a child",
          "q": "Did you like going to parks as a child?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】喜好：童年爱去公园玩/散步。 本题按「喜好类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "喜好：童年爱去公园玩/散步。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Yes",
              "I loved it",
              "Absolutely",
              "So much fun"
            ],
            "原因或时间": [
              "play outside",
              "with my parents",
              "when I was a child"
            ],
            "频次": [
              "at weekends",
              "during the holidays",
              "often"
            ],
            "感受": [
              "feel relaxed and at ease",
              "great memories",
              "fresh air"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that play outside and with my parents matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity relaxed, which helps me unwind, and feel relaxed and at ease.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 16,
          "title": "Do you still like going to parks now",
          "q": "Do you still like going to parks now?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】喜好：现在仍爱公园散步/透气。 本题按「喜好类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "喜好：现在仍爱公园散步/透气。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Still love it",
              "Quite often"
            ],
            "原因或时间": [
              "go for a walk",
              "fresh air",
              "escape the the lively atmosphere"
            ],
            "频次": [
              "at weekends",
              "after dinner",
              "when stressed"
            ],
            "感受": [
              "helps me unwind",
              "feel at peace",
              "recharge my energy"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that go for a walk and fresh air matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity practical, which helps me unwind, and helps me unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 17,
          "title": "Would you like to see more parks in your city",
          "q": "Would you like to see more parks in your city?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】喜好：希望更多绿地，理由健康休闲。 本题按「喜好类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "喜好：希望更多绿地，理由健康休闲。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "We need more"
            ],
            "原因或时间": [
              "more green space",
              "for families",
              "better air quality"
            ],
            "频次": [
              "in my neighbourhood",
              "near schools",
              "city planning"
            ],
            "感受": [
              "good for well-being",
              "everyone benefits",
              "really important"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on more green space and for families for the reason that it fits my long-term plan. I may do this in my neighbourhood, after I have more time and money. I find the idea important, and good for well-being is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 18,
          "title": "Are there any parks you want to go to in the future",
          "q": "Are there any parks you want to go to in the future?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】喜好：想去的公园/城市名+理由风景。 本题按「喜好类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "喜好：想去的公园/城市名+理由风景。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Yes",
              "a few",
              "Definitely",
              "Several on my list"
            ],
            "原因或时间": [
              "a famous park",
              "with lakes",
              "better scenery"
            ],
            "频次": [
              "during the holidays",
              "next vacation",
              "when I travel"
            ],
            "感受": [
              "sounds exciting",
              "on my bucket list",
              "would love to visit"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on a famous park and with lakes for the reason that it fits my long-term plan. I may do this during the holidays, after I have more time and money. I find the idea practical, and sounds exciting is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 19,
          "title": "What do you like to do when visiting a park",
          "q": "What do you like to do when visiting a park?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】喜好：散步/聊天/拍照/慢跑。 本题按「喜好类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "喜好：散步/聊天/拍照/慢跑。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Go for a walk",
              "Hang out",
              "Several things"
            ],
            "原因或时间": [
              "with friends",
              "take photos",
              "go jogging"
            ],
            "频次": [
              "at weekends",
              "after dinner",
              "when the weather is nice"
            ],
            "感受": [
              "feel relaxed and at ease",
              "clear my mind",
              "enjoy nature"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Several things. I am keen on this for the reason that with friends and take photos matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity relaxed, which helps me unwind, and feel relaxed and at ease.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 20,
          "title": "Do you like the area that you live in",
          "q": "Do you like the area that you live in?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 6,
          "tip": "【万年·热度#6·近4473人】喜好：说清喜欢什么+原因；住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。 本题按「喜好类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "喜好：说清喜欢什么+原因；住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "Definitely",
              "Yes",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "great infrastructure",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "just a 10-minute walk from my home",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "really convenient",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that great infrastructure and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity convenient, which helps me unwind, and really convenient.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 21,
          "title": "Where do you like to go in that area",
          "q": "Where do you like to go in that area?",
          "topicEn": "The area you live in",
          "topicZh": "你住的区域",
          "tag": "万年",
          "recentCount": 4473,
          "heatRank": 6,
          "tip": "【万年·热度#6·近4473人】喜好：说清喜欢什么+原因；住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。 本题按「喜好类」四步答；素材：住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。。",
          "logic": "喜好：说清喜欢什么+原因；住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "material": "住的区域=residential areas + neighbors + quiet/noisy，变化用 shopping malls。",
          "words": {
            "正面回答": [
              "I love going to the cafes",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when I have some free time",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "read",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "reflect on things",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I love going to the cafes. I am keen on this for the reason that when I have some free time and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and reflect on things.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 22,
          "title": "Do you like shopping",
          "q": "Do you like shopping?",
          "topicEn": "Shopping",
          "topicZh": "购物",
          "tag": "新增",
          "recentCount": 4312,
          "heatRank": 7,
          "tip": "【新增·热度#7·近4312人】喜好：喜欢/不喜欢购物+网购方便。 本题按「喜好类」四步答；素材：购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。。",
          "logic": "喜好：喜欢/不喜欢购物+网购方便。",
          "material": "购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。",
          "words": {
            "正面回答": [
              "Yes",
              "I enjoy it",
              "Sometimes",
              "Not really"
            ],
            "原因或时间": [
              "shop online",
              "shopping malls",
              "pay by phone"
            ],
            "频次": [
              "at weekends",
              "when I need things",
              "from time to time"
            ],
            "感受": [
              "really convenient",
              "fun with friends",
              "can be tiring"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that shop online and shopping malls matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity convenient, which helps me unwind, and really convenient.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 23,
          "title": "Do you like looking at yourself in the mirror? How often",
          "q": "Do you like looking at yourself in the mirror? How often?",
          "topicEn": "Mirrors",
          "topicZh": "镜子",
          "tag": "新增",
          "recentCount": 4116,
          "heatRank": 8,
          "tip": "【新增·热度#8·近4116人】喜好：出门前照镜子+频率每天。 本题按「喜好类」四步答；素材：镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。。",
          "logic": "喜好：出门前照镜子+频率每天。",
          "material": "镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。",
          "words": {
            "正面回答": [
              "Yes",
              "I do",
              "Every day",
              "Quite often"
            ],
            "原因或时间": [
              "before heading out",
              "check my look",
              "when getting dressed"
            ],
            "频次": [
              "every morning",
              "before parties",
              "almost daily"
            ],
            "感受": [
              "feel more confident",
              "part of my routine",
              "takes a minute"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that before heading out and check my look matters to me. Whenever I have time, I enjoy it every morning to stay positive. I find this activity practical, which helps me unwind, and feel more confident.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 24,
          "title": "Would you use mirrors to decorate your room",
          "q": "Would you use mirrors to decorate your room?",
          "topicEn": "Mirrors",
          "topicZh": "镜子",
          "tag": "新增",
          "recentCount": 4116,
          "heatRank": 8,
          "tip": "【新增·热度#8·近4116人】喜好：会用镜子装饰/或觉得不需要。 本题按「喜好类」四步答；素材：镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。。",
          "logic": "喜好：会用镜子装饰/或觉得不需要。",
          "material": "镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。",
          "words": {
            "正面回答": [
              "Maybe",
              "Yes",
              "I would",
              "Not really"
            ],
            "原因或时间": [
              "make the room brighter",
              "modern look",
              "above the desk"
            ],
            "频次": [
              "if I redecorate",
              "in the future",
              "not now"
            ],
            "感受": [
              "looks stylish",
              "practical too",
              "personal taste"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Maybe. I am keen on this for the reason that make the room brighter and modern look matters to me. Whenever I have time, I enjoy it if I redecorate to stay positive. I find this activity practical, which helps me unwind, and looks stylish.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 25,
          "title": "What kind of house or apartment do you want to live in the future",
          "q": "What kind of house or apartment do you want to live in the future?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「喜好类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "a spacious house",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "enjoy the peace and quiet",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "a residential area",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "a good form of self-care",
              "unwind",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Yes, definitely. I hope to focus on enjoy the peace and quiet and because for the reason that it fits my long-term plan. I may do this quite often, after I have more time and money. I find the idea relaxed, and a good form of self-care is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 26,
          "title": "What part of your home do you like the most",
          "q": "What part of your home do you like the most?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「喜好类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "my bedroom",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when I need some me-time",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "listen to music",
              "binge-watch TV shows",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "unwind",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "My bedroom. I am keen on this for the reason that when I need some me-time and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 27,
          "title": "What's your favorite room in your apartment or house",
          "q": "What's your favorite room in your apartment or house?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「喜好类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "the living room",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "after dinner",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "spend time with my family",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "have a good laugh",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that after dinner and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and have a good laugh.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 28,
          "title": "Do you plan to live there for a long time",
          "q": "Do you plan to live there for a long time?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 9,
          "tip": "【万年·热度#9·近3178人】喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「喜好类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "喜好：说清喜欢什么+原因；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "yes",
              "I plan to",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "as long as I live here",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "close to convenience stores",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "feel relaxed and at ease",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that as long as I live here and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and feel relaxed and at ease.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 29,
          "title": "What kind of clothes do you like to wear",
          "q": "What kind of clothes do you like to wear?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 10,
          "tip": "【新增·热度#10·近3115人】喜好：休闲舒适为主，T恤牛仔裤。 本题按「喜好类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "喜好：休闲舒适为主，T恤牛仔裤。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Casual clothes",
              "Comfortable styles",
              "Simple outfits"
            ],
            "原因或时间": [
              "t-shirt",
              "jeans",
              "sneakers"
            ],
            "频次": [
              "every day",
              "at university",
              "on weekdays"
            ],
            "感受": [
              "feel comfortable",
              "easy to match",
              "practical"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Casual clothes. I am keen on this for the reason that t-shirt and jeans matters to me. Whenever I have time, I enjoy it every day to stay positive. I find this activity comfortable, which helps me unwind, and feel comfortable.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 30,
          "title": "Do you like wearing T-shirts",
          "q": "Do you like wearing T-shirts?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 10,
          "tip": "【新增·热度#10·近3115人】喜好：爱穿T恤，理由舒服百搭。 本题按「喜好类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "喜好：爱穿T恤，理由舒服百搭。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Yes",
              "I love them",
              "Definitely",
              "all the time"
            ],
            "原因或时间": [
              "comfortable",
              "easy to wash",
              "go with everything"
            ],
            "频次": [
              "in summer",
              "almost every day",
              "at home too"
            ],
            "感受": [
              "feel relaxed",
              "my go-to choice",
              "never go wrong"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that comfortable and easy to wash matters to me. Whenever I have time, I enjoy it almost every day to stay positive. I find this activity relaxed, which helps me unwind, and feel relaxed.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 31,
          "title": "What colour clothes do you like",
          "q": "What colour clothes do you like?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 10,
          "tip": "【新增·热度#10·近3115人】喜好：颜色偏好+理由（耐脏/显气质）。 本题按「喜好类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "喜好：颜色偏好+理由（耐脏/显气质）。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Blue and white",
              "Dark colours",
              "Neutral tones"
            ],
            "原因或时间": [
              "easy to match",
              "look clean",
              "not too flashy"
            ],
            "频次": [
              "when shopping",
              "most of my wardrobe",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "feel confident",
              "practical choice",
              "personal style"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Blue and white. I am keen on this for the reason that easy to match and look clean matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity practical, which helps me unwind, and feel confident.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 32,
          "title": "Do you like to keep things tidy",
          "q": "Do you like to keep things tidy?",
          "topicEn": "Tidiness",
          "topicZh": "整洁",
          "tag": "新增",
          "recentCount": 2982,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2982人】喜好：爱整洁→桌面整齐更好学习。 本题按「喜好类」四步答；素材：整洁=study space tidy → focus better，童年对比一句即可。。",
          "logic": "喜好：爱整洁→桌面整齐更好学习。",
          "material": "整洁=study space tidy → focus better，童年对比一句即可。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "I try to",
              "Quite important to me"
            ],
            "原因或时间": [
              "study desk",
              "put things away",
              "organised space"
            ],
            "频次": [
              "every day",
              "before studying",
              "at the end of the day"
            ],
            "感受": [
              "focus better",
              "feel less stressed",
              "more productive"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that study desk and put things away matters to me. Whenever I have time, I enjoy it every day to stay positive. I find this activity practical, which helps me unwind, and focus better.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 33,
          "title": "Do you like your hometown",
          "q": "Do you like your hometown?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 12,
          "tip": "【万年·热度#12·近2912人】喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「喜好类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "I'm a big fan of it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "a foodie paradise",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "street food",
              "tasty local food",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it really hits the spot",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm a big fan of it. I am keen on this for the reason that a foodie paradise and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and it really hits the spot.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 34,
          "title": "Do you like living there",
          "q": "Do you like living there?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 12,
          "tip": "【万年·热度#12·近2912人】喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「喜好类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "yes",
              "I really enjoy living there",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "in my free time",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "go into the city centre",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "take a proper break",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that in my free time and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and take a proper break.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 35,
          "title": "What do you like (most) about your hometown",
          "q": "What do you like (most) about your hometown?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 12,
          "tip": "【万年·热度#12·近2912人】喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「喜好类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "the natural scenery",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "on sunny days",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "go for a walk in the park",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "relieve stress",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that on sunny days and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and relieve stress.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 36,
          "title": "Is there anything you dislike about it",
          "q": "Is there anything you dislike about it?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 12,
          "tip": "【万年·热度#12·近2912人】喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「喜好类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "喜好：说清喜欢什么+原因；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "The only thing I dislike is",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "the heavy traffic",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "during rush hour",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it really gets to me",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. Not really. What I dislike most is the heavy traffic during rush hour — it wears me out. Whenever I have time, I prefer quieter spots so I can stay positive and unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 37,
          "title": "Do you like singing? Why",
          "q": "Do you like singing? Why?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 13,
          "tip": "【新增·热度#13·近2135人】喜好：喜欢唱歌因为开心/解压。 本题按「喜好类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "喜好：喜欢唱歌因为开心/解压。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "Yes",
              "I love it",
              "Quite enjoy it",
              "Sometimes"
            ],
            "原因或时间": [
              "it always cheers me up",
              "with friends at KTV",
              "relieve stress"
            ],
            "频次": [
              "at weekends",
              "with friends",
              "when I'm happy"
            ],
            "感受": [
              "feel relaxed",
              "great fun",
              "express emotions"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that it always cheers me up and with friends at KTV matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity relaxed, which helps me unwind, and feel relaxed.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 38,
          "title": "Who do you want to sing for",
          "q": "Who do you want to sing for?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 13,
          "tip": "【新增·热度#13·近2135人】喜好：想为家人/朋友唱。 本题按「喜好类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "喜好：想为家人/朋友唱。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "My closest friends",
              "My family",
              "Close friends"
            ],
            "原因或时间": [
              "at gatherings",
              "birthday parties",
              "casual hangouts"
            ],
            "频次": [
              "on special days",
              "when we meet",
              "at KTV"
            ],
            "感受": [
              "share happiness",
              "create memories",
              "feel connected"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "My closest friends. I hope to focus on at gatherings and birthday parties for the reason that it fits my long-term plan. I may do this on special days, after I have more time and money. I find the idea practical, and share happiness is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 39,
          "title": "Do you like listening to others singing",
          "q": "Do you like listening to others singing?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 13,
          "tip": "【新增·热度#13·近2135人】喜好：听别人唱歌看综艺/比赛。 本题按「喜好类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "喜好：听别人唱歌看综艺/比赛。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Quite enjoy it",
              "Sometimes"
            ],
            "原因或时间": [
              "music shows",
              "friends at KTV",
              "live performances"
            ],
            "频次": [
              "on TV",
              "at parties",
              "online videos"
            ],
            "感受": [
              "inspiring",
              "relaxing",
              "appreciate their talent"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that music shows and friends at KTV matters to me. Whenever I have time, I enjoy it on TV to stay positive. I find this activity practical, which helps me unwind, and inspiring.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 40,
          "title": "Do you like science fiction movies? Why",
          "q": "Do you like science fiction movies? Why?",
          "topicEn": "Outer space and stars",
          "topicZh": "外太空与星星",
          "tag": "新增",
          "recentCount": 1988,
          "heatRank": 14,
          "tip": "【新增·热度#14·近1988人】喜好：爱科幻片因为想象力和视觉震撼。 本题按「喜好类」四步答；素材：太空题用 science fiction movies / documentaries，别装专业天文。。",
          "logic": "喜好：爱科幻片因为想象力和视觉震撼。",
          "material": "太空题用 science fiction movies / documentaries，别装专业天文。",
          "words": {
            "正面回答": [
              "Yes",
              "I'm a big fan",
              "Love them",
              "Quite enjoy them"
            ],
            "原因或时间": [
              "imagination",
              "visual effects",
              "future technology"
            ],
            "频次": [
              "in my free time",
              "with friends",
              "on weekends"
            ],
            "感受": [
              "really fun",
              "mind-blowing",
              "inspire curiosity"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that imagination and visual effects matters to me. Whenever I have time, I enjoy it in my free time to stay positive. I find this activity fun, which helps me unwind, and really fun.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 41,
          "title": "Do you want to know more about outer space",
          "q": "Do you want to know more about outer space?",
          "topicEn": "Outer space and stars",
          "topicZh": "外太空与星星",
          "tag": "新增",
          "recentCount": 1988,
          "heatRank": 14,
          "tip": "【新增·热度#14·近1988人】喜好：想了解更多宇宙知识。 本题按「喜好类」四步答；素材：太空题用 science fiction movies / documentaries，别装专业天文。。",
          "logic": "喜好：想了解更多宇宙知识。",
          "material": "太空题用 science fiction movies / documentaries，别装专业天文。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Quite curious",
              "Absolutely"
            ],
            "原因或时间": [
              "documentaries",
              "books about space",
              "online videos"
            ],
            "频次": [
              "when I have time",
              "in the future",
              "from time to time"
            ],
            "感受": [
              "universe is mysterious",
              "always learning",
              "fascinating topic"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on documentaries and books about space for the reason that it fits my long-term plan. I may do this from time to time, after I have more time and money. I find the idea practical, and universe is mysterious is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 42,
          "title": "Do you want to go into outer space in the future",
          "q": "Do you want to go into outer space in the future?",
          "topicEn": "Outer space and stars",
          "topicZh": "外太空与星星",
          "tag": "新增",
          "recentCount": 1988,
          "heatRank": 14,
          "tip": "【新增·热度#14·近1988人】喜好：想去/太遥远/看纪录片就够。 本题按「喜好类」四步答；素材：太空题用 science fiction movies / documentaries，别装专业天文。。",
          "logic": "喜好：想去/太遥远/看纪录片就够。",
          "material": "太空题用 science fiction movies / documentaries，别装专业天文。",
          "words": {
            "正面回答": [
              "Maybe in dreams",
              "Not realistically",
              "Would be amazing"
            ],
            "原因或时间": [
              "if technology allows",
              "as a tourist",
              "not for me"
            ],
            "频次": [
              "in the distant future",
              "not soon",
              "hard to say"
            ],
            "感受": [
              "sounds thrilling",
              "too risky",
              "happy to watch from Earth"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Maybe in dreams. I hope to focus on if technology allows and as a tourist for the reason that it fits my long-term plan. I may do this in the distant future, after I have more time and money. I find the idea practical, and sounds thrilling is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 43,
          "title": "Do you like this city? Why",
          "q": "Do you like this city? Why?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】喜好：说清喜欢什么+原因；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「喜好类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "喜好：说清喜欢什么+原因；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I'm passionate about it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "ever ever ever ever ever since I moved here",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "take part in extracurricular activities",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "holds a lot of memories for me",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm passionate about it. I am keen on this for the reason that ever ever ever ever ever since I moved here and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and holds a lot of memories for me.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 44,
          "title": "Would you recommend your city to others",
          "q": "Would you recommend your city to others?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 15,
          "tip": "【万年·热度#15·近1883人】喜好：说清喜欢什么+原因；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「喜好类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "喜好：说清喜欢什么+原因；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "I highly recommend it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "the food never disappoints",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I highly recommend it. I am keen on this for the reason that because and when I matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and the food never disappoints.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 45,
          "title": "Do you like science",
          "q": "Do you like science?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 16,
          "tip": "【新增·热度#16·近1834人】喜好：喜欢/一般+实验有趣。 本题按「喜好类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "喜好：喜欢/一般+实验有趣。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "Yes",
              "quite a lot",
              "Somewhat",
              "Certain topics"
            ],
            "原因或时间": [
              "interesting experiments",
              "understand the world",
              "biology"
            ],
            "频次": [
              "in school",
              "when topics are practical",
              "from time to time"
            ],
            "感受": [
              "curious mind",
              "sometimes challenging",
              "worth learning"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that interesting experiments and understand the world matters to me. Whenever I have time, I enjoy it from time to time to stay positive. I find this activity practical, which helps me unwind, and curious mind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 46,
          "title": "Which science subject is interesting to you",
          "q": "Which science subject is interesting to you?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 16,
          "tip": "【新增·热度#16·近1834人】喜好：生物/物理等+具体原因。 本题按「喜好类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "喜好：生物/物理等+具体原因。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "Biology",
              "Physics",
              "Chemistry"
            ],
            "原因或时间": [
              "human body",
              "how things work",
              "experiments"
            ],
            "频次": [
              "in high school",
              "still now",
              "most classes"
            ],
            "感受": [
              "really fun",
              "practical knowledge",
              "easier to relate"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Biology. I am keen on this for the reason that human body and how things work matters to me. Whenever I have time, I enjoy it in high school to stay positive. I find this activity fun, which helps me unwind, and really fun.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 47,
          "title": "Do you like watching science TV programs",
          "q": "Do you like watching science TV programs?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 16,
          "tip": "【新增·热度#16·近1834人】喜好：看科普节目/纪录片。 本题按「喜好类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "喜好：看科普节目/纪录片。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "Yes",
              "sometimes",
              "Quite enjoy them",
              "Occasionally"
            ],
            "原因或时间": [
              "documentaries",
              "science channels",
              "online videos"
            ],
            "频次": [
              "in my free time",
              "with my family",
              "before bed"
            ],
            "感受": [
              "learn new things",
              "relaxing and informative",
              "well made"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that documentaries and science channels matters to me. Whenever I have time, I enjoy it in my free time to stay positive. I find this activity practical, which helps me unwind, and learn new things.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 48,
          "title": "Would you like to have more free time in the future",
          "q": "Would you like to have more free time in the future?",
          "topicEn": "Spare time",
          "topicZh": "空闲时间",
          "tag": "沿用",
          "recentCount": 1834,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近1834人】喜好：希望更多空闲休息/发展爱好。 本题按「喜好类」四步答；素材：空闲时间直接套 daily leisure：watch short videos / hang out / sports。。",
          "logic": "喜好：希望更多空闲休息/发展爱好。",
          "material": "空闲时间直接套 daily leisure：watch short videos / hang out / sports。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "Would love that"
            ],
            "原因或时间": [
              "develop hobbies",
              "get proper rest",
              "travel more"
            ],
            "频次": [
              "after graduation",
              "when work is stable",
              "in the future"
            ],
            "感受": [
              "balance is important",
              "everyone needs downtime",
              "quality over quantity"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on develop hobbies and get proper rest for the reason that it fits my long-term plan. I may do this after graduation, after I have more time and money. I find the idea important, and balance is important is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 49,
          "title": "Do you like taking pictures of different views",
          "q": "Do you like taking pictures of different views?",
          "topicEn": "Views",
          "topicZh": "风景/取景",
          "tag": "沿用",
          "recentCount": 1743,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近1743人】喜好：说清喜欢什么+原因；与 scenery 共用 take photos of views，城乡对比即可。 本题按「喜好类」四步答；素材：与 scenery 共用 take photos of views，城乡对比即可。。",
          "logic": "喜好：说清喜欢什么+原因；与 scenery 共用 take photos of views，城乡对比即可。",
          "material": "与 scenery 共用 take photos of views，城乡对比即可。",
          "words": {
            "正面回答": [
              "I'm crazy about it",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when travelling",
              "on vacation",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "cityscapes and nature",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "relieve stress",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm crazy about it. I am keen on this for the reason that when travelling and on vacation matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and relieve stress.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 50,
          "title": "What is your favourite food",
          "q": "What is your favourite food?",
          "topicEn": "Food",
          "topicZh": "食物",
          "tag": "沿用",
          "recentCount": 1680,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1680人】喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。 本题按「喜好类」四步答；素材：食物=favourite dish + street food/takeout，童年口味变化一句。。",
          "logic": "喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。",
          "material": "食物=favourite dish + street food/takeout，童年口味变化一句。",
          "words": {
            "正面回答": [
              "I am a big fan of",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "delicious",
              "mouth-watering desserts",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "order takeout",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it really hits the spot",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I am a big fan of. I am keen on this for the reason that delicious and mouth-watering desserts matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and it really hits the spot.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 51,
          "title": "What kind of food did you like when you were young",
          "q": "What kind of food did you like when you were young?",
          "topicEn": "Food",
          "topicZh": "食物",
          "tag": "沿用",
          "recentCount": 1680,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1680人】喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。 本题按「喜好类」四步答；素材：食物=favourite dish + street food/takeout，童年口味变化一句。。",
          "logic": "喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。",
          "material": "食物=favourite dish + street food/takeout，童年口味变化一句。",
          "words": {
            "正面回答": [
              "I had a sweet tooth",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "childhood",
              "before primary school",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "have cake for breakfast",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it always cheers me up",
              "have a great time",
              "feel relaxed",
              "really enjoyable"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I had a sweet tooth. I am keen on this for the reason that childhood and before primary school matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and it always cheers me up.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 52,
          "title": "Has your favourite food changed since you were a child",
          "q": "Has your favourite food changed since you were a child?",
          "topicEn": "Food",
          "topicZh": "食物",
          "tag": "沿用",
          "recentCount": 1680,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1680人】喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。 本题按「喜好类」四步答；素材：食物=favourite dish + street food/takeout，童年口味变化一句。。",
          "logic": "喜好：说清喜欢什么+原因；食物=favourite dish + street food/takeout，童年口味变化一句。",
          "material": "食物=favourite dish + street food/takeout，童年口味变化一句。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely changed",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "to stay healthy",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "buy fresh groceries",
              "fresh ingredients",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "good for both body and mind",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that to stay healthy and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and good for both body and mind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 53,
          "title": "Do you like to watch comedies",
          "q": "Do you like to watch comedies?",
          "topicEn": "Jokes & Comedies",
          "topicZh": "笑话与喜剧",
          "tag": "新增",
          "recentCount": 1680,
          "heatRank": 20,
          "tip": "【新增·热度#20·近1680人】喜好：爱看喜剧电影/综艺解压。 本题按「喜好类」四步答；素材：笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。。",
          "logic": "喜好：爱看喜剧电影/综艺解压。",
          "material": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Love comedies",
              "Quite often"
            ],
            "原因或时间": [
              "watch comedies",
              "funny TV shows",
              "stand-up clips"
            ],
            "频次": [
              "at weekends",
              "after a long day",
              "with friends"
            ],
            "感受": [
              "have a good laugh",
              "relieve stress",
              "feel lighter"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that watch comedies and funny TV shows matters to me. Whenever I have time, I enjoy it at weekends to stay positive. I find this activity practical, which helps me unwind, and have a good laugh.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 54,
          "title": "Is there a building that you would like to visit",
          "q": "Is there a building that you would like to visit?",
          "topicEn": "Building",
          "topicZh": "建筑",
          "tag": "沿用",
          "recentCount": 1400,
          "heatRank": 21,
          "tip": "【沿用·热度#21·近1400人】喜好：说清喜欢什么+原因；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。 本题按「喜好类」四步答；素材：建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。。",
          "logic": "喜好：说清喜欢什么+原因；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "material": "建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "words": {
            "正面回答": [
              "yes",
              "there is one",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "its its its its its unique design",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "cafes",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "meet like-minded people",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that its its its its its unique design and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and meet like-minded people.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 55,
          "title": "Do you want to live in a tall building",
          "q": "Do you want to live in a tall building?",
          "topicEn": "Building",
          "topicZh": "建筑",
          "tag": "沿用",
          "recentCount": 1400,
          "heatRank": 21,
          "tip": "【沿用·热度#21·近1400人】喜好：想住高楼视野好/或担心电梯不方便。 本题按「喜好类」四步答；素材：建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。。",
          "logic": "喜好：想住高楼视野好/或担心电梯不方便。",
          "material": "建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "words": {
            "正面回答": [
              "Maybe",
              "Not really",
              "it depends on the person"
            ],
            "原因或时间": [
              "good views",
              "modern facilities",
              "near the city centre"
            ],
            "频次": [
              "in the future",
              "when I work",
              "not now"
            ],
            "感受": [
              "sounds convenient",
              "worry about elevators",
              "prefer lower floors"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Maybe. I hope to focus on good views and modern facilities for the reason that it fits my long-term plan. I may do this in the future, after I have more time and money. I find the idea convenient, and sounds convenient is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 56,
          "title": "What's your favourite animal? Why",
          "q": "What's your favourite animal? Why?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 22,
          "tip": "【沿用·热度#22·近1330人】喜好：说清喜欢什么+原因；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。 本题按「喜好类」四步答；素材：宠物=puppy at home。",
          "logic": "喜好：说清喜欢什么+原因；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "I'm a dog person",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "they are incredibly loyal",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "keep me company at home",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "a great way to unwind",
              "unwind",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm a dog person. I am keen on this for the reason that they are incredibly loyal and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and a great way to unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 57,
          "title": "Do you like getting up early in the morning",
          "q": "Do you like getting up early in the morning?",
          "topicEn": "Morning time",
          "topicZh": "早晨",
          "tag": "沿用",
          "recentCount": 1085,
          "heatRank": 23,
          "tip": "【沿用·热度#23·近1085人】喜好：说清喜欢什么+原因；早晨=get up → breakfast → get dressed，童年对比更晚起。 本题按「喜好类」四步答；素材：早晨=get up → breakfast → get dressed，童年对比更晚起。。",
          "logic": "喜好：说清喜欢什么+原因；早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "material": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "words": {
            "正面回答": [
              "Honestly",
              "yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "the first thing I do after getting up",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "go jogging",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "energetic",
              "full of energy",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that the first thing I do after getting up and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity energetic, which helps me unwind, and energetic.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 58,
          "title": "Do you like watching team games? Why",
          "q": "Do you like watching team games? Why?",
          "topicEn": "Sports team",
          "topicZh": "运动队",
          "tag": "沿用",
          "recentCount": 1022,
          "heatRank": 24,
          "tip": "【沿用·热度#24·近1022人】喜好：说清喜欢什么+原因；运动队=basketball/volleyball + teamwork，观看与参与同一套。 本题按「喜好类」四步答；素材：运动队=basketball/volleyball + teamwork，观看与参与同一套。。",
          "logic": "喜好：说清喜欢什么+原因；运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "material": "运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "words": {
            "正面回答": [
              "I'm really into them",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "in my free time",
              "when I have some free time",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "watch basketball games games games games games",
              "volleyball games",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "clear my mind",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm really into them. I am keen on this for the reason that in my free time and when I have some free time matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and clear my mind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 59,
          "title": "What are your favourite activities",
          "q": "What are your favourite activities?",
          "topicEn": "Childhood activities",
          "topicZh": "童年活动",
          "tag": "沿用",
          "recentCount": 994,
          "heatRank": 25,
          "tip": "【沿用·热度#25·近994人】喜好：现在最爱运动/听歌/阅读等。 本题按「喜好类」四步答；素材：童年活动=play outside / with friends，现在对比更 indoor。。",
          "logic": "喜好：现在最爱运动/听歌/阅读等。",
          "material": "童年活动=play outside / with friends，现在对比更 indoor。",
          "words": {
            "正面回答": [
              "Several favourites",
              "A few main ones",
              "Quite a few"
            ],
            "原因或时间": [
              "listen to music",
              "do some sports",
              "read"
            ],
            "频次": [
              "in my free time",
              "at weekends",
              "almost every day"
            ],
            "感受": [
              "keep me happy",
              "relieve stress",
              "good balance"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Several favourites. I am keen on this for the reason that listen to music and do some sports matters to me. Whenever I have time, I enjoy it in my free time to stay positive. I find this activity practical, which helps me unwind, and keep me happy.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 60,
          "title": "What were your favourite activities when you were a child",
          "q": "What were your favourite activities when you were a child?",
          "topicEn": "Childhood activities",
          "topicZh": "童年活动",
          "tag": "沿用",
          "recentCount": 994,
          "heatRank": 25,
          "tip": "【沿用·热度#25·近994人】喜好：说清喜欢什么+原因；童年活动=play outside / with friends，现在对比更 indoor。 本题按「喜好类」四步答；素材：童年活动=play outside / with friends，现在对比更 indoor。。",
          "logic": "喜好：说清喜欢什么+原因；童年活动=play outside / with friends，现在对比更 indoor。",
          "material": "童年活动=play outside / with friends，现在对比更 indoor。",
          "words": {
            "正面回答": [
              "One of my favourite things to do as a child was",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "outside of class",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "hang out with friends",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "have a good laugh",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. When I was a child, I enjoyed outside of class and because, which created warm memories. Back then I did this quite often, and I still remember how simple it felt. I find those days relaxed, which is why have a good laugh.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 61,
          "title": "Do you enjoy being the age you are now",
          "q": "Do you enjoy being the age you are now?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 26,
          "tip": "【沿用·热度#26·近959人】喜好：享受当下青春/压力也有。 本题按「喜好类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "喜好：享受当下青春/压力也有。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "Yes",
              "mostly",
              "Quite enjoy it",
              "It's okay"
            ],
            "原因或时间": [
              "freedom at university",
              "learn and grow",
              "meet new people"
            ],
            "频次": [
              "at this stage of my life of my life of my life of my life",
              "right now",
              "these years"
            ],
            "感受": [
              "full of opportunities",
              "some pressure too",
              "grateful for now"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that freedom at university and learn and grow matters to me. Whenever I have time, I enjoy it these years to stay positive. I find this activity practical, which helps me unwind, and full of opportunities.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 62,
          "title": "Do you like reading",
          "q": "Do you like reading?",
          "topicEn": "Reading",
          "topicZh": "阅读",
          "tag": "沿用",
          "recentCount": 875,
          "heatRank": 27,
          "tip": "【沿用·热度#27·近875人】喜好：说清喜欢什么+原因；阅读=read books / flip through pages，纸质 vs 屏幕对比。 本题按「喜好类」四步答；素材：阅读=read books / flip through pages，纸质 vs 屏幕对比。。",
          "logic": "喜好：说清喜欢什么+原因；阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "material": "阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "words": {
            "正面回答": [
              "I'm passionate about reading",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when I feel bored",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "read at the library",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "unwind",
              "feel at peace",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I'm passionate about reading. I am keen on this for the reason that when I feel bored and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 63,
          "title": "Where would you like to take a long walk if you had the chance",
          "q": "Where would you like to take a long walk if you had the chance?",
          "topicEn": "Walking",
          "topicZh": "走路",
          "tag": "沿用",
          "recentCount": 854,
          "heatRank": 28,
          "tip": "【沿用·热度#28·近854人】喜好：说清喜欢什么+原因；走路=go for a walk in the park，解压+景色一笔带过。 本题按「喜好类」四步答；素材：走路=go for a walk in the park，解压+景色一笔带过。。",
          "logic": "喜好：说清喜欢什么+原因；走路=go for a walk in the park，解压+景色一笔带过。",
          "material": "走路=go for a walk in the park，解压+景色一笔带过。",
          "words": {
            "正面回答": [
              "the local park",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "when the weather is nice",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "go for a walk",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "feel relaxed and at ease",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型5 plan to / hope to",
              "pattern": "I plan / hope to ______ in the future.",
              "tip": "第2步：将来计划用 plan to / hope to"
            },
            "2": {
              "name": "After I graduate / In a few years",
              "pattern": "After I graduate / In a few years, I ______.",
              "tip": "第3步：时间线落到毕业后或几年后"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I hope to focus on when the weather is nice and because for the reason that it fits my long-term plan. I may do this quite often, after I have more time and money. I find the idea relaxed, and feel relaxed and at ease is how I feel about it now.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 64,
          "title": "Do you like to take scenery pictures",
          "q": "Do you like to take scenery pictures?",
          "topicEn": "Scenery",
          "topicZh": "景色",
          "tag": "沿用",
          "recentCount": 777,
          "heatRank": 29,
          "tip": "【沿用·热度#29·近777人】喜好：说清喜欢什么+原因；景色=travel + take photos，山/海对比用 mountains vs sea。 本题按「喜好类」四步答；素材：景色=travel + take photos，山/海对比用 mountains vs sea。。",
          "logic": "喜好：说清喜欢什么+原因；景色=travel + take photos，山/海对比用 mountains vs sea。",
          "material": "景色=travel + take photos，山/海对比用 mountains vs sea。",
          "words": {
            "正面回答": [
              "Definitely",
              "Yes",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "capture moments of my life",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "take photos outdoors",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "It",
              "s something I",
              "ll never forget"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that capture moments of my life and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity practical, which helps me unwind, and It.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 65,
          "title": "Do you like crowded places",
          "q": "Do you like crowded places?",
          "topicEn": "Crowded place",
          "topicZh": "拥挤的地方",
          "tag": "沿用",
          "recentCount": 728,
          "heatRank": 30,
          "tip": "【沿用·热度#30·近728人】喜好：说清喜欢什么+原因；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。 本题按「喜好类」四步答；素材：拥挤=city centre / rush hour / shopping malls，喜好偏 not really。。",
          "logic": "喜好：说清喜欢什么+原因；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "material": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "words": {
            "正面回答": [
              "to be honest",
              "no",
              "Yes",
              "Definitely",
              "I love it"
            ],
            "原因或时间": [
              "especially during rush hour",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "take the subway",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "it really gets to me",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that especially during rush hour and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and it really gets to me.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 66,
          "title": "Do you have any hobbies",
          "q": "Do you have any hobbies?",
          "topicEn": "Hobby",
          "topicZh": "爱好",
          "tag": "沿用",
          "recentCount": 651,
          "heatRank": 31,
          "tip": "【沿用·热度#31·近651人】喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。 本题按「喜好类」四步答；素材：爱好直接指向 listen to music / sports / reading 中已背的一项。。",
          "logic": "喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "material": "爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "words": {
            "正面回答": [
              "I have quite a few",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "at weekends",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "binge-watch TV shows",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "sit back and relax",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "I have quite a few. I am keen on this for the reason that at weekends and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and sit back and relax.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 67,
          "title": "Did you have any hobbies when you were a child",
          "q": "Did you have any hobbies when you were a child?",
          "topicEn": "Hobby",
          "topicZh": "爱好",
          "tag": "沿用",
          "recentCount": 651,
          "heatRank": 31,
          "tip": "【沿用·热度#31·近651人】喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。 本题按「喜好类」四步答；素材：爱好直接指向 listen to music / sports / reading 中已背的一项。。",
          "logic": "喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "material": "爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "words": {
            "正面回答": [
              "Absolutely",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "before primary school",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "play video games",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "great fun",
              "have a great time",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. When I was a child, I enjoyed before primary school and because, which created warm memories. Back then I did this quite often, and I still remember how simple it felt. I find those days fun, which is why great fun.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 68,
          "title": "Do you have a hobby that you’ve had since childhood",
          "q": "Do you have a hobby that you’ve had since childhood?",
          "topicEn": "Hobby",
          "topicZh": "爱好",
          "tag": "沿用",
          "recentCount": 651,
          "heatRank": 31,
          "tip": "【沿用·热度#31·近651人】喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。 本题按「喜好类」四步答；素材：爱好直接指向 listen to music / sports / reading 中已背的一项。。",
          "logic": "喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "material": "爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "words": {
            "正面回答": [
              "Exactly",
              "Yes",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "before bed",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "flip through physical books",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "reflect on things",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. When I was a child, I enjoyed before bed and because, which created warm memories. Back then I did this quite often, and I still remember how simple it felt. I find those days relaxed, which is why reflect on things.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 69,
          "title": "Do you have the same hobbies as your family members",
          "q": "Do you have the same hobbies as your family members?",
          "topicEn": "Hobby",
          "topicZh": "爱好",
          "tag": "沿用",
          "recentCount": 651,
          "heatRank": 31,
          "tip": "【沿用·热度#31·近651人】喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。 本题按「喜好类」四步答；素材：爱好直接指向 listen to music / sports / reading 中已背的一项。。",
          "logic": "喜好：说清喜欢什么+原因；爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "material": "爱好直接指向 listen to music / sports / reading 中已背的一项。",
          "words": {
            "正面回答": [
              "Yes",
              "we share some",
              "Definitely",
              "I love it",
              "Not really"
            ],
            "原因或时间": [
              "during the holidays",
              "because",
              "when I",
              "for the reason that"
            ],
            "频次": [
              "eat out together",
              "quite often",
              "at weekends",
              "from time to time"
            ],
            "感受": [
              "open up to each other",
              "feel relaxed",
              "really enjoyable",
              "it always cheers me up"
            ]
          },
          "frames": {
            "1": {
              "name": "句型6 Whenever / 句型3 for the reason that",
              "pattern": "Whenever I ______, I ______. / I am keen on ______ for the reason that ______.",
              "tip": "第2步：有时间用 Whenever；讲原因用 for the reason that / since"
            },
            "2": {
              "name": "句型5 to do 目的状语",
              "pattern": "I am crazy about ______ to ______.",
              "tip": "第3步：行为举例时用 to do 交代目的（去哪/做什么）"
            },
            "3": {
              "name": "句型2 + 句型4 I find..., which",
              "pattern": "I find this activity ______, which ______.",
              "tip": "第4步：宾补写感受，再用 which 补放松/收获"
            }
          },
          "sample": "Yes, definitely. I am keen on this for the reason that during the holidays and because matters to me. Whenever I have time, I enjoy it quite often to stay positive. I find this activity relaxed, which helps me unwind, and open up to each other.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        }
      ]
    },
    {
      "id": "xingwei",
      "name": "行为习惯类",
      "steps": [
        "正面回答",
        "原因",
        "时间线+行为描述",
        "影响"
      ],
      "questions": [
        {
          "id": 1,
          "title": "Do you wear a watch",
          "q": "Do you wear a watch?",
          "topicEn": "Watch",
          "topicZh": "手表",
          "tag": "新增",
          "recentCount": 39172,
          "heatRank": 1,
          "tip": "【新增·热度#1·近39172人】习惯：每天戴手表看时间，尤其上课/出门。 本题按「行为习惯类」四步答；素材：物品·手表（实用计时）。",
          "logic": "习惯：每天戴手表看时间，尤其上课/出门。",
          "material": "物品·手表（实用计时）",
          "words": {
            "正面回答": [
              "Yes",
              "almost every day",
              "Definitely",
              "Usually"
            ],
            "原因": [
              "check the time",
              "stay punctual",
              "before heading out"
            ],
            "时间线+行为描述": [
              "during class",
              "when I head out",
              "every morning"
            ],
            "影响": [
              "helps me stay organised",
              "really convenient",
              "saves time"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, almost every day. Since I need to stay punctual, I check the time before heading out. It is convenient for me to wear it during class every morning. Wearing a watch can be seen as a habit that helps me stay organised.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 2,
          "title": "What do you usually do when there is a traffic jam",
          "q": "What do you usually do when there is a traffic jam?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 2,
          "tip": "【新增·热度#2·近12327人】习惯：堵车时听歌/刷短视频/耐心等。 本题按「行为习惯类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "习惯：堵车时听歌/刷短视频/耐心等。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "I stay calm",
              "I listen to music",
              "Usually patient"
            ],
            "原因": [
              "listen to music",
              "watch short videos",
              "chat with friends"
            ],
            "时间线+行为描述": [
              "during rush hour",
              "on the highway",
              "in the city"
            ],
            "影响": [
              "helps me pass the time",
              "relieve stress",
              "stay relaxed"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型6 While waiting / During rush hour",
              "pattern": "While waiting / During rush hour, I ______.",
              "tip": "第3步：堵车场景用 While waiting 描述当下行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "I usually stay calm. Since I do not want to get stressed, I listen to music or watch short videos. While waiting during rush hour, it is common for me to chat with friends. This can be seen as a way to relieve stress and pass the time.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 3,
          "title": "How much time do you spend on your studies each week",
          "q": "How much time do you spend on your studies each week?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「行为习惯类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "I spend a lot of time",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "work hard at my studies",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "the classroom",
              "finish homework on my own",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "What makes me happy is the moment when",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "I spend a lot of time. Since work hard at my studies and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me What makes me happy is the moment when, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 4,
          "title": "What technology do you use when you study",
          "q": "What technology do you use when you study?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「行为习惯类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "iPad",
              "mainly my laptop and iPad",
              "Yes",
              "Usually",
              "Definitely"
            ],
            "原因": [
              "it's just my personal habit",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "attend classes",
              "listen to a lecture",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "practical",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since it's just my personal habit and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me practical, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 5,
          "title": "What technology do you use at work",
          "q": "What technology do you use at work?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「行为习惯类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "习惯：描述日常频率和场景；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "iPad",
              "mainly my laptop and iPad",
              "Yes",
              "Usually",
              "Definitely"
            ],
            "原因": [
              "it's just my personal habit",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "attend classes",
              "listen to a lecture",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "practical",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since it's just my personal habit and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me practical, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 6,
          "title": "What kinds of websites do you often visit",
          "q": "What kinds of websites do you often visit?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 4,
          "tip": "【新增·热度#4·近8064人】习惯：学习+社交+购物网站。 本题按「行为习惯类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "习惯：学习+社交+购物网站。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Several types",
              "Quite a few",
              "Many kinds"
            ],
            "原因": [
              "study resources",
              "social media",
              "shopping sites"
            ],
            "时间线+行为描述": [
              "every day",
              "throughout the day",
              "whenever online"
            ],
            "影响": [
              "save me a lot of time",
              "really convenient",
              "keep me updated"
            ]
          },
          "frames": {
            "1": {
              "name": "句型2 I prefer / am keen on",
              "pattern": "I prefer / am keen on ______ because ______.",
              "tip": "第2步：类型题用 prefer / keen on + 简短原因"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Several types. Since study resources and social media matters in my routine, I keep the habit consistently. It is common for me to do this every day, so it has become automatic. This can be regarded as a habit that save me a lot of time, and it also helps me really convenient.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 7,
          "title": "How often do you go shopping",
          "q": "How often do you go shopping?",
          "topicEn": "Shopping",
          "topicZh": "购物",
          "tag": "新增",
          "recentCount": 4312,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4312人】习惯：网购频繁/偶尔逛商场。 本题按「行为习惯类」四步答；素材：购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。。",
          "logic": "习惯：网购频繁/偶尔逛商场。",
          "material": "购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。",
          "words": {
            "正面回答": [
              "Quite often",
              "from time to time",
              "Almost every week"
            ],
            "原因": [
              "shop online",
              "shopping malls",
              "buy clothes"
            ],
            "时间线+行为描述": [
              "at weekends",
              "when I need something",
              "every few weeks"
            ],
            "影响": [
              "really convenient",
              "save time",
              "enjoy browsing sometimes"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Quite often. Since shop online and shopping malls matters in my routine, I keep the habit consistently. It is common for me to do this at weekends, so it has become automatic. This can be regarded as a habit that helps me really convenient, and it also save time.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 8,
          "title": "Do you usually take a mirror with you",
          "q": "Do you usually take a mirror with you?",
          "topicEn": "Mirrors",
          "topicZh": "镜子",
          "tag": "新增",
          "recentCount": 4116,
          "heatRank": 6,
          "tip": "【新增·热度#6·近4116人】习惯：包里小镜子/用手机代替。 本题按「行为习惯类」四步答；素材：镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。。",
          "logic": "习惯：包里小镜子/用手机代替。",
          "material": "镜子挂在 get dressed / look at myself in the mirror 日常链，少谈装饰美学。",
          "words": {
            "正面回答": [
              "Not usually",
              "Sometimes",
              "Rarely"
            ],
            "原因": [
              "use my phone",
              "small pocket mirror",
              "only for travel"
            ],
            "时间线+行为描述": [
              "when travelling",
              "at formal events",
              "almost never"
            ],
            "影响": [
              "phone is enough",
              "not necessary",
              "convenient either way"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Not usually. Since use my phone and small pocket mirror matters in my routine, I keep the habit consistently. It is common for me to do this when travelling, so it has become automatic. This can be regarded as a habit that helps me phone is enough, and it also helps me not necessary.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 9,
          "title": "Do you listen to music while doing other things",
          "q": "Do you listen to music while doing other things?",
          "topicEn": "Music",
          "topicZh": "音乐",
          "tag": "新增",
          "recentCount": 3997,
          "heatRank": 7,
          "tip": "【新增·热度#7·近3997人】习惯：学习/运动时听歌。 本题按「行为习惯类」四步答；素材：音乐=listen to music 解压。",
          "logic": "习惯：学习/运动时听歌。",
          "material": "音乐=listen to music 解压",
          "words": {
            "正面回答": [
              "Yes",
              "often",
              "almost always",
              "Quite often"
            ],
            "原因": [
              "while studying",
              "on the subway",
              "during workouts"
            ],
            "时间线+行为描述": [
              "every day",
              "when I commute",
              "in my free time"
            ],
            "影响": [
              "helps me focus",
              "relieve stress",
              "makes tasks easier"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since while studying and on the subway matters in my routine, I keep the habit consistently. It is common for me to do this every day, so it has become automatic. This can be regarded as a habit that helps me focus, and it also relieve stress.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 10,
          "title": "What room does your family spend most of the time in",
          "q": "What room does your family spend most of the time in?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 8,
          "tip": "【万年·热度#8·近3178人】习惯：描述日常频率和场景；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「行为习惯类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "习惯：描述日常频率和场景；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "definitely the living room",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "share stories",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "dinner",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "precious memories",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since share stories and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me precious memories, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 11,
          "title": "What do you usually do in your apartment",
          "q": "What do you usually do in your apartment?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 8,
          "tip": "【万年·热度#8·近3178人】习惯：描述日常频率和场景；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「行为习惯类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "习惯：描述日常频率和场景；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "I usually stay at home",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "have some me-time",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "my rented apartment",
              "flip through physical books",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "slow down",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + to do",
              "pattern": "It is ______ for me to ______ when ______.",
              "tip": "第3步：What do you do 题用形式主语描述具体行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "I usually stay at home. For the reason that I need a clear routine, I focus on have some me-time and since. It is normal for me to do this every morning, especially when my schedule is busy. This habit can be seen as something that helps me slow down, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 12,
          "title": "Do you spend a lot of time choosing clothes",
          "q": "Do you spend a lot of time choosing clothes?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 9,
          "tip": "【新增·热度#9·近3115人】习惯：出门前选衣时间长短。 本题按「行为习惯类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "习惯：出门前选衣时间长短。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Not really",
              "Sometimes",
              "A few minutes"
            ],
            "原因": [
              "grab my things and head out",
              "pick quickly",
              "same style daily"
            ],
            "时间线+行为描述": [
              "every morning",
              "before class",
              "on weekdays"
            ],
            "影响": [
              "prefer simplicity",
              "save time",
              "not fussy about fashion"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Not really. Since grab my things and head out and pick quickly matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me prefer simplicity, and it also save time.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 13,
          "title": "Did you keep your room tidy as a child",
          "q": "Did you keep your room tidy as a child?",
          "topicEn": "Tidiness",
          "topicZh": "整洁",
          "tag": "新增",
          "recentCount": 2982,
          "heatRank": 10,
          "tip": "【新增·热度#10·近2982人】习惯：童年房间整不整齐+父母督促。 本题按「行为习惯类」四步答；素材：整洁=study space tidy → focus better，童年对比一句即可。。",
          "logic": "习惯：童年房间整不整齐+父母督促。",
          "material": "整洁=study space tidy → focus better，童年对比一句即可。",
          "words": {
            "正面回答": [
              "Not really",
              "My parents helped",
              "Sometimes"
            ],
            "原因": [
              "messy desk",
              "toys everywhere",
              "needed reminders"
            ],
            "时间线+行为描述": [
              "when I was young",
              "before exams",
              "on weekends"
            ],
            "影响": [
              "learned over time",
              "childhood habit",
              "got better later"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Not really. Since messy desk and toys everywhere matters in my routine, I keep the habit consistently. It is common for me to do this before exams, so it has become automatic. This can be regarded as a habit that helps me learned over time, and it also helps me childhood habit.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 14,
          "title": "How do you keep your work or study space tidy",
          "q": "How do you keep your work or study space tidy?",
          "topicEn": "Tidiness",
          "topicZh": "整洁",
          "tag": "新增",
          "recentCount": 2982,
          "heatRank": 10,
          "tip": "【新增·热度#10·近2982人】习惯：每天收拾桌面/分类收纳。 本题按「行为习惯类」四步答；素材：整洁=study space tidy → focus better，童年对比一句即可。。",
          "logic": "习惯：每天收拾桌面/分类收纳。",
          "material": "整洁=study space tidy → focus better，童年对比一句即可。",
          "words": {
            "正面回答": [
              "I tidy up daily",
              "Put things away",
              "A quick clean"
            ],
            "原因": [
              "sort my notes",
              "clear the desk",
              "throw out rubbish"
            ],
            "时间线+行为描述": [
              "after studying",
              "every evening",
              "before I start work"
            ],
            "影响": [
              "focus better",
              "feel more organised",
              "saves time later"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I tidy up daily. Since sort my notes and clear the desk matters in my routine, I keep the habit consistently. It is common for me to do this after studying, so it has become automatic. This can be regarded as a habit that helps me focus better, and it also helps me feel more organised.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 15,
          "title": "Do you use headphones",
          "q": "Do you use headphones?",
          "topicEn": "Headphones",
          "topicZh": "耳机",
          "tag": "新增",
          "recentCount": 2597,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2597人】习惯：经常用耳机听歌/听课。 本题按「行为习惯类」四步答；素材：耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。。",
          "logic": "习惯：经常用耳机听歌/听课。",
          "material": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
          "words": {
            "正面回答": [
              "Yes",
              "almost every day",
              "Quite often",
              "Definitely"
            ],
            "原因": [
              "listen to music",
              "online lectures",
              "on the subway"
            ],
            "时间线+行为描述": [
              "when commuting",
              "at the library",
              "every day"
            ],
            "影响": [
              "block background noise",
              "helps me focus",
              "private listening"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since listen to music and online lectures matters in my routine, I keep the habit consistently. It is common for me to do this every day, so it has become automatic. This can be regarded as a habit that helps me block background noise, and it also helps me focus.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 16,
          "title": "When would you use headphones",
          "q": "When would you use headphones?",
          "topicEn": "Headphones",
          "topicZh": "耳机",
          "tag": "新增",
          "recentCount": 2597,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2597人】习惯：通勤/图书馆/运动时戴耳机。 本题按「行为习惯类」四步答；素材：耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。。",
          "logic": "习惯：通勤/图书馆/运动时戴耳机。",
          "material": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
          "words": {
            "正面回答": [
              "When commuting",
              "While studying",
              "Several situations"
            ],
            "原因": [
              "on the subway",
              "at the library",
              "during workouts"
            ],
            "时间线+行为描述": [
              "every morning",
              "before exams",
              "at the gym"
            ],
            "影响": [
              "block noise",
              "stay focused",
              "enjoy music privately"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Several situations. Since on the subway and at the library matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me block noise, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 17,
          "title": "In what conditions would you not use headphones",
          "q": "In what conditions would you not use headphones?",
          "topicEn": "Headphones",
          "topicZh": "耳机",
          "tag": "新增",
          "recentCount": 2597,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2597人】习惯：上课/与人交流时不戴。 本题按「行为习惯类」四步答；素材：耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。。",
          "logic": "习惯：上课/与人交流时不戴。",
          "material": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
          "words": {
            "正面回答": [
              "In class",
              "When chatting",
              "At gatherings"
            ],
            "原因": [
              "need to hear others",
              "safety on the street",
              "face-to-face talks"
            ],
            "时间线+行为描述": [
              "during meetings",
              "with family",
              "when walking at night"
            ],
            "影响": [
              "stay aware",
              "be polite",
              "safety first"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "In class. Since need to hear others and safety on the street matters in my routine, I keep the habit consistently. It is common for me to do this during meetings, so it has become automatic. This can be regarded as a habit that helps me stay aware, and it also helps me be polite.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 18,
          "title": "Do you often see your neighbors",
          "q": "Do you often see your neighbors?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 12,
          "tip": "【万年·热度#12·近1883人】习惯：描述日常频率和场景；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「行为习惯类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "习惯：描述日常频率和场景；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "yes",
              "quite often",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "a residential area",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "head out",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "have a good chat",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since a residential area and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me have a good chat, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 19,
          "title": "Do you often have free time",
          "q": "Do you often have free time?",
          "topicEn": "Spare time",
          "topicZh": "空闲时间",
          "tag": "沿用",
          "recentCount": 1834,
          "heatRank": 13,
          "tip": "【沿用·热度#13·近1834人】习惯：空闲时间多不多+学业忙。 本题按「行为习惯类」四步答；素材：空闲时间直接套 daily leisure：watch short videos / hang out / sports。。",
          "logic": "习惯：空闲时间多不多+学业忙。",
          "material": "空闲时间直接套 daily leisure：watch short videos / hang out / sports。",
          "words": {
            "正面回答": [
              "Not much lately",
              "Some evenings",
              "At weekends"
            ],
            "原因": [
              "busy with studies",
              "packed schedule",
              "after assignments"
            ],
            "时间线+行为描述": [
              "at weekends",
              "before exams",
              "rarely on weekdays"
            ],
            "影响": [
              "wish I had more",
              "use it wisely",
              "still manage to relax"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Not much lately. Since busy with studies and packed schedule matters in my routine, I keep the habit consistently. It is common for me to do this at weekends, so it has become automatic. This can be regarded as a habit that helps me wish I had more, and it also helps me use it wisely.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 20,
          "title": "What do you usually do in your spare time",
          "q": "What do you usually do in your spare time?",
          "topicEn": "Spare time",
          "topicZh": "空闲时间",
          "tag": "沿用",
          "recentCount": 1834,
          "heatRank": 13,
          "tip": "【沿用·热度#13·近1834人】习惯：刷视频/运动/和朋友聚会。 本题按「行为习惯类」四步答；素材：空闲时间直接套 daily leisure：watch short videos / hang out / sports。。",
          "logic": "习惯：刷视频/运动/和朋友聚会。",
          "material": "空闲时间直接套 daily leisure：watch short videos / hang out / sports。",
          "words": {
            "正面回答": [
              "Several things",
              "A few favourites",
              "Depends on mood"
            ],
            "原因": [
              "watch short videos",
              "hang out",
              "do some sports"
            ],
            "时间线+行为描述": [
              "at weekends",
              "in my free time",
              "after dinner"
            ],
            "影响": [
              "relieve stress",
              "helps me unwind",
              "recharge my energy"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + to do",
              "pattern": "It is ______ for me to ______ when ______.",
              "tip": "第3步：What do you do 题用形式主语描述具体行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Several things. For the reason that I need a clear routine, I focus on watch short videos and hang out. It is normal for me to do this at weekends, especially when my schedule is busy. This habit can be seen as something that relieve stress, and it also helps me unwind.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 21,
          "title": "Do you eat different foods at different times of the year",
          "q": "Do you eat different foods at different times of the year?",
          "topicEn": "Food",
          "topicZh": "食物",
          "tag": "沿用",
          "recentCount": 1680,
          "heatRank": 14,
          "tip": "【沿用·热度#14·近1680人】习惯：描述日常频率和场景；食物=favourite dish + street food/takeout，童年口味变化一句。 本题按「行为习惯类」四步答；素材：食物=favourite dish + street food/takeout，童年口味变化一句。。",
          "logic": "习惯：描述日常频率和场景；食物=favourite dish + street food/takeout，童年口味变化一句。",
          "material": "食物=favourite dish + street food/takeout，童年口味变化一句。",
          "words": {
            "正面回答": [
              "Absolutely yes",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "groceries",
              "fresh ingredients",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "get together",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "good for both body and mind",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since groceries and fresh ingredients matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me good for both body and mind, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 22,
          "title": "Do you take photos of buildings",
          "q": "Do you take photos of buildings?",
          "topicEn": "Building",
          "topicZh": "建筑",
          "tag": "沿用",
          "recentCount": 1400,
          "heatRank": 15,
          "tip": "【沿用·热度#15·近1400人】习惯：描述日常频率和场景；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。 本题按「行为习惯类」四步答；素材：建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。。",
          "logic": "习惯：描述日常频率和场景；建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "material": "建筑=near home tall buildings / take photos，参观欲落到 city centre landmarks。",
          "words": {
            "正面回答": [
              "I often take photos",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "be passionate about things",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "the city centre",
              "take photos",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "reflect on things",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "I often take photos. Since be passionate about things and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me reflect on things, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 23,
          "title": "How often do you visit a zoo",
          "q": "How often do you visit a zoo?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近1330人】习惯：偶尔去动物园，假期带孩子或朋友。 本题按「行为习惯类」四步答；素材：宠物=puppy at home。",
          "logic": "习惯：偶尔去动物园，假期带孩子或朋友。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "Not very often",
              "Occasionally",
              "A few times a year"
            ],
            "原因": [
              "with friends",
              "see animals",
              "city zoo"
            ],
            "时间线+行为描述": [
              "during the holidays",
              "once or twice a year",
              "when I have time"
            ],
            "影响": [
              "fun experience",
              "learn about animals",
              "good for a day out"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型6 Whenever / 频率副词",
              "pattern": "Whenever I ______ / I ______ quite often.",
              "tip": "第3步：频次题用 Whenever 或 often / from time to time"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "A few times a year. Since with friends and see animals matters in my routine, I keep the habit consistently. It is common for me to do this during the holidays, so it has become automatic. This can be regarded as a habit that helps me fun experience, and it also helps me learn about animals.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 24,
          "title": "Do you type on a desktop or laptop keyboard every day",
          "q": "Do you type on a desktop or laptop keyboard every day?",
          "topicEn": "Typing",
          "topicZh": "打字",
          "tag": "沿用",
          "recentCount": 1260,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近1260人】习惯：描述日常频率和场景；打字=daily laptop + practice speed，对比 handwriting 强调 faster。 本题按「行为习惯类」四步答；素材：打字=daily laptop + practice speed，对比 handwriting 强调 faster。。",
          "logic": "习惯：描述日常频率和场景；打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "material": "打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "words": {
            "正面回答": [
              "my laptop keyboard",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "My laptop keyboard. Since since and for the reason that matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me stay focused, and it also saves time.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 25,
          "title": "How do you remember important things",
          "q": "How do you remember important things?",
          "topicEn": "Memory",
          "topicZh": "记忆",
          "tag": "沿用",
          "recentCount": 1218,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近1218人】习惯：手机备忘录/清单/重复记忆。 本题按「行为习惯类」四步答；素材：记忆=phone notes / to-do list，忘事承认 once forgot + lesson。。",
          "logic": "习惯：手机备忘录/清单/重复记忆。",
          "material": "记忆=phone notes / to-do list，忘事承认 once forgot + lesson。",
          "words": {
            "正面回答": [
              "Phone notes",
              "To-do lists",
              "Several methods"
            ],
            "原因": [
              "set reminders",
              "write them down",
              "repeat aloud"
            ],
            "时间线+行为描述": [
              "every day",
              "before exams",
              "for appointments"
            ],
            "影响": [
              "rarely forget",
              "really convenient",
              "saves mental energy"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Several methods. Since set reminders and write them down matters in my routine, I keep the habit consistently. It is common for me to do this every day, so it has become automatic. This can be regarded as a habit that helps me rarely forget, and it also helps me really convenient.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 26,
          "title": "What do you usually do in the morning",
          "q": "What do you usually do in the morning?",
          "topicEn": "Morning time",
          "topicZh": "早晨",
          "tag": "沿用",
          "recentCount": 1085,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1085人】习惯：描述日常频率和场景；早晨=get up → breakfast → get dressed，童年对比更晚起。 本题按「行为习惯类」四步答；素材：早晨=get up → breakfast → get dressed，童年对比更晚起。。",
          "logic": "习惯：描述日常频率和场景；早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "material": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "words": {
            "正面回答": [
              "I have a daily routine",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "self-care",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "after I get up",
              "go jogging",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "energetic",
              "full of energy",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + to do",
              "pattern": "It is ______ for me to ______ when ______.",
              "tip": "第3步：What do you do 题用形式主语描述具体行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "I have a daily routine. For the reason that I need a clear routine, I focus on self-care and since. It is normal for me to do this after I get up, especially when my schedule is busy. This habit can be seen as something that helps me energetic, and it also helps me full of energy.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 27,
          "title": "What did you do in the morning when you were little? Why",
          "q": "What did you do in the morning when you were little? Why?",
          "topicEn": "Morning time",
          "topicZh": "早晨",
          "tag": "沿用",
          "recentCount": 1085,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近1085人】习惯：描述日常频率和场景；早晨=get up → breakfast → get dressed，童年对比更晚起。 本题按「行为习惯类」四步答；素材：早晨=get up → breakfast → get dressed，童年对比更晚起。。",
          "logic": "习惯：描述日常频率和场景；早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "material": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "words": {
            "正面回答": [
              "It was quite simple",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "my parents requirements",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "before primary school",
              "have breakfast",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "strive in one",
              "s studies",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since my parents requirements and since matters in my routine, I keep the habit consistently. It is common for me to do this before primary school, so it has become automatic. This can be regarded as a habit that helps me strive in one, and it also helps me s studies.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue-alias"
        },
        {
          "id": 28,
          "title": "Do you walk a lot",
          "q": "Do you walk a lot?",
          "topicEn": "Walking",
          "topicZh": "走路",
          "tag": "沿用",
          "recentCount": 854,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近854人】习惯：描述日常频率和场景；走路=go for a walk in the park，解压+景色一笔带过。 本题按「行为习惯类」四步答；素材：走路=go for a walk in the park，解压+景色一笔带过。。",
          "logic": "习惯：描述日常频率和场景；走路=go for a walk in the park，解压+景色一笔带过。",
          "material": "走路=go for a walk in the park，解压+景色一笔带过。",
          "words": {
            "正面回答": [
              "Definitely",
              "Yes",
              "Usually",
              "Not really"
            ],
            "原因": [
              "relieve stress",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "in my free time",
              "go for a walk",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "feel relaxed and at ease",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since relieve stress and since matters in my routine, I keep the habit consistently. It is common for me to do this in my free time, so it has become automatic. This can be regarded as a habit that helps me feel relaxed and at ease, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 29,
          "title": "Did you often go outside to have a walk when you were a child",
          "q": "Did you often go outside to have a walk when you were a child?",
          "topicEn": "Walking",
          "topicZh": "走路",
          "tag": "沿用",
          "recentCount": 854,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近854人】习惯：描述日常频率和场景；走路=go for a walk in the park，解压+景色一笔带过。 本题按「行为习惯类」四步答；素材：走路=go for a walk in the park，解压+景色一笔带过。。",
          "logic": "习惯：描述日常频率和场景；走路=go for a walk in the park，解压+景色一笔带过。",
          "material": "走路=go for a walk in the park，解压+景色一笔带过。",
          "words": {
            "正面回答": [
              "Yes",
              "I used to",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "get close to nature",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "when the weather is nice",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "have a good laugh",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型7 can be seen / regarded as",
              "pattern": "______ can be seen / regarded as ______.",
              "tip": "第4步：被动语态收束影响，更客观"
            }
          },
          "sample": "Yes, definitely. Since get close to nature and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me have a good laugh, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 30,
          "title": "Do you look out the window at the scenery when travelling by bus or car",
          "q": "Do you look out the window at the scenery when travelling by bus or car?",
          "topicEn": "Scenery",
          "topicZh": "景色",
          "tag": "沿用",
          "recentCount": 777,
          "heatRank": 21,
          "tip": "【沿用·热度#21·近777人】习惯：描述日常频率和场景；景色=travel + take photos，山/海对比用 mountains vs sea。 本题按「行为习惯类」四步答；素材：景色=travel + take photos，山/海对比用 mountains vs sea。。",
          "logic": "习惯：描述日常频率和场景；景色=travel + take photos，山/海对比用 mountains vs sea。",
          "material": "景色=travel + take photos，山/海对比用 mountains vs sea。",
          "words": {
            "正面回答": [
              "I always do that",
              "Yes",
              "Usually",
              "Definitely",
              "Not really"
            ],
            "原因": [
              "when I feel bored",
              "since",
              "for the reason that",
              "because"
            ],
            "时间线+行为描述": [
              "take a bus",
              "listen to music",
              "every morning",
              "before class",
              "after dinner"
            ],
            "影响": [
              "clear my mind",
              "helps me stay focused",
              "saves time",
              "keeps me organised"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since / as",
              "pattern": "For the reason that / Since ______, I ______.",
              "tip": "第2步：高级原因状语，替换普通 because"
            },
            "2": {
              "name": "句型1A It is + adj. + for me to do",
              "pattern": "It is ______ for me to ______.",
              "tip": "第3步：形式主语描述时间线里的行为"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I always do that. Since when I feel bored and since matters in my routine, I keep the habit consistently. It is common for me to do this every morning, so it has become automatic. This can be regarded as a habit that helps me clear my mind, and it also helps me stay focused.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        }
      ]
    },
    {
      "id": "guandian",
      "name": "观点类",
      "steps": [
        "正面回答",
        "举例或原因",
        "作用或影响",
        "感受"
      ],
      "questions": [
        {
          "id": 1,
          "title": "Why do some people wear expensive watches",
          "q": "Why do some people wear expensive watches?",
          "topicEn": "Watch",
          "topicZh": "手表",
          "tag": "新增",
          "recentCount": 39172,
          "heatRank": 1,
          "tip": "【新增·热度#1·近39172人】观点：谈 status symbol / fashion，别说自己买奢侈品。 本题按「观点类」四步答；素材：物品·手表（实用计时）。",
          "logic": "观点：谈 status symbol / fashion，别说自己买奢侈品。",
          "material": "物品·手表（实用计时）",
          "words": {
            "正面回答": [
              "I think so",
              "it depends on the person",
              "Probably"
            ],
            "举例或原因": [
              "status symbol",
              "fashion statement",
              "show success"
            ],
            "作用或影响": [
              "match outfits",
              "at formal events",
              "for most people",
              "quite often"
            ],
            "感受": [
              "it depends on the person",
              "not my style",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since",
              "pattern": "I chose it for the reason that / since ______.",
              "tip": "第2步：Why 题直接给原因状语"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "I think so. Since an expensive watch can be a status symbol, some people wear one to make a fashion statement. They often do this at formal events, which shows success. I find it understandable, though it is not my style.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 2,
          "title": "Do you think it is important to wear a watch? Why",
          "q": "Do you think it is important to wear a watch? Why?",
          "topicEn": "Watch",
          "topicZh": "手表",
          "tag": "新增",
          "recentCount": 39172,
          "heatRank": 1,
          "tip": "【新增·热度#1·近39172人】观点：对学生=守时 punctual；可说不戴也行但方便。 本题按「观点类」四步答；素材：物品·手表（实用计时）。",
          "logic": "观点：对学生=守时 punctual；可说不戴也行但方便。",
          "material": "物品·手表（实用计时）",
          "words": {
            "正面回答": [
              "Yes",
              "quite important",
              "Quite useful",
              "It helps"
            ],
            "举例或原因": [
              "stay punctual",
              "check time quickly",
              "during class"
            ],
            "作用或影响": [
              "in class and meetings",
              "every day",
              "when busy"
            ],
            "感受": [
              "I find it practical",
              "really convenient",
              "helps me focus"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, quite important. Since students need to stay punctual, I wear a watch to check time quickly. It helps in class and meetings every day, which keeps me on schedule. I find it practical and really convenient.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 3,
          "title": "Do you think car colours are important",
          "q": "Do you think car colours are important?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 2,
          "tip": "【新增·热度#2·近12327人】观点：颜色=个性/耐脏，举例白车黑车。 本题按「观点类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "观点：颜色=个性/耐脏，举例白车黑车。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "it depends on the person",
              "Somewhat",
              "For some people"
            ],
            "举例或原因": [
              "personality",
              "easy to keep clean",
              "white or black cars"
            ],
            "作用或影响": [
              "when buying a car",
              "for resale value",
              "for most people",
              "quite often"
            ],
            "感受": [
              "some people care a lot",
              "not that important to me",
              "personal taste"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "It depends. Since colour can show personality, some people choose white or black cars to keep them easy to clean. When buying a car, this matters for resale value, which some buyers care about. Personally, I find it not that important to me.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 4,
          "title": "Do you think that your subject is popular in your country",
          "q": "Do you think that your subject is popular in your country?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】观点：先表态再理由；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「观点类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "观点：先表态再理由；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "it's quite popular",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "attend classes",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "practical",
              "for most people",
              "quite often"
            ],
            "感受": [
              "self-motivated",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since attend classes and since plays a real role. People often notice it through practical and for most people, which makes a clear difference in daily life. I find it important to keep this in mind, and self-motivated is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 5,
          "title": "What are the benefits of being your age",
          "q": "What are the benefits of being your age?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】观点：先表态再理由；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「观点类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "观点：先表态再理由；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "there are many advantages",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "hang out",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "be passionate about things",
              "for most people",
              "quite often"
            ],
            "感受": [
              "have a great time",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since hang out and since is common, people tend to talk about it seriously. This shows up in be passionate about things and for most people, which affects daily life more than we think. I find it important, and have a great time is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 6,
          "title": "What do you think is the most important at the moment",
          "q": "What do you think is the most important at the moment?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 3,
          "tip": "【万年·热度#3·近8666人】观点：先表态再理由；人生阶段用 childhood → university → next five years，计划落回 study。 本题按「观点类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "观点：先表态再理由；人生阶段用 childhood → university → next five years，计划落回 study。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "my studies",
              "for sure",
              "Yes",
              "I think so",
              "it depends on the person"
            ],
            "举例或原因": [
              "work hard at my studies",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "finish homework on my own",
              "for most people",
              "quite often"
            ],
            "感受": [
              "clear my mind",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "My studies. In my view, this matters since work hard at my studies and since plays a real role. People often notice it through finish homework on my own and for most people, which makes a clear difference in daily life. I find it important to keep this in mind, and clear my mind is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 7,
          "title": "What kinds of websites are popular in your country",
          "q": "What kinds of websites are popular in your country?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 4,
          "tip": "【新增·热度#4·近8064人】观点：短视频/电商/外卖平台流行。 本题按「观点类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "观点：短视频/电商/外卖平台流行。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "Short video apps",
              "E-commerce sites",
              "Social platforms"
            ],
            "举例或原因": [
              "Douyin",
              "Taobao",
              "WeChat"
            ],
            "作用或影响": [
              "almost everyone uses them",
              "every day",
              "all age groups"
            ],
            "感受": [
              "very convenient",
              "really popular",
              "part of daily life"
            ]
          },
          "frames": {
            "1": {
              "name": "句型2 I prefer / am keen on",
              "pattern": "I prefer / am keen on ______ because ______.",
              "tip": "第2步：类型题用 prefer / keen on + 简短原因"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Short video apps. Since Douyin and Taobao is common, people tend to talk about it seriously. This shows up in almost everyone uses them and every day, which affects daily life more than we think. I find it convenient, and very convenient is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 8,
          "title": "Does happy music make you feel more excited",
          "q": "Does happy music make you feel more excited?",
          "topicEn": "Music",
          "topicZh": "音乐",
          "tag": "新增",
          "recentCount": 3997,
          "heatRank": 5,
          "tip": "【新增·热度#5·近3997人】观点：欢快音乐让人更有活力。 本题按「观点类」四步答；素材：音乐=listen to music 解压。",
          "logic": "观点：欢快音乐让人更有活力。",
          "material": "音乐=listen to music 解压",
          "words": {
            "正面回答": [
              "Yes",
              "definitely",
              "Absolutely",
              "Most of the time"
            ],
            "举例或原因": [
              "upbeat songs",
              "faster tempo",
              "before exercising"
            ],
            "作用或影响": [
              "when I'm tired",
              "in the morning",
              "at parties"
            ],
            "感受": [
              "feel more energetic",
              "in a better mood",
              "mood booster"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since upbeat songs and faster tempo plays a real role. People often notice it through when I'm tired and in the morning, which makes a clear difference in daily life. I find it energetic to keep this in mind, and feel more energetic is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 9,
          "title": "What makes you feel pleasant in your home",
          "q": "What makes you feel pleasant in your home?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 6,
          "tip": "【万年·热度#6·近3178人】观点：先表态再理由；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「观点类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "观点：先表态再理由；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "the quiet",
              "private atmosphere",
              "Yes",
              "I think so",
              "it depends on the person"
            ],
            "举例或原因": [
              "dorms",
              "home",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "have some me-time",
              "for most people",
              "quite often"
            ],
            "感受": [
              "unwind",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since dorms and home is common, people tend to talk about it seriously. This shows up in have some me-time and for most people, which affects daily life more than we think. I find it important, and unwind is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 10,
          "title": "Do you think it is important to live in a comfortable environment",
          "q": "Do you think it is important to live in a comfortable environment?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 6,
          "tip": "【万年·热度#6·近3178人】观点：先表态再理由；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「观点类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "观点：先表态再理由；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "it's incredibly important",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "a residential area",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "self-care",
              "for most people",
              "quite often"
            ],
            "感受": [
              "feel relaxed and at ease",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since a residential area and since plays a real role. People often notice it through self-care and for most people, which makes a clear difference in daily life. I find it relaxed to keep this in mind, and feel relaxed and at ease is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 11,
          "title": "Do you think that it is necessary to be tidy",
          "q": "Do you think that it is necessary to be tidy?",
          "topicEn": "Tidiness",
          "topicZh": "整洁",
          "tag": "新增",
          "recentCount": 2982,
          "heatRank": 7,
          "tip": "【新增·热度#7·近2982人】观点：整洁提高效率，但不必完美主义。 本题按「观点类」四步答；素材：整洁=study space tidy → focus better，童年对比一句即可。。",
          "logic": "观点：整洁提高效率，但不必完美主义。",
          "material": "整洁=study space tidy → focus better，童年对比一句即可。",
          "words": {
            "正面回答": [
              "Yes",
              "quite necessary",
              "It helps a lot",
              "Generally yes"
            ],
            "举例或原因": [
              "focus better",
              "find things easily",
              "clear mind"
            ],
            "作用或影响": [
              "for studying",
              "at work",
              "in shared spaces"
            ],
            "感受": [
              "good habit",
              "not obsessive though",
              "balance is key"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since focus better and find things easily plays a real role. People often notice it through for studying and at work, which makes a clear difference in daily life. I find it practical to keep this in mind, and good habit is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 12,
          "title": "Do you think you will continue living there for a long time",
          "q": "Do you think you will continue living there for a long time?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 8,
          "tip": "【万年·热度#8·近2912人】观点：先表态再理由；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「观点类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "观点：先表态再理由；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "most likely",
              "yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "convenience stores",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "lifestyle",
              "for most people",
              "quite often"
            ],
            "感受": [
              "holds a lot of precious memories",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since convenience stores and since plays a real role. People often notice it through lifestyle and for most people, which makes a clear difference in daily life. I find it important to keep this in mind, and holds a lot of precious memories is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 13,
          "title": "Is your hometown a good place for young people to pursue their careers",
          "q": "Is your hometown a good place for young people to pursue their careers?",
          "topicEn": "Hometown",
          "topicZh": "家乡",
          "tag": "万年",
          "recentCount": 2912,
          "heatRank": 8,
          "tip": "【万年·热度#8·近2912人】观点：先表态再理由；家乡三件套：big/small city + famous for + young people，历史文化各一句。 本题按「观点类」四步答；素材：家乡三件套：big/small city + famous for + young people，历史文化各一句。。",
          "logic": "观点：先表态再理由；家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "material": "家乡三件套：big/small city + famous for + young people，历史文化各一句。",
          "words": {
            "正面回答": [
              "it's a great place for that",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "university students",
              "young workers",
              "start-ups"
            ],
            "作用或影响": [
              "take the initiative to",
              "for most people",
              "quite often"
            ],
            "感受": [
              "a real a real a real a real a real sense of achievement",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since university students and young workers is common, people tend to talk about it seriously. This shows up in take the initiative to and for most people, which affects daily life more than we think. I find it important, and a real a real a real a real a real sense of achievement is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 14,
          "title": "Is wearing headphones comfortable",
          "q": "Is wearing headphones comfortable?",
          "topicEn": "Headphones",
          "topicZh": "耳机",
          "tag": "新增",
          "recentCount": 2597,
          "heatRank": 9,
          "tip": "【新增·热度#9·近2597人】观点：短时间舒服，久了耳朵累。 本题按「观点类」四步答；素材：耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。。",
          "logic": "观点：短时间舒服，久了耳朵累。",
          "material": "耳机服务 listen to music / block noise，不舒适题承认 long time uncomfortable。",
          "words": {
            "正面回答": [
              "Mostly yes",
              "it depends on the person",
              "For a while"
            ],
            "举例或原因": [
              "soft ear cushions",
              "wireless is light",
              "good for commuting"
            ],
            "作用或影响": [
              "after an hour",
              "long sessions",
              "cheap ones hurt"
            ],
            "感受": [
              "comfortable enough",
              "take breaks sometimes",
              "worth it for music"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "It depends on the person. Since soft ear cushions and wireless is light is common, people tend to talk about it seriously. This shows up in after an hour and long sessions, which affects daily life more than we think. I find it comfortable, and comfortable enough is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 15,
          "title": "Do you think you spend too much time on social media",
          "q": "Do you think you spend too much time on social media?",
          "topicEn": "Social media",
          "topicZh": "社交媒体",
          "tag": "新增",
          "recentCount": 2310,
          "heatRank": 10,
          "tip": "【新增·热度#10·近2310人】观点：承认有点多，但用于学习/社交。 本题按「观点类」四步答；素材：社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。。",
          "logic": "观点：承认有点多，但用于学习/社交。",
          "material": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
          "words": {
            "正面回答": [
              "Sometimes yes",
              "A bit too much",
              "it depends on the person"
            ],
            "举例或原因": [
              "watch short videos",
              "chat with friends",
              "browse feeds"
            ],
            "作用或影响": [
              "before bed",
              "during breaks",
              "too often"
            ],
            "感受": [
              "should cut down",
              "also useful",
              "need self-control"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "It depends on the person. In my view, this matters since watch short videos and chat with friends plays a real role. People often notice it through before bed and during breaks, which makes a clear difference in daily life. I find it useful to keep this in mind, and should cut down is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 16,
          "title": "What do people often do on social media",
          "q": "What do people often do on social media?",
          "topicEn": "Social media",
          "topicZh": "社交媒体",
          "tag": "新增",
          "recentCount": 2310,
          "heatRank": 10,
          "tip": "【新增·热度#10·近2310人】观点：聊天、刷视频、晒生活。 本题按「观点类」四步答；素材：社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。。",
          "logic": "观点：聊天、刷视频、晒生活。",
          "material": "社媒=WeChat/Xiaohongshu 发帖聊天，观点题谈 spend too much time。",
          "words": {
            "正面回答": [
              "Many things",
              "Quite a lot",
              "Various activities"
            ],
            "举例或原因": [
              "chat with friends",
              "watch short videos",
              "post photos"
            ],
            "作用或影响": [
              "every day",
              "in their free time",
              "before bed"
            ],
            "感受": [
              "stay connected",
              "entertainment",
              "part of modern life"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Quite a lot. Since chat with friends and watch short videos is common, people tend to talk about it seriously. This shows up in every day and in their free time, which affects daily life more than we think. I find it practical, and stay connected is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 17,
          "title": "Do you think singing can bring happiness to people",
          "q": "Do you think singing can bring happiness to people?",
          "topicEn": "Singing",
          "topicZh": "唱歌",
          "tag": "新增",
          "recentCount": 2135,
          "heatRank": 11,
          "tip": "【新增·热度#11·近2135人】观点：唱歌释放情绪、增进感情。 本题按「观点类」四步答；素材：唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。。",
          "logic": "观点：唱歌释放情绪、增进感情。",
          "material": "唱歌=KTV/sing a song，开心与学习经历共用同一兴趣。",
          "words": {
            "正面回答": [
              "Yes",
              "absolutely",
              "Definitely",
              "I believe so"
            ],
            "举例或原因": [
              "share joy",
              "relieve stress",
              "bond with others"
            ],
            "作用或影响": [
              "at parties",
              "for all ages",
              "for most people",
              "quite often"
            ],
            "感受": [
              "music heals",
              "universal language",
              "simple but powerful"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since share joy and relieve stress plays a real role. People often notice it through at parties and for all ages, which makes a clear difference in daily life. I find it practical to keep this in mind, and music heals is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 18,
          "title": "Is the city friendly to children and old people",
          "q": "Is the city friendly to children and old people?",
          "topicEn": "The city you live in",
          "topicZh": "你住的城市",
          "tag": "万年",
          "recentCount": 1883,
          "heatRank": 12,
          "tip": "【万年·热度#12·近1883人】观点：先表态再理由；城市线：city + weather + friendly people + changes，与 area 素材互通。 本题按「观点类」四步答；素材：城市线：city + weather + friendly people + changes，与 area 素材互通。。",
          "logic": "观点：先表态再理由；城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "material": "城市线：city + weather + friendly people + changes，与 area 素材互通。",
          "words": {
            "正面回答": [
              "very friendly",
              "yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "the park",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "go for a walk",
              "for most people",
              "quite often"
            ],
            "感受": [
              "practical",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since the park and since is common, people tend to talk about it seriously. This shows up in go for a walk and for most people, which affects daily life more than we think. I find it practical, and practical is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 19,
          "title": "Do Chinese people often visit science museums",
          "q": "Do Chinese people often visit science museums?",
          "topicEn": "Science",
          "topicZh": "科学",
          "tag": "新增",
          "recentCount": 1834,
          "heatRank": 13,
          "tip": "【新增·热度#13·近1834人】观点：假期带孩子去科技馆很常见。 本题按「观点类」四步答；素材：科学=school science + museum/experiments，兴趣落到 interesting experiments。。",
          "logic": "观点：假期带孩子去科技馆很常见。",
          "material": "科学=school science + museum/experiments，兴趣落到 interesting experiments。",
          "words": {
            "正面回答": [
              "Yes",
              "quite often",
              "Especially families",
              "it's quite popular"
            ],
            "举例或原因": [
              "science museum",
              "interactive exhibits",
              "during the holidays"
            ],
            "作用或影响": [
              "on weekends",
              "school trips",
              "during vacations"
            ],
            "感受": [
              "educational and fun",
              "good for kids",
              "worth visiting"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since science museum and interactive exhibits is common, people tend to talk about it seriously. This shows up in on weekends and school trips, which affects daily life more than we think. I find it fun, and educational and fun is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 20,
          "title": "Are comedy shows popular in your country",
          "q": "Are comedy shows popular in your country?",
          "topicEn": "Jokes & Comedies",
          "topicZh": "笑话与喜剧",
          "tag": "新增",
          "recentCount": 1680,
          "heatRank": 14,
          "tip": "【新增·热度#14·近1680人】观点：脱口秀/喜剧综艺很火。 本题按「观点类」四步答；素材：笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。。",
          "logic": "观点：脱口秀/喜剧综艺很火。",
          "material": "笑话喜剧=watch comedies / have a good laugh，现场表演用 live show。",
          "words": {
            "正面回答": [
              "Yes",
              "very popular",
              "it's quite popular",
              "Growing fast"
            ],
            "举例或原因": [
              "stand-up comedy",
              "TV variety shows",
              "online clips"
            ],
            "作用或影响": [
              "young people love them",
              "every weekend",
              "on streaming apps"
            ],
            "感受": [
              "easy entertainment",
              "social topic",
              "good stress relief"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since stand-up comedy and TV variety shows is common, people tend to talk about it seriously. This shows up in young people love them and every weekend, which affects daily life more than we think. I find it practical, and easy entertainment is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 21,
          "title": "What do you consider when choosing a gift",
          "q": "What do you consider when choosing a gift?",
          "topicEn": "Gifts",
          "topicZh": "礼物",
          "tag": "沿用",
          "recentCount": 1386,
          "heatRank": 15,
          "tip": "【沿用·热度#15·近1386人】观点：先表态再理由；礼物=handmade / thoughtful gift，选择看 receiver's preference。 本题按「观点类」四步答；素材：礼物=handmade / thoughtful gift，选择看 receiver's preference。。",
          "logic": "观点：先表态再理由；礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "material": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "words": {
            "正面回答": [
              "functionality comes first",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "coat",
              "sweatshirt",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "practical",
              "for most people",
              "quite often"
            ],
            "感受": [
              "lifts my mood",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since coat and sweatshirt is common, people tend to talk about it seriously. This shows up in practical and for most people, which affects daily life more than we think. I find it important, and lifts my mood is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 22,
          "title": "Do you think you are good at choosing gifts",
          "q": "Do you think you are good at choosing gifts?",
          "topicEn": "Gifts",
          "topicZh": "礼物",
          "tag": "沿用",
          "recentCount": 1386,
          "heatRank": 15,
          "tip": "【沿用·热度#15·近1386人】观点：先表态再理由；礼物=handmade / thoughtful gift，选择看 receiver's preference。 本题按「观点类」四步答；素材：礼物=handmade / thoughtful gift，选择看 receiver's preference。。",
          "logic": "观点：先表态再理由；礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "material": "礼物=handmade / thoughtful gift，选择看 receiver's preference。",
          "words": {
            "正面回答": [
              "I'm quite good at it",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "open up to each other",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "lifestyle",
              "for most people",
              "quite often"
            ],
            "感受": [
              "have a good laugh",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "I'm quite good at it. In my view, this matters since open up to each other and since plays a real role. People often notice it through lifestyle and for most people, which makes a clear difference in daily life. I find it important to keep this in mind, and have a good laugh is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 23,
          "title": "What is the most popular animal in China",
          "q": "What is the most popular animal in China?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近1330人】观点：先表态再理由；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。 本题按「观点类」四步答；素材：宠物=puppy at home。",
          "logic": "观点：先表态再理由；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "I'd say pandas and dogs",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "loyal",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "self-care",
              "for most people",
              "quite often"
            ],
            "感受": [
              "a great way to unwind",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "I'd say pandas and dogs. Since loyal and since is common, people tend to talk about it seriously. This shows up in self-care and for most people, which affects daily life more than we think. I find it important, and a great way to unwind is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 24,
          "title": "Are there many people keeping pets in your country",
          "q": "Are there many people keeping pets in your country?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近1330人】观点：养宠物越来越普遍，尤其猫狗。 本题按「观点类」四步答；素材：宠物=puppy at home。",
          "logic": "观点：养宠物越来越普遍，尤其猫狗。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "Yes",
              "more and more",
              "Quite common",
              "Definitely growing"
            ],
            "举例或原因": [
              "cats and dogs",
              "especially in cities",
              "emotional companions"
            ],
            "作用或影响": [
              "nowadays",
              "among young people",
              "in urban areas"
            ],
            "感受": [
              "shows lifestyle change",
              "pets bring joy",
              "responsible ownership matters"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since cats and dogs and especially in cities is common, people tend to talk about it seriously. This shows up nowadays and among young people, which affects daily life more than we think. I find it practical, and shows lifestyle change is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 25,
          "title": "Should schools teach students knowledge about pets or animals",
          "q": "Should schools teach students knowledge about pets or animals?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近1330人】观点：应该教，培养爱心与责任感。 本题按「观点类」四步答；素材：宠物=puppy at home。",
          "logic": "观点：应该教，培养爱心与责任感。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "Yes",
              "they should",
              "Definitely",
              "Absolutely"
            ],
            "举例或原因": [
              "animal welfare",
              "respect nature",
              "responsible pet care"
            ],
            "作用或影响": [
              "in science class",
              "through field trips",
              "at primary school"
            ],
            "感受": [
              "build empathy",
              "practical knowledge",
              "good for society"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Yes, definitely. In my view, this matters since animal welfare and respect nature plays a real role. People often notice it through in science class and through field trips, which makes a clear difference in daily life. I find it practical to keep this in mind, and build empathy is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 26,
          "title": "Is team sports popular in your culture",
          "q": "Is team sports popular in your culture?",
          "topicEn": "Sports team",
          "topicZh": "运动队",
          "tag": "沿用",
          "recentCount": 1022,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近1022人】观点：先表态再理由；运动队=basketball/volleyball + teamwork，观看与参与同一套。 本题按「观点类」四步答；素材：运动队=basketball/volleyball + teamwork，观看与参与同一套。。",
          "logic": "观点：先表态再理由；运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "material": "运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "words": {
            "正面回答": [
              "Absolutely yes",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "play basketball",
              "volleyball",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "motivate each other",
              "for most people",
              "quite often"
            ],
            "感受": [
              "feel relaxed and at ease",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since play basketball and volleyball is common, people tend to talk about it seriously. This shows up in motivate each other and for most people, which affects daily life more than we think. I find it relaxed, and feel relaxed and at ease is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 27,
          "title": "What do you think is the most important at the moment",
          "q": "What do you think is the most important at the moment?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近959人】观点：先表态再理由；人生阶段用 childhood → university → next five years，计划落回 study。 本题按「观点类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "观点：先表态再理由；人生阶段用 childhood → university → next five years，计划落回 study。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "my studies",
              "for sure",
              "Yes",
              "I think so",
              "it depends on the person"
            ],
            "举例或原因": [
              "work hard at my studies",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "finish homework on my own",
              "for most people",
              "quite often"
            ],
            "感受": [
              "clear my mind",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "My studies. In my view, this matters since work hard at my studies and since plays a real role. People often notice it through finish homework on my own and for most people, which makes a clear difference in daily life. I find it important to keep this in mind, and clear my mind is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 28,
          "title": "How do people remember each stage of their lives",
          "q": "How do people remember each stage of their lives?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近959人】观点：靠照片/日记/重要事件标记。 本题按「观点类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "观点：靠照片/日记/重要事件标记。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "In different ways",
              "Through memories",
              "Many methods"
            ],
            "举例或原因": [
              "photos",
              "diaries",
              "important milestones"
            ],
            "作用或影响": [
              "birthdays",
              "graduations",
              "family trips"
            ],
            "感受": [
              "precious memories",
              "shape who we are",
              "look back fondly"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "In different ways. Since photos and diaries is common, people tend to talk about it seriously. This shows up in birthdays and graduations, which affects daily life more than we think. I find it practical, and precious memories is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 29,
          "title": "At what age do you think people are the happiest",
          "q": "At what age do you think people are the happiest?",
          "topicEn": "Life stages",
          "topicZh": "人生阶段",
          "tag": "沿用",
          "recentCount": 959,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近959人】观点：童年无忧无虑或青年有自由。 本题按「观点类」四步答；素材：人生阶段用 childhood → university → next five years，计划落回 study。。",
          "logic": "观点：童年无忧无虑或青年有自由。",
          "material": "人生阶段用 childhood → university → next five years，计划落回 study。",
          "words": {
            "正面回答": [
              "It varies",
              "Childhood perhaps",
              "Hard to say"
            ],
            "举例或原因": [
              "childhood is carefree",
              "young adults have freedom",
              "depends on the person"
            ],
            "作用或影响": [
              "different life stages",
              "for different people",
              "no single answer"
            ],
            "感受": [
              "each age has joys",
              "subjective question",
              "interesting to think about"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 In my view / since",
              "pattern": "In my view, ______ since ______.",
              "tip": "第2步：观点题先亮态度，since 给理由"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "It varies. In my view, this matters since childhood is carefree and young adults have freedom plays a real role. People often notice it through different life stages and for different people, which makes a clear difference in daily life. I find it practical to keep this in mind, and each age has joys is my overall attitude.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 30,
          "title": "Why do people like to walk in parks",
          "q": "Why do people like to walk in parks?",
          "topicEn": "Walking",
          "topicZh": "走路",
          "tag": "沿用",
          "recentCount": 854,
          "heatRank": 19,
          "tip": "【沿用·热度#19·近854人】观点：先表态再理由；走路=go for a walk in the park，解压+景色一笔带过。 本题按「观点类」四步答；素材：走路=go for a walk in the park，解压+景色一笔带过。。",
          "logic": "观点：先表态再理由；走路=go for a walk in the park，解压+景色一笔带过。",
          "material": "走路=go for a walk in the park，解压+景色一笔带过。",
          "words": {
            "正面回答": [
              "to get close to nature",
              "Yes",
              "I think so",
              "it depends on the person",
              "Somewhat"
            ],
            "举例或原因": [
              "in their free time",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "have some me-time",
              "for most people",
              "quite often"
            ],
            "感受": [
              "go for a walk",
              "relieve stress",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 for the reason that / since",
              "pattern": "I chose it for the reason that / since ______.",
              "tip": "第2步：Why 题直接给原因状语"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "Yes, definitely. Since in their free time and since is common, people tend to talk about it seriously. This shows up in have some me-time and for most people, which affects daily life more than we think. I find it important, and go for a walk is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 31,
          "title": "Do most people like crowded places",
          "q": "Do most people like crowded places?",
          "topicEn": "Crowded place",
          "topicZh": "拥挤的地方",
          "tag": "沿用",
          "recentCount": 728,
          "heatRank": 20,
          "tip": "【沿用·热度#20·近728人】观点：先表态再理由；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。 本题按「观点类」四步答；素材：拥挤=city centre / rush hour / shopping malls，喜好偏 not really。。",
          "logic": "观点：先表态再理由；拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "material": "拥挤=city centre / rush hour / shopping malls，喜好偏 not really。",
          "words": {
            "正面回答": [
              "it depends on the person",
              "Yes",
              "I think so",
              "Somewhat"
            ],
            "举例或原因": [
              "be passionate about",
              "city centre",
              "since",
              "in my view"
            ],
            "作用或影响": [
              "meet like-minded people",
              "for most people",
              "quite often"
            ],
            "感受": [
              "it really gets to me",
              "quite important",
              "makes sense",
              "understandable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型3 since + 句型5 to do",
              "pattern": "Since ______, people / I ______ to ______.",
              "tip": "第2步：since/for the reason that 给原因，to do 表目的"
            },
            "2": {
              "name": "句型4 which 补充说明",
              "pattern": "..., which ______.",
              "tip": "第3步：非限定定语从句，补作用或影响"
            },
            "3": {
              "name": "句型1B I find it + adj. + to do",
              "pattern": "I / they find it ______ to ______.",
              "tip": "第4步：形式宾语收束感受或普遍看法"
            }
          },
          "sample": "It depends on the person. Since be passionate about and city centre is common, people tend to talk about it seriously. This shows up in meet like-minded people and for most people, which affects daily life more than we think. I find it important, and it really gets to me is a fair conclusion.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        }
      ]
    },
    {
      "id": "duibi",
      "name": "对比类",
      "steps": [
        "正面回答",
        "选项1的特点与作用",
        "选项2的特点与作用",
        "个人感受"
      ],
      "questions": [
        {
          "id": 1,
          "title": "Do you prefer to be a driver or a passenger",
          "q": "Do you prefer to be a driver or a passenger?",
          "topicEn": "Cars",
          "topicZh": "汽车",
          "tag": "新增",
          "recentCount": 12327,
          "heatRank": 1,
          "tip": "【新增·热度#1·近12327人】对比：司机=自由；乘客=放松。 本题按「对比类」四步答；素材：汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。。",
          "logic": "对比：司机=自由；乘客=放松。",
          "material": "汽车题按子题分：童年出游/车型偏好/堵车行为/司机乘客对比，词块别混用。",
          "words": {
            "正面回答": [
              "I'd rather be a passenger",
              "I prefer being a passenger",
              "Passenger"
            ],
            "选项1的特点与作用": [
              "more relaxing",
              "can rest",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "driver has more control",
              "more tiring",
              "need to focus"
            ],
            "个人感受": [
              "I feel more comfortable as a passenger",
              "can enjoy the view",
              "less pressure"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I'd rather be a passenger. As for being a passenger, it is regarded as more relaxing to rest. By contrast, regarding driving, people find it more tiring to focus the whole time. I find being a passenger more comfortable, which lets me enjoy the view.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 2,
          "title": "Do you prefer to study in the mornings or in the afternoons",
          "q": "Do you prefer to study in the mornings or in the afternoons?",
          "topicEn": "Work or studies",
          "topicZh": "工作/学习",
          "tag": "万年",
          "recentCount": 8666,
          "heatRank": 2,
          "tip": "【万年·热度#2·近8666人】对比：两边各说特点再表态；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。 本题按「对比类」四步答；素材：学生线：subject + why choose + study routine。",
          "logic": "对比：两边各说特点再表态；学生线：subject + why choose + study routine；工作线可简答后拉回学习场景。",
          "material": "学生线：subject + why choose + study routine",
          "words": {
            "正面回答": [
              "definitely in the mornings",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "have breakfast",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "binge-watch TV shows",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "work hard at my studies",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer having breakfast to binge-watching TV shows. A proper breakfast keeps me focused for morning classes, while long shows often waste time and make me sluggish. Overall, studying with energy matters more to me.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 3,
          "title": "Do you prefer getting information from websites or books",
          "q": "Do you prefer getting information from websites or books?",
          "topicEn": "Websites",
          "topicZh": "网站",
          "tag": "新增",
          "recentCount": 8064,
          "heatRank": 3,
          "tip": "【新增·热度#3·近8064人】对比：网站快更新；书更系统。 本题按「对比类」四步答；素材：网站=查资料+刷内容：search information / watch short videos，感受用 practical。。",
          "logic": "对比：网站快更新；书更系统。",
          "material": "网站=查资料+刷内容：search information / watch short videos，感受用 practical。",
          "words": {
            "正面回答": [
              "I prefer websites",
              "Websites for sure",
              "Mostly websites"
            ],
            "选项1的特点与作用": [
              "faster",
              "up to date",
              "easy to search"
            ],
            "选项2的特点与作用": [
              "books are deeper",
              "better for focus",
              "more detailed"
            ],
            "个人感受": [
              "websites suit my daily needs",
              "both are useful",
              "depends on the topic"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer websites. As for websites, they are regarded as faster and up to date to search. By contrast, regarding books, people find them deeper and better for focus. I find websites more suitable for daily needs, which still leaves room for books on hard topics.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "hand",
          "wordSource": "explicit"
        },
        {
          "id": 4,
          "title": "Do you like your primary school teachers more than your high school t...",
          "q": "Do you like your primary school teachers more than your high school teachers?",
          "topicEn": "Teachers",
          "topicZh": "老师",
          "tag": "新增",
          "recentCount": 5845,
          "heatRank": 4,
          "tip": "【新增·热度#4·近5845人】对比：小学亲切 vs 高中严格但专业。 本题按「对比类」四步答；素材：记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。。",
          "logic": "对比：小学亲切 vs 高中严格但专业。",
          "material": "记住一位老师+具体帮助（explain concepts），喜好/对比都复用同一老师故事。",
          "words": {
            "正面回答": [
              "I prefer high school teachers",
              "Both were great",
              "Hard to choose"
            ],
            "选项1的特点与作用": [
              "more professional",
              "deeper knowledge",
              "better at explaining"
            ],
            "选项2的特点与作用": [
              "primary teachers were warmer",
              "like family",
              "more playful"
            ],
            "个人感受": [
              "both mattered to me",
              "different stages",
              "each helped me grow"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "I prefer high school teachers. As for the first side, it is regarded as stronger because of more professional and deeper knowledge. By contrast, regarding the other side, people find it different due to primary teachers were warmer and like family. Overall, I find both mattered to me more suitable, which different stages.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 5,
          "title": "Would you prefer to play in a personal garden or public garden",
          "q": "Would you prefer to play in a personal garden or public garden?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】对比：私家花园安静 vs 公园设施多。 本题按「对比类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "对比：私家花园安静 vs 公园设施多。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "I'd prefer a public garden",
              "Public garden",
              "Depends"
            ],
            "选项1的特点与作用": [
              "more facilities",
              "bigger space",
              "meet more people"
            ],
            "选项2的特点与作用": [
              "personal garden is quieter",
              "more private",
              "at home"
            ],
            "个人感受": [
              "public parks are more fun",
              "easier to access",
              "more variety"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I'd prefer a public garden. As for the first side, it is regarded as stronger because of more facilities and bigger space. By contrast, regarding the other side, people find it different due to personal garden is quieter and more private. Overall, I find public parks are more fun more suitable, which easier to access.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 6,
          "title": "How are the parks today different from those you visited as a kid",
          "q": "How are the parks today different from those you visited as a kid?",
          "topicEn": "Public gardens and parks",
          "topicZh": "公园",
          "tag": "新增",
          "recentCount": 4816,
          "heatRank": 5,
          "tip": "【新增·热度#5·近4816人】对比：现在公园更现代/更多健身设施。 本题按「对比类」四步答；素材：公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。。",
          "logic": "对比：现在公园更现代/更多健身设施。",
          "material": "公园万能：go for a walk / hang out / fresh air，童年与现在同一地点。",
          "words": {
            "正面回答": [
              "Quite different",
              "Much better now",
              "Huge changes"
            ],
            "选项1的特点与作用": [
              "more playgrounds",
              "better paths",
              "fitness equipment"
            ],
            "选项2的特点与作用": [
              "older parks were simpler",
              "fewer facilities",
              "more natural"
            ],
            "个人感受": [
              "both are nice",
              "prefer the upgrades",
              "more convenient now"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "Quite different. As for the first side, it is regarded as stronger because of more playgrounds and better paths. By contrast, regarding the other side, people find it different due to older parks were simpler and fewer facilities. Overall, I find both are nice more suitable, which prefer the upgrades.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 7,
          "title": "Do you prefer online shopping or in-store shopping",
          "q": "Do you prefer online shopping or in-store shopping?",
          "topicEn": "Shopping",
          "topicZh": "购物",
          "tag": "新增",
          "recentCount": 4312,
          "heatRank": 6,
          "tip": "【新增·热度#6·近4312人】对比：网购方便 vs 实体店可试穿。 本题按「对比类」四步答；素材：购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。。",
          "logic": "对比：网购方便 vs 实体店可试穿。",
          "material": "购物统一 shop online / shopping malls / return items，对比线强调方便 vs 试穿。",
          "words": {
            "正面回答": [
              "I prefer online shopping",
              "Online for sure",
              "Mostly online"
            ],
            "选项1的特点与作用": [
              "more convenient",
              "pay by phone",
              "delivered to my door"
            ],
            "选项2的特点与作用": [
              "can try on clothes",
              "see the quality",
              "instant purchase"
            ],
            "个人感受": [
              "online suits my lifestyle",
              "both have pros",
              "depends on the item"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer online shopping. As for the first side, it is regarded as stronger because of more convenient and pay by phone. By contrast, regarding the other side, people find it different due to can try on clothes and see the quality. Overall, I find online suits my lifestyle more suitable, which both have pros.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 8,
          "title": "Do you prefer sad or happy music",
          "q": "Do you prefer sad or happy music?",
          "topicEn": "Music",
          "topicZh": "音乐",
          "tag": "新增",
          "recentCount": 3997,
          "heatRank": 7,
          "tip": "【新增·热度#7·近3997人】对比：开心音乐解压 vs 慢歌安静。 本题按「对比类」四步答；素材：音乐=listen to music 解压。",
          "logic": "对比：开心音乐解压 vs 慢歌安静。",
          "material": "音乐=listen to music 解压",
          "words": {
            "正面回答": [
              "I prefer happy music",
              "Happy music",
              "Mostly upbeat"
            ],
            "选项1的特点与作用": [
              "relieve stress",
              "feel more positive",
              "while studying"
            ],
            "选项2的特点与作用": [
              "sad songs are emotional",
              "good when relaxing",
              "sometimes meaningful"
            ],
            "个人感受": [
              "happy music fits my mood",
              "both are fine",
              "depends on the moment"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer happy music. As for the first side, it is regarded as stronger because of relieve stress and feel more positive. By contrast, regarding the other side, people find it different due to sad songs are emotional and good when relaxing. Overall, I find happy music fits my mood more suitable, which both are fine.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 9,
          "title": "Do you prefer living in a house or an apartment",
          "q": "Do you prefer living in a house or an apartment?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 8,
          "tip": "【万年·热度#8·近3178人】对比：两边各说特点再表态；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「对比类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "对比：两边各说特点再表态；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "an apartment",
              "for now",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "my rented apartment",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "attend classes",
              "parties",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "practical",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer living in a rented apartment near campus. It is more practical for attending classes, even though parties with friends are fun. Being close to school helps me manage time better.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 10,
          "title": "What’s the difference between where you are living now and where you ...",
          "q": "What’s the difference between where you are living now and where you have lived in the past?",
          "topicEn": "Home & Accommodation",
          "topicZh": "住宿",
          "tag": "万年",
          "recentCount": 3178,
          "heatRank": 8,
          "tip": "【万年·热度#8·近3178人】对比：两边各说特点再表态；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。 本题按「对比类」四步答；素材：住宿线：dorms/apartment + roommate + favourite room，交通用 subway。。",
          "logic": "对比：两边各说特点再表态；住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "material": "住宿线：dorms/apartment + roommate + favourite room，交通用 subway。",
          "words": {
            "正面回答": [
              "there's a huge difference",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "a residential area",
              "convenience stores",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "dorms",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "feel relaxed and at ease",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer A. As for the first side, it is regarded as stronger because of a residential area and convenience stores. By contrast, regarding the other side, people find it different due to dorms and by contrast. Overall, I find feel relaxed and at ease more suitable, which I prefer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 11,
          "title": "Do you prefer to wear comfortable and casual clothes or smart clothes",
          "q": "Do you prefer to wear comfortable and casual clothes or smart clothes?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 9,
          "tip": "【新增·热度#9·近3115人】对比：休闲舒服 vs 正式得体。 本题按「对比类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "对比：休闲舒服 vs 正式得体。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Comfortable and casual",
              "Casual for sure",
              "Comfort first"
            ],
            "选项1的特点与作用": [
              "t-shirt",
              "sneakers",
              "soft fabrics"
            ],
            "选项2的特点与作用": [
              "smart clothes for interviews",
              "formal events",
              "look professional"
            ],
            "个人感受": [
              "casual fits my lifestyle",
              "smart when needed",
              "both have uses"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "Comfortable and casual. As for the first side, it is regarded as stronger because of t-shirt and sneakers. By contrast, regarding the other side, people find it different due to smart clothes for interviews and formal events. Overall, I find casual fits my lifestyle more suitable, which smart when needed.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 12,
          "title": "Do you wear different styles of clothes on weekdays and weekends",
          "q": "Do you wear different styles of clothes on weekdays and weekends?",
          "topicEn": "Clothing",
          "topicZh": "衣服",
          "tag": "新增",
          "recentCount": 3115,
          "heatRank": 9,
          "tip": "【新增·热度#9·近3115人】对比：工作日简约 vs 周末更随意。 本题按「对比类」四步答；素材：衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。。",
          "logic": "对比：工作日简约 vs 周末更随意。",
          "material": "衣服只记 t-shirt / coat / comfortable，工作日周末对比即可。",
          "words": {
            "正面回答": [
              "Yes",
              "quite different",
              "A little different",
              "Somewhat"
            ],
            "选项1的特点与作用": [
              "casual on weekends",
              "sportswear",
              "more colourful"
            ],
            "选项2的特点与作用": [
              "simple on weekdays",
              "uniform-like",
              "for class"
            ],
            "个人感受": [
              "weekends feel freer",
              "both are comfortable",
              "depends on plans"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "Yes, definitely. As for the first side, it is regarded as stronger because of casual on weekends and sportswear. By contrast, regarding the other side, people find it different due to simple on weekdays and uniform-like. Overall, I find weekends feel freer more suitable, which both are comfortable.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 13,
          "title": "Which day do you have more free time on, Saturday or Sunday",
          "q": "Which day do you have more free time on, Saturday or Sunday?",
          "topicEn": "Spare time",
          "topicZh": "空闲时间",
          "tag": "沿用",
          "recentCount": 1834,
          "heatRank": 10,
          "tip": "【沿用·热度#10·近1834人】对比：周六外出周日休息或相反。 本题按「对比类」四步答；素材：空闲时间直接套 daily leisure：watch short videos / hang out / sports。。",
          "logic": "对比：周六外出周日休息或相反。",
          "material": "空闲时间直接套 daily leisure：watch short videos / hang out / sports。",
          "words": {
            "正面回答": [
              "Saturday",
              "Sunday",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "hang out with friends",
              "go shopping",
              "more social"
            ],
            "选项2的特点与作用": [
              "stay at home",
              "finish homework",
              "prepare for Monday"
            ],
            "个人感受": [
              "Saturday is livelier",
              "Sunday is calmer",
              "both are precious"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "It depends on the person. As for the first side, it is regarded as stronger because of hang out with friends and go shopping. By contrast, regarding the other side, people find it different due to stay at home and finish homework. Overall, I find Saturday is livelier more suitable, which Sunday is calmer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 14,
          "title": "Do you prefer views in urban areas or rural areas",
          "q": "Do you prefer views in urban areas or rural areas?",
          "topicEn": "Views",
          "topicZh": "风景/取景",
          "tag": "沿用",
          "recentCount": 1743,
          "heatRank": 11,
          "tip": "【沿用·热度#11·近1743人】对比：两边各说特点再表态；与 scenery 共用 take photos of views，城乡对比即可。 本题按「对比类」四步答；素材：与 scenery 共用 take photos of views，城乡对比即可。。",
          "logic": "对比：两边各说特点再表态；与 scenery 共用 take photos of views，城乡对比即可。",
          "material": "与 scenery 共用 take photos of views，城乡对比即可。",
          "words": {
            "正面回答": [
              "I prefer urban views",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "city centre",
              "shopping malls",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "the park",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "practical and makes me happy",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer urban views. As for the first side, it is regarded as stronger because of city centre and shopping malls. By contrast, regarding the other side, people find it different due to the park and by contrast. Overall, I find practical and makes me happy more suitable, which I prefer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 15,
          "title": "Do you prefer views in your own country or in other countries",
          "q": "Do you prefer views in your own country or in other countries?",
          "topicEn": "Views",
          "topicZh": "风景/取景",
          "tag": "沿用",
          "recentCount": 1743,
          "heatRank": 11,
          "tip": "【沿用·热度#11·近1743人】对比：两边各说特点再表态；与 scenery 共用 take photos of views，城乡对比即可。 本题按「对比类」四步答；素材：与 scenery 共用 take photos of views，城乡对比即可。。",
          "logic": "对比：两边各说特点再表态；与 scenery 共用 take photos of views，城乡对比即可。",
          "material": "与 scenery 共用 take photos of views，城乡对比即可。",
          "words": {
            "正面回答": [
              "in my own country",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "tasty local food",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "groceries",
              "fresh ingredients",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "it really hits the spot",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer tasty local food when I eat out. It really hits the spot, although buying groceries and cooking with fresh ingredients is healthier. For a quick treat, local dishes win for me.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 16,
          "title": "Where do you prefer to keep your pet, indoors or outdoors",
          "q": "Where do you prefer to keep your pet, indoors or outdoors?",
          "topicEn": "Pets and Animals",
          "topicZh": "宠物与动物",
          "tag": "沿用",
          "recentCount": 1330,
          "heatRank": 12,
          "tip": "【沿用·热度#12·近1330人】对比：两边各说特点再表态；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。 本题按「对比类」四步答；素材：宠物=puppy at home。",
          "logic": "对比：两边各说特点再表态；宠物=puppy at home；动物喜好/动物园复用同一情感词 unwind。",
          "material": "宠物=puppy at home",
          "words": {
            "正面回答": [
              "definitely indoors",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "home",
              "dorms",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "the park",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "unwind",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer A. As for the first side, it is regarded as stronger because of home and dorms. By contrast, regarding the other side, people find it different due to the park and by contrast. Overall, I find unwind more suitable, which I prefer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 17,
          "title": "Do you prefer typing or handwriting",
          "q": "Do you prefer typing or handwriting?",
          "topicEn": "Typing",
          "topicZh": "打字",
          "tag": "沿用",
          "recentCount": 1260,
          "heatRank": 13,
          "tip": "【沿用·热度#13·近1260人】对比：两边各说特点再表态；打字=daily laptop + practice speed，对比 handwriting 强调 faster。 本题按「对比类」四步答；素材：打字=daily laptop + practice speed，对比 handwriting 强调 faster。。",
          "logic": "对比：两边各说特点再表态；打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "material": "打字=daily laptop + practice speed，对比 handwriting 强调 faster。",
          "words": {
            "正面回答": [
              "typing",
              "for sure",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "shop online",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "the classroom",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "time-saving and effortless",
              "practical",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer shopping online because it is time-saving and effortless. Going out or dealing with crowded places takes longer. For daily needs, online shopping suits me better.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 18,
          "title": "Are there any differences between what you do in the morning now and ...",
          "q": "Are there any differences between what you do in the morning now and what you did in the past?",
          "topicEn": "Morning time",
          "topicZh": "早晨",
          "tag": "沿用",
          "recentCount": 1085,
          "heatRank": 14,
          "tip": "【沿用·热度#14·近1085人】对比：两边各说特点再表态；早晨=get up → breakfast → get dressed，童年对比更晚起。 本题按「对比类」四步答；素材：早晨=get up → breakfast → get dressed，童年对比更晚起。。",
          "logic": "对比：两边各说特点再表态；早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "material": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "words": {
            "正面回答": [
              "totally different",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "have breakfast",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "watch short videos",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "feel relaxed and at ease",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "I prefer having breakfast in the morning rather than scrolling short videos. Eating properly helps me feel relaxed and ready for the day, while videos often leave me restless.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 19,
          "title": "Do you spend your mornings doing the same things on both weekends and...",
          "q": "Do you spend your mornings doing the same things on both weekends and weekdays? Why?",
          "topicEn": "Morning time",
          "topicZh": "早晨",
          "tag": "沿用",
          "recentCount": 1085,
          "heatRank": 14,
          "tip": "【沿用·热度#14·近1085人】对比：两边各说特点再表态；早晨=get up → breakfast → get dressed，童年对比更晚起。 本题按「对比类」四步答；素材：早晨=get up → breakfast → get dressed，童年对比更晚起。。",
          "logic": "对比：两边各说特点再表态；早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "material": "早晨=get up → breakfast → get dressed，童年对比更晚起。",
          "words": {
            "正面回答": [
              "no",
              "they're quite different",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "attend classes",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "binge-watch TV shows",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "self-care",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "I prefer attending classes over binge-watching TV shows. Classes keep me on track, and I still leave some evening time for self-care. Balance matters more than endless episodes.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 20,
          "title": "What are the differences between team sports and individual sports",
          "q": "What are the differences between team sports and individual sports?",
          "topicEn": "Sports team",
          "topicZh": "运动队",
          "tag": "沿用",
          "recentCount": 1022,
          "heatRank": 15,
          "tip": "【沿用·热度#15·近1022人】对比：两边各说特点再表态；运动队=basketball/volleyball + teamwork，观看与参与同一套。 本题按「对比类」四步答；素材：运动队=basketball/volleyball + teamwork，观看与参与同一套。。",
          "logic": "对比：两边各说特点再表态；运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "material": "运动队=basketball/volleyball + teamwork，观看与参与同一套。",
          "words": {
            "正面回答": [
              "they're very different",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "play basketball",
              "volleyball",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "go jogging",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "meet like-minded people",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "I prefer A. As for the first side, it is regarded as stronger because of play basketball and volleyball. By contrast, regarding the other side, people find it different due to go jogging and by contrast. Overall, I find meet like-minded people more suitable, which I prefer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 21,
          "title": "Did you prefer to do activities alone or with a group of people when ...",
          "q": "Did you prefer to do activities alone or with a group of people when you were a child?",
          "topicEn": "Childhood activities",
          "topicZh": "童年活动",
          "tag": "沿用",
          "recentCount": 994,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近994人】对比：两边各说特点再表态；童年活动=play outside / with friends，现在对比更 indoor。 本题按「对比类」四步答；素材：童年活动=play outside / with friends，现在对比更 indoor。。",
          "logic": "对比：两边各说特点再表态；童年活动=play outside / with friends，现在对比更 indoor。",
          "material": "童年活动=play outside / with friends，现在对比更 indoor。",
          "words": {
            "正面回答": [
              "with a group of people",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "play video games",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "me-time",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "have a good laugh",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer playing video games when I need a good laugh with friends. Quiet me-time is also valuable, but games help me unwind faster after a stressful day.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 22,
          "title": "Are there any differences between the activities you liked when you w...",
          "q": "Are there any differences between the activities you liked when you were a child and those you like now?",
          "topicEn": "Childhood activities",
          "topicZh": "童年活动",
          "tag": "沿用",
          "recentCount": 994,
          "heatRank": 16,
          "tip": "【沿用·热度#16·近994人】对比：童年户外 vs 现在室内/手机。 本题按「对比类」四步答；素材：童年活动=play outside / with friends，现在对比更 indoor。。",
          "logic": "对比：童年户外 vs 现在室内/手机。",
          "material": "童年活动=play outside / with friends，现在对比更 indoor。",
          "words": {
            "正面回答": [
              "Yes",
              "quite different",
              "totally different",
              "Somewhat different"
            ],
            "选项1的特点与作用": [
              "play outside as a kid",
              "more screen time now",
              "different interests"
            ],
            "选项2的特点与作用": [
              "childhood was outdoors",
              "toys and games",
              "with neighbourhood friends"
            ],
            "个人感受": [
              "natural shift",
              "still enjoy active things",
              "life changes interests"
            ]
          },
          "frames": {
            "1": {
              "name": "过去时 When I was...",
              "pattern": "When I was a child / little, I ______.",
              "tip": "第2步：童年题用过去时，别套 Whenever"
            },
            "2": {
              "name": "Back then / At that time",
              "pattern": "Back then / At that time, I ______.",
              "tip": "第3步：承接童年时间线"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "Yes, definitely. As for the first side, it is regarded as stronger because of play outside as a kid and more screen time now. By contrast, regarding the other side, people find it different due to childhood was outdoors and toys and games. Overall, I find natural shift more suitable, which still enjoy active things.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "explicit"
        },
        {
          "id": 23,
          "title": "Do you prefer to read on paper or on a screen",
          "q": "Do you prefer to read on paper or on a screen?",
          "topicEn": "Reading",
          "topicZh": "阅读",
          "tag": "沿用",
          "recentCount": 875,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近875人】对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。 本题按「对比类」四步答；素材：阅读=read books / flip through pages，纸质 vs 屏幕对比。。",
          "logic": "对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "material": "阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "words": {
            "正面回答": [
              "I prefer reading on paper",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "flip through physical books",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "spend a lot of time on my phone",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "reflect on things",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer reading on paper because flipping through physical books helps me reflect. Spending a lot of time on my phone is convenient, but paper reading feels deeper and calmer.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 24,
          "title": "When do you need to read carefully, and when not",
          "q": "When do you need to read carefully, and when not?",
          "topicEn": "Reading",
          "topicZh": "阅读",
          "tag": "沿用",
          "recentCount": 875,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近875人】对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。 本题按「对比类」四步答；素材：阅读=read books / flip through pages，纸质 vs 屏幕对比。。",
          "logic": "对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "material": "阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "words": {
            "正面回答": [
              "it depends on what I am reading",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "study",
              "library",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "watch short videos",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "finish homework on my own",
              "practical",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I find + 句型4 which",
              "pattern": "I find ______ more ______, which ______.",
              "tip": "第4步：个人偏好 + which 补一句理由"
            }
          },
          "sample": "It depends on what I am reading. As for the first side, it is regarded as stronger because of study and library. By contrast, regarding the other side, people find it different due to watch short videos and by contrast. Overall, I find finish homework on my own more suitable, which practical.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 25,
          "title": "Do you prefer scanning or detailed reading",
          "q": "Do you prefer scanning or detailed reading?",
          "topicEn": "Reading",
          "topicZh": "阅读",
          "tag": "沿用",
          "recentCount": 875,
          "heatRank": 17,
          "tip": "【沿用·热度#17·近875人】对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。 本题按「对比类」四步答；素材：阅读=read books / flip through pages，纸质 vs 屏幕对比。。",
          "logic": "对比：两边各说特点再表态；阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "material": "阅读=read books / flip through pages，纸质 vs 屏幕对比。",
          "words": {
            "正面回答": [
              "detailed reading",
              "mostly",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "physical books",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "takeout",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "work hard at my studies",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer physical books when I study hard. Takeout is convenient on busy nights, but books keep me focused better than eating while scrolling.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        },
        {
          "id": 26,
          "title": "Do you prefer the mountains or the sea",
          "q": "Do you prefer the mountains or the sea?",
          "topicEn": "Scenery",
          "topicZh": "景色",
          "tag": "沿用",
          "recentCount": 777,
          "heatRank": 18,
          "tip": "【沿用·热度#18·近777人】对比：两边各说特点再表态；景色=travel + take photos，山/海对比用 mountains vs sea。 本题按「对比类」四步答；素材：景色=travel + take photos，山/海对比用 mountains vs sea。。",
          "logic": "对比：两边各说特点再表态；景色=travel + take photos，山/海对比用 mountains vs sea。",
          "material": "景色=travel + take photos，山/海对比用 mountains vs sea。",
          "words": {
            "正面回答": [
              "definitely the sea",
              "I prefer A",
              "I'd rather",
              "it depends on the person"
            ],
            "选项1的特点与作用": [
              "enjoy tasty local food",
              "is regarded as",
              "more convenient",
              "less stressful"
            ],
            "选项2的特点与作用": [
              "hiking",
              "by contrast",
              "on the other hand",
              "find it harder"
            ],
            "个人感受": [
              "unwind",
              "I prefer",
              "which is why",
              "more comfortable"
            ]
          },
          "frames": {
            "1": {
              "name": "句型7 regarded as + 句型5 to do",
              "pattern": "As for A, ______ is regarded as ______ to ______.",
              "tip": "第2步：选项1用被动 + 目的状语写特点与作用"
            },
            "2": {
              "name": "句型1B find it + adj. + to do",
              "pattern": "By contrast, regarding B, they find it ______ to ______.",
              "tip": "第3步：选项2用形式宾语对比难点/偏好"
            },
            "3": {
              "name": "句型2 I prefer + 句型4 which",
              "pattern": "I prefer ______, which ______.",
              "tip": "第4步：对比收束用 prefer + which 给理由"
            }
          },
          "sample": "I prefer enjoying tasty local food to unwind, though hiking is a healthier option. After a long week, good food helps me relax more quickly.",
          "sampleOk": true,
          "sampleNote": "ok",
          "sampleSource": "template",
          "wordSource": "clue"
        }
      ]
    }
  ]
};
