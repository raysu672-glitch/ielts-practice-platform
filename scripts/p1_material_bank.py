# -*- coding: utf-8 -*-
"""
P1 composable life-material bank — adapted from classroom PDF《P1素材》
(衣食住行 / 高频行为爱好 / 时间线 / 感受 / 同义替换 / 万能句式)
and mapped onto the current-season topic list.
"""
from __future__ import annotations

import re
from typing import Any


def _norm_q(s: str) -> str:
    s = (s or "").lower().strip()
    return re.sub(r"[^a-z0-9]+", "", s)

# —— PDF 模块五：同义替换（示范与词卡可轮换）——
FEEL_RELAX = [
    "helps me chill out",
    "helps me sit down and relax",
    "helps me take a break and relax",
    "helps me relax my mind",
    "helps me slow down",
]
FEEL_STRESS = [
    "helps me relieve stress",
    "is a great stress buster",
    "helps me de-stress",
    "helps reduce stress",
]
FEEL_HAPPY = [
    "makes me happy",
    "helps to light up my mood",
    "gives me a good feeling",
    "helps me enjoy a good laugh",
]
FEEL_PRACTICAL = [
    "practical",
    "really convenient",
    "quite useful",
    "useful for my future job",
]
FREQ_OFTEN = [
    "regularly",
    "as often as I can",
    "from time to time",
    "every weekday",
    "in my spare time",
    "when I have time to kill",
]
TIME_LINE = [
    "in childhood",
    "before I went to primary school",
    "after I went to middle school",
    "when I started university",
    "after I get up",
    "before I go out",
    "before I go to sleep",
    "in my free time",
]

