# -*- coding: utf-8 -*-
"""P1-only core kits: student 衣食住行 daily life (NOT shared with P2 deep stories)."""
from __future__ import annotations

from typing import Any

# 8 套可拆、可串的日常宇宙：贴合学生衣食住行 + 学/闲/机
# 原则：短细节、无 P2 长事件；同题多套可选；一套可跨多话题。
CORE_KITS: dict[str, dict[str, Any]] = {
    "wear_daily": {
        "id": "wear_daily",
        "nameZh": "日常穿戴",
        "summary": "球鞋、T恤、耳机、手表——上课通勤身边常用的东西。",
        "people": ["my parents", "classmates"],
        "places": ["campus", "the subway", "my desk"],
        "objects": ["sneakers", "a simple t-shirt", "wireless earbuds", "a simple watch"],
        "beats": {
            "now": "I wear sneakers and casual clothes most school days",
            "childhood": "school shoes and clothes chosen by my parents",
            "change": "I care more about comfort than loud fashion",
            "contrast_a": "comfort and easy matching",
            "contrast_b": "style-first outfits that feel tight",
            "feel": "comfortable and ready",
        },
        "open": ["Yes, I do", "Most days", "Quite often"],
        "examples": ["sneakers", "a simple t-shirt", "wireless earbuds", "a simple watch"],
        "freq": ["every day", "on the subway", "before class"],
        "feel": ["comfortable", "practical", "really convenient"],
        "why": ["comfort matters most", "they are easy to match", "they help me stay on time"],
        "opt_a": ["comfort", "casual clothes"],
        "opt_b": ["fashion shoes", "formal clothes every day"],
        "impact": ["protects my feet", "saves matching time", "keeps me punctual"],
        "child_examples": ["school shoes", "a coat from my parents", "a basic wired pair"],
        "change_a": ["comfort-first choices", "wireless earbuds"],
        "change_b": ["uncomfortable fashion", "always checking the phone for time"],
        "third_why": ["students walk a lot on campus", "daily gear must feel easy", "subway noise is heavy"],
    },
    "food_campus": {
        "id": "food_campus",
        "nameZh": "食堂与饮食",
        "summary": "食堂、水果蔬菜、周末小吃——每天都会碰到的吃。",
        "people": ["my roommate", "canteen staff"],
        "places": ["the campus canteen", "a small fruit stall", "street markets nearby"],
        "objects": ["fresh fruit", "cooked vegetables", "a simple lunch set"],
        "beats": {
            "now": "I eat at the canteen on weekdays and buy fruit after class",
            "childhood": "I disliked some bitter vegetables but liked fruit after meals",
            "change": "I try to add more vegetables instead of only takeout",
            "contrast_a": "canteen meals with vegetables",
            "contrast_b": "late-night takeout every day",
            "feel": "lighter and more energetic",
        },
        "open": ["Yes, I do", "Most weekdays", "At the canteen"],
        "examples": ["canteen lunch", "fresh fruit", "cooked vegetables", "street food at weekends"],
        "freq": ["every weekday", "after class", "at weekends"],
        "feel": ["fresh", "filling enough", "healthier"],
        "why": ["it keeps me full for study", "fruit is easy to carry", "vegetables are not hard to find"],
        "opt_a": ["canteen meals", "fresh fruit"],
        "opt_b": ["only takeout", "skipping vegetables"],
        "impact": ["keeps my energy steady", "costs less than delivery", "improves my diet a bit"],
        "child_examples": ["fruit after meals", "tomato dishes", "bitter vegetables I disliked"],
        "change_a": ["more vegetables", "regular canteen meals"],
        "change_b": ["only spicy takeout", "skipping breakfast"],
        "third_why": ["students need cheap filling food", "fresh stalls are nearby", "delivery is convenient but heavy"],
    },
    "home_dorm": {
        "id": "home_dorm",
        "nameZh": "宿舍生活",
        "summary": "宿舍/合租、书桌、室友、垃圾分类——住的那点事。",
        "people": ["my roommate", "floor mates"],
        "places": ["campus dorms", "a rented apartment", "the shared desk area"],
        "objects": ["a tidy desk", "storage boxes", "recycling bins"],
        "beats": {
            "now": "I live in dorms near campus and keep my desk clear before studying",
            "childhood": "my parents asked me to put things away after homework",
            "change": "sorting rubbish and tidying before bed became a habit",
            "contrast_a": "a tidy desk and sorting rubbish",
            "contrast_b": "a messy shared room and mixed trash",
            "feel": "settled and responsible",
        },
        "open": ["I live in dorms", "Yes, I try to", "Most days"],
        "examples": ["campus dorms", "a tidy desk", "my roommate", "recycling bins"],
        "freq": ["every day", "before studying", "after class"],
        "feel": ["convenient", "more focused", "responsible"],
        "why": ["it is close to class", "a clear desk helps focus", "sorting rubbish is a basic habit"],
        "opt_a": ["a tidy shared room", "sorting rubbish"],
        "opt_b": ["leaving things around", "throwing everything together"],
        "impact": ["helps me focus", "keeps conflicts low with roommates", "helps the environment"],
        "child_examples": ["putting toys away", "homework at a small desk", "parents reminding me"],
        "change_a": ["sorting rubbish", "evening tidy-up"],
        "change_b": ["ignoring recycling", "studying in a mess"],
        "third_why": ["shared rooms need rules", "tidy spaces reduce stress", "cities push recycling"],
    },
    "commute_city": {
        "id": "commute_city",
        "nameZh": "地铁通勤",
        "summary": "地铁、住区步行、高峰——出门路上的固定路线。",
        "people": ["commuters", "friendly neighbors"],
        "places": ["the subway", "a residential area", "my city centre"],
        "objects": ["a transit card", "sneakers for walking", "a folded umbrella"],
        "beats": {
            "now": "I take the subway to campus and walk ten minutes from the station",
            "childhood": "school was near home so I walked with classmates",
            "change": "subway became my default instead of long bus rides",
            "contrast_a": "subway plus a short walk",
            "contrast_b": "driving through rush-hour traffic",
            "feel": "efficient but a bit crowded at peaks",
        },
        "open": ["Yes, I do", "By subway", "Near my home"],
        "examples": ["the subway", "a short walk from the station", "rush-hour crowds", "weekend short trips"],
        "freq": ["every weekday", "during rush hour", "at weekends nearby"],
        "feel": ["convenient", "a bit crowded", "time-saving"],
        "why": ["the subway is reliable", "walking is good after classes", "shops are near my stop"],
        "opt_a": ["taking the subway", "walking the last part"],
        "opt_b": ["sitting in rush-hour traffic", "long irregular bus waits"],
        "impact": ["saves commute time", "keeps my day predictable", "lets me review notes on the train"],
        "child_examples": ["walking to school", "a short bus with my parents", "neighbourhood streets"],
        "change_a": ["subway-first commuting", "walking more"],
        "change_b": ["only long bus rides", "avoiding walking entirely"],
        "third_why": ["cities rely on metro lines", "peak hours feel packed", "short walks connect daily needs"],
    },
    "study_campus": {
        "id": "study_campus",
        "nameZh": "上课与图书馆",
        "summary": "专业课、图书馆、作业、老师——学生每天最熟的学习线。",
        "people": ["my classmates", "a patient teacher"],
        "places": ["campus classrooms", "the library", "a quiet study corner"],
        "objects": ["a notebook", "assignments", "library books"],
        "beats": {
            "now": "I attend campus classes and finish assignments in the library",
            "childhood": "secondary-school homework felt heavy but the routine was simple",
            "change": "I plan library blocks instead of last-minute cramming",
            "contrast_a": "studying on campus with a notebook",
            "contrast_b": "only scrolling notes on a phone in bed",
            "feel": "practical and a bit pressured near exams",
        },
        "open": ["I'm a student", "Yes, I do", "Every weekday"],
        "examples": ["campus classes", "library work", "handwritten notes", "group assignments"],
        "freq": ["every weekday", "before exams", "at weekends for review"],
        "feel": ["practical", "focused", "useful for my future"],
        "why": ["it matches my major", "the library is quiet", "notes help me remember"],
        "opt_a": ["studying on campus", "writing by hand"],
        "opt_b": ["only late-night cramming", "only typing on a phone"],
        "impact": ["builds useful skills", "keeps me organised", "supports exams"],
        "child_examples": ["secondary-school homework", "a favourite teacher", "simple class routines"],
        "change_a": ["planned library time", "handwritten review"],
        "change_b": ["last-minute panic", "no fixed study place"],
        "third_why": ["quiet spaces help memory", "good teachers explain patiently", "students need clear routines"],
    },
    "leisure_reset": {
        "id": "leisure_reset",
        "nameZh": "公园与放松",
        "summary": "公园散步、歌单、轻度运动——累了就出门换口气。",
        "people": ["a roommate", "friends after class"],
        "places": ["a nearby park", "the sports field", "campus paths"],
        "objects": ["a playlist", "a water bottle", "a badminton racket"],
        "beats": {
            "now": "When I feel tired I walk in a nearby park or play a short game",
            "childhood": "I played outside after school instead of staring at screens",
            "change": "I try to leave the desk when boredom hits",
            "contrast_a": "a park walk or light sport",
            "contrast_b": "endless scrolling in bed",
            "feel": "refreshed and lighter",
        },
        "open": ["Yes, I do", "At weekends", "When I feel tired"],
        "examples": ["a nearby park", "evening walks", "a short playlist", "a light badminton game"],
        "freq": ["at weekends", "after long study", "from time to time"],
        "feel": ["refreshed", "more relaxed", "clearer"],
        "why": ["fresh air helps", "moving resets my head", "music improves my mood"],
        "opt_a": ["going outside", "light exercise"],
        "opt_b": ["endless scrolling", "staying alone indoors"],
        "impact": ["improves my mood", "helps me sleep", "makes the next study block easier"],
        "child_examples": ["playing outside", "drawing at home", "simple games with classmates"],
        "change_a": ["fixed outdoor breaks", "short playlists"],
        "change_b": ["only phone breaks", "skipping movement"],
        "third_why": ["phones offer endless clips", "attention gets shorter", "people need real breaks"],
    },
    "phone_tools": {
        "id": "phone_tools",
        "nameZh": "手机与查资料",
        "summary": "网站搜索、微信、通勤刷到的内容——手机上的日常工具。",
        "people": ["group-chat classmates", "online creators"],
        "places": ["study websites", "WeChat chats", "the subway feed"],
        "objects": ["search tools", "Xiaohongshu", "phone notes"],
        "beats": {
            "now": "I use websites for study search and WeChat to keep in touch",
            "childhood": "information came from books and TV more than phones",
            "change": "search got faster, but ads and clips waste time if I am not careful",
            "contrast_a": "study websites and quick search",
            "contrast_b": "pop-up spam and aimless scrolling",
            "feel": "useful when focused, tiring when noisy",
        },
        "open": ["Yes, I do", "Almost every day", "On my phone"],
        "examples": ["study websites", "WeChat chats", "search tools", "short clips on the commute"],
        "freq": ["every day", "before exams", "on the commute"],
        "feel": ["useful", "really convenient", "sometimes distracting"],
        "why": ["it is fast to search", "I can keep in touch", "notes stay on my phone"],
        "opt_a": ["websites for study", "useful information"],
        "opt_b": ["books only", "pop-up spam"],
        "impact": ["saves search time", "helps group work", "can waste attention if I scroll too long"],
        "child_examples": ["paper textbooks", "TV commercials", "asking teachers directly"],
        "change_a": ["fast online search", "class group chats"],
        "change_b": ["only paper notes", "slow information"],
        "third_why": ["platforms push repeated ads", "students need quick answers", "attention is easy to lose"],
    },
    "hometown_life": {
        "id": "hometown_life",
        "nameZh": "回家与习惯",
        "summary": "家乡街道、本地食物、礼貌、老同学——回家就能用的记忆。",
        "people": ["my parents", "old classmates", "neighbors back home"],
        "places": ["my hometown", "familiar streets", "secondary school"],
        "objects": ["local food", "family photos", "old school notes"],
        "beats": {
            "now": "When I go back, local food and familiar streets feel warm",
            "childhood": "secondary school routines and polite habits at home",
            "change": "I notice hometown feels slower than my study city",
            "contrast_a": "familiar streets and local food",
            "contrast_b": "a rushed big-city pace every holiday",
            "feel": "warm and nostalgic",
        },
        "open": ["Yes, I do", "When I go back", "In my hometown"],
        "examples": ["my hometown", "local food", "familiar streets", "old classmates"],
        "freq": ["in the holiday", "once or twice a year", "when I call home"],
        "feel": ["warm", "familiar", "nostalgic"],
        "why": ["family is nearby", "the food tastes like home", "people are polite in small ways"],
        "opt_a": ["staying close to family habits", "local food"],
        "opt_b": ["never going back", "only big-city holidays"],
        "impact": ["keeps family ties", "reminds me to be polite", "gives me a slower reset"],
        "child_examples": ["secondary-school days", "saying thank you at home", "local festival food"],
        "change_a": ["valuing hometown visits", "keeping polite habits"],
        "change_b": ["ignoring family routines", "only chasing city speed"],
        "third_why": ["hometown food carries memory", "politeness reduces conflict", "young people leave then return for holidays"],
    },
}


