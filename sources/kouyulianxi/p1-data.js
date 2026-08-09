// P1 data - 全库按题面逻辑裁剪词块
const P1_DATA = {
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
          "title": "Have you ever had a pet before",
          "q": "Have you ever had a pet before?",
          "clueId": "1",
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
              "park"
            ],
            "感受": [
              "unwind",
              "really lifts my mood"
            ]
          }
        },
        {
          "id": 2,
          "title": "Have you ever been part of a sports team",
          "q": "Have you ever been part of a sports team?",
          "clueId": "2",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "来源或举例": [
              "play basketball",
              "volleyball in the sports centre"
            ],
            "频次": [
              "at weekends",
              "in my free time"
            ],
            "感受": [
              "sense of teamwork",
              "practical"
            ]
          }
        },
        {
          "id": 3,
          "title": "Have you ever sent handmade gifts to others",
          "q": "Have you ever sent handmade gifts to others?",
          "clueId": "3",
          "words": {
            "正面回答": [
              "Exactly"
            ],
            "来源或举例": [
              "a t-shirt",
              "coat"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "it makes me happy"
            ]
          }
        },
        {
          "id": 4,
          "title": "Have you ever received a great gift",
          "q": "Have you ever received a great gift?",
          "clueId": "3",
          "words": {
            "正面回答": [
              "Exactly",
              "just last month"
            ],
            "来源或举例": [
              "a t-shirt",
              "coat"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "it makes me happy"
            ]
          }
        },
        {
          "id": 5,
          "title": "What gift have you received recently",
          "q": "What gift have you received recently?",
          "clueId": "3",
          "words": {
            "正面回答": [
              "just last month"
            ],
            "来源或举例": [
              "a t-shirt",
              "coat"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "it makes me happy"
            ]
          }
        },
        {
          "id": 6,
          "title": "Where did you go for a walk lately",
          "q": "Where did you go for a walk lately?",
          "clueId": "4",
          "words": {
            "正面回答": [
              "Recently",
              "just a few days ago"
            ],
            "来源或举例": [
              "the local park",
              "city centre"
            ],
            "频次": [
              "after dinner",
              "feel bored"
            ],
            "感受": [
              "feel relaxed and at ease",
              "relax my mind"
            ]
          }
        },
        {
          "id": 7,
          "title": "When did you learn how to type on a keyboard",
          "q": "When did you learn how to type on a keyboard?",
          "clueId": "5",
          "words": {
            "正面回答": [
              "In my childhood",
              "in primary school"
            ],
            "来源或举例": [
              "shop online",
              "play video games"
            ],
            "频次": [
              "regularly",
              "as often as I can"
            ],
            "感受": [
              "practical",
              "time-saving"
            ]
          }
        },
        {
          "id": 8,
          "title": "How do you improve your typing",
          "q": "How do you improve your typing?",
          "clueId": "5",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "shop online",
              "play video games"
            ],
            "频次": [
              "regularly",
              "as often as I can"
            ],
            "感受": [
              "practical",
              "time-saving"
            ]
          }
        },
        {
          "id": 9,
          "title": "What are the most beautiful sights you have seen while traveling",
          "q": "What are the most beautiful sights you have seen while traveling?",
          "clueId": "6",
          "words": {
            "正面回答": [
              "To be honest",
              "the seaside"
            ],
            "来源或举例": [
              "take photos of the stunning views"
            ],
            "频次": [
              "during holidays",
              "when I have days off"
            ],
            "感受": [
              "It's something I'll never forget"
            ]
          }
        },
        {
          "id": 10,
          "title": "Are there tall buildings near your home",
          "q": "Are there tall buildings near your home?",
          "clueId": "7",
          "words": {
            "正面回答": [
              "Yes",
              "lots of them"
            ],
            "来源或举例": [
              "shopping malls and hotels"
            ],
            "频次": [
              "go there regularly",
              "in my free time"
            ],
            "感受": [
              "super convenient",
              "practical"
            ]
          }
        },
        {
          "id": 11,
          "title": "What plant did you grow when you were young",
          "q": "What plant did you grow when you were young?",
          "clueId": "8",
          "words": {
            "正面回答": [
              "Actually yes"
            ],
            "来源或举例": [
              "some flowers on my balcony",
              "bought from street market"
            ],
            "频次": [
              "water them every day"
            ],
            "感受": [
              "gives me a chance to reflect on things"
            ]
          }
        },
        {
          "id": 12,
          "title": "Do you know anything about growing a plant",
          "q": "Do you know anything about growing a plant?",
          "clueId": "8",
          "words": {
            "正面回答": [
              "Actually yes"
            ],
            "来源或举例": [
              "some flowers on my balcony",
              "bought from street market"
            ],
            "频次": [],
            "感受": [
              "gives me a chance to reflect on things"
            ]
          }
        },
        {
          "id": 13,
          "title": "Have you ever talked with someone you don't know in public places",
          "q": "Have you ever talked with someone you don't know in public places?",
          "clueId": "9",
          "words": {
            "正面回答": [
              "Occasionally",
              "yes"
            ],
            "来源或举例": [
              "in the cafes",
              "library"
            ],
            "频次": [
              "seldom",
              "just from time to time"
            ],
            "感受": [
              "good chance to have a conversation",
              "share opinions"
            ]
          }
        },
        {
          "id": 14,
          "title": "Are there any rules for students at your school",
          "q": "Are there any rules for students at your school?",
          "clueId": "10",
          "words": {
            "正面回答": [
              "Definitely",
              "a lot of rules"
            ],
            "来源或举例": [
              "no phones in the classroom"
            ],
            "频次": [
              "we have to follow them daily"
            ],
            "感受": [
              "forces me to work hard at my studies"
            ]
          }
        },
        {
          "id": 15,
          "title": "Have you ever had a really dedicated teacher",
          "q": "Have you ever had a really dedicated teacher?",
          "clueId": "10",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "来源或举例": [
              "complete homework independently"
            ],
            "频次": [],
            "感受": [
              "forces me to work hard at my studies",
              "complete homework independently"
            ]
          }
        },
        {
          "id": 16,
          "title": "Have you ever had a really strict teacher",
          "q": "Have you ever had a really strict teacher?",
          "clueId": "10",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "来源或举例": [
              "complete homework independently"
            ],
            "频次": [],
            "感受": [
              "forces me to work hard at my studies",
              "complete homework independently"
            ]
          }
        },
        {
          "id": 17,
          "title": "Have you ever bought shoes online",
          "q": "Have you ever bought shoes online?",
          "clueId": "11",
          "words": {
            "正面回答": [
              "Absolutely"
            ],
            "来源或举例": [
              "shop online",
              "browse websites"
            ],
            "频次": [
              "regularly",
              "whenever I need"
            ],
            "感受": [
              "practical",
              "cheap and handy"
            ]
          }
        },
        {
          "id": 18,
          "title": "Do you have an experience when you did something well",
          "q": "Do you have an experience when you did something well?",
          "clueId": "12",
          "words": {
            "正面回答": [
              "Yes",
              "I have an impressive memory"
            ],
            "来源或举例": [
              "complete homework independently",
              "pass an exam"
            ],
            "频次": [
              "last semester"
            ],
            "感受": [
              "made me feel self-driven",
              "a sense of achievement"
            ]
          }
        },
        {
          "id": 19,
          "title": "Do you have an experience when your teacher thought you did a good job",
          "q": "Do you have an experience when your teacher thought you did a good job?",
          "clueId": "12",
          "words": {
            "正面回答": [
              "Yes",
              "I have an impressive memory"
            ],
            "来源或举例": [
              "complete homework independently",
              "pass an exam"
            ],
            "频次": [
              "last semester"
            ],
            "感受": [
              "made me feel self-driven",
              "a sense of achievement"
            ]
          }
        },
        {
          "id": 20,
          "title": "Is the city where you live crowded",
          "q": "Is the city where you live crowded?",
          "clueId": "13",
          "words": {
            "正面回答": [
              "Honestly",
              "yes"
            ],
            "来源或举例": [
              "the city centre",
              "use the subway in rush hour"
            ],
            "频次": [
              "every single day"
            ],
            "感受": [
              "it bothers me",
              "feel terrible"
            ]
          }
        },
        {
          "id": 21,
          "title": "Is there a crowded place near where you live",
          "q": "Is there a crowded place near where you live?",
          "clueId": "13",
          "words": {
            "正面回答": [
              "Honestly",
              "yes"
            ],
            "来源或举例": [
              "the city centre",
              "use the subway in rush hour"
            ],
            "频次": [
              "every single day"
            ],
            "感受": [
              "it bothers me",
              "feel terrible"
            ]
          }
        },
        {
          "id": 22,
          "title": "When was the last time you were in a crowded place",
          "q": "When was the last time you were in a crowded place?",
          "clueId": "13",
          "words": {
            "正面回答": [
              "the city centre"
            ],
            "来源或举例": [
              "the city centre",
              "use the subway in rush hour"
            ],
            "频次": [],
            "感受": [
              "it bothers me",
              "feel terrible"
            ]
          }
        },
        {
          "id": 23,
          "title": "Have you ever worked with old people",
          "q": "Have you ever worked with old people?",
          "clueId": "14",
          "words": {
            "正面回答": [
              "Yes",
              "in a community event"
            ],
            "来源或举例": [
              "have a conversation",
              "have a chat with them"
            ],
            "频次": [
              "when I started university"
            ],
            "感受": [
              "great chance to share experiences",
              "learn from them"
            ]
          }
        },
        {
          "id": 24,
          "title": "Do many people grow vegetables in your city",
          "q": "Do many people grow vegetables in your city?",
          "clueId": "15",
          "words": {
            "正面回答": [
              "Not really"
            ],
            "来源或举例": [
              "people live in high-rise residential areas",
              "apartments"
            ],
            "频次": [
              "rarely see it"
            ],
            "感受": [
              "we usually buy groceries",
              "food ingredients instead"
            ]
          }
        },
        {
          "id": 25,
          "title": "Have you borrowed books from others",
          "q": "Have you borrowed books from others?",
          "clueId": "16",
          "words": {
            "正面回答": [
              "Yes",
              "exactly"
            ],
            "来源或举例": [
              "borrowed real books from friends in dorms"
            ],
            "频次": [
              "whenever necessary"
            ],
            "感受": [
              "shows altruistic behaviour",
              "mutual help"
            ]
          }
        },
        {
          "id": 26,
          "title": "Have you borrowed money from others",
          "q": "Have you borrowed money from others?",
          "clueId": "16",
          "words": {
            "正面回答": [
              "Yes",
              "exactly"
            ],
            "来源或举例": [
              "from friends in dorms"
            ],
            "频次": [
              "whenever necessary"
            ],
            "感受": [
              "shows altruistic behaviour",
              "mutual help"
            ]
          }
        },
        {
          "id": 27,
          "title": "Is there an advertisement that made an impression on you when you were a child",
          "q": "Is there an advertisement that made an impression on you when you were a child?",
          "clueId": "17",
          "words": {
            "正面回答": [
              "Yes",
              "one deeply impressed me"
            ],
            "来源或举例": [
              "saw it when I watch movies"
            ],
            "频次": [
              "childhood",
              "before I went to primary school"
            ],
            "感受": [
              "it makes me happy",
              "interesting"
            ]
          }
        },
        {
          "id": 28,
          "title": "Are there many museums in your hometown",
          "q": "Are there many museums in your hometown?",
          "clueId": "18",
          "words": {
            "正面回答": [
              "Yes",
              "quite a few"
            ],
            "来源或举例": [
              "located in the city centre"
            ],
            "频次": [
              "in my free time"
            ],
            "感受": [
              "helps me to slow down and learn history"
            ]
          }
        },
        {
          "id": 29,
          "title": "When was the last time you visited a museum",
          "q": "When was the last time you visited a museum?",
          "clueId": "18",
          "words": {
            "正面回答": [
              "recently"
            ],
            "来源或举例": [
              "located in the city centre"
            ],
            "频次": [
              "in my free time"
            ],
            "感受": [
              "helps me to slow down and learn history"
            ]
          }
        },
        {
          "id": 30,
          "title": "Did your parents teach you to share when you were a child",
          "q": "Did your parents teach you to share when you were a child?",
          "clueId": "19",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "来源或举例": [
              "share a meal",
              "share thoughts and feelings with friends"
            ],
            "频次": [
              "regularly",
              "all the time"
            ],
            "感受": [
              "good for mental self-care"
            ]
          }
        },
        {
          "id": 31,
          "title": "Do you have anything to share with others recently",
          "q": "Do you have anything to share with others recently?",
          "clueId": "19",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "来源或举例": [
              "share a meal",
              "share thoughts and feelings with friends"
            ],
            "频次": [
              "regularly"
            ],
            "感受": [
              "good for mental self-care"
            ]
          }
        },
        {
          "id": 32,
          "title": "What subjects are you studying",
          "q": "What subjects are you studying?",
          "clueId": "20",
          "words": {
            "正面回答": [
              "I am a student majoring in"
            ],
            "来源或举例": [
              "Study",
              "go to classes",
              "listen to a lecture"
            ],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 33,
          "title": "What work do you do",
          "q": "What work do you do?",
          "clueId": "20",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 34,
          "title": "What requirements did you need to meet to get your current job",
          "q": "What requirements did you need to meet to get your current job?",
          "clueId": "20",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 35,
          "title": "Why did you choose to study that subject",
          "q": "Why did you choose to study that subject?",
          "clueId": "20",
          "words": {
            "正面回答": [
              "I am a student majoring in"
            ],
            "来源或举例": [
              "Study",
              "go to classes",
              "listen to a lecture"
            ],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 36,
          "title": "Why did you choose to do that type of work",
          "q": "Why did you choose to do that type of work?",
          "clueId": "20",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 37,
          "title": "Do you have any plans for your studies in the next five years",
          "q": "Do you have any plans for your studies in the next five years?",
          "clueId": "20",
          "words": {
            "正面回答": [
              "I am a student majoring in"
            ],
            "来源或举例": [
              "Study",
              "go to classes",
              "listen to a lecture"
            ],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 38,
          "title": "Do you have any plans for your work in the next five years",
          "q": "Do you have any plans for your work in the next five years?",
          "clueId": "20",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "every weekday"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 39,
          "title": "Who helps you the most? And how",
          "q": "Who helps you the most? And how?",
          "clueId": "20",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [],
            "感受": []
          }
        },
        {
          "id": 40,
          "title": "Are the transport facilities to your home very good",
          "q": "Are the transport facilities to your home very good?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 41,
          "title": "Please describe the room you live in.",
          "q": "Please describe the room you live in.",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 42,
          "title": "Can you describe the place where you live",
          "q": "Can you describe the place where you live?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 43,
          "title": "How long have you lived there",
          "q": "How long have you lived there?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 44,
          "title": "Who do you live with",
          "q": "Who do you live with?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 45,
          "title": "What kinds of accommodation do you live in",
          "q": "What kinds of accommodation do you live in?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 46,
          "title": "Where is your hometown",
          "q": "Where is your hometown?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 47,
          "title": "Is that a big city or a small place",
          "q": "Is that a big city or a small place?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 48,
          "title": "Please describe your hometown a little.",
          "q": "Please describe your hometown a little.",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 49,
          "title": "How long have you been living there",
          "q": "How long have you been living there?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 50,
          "title": "What's your hometown famous for",
          "q": "What's your hometown famous for?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 51,
          "title": "Did you learn about the history of your hometown at school",
          "q": "Did you learn about the history of your hometown at school?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 52,
          "title": "Did you learn about the culture of your hometown at school",
          "q": "Did you learn about the culture of your hometown at school?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 53,
          "title": "Did you learn about the history of your hometown in childhood",
          "q": "Did you learn about the history of your hometown in childhood?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 54,
          "title": "Did you learn about the culture of your hometown in childhood",
          "q": "Did you learn about the culture of your hometown in childhood?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 55,
          "title": "Are there many young people in your hometown",
          "q": "Are there many young people in your hometown?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 56,
          "title": "Do you know any famous people in your area",
          "q": "Do you know any famous people in your area?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 57,
          "title": "What are some changes in the area recently",
          "q": "What are some changes in the area recently?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 58,
          "title": "Do you know any of your neighbors",
          "q": "Do you know any of your neighbors?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 59,
          "title": "Are the people in your neighborhood nice and friendly",
          "q": "Are the people in your neighborhood nice and friendly?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 60,
          "title": "Do you live in a noisy or a quiet area",
          "q": "Do you live in a noisy or a quiet area?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 61,
          "title": "What city do you live in",
          "q": "What city do you live in?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 62,
          "title": "How long have you lived in this city",
          "q": "How long have you lived in this city?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 63,
          "title": "Is this city your permanent residence",
          "q": "Is this city your permanent residence?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 64,
          "title": "Are there big changes in this city",
          "q": "Are there big changes in this city?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [
              "surrounded by convenience stores",
              "shopping malls",
              "easy to use the subway"
            ],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 65,
          "title": "Are there people of different ages living in this city",
          "q": "Are there people of different ages living in this city?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 66,
          "title": "Are the people friendly in the city",
          "q": "Are the people friendly in the city?",
          "clueId": "21",
          "words": {
            "正面回答": [
              "I live in a big city",
              "have lived here since childhood"
            ],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 67,
          "title": "What's the weather like where you live",
          "q": "What's the weather like where you live?",
          "clueId": "21",
          "words": {
            "正面回答": [],
            "来源或举例": [],
            "频次": [
              "in my daily life"
            ],
            "感受": [
              "feel relaxed and at ease",
              "nice place to sit down and relax"
            ]
          }
        },
        {
          "id": 68,
          "title": "When was the last time you had a few days off",
          "q": "When was the last time you had a few days off?",
          "clueId": "22",
          "words": {
            "正面回答": [
              "Just last month"
            ],
            "来源或举例": [
              "binge-watch TV shows",
              "have some me time at home"
            ],
            "频次": [
              "rarely get the chance"
            ],
            "感受": [
              "relax my mind",
              "take a break and relax"
            ]
          }
        },
        {
          "id": 69,
          "title": "Can you remember the dreams you had",
          "q": "Can you remember the dreams you had?",
          "clueId": "23",
          "words": {
            "正面回答": [
              "Yes",
              "sometimes I do"
            ],
            "来源或举例": [
              "usually recall them right after I get up"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "I don't know how to explain it",
              "but it's fascinating"
            ]
          }
        },
        {
          "id": 70,
          "title": "Have you ever lost your keys",
          "q": "Have you ever lost your keys?",
          "clueId": "24",
          "words": {
            "正面回答": [
              "Unfortunately",
              "yes"
            ],
            "来源或举例": [
              "when I tried to grab my stuff",
              "before I go out"
            ],
            "频次": [
              "only once or twice"
            ],
            "感受": [
              "it bothers me a lot",
              "taught me to be careful"
            ]
          }
        },
        {
          "id": 71,
          "title": "What did you often do with your friends in your childhood",
          "q": "What did you often do with your friends in your childhood?",
          "clueId": "m1",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "play video games"
            ],
            "频次": [
              "regularly"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 72,
          "title": "Do you have any plans for the next five years",
          "q": "Do you have any plans for the next five years?",
          "clueId": "m2",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "work hard at my studies"
            ],
            "频次": [
              "every day"
            ],
            "感受": [
              "practical"
            ]
          }
        },
        {
          "id": 73,
          "title": "What are examples of good and poor phone manners",
          "q": "What are examples of good and poor phone manners?",
          "clueId": "m3",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "have a chat"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "bothers me"
            ]
          }
        },
        {
          "id": 74,
          "title": "What kind of music events are there in your country",
          "q": "What kind of music events are there in your country?",
          "clueId": "m4",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "listen to music"
            ],
            "频次": [
              "at weekends"
            ],
            "感受": [
              "relax"
            ]
          }
        },
        {
          "id": 75,
          "title": "What short-term jobs do young people do in other countries",
          "q": "What short-term jobs do young people do in other countries?",
          "clueId": "m5",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "eat out"
            ],
            "频次": [
              "during holidays"
            ],
            "感受": [
              "practical"
            ]
          }
        },
        {
          "id": 76,
          "title": "What kind of things are people happy to pay a high price for",
          "q": "What kind of things are people happy to pay a high price for?",
          "clueId": "m6",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "clothes",
              "coat"
            ],
            "频次": [
              "from time to time"
            ],
            "感受": [
              "makes me happy"
            ]
          }
        },
        {
          "id": 77,
          "title": "What challenges do young people face when working abroad",
          "q": "What challenges do young people face when working abroad?",
          "clueId": "m7",
          "words": {
            "正面回答": [],
            "来源或举例": [
              "renting an apartment"
            ],
            "频次": [
              "every day"
            ],
            "感受": [
              "pressure",
              "bothers me"
            ]
          }
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
          "title": "What is your favourite food",
          "q": "What is your favourite food?",
          "words": {
            "正面回答": [
              "I am a big fan of"
            ],
            "原因或时间": [
              "delicious",
              "mouth-watering sweet treats"
            ],
            "频次": [
              "order takeaways"
            ],
            "感受": [
              "satisfy my taste buds"
            ]
          }
        },
        {
          "id": 2,
          "title": "What kind of food did you like when you were young",
          "q": "What kind of food did you like when you were young?",
          "words": {
            "正面回答": [
              "I enjoyed sweet food"
            ],
            "原因或时间": [
              "childhood",
              "before I went to primary school"
            ],
            "频次": [
              "eat breakfast with cakes"
            ],
            "感受": [
              "it makes me happy",
              "have a blast"
            ]
          }
        },
        {
          "id": 3,
          "title": "What's your favourite animal? Why",
          "q": "What's your favourite animal? Why?",
          "words": {
            "正面回答": [
              "I'm quite fond of dogs"
            ],
            "原因或时间": [
              "they are loyal"
            ],
            "频次": [
              "stay at home with me"
            ],
            "感受": [
              "a great stress buster",
              "unwind"
            ]
          }
        },
        {
          "id": 4,
          "title": "Do you like watching team games? Why",
          "q": "Do you like watching team games? Why?",
          "words": {
            "正面回答": [
              "I am keen on them"
            ],
            "原因或时间": [
              "in my free time",
              "when I have time for myself"
            ],
            "频次": [
              "watch basketball",
              "volleyball games"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 5,
          "title": "Do you have any hobbies",
          "q": "Do you have any hobbies?",
          "words": {
            "正面回答": [
              "I have quite a few"
            ],
            "原因或时间": [
              "at weekends"
            ],
            "频次": [
              "binge-watch TV shows"
            ],
            "感受": [
              "sit down and relax"
            ]
          }
        },
        {
          "id": 6,
          "title": "Did you have any hobbies when you were a child",
          "q": "Did you have any hobbies when you were a child?",
          "words": {
            "正面回答": [
              "Absolutely"
            ],
            "原因或时间": [
              "before I went to primary school"
            ],
            "频次": [
              "play video games"
            ],
            "感受": [
              "super amusing",
              "have a blast"
            ]
          }
        },
        {
          "id": 7,
          "title": "Do you have a hobby that you've had since childhood",
          "q": "Do you have a hobby that you've had since childhood?",
          "words": {
            "正面回答": [
              "Exactly"
            ],
            "原因或时间": [
              "before I go to sleep"
            ],
            "频次": [
              "flip through the pages of real books"
            ],
            "感受": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 8,
          "title": "Do you have the same hobbies as your family members",
          "q": "Do you have the same hobbies as your family members?",
          "words": {
            "正面回答": [
              "Yes",
              "we share some"
            ],
            "原因或时间": [
              "during holidays"
            ],
            "频次": [
              "eat out in a restaurant"
            ],
            "感受": [
              "share thoughts and feelings"
            ]
          }
        },
        {
          "id": 9,
          "title": "Do you like getting up early in the morning",
          "q": "Do you like getting up early in the morning?",
          "words": {
            "正面回答": [
              "Honestly",
              "yes"
            ],
            "原因或时间": [
              "the first thing I do after I get up"
            ],
            "频次": [
              "go jogging"
            ],
            "感受": [
              "energetic",
              "full of beans"
            ]
          }
        },
        {
          "id": 10,
          "title": "Do you like reading",
          "q": "Do you like reading?",
          "words": {
            "正面回答": [
              "I am passionate about reading"
            ],
            "原因或时间": [
              "when I feel bored"
            ],
            "频次": [
              "read books in the library"
            ],
            "感受": [
              "chill out",
              "feel peaceful"
            ]
          }
        },
        {
          "id": 11,
          "title": "Where would you like to take a long walk if you had the chance",
          "q": "Where would you like to take a long walk if you had the chance?",
          "words": {
            "正面回答": [
              "the local park"
            ],
            "原因或时间": [
              "when the weather is nice"
            ],
            "频次": [
              "go for a walk"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 12,
          "title": "Do you like to take scenery pictures",
          "q": "Do you like to take scenery pictures?",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "原因或时间": [
              "record my life"
            ],
            "频次": [
              "take photos outdoors"
            ],
            "感受": [
              "It's something I'll never forget"
            ]
          }
        },
        {
          "id": 13,
          "title": "Do you like taking pictures of different views",
          "q": "Do you like taking pictures of different views?",
          "words": {
            "正面回答": [
              "I'm crazy about it"
            ],
            "原因或时间": [
              "when traveling",
              "on vacations"
            ],
            "频次": [
              "city centre and nature"
            ],
            "感受": [
              "reduce stress"
            ]
          }
        },
        {
          "id": 14,
          "title": "Is there a building that you would like to visit",
          "q": "Is there a building that you would like to visit?",
          "words": {
            "正面回答": [
              "Yes",
              "there is one"
            ],
            "原因或时间": [
              "unique design"
            ],
            "频次": [
              "cafes"
            ],
            "感受": [
              "meet people with similar interests"
            ]
          }
        },
        {
          "id": 15,
          "title": "What were your favourite activities when you were a child",
          "q": "What were your favourite activities when you were a child?",
          "words": {
            "正面回答": [
              "One of my favourite things to do as a child was"
            ],
            "原因或时间": [
              "outside the classroom"
            ],
            "频次": [
              "hang out with friends"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 16,
          "title": "Would you like to see more public places near where you live",
          "q": "Would you like to see more public places near where you live?",
          "words": {
            "正面回答": [
              "Yes",
              "absolutely"
            ],
            "原因或时间": [
              "convenient for gatherings"
            ],
            "频次": [
              "shopping malls"
            ],
            "感受": [
              "very practical"
            ]
          }
        },
        {
          "id": 17,
          "title": "Would you like to work as a teacher in a rule-free school",
          "q": "Would you like to work as a teacher in a rule-free school?",
          "words": {
            "正面回答": [
              "I'd love to"
            ],
            "原因或时间": [
              "free atmosphere"
            ],
            "频次": [
              "share opinions outside the classroom"
            ],
            "感受": [
              "be more self-driven"
            ]
          }
        },
        {
          "id": 18,
          "title": "Do you like buying shoes? How often",
          "q": "Do you like buying shoes? How often?",
          "words": {
            "正面回答": [
              "Yes",
              "I am a big fan"
            ],
            "原因或时间": [
              "when I get dressed"
            ],
            "频次": [
              "shop online regularly"
            ],
            "感受": [
              "it really lifts my mood"
            ]
          }
        },
        {
          "id": 19,
          "title": "Do you like crowded places",
          "q": "Do you like crowded places?",
          "words": {
            "正面回答": [
              "To be honest",
              "no"
            ],
            "原因或时间": [
              "especially in rush hour"
            ],
            "频次": [
              "use the subway"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 20,
          "title": "Are you happy to work with people who are older than you",
          "q": "Are you happy to work with people who are older than you?",
          "words": {
            "正面回答": [
              "Yes",
              "I am happy to"
            ],
            "原因或时间": [
              "they have rich experience"
            ],
            "频次": [
              "have a conversation"
            ],
            "感受": [
              "it could be useful for my future job"
            ]
          }
        },
        {
          "id": 21,
          "title": "Do you enjoy spending time with old people",
          "q": "Do you enjoy spending time with old people?",
          "words": {
            "正面回答": [
              "Definitely enjoy it"
            ],
            "原因或时间": [
              "in my spare time"
            ],
            "频次": [
              "share experiences"
            ],
            "感受": [
              "feel appreciated"
            ]
          }
        },
        {
          "id": 22,
          "title": "Are you interested in growing vegetables and fruits",
          "q": "Are you interested in growing vegetables and fruits?",
          "words": {
            "正面回答": [
              "Quite interested"
            ],
            "原因或时间": [
              "when I'm not studying"
            ],
            "频次": [
              "groceries",
              "food ingredients"
            ],
            "感受": [
              "a nice way to sit down and relax"
            ]
          }
        },
        {
          "id": 23,
          "title": "Do you like chatting with friends",
          "q": "Do you like chatting with friends?",
          "words": {
            "正面回答": [
              "It's my top choice"
            ],
            "原因或时间": [
              "at weekends"
            ],
            "频次": [
              "have a chat in cafes"
            ],
            "感受": [
              "mutually motivate each other"
            ]
          }
        },
        {
          "id": 24,
          "title": "Do you like to lend things to others",
          "q": "Do you like to lend things to others?",
          "words": {
            "正面回答": [
              "I don't mind"
            ],
            "原因或时间": [
              "in daily life"
            ],
            "频次": [
              "lend real books"
            ],
            "感受": [
              "shows altruistic behaviour"
            ]
          }
        },
        {
          "id": 25,
          "title": "Do you mind if others borrow money from you",
          "q": "Do you mind if others borrow money from you?",
          "words": {
            "正面回答": [
              "Honestly",
              "yes"
            ],
            "原因或时间": [
              "it's complicated"
            ],
            "频次": [
              "hard to grab my stuff back"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 26,
          "title": "Do you like advertisements",
          "q": "Do you like advertisements?",
          "words": {
            "正面回答": [
              "It depends on the situation"
            ],
            "原因或时间": [
              "when I browse videos"
            ],
            "频次": [
              "creative ads"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 27,
          "title": "What kind of advertising do you like",
          "q": "What kind of advertising do you like?",
          "words": {
            "正面回答": [
              "Humorous ones"
            ],
            "原因或时间": [
              "when I watch movies"
            ],
            "频次": [
              "ads placement"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 28,
          "title": "What kind of things do you like to share with others",
          "q": "What kind of things do you like to share with others?",
          "words": {
            "正面回答": [
              "I like to share a meal"
            ],
            "原因或时间": [
              "when I go to parties"
            ],
            "频次": [
              "pig out on tasty local food"
            ],
            "感受": [
              "meet people with similar interests"
            ]
          }
        },
        {
          "id": 29,
          "title": "Who is the first person you would like to share good news with",
          "q": "Who is the first person you would like to share good news with?",
          "words": {
            "正面回答": [
              "my homie",
              "besties"
            ],
            "原因或时间": [
              "whenever I get news"
            ],
            "频次": [
              "share thoughts and feelings on WeChat"
            ],
            "感受": [
              "it really lifts my mood"
            ]
          }
        },
        {
          "id": 30,
          "title": "Do you like your subject",
          "q": "Do you like your subject?",
          "words": {
            "正面回答": [
              "I'm passionate about it"
            ],
            "原因或时间": [
              "very practical"
            ],
            "频次": [
              "go to classes",
              "listen to a lecture"
            ],
            "感受": [
              "self-driven",
              "work hard at my studies"
            ]
          }
        },
        {
          "id": 31,
          "title": "Do you want to change your major",
          "q": "Do you want to change your major?",
          "words": {
            "正面回答": [
              "Absolutely not"
            ],
            "原因或时间": [
              "feel passionate about it"
            ],
            "频次": [
              "go to the library to study"
            ],
            "感受": []
          }
        },
        {
          "id": 32,
          "title": "Are you looking forward to working",
          "q": "Are you looking forward to working?",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "原因或时间": [
              "after graduation"
            ],
            "频次": [
              "no longer rely on parents"
            ],
            "感受": [
              "take action and be independent"
            ]
          }
        },
        {
          "id": 33,
          "title": "Do you like your job",
          "q": "Do you like your job?",
          "words": {
            "正面回答": [
              "Yes",
              "I do"
            ],
            "原因或时间": [
              "good atmosphere"
            ],
            "频次": [
              "share opinions"
            ],
            "感受": [
              "very practical and fulfilling"
            ]
          }
        },
        {
          "id": 34,
          "title": "Do you want to change to another job",
          "q": "Do you want to change to another job?",
          "words": {
            "正面回答": [
              "Not at the moment"
            ],
            "原因或时间": [
              "at this stage"
            ],
            "频次": [
              "focus on current tasks"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 35,
          "title": "Do you miss being a student",
          "q": "Do you miss being a student?",
          "words": {
            "正面回答": [
              "Absolutely miss it"
            ],
            "原因或时间": [
              "when tired of work"
            ],
            "频次": [
              "the school canteen and classroom"
            ],
            "感受": [
              "holds precious memories and emotions"
            ]
          }
        },
        {
          "id": 36,
          "title": "What kind of house or apartment do you want to live in in the future",
          "q": "What kind of house or apartment do you want to live in in the future?",
          "words": {
            "正面回答": [
              "A spacious house"
            ],
            "原因或时间": [
              "love quietness"
            ],
            "频次": [
              "residential areas"
            ],
            "感受": [
              "good for self-care",
              "chill out"
            ]
          }
        },
        {
          "id": 37,
          "title": "What part of your home do you like the most",
          "q": "What part of your home do you like the most?",
          "words": {
            "正面回答": [
              "My bedroom"
            ],
            "原因或时间": [
              "when I need me time"
            ],
            "频次": [
              "listen to music",
              "binge-watch TV shows"
            ],
            "感受": [
              "unwind"
            ]
          }
        },
        {
          "id": 38,
          "title": "What's your favorite room in your apartment or house",
          "q": "What's your favorite room in your apartment or house?",
          "words": {
            "正面回答": [
              "The living room"
            ],
            "原因或时间": [
              "after dinner"
            ],
            "频次": [
              "hang out with family"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 39,
          "title": "Do you plan to live there for a long time",
          "q": "Do you plan to live there for a long time?",
          "words": {
            "正面回答": [
              "Yes",
              "I plan to"
            ],
            "原因或时间": [
              "as long as I'm here"
            ],
            "频次": [
              "close to convenience stores"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 40,
          "title": "Do you like your hometown",
          "q": "Do you like your hometown?",
          "words": {
            "正面回答": [
              "I'm a big fan of it"
            ],
            "原因或时间": [
              "food heaven"
            ],
            "频次": [
              "street food",
              "tasty local food"
            ],
            "感受": [
              "satisfy my taste buds"
            ]
          }
        },
        {
          "id": 41,
          "title": "Do you like living there",
          "q": "Do you like living there?",
          "words": {
            "正面回答": [
              "Yes",
              "I enjoy living there"
            ],
            "原因或时间": [
              "in my free time"
            ],
            "频次": [
              "go to the city centre"
            ],
            "感受": [
              "take a break and relax"
            ]
          }
        },
        {
          "id": 42,
          "title": "What do you like (most) about your hometown",
          "q": "What do you like (most) about your hometown?",
          "words": {
            "正面回答": [
              "The natural views"
            ],
            "原因或时间": [
              "on Sunny days"
            ],
            "频次": [
              "go for a walk in the park"
            ],
            "感受": [
              "reduce stress"
            ]
          }
        },
        {
          "id": 43,
          "title": "Is there anything you dislike about it",
          "q": "Is there anything you dislike about it?",
          "words": {
            "正面回答": [
              "The only thing I dislike is"
            ],
            "原因或时间": [
              "heavy traffic"
            ],
            "频次": [
              "during rush hour"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 44,
          "title": "Do you like the area that you live in",
          "q": "Do you like the area that you live in?",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "原因或时间": [
              "great infrastructure"
            ],
            "频次": [
              "just about 10mins walk away from my home"
            ],
            "感受": [
              "super practical"
            ]
          }
        },
        {
          "id": 45,
          "title": "Where do you like to go in that area",
          "q": "Where do you like to go in that area?",
          "words": {
            "正面回答": [
              "I prefer going to the cafes"
            ],
            "原因或时间": [
              "when I have time for myself"
            ],
            "频次": [
              "read books"
            ],
            "感受": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 46,
          "title": "Do you like this city? Why",
          "q": "Do you like this city? Why?",
          "words": {
            "正面回答": [
              "I'm passionate about it"
            ],
            "原因或时间": [
              "since I moved here"
            ],
            "频次": [
              "go to extra classes and events"
            ],
            "感受": [
              "holds memories and emotions"
            ]
          }
        },
        {
          "id": 47,
          "title": "What would you like to do if you had a day off tomorrow",
          "q": "What would you like to do if you had a day off tomorrow?",
          "words": {
            "正面回答": [
              "I would like to take a rest"
            ],
            "原因或时间": [
              "during the day off"
            ],
            "频次": [
              "stay at home and have some me time"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 48,
          "title": "Do you want to make your dreams come true",
          "q": "Do you want to make your dreams come true?",
          "words": {
            "正面回答": [
              "Absolutely desire it"
            ],
            "原因或时间": [
              "for my future"
            ],
            "频次": [
              "take the initiative to work hard",
              "work hard at my studies"
            ],
            "感受": [
              "The thing will make me happy is the time when it comes true"
            ]
          }
        },
        {
          "id": 49,
          "title": "Do you want to live in a tall building",
          "q": "Do you want to live in a tall building?",
          "words": {
            "正面回答": [],
            "原因或时间": [
              "convenient"
            ],
            "频次": [
              "shopping malls"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 50,
          "title": "What are your favourite activities",
          "q": "What are your favourite activities?",
          "words": {
            "正面回答": [],
            "原因或时间": [
              "free time"
            ],
            "频次": [
              "binge-watch TV shows"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 51,
          "title": "Do you enjoy being the age you are now",
          "q": "Do you enjoy being the age you are now?",
          "words": {
            "正面回答": [],
            "原因或时间": [],
            "频次": [
              "go to parties"
            ],
            "感受": [
              "lift my mood"
            ]
          }
        },
        {
          "id": 52,
          "title": "Do you want to be a famous person",
          "q": "Do you want to be a famous person?",
          "words": {
            "正面回答": [],
            "原因或时间": [],
            "频次": [
              "shop online"
            ],
            "感受": [
              "satisfy"
            ]
          }
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
          "title": "Do you eat different foods at different times of the year",
          "q": "Do you eat different foods at different times of the year?",
          "words": {
            "正面回答": [
              "Absolutely yes"
            ],
            "原因": [
              "groceries",
              "food ingredients"
            ],
            "时间线+行为描述": [
              "get together"
            ],
            "影响": [
              "good for the mind and the body"
            ]
          }
        },
        {
          "id": 2,
          "title": "What do you usually do in the morning",
          "q": "What do you usually do in the morning?",
          "words": {
            "正面回答": [
              "I have a daily routine"
            ],
            "原因": [
              "self-care"
            ],
            "时间线+行为描述": [
              "after I get up",
              "go jogging"
            ],
            "影响": [
              "energetic",
              "full of beans"
            ]
          }
        },
        {
          "id": 3,
          "title": "What did you do in the morning when you were little",
          "q": "What did you do in the morning when you were little?",
          "words": {
            "正面回答": [
              "It was quite simple"
            ],
            "原因": [
              "my parents requirements"
            ],
            "时间线+行为描述": [
              "before I went to primary school",
              "eat breakfast"
            ],
            "影响": [
              "work hard at my studies"
            ]
          }
        },
        {
          "id": 4,
          "title": "Do you walk a lot",
          "q": "Do you walk a lot?",
          "words": {
            "正面回答": [
              "Definitely"
            ],
            "原因": [
              "reduce stress"
            ],
            "时间线+行为描述": [
              "in my free time",
              "go for a walk"
            ],
            "影响": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 5,
          "title": "Did you often go outside to have a walk when you were a child",
          "q": "Did you often go outside to have a walk when you were a child?",
          "words": {
            "正面回答": [
              "Yes",
              "I used to"
            ],
            "原因": [
              "have exposure to the nature"
            ],
            "时间线+行为描述": [
              "when the weather is nice"
            ],
            "影响": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 6,
          "title": "Do you look out the window at the scenery when travelling by bus or car",
          "q": "Do you look out the window at the scenery when travelling by bus or car?",
          "words": {
            "正面回答": [
              "I always do that"
            ],
            "原因": [
              "when I feel bored"
            ],
            "时间线+行为描述": [
              "take a bus",
              "listen to music"
            ],
            "影响": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 7,
          "title": "Do you take photos of buildings",
          "q": "Do you take photos of buildings?",
          "words": {
            "正面回答": [
              "I often take photos"
            ],
            "原因": [
              "feel passionate about something"
            ],
            "时间线+行为描述": [
              "the city centre",
              "take photos"
            ],
            "影响": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 8,
          "title": "Do you keep plants at home",
          "q": "Do you keep plants at home?",
          "words": {
            "正面回答": [
              "Yes",
              "quite a few"
            ],
            "原因": [
              "sensory experiences"
            ],
            "时间线+行为描述": [
              "stay home"
            ],
            "影响": [
              "a great stress buster",
              "unwind"
            ]
          }
        },
        {
          "id": 9,
          "title": "Do you wear headphones in public places",
          "q": "Do you wear headphones in public places?",
          "words": {
            "正面回答": [
              "Almost always"
            ],
            "原因": [
              "have some me time"
            ],
            "时间线+行为描述": [
              "in public during rush hour"
            ],
            "影响": [
              "escape from the city's hustle and bustle"
            ]
          }
        },
        {
          "id": 10,
          "title": "Do you often go to public places with your friends",
          "q": "Do you often go to public places with your friends?",
          "words": {
            "正面回答": [
              "Regularly"
            ],
            "原因": [
              "hustle and bustle"
            ],
            "时间线+行为描述": [
              "shopping malls"
            ],
            "影响": [
              "expand my social circle"
            ]
          }
        },
        {
          "id": 11,
          "title": "How much money do you usually spend on shoes",
          "q": "How much money do you usually spend on shoes?",
          "words": {
            "正面回答": [
              "I spend quite a lot"
            ],
            "原因": [
              "get dressed"
            ],
            "时间线+行为描述": [
              "shop online"
            ],
            "影响": [
              "it makes me happy"
            ]
          }
        },
        {
          "id": 12,
          "title": "Do you often tell your friends when they do something well",
          "q": "Do you often tell your friends when they do something well?",
          "words": {
            "正面回答": [
              "Exactly",
              "I always tell them"
            ],
            "原因": [
              "mutually motivate each other"
            ],
            "时间线+行为描述": [
              "go to parties"
            ],
            "影响": [
              "altruistic behaviour"
            ]
          }
        },
        {
          "id": 13,
          "title": "Do you bring food or snacks with you when going out",
          "q": "Do you bring food or snacks with you when going out?",
          "words": {
            "正面回答": [
              "I have the habit of bringing snacks"
            ],
            "原因": [
              "practical"
            ],
            "时间线+行为描述": [
              "grab my stuff before I go out"
            ],
            "影响": [
              "self-care"
            ]
          }
        },
        {
          "id": 14,
          "title": "Do you always take your mobile phone with you when going out",
          "q": "Do you always take your mobile phone with you when going out?",
          "words": {
            "正面回答": [
              "Absolutely"
            ],
            "原因": [
              "rely on"
            ],
            "时间线+行为描述": [
              "places",
              "pay with my phone"
            ],
            "影响": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 15,
          "title": "Do you often bring cash with you",
          "q": "Do you often bring cash with you?",
          "words": {
            "正面回答": [
              "Seldom nowadays"
            ],
            "原因": [
              "practical"
            ],
            "时间线+行为描述": [
              "convenience stores"
            ],
            "影响": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 16,
          "title": "How often do you use cash",
          "q": "How often do you use cash?",
          "words": {
            "正面回答": [
              "Rarely use it"
            ],
            "原因": [
              "lifestyle preferences"
            ],
            "时间线+行为描述": [
              "street market"
            ],
            "影响": [
              "it makes me happy"
            ]
          }
        },
        {
          "id": 17,
          "title": "What do you usually chat about with friends",
          "q": "What do you usually chat about with friends?",
          "words": {
            "正面回答": [
              "Various topics"
            ],
            "原因": [
              "meet people with similar interests"
            ],
            "时间线+行为描述": [
              "cafes",
              "have a chat"
            ],
            "影响": [
              "share thoughts and feelings"
            ]
          }
        },
        {
          "id": 18,
          "title": "Do you argue with friends",
          "q": "Do you argue with friends?",
          "words": {
            "正面回答": [
              "Occasionally we do"
            ],
            "原因": [
              "have strong opinions"
            ],
            "时间线+行为描述": [
              "share opinions"
            ],
            "影响": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 19,
          "title": "Do you often see advertisements when you are on your phone or computer",
          "q": "Do you often see advertisements when you are on your phone or computer?",
          "words": {
            "正面回答": [
              "All the time"
            ],
            "原因": [
              "obsessed with short videos"
            ],
            "时间线+行为描述": [
              "spend a lot of time on dou yin"
            ],
            "影响": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 20,
          "title": "Do you often visit a museum",
          "q": "Do you often visit a museum?",
          "words": {
            "正面回答": [
              "From time to time"
            ],
            "原因": [
              "outside the classroom"
            ],
            "时间线+行为描述": [
              "the city centre"
            ],
            "影响": [
              "good for the mind and the body"
            ]
          }
        },
        {
          "id": 21,
          "title": "How often do you take a rest or a break",
          "q": "How often do you take a rest or a break?",
          "words": {
            "正面回答": [
              "Every single day"
            ],
            "原因": [
              "to relieve stress"
            ],
            "时间线+行为描述": [
              "library"
            ],
            "影响": [
              "sit down and relax"
            ]
          }
        },
        {
          "id": 22,
          "title": "What do you usually do when you are resting",
          "q": "What do you usually do when you are resting?",
          "words": {
            "正面回答": [
              "I do lots of things"
            ],
            "原因": [
              "have some me time"
            ],
            "时间线+行为描述": [
              "dorms",
              "binge-watch TV shows"
            ],
            "影响": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 23,
          "title": "Do you take a nap when you are taking your rest",
          "q": "Do you take a nap when you are taking your rest?",
          "words": {
            "正面回答": [
              "Yes",
              "I usually take a nap"
            ],
            "原因": [
              "self-care"
            ],
            "时间线+行为描述": [
              "until midday"
            ],
            "影响": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 24,
          "title": "How much time do you spend on your studies each week",
          "q": "How much time do you spend on your studies each week?",
          "words": {
            "正面回答": [
              "I spend a massive amount of time"
            ],
            "原因": [
              "work hard at my studies"
            ],
            "时间线+行为描述": [
              "classroom",
              "complete homework independently"
            ],
            "影响": [
              "The thing will make me happy is the time when"
            ]
          }
        },
        {
          "id": 25,
          "title": "What technology do you use when you study",
          "q": "What technology do you use when you study?",
          "words": {
            "正面回答": [
              "Mainly computers and iPads"
            ],
            "原因": [
              "it has something to do with my personality"
            ],
            "时间线+行为描述": [
              "go to classes",
              "listen to a lecture"
            ],
            "影响": [
              "practical"
            ]
          }
        },
        {
          "id": 26,
          "title": "What technology do you use at work",
          "q": "What technology do you use at work?",
          "words": {
            "正面回答": [
              "Mainly computers and iPads"
            ],
            "原因": [
              "it has something to do with my personality"
            ],
            "时间线+行为描述": [],
            "影响": [
              "practical"
            ]
          }
        },
        {
          "id": 27,
          "title": "What room does your family spend most of the time in",
          "q": "What room does your family spend most of the time in?",
          "words": {
            "正面回答": [
              "Definitely the living room"
            ],
            "原因": [
              "share experiences"
            ],
            "时间线+行为描述": [
              "dinner"
            ],
            "影响": [
              "memories and emotions"
            ]
          }
        },
        {
          "id": 28,
          "title": "What do you usually do in your apartment",
          "q": "What do you usually do in your apartment?",
          "words": {
            "正面回答": [
              "I usually stay indoors"
            ],
            "原因": [
              "have some me time"
            ],
            "时间线+行为描述": [
              "renting an apartment",
              "flip through the pages of real books"
            ],
            "影响": [
              "slow down"
            ]
          }
        },
        {
          "id": 29,
          "title": "Do you often see your neighbors",
          "q": "Do you often see your neighbors?",
          "words": {
            "正面回答": [
              "Yes",
              "quite often"
            ],
            "原因": [
              "residential areas"
            ],
            "时间线+行为描述": [
              "head out"
            ],
            "影响": [
              "have a conversation"
            ]
          }
        },
        {
          "id": 30,
          "title": "What do you usually do when you have days off",
          "q": "What do you usually do when you have days off?",
          "words": {
            "正面回答": [
              "I have a packed schedule"
            ],
            "原因": [
              "feel passionate about"
            ],
            "时间线+行为描述": [
              "pig out on tasty local food",
              "eat out in a restaurant"
            ],
            "影响": [
              "it really lifts my mood"
            ]
          }
        },
        {
          "id": 31,
          "title": "Do you usually spend your days off with your parents or with your friends",
          "q": "Do you usually spend your days off with your parents or with your friends?",
          "words": {
            "正面回答": [
              "Mostly with my friends"
            ],
            "原因": [
              "meet people with similar interests"
            ],
            "时间线+行为描述": [
              "in my free time",
              "hang out"
            ],
            "影响": [
              "take a break and relax"
            ]
          }
        },
        {
          "id": 32,
          "title": "Do you share your dreams with others",
          "q": "Do you share your dreams with others?",
          "words": {
            "正面回答": [
              "Yes",
              "I frequently do"
            ],
            "原因": [
              "share thoughts and feelings"
            ],
            "时间线+行为描述": [
              "get together with friends and classmates"
            ],
            "影响": [
              "mutually motivate each other"
            ]
          }
        },
        {
          "id": 33,
          "title": "Do you always bring a lot of keys with you",
          "q": "Do you always bring a lot of keys with you?",
          "words": {
            "正面回答": [
              "No",
              "seldom"
            ],
            "原因": [
              "rely on"
            ],
            "时间线+行为描述": [
              "grab my stuff before I go out"
            ],
            "影响": [
              "practical"
            ]
          }
        },
        {
          "id": 34,
          "title": "Do you often forget the keys and lock yourself out",
          "q": "Do you often forget the keys and lock yourself out?",
          "words": {
            "正面回答": [
              "It depends",
              "occasionally yes"
            ],
            "原因": [
              "something comes up"
            ],
            "时间线+行为描述": [
              "school"
            ],
            "影响": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 35,
          "title": "When would old people ask young people for advice",
          "q": "When would old people ask young people for advice?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "spend time on phone"
            ],
            "影响": [
              "altruistic behaviour"
            ]
          }
        },
        {
          "id": 36,
          "title": "Are there any occasions when people need to pretend to smile",
          "q": "Are there any occasions when people need to pretend to smile?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "have a conversation"
            ],
            "影响": []
          }
        },
        {
          "id": 37,
          "title": "Why do more people own and drive private vehicles now",
          "q": "Why do more people own and drive private vehicles now?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "head out"
            ],
            "影响": [
              "practical",
              "time-saving"
            ]
          }
        },
        {
          "id": 38,
          "title": "What can children do to help their parents",
          "q": "What can children do to help their parents?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "chores"
            ],
            "影响": [
              "self-care"
            ]
          }
        },
        {
          "id": 39,
          "title": "Why do many people like listening to music while doing sports",
          "q": "Why do many people like listening to music while doing sports?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "go jogging"
            ],
            "影响": [
              "unwind"
            ]
          }
        },
        {
          "id": 40,
          "title": "Why are employees reluctant to ask their managers for help",
          "q": "Why are employees reluctant to ask their managers for help?",
          "words": {
            "正面回答": [],
            "原因": [],
            "时间线+行为描述": [
              "complete independently"
            ],
            "影响": [
              "bothers me"
            ]
          }
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
          "title": "What is the most popular animal in China",
          "q": "What is the most popular animal in China?",
          "words": {
            "正面回答": [
              "I think pandas and dogs"
            ],
            "举例或原因": [
              "loyal"
            ],
            "作用或影响": [
              "self-care"
            ],
            "感受": [
              "a great stress buster"
            ]
          }
        },
        {
          "id": 2,
          "title": "Is team sports popular in your culture",
          "q": "Is team sports popular in your culture?",
          "words": {
            "正面回答": [
              "Absolutely yes"
            ],
            "举例或原因": [
              "play basketball",
              "volleyball"
            ],
            "作用或影响": [
              "mutually motivate each other"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 3,
          "title": "What do you consider when choosing a gift",
          "q": "What do you consider when choosing a gift?",
          "words": {
            "正面回答": [
              "Functionality comes first"
            ],
            "举例或原因": [
              "coat",
              "sweatshirt"
            ],
            "作用或影响": [
              "practical"
            ],
            "感受": [
              "lift my mood"
            ]
          }
        },
        {
          "id": 4,
          "title": "Do you think you are good at choosing gifts",
          "q": "Do you think you are good at choosing gifts?",
          "words": {
            "正面回答": [
              "I'm quite good at it"
            ],
            "举例或原因": [
              "share thoughts and feelings"
            ],
            "作用或影响": [
              "lifestyle preferences"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 5,
          "title": "Why do people like to walk in parks",
          "q": "Why do people like to walk in parks?",
          "words": {
            "正面回答": [
              "To have exposure to nature"
            ],
            "举例或原因": [
              "in free time"
            ],
            "作用或影响": [
              "have some me time"
            ],
            "感受": [
              "go for a walk",
              "reduce stress"
            ]
          }
        },
        {
          "id": 6,
          "title": "Do Chinese people send plants as gifts",
          "q": "Do Chinese people send plants as gifts?",
          "words": {
            "正面回答": [
              "Occasionally",
              "yes"
            ],
            "举例或原因": [
              "sensory experiences"
            ],
            "作用或影响": [
              "home"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 7,
          "title": "Do you think students would benefit more from more rules",
          "q": "Do you think students would benefit more from more rules?",
          "words": {
            "正面回答": [
              "Moderate rules are beneficial"
            ],
            "举例或原因": [
              "classroom"
            ],
            "作用或影响": [
              "complete homework independently"
            ],
            "感受": [
              "self-driven"
            ]
          }
        },
        {
          "id": 8,
          "title": "Do most people like crowded places",
          "q": "Do most people like crowded places?",
          "words": {
            "正面回答": [
              "It depends"
            ],
            "举例或原因": [
              "feel passionate about",
              "city centre"
            ],
            "作用或影响": [
              "meet people with similar interests"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 9,
          "title": "What are the benefits of being friends with or working with old people",
          "q": "What are the benefits of being friends with or working with old people?",
          "words": {
            "正面回答": [
              "There are lots of merits"
            ],
            "举例或原因": [
              "have a conversation"
            ],
            "作用或影响": [
              "share experiences"
            ],
            "感受": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 10,
          "title": "Is growing vegetables popular in your country",
          "q": "Is growing vegetables popular in your country?",
          "words": {
            "正面回答": [
              "Mainly popular in rural areas"
            ],
            "举例或原因": [
              "groceries",
              "food ingredients"
            ],
            "作用或影响": [
              "lifestyle preferences"
            ],
            "感受": [
              "good for the mind and the body"
            ]
          }
        },
        {
          "id": 11,
          "title": "Do you think it's easy to grow vegetables",
          "q": "Do you think it's easy to grow vegetables?",
          "words": {
            "正面回答": [
              "Not easy at all"
            ],
            "举例或原因": [
              "take the initiative to"
            ],
            "作用或影响": [
              "takeaways"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 12,
          "title": "Should schools teach students how to grow vegetables",
          "q": "Should schools teach students how to grow vegetables?",
          "words": {
            "正面回答": [
              "They definitely should"
            ],
            "举例或原因": [
              "extra classes and events"
            ],
            "作用或影响": [
              "practical"
            ],
            "感受": [
              "sense of achievement"
            ]
          }
        },
        {
          "id": 13,
          "title": "How do you feel when people dont return things they borrowed from you",
          "q": "How do you feel when people dont return things they borrowed from you?",
          "words": {
            "正面回答": [
              "I feel terrible"
            ],
            "举例或原因": [
              "real books"
            ],
            "作用或影响": [
              "share experiences"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 14,
          "title": "Do you mind if others borrow money from you",
          "q": "Do you mind if others borrow money from you?",
          "words": {
            "正面回答": [
              "It depends on the situation"
            ],
            "举例或原因": [
              "homie",
              "besties"
            ],
            "作用或影响": [
              "altruistic behaviour"
            ],
            "感受": [
              "lift my mood"
            ]
          }
        },
        {
          "id": 15,
          "title": "Do you think museums are important",
          "q": "Do you think museums are important?",
          "words": {
            "正面回答": [
              "Vitally important"
            ],
            "举例或原因": [
              "city centre"
            ],
            "作用或影响": [
              "listen to a lecture"
            ],
            "感受": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 16,
          "title": "How do you feel after taking a nap",
          "q": "How do you feel after taking a nap?",
          "words": {
            "正面回答": [
              "Fully refreshed"
            ],
            "举例或原因": [
              "when I feel bored"
            ],
            "作用或影响": [
              "self-care"
            ],
            "感受": [
              "full of beans"
            ]
          }
        },
        {
          "id": 17,
          "title": "What kind of things are not suitable for sharing",
          "q": "What kind of things are not suitable for sharing?",
          "words": {
            "正面回答": [
              "Private information"
            ],
            "举例或原因": [
              "WeChat"
            ],
            "作用或影响": [
              "rely on"
            ],
            "感受": [
              "it bothers me"
            ]
          }
        },
        {
          "id": 18,
          "title": "Do you think that your subject is popular in your country",
          "q": "Do you think that your subject is popular in your country?",
          "words": {
            "正面回答": [
              "Quite popular"
            ],
            "举例或原因": [
              "go to classes"
            ],
            "作用或影响": [
              "practical"
            ],
            "感受": [
              "self-driven"
            ]
          }
        },
        {
          "id": 19,
          "title": "What are the benefits of being your age",
          "q": "What are the benefits of being your age?",
          "words": {
            "正面回答": [
              "Many obvious advantages"
            ],
            "举例或原因": [
              "hang out"
            ],
            "作用或影响": [
              "feel passionate about something"
            ],
            "感受": [
              "have a blast"
            ]
          }
        },
        {
          "id": 20,
          "title": "What changes would you like to see in your school",
          "q": "What changes would you like to see in your school?",
          "words": {
            "正面回答": [
              "The food service"
            ],
            "举例或原因": [
              "school canteen"
            ],
            "作用或影响": [
              "delicious"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 21,
          "title": "What do you think is the most important at the moment",
          "q": "What do you think is the most important at the moment?",
          "words": {
            "正面回答": [
              "My academic performance"
            ],
            "举例或原因": [
              "work hard at my studies"
            ],
            "作用或影响": [
              "complete homework independently"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 22,
          "title": "What makes you feel pleasant in your home",
          "q": "What makes you feel pleasant in your home?",
          "words": {
            "正面回答": [
              "The quiet and private atmosphere"
            ],
            "举例或原因": [
              "dorms",
              "home"
            ],
            "作用或影响": [
              "have some me time"
            ],
            "感受": [
              "unwind"
            ]
          }
        },
        {
          "id": 23,
          "title": "Do you think it is important to live in a comfortable environment",
          "q": "Do you think it is important to live in a comfortable environment?",
          "words": {
            "正面回答": [
              "It is of vital importance"
            ],
            "举例或原因": [
              "residential areas"
            ],
            "作用或影响": [
              "self-care"
            ],
            "感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 24,
          "title": "Do you think you will continue living there for a long time",
          "q": "Do you think you will continue living there for a long time?",
          "words": {
            "正面回答": [
              "Most likely",
              "yes"
            ],
            "举例或原因": [
              "convenience stores"
            ],
            "作用或影响": [
              "lifestyle preferences"
            ],
            "感受": [
              "holds precious memories and emotions"
            ]
          }
        },
        {
          "id": 25,
          "title": "Is your hometown a good place for young people to pursue their careers",
          "q": "Is your hometown a good place for young people to pursue their careers?",
          "words": {
            "正面回答": [
              "An ideal place indeed"
            ],
            "举例或原因": [
              "city centre"
            ],
            "作用或影响": [
              "take the initiative to"
            ],
            "感受": [
              "sense of achievement"
            ]
          }
        },
        {
          "id": 26,
          "title": "Is the city friendly to children and old people",
          "q": "Is the city friendly to children and old people?",
          "words": {
            "正面回答": [
              "Very friendly"
            ],
            "举例或原因": [
              "park"
            ],
            "作用或影响": [
              "go for a walk"
            ],
            "感受": [
              "practical"
            ]
          }
        },
        {
          "id": 27,
          "title": "Would you recommend your city to others",
          "q": "Would you recommend your city to others?",
          "words": {
            "正面回答": [
              "I highly recommend it"
            ],
            "举例或原因": [
              "tasty local food"
            ],
            "作用或影响": [
              "share a meal"
            ],
            "感受": [
              "satisfy your taste buds"
            ]
          }
        },
        {
          "id": 28,
          "title": "Do you share your dreams with others",
          "q": "Do you share your dreams with others?",
          "words": {
            "正面回答": [
              "I frequently do"
            ],
            "举例或原因": [
              "go to parties",
              "get together"
            ],
            "作用或影响": [
              "share thoughts and feelings"
            ],
            "感受": [
              "mutually motivate each other"
            ]
          }
        },
        {
          "id": 29,
          "title": "Do you think dreams have special meanings",
          "q": "Do you think dreams have special meanings?",
          "words": {
            "正面回答": [
              "Sometimes they do"
            ],
            "举例或原因": [
              "something comes up"
            ],
            "作用或影响": [
              "reflect on things"
            ],
            "感受": [
              "reduce stress"
            ]
          }
        },
        {
          "id": 30,
          "title": "Do you think its a good idea to leave your keys with a neighbour",
          "q": "Do you think its a good idea to leave your keys with a neighbour?",
          "words": {
            "正面回答": [
              "Good idea if trusted"
            ],
            "举例或原因": [
              "head out"
            ],
            "作用或影响": [
              "altruistic behaviour"
            ],
            "感受": [
              "practical",
              "it bothers me"
            ]
          }
        },
        {
          "id": 31,
          "title": "At what age do you think people are the happiest",
          "q": "At what age do you think people are the happiest?",
          "words": {
            "正面回答": [],
            "举例或原因": [
              "childhood"
            ],
            "作用或影响": [
              "play video games"
            ],
            "感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 32,
          "title": "What kind of jobs are the most popular in your country",
          "q": "What kind of jobs are the most popular in your country?",
          "words": {
            "正面回答": [],
            "举例或原因": [
              "practical"
            ],
            "作用或影响": [
              "make money"
            ],
            "感受": [
              "sense of achievement"
            ]
          }
        },
        {
          "id": 33,
          "title": "Is it easy to become famous in your country",
          "q": "Is it easy to become famous in your country?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "browse videos"
            ],
            "感受": []
          }
        },
        {
          "id": 34,
          "title": "How does the internet benefit people",
          "q": "How does the internet benefit people?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "takeaways",
              "shop online"
            ],
            "感受": []
          }
        },
        {
          "id": 35,
          "title": "Is smiling important in your culture",
          "q": "Is smiling important in your culture?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "have a conversation"
            ],
            "感受": [
              "comfortable"
            ]
          }
        },
        {
          "id": 36,
          "title": "What do you think of the future of electric cars",
          "q": "What do you think of the future of electric cars?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "reduce emission"
            ],
            "感受": []
          }
        },
        {
          "id": 37,
          "title": "Do you think smart children are happier than other children",
          "q": "Do you think smart children are happier than other children?",
          "words": {
            "正面回答": [],
            "举例或原因": [
              "work hard at studies"
            ],
            "作用或影响": [
              "appreciated"
            ],
            "感受": []
          }
        },
        {
          "id": 38,
          "title": "Is it important for schools to identify and develop each student's talents",
          "q": "Is it important for schools to identify and develop each student's talents?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "study"
            ],
            "感受": [
              "sense of achievement"
            ]
          }
        },
        {
          "id": 39,
          "title": "Do you think children should receive some musical education",
          "q": "Do you think children should receive some musical education?",
          "words": {
            "正面回答": [],
            "举例或原因": [
              "interests"
            ],
            "作用或影响": [
              "listen to music"
            ],
            "感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 40,
          "title": "Do you think schools should teach children to do household chores",
          "q": "Do you think schools should teach children to do household chores?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "self-care"
            ],
            "感受": [
              "practical"
            ]
          }
        },
        {
          "id": 41,
          "title": "Should children do everything their parents ask them to do",
          "q": "Should children do everything their parents ask them to do?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "reflect on things"
            ],
            "感受": [
              "bothers me"
            ]
          }
        },
        {
          "id": 42,
          "title": "How can employers encourage their staff",
          "q": "How can employers encourage their staff?",
          "words": {
            "正面回答": [],
            "举例或原因": [],
            "作用或影响": [
              "eat out in a restaurant"
            ],
            "感受": [
              "mutually motivate each other"
            ]
          }
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
          "title": "Where do you prefer to keep your pet, indoors or outdoors",
          "q": "Where do you prefer to keep your pet, indoors or outdoors?",
          "words": {
            "正面回答": [
              "Indoors"
            ],
            "选项1的特点与作用": [
              "home",
              "dorms"
            ],
            "选项2的特点与作用": [
              "park"
            ],
            "个人感受": [
              "unwind"
            ]
          }
        },
        {
          "id": 2,
          "title": "What are the differences between team sports and individual sports",
          "q": "What are the differences between team sports and individual sports?",
          "words": {
            "正面回答": [
              "Huge differences in atmosphere"
            ],
            "选项1的特点与作用": [
              "play basketball",
              "volleyball"
            ],
            "选项2的特点与作用": [
              "go jogging"
            ],
            "个人感受": [
              "meet people with similar interests"
            ]
          }
        },
        {
          "id": 3,
          "title": "Are there any differences between what you do in the morning now and what you did in the past",
          "q": "Are there any differences between what you do in the morning now and what you did in the past?",
          "words": {
            "正面回答": [
              "Totally different"
            ],
            "选项1的特点与作用": [
              "eat breakfast"
            ],
            "选项2的特点与作用": [
              "browse videos"
            ],
            "个人感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 4,
          "title": "Do you spend your mornings doing the same things on both weekends and weekdays? Why",
          "q": "Do you spend your mornings doing the same things on both weekends and weekdays? Why?",
          "words": {
            "正面回答": [
              "No",
              "quite different"
            ],
            "选项1的特点与作用": [
              "go to classes"
            ],
            "选项2的特点与作用": [
              "binge-watch TV shows"
            ],
            "个人感受": [
              "self-care"
            ]
          }
        },
        {
          "id": 5,
          "title": "Do you prefer to read on paper or on a screen",
          "q": "Do you prefer to read on paper or on a screen?",
          "words": {
            "正面回答": [
              "Read on paper"
            ],
            "选项1的特点与作用": [
              "flip through the pages of real books"
            ],
            "选项2的特点与作用": [
              "spend a lot of time on phone"
            ],
            "个人感受": [
              "reflect on things"
            ]
          }
        },
        {
          "id": 6,
          "title": "When do you need to read carefully, and when not",
          "q": "When do you need to read carefully, and when not?",
          "words": {
            "正面回答": [
              "It depends on the content"
            ],
            "选项1的特点与作用": [
              "study",
              "library"
            ],
            "选项2的特点与作用": [
              "browse videos"
            ],
            "个人感受": [
              "complete homework independently",
              "practical"
            ]
          }
        },
        {
          "id": 7,
          "title": "Do you prefer scanning or detailed reading",
          "q": "Do you prefer scanning or detailed reading?",
          "words": {
            "正面回答": [
              "Detailed reading"
            ],
            "选项1的特点与作用": [
              "real books"
            ],
            "选项2的特点与作用": [
              "takeaways"
            ],
            "个人感受": [
              "work hard at my studies"
            ]
          }
        },
        {
          "id": 8,
          "title": "Do you prefer typing or handwriting",
          "q": "Do you prefer typing or handwriting?",
          "words": {
            "正面回答": [
              "Typing"
            ],
            "选项1的特点与作用": [
              "shop online"
            ],
            "选项2的特点与作用": [
              "classroom"
            ],
            "个人感受": [
              "time-saving and labor-saving",
              "practical"
            ]
          }
        },
        {
          "id": 9,
          "title": "Do you type on a desktop or laptop keyboard every day",
          "q": "Do you type on a desktop or laptop keyboard every day?",
          "words": {
            "正面回答": [
              "Laptop keyboard"
            ],
            "选项1的特点与作用": [
              "grab my stuff and head out"
            ],
            "选项2的特点与作用": [
              "dorms"
            ],
            "个人感受": [
              "study"
            ]
          }
        },
        {
          "id": 10,
          "title": "Do you prefer the mountains or the sea",
          "q": "Do you prefer the mountains or the sea?",
          "words": {
            "正面回答": [
              "The sea"
            ],
            "选项1的特点与作用": [
              "pig out on tasty local food"
            ],
            "选项2的特点与作用": [
              "hiking"
            ],
            "个人感受": [
              "chill out"
            ]
          }
        },
        {
          "id": 11,
          "title": "Did you prefer to do activities alone or with a group of people when you were a child",
          "q": "Did you prefer to do activities alone or with a group of people when you were a child?",
          "words": {
            "正面回答": [
              "With a group of people"
            ],
            "选项1的特点与作用": [
              "play video games"
            ],
            "选项2的特点与作用": [
              "me time"
            ],
            "个人感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 12,
          "title": "Do you prefer views in urban areas or rural areas",
          "q": "Do you prefer views in urban areas or rural areas?",
          "words": {
            "正面回答": [
              "Urban areas"
            ],
            "选项1的特点与作用": [
              "city centre",
              "shopping malls"
            ],
            "选项2的特点与作用": [
              "park"
            ],
            "个人感受": [
              "practical and makes me happy"
            ]
          }
        },
        {
          "id": 13,
          "title": "Do you prefer views in your own country or in other countries",
          "q": "Do you prefer views in your own country or in other countries?",
          "words": {
            "正面回答": [
              "In my own country"
            ],
            "选项1的特点与作用": [
              "tasty local food"
            ],
            "选项2的特点与作用": [
              "groceries",
              "food ingredients"
            ],
            "个人感受": [
              "satisfy my taste buds"
            ]
          }
        },
        {
          "id": 14,
          "title": "Do you prefer to have more or fewer rules at school",
          "q": "Do you prefer to have more or fewer rules at school?",
          "words": {
            "正面回答": [
              "Fewer rules"
            ],
            "选项1的特点与作用": [
              "extra classes and events"
            ],
            "选项2的特点与作用": [
              "classroom"
            ],
            "个人感受": [
              "relax my mind"
            ]
          }
        },
        {
          "id": 15,
          "title": "Which do you prefer, fashionable shoes or comfortable shoes",
          "q": "Which do you prefer, fashionable shoes or comfortable shoes?",
          "words": {
            "正面回答": [
              "Comfortable shoes"
            ],
            "选项1的特点与作用": [
              "go jogging",
              "go for a walk"
            ],
            "选项2的特点与作用": [
              "get dressed"
            ],
            "个人感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 16,
          "title": "Do you prefer to chat with a group of people or with only one friend",
          "q": "Do you prefer to chat with a group of people or with only one friend?",
          "words": {
            "正面回答": [
              "With only one friend"
            ],
            "选项1的特点与作用": [
              "cafes"
            ],
            "选项2的特点与作用": [
              "parties"
            ],
            "个人感受": [
              "share experiences and mutually motivate each other"
            ]
          }
        },
        {
          "id": 17,
          "title": "Do you prefer to communicate face-to-face or via social media",
          "q": "Do you prefer to communicate face-to-face or via social media?",
          "words": {
            "正面回答": [
              "Face-to-face"
            ],
            "选项1的特点与作用": [
              "eat out in a restaurant"
            ],
            "选项2的特点与作用": [
              "have a chat on WeChat"
            ],
            "个人感受": [
              "share thoughts and feelings"
            ]
          }
        },
        {
          "id": 18,
          "title": "Do you prefer to share news with your friends or your parents",
          "q": "Do you prefer to share news with your friends or your parents?",
          "words": {
            "正面回答": [
              "Friends"
            ],
            "选项1的特点与作用": [
              "people with similar interests"
            ],
            "选项2的特点与作用": [
              "home"
            ],
            "个人感受": [
              "lift my mood"
            ]
          }
        },
        {
          "id": 19,
          "title": "Do you prefer to study in the mornings or in the afternoons",
          "q": "Do you prefer to study in the mornings or in the afternoons?",
          "words": {
            "正面回答": [
              "In the mornings"
            ],
            "选项1的特点与作用": [
              "eat breakfast"
            ],
            "选项2的特点与作用": [
              "binge-watch TV shows"
            ],
            "个人感受": [
              "work hard at my studies"
            ]
          }
        },
        {
          "id": 20,
          "title": "Do you prefer living in a house or an apartment",
          "q": "Do you prefer living in a house or an apartment?",
          "words": {
            "正面回答": [
              "An apartment"
            ],
            "选项1的特点与作用": [
              "renting an apartment"
            ],
            "选项2的特点与作用": [
              "go to classes",
              "parties"
            ],
            "个人感受": [
              "practical"
            ]
          }
        },
        {
          "id": 21,
          "title": "What's the difference between where you are living now and where you have lived in the past",
          "q": "What's the difference between where you are living now and where you have lived in the past?",
          "words": {
            "正面回答": [
              "Huge differences"
            ],
            "选项1的特点与作用": [
              "residential areas",
              "convenience stores"
            ],
            "选项2的特点与作用": [
              "dorms"
            ],
            "个人感受": [
              "feel relaxed and at ease"
            ]
          }
        },
        {
          "id": 22,
          "title": "Do you usually spend your days off with your parents or with your friends",
          "q": "Do you usually spend your days off with your parents or with your friends?",
          "words": {
            "正面回答": [
              "With my friends"
            ],
            "选项1的特点与作用": [
              "hang out"
            ],
            "选项2的特点与作用": [
              "stay home"
            ],
            "个人感受": [
              "enjoy a good laugh"
            ]
          }
        },
        {
          "id": 23,
          "title": "Is it better to live in a new building or an old one",
          "q": "Is it better to live in a new building or an old one?",
          "words": {
            "正面回答": [],
            "选项1的特点与作用": [
              "shopping malls"
            ],
            "选项2的特点与作用": [
              "bothers me"
            ],
            "个人感受": [
              "comfortable"
            ]
          }
        },
        {
          "id": 24,
          "title": "What are the differences between old and young people's music preferences",
          "q": "What are the differences between old and young people's music preferences?",
          "words": {
            "正面回答": [],
            "选项1的特点与作用": [
              "traditional"
            ],
            "选项2的特点与作用": [
              "listen to music",
              "browse videos"
            ],
            "个人感受": [
              "chill out"
            ]
          }
        }
      ]
    }
  ]
};