# kinds: 衣 / 食 / 住 / 行 / 地点 / 行为 / 爱好 / 社交 / 学习 / 媒介
MATERIALS: dict[str, dict[str, Any]] = {
    # ========== 模块一：衣食住行 & 地点 ==========
    "campus_tee_coat": {
        "id": "campus_tee_coat",
        "nameZh": "T恤外套穿搭",
        "kind": "衣·穿戴",
        "module": "衣食住行",
        "summary": "PDF衣：t-shirt / coat / sweatshirt；出门 get dressed。",
        "topics": ["clothing", "tidiness"],
        "open": {
            "yes": ["Yes, I do", "Most weekdays", "Yes, casual clothes"],
            "kind": ["a simple t-shirt", "a coat", "a sweatshirt"],
            "prefer": ["I prefer comfortable clothes", "I'd rather choose comfort", "Comfort comes first"],
        },
        "origins": [
            "After I went to middle school my mum started buying me simple t-shirts and a coat for campus",
            "When I started university I kept the same casual look — t-shirt, sweatshirt, and a coat",
        ],
        "routes": [
            {"freq": "every weekday after I get up", "feel": "loose and comfortable", "impact": "helps me get dressed quickly before I head out"},
            {"freq": "before I go out", "feel": "practical", "impact": "makes me look neat without spending extra hours"},
        ],
    },
    "hallway_mirror_routine": {
        "id": "hallway_mirror_routine",
        "nameZh": "出门照镜子",
        "kind": "衣·习惯",
        "module": "衣食住行",
        "summary": "PDF日常：look at myself in the mirror / get dressed / head out。",
        "topics": ["mirrors", "politeness", "home & accommodation", "tidiness"],
        "open": {
            "yes": ["Yes, I do", "Every morning", "Yes, before heading out"],
            "kind": ["look at myself in the mirror", "a quick check by the door", "a hallway mirror"],
            "prefer": ["I prefer a quick check", "I'd rather look once before leaving", "A mirror by the door is enough"],
        },
        "origins": [
            "The first thing I do after I get up is get dressed and look at myself in the mirror",
            "Before I go out I always grab my stuff and check the hallway mirror",
        ],
        "routes": [
            {"freq": "every weekday before I go out", "feel": "practical", "impact": "helps me head out looking neat"},
            {"freq": "when I change jackets", "feel": "necessary", "impact": "avoids awkward looks in public"},
        ],
    },
    "campus_sweatshirt": {
        "id": "campus_sweatshirt",
        "nameZh": "卫衣外套",
        "kind": "衣·穿戴",
        "module": "衣食住行",
        "summary": "PDF衣：sweatshirt / coat；冷天校园穿。",
        "topics": ["clothing", "tiredness"],
        "open": {
            "yes": ["Yes, I do", "In cooler weather", "Yes, a sweatshirt"],
            "kind": ["a sweatshirt", "a coat", "casual campus clothes"],
            "prefer": ["I prefer a sweatshirt", "I'd rather wear a coat", "Casual clothes come first"],
        },
        "origins": [
            "After I went to middle school I started wearing a sweatshirt and coat on campus",
            "When I started university I kept a thick coat for cold mornings",
        ],
        "routes": [
            {"freq": "every weekday in cool weather", "feel": "loose and comfortable", "impact": "keeps me warm before I head out"},
            {"freq": "when I go for a walk after class", "feel": "practical", "impact": "is easy to put on before I head out"},
        ],
    },
    "campus_sneakers": {
        "id": "campus_sneakers",
        "nameZh": "舒适球鞋",
        "kind": "衣·鞋子",
        "module": "衣食住行",
        "summary": "校园走路/通勤；舒适优先于款式。",
        "topics": ["shoes", "tiredness", "travelling"],
        "open": {
            "yes": ["Yes, I do", "Most days", "Yes, sneakers"],
            "kind": ["comfortable sneakers", "a simple pair", "school shoes"],
            "prefer": ["I prefer comfort", "I'd rather choose sneakers", "Comfort matters more than style"],
        },
        "origins": [
            "My parents bought me a comfortable pair before the new school term",
            "In childhood I mostly wore school shoes; now I stick to sneakers",
        ],
        "routes": [
            {"freq": "every weekday on campus", "feel": "loose and comfortable", "impact": "protects my feet when I go for a walk"},
            {"freq": "at weekends when I go jogging", "feel": "practical", "impact": "helps me do some sports without sore feet"},
        ],
    },
    "style_shoes_weekend": {
        "id": "style_shoes_weekend",
        "nameZh": "周末好看的鞋",
        "kind": "衣·鞋子",
        "module": "衣食住行",
        "summary": "平时球鞋，周末偶尔穿更有型的鞋。",
        "topics": ["shoes", "clothing", "shopping"],
        "open": {
            "yes": ["Yes, sometimes", "At weekends", "For style"],
            "kind": ["a stylish pair", "weekend shoes", "shoes that look nicer"],
            "prefer": ["I prefer comfort on weekdays", "I'd rather choose style at weekends", "It depends on the day"],
        },
        "origins": [
            "I bought a nicer pair for weekends after I started university",
            "My roommate talked me into a stylish pair for hanging out",
        ],
        "routes": [
            {"freq": "most weekends when I hang out", "feel": "makes me happy", "impact": "lets me show preferences without hurting my feet all week"},
            {"freq": "when I go shopping in the city centre", "feel": "practical", "impact": "still works for a short walk"},
        ],
    },
    "dressing_mirror_home": {
        "id": "dressing_mirror_home",
        "nameZh": "房间穿衣镜",
        "kind": "衣·习惯",
        "module": "衣食住行",
        "summary": "宿舍/租房里的穿衣镜；出门前整理。",
        "topics": ["mirrors", "home & accommodation", "clothing", "tidiness"],
        "open": {
            "yes": ["Yes, I do", "In my room", "Yes, a full-length one"],
            "kind": ["a dressing mirror", "a full-length mirror", "the mirror in my room"],
            "prefer": ["I prefer a full-length mirror", "I'd rather check in my room", "One mirror is enough"],
        },
        "origins": [
            "I put a full-length mirror in the dorm so I can get dressed properly",
            "When I rented an apartment I bought a cheap dressing mirror for the bedroom",
        ],
        "routes": [
            {"freq": "every morning before class", "feel": "practical", "impact": "helps me get dressed and head out with confidence"},
            {"freq": "before I go out at weekends", "feel": "necessary", "impact": "avoids awkward looks in public"},
        ],
    },
    "canteen_and_takeaways": {
        "id": "canteen_and_takeaways",
        "nameZh": "食堂与外卖",
        "kind": "食·日常",
        "module": "衣食住行",
        "summary": "PDF食：breakfast / the school canteen / takeaways / street food。",
        "topics": [
            "fruit and vegetables", "shopping", "street markets", "home & accommodation",
            "tiredness", "work or studies", "hometown",
        ],
        "open": {
            "yes": ["Yes, I do", "Most weekdays", "Yes, at the canteen"],
            "kind": ["the school canteen", "takeaways", "street food"],
            "prefer": ["I prefer the canteen", "I'd rather eat street food", "Canteen meals feel easier"],
        },
        "origins": [
            "When I started university I got used to breakfast and dinner at the school canteen",
            "In my spare time I also pig out on tasty local street food near campus",
        ],
        "routes": [
            {"freq": "every weekday after classes", "feel": "delicious", "impact": "keeps me full without spending extra hours cooking"},
            {"freq": "when I feel bored at weekends", "feel": "makes me happy", "impact": "lets me enjoy street food with friends"},
        ],
    },
    "fruit_groceries": {
        "id": "fruit_groceries",
        "nameZh": "水果生鲜",
        "kind": "食·蔬果",
        "module": "衣食住行",
        "summary": "PDF食：groceries / food ingredients；水果维生素。",
        "topics": ["fruit and vegetables", "shopping", "street markets", "tiredness", "feeling bored"],
        "open": {
            "yes": ["Yes, I do", "Quite often", "Yes, fresh fruit"],
            "kind": ["fresh fruit", "vegetables", "groceries"],
            "prefer": ["I prefer fresh fruit", "I'd rather buy groceries nearby", "Fruit feels healthier"],
        },
        "origins": [
            "There is a convenience store just about 10 minutes' walk away from my dorm, and I buy fruit there",
            "My mum kept telling me to eat fruit, so after classes I grab some groceries",
        ],
        "routes": [
            {"freq": "most weekdays after class", "feel": "helps to light up my mood", "impact": "gives me a quick energy boost"},
            {"freq": "when I feel sleepy in the afternoon", "feel": "practical", "impact": "is better than takeaways for my health"},
        ],
    },
    "dorm_apartment_life": {
        "id": "dorm_apartment_life",
        "nameZh": "宿舍租房生活",
        "kind": "住·居所",
        "module": "衣食住行",
        "summary": "PDF住：dorms / renting an apartment / residential areas。",
        "topics": [
            "home & accommodation", "the area you live in", "the city you live in",
            "tidiness", "rubbish and recycling", "tiredness",
        ],
        "qHints": {
            "tidiness": (
                "are you a tidy", "keep things tidy", "necessary to be tidy",
                "tidy your room", "do you like to keep",
            ),
        },
        "open": {
            "yes": ["I live in dorms", "I rent an apartment", "In a residential area"],
            "kind": ["campus dorms", "a rented apartment", "a residential area"],
            "prefer": ["I prefer dorms for now", "I'd rather rent near the subway", "A quiet residential area fits me"],
        },
        "origins": [
            "When I started university I moved into campus dorms with my roommate",
            "Later I tried renting an apartment in a residential area about 10 minutes' walk from the subway",
        ],
        "routes": [
            {"freq": "every evening at home", "feel": "loose and comfortable", "impact": "gives me some me time after classes"},
            {"freq": "at weekends when I stay home", "feel": "practical", "impact": "helps me finish homework independently"},
        ],
    },
    "tidy_desk_habit": {
        "id": "tidy_desk_habit",
        "nameZh": "书桌收纳",
        "kind": "住·整洁",
        "module": "衣食住行",
        "summary": "宿舍书桌收拾；方便学习。",
        # 不对 Work or studies 硬挂：书桌整洁答身份/选专业/职业规划会突兀（硬规则5）
        "topics": ["tidiness", "home & accommodation", "paper", "mirrors"],
        "open": {
            "yes": ["Yes, I try to", "Most of the time", "Yes, before studying"],
            "kind": ["a tidy desk", "put things away", "storage boxes"],
            "prefer": ["I prefer a tidy desk", "I'd rather put things away", "A clear desk works better"],
        },
        "origins": [
            "My roommate and I agreed to tidy the desk every night after the first messy month",
            "After I went to middle school I learned to put things away before I go to sleep",
        ],
        "routes": [
            {"freq": "every evening before I study", "feel": "practical", "impact": "helps me strive in my studies with a clear desk"},
            {"freq": "every weekend morning", "feel": "helps me chill out", "impact": "reduces small conflicts in the dorm"},
        ],
    },
    "parents_tidy_home": {
        "id": "parents_tidy_home",
        "nameZh": "父母整理房间",
        "kind": "住·整洁",
        "module": "衣食住行",
        "summary": "童年父母整理；整洁题第二套。",
        "topics": ["tidiness", "home & accommodation"],
        "open": {
            "yes": ["My mum did", "My parents mostly", "Yes, at home"],
            "kind": ["my mum kept the room tidy", "parents' cleaning routine", "weekend deep clean"],
            "prefer": ["I preferred when mum helped", "I'd rather tidy with family", "A clean room felt calmer"],
        },
        "origins": [
            "When I was a child my mum mostly kept my room tidy and asked me to put toys away",
            "My parents did a deeper clean every weekend while I only handled small things",
        ],
        "routes": [
            {"freq": "every weekend at home", "feel": "warm", "impact": "made me notice a clear desk later"},
            {"freq": "after school in the evening", "feel": "organised", "impact": "reduced arguments about mess"},
        ],
    },
    "recycle_bins_floor": {
        "id": "recycle_bins_floor",
        "nameZh": "楼层垃圾分类",
        "kind": "住·环保",
        "module": "衣食住行",
        "summary": "纸壳塑料分开扔；宿舍楼层分类桶。",
        "topics": ["rubbish and recycling", "paper", "home & accommodation", "the area you live in", "politeness"],
        "open": {
            "yes": ["Yes, I do", "I try to", "At home and in the dorm, yes"],
            "kind": ["recycling bins", "sorted rubbish", "paper and plastic"],
            "prefer": ["I prefer sorting rubbish", "I'd rather use the recycle bins", "Sorting feels responsible"],
        },
        "origins": [
            "Our dorm building put recycling bins on each floor, and the notice made it hard to ignore",
            "A cleaner once reminded me politely, and I started separating paper and bottles after that",
        ],
        "routes": [
            {"freq": "every day after meals", "feel": "practical", "impact": "keeps the shared kitchen cleaner"},
            {"freq": "whenever I finish online parcels", "feel": "responsible", "impact": "helps reduce waste in our residential area"},
        ],
    },
    "subway_bus_commute": {
        "id": "subway_bus_commute",
        "nameZh": "地铁公交通勤",
        "kind": "行·出行",
        "module": "衣食住行",
        "summary": "PDF行：use the subway / take a bus；rush hour。",
        "topics": [
            "cars", "travelling", "the city you live in", "the area you live in",
            "tiredness",
        ],
        "qHints": {
            "travelling": ("travel", "trip", "commute", "get around", "subway", "bus", "holiday"),
            "cars": (
                "car", "drive", "traffic", "commute", "subway", "bus", "get around",
                "own", "journey", "passenger", "jam",
            ),

            "the city you live in": ("city", "live", "subway", "bus", "get around", "transport"),
            "the area you live in": ("area", "live", "subway", "bus", "nearby", "transport"),
            "tiredness": ("tired", "commute", "subway", "rest"),
        },
        "open": {
            "yes": ["Yes, I do", "By subway", "Most weekdays"],
            "kind": ["the subway", "a bus ride", "subway plus a short walk"],
            "prefer": ["I prefer the subway", "I'd rather take the metro", "The subway is more reliable"],
        },
        "origins": [
            "I chose a route with a subway station about 10 minutes' walk from my place when I moved here",
            "After missing too many buses in rain, I switched to the subway as my default",
        ],
        "routes": [
            {"freq": "every weekday in rush hour", "feel": "practical", "impact": "keeps my day reliable on busy mornings"},
            {"freq": "every weekday with a short walk", "feel": "really convenient", "impact": "lets me browse videos or review notes on the train"},
        ],
    },
    "family_car_passenger": {
        "id": "family_car_passenger",
        "nameZh": "全家开车出行",
        "kind": "行·汽车",
        "module": "衣食住行",
        "summary": "PDF行：drive a car；假期当乘客。",
        "topics": ["cars", "travelling", "hometown", "tiredness"],
        "open": {
            "yes": ["Yes, as a passenger", "On family trips", "Sometimes by car"],
            "kind": ["a family car", "short road trips", "riding as a passenger"],
            "prefer": ["I prefer being a passenger", "I'd rather sit by the window", "Family trips by car feel easier"],
        },
        "origins": [
            "In childhood my parents drove to nearby towns, and I sat by the window",
            "After I went to middle school we still took short car journeys in the holiday",
        ],
        "routes": [
            {"freq": "once or twice a year in the holiday", "feel": "helps me chill out", "impact": "creates family time without rushing"},
            {"freq": "on short weekend trips", "feel": "loose and comfortable", "impact": "beats standing on a crowded bus"},
        ],
    },
    "yellow_bike_gift": {
        "id": "yellow_bike_gift",
        "nameZh": "黄色小自行车",
        "kind": "行·单车",
        "module": "衣食住行",
        "summary": "可控 Freestyle 核心套装：童年新活动/开学日/公园/疲倦放松/出行；不挂名字折纸拾金。",
        "topics": [
            "opportunities", "secondary school", "public gardens and parks",
            "tiredness", "travelling", "feeling bored",
        ],
        "qHints": {
            "opportunities": ("activit", "child", "younger", "as a child", "when you were"),
            "secondary school": ("secondary", "first day", "school", "classmate"),
            "public gardens and parks": ("park", "garden"),
            "tiredness": ("tired", "relax", "rest", "unwind"),
            "travelling": ("travel", "trip", "journey", "bike", "cycle", "window"),
            "feeling bored": ("bored", "boring", "bike", "cycle", "park"),
        },
        "open": {
            "yes": ["Yes, I did", "Yes, I used to", "Yes, I had one"],
            "kind": ["a small yellow bike", "my yellow bike", "cycling in the park", "a new activity"],
            "prefer": ["I'd rather cycle", "I prefer cycling", "Cycling feels better"],
        },
        "origins": [
            "After I went to middle school my mum bought me a small yellow bike as a birthday gift",
            "When I entered junior high my sister gave me a bike as a graduation gift",
        ],
        "routes": [
            {"freq": "every weekday to school", "feel": "really convenient", "impact": "saved walking time for commuting"},
            {"freq": "at weekends in the park for about an hour", "feel": "helps me unwind", "impact": "gives me something active to do"},
        ],
    },
    "nearby_park_walk": {
        "id": "nearby_park_walk",
        "nameZh": "附近公园散步",
        "kind": "地点·公园",
        "module": "衣食住行",
        "summary": "PDF地点：park；万能句 10mins walk。",
        "topics": [
            "public gardens and parks", "feeling bored", "tiredness", "the area you live in",
            "travelling", "music", "jokes & comedies",
        ],
        "open": {
            "yes": ["Yes, I do", "At weekends", "When I feel bored"],
            "kind": ["a nearby park", "evening walks", "go for a walk"],
            "prefer": ["I prefer going outside", "I'd rather walk in the park", "A park walk feels better"],
        },
        "origins": [
            "There is a park just about 10 minutes' walk away from my dorm, and I found it when I needed a break",
            "My roommate started dragging me out after dinner, and it became our reset habit",
        ],
        "routes": [
            {"freq": "most evenings after study", "feel": "helps to light up my mood", "impact": "helps me chill out and clear my head"},
            {"freq": "when I feel bored at weekends", "feel": "helps me relieve stress", "impact": "beats endless scrolling on my phone"},
        ],
    },
    "mall_street_market": {
        "id": "mall_street_market",
        "nameZh": "商超与街市",
        "kind": "地点·购物",
        "module": "衣食住行",
        "summary": "PDF：shopping malls / street market / pay with my phone。",
        "topics": [
            "shopping", "street markets", "fruit and vegetables", "feeling bored",
            "hometown", "advertisements", "travelling",
        ],
        "open": {
            "yes": ["Yes, I do", "At weekends", "For street food"],
            "kind": ["shopping malls", "a street market", "convenience stores"],
            "prefer": ["I prefer a street market", "I'd rather shop in the mall", "Street markets feel more fun"],
        },
        "origins": [
            "I followed classmates to a weekend street market near campus for cheap fruit and snacks",
            "Back home we always walked night markets, so I look for the same feeling in this city",
        ],
        "routes": [
            {"freq": "most weekends in the evening", "feel": "makes me happy", "impact": "lets me pay with my phone and save money"},
            {"freq": "when I have time to kill", "feel": "helps to light up my mood", "impact": "is a nice way to hang out and pig out on local food"},
        ],
    },

    # ========== 模块二：高频行为与兴趣 ==========
    "study_library_classes": {
        "id": "study_library_classes",
        "nameZh": "上课与图书馆",
        "kind": "行为·学习",
        "module": "高频行为",
        "summary": "PDF：go to classes / study / library / flip through real books。",
        "topics": [
            "secondary school", "work or studies", "paper", "opportunities",
            "websites", "science",
        ],
        "open": {
            "yes": ["I'm a student", "Yes, I do", "Most weekdays"],
            "kind": ["go to classes", "library study", "flip through real books"],
            "prefer": ["I prefer the library", "I'd rather study on campus", "A quiet library works better"],
        },
        "origins": [
            "When I started university a classmate booked library seats with me, and the habit stuck",
            "I started going after failing a quiz, because my dorm was too noisy to focus",
        ],
        "routes": [
            {"freq": "every weekday after lunch", "feel": "practical", "impact": "helps me complete homework independently"},
            {"freq": "before exams every evening", "feel": "useful for my future job", "impact": "helps me strive in my studies"},
        ],
    },
    "business_major_path": {
        "id": "business_major_path",
        "nameZh": "商科专业日常",
        "kind": "行为·学习",
        "module": "高频行为",
        "summary": "学生线：business major + classes + future job。",
        "topics": ["work or studies", "opportunities", "paper", "websites"],
        "open": {
            "yes": ["I'm a student", "Yes, I study business", "Not working yet"],
            "kind": ["business major", "related courses", "group projects"],
            "prefer": ["I prefer finishing my degree first", "I'd rather study on campus", "Campus study fits me now"],
        },
        "origins": [
            "I chose business because the path looked clearer for internships and related courses",
            "After talking with seniors I stayed with this major instead of switching in the second year",
        ],
        "routes": [
            {"freq": "every weekday with classes and library time", "feel": "useful for my future job", "impact": "builds skills I can use later"},
            {"freq": "every term around group projects", "feel": "practical", "impact": "lets me share opinions and meet people with similar interests"},
        ],
    },
    "handwritten_notes_paper": {
        "id": "handwritten_notes_paper",
        "nameZh": "手写纸质笔记",
        "kind": "行为·学习",
        "module": "高频行为",
        "summary": "PDF：flip through the pages of real books / paper notes。",
        # 不对 Work or studies 硬挂：手写笔记挂身份/选专业/职业规划会突兀（硬规则5）
        "topics": ["secondary school", "paper", "websites", "science"],
        "open": {
            "yes": ["Yes, I do", "Quite often", "Yes, with a notebook"],
            "kind": ["handwritten notes", "real books", "paper worksheets"],
            "prefer": ["I prefer writing by hand", "I'd rather use paper", "Handwriting feels clearer"],
        },
        "origins": [
            "A teacher said photos disappear in the camera roll, so I went back to a notebook",
            "In secondary school I liked to flip through the pages of real books after class",
        ],
        "routes": [
            {"freq": "every weekday in class", "feel": "practical", "impact": "helps memory better than only screens"},
            {"freq": "before exams when I review", "feel": "focused", "impact": "makes revision easier"},
        ],
    },
    "phone_xiaohongshu_wechat": {
        "id": "phone_xiaohongshu_wechat",
        "nameZh": "手机刷短视频微信",
        "kind": "行为·媒介",
        "module": "高频行为",
        "summary": "PDF：douyin / xiaohongshu / wechat / browse videos / shop online。",
        "topics": [
            "social media", "websites", "feeling bored", "tiredness",
            "shopping", "headphones", "music",
        ],
        "open": {
            "yes": ["Yes, I do", "Every day", "Yes, mainly WeChat"],
            "kind": ["WeChat", "Xiaohongshu", "short videos on Douyin"],
            "prefer": ["I prefer WeChat for class news", "I'd rather check Xiaohongshu", "Group chats are enough"],
        },
        "origins": [
            "Every course created a WeChat group in week one, so it became my default notice board",
            "When I feel bored I spend a lot of time on Douyin and Xiaohongshu",
        ],
        "routes": [
            {"freq": "every day after class", "feel": "helps to light up my mood", "impact": "lets me connect with friends and family for free"},
            {"freq": "when I have time to kill on the subway", "feel": "makes me happy", "impact": "also makes it easy to get obsessed with short videos if I am not careful"},
        ],
    },
    "douyin_scroll_habit": {
        "id": "douyin_scroll_habit",
        "nameZh": "刷抖音短视频",
        "kind": "行为·媒介",
        "module": "高频行为",
        "summary": "PDF：browse videos / obsessed with short videos。",
        "topics": ["social media", "feeling bored", "tiredness", "advertisements"],
        "open": {
            "yes": ["Yes, I do", "Too often", "Yes, Douyin"],
            "kind": ["Douyin short videos", "browse videos", "funny clips"],
            "prefer": ["I'd rather browse short videos", "I prefer Douyin when bored", "Clips are enough"],
        },
        "origins": [
            "When I feel bored I open Douyin and browse videos without noticing the time",
            "My roommate got me into short videos during exam week as a quick break",
        ],
        "routes": [
            {"freq": "every evening before I go to sleep", "feel": "helps to light up my mood", "impact": "helps me chill out but I can get obsessed with short videos"},
            {"freq": "when I have time to kill", "feel": "makes me happy", "impact": "is a great stress buster if I set a limit"},
        ],
    },
    "study_websites_search": {
        "id": "study_websites_search",
        "nameZh": "查资料网站",
        "kind": "行为·学习",
        "module": "高频行为",
        "summary": "PDF学习+网站：search / study resources。",
        "topics": ["websites", "science", "paper", "opportunities", "advertisements"],
        "open": {
            "yes": ["Yes, I do", "Almost every day", "Yes, for study"],
            "kind": ["study websites", "search tools", "online resources"],
            "prefer": ["I prefer websites", "I'd rather search online", "Websites are faster for me"],
        },
        "origins": [
            "I started bookmarking two study sites after a project deadline felt impossible with only textbooks",
            "A teacher shared reliable links, and I reused them for later assignments",
        ],
        "routes": [
            {"freq": "every weekday before assignments", "feel": "really convenient", "impact": "I mainly use it for searching information quickly"},
            {"freq": "before exams when I check examples", "feel": "practical", "impact": "helps me understand faster"},
        ],
    },
    "wireless_earbuds_music": {
        "id": "wireless_earbuds_music",
        "nameZh": "耳机听歌",
        "kind": "爱好·音乐",
        "module": "高频行为",
        "summary": "PDF：listen to music / headphones；地铁降噪。",
        "topics": ["headphones", "music", "tiredness", "social media", "travelling", "singing"],
        "open": {
            "yes": ["Yes, I do", "Almost every day", "Yes, wireless ones"],
            "kind": ["wireless earbuds", "music playlists", "happy songs"],
            "prefer": ["I prefer earbuds", "I'd rather listen with headphones", "Music helps more than silence"],
        },
        "origins": [
            "I bought wireless earbuds for noisy subway rides after starting university",
            "One thing I like to do in my free time is listen to music to relax my mind",
        ],
        "routes": [
            {"freq": "every day on the subway", "feel": "helps me relieve stress", "impact": "blocks noise so I can review words"},
            {"freq": "while studying at night", "feel": "helps me chill out", "impact": "helps me finish assignments with a calmer mood"},
        ],
    },
    "focus_wired_headphones": {
        "id": "focus_wired_headphones",
        "nameZh": "有线耳机专注",
        "kind": "爱好·音乐",
        "module": "高频行为",
        "summary": "图书馆有线耳机；耳机题第二套，偏专注学习。",
        "topics": ["headphones", "music"],
        "open": {
            "yes": ["Yes, for study", "Wired ones", "In the library"],
            "kind": ["wired headphones", "study playlists", "soft instrumental tracks"],
            "prefer": ["I prefer wired headphones for study", "I'd rather block noise in the library", "Instrumental tracks help more"],
        },
        "origins": [
            "I keep a cheap wired pair in my bag for the library because batteries never die mid-essay",
            "After wireless earbuds ran out during an exam week, I switched to wired ones for study",
        ],
        "routes": [
            {"freq": "every weekday in the library", "feel": "helps me focus", "impact": "blocks chatter so I finish reading faster"},
            {"freq": "when I revise at night", "feel": "practical", "impact": "keeps me on task without scrolling"},
        ],
    },
    "school_choir_songs": {
        "id": "school_choir_songs",
        "nameZh": "学校课堂歌曲",
        "kind": "爱好·唱歌",
        "module": "高频行为",
        "summary": "童年课堂歌；唱歌题第二套。",
        "topics": ["singing", "secondary school", "music"],
        "open": {
            "yes": ["Yes, in music class", "Simple school songs", "When I was a child"],
            "kind": ["classroom songs", "children's songs", "school choir practice"],
            "prefer": ["I preferred simple songs", "I'd rather sing with classmates", "School songs felt easier"],
        },
        "origins": [
            "We sang simple children's songs and classroom songs in music class",
            "Sometimes the whole class practised a festival song together after lunch",
        ],
        "routes": [
            {"freq": "in music lessons every week", "feel": "warm", "impact": "made school days feel lighter"},
            {"freq": "before festivals at school", "feel": "enjoyable", "impact": "helped shy students join in"},
        ],
    },
    "singing_ktv_songs": {
        "id": "singing_ktv_songs",
        "nameZh": "唱歌KTV",
        "kind": "爱好·唱歌",
        "module": "高频行为",
        "summary": "PDF：sing a song；童年儿歌到KTV。",
        "topics": ["singing", "music", "jokes & comedies", "feeling bored"],
        "open": {
            "yes": ["Yes, I do", "With friends", "Quite often"],
            "kind": ["sing a song", "KTV nights", "simple school songs"],
            "prefer": ["I prefer singing with friends", "I'd rather go to KTV", "Shared songs feel better"],
        },
        "origins": [
            "One of my favourite things to do in my free time as a child was sing simple school songs",
            "I don't think I have a talent for singing, but I still enjoy KTV with classmates",
        ],
        "routes": [
            {"freq": "most weekends with friends", "feel": "helps me enjoy a good laugh", "impact": "is a nice way to hang out and light up my mood"},
            {"freq": "when I feel bored after exams", "feel": "makes me happy", "impact": "helps me de-stress quickly"},
        ],
    },
    "comedy_hang_out": {
        "id": "comedy_hang_out",
        "nameZh": "看喜剧和朋友玩",
        "kind": "爱好·娱乐",
        "module": "高频行为",
        "summary": "PDF：watch movies / hang out / enjoy a good laugh。",
        "topics": ["jokes & comedies", "feeling bored", "social media", "tiredness", "music", "singing"],
        "open": {
            "yes": ["Yes, I do", "With friends", "Quite often"],
            "kind": ["watch comedies", "funny clips", "hang out with friends"],
            "prefer": ["I prefer laughing with friends", "I'd rather watch light comedies", "Shared jokes feel better"],
        },
        "origins": [
            "Our dorm started a Friday night comedy playlist after a heavy week of deadlines",
            "I am not great at telling jokes, but hanging out and watching comedies always works",
        ],
        "routes": [
            {"freq": "most weekends in the dorm", "feel": "helps me enjoy a good laugh", "impact": "is a nice way to relieve stress"},
            {"freq": "when everyone feels tired", "feel": "makes me happy", "impact": "lets us catch up and share a good laugh"},
        ],
    },
    "light_sports_walk": {
        "id": "light_sports_walk",
        "nameZh": "散步慢跑运动",
        "kind": "爱好·运动",
        "module": "高频行为",
        "summary": "PDF运动：go for a walk / go jogging / do some sports / gym。",
        "topics": [
            "public gardens and parks", "tiredness", "feeling bored", "opportunities",
            "secondary school", "the area you live in",
        ],
        "open": {
            "yes": ["Yes, I do", "Quite often", "At weekends"],
            "kind": ["go for a walk", "go jogging", "do some sports"],
            "prefer": ["I prefer moving a bit", "I'd rather walk outside", "A short jog feels better"],
        },
        "origins": [
            "A roommate booked the gym during exam week and I realised moving resets me faster than scrolling",
            "After I went to middle school I rejoined casual sports because sitting all day made me restless",
        ],
        "routes": [
            {"freq": "twice a week after class", "feel": "good for the mind and the body", "impact": "helps me relieve stress"},
            {"freq": "at weekends in the park", "feel": "helps me chill out", "impact": "helps me sleep better"},
        ],
    },
    "patient_teacher_help": {
        "id": "patient_teacher_help",
        "nameZh": "耐心的老师",
        "kind": "社交·学习",
        "module": "高频行为",
        "summary": "PDF：explain concepts / mutually motivate；老师帮助。",
        # 仅挂 Teachers —— 勿扩到 science/name/secondary school，否则会硬套「耐心的老师」
        "topics": ["teachers"],
        "open": {
            "yes": ["Yes", "My favourite teacher", "Someone patient"],
            "kind": ["a patient teacher", "clear explanations", "encouraging feedback"],
            "prefer": ["I prefer patient teachers", "I'd rather have clear explanations", "Encouragement matters more"],
        },
        "origins": [
            "In secondary school one teacher stayed after class to explain concepts without rushing me",
            "A campus lecturer used simple examples and that became my standard for good teaching",
        ],
        "routes": [
            {"freq": "every week in that class", "feel": "appreciated", "impact": "made me less afraid to ask questions"},
            {"freq": "whenever assignments felt hard", "feel": "makes me happy", "impact": "helped me keep going and stay self-driven"},
        ],
    },
    "polite_thank_you": {
        "id": "polite_thank_you",
        "nameZh": "说谢谢有礼貌",
        "kind": "社交·礼貌",
        "module": "高频行为",
        "summary": "家人教导；开门食堂说谢谢。",
        "topics": ["politeness", "hometown", "teachers", "shopping", "street markets", "name"],
        "open": {
            "yes": ["Yes, I do", "Yes, it matters", "I try to"],
            "kind": ["saying thank you", "holding the door", "small polite words"],
            "prefer": ["I prefer being polite", "I'd rather say thank you", "Small manners feel natural"],
        },
        "origins": [
            "My parents corrected me every time I forgot thank you at shops when I was little",
            "A teacher praised classmates who held the door, and it became automatic for me",
        ],
        "routes": [
            {"freq": "every day in public", "feel": "respectful", "impact": "makes small interactions smoother"},
            {"freq": "at the canteen and on campus", "feel": "natural", "impact": "reduces awkward moments"},
        ],
    },
    "simple_watch_gift": {
        "id": "simple_watch_gift",
        "nameZh": "普通手表礼物",
        "kind": "物品·手表",
        "module": "衣食住行",
        "summary": "开学礼物；看时间不用掏手机。",
        "topics": ["watch", "politeness", "tiredness"],
        "open": {
            "yes": ["Yes, I do", "Most weekdays", "Yes, a simple one"],
            "kind": ["a simple watch", "a birthday gift watch", "checking the time"],
            "prefer": ["I prefer a simple watch", "I'd rather wear a watch", "A watch feels clearer"],
        },
        "origins": [
            "My parents gave me a simple watch before I started high school",
            "I bought it myself when I kept missing the start of morning classes",
        ],
        "routes": [
            {"freq": "every weekday before class", "feel": "practical", "impact": "keeps me punctual without checking my phone"},
            {"freq": "during exams and meetings", "feel": "reliable", "impact": "saves awkward phone checks in public"},
        ],
    },
    "phone_time_check": {
        "id": "phone_time_check",
        "nameZh": "手机看时间",
        "kind": "物品·手表",
        "module": "高频行为",
        "summary": "不戴表时用手机看时间；手表题第二套。",
        "topics": ["watch", "tiredness", "social media"],
        "open": {
            "yes": ["Not really a watch", "I mostly use my phone", "Sometimes"],
            "kind": ["my phone clock", "checking time on my phone", "phone reminders"],
            "prefer": ["I'd rather use my phone", "I prefer phone alarms", "A phone is enough"],
        },
        "origins": [
            "I stopped wearing a watch after I got used to checking time on my phone",
            "Between classes I glance at my phone lock screen for the time",
        ],
        "routes": [
            {"freq": "every weekday before class", "feel": "really convenient", "impact": "saves me carrying an extra item"},
            {"freq": "when I feel tired in the evening", "feel": "practical", "impact": "helps me decide when to stop studying"},
        ],
    },
    "campus_opportunity_notice": {
        "id": "campus_opportunity_notice",
        "nameZh": "校园机会通知",
        "kind": "学习·机会",
        "module": "学习工作",
        "summary": "老师/班级群/实习帖；机会题主素材。",
        "topics": ["opportunities", "social media", "websites"],
        "open": {
            "yes": ["Yes, I try to", "When I see a notice", "Usually yes"],
            "kind": ["campus notices", "internship posts", "teacher recommendations"],
            "prefer": ["I prefer checking notices early", "I'd rather ask teachers first", "Group chats are faster"],
        },
        "origins": [
            "I find most opportunities through teachers, classmates and campus WeChat notices",
            "Internship posts on study websites and class groups are how I hear about new chances",
        ],
        "routes": [
            {"freq": "every week during term", "feel": "practical", "impact": "helps me apply a bit earlier"},
            {"freq": "when a teacher shares a link", "feel": "useful", "impact": "keeps me from missing quiet deadlines"},
        ],
    },
    "subway_screen_ads": {
        "id": "subway_screen_ads",
        "nameZh": "地铁广告屏",
        "kind": "媒介·广告",
        "module": "高频行为",
        "summary": "通勤刷到屏幕广告；有的抓眼有的烦人。",
        "topics": ["advertisements", "the city you live in", "shopping"],
        "open": {
            "yes": ["Yes, I notice them", "On the subway", "Quite often"],
            "kind": ["subway screen ads", "phone ads", "catchy slogan screens"],
            "prefer": ["I prefer useful ads", "I'd rather see clear offers", "Simple information is better"],
        },
        "origins": [
            "I started noticing them when my commute got longer and the carriage screens never went dark",
            "A catchy slogan stuck in my head after weeks on the same line",
        ],
        "routes": [
            {"freq": "every weekday on the commute", "feel": "it bothers me sometimes", "impact": "can still influence small purchases"},
            {"freq": "whenever I browse videos while waiting", "feel": "hard to ignore", "impact": "wastes attention if I stare too long"},
        ],
    },
    "school_science_lab": {
        "id": "school_science_lab",
        "nameZh": "学校科学实验课",
        "kind": "学习·科学",
        "module": "学习工作",
        "summary": "课堂实验、生物兴趣；勿硬套航天纪录片。",
        "topics": ["science", "secondary school", "outer space and stars"],
        "qHints": {
            "science": (
                "experiment", "lab", "school", "learn", "start", "area of science",
                "biology", "like science", "science at school", "classroom",
                "programme", "program", "video", "videos", "enjoy",
            ),
            "outer space and stars": ("space", "star", "stars", "universe", "planet", "learn", "child", "school"),
        },
        "open": {
            "yes": ["Yes, especially experiments", "Yes, in science class", "I liked biology most"],
            "kind": ["biology experiments", "science class", "simple school labs"],
            "prefer": ["I prefer experiments", "I'd rather do lab work", "Hands-on science feels clearer"],
        },
        "origins": [
            "We did simple biology experiments at school, which made science feel concrete",
            "A clear science class explanation made me more curious about how things work",
        ],
        "routes": [
            {"freq": "in secondary-school science lessons", "feel": "keeps me curious", "impact": "helps me understand daily life better"},
            {"freq": "when we had lab sessions", "feel": "feels practical", "impact": "makes theory easier to remember"},
        ],
    },
    "daily_tech_science": {
        "id": "daily_tech_science",
        "nameZh": "日常科技与科学",
        "kind": "生活·科学",
        "module": "高频行为",
        "summary": "手机地图、地铁系统等出行里的科学应用。",
        "topics": ["science"],
        "qHints": {
            "science": ("daily", "everyday", "affect", "affects", "life", "phone", "subway", "transport", "map"),
        },
        "open": {
            "yes": ["It affects me every day", "In small daily ways", "Through my phone and transport"],
            "kind": ["phone maps", "subway systems", "weather apps on the go"],
            "prefer": ["I notice transport tech most", "I'd rather talk about daily tools", "Everyday science feels clearer"],
        },
        "origins": [
            "I notice science most when I use maps and the subway on weekdays",
            "Trains and phone maps make ordinary trips easier",
        ],
        "routes": [
            {"freq": "every weekday on campus", "feel": "really convenient", "impact": "makes ordinary trips faster"},
            {"freq": "whenever I go out", "feel": "practical", "impact": "shows science in daily transport"},
        ],
    },
    "weather_search_tools": {
        "id": "weather_search_tools",
        "nameZh": "天气搜索与在线工具",
        "kind": "生活·科学",
        "module": "高频行为",
        "summary": "查天气、搜索引擎、在线课；家里常用的科学小工具。",
        "topics": ["science"],
        "qHints": {
            "science": ("daily", "everyday", "affect", "affects", "life", "weather", "search", "online", "home"),
        },
        "open": {
            "yes": ["Yes, in small ways", "It helps at home and in study", "Through simple online tools"],
            "kind": ["check the weather", "a search engine", "online classes"],
            "prefer": ["I notice home tools most", "I'd rather talk about search and weather", "Simple online tools feel clearer"],
        },
        "origins": [
            "I check the weather and search homework questions on my phone at home",
            "Online classes and a quick search make study tasks easier",
        ],
        "routes": [
            {"freq": "most evenings after study", "feel": "practical", "impact": "saves time on small tasks"},
            {"freq": "almost every day at home", "feel": "really useful", "impact": "makes homework and plans easier"},
        ],
    },
    "space_docs_night": {
        "id": "space_docs_night",
        "nameZh": "夜里看航天纪录片",
        "kind": "爱好·科普",
        "module": "高频行为",
        "summary": "航天/星空纪录片；仅挂太空与科学节目类题。",
        "topics": ["outer space and stars", "science"],
        "open": {
            "yes": ["Yes, I do", "Sometimes at night", "Yes, short documentaries"],
            "kind": ["space documentaries", "science videos", "night-sky clips"],
            "prefer": ["I prefer documentaries", "I'd rather watch space clips", "Short docs feel calmer"],
        },
        "origins": [
            "I downloaded a space documentary series during a boring exam month",
            "A science class clip made me curious, so I continued with longer videos on my own",
        ],
        "routes": [
            {"freq": "a few nights a week before I go to sleep", "feel": "helps me chill out", "impact": "gives me a soft break from assignments"},
            {"freq": "when I feel stuck in study", "feel": "makes me happy", "impact": "reminds me the world is bigger than deadlines"},
        ],
    },
    "hometown_local_food": {
        "id": "hometown_local_food",
        "nameZh": "家乡本地小吃",
        "kind": "食·家乡",
        "module": "衣食住行",
        "summary": "PDF：street food / local food；记忆与情感。",
        "topics": ["hometown", "street markets", "fruit and vegetables", "travelling", "feeling bored", "politeness"],
        "open": {
            "yes": ["Yes, I do", "When I go back", "In my hometown"],
            "kind": ["local street food", "familiar snacks", "family-style dishes"],
            "prefer": ["I prefer local food", "I'd rather eat at home stalls", "Hometown food feels warmer"],
        },
        "origins": [
            "Every holiday my parents take me to the same breakfast stall near our old neighbourhood",
            "It's about the memories and emotions from growing up with that taste",
        ],
        "routes": [
            {"freq": "every time I go home", "feel": "makes me happy", "impact": "helps me reset after a busy term"},
            {"freq": "once or twice a year in the holiday", "feel": "gives me a good feeling", "impact": "keeps family conversations easy"},
        ],
    },
    "name_parents_choice": {
        "id": "name_parents_choice",
        "nameZh": "父母取的名字",
        "kind": "社交·名字",
        "module": "高频行为",
        "summary": "名字含义；父母选择。",
        "topics": ["name", "politeness", "hometown", "teachers", "opportunities"],
        "open": {
            "yes": ["Yes", "My parents chose it", "It has a meaning"],
            "kind": ["my given name", "its meaning", "my parents' choice"],
            "prefer": ["I like my name", "I'd rather keep it", "The meaning feels positive"],
        },
        "origins": [
            "My parents chose my name before I went to primary school because it has a positive meaning",
            "Teachers and classmates have always found it easy to remember",
        ],
        "routes": [
            {"freq": "every day when people call me", "feel": "appreciated", "impact": "helps me feel connected to my family"},
            {"freq": "when I introduce myself", "feel": "practical", "impact": "makes first conversations smoother"},
        ],
    },
    "name_nickname_school": {
        "id": "name_nickname_school",
        "nameZh": "学校短昵称",
        "kind": "社交·名字",
        "module": "高频行为",
        "summary": "同学昵称；名字话题第二套。",
        "topics": ["name", "secondary school", "politeness"],
        "open": {
            "yes": ["Yes, sometimes", "Friends use a short form", "At school yes"],
            "kind": ["a short nickname", "what friends call me", "a classroom nickname"],
            "prefer": ["I prefer my real name", "I'd rather keep the short form with friends", "Both feel fine"],
        },
        "origins": [
            "In secondary school classmates shortened my name because it was quicker to shout",
            "Friends still use a light nickname in group chats even now",
        ],
        "routes": [
            {"freq": "every day at school back then", "feel": "warm", "impact": "made classroom chat feel closer"},
            {"freq": "when friends message me", "feel": "natural", "impact": "keeps old friendships easy"},
        ],
    },
}