# 题目主语锚点：换素材只换场景/理由，不能把「鞋子题」答成「我选地铁」
TOPIC_ANCHORS: dict[str, dict[str, Any]] = {
    "work or studies": {
        "examples": ["business major", "campus classes", "library work", "assignments"],
        "why": ["it matches my strengths", "it leads to a clearer career path", "I can take related courses"],
        "child_examples": ["simple school subjects", "homework after class", "a patient teacher"],
    },
    "shoes": {
        "examples": ["sneakers", "a comfortable pair", "school shoes", "new shoes"],
        "why": ["comfort matters most", "they are good for walking", "I need them every day"],
        "child_examples": ["school shoes", "simple sneakers", "a pair from my parents"],
        "opt_a": ["comfort", "sneakers"],
        "opt_b": ["style", "fashion shoes"],
    },
    "websites": {
        "examples": ["study websites", "search tools", "Xiaohongshu", "short-video sites"],
        "why": ["it is fast to search", "there are rich study resources", "the information stays up to date"],
        "opt_a": ["websites", "online search"],
        "opt_b": ["books", "paper notes"],
    },
    "headphones": {
        "examples": ["wireless earbuds", "noise blocking", "music playlists", "subway rides"],
        "why": ["they block noise", "I can focus better", "I can enjoy music"],
    },
    "tidiness": {
        "examples": ["a tidy desk", "storage boxes", "clean shelves", "put-away habits"],
        "why": ["I can focus better", "it saves time", "I feel calm"],
    },
    "singing": {
        "examples": ["KTV nights", "favourite songs", "singing with friends", "music class"],
        "why": ["it cheers me up", "I can spend time with friends", "it helps me release stress"],
        "child_examples": ["nursery rhymes", "simple school songs", "karaoke with family"],
    },
    "science": {
        "examples": ["science class", "simple experiments", "biology", "museum visits"],
        "why": ["I am curious about experiments", "biology feels useful", "museum visits inspire me"],
    },
    "name": {
        "examples": ["my given name", "its meaning", "my parents' choice", "a nickname"],
        "why": ["my parents chose it", "it has a positive meaning", "it is easy to remember"],
    },
    "rubbish and recycling": {
        "examples": ["recycling bins", "sorted rubbish", "plastic bottles", "paper waste"],
        "why": ["it protects the environment", "it helps reduce waste", "it is a good habit"],
        "opt_a": ["sorting rubbish", "using recycle bins"],
        "opt_b": ["throwing everything together", "ignoring recycling"],
        "child_examples": ["putting trash in a bin", "paper collection at school"],
    },
    "feeling bored": {
        "examples": ["a walk outside", "short playlists", "hanging out", "a quick chat"],
        "why": ["I can kill time wisely", "I can see friends", "it changes the environment for a while"],
        "child_examples": ["drawing at home", "playing outside", "simple board games"],
        "third_why": ["phones offer endless options", "attention spans get shorter", "people expect constant stimulation"],
    },
    "home & accommodation": {
        "examples": ["campus dorms", "a rented apartment", "my roommate", "the living room"],
        "why": ["it is near the subway", "I can share costs", "it is quiet enough"],
    },
    "fruit and vegetables": {
        "examples": ["fresh fruit", "cooked vegetables", "tomato dishes", "canteen vegetables"],
        "why": ["it helps me stay healthy", "the food tastes good", "it is easy to cook"],
        "child_examples": ["bitter vegetables", "fruit after meals", "tomato dishes"],
    },
    "watch": {
        "examples": ["a simple watch", "a smartwatch", "checking the time", "before class"],
        "why": ["it helps me stay punctual", "I can check the time quickly", "no phone is needed"],
    },
    "public gardens and parks": {
        "examples": ["a nearby park", "evening walks", "fresh air", "benches under trees"],
        "why": ["there is fresh air", "I can relax", "I can meet friends"],
    },
    "clothing": {
        "examples": ["a simple t-shirt", "a coat", "casual clothes", "comfortable outfits"],
        "why": ["it feels comfortable", "it is easy to match", "it fits the weather"],
        "opt_a": ["comfortable casual clothes", "a simple t-shirt"],
        "opt_b": ["formal clothes", "trendy outfits"],
        "child_examples": ["clothes from my parents", "a school uniform", "a winter coat"],
    },
    "shopping": {
        "examples": ["online shops", "shopping malls", "weekend bargains", "careful returns"],
        "why": ["I can compare prices", "returns are easy", "it saves time"],
    },
    "outer space and stars": {
        "examples": ["space documentaries", "night sky apps", "star photos", "sci-fi clips"],
        "why": ["I am curious about space", "the visuals are amazing", "it is relaxing at night"],
        "child_examples": ["picture books about planets", "star stickers", "space cartoons"],
    },
    "advertisements": {
        "examples": ["phone ads", "subway screens", "catchy slogans", "product offers"],
        "why": ["the music is catchy", "the offers are clear", "repeated exposure sticks"],
        "child_examples": ["TV commercials", "cartoon ads", "jingles on TV"],
        "opt_a": ["useful product ads", "clear information"],
        "opt_b": ["pop-up spam", "misleading claims"],
    },
    "teachers": {
        "examples": ["my favourite teacher", "clear explanations", "patient feedback", "encouragement"],
        "why": ["teachers give patient explanations", "I get real encouragement", "there are clear examples"],
    },
    "opportunities": {
        "examples": ["an internship offer", "a campus contest", "a part-time project", "a workshop"],
        "why": ["it supports career growth", "I can learn new skills", "I want to avoid regret"],
    },
    "travelling": {
        "examples": ["nature spots", "coastal towns", "city trips", "short weekend travel"],
        "why": ["I can see new places", "it gives me family time", "I can enjoy nature"],
        "opt_a": ["travelling with other people", "nature trips"],
        "opt_b": ["travelling alone", "busy city tours"],
        "child_examples": ["family holidays", "short city trips", "seaside weekends"],
    },
    "the area you live in": {
        "examples": ["a residential area", "friendly neighbors", "convenience stores", "quiet streets"],
        "why": ["it is quiet enough", "there are shops nearby", "neighbors are friendly"],
    },
    "social media": {
        "examples": ["WeChat chats", "Xiaohongshu posts", "class group chats", "short updates"],
        "why": ["I can keep in touch", "I can get information quickly", "I can share photos"],
    },
    "music": {
        "examples": ["happy playlists", "study music", "headphones", "new songs"],
        "why": ["it relieves stress", "it improves my mood", "it helps background focus"],
        "child_examples": ["school music class", "singing with family", "a cheap keyboard"],
    },
    "cars": {
        "examples": ["a practical car", "comfortable seats", "family car trips", "rush-hour traffic"],
        "why": ["there is more space", "it is better for family travel", "it is door-to-door"],
        "opt_a": ["being a passenger", "comfortable seats"],
        "opt_b": ["driving in rush hour", "standing on a bus"],
        "child_examples": ["family car trips", "looking out of the window", "long holiday rides"],
        "change_a": ["electric cars", "self-driving features"],
        "change_b": ["petrol-only cars", "heavy traffic stress"],
    },
    "paper": {
        "examples": ["a notebook", "handwritten notes", "printouts", "recycled paper"],
        "why": ["it helps memory", "there are fewer distractions", "it is easy to review"],
        "opt_a": ["writing by hand", "a paper notebook"],
        "opt_b": ["only on a screen", "typing everything"],
    },
    "politeness": {
        "examples": ["saying thank you", "holding the door", "respectful words", "helping strangers"],
        "why": ["it shows respect", "it makes others comfortable", "it shows good manners"],
    },
    "secondary school": {
        "examples": ["favourite subjects", "close classmates", "school breaks", "simple routines"],
        "why": ["I stay close to classmates", "the subjects are interesting", "the routine is simple"],
    },
    "tiredness": {
        "examples": ["heavy assignments", "too much screen time", "poor sleep", "afternoon slump"],
        "why": ["there is too much screen time", "assignments feel heavy", "sleep becomes poor"],
    },
    "jokes & comedies": {
        "examples": ["funny jokes", "comedy shows", "laughing with friends", "light clips"],
        "why": ["it helps me release stress", "we can share laughs", "I enjoy the stories"],
    },
    "hometown": {
        "examples": ["my hometown", "local food", "familiar streets", "family nearby"],
        "why": ["I like the local food", "the streets feel familiar", "my family is nearby"],
    },
    "street markets": {
        "examples": ["street food stalls", "small bargains", "fresh fruit", "a lively market"],
        "why": ["there is fresh fruit", "I can find cheap bargains", "the atmosphere is lively"],
        "opt_a": ["a street market", "street food"],
        "opt_b": ["a shopping mall", "supermarket only"],
    },
    "mirrors": {
        "examples": ["the hallway mirror", "a quick look check", "getting dressed", "before heading out"],
        "why": ["I can check my look", "I can get dressed properly", "I feel ready"],
    },
    "the city you live in": {
        "examples": ["the subway", "friendly people", "campus areas", "city parks"],
        "why": ["the subway is convenient", "people are friendly", "there are more opportunities"],
    },
}