def normalize_topic(topic_en: str) -> str:
    return (topic_en or "").strip().lower()


# Controlled multi-topic allow-list (Freestyle): same kit may serve related topics,
# but only those listed — never auto-expand by "near meaning".
MATERIAL_TOPIC_ALLOW: dict[str, tuple[str, ...]] = {
    "campus_tee_coat": ("clothing",),
    "campus_sweatshirt": ("clothing",),
    "hallway_mirror_routine": ("mirrors",),
    "dressing_mirror_home": ("mirrors", "clothing"),
    "campus_sneakers": ("shoes",),
    "style_shoes_weekend": ("shoes", "shopping"),
    "canteen_and_takeaways": ("fruit and vegetables", "hometown"),
    "fruit_groceries": ("fruit and vegetables", "shopping", "street markets"),
    "dorm_apartment_life": (
        "home & accommodation", "the area you live in", "tidiness", "the city you live in",
    ),
    "tidy_desk_habit": ("tidiness", "home & accommodation"),
    "parents_tidy_home": ("tidiness", "home & accommodation"),
    "recycle_bins_floor": ("rubbish and recycling", "paper"),
    # paper notes as second rubbish angle (sorting printouts)
    "subway_bus_commute": (
        "the city you live in", "the area you live in", "travelling", "cars",
    ),
    "family_car_passenger": ("cars", "travelling", "hometown"),
    "yellow_bike_gift": (
        "opportunities", "secondary school", "public gardens and parks",
        "tiredness", "travelling", "feeling bored",
    ),
    "nearby_park_walk": (
        "public gardens and parks", "feeling bored", "tiredness",
        "the area you live in", "the city you live in",
    ),
    "mall_street_market": ("shopping", "street markets", "fruit and vegetables"),
    "study_library_classes": ("work or studies", "secondary school", "teachers"),
    "business_major_path": ("work or studies", "opportunities"),
    "handwritten_notes_paper": ("paper", "secondary school", "rubbish and recycling"),
    "phone_xiaohongshu_wechat": ("social media", "websites", "advertisements", "opportunities"),
    "douyin_scroll_habit": ("social media", "feeling bored", "jokes & comedies"),
    # 查网站/耳机/老师/校园通知：可挂各自主话题，不硬塞进 Work or studies 凑第三套
    "study_websites_search": ("websites", "opportunities"),
    "wireless_earbuds_music": ("headphones", "music", "travelling", "tiredness"),
    "focus_wired_headphones": ("headphones", "music"),
    "school_choir_songs": ("singing", "secondary school", "music"),
    "singing_ktv_songs": ("singing", "music", "feeling bored"),
    "comedy_hang_out": ("jokes & comedies", "feeling bored", "social media"),
    "light_sports_walk": ("tiredness", "public gardens and parks", "feeling bored"),
    "patient_teacher_help": ("teachers", "secondary school", "politeness"),
    "polite_thank_you": ("politeness",),
    "simple_watch_gift": ("watch",),
    "phone_time_check": ("watch",),
    "subway_screen_ads": ("advertisements", "the city you live in", "travelling"),
    "space_docs_night": ("outer space and stars", "science", "feeling bored"),
    "school_science_lab": ("science", "secondary school", "outer space and stars"),
    "daily_tech_science": ("science",),
    "weather_search_tools": ("science",),
    # 家乡小吃：Hometown / 市集 / 水果；也可挂 Cars 童年车程、Travelling 回乡
    "hometown_local_food": (
        "hometown", "street markets", "fruit and vegetables", "cars", "travelling",
    ),
    "name_parents_choice": ("name",),
    "name_nickname_school": ("name", "secondary school", "politeness"),
    "campus_opportunity_notice": ("opportunities", "social media"),
}