TOPIC_BIND: dict[str, dict[str, Any]] = {
    "work or studies": {
        "primaryKitId": "study_campus",
        "altKitIds": ["home_dorm", "commute_city"],
        "angle": "campus classes and library blocks",
    },
    "shoes": {
        "primaryKitId": "wear_daily",
        "altKitIds": ["commute_city", "study_campus"],
        "angle": "sneakers for campus walking and commuting",
    },
    "websites": {
        "primaryKitId": "phone_tools",
        "altKitIds": ["study_campus", "leisure_reset"],
        "angle": "study search and light browsing",
    },
    "headphones": {
        "primaryKitId": "wear_daily",
        "altKitIds": ["commute_city", "leisure_reset"],
        "angle": "earbuds on the subway and while studying",
    },
    "tidiness": {
        "primaryKitId": "home_dorm",
        "altKitIds": ["study_campus", "wear_daily"],
        "angle": "tidy desk before study",
    },
    "singing": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["phone_tools", "hometown_life"],
        "angle": "songs with friends after a reset",
    },
    "science": {
        "primaryKitId": "study_campus",
        "altKitIds": ["phone_tools", "leisure_reset"],
        "angle": "class experiments and curious topics",
    },
    "name": {
        "primaryKitId": "hometown_life",
        "altKitIds": ["study_campus", "home_dorm"],
        "angle": "parents chose a name with meaning",
    },
    "rubbish and recycling": {
        "primaryKitId": "home_dorm",
        "altKitIds": ["commute_city", "hometown_life"],
        "angle": "sorting bins in the dorm",
    },
    "feeling bored": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["phone_tools", "food_campus"],
        "angle": "go outside instead of empty scrolling",
    },
    "home & accommodation": {
        "primaryKitId": "home_dorm",
        "altKitIds": ["commute_city", "study_campus"],
        "angle": "dorms near campus and roommate life",
    },
    "fruit and vegetables": {
        "primaryKitId": "food_campus",
        "altKitIds": ["hometown_life", "home_dorm"],
        "angle": "canteen vegetables and fruit after class",
    },
    "watch": {
        "primaryKitId": "wear_daily",
        "altKitIds": ["study_campus", "commute_city"],
        "angle": "a simple watch for punctual days",
    },
    "public gardens and parks": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["commute_city", "home_dorm"],
        "angle": "nearby park walks after study",
    },
    "clothing": {
        "primaryKitId": "wear_daily",
        "altKitIds": ["hometown_life", "study_campus"],
        "angle": "simple t-shirt and casual campus wear",
    },
    "shopping": {
        "primaryKitId": "food_campus",
        "altKitIds": ["wear_daily", "phone_tools"],
        "angle": "weekend stalls and careful daily buys",
    },
    "outer space and stars": {
        "primaryKitId": "phone_tools",
        "altKitIds": ["leisure_reset", "study_campus"],
        "angle": "documentaries and curious night clips",
    },
    "advertisements": {
        "primaryKitId": "phone_tools",
        "altKitIds": ["commute_city", "wear_daily"],
        "angle": "subway screens and phone feed ads",
    },
    "teachers": {
        "primaryKitId": "study_campus",
        "altKitIds": ["hometown_life", "phone_tools"],
        "angle": "patient explanations in class",
    },
    "opportunities": {
        "primaryKitId": "study_campus",
        "altKitIds": ["phone_tools", "commute_city"],
        "angle": "campus contests and internship notices",
    },
    "travelling": {
        "primaryKitId": "commute_city",
        "altKitIds": ["hometown_life", "leisure_reset"],
        "angle": "short trips and holiday visits home",
    },
    "the area you live in": {
        "primaryKitId": "commute_city",
        "altKitIds": ["home_dorm", "hometown_life"],
        "angle": "residential streets near the station",
    },
    "social media": {
        "primaryKitId": "phone_tools",
        "altKitIds": ["study_campus", "leisure_reset"],
        "angle": "WeChat groups and limited scrolling",
    },
    "music": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["wear_daily", "commute_city"],
        "angle": "playlists with earbuds on the way",
    },
    "cars": {
        "primaryKitId": "commute_city",
        "altKitIds": ["hometown_life", "wear_daily"],
        "angle": "family rides vs daily subway habit",
    },
    "paper": {
        "primaryKitId": "study_campus",
        "altKitIds": ["home_dorm", "phone_tools"],
        "angle": "notebook handwriting for memory",
    },
    "politeness": {
        "primaryKitId": "hometown_life",
        "altKitIds": ["home_dorm", "commute_city"],
        "angle": "thank you and small daily manners",
    },
    "secondary school": {
        "primaryKitId": "hometown_life",
        "altKitIds": ["study_campus", "leisure_reset"],
        "angle": "old classmates and simple school days",
    },
    "tiredness": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["study_campus", "home_dorm"],
        "angle": "screen fatigue then a short reset",
    },
    "jokes & comedies": {
        "primaryKitId": "leisure_reset",
        "altKitIds": ["phone_tools", "hometown_life"],
        "angle": "light laughs with friends after study",
    },
    "hometown": {
        "primaryKitId": "hometown_life",
        "altKitIds": ["food_campus", "commute_city"],
        "angle": "local food and familiar streets",
    },
    "street markets": {
        "primaryKitId": "food_campus",
        "altKitIds": ["hometown_life", "commute_city"],
        "angle": "weekend stalls and fresh fruit",
    },
    "mirrors": {
        "primaryKitId": "wear_daily",
        "altKitIds": ["home_dorm", "study_campus"],
        "angle": "quick look check before heading out",
    },
    "the city you live in": {
        "primaryKitId": "commute_city",
        "altKitIds": ["study_campus", "food_campus"],
        "angle": "subway city life around campus",
    },
}