# 题级素材白名单（优先于话题池）：同一话题下各题可挂不同套装。
# 对不上的题不要硬塞；未列出的题仍走话题池 + qHints 打分。
# 值：有序 kit id，通常 2 套（够用即可，不必凑 3）。
QUESTION_KIT_ALLOW: dict[str, tuple[str, ...]] = {
    # —— Work or studies：身份/日常 ≠ 选专业 ≠ 几年后 ——
    _norm_q("Do you work or are you a student?"): (
        "study_library_classes",
        "business_major_path",
    ),
    _norm_q("Why did you choose that job or that subject?"): (
        "business_major_path",
        "study_library_classes",
    ),
    _norm_q("What do you find most challenging about your work or your studies?"): (
        "study_library_classes",
        "business_major_path",
    ),
    _norm_q("What do you like most about your job or your studies?"): (
        "study_library_classes",
        "business_major_path",
    ),
    _norm_q("What is a typical day like for you at work or at school?"): (
        "study_library_classes",
        "business_major_path",
    ),
    _norm_q("What would you like to be doing in your career or studies in a few years?"): (
        "business_major_path",
        "campus_opportunity_notice",
    ),
    # —— Feeling bored：童年不宜刷短视频；观点题偏户外；原因题偏屏幕 vs 少活动 ——
    _norm_q("Do you often feel bored?"): (
        "douyin_scroll_habit",
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    _norm_q("When do you usually feel bored?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
        "douyin_scroll_habit",
    ),
    _norm_q("What do you do when you feel bored?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
        "douyin_scroll_habit",
    ),
    _norm_q("How did you deal with boredom as a child?"): (
        "yellow_bike_gift",
        "nearby_park_walk",
    ),
    _norm_q("Why do people today seem to get bored more easily?"): (
        "douyin_scroll_habit",
        "yellow_bike_gift",
    ),
    _norm_q("Is it ever good to feel bored?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    # —— Science：学校喜好 ≠ 日常生活科技 ——
    _norm_q("Did you like science at school?"): (
        "school_science_lab",
        "space_docs_night",
    ),
    _norm_q("How does science affect our daily life?"): (
        "daily_tech_science",
        "weather_search_tools",
    ),
    _norm_q("How does science affect your daily life?"): (
        "daily_tech_science",
        "weather_search_tools",
    ),
    _norm_q("Which area of science interests you the most?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("When did you start to learn about science?"): (
        "school_science_lab",
        "space_docs_night",
    ),
    _norm_q("What science programmes or videos do you enjoy?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("What scientific discovery would you like to see in the future?"): (
        "space_docs_night",
        "daily_tech_science",
        "school_science_lab",
    ),
    # —— Opportunities：童年活动 ≠ 现在找机会/抓机会 ——
    _norm_q("Did you have any opportunities to take part in new activities as a child?"): (
        "yellow_bike_gift",
        "campus_opportunity_notice",
    ),
    _norm_q("What is one good opportunity you had when you were younger?"): (
        "yellow_bike_gift",
        "campus_opportunity_notice",
    ),
    _norm_q("How do you find out about new opportunities?"): (
        "business_major_path",
        "phone_xiaohongshu_wechat",
        "study_websites_search",
    ),
    _norm_q("Is it important to seize opportunities when they come?"): (
        "business_major_path",
        "phone_xiaohongshu_wechat",
        "study_websites_search",
    ),
    _norm_q("Why do some people miss good opportunities?"): (
        "phone_xiaohongshu_wechat",
        "study_websites_search",
        "business_major_path",
    ),
    _norm_q("What kind of opportunity would you like to have in the next few years?"): (
        "business_major_path",
        "campus_opportunity_notice",
    ),
    _norm_q("Do you usually take an opportunity when it comes along?"): (
        "campus_opportunity_notice",
        "business_major_path",
        "phone_xiaohongshu_wechat",
    ),
    # —— Watch：戴表 vs 手机看时间 ——
    _norm_q("Do you wear a watch?"): (
        "simple_watch_gift",
        "phone_time_check",
    ),
    _norm_q("Have you ever got a watch as a gift?"): (
        "simple_watch_gift",
        "phone_time_check",
    ),
    _norm_q("Why do some people wear expensive watches?"): (
        "simple_watch_gift",
        "phone_time_check",
    ),
    _norm_q("Do you think it is important to wear a watch?"): (
        "simple_watch_gift",
        "phone_time_check",
    ),
    _norm_q("Do you think it is important to wear a watch? Why?"): (
        "simple_watch_gift",
        "phone_time_check",
    ),
    # —— Cars：有无车/出行 ≠ 童年车程 ≠ 未来车 ——
    _norm_q("Do you have a car?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("What do you remember about car journeys as a child?"): (
        "family_car_passenger",
        "hometown_local_food",
    ),
    _norm_q("What kind of car would you like to own?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("How do you usually get around your city?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("How do you think cars will change in the future?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("Do you prefer to be a driver or a passenger?"): (
        "family_car_passenger",
        "subway_bus_commute",
    ),
    # —— Headphones：有线专注 vs 无线通勤 ——
    _norm_q("When did you get your first pair of headphones?"): (
        "focus_wired_headphones",
        "wireless_earbuds_music",
    ),
    _norm_q("Do you use headphones?"): (
        "focus_wired_headphones",
        "wireless_earbuds_music",
    ),
    _norm_q("How often do you use headphones?"): (
        "focus_wired_headphones",
        "wireless_earbuds_music",
    ),
    _norm_q("What do you usually listen to with your headphones?"): (
        "focus_wired_headphones",
        "wireless_earbuds_music",
    ),
    _norm_q("In what situations should people not wear headphones?"): (
        "focus_wired_headphones",
        "wireless_earbuds_music",
    ),
    _norm_q("Which do you prefer, big headphones or small earbuds?"): (
        "wireless_earbuds_music",
        "focus_wired_headphones",
    ),
    # —— Music：乐器/合唱 ≠ 耳机刷歌（第三套耳机常多余）——
    _norm_q("Did you learn to play an instrument as a child?"): (
        "school_choir_songs",
        "wireless_earbuds_music",
    ),
    _norm_q("Do you listen to music while doing other things?"): (
        "wireless_earbuds_music",
        "school_choir_songs",
    ),
    _norm_q("What kind of music do you like?"): (
        "wireless_earbuds_music",
        "school_choir_songs",
    ),
    _norm_q("When do you usually listen to music?"): (
        "wireless_earbuds_music",
        "school_choir_songs",
    ),
    _norm_q("How do you usually discover new music?"): (
        "wireless_earbuds_music",
        "school_choir_songs",
    ),
    _norm_q("How has your taste in music changed over the years?"): (
        "wireless_earbuds_music",
        "school_choir_songs",
    ),
    # —— Teachers：耐心答疑 vs 带读图书馆 ——
    _norm_q("What makes someone a good teacher?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    _norm_q("Have you ever wanted to be a teacher?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    _norm_q("What kind of teacher do you learn best from?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    _norm_q("Who was your favourite teacher when you were at school?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    _norm_q("In what way has your favourite teacher helped you?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    _norm_q("How has the way teachers teach changed since you were a child?"): (
        "patient_teacher_help",
        "study_library_classes",
    ),
    # —— Secondary school：合唱/实验为主；骑车只挂通勤相关题 ——
    _norm_q("Do you still keep in touch with your classmates from secondary school?"): (
        "school_choir_songs",
        "school_science_lab",
    ),
    _norm_q("Is there anything you miss about your secondary school?"): (
        "school_choir_songs",
        "yellow_bike_gift",
        "school_science_lab",
    ),
    _norm_q("What was your secondary school like?"): (
        "school_choir_songs",
        "school_science_lab",
        "yellow_bike_gift",
    ),
    _norm_q("What was your favourite subject at secondary school?"): (
        "school_choir_songs",
        "school_science_lab",
    ),
    _norm_q("How did you usually spend your breaks at school?"): (
        "school_choir_songs",
        "school_science_lab",
    ),
    _norm_q("How are secondary schools today different from when you were there?"): (
        "school_choir_songs",
        "school_science_lab",
    ),
    # —— Tidiness：书桌习惯 ≠ 童年谁收拾 ≠ 宿舍轮值 ——
    _norm_q("Are you a tidy person?"): (
        "tidy_desk_habit",
        "parents_tidy_home",
    ),
    _norm_q("Who kept your room tidy when you were a child?"): (
        "parents_tidy_home",
        "tidy_desk_habit",
    ),
    _norm_q("Do you like to keep things tidy?"): (
        "tidy_desk_habit",
        "parents_tidy_home",
    ),
    _norm_q("How often do you tidy your room?"): (
        "tidy_desk_habit",
        "dorm_apartment_life",
    ),
    _norm_q("Do you think that it is necessary to be tidy?"): (
        "tidy_desk_habit",
        "dorm_apartment_life",
    ),
    _norm_q("How have your tidying habits changed as you've got older?"): (
        "tidy_desk_habit",
        "parents_tidy_home",
    ),
    # —— Tiredness：影响学习 ≠ 累了做什么 ≠ 为何社会上很多人累 ——
    _norm_q("How does tiredness affect your work or studies?"): (
        "study_library_classes",
        "nearby_park_walk",
    ),
    _norm_q("What used to make you tired when you were a child?"): (
        "yellow_bike_gift",
        "nearby_park_walk",
        "light_sports_walk",
    ),
    _norm_q("Do you often get tired?"): (
        "nearby_park_walk",
        "light_sports_walk",
    ),
    _norm_q("When do you usually feel tired?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    _norm_q("What do you usually do when you feel tired?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
        "light_sports_walk",
    ),
    _norm_q("Why do you think so many people feel tired these days?"): (
        "douyin_scroll_habit",
        "nearby_park_walk",
        "light_sports_walk",
    ),
    # —— Parks：附近有没有 / 童年玩什么 / 现在喜欢做什么 ——
    _norm_q("Is there a park near your home?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    _norm_q("What did you do in parks when you were a child?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
        "light_sports_walk",
    ),
    _norm_q("What do you like to do in a park?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
        "light_sports_walk",
    ),
    _norm_q("Did you like going to parks as a child?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    _norm_q("How often do you go to parks?"): (
        "nearby_park_walk",
        "yellow_bike_gift",
    ),
    _norm_q("How have the parks in your city changed in recent years?"): (
        "nearby_park_walk",
        "light_sports_walk",
    ),
    # —— Travelling：靠窗 ≠ 童年假期 ≠ 未来想去哪 ——
    _norm_q("Where did you go on holiday when you were a child?"): (
        "family_car_passenger",
        "subway_bus_commute",
        "hometown_local_food",
    ),
    _norm_q("Do you prefer sitting by the window when you travel?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("What kind of places do you like to visit?"): (
        "subway_bus_commute",
        "family_car_passenger",
        "hometown_local_food",
    ),
    _norm_q("Where would you most like to travel in the future?"): (
        "family_car_passenger",
        "subway_bus_commute",
        "yellow_bike_gift",
    ),
    _norm_q("How often do you travel?"): (
        "subway_bus_commute",
        "family_car_passenger",
    ),
    _norm_q("Do you prefer travelling alone or with other people?"): (
        "family_car_passenger",
        "subway_bus_commute",
        "yellow_bike_gift",
    ),
    # —— Home：住哪类房 / 和谁住 ≠ 书桌整洁专题 ——
    _norm_q("Do you live in a house or a flat?"): (
        "dorm_apartment_life",
        "parents_tidy_home",
    ),
    _norm_q("Who do you live with?"): (
        "dorm_apartment_life",
        "parents_tidy_home",
    ),
    _norm_q("Which room in your home do you like best?"): (
        "dorm_apartment_life",
        "tidy_desk_habit",
        "parents_tidy_home",
    ),
    _norm_q("What kind of home would you like to have in the future?"): (
        "dorm_apartment_life",
        "parents_tidy_home",
    ),
    _norm_q("What do you usually do at home in the evenings?"): (
        "dorm_apartment_life",
        "tidy_desk_habit",
    ),
    _norm_q("How is your home different from the one you lived in as a child?"): (
        "dorm_apartment_life",
        "parents_tidy_home",
    ),
    # —— Hometown：美食/食堂回忆/全家短途 ——
    _norm_q("Where is your hometown?"): (
        "hometown_local_food",
        "family_car_passenger",
    ),
    _norm_q("What is your hometown best known for?"): (
        "hometown_local_food",
        "canteen_and_takeaways",
    ),
    _norm_q("What do you like most about your hometown?"): (
        "hometown_local_food",
        "family_car_passenger",
    ),
    _norm_q("Would you like to live in your hometown in the future?"): (
        "hometown_local_food",
        "family_car_passenger",
    ),
    _norm_q("What do people in your hometown usually do at the weekend?"): (
        "hometown_local_food",
        "family_car_passenger",
        "canteen_and_takeaways",
    ),
    _norm_q("How has your hometown changed since you were a child?"): (
        "hometown_local_food",
        "family_car_passenger",
        "canteen_and_takeaways",
    ),
    # —— Area：住多久 ≠ 设施 ≠ 最喜欢什么 ——
    _norm_q("How long have you lived there?"): (
        "dorm_apartment_life",
        "subway_bus_commute",
    ),
    _norm_q("What facilities are there near where you live?"): (
        "nearby_park_walk",
        "dorm_apartment_life",
        "subway_bus_commute",
    ),
    _norm_q("What would you improve about your area if you could?"): (
        "dorm_apartment_life",
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    _norm_q("What is the area where you live like?"): (
        "dorm_apartment_life",
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    _norm_q("What do you like most about your neighbourhood?"): (
        "nearby_park_walk",
        "dorm_apartment_life",
        "subway_bus_commute",
    ),
    _norm_q("How has your area changed over the last few years?"): (
        "dorm_apartment_life",
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    # —— City：身份/出行 ≠ 天气（查天气）≠ 广告屏硬套 ——
    _norm_q("Which city do you live in now?"): (
        "subway_bus_commute",
        "dorm_apartment_life",
    ),
    _norm_q("What is the best way to get around your city?"): (
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    _norm_q("Where would you take a friend who was visiting your city?"): (
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    _norm_q("What do you like most about living in this city?"): (
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    _norm_q("What's the weather like where you live?"): (
        "subway_bus_commute",
        "weather_search_tools",
    ),
    _norm_q("How has your city changed over the past ten years?"): (
        "subway_bus_commute",
        "nearby_park_walk",
    ),
    # —— Shopping ——
    _norm_q("What was the last thing you bought?"): (
        "fruit_groceries",
        "mall_street_market",
    ),
    _norm_q("Who did you go shopping with when you were a child?"): (
        "mall_street_market",
        "fruit_groceries",
    ),
    _norm_q("Do you enjoy shopping?"): (
        "mall_street_market",
        "fruit_groceries",
    ),
    _norm_q("Do you like shopping?"): (
        "mall_street_market",
        "fruit_groceries",
    ),
    _norm_q("How often do you go shopping?"): (
        "mall_street_market",
        "fruit_groceries",
    ),
    _norm_q("Do you prefer shopping online or in shops?"): (
        "mall_street_market",
        "fruit_groceries",
    ),
    # —— Street Markets ——
    _norm_q("When was the last time you went to a street market?"): (
        "mall_street_market",
        "hometown_local_food",
        "fruit_groceries",
    ),
    _norm_q("Are there many street markets in your country?"): (
        "mall_street_market",
        "hometown_local_food",
        "fruit_groceries",
    ),
    _norm_q("Are there many street markets in China?"): (
        "mall_street_market",
        "hometown_local_food",
        "fruit_groceries",
    ),
    _norm_q("What do people usually buy on the street market?"): (
        "mall_street_market",
        "fruit_groceries",
        "hometown_local_food",
    ),
    _norm_q("Do you prefer to go shopping in the shopping mall or on the street market?"): (
        "mall_street_market",
        "fruit_groceries",
        "hometown_local_food",
    ),
    # —— Fruit and vegetables：食堂/买菜/市集按题拆 ——
    _norm_q("Which vegetables did you dislike as a child?"): (
        "fruit_groceries",
        "canteen_and_takeaways",
    ),
    _norm_q("Do people often grow vegetables by themselves?"): (
        "fruit_groceries",
        "canteen_and_takeaways",
    ),
    _norm_q("What is your favourite fruit?"): (
        "fruit_groceries",
        "mall_street_market",
    ),
    _norm_q("Do you like eating vegetables?"): (
        "fruit_groceries",
        "canteen_and_takeaways",
    ),
    _norm_q("How often do you eat vegetables?"): (
        "fruit_groceries",
        "canteen_and_takeaways",
    ),
    _norm_q("How has the way people buy fruit and vegetables changed?"): (
        "fruit_groceries",
        "mall_street_market",
    ),
    # —— Clothing：日常T恤外套 ≠ 镜子挑选（花时间选衣才挂镜子）——
    _norm_q("Who chose your clothes when you were a child?"): (
        "campus_tee_coat",
        "campus_sweatshirt",
    ),
    _norm_q("Do you spend a lot of time choosing clothes?"): (
        "campus_tee_coat",
        "dressing_mirror_home",
    ),
    _norm_q("What kind of clothes do you like to wear?"): (
        "campus_tee_coat",
        "campus_sweatshirt",
    ),
    _norm_q("Do you like wearing T-shirts?"): (
        "campus_tee_coat",
        "campus_sweatshirt",
    ),
    _norm_q("What kind of clothes do you usually wear?"): (
        "campus_tee_coat",
        "campus_sweatshirt",
        "dressing_mirror_home",
    ),
    _norm_q("Do you prefer comfortable clothes or fashionable ones?"): (
        "campus_tee_coat",
        "dressing_mirror_home",
    ),
    # —— Shoes ——
    _norm_q("What kind of shoes do you wear most often?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    _norm_q("What kind of shoes did you wear as a child?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    _norm_q("Do you like buying shoes?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    _norm_q("What is your favourite type of shoes?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    _norm_q("How often do you buy new shoes?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    _norm_q("Which matters more to you in a pair of shoes, comfort or style?"): (
        "campus_sneakers",
        "style_shoes_weekend",
    ),
    # —— Mirrors ——
    _norm_q("Why do some shops and restaurants have so many mirrors?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    _norm_q("How did you feel about looking in the mirror as a teenager?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    _norm_q("Do you like having lots of mirrors at home?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    _norm_q("Do you like looking at yourself in the mirror?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    _norm_q("How often do you look in the mirror each day?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    _norm_q("How have phone cameras changed the way people use mirrors?"): (
        "hallway_mirror_routine",
        "dressing_mirror_home",
    ),
    # —— Politeness：谢谢习惯 ≠ 耐心老师（勿昵称抢戏）——
    _norm_q("How do people in your country show politeness?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    _norm_q("Who taught you to be polite when you were a child?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    _norm_q("What kind of behaviour do you find rude?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    _norm_q("Why is it important to be polite to strangers?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    _norm_q("On what occasions should we be polite?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    _norm_q("How have people's manners changed compared with the past?"): (
        "polite_thank_you",
        "patient_teacher_help",
    ),
    # —— Name：父母取名 ≠ 校园昵称（朋友怎么叫/婴儿名趋势按题拆）——
    _norm_q("Who chose your name?"): (
        "name_parents_choice",
        "name_nickname_school",
    ),
    _norm_q("Does your name have a special meaning?"): (
        "name_parents_choice",
        "name_nickname_school",
    ),
    _norm_q("How do you feel about your name?"): (
        "name_parents_choice",
        "name_nickname_school",
    ),
    _norm_q("What did your friends call you when you were a child?"): (
        "name_nickname_school",
        "name_parents_choice",
    ),
    _norm_q("Do you often forget people's names?"): (
        "name_nickname_school",
        "name_parents_choice",
    ),
    _norm_q("How have popular names for babies changed in your country?"): (
        "name_parents_choice",
        "name_nickname_school",
    ),
    # —— Rubbish / Paper：分类桶 ≠ 手写废纸（街头捡拾以桶线为主）——
    _norm_q("Do you recycle at home?"): (
        "recycle_bins_floor",
        "handwritten_notes_paper",
    ),
    _norm_q("What kinds of things do you throw away most often?"): (
        "recycle_bins_floor",
        "handwritten_notes_paper",
    ),
    _norm_q("How do people in your area sort their rubbish?"): (
        "recycle_bins_floor",
        "handwritten_notes_paper",
    ),
    _norm_q("How do you recycle things like paper and plastic?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("What do you do when you see rubbish on the street?"): (
        "recycle_bins_floor",
        "handwritten_notes_paper",
    ),
    _norm_q("How have people's attitudes to rubbish changed in recent years?"): (
        "recycle_bins_floor",
        "handwritten_notes_paper",
    ),
    _norm_q("What did you use paper for most when you were at school?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("What do you do with paper you no longer need?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("What did you like to do with paper as a child?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("How often do you use paper in your daily life?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("How do you think our use of paper will change in the future?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    _norm_q("Do you prefer reading on paper or on a screen?"): (
        "handwritten_notes_paper",
        "recycle_bins_floor",
    ),
    # —— Singing：KTV ≠ 学校合唱 ——
    _norm_q("What songs did you sing when you were a child?"): (
        "school_choir_songs",
        "singing_ktv_songs",
    ),
    _norm_q("Have you ever learnt how to sing?"): (
        "school_choir_songs",
        "singing_ktv_songs",
    ),
    _norm_q("Do you like singing?"): (
        "singing_ktv_songs",
        "school_choir_songs",
    ),
    _norm_q("When do you usually sing?"): (
        "singing_ktv_songs",
        "school_choir_songs",
    ),
    _norm_q("Do you think singing can bring happiness to people?"): (
        "singing_ktv_songs",
        "school_choir_songs",
    ),
    _norm_q("How popular is karaoke now compared with the past?"): (
        "singing_ktv_songs",
        "school_choir_songs",
    ),
    # —— Jokes：童年不宜抖音主线；成人可短视频/聚会喜剧 ——
    _norm_q("Who is the funniest person you know?"): (
        "comedy_hang_out",
        "douyin_scroll_habit",
    ),
    _norm_q("What made you laugh when you were a child?"): (
        "comedy_hang_out",
        "douyin_scroll_habit",
    ),
    _norm_q("Are you good at telling jokes?"): (
        "comedy_hang_out",
        "douyin_scroll_habit",
    ),
    _norm_q("Do you like telling jokes?"): (
        "comedy_hang_out",
        "douyin_scroll_habit",
    ),
    _norm_q("What kind of comedy do you enjoy?"): (
        "comedy_hang_out",
        "douyin_scroll_habit",
    ),
    _norm_q("Why do you think comedy shows are so popular these days?"): (
        "douyin_scroll_habit",
        "comedy_hang_out",
    ),
    # —— Social media：微信小红书 ≠ 抖音刷屏 ≠ 聚会喜剧（第三套常多余）——
    _norm_q("Which social media apps do you use most?"): (
        "phone_xiaohongshu_wechat",
        "douyin_scroll_habit",
    ),
    _norm_q("How much time do you spend on social media each day?"): (
        "phone_xiaohongshu_wechat",
        "douyin_scroll_habit",
    ),
    _norm_q("What do you usually post online?"): (
        "phone_xiaohongshu_wechat",
        "douyin_scroll_habit",
        "comedy_hang_out",
    ),
    _norm_q("What do people often do on social media?"): (
        "phone_xiaohongshu_wechat",
        "douyin_scroll_habit",
    ),
    _norm_q("How do you think social media will change in the future?"): (
        "phone_xiaohongshu_wechat",
        "douyin_scroll_habit",
    ),
    _norm_q("Do you think you spend too much time on social media?"): (
        "douyin_scroll_habit",
        "phone_xiaohongshu_wechat",
    ),
    # —— Websites：学习检索 ≠ 生活种草站 ——
    _norm_q("Which websites do you visit most often?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("What makes a website easy to use?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("What is your favourite website?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("Would you like to have your own website?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("How have websites changed compared with ten years ago?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("Do you prefer getting information from websites or books?"): (
        "study_websites_search",
        "phone_xiaohongshu_wechat",
    ),
    # —— Advertisements：手机信息流 ≠ 地铁屏 ——
    _norm_q("Where do you see adverts most often?"): (
        "phone_xiaohongshu_wechat",
        "subway_screen_ads",
    ),
    _norm_q("Have you ever bought something because of an advert?"): (
        "phone_xiaohongshu_wechat",
        "subway_screen_ads",
    ),
    _norm_q("Which advert do you remember from your childhood?"): (
        "subway_screen_ads",
        "phone_xiaohongshu_wechat",
    ),
    _norm_q("What kind of adverts do you enjoy watching?"): (
        "phone_xiaohongshu_wechat",
        "subway_screen_ads",
    ),
    _norm_q("How have adverts changed over the past few years?"): (
        "phone_xiaohongshu_wechat",
        "subway_screen_ads",
    ),
    # —— Outer space：纪录片 ≠ 课堂实验 ——
    _norm_q("What did you learn about space when you were a child?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("Have you ever learnt about outer space and stars?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("Do you like looking at the stars?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("What would you most like to know about outer space?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("How often can you see stars where you live?"): (
        "space_docs_night",
        "school_science_lab",
    ),
    _norm_q("How do you think space travel will change in the future?"): (
        "space_docs_night",
        "school_science_lab",
    ),
}


def effective_topics(m: dict[str, Any]) -> list[str]:
    mid = m.get("id") or ""
    if mid in MATERIAL_TOPIC_ALLOW:
        return list(MATERIAL_TOPIC_ALLOW[mid])
    return [normalize_topic(x) for x in m.get("topics") or []]


def all_materials() -> list[dict[str, Any]]:
    return list(MATERIALS.values())


def get_material(mid: str) -> dict[str, Any] | None:
    return MATERIALS.get((mid or "").strip())


def materials_for_topic(topic_en: str, limit: int = 4) -> list[dict[str, Any]]:
    """Return materials allowed for this topic only — never pad with unrelated kits."""
    t = normalize_topic(topic_en)
    hit = [m for m in MATERIALS.values() if t in effective_topics(m)]

    def _score(m: dict[str, Any]) -> tuple[int, str]:
        topics = effective_topics(m)
        try:
            pos = topics.index(t)
        except ValueError:
            pos = 99
        return (pos, m["id"])

    hit.sort(key=_score)
    return hit[:limit]


def material_ids_for_topic(topic_en: str, limit: int = 4) -> list[str]:
    return [m["id"] for m in materials_for_topic(topic_en, limit=limit)]


_Q_SYNONYMS: dict[str, tuple[str, ...]] = {
    "bike": ("bicycle", "bicycles", "cycling", "cycle"),
    "subway": ("metro", "underground", "tube"),
    "sneakers": ("shoes", "trainers"),
    "canteen": ("cafeteria", "campus food"),
    "playlist": ("music", "songs", "singing", "sing"),
    "park": ("garden", "gardens", "near your home", "near where you live"),
    "teacher": ("teachers", "tutor"),
    "notes": ("paper", "notebook"),
    "recycle": ("recycling", "rubbish", "garbage"),
    "dorms": ("home", "accommodation", "apartment", "flat"),
    "apartment": ("home", "accommodation", "flat", "rent"),
    "residential": ("home", "accommodation", "area"),
    "documentaries": ("discovery", "science", "space", "stars"),
    "science": ("discovery", "scientific"),
    "comedy": ("comedies", "jokes", "funny"),
    "space": ("stars", "astronomy", "universe"),
    "mirror": ("mirrors",),
    "watch": ("watches",),
    "tee": ("t-shirt", "t-shirts", "clothes", "clothing"),
    "coat": ("clothes", "clothing", "jacket"),
    "sweatshirt": ("clothes", "clothing", "sweatshirts"),
    "sneakers": ("shoes", "shoe", "trainers", "trainers"),
    "wechat": ("social media", "apps", "app"),
    "xiaohongshu": ("social media", "apps", "app"),
    "douyin": ("social media", "apps", "videos", "short"),
    "phone": ("social media", "apps"),
}


def _material_hit_score(m: dict[str, Any], ql: str) -> int:
    """How well a material matches this question (0 = unrelated to the wording)."""
    import re

    if not ql:
        return 0

    def _token_hit(token: str) -> bool:
        if len(token) < 4:
            return False
        if token in ql:
            return True
        return any(syn in ql for syn in _Q_SYNONYMS.get(token, ()))

    stop = {
        "this", "that", "with", "from", "have", "been", "were", "when", "what",
        "your", "they", "them", "than", "then", "into", "also", "only", "just",
        "very", "more", "most", "some", "such", "over", "after", "before", "about",
        "because", "while", "during", "every", "often", "really", "quite", "small",
        "simple", "clear", "daily", "life", "keep", "helps", "makes", "feels", "weekdays",
        # id suffixes that falsely match broad topic words (e.g. dressing_mirror_home vs home Q)
        "home", "habit", "path", "night", "gift", "help", "walk", "area", "life",
        "floor", "classes", "search", "songs", "food", "ads", "watch", "name",
    }
    opens = m.get("open") or {}
    # Score kind/yes labels first; id tokens only as weak hint (and without generic suffixes)
    kind_yes = " ".join(
        [
            " ".join(opens.get("kind") or []),
            " ".join(opens.get("yes") or []),
        ]
    ).lower()
    id_bits = " ".join(
        t for t in m.get("id", "").replace("_", " ").lower().split() if t not in stop
    )
    score = 0
    for t in {x for x in re.findall(r"[a-z]{4,}", kind_yes) if x not in stop}:
        if _token_hit(t):
            score += 3
    for t in {x for x in re.findall(r"[a-z]{4,}", id_bits) if x not in stop}:
        if _token_hit(t):
            score += 1
    return score


# Extra keyword gate for materials that look similar across topics
_MATERIAL_Q_REQUIRE: dict[str, tuple[str, ...]] = {
    "patient_teacher_help": ("teacher", "teachers", "tutor", "teaching"),
    "campus_sneakers": ("shoe", "shoes", "sneaker", "trainer", "footwear"),
    "style_shoes_weekend": ("shoe", "shoes", "sneaker", "trainer", "footwear"),
    "simple_watch_gift": ("watch", "watches", "time", "punctual"),
    "phone_time_check": ("watch", "watches", "time", "phone"),
    "name_parents_choice": ("name", "names", "call you", "called", "meaning"),
    "name_nickname_school": ("name", "names", "call", "nickname", "friends"),
    "recycle_bins_floor": ("rubbish", "recycl", "garbage", "litter", "bin"),
    "focus_wired_headphones": ("headphone", "earbud", "listen", "music", "wired"),
    "wireless_earbuds_music": ("headphone", "earbud", "music", "listen", "song", "playlist"),
    "subway_screen_ads": ("ad", "advert", "commercial", "poster"),
    "campus_opportunity_notice": (
        "opportunit", "internship", "notice", "chance", "seize", "miss", "find out", "take an",
    ),
    "space_docs_night": (
        "space", "star", "stars", "universe", "planet", "astronomy",
        "documentary", "documentaries", "programme", "program", "video", "videos",
        "area of science", "interests you", "outer space",
    ),
    "school_science_lab": (
        "experiment", "lab", "biology", "school", "learn", "learnt", "learned",
        "start to learn", "area of science", "subject", "classroom",
        "discover", "discovery", "scientific", "like science", "science at school",
    ),
    "daily_tech_science": (
        "daily life", "everyday", "affect", "affects", "technology", "phone", "transport", "subway", "map",
    ),
    "weather_search_tools": (
        "daily life", "everyday", "affect", "affects", "weather", "search", "online", "app", "home",
    ),
    "light_sports_walk": (
        "tired", "walk", "sport", "exercise", "park", "garden", "relax", "rest",
    ),
}


def _material_allowed_for_q(m: dict[str, Any], topic_en: str, qtext: str) -> bool:
    """Allow-listed topic + optional per-topic qHints + global require gate."""
    t = normalize_topic(topic_en)
    if t not in effective_topics(m):
        return False
    blob = f"{topic_en} {qtext}".lower()
    q_hints = (m.get("qHints") or {}).get(t)
    if q_hints and qtext and not any(k in blob for k in q_hints):
        return False
    req = _MATERIAL_Q_REQUIRE.get(m.get("id") or "")
    if req and qtext and not any(k in blob for k in req):
        return False
    return True


def materials_for_question(topic_en: str, qtext: str = "", limit: int = 3) -> list[dict[str, Any]]:
    """Per-question kits first; else topic pool + qHints scoring.

    Hard rule: do not force a kit onto a question that cannot serve the stem.
    Topic allow-list is only a candidate pool — not「同话题必须同一套」.
    """
    # 1) 题级白名单：可跨话题池选真正扣题的套装
    allow = QUESTION_KIT_ALLOW.get(_norm_q(qtext)) if qtext else None
    if allow:
        out: list[dict[str, Any]] = []
        seen: set[str] = set()
        for mid in allow:
            m = get_material(mid)
            if not m or mid in seen:
                continue
            seen.add(mid)
            out.append(m)
            if len(out) >= limit:
                break
        if out:
            return out

    # 2) 话题候选 + 本题 qHints/require；按题干关键词排序
    t = normalize_topic(topic_en)
    base = [m for m in MATERIALS.values() if _material_allowed_for_q(m, topic_en, qtext)]
    ql = (qtext or "").lower()
    if not base:
        # 仅在严格筛选为空时，退回话题池（仍不跨话题乱塞）
        base = [m for m in MATERIALS.values() if t in effective_topics(m)]
    if not ql:
        return base[:limit]

    scored = [(_material_hit_score(m, ql), i, m) for i, m in enumerate(base)]
    scored.sort(key=lambda x: (-x[0], x[1]))
    hits = [m for h, _, m in scored if h > 0]
    rest = [m for h, _, m in scored if h <= 0]
    out = []
    seen = set()
    for m in hits + rest:
        mid = m["id"]
        if mid in seen:
            continue
        seen.add(mid)
        out.append(m)
        if len(out) >= limit:
            break
    # 未进题级白名单的题：不足 2 套时用同话题料补位（仍不跨话题乱塞）
    if len(out) < min(2, limit):
        for m in MATERIALS.values():
            if t not in effective_topics(m) or m["id"] in seen:
                continue
            seen.add(m["id"])
            out.append(m)
            if len(out) >= min(2, limit):
                break
    return out


def material_ids_for_question(topic_en: str, qtext: str = "", limit: int = 3) -> list[str]:
    return [m["id"] for m in materials_for_question(topic_en, qtext, limit=limit)]

def export_bank_for_js() -> dict[str, Any]:
    return {
        "materials": [
            {
                "id": m["id"],
                "nameZh": m["nameZh"],
                "kind": m.get("kind") or "",
                "module": m.get("module") or "",
                "summary": m.get("summary") or "",
                "topics": effective_topics(m),
            }
            for m in MATERIALS.values()
        ],
        "feelPools": {
            "relax": FEEL_RELAX,
            "stress": FEEL_STRESS,
            "happy": FEEL_HAPPY,
            "practical": FEEL_PRACTICAL,
        },
        "freqPool": FREQ_OFTEN,
        "timeLine": TIME_LINE,
    }