def normalize_topic(topic_en: str) -> str:
    return (topic_en or "").strip().lower()


def get_kit(kit_id: str) -> dict[str, Any] | None:
    return CORE_KITS.get((kit_id or "").strip())


def get_topic_bind(topic_en: str) -> dict[str, Any] | None:
    return TOPIC_BIND.get(normalize_topic(topic_en))


def get_topic_anchors(topic_en: str) -> dict[str, Any] | None:
    return TOPIC_ANCHORS.get(normalize_topic(topic_en))


def kit_ids_for_topic(topic_en: str) -> list[str]:
    bind = get_topic_bind(topic_en)
    if not bind:
        return ["study_campus", "home_dorm"]
    ids = [bind["primaryKitId"]] + list(bind.get("altKitIds") or [])
    out: list[str] = []
    for i in ids:
        if i in CORE_KITS and i not in out:
            out.append(i)
    return out or ["study_campus"]


def primary_kit_id(topic_en: str) -> str:
    ids = kit_ids_for_topic(topic_en)
    return ids[0]


def kit_to_pool(kit: dict[str, Any], topic_en: str = "") -> dict[str, Any]:
    bind = get_topic_bind(topic_en) or {}
    angle = bind.get("angle") or kit.get("summary") or ""
    chips = list(kit.get("examples") or ["a clear example"])
    return {
        "kitId": kit["id"],
        "kitNameZh": kit.get("nameZh") or kit["id"],
        "kitSummary": kit.get("summary") or "",
        "mat": f"{kit.get('nameZh') or kit['id']}：{angle}",
        "logic": (
            f"P1 日常素材【{kit.get('nameZh')}】（与 P2 长故事分开）；"
            f"本题角度：{angle}。一道题可换套，一套可串多题；连问只取本题片段。"
        ),
        "open": list(kit.get("open") or ["Yes", "Definitely", "Sure"]),
        "examples": chips,
        "freq": list(kit.get("freq") or ["every day", "at weekends", "from time to time"]),
        "feel": list(kit.get("feel") or ["practical", "quite useful"]),
        "why": list(kit.get("why") or chips[:3]),
        "opt_a": list(kit.get("opt_a") or chips[:2]),
        "opt_b": list(kit.get("opt_b") or list(reversed(chips[:2]))),
        "impact": list(kit.get("impact") or ["makes life easier", "keeps me positive"]),
        "story": list(kit.get("beats", {}).values()) if isinstance(kit.get("beats"), dict) else [],
        "child_examples": list(kit.get("child_examples") or []),
        "change_a": list(kit.get("change_a") or kit.get("opt_a") or chips[:2]),
        "change_b": list(kit.get("change_b") or kit.get("opt_b") or list(reversed(chips[:2]))),
        "third_why": list(kit.get("third_why") or []),
        "beats": dict(kit.get("beats") or {}),
        "angle": angle,
    }


def export_kits_for_js() -> dict[str, Any]:
    return {
        "kits": [
            {
                "id": k["id"],
                "nameZh": k["nameZh"],
                "summary": k["summary"],
            }
            for k in CORE_KITS.values()
        ],
        "topicBind": {
            t: {
                "primaryKitId": b["primaryKitId"],
                "altKitIds": list(b.get("altKitIds") or []),
                "kitIds": kit_ids_for_topic(t),
                "angle": b.get("angle") or "",
            }
            for t, b in TOPIC_BIND.items()
        },
    }
