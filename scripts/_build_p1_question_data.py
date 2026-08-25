# -*- coding: utf-8 -*-
"""One-off builder: produce scripts/p1_question_data.json for all 231 heat questions."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from p1_word_banks_core import (  # noqa: E402
    CLUE_ALIAS,
    FIXES,
    TOPIC_KITS,
    apply_fixes,
    enrich_step_words,
    norm_q,
    pack,
    tweak_combined,
)

HEAT = ROOT / "_p1_heat_parsed.json"
CLUE = ROOT / "_p1_clue_index.json"
OUT = ROOT / "scripts" / "p1_question_data.json"

# Per-question overrides: norm_q -> {logic, words as 4 lists}
HAND: dict[str, dict] = {}


def hand(cat: str, q: str, logic: str, a: list, b: list, c: list, d: list) -> None:
    HAND[norm_q(q)] = {
        "cat": cat,
        "logic": logic,
        "words": pack(cat, a, b, c, d),
    }


def build_hand_banks() -> None:
  # === WATCH ===
    hand(
        "shishi",
        "Have you ever got a watch as a gift?",
        "事实：收到手表礼物→谁送的+实用；别聊名牌。",
        ["Yes, definitely", "Absolutely", "Sure"],
        ["from my parents", "birthday gift", "smartwatch"],
        ["on special occasions", "last year", "once"],
        ["really convenient", "practical", "a useful gift"],
    )
    hand(
        "xingwei",
        "Do you wear a watch?",
        "习惯：每天戴手表看时间，尤其上课/出门。",
        ["Yes, almost every day", "Definitely", "Usually"],
        ["check the time", "stay punctual", "before heading out"],
        ["during class", "when I head out", "every morning"],
        ["helps me stay organised", "really convenient", "saves time"],
    )
    hand(
        "guandian",
        "Why do some people wear expensive watches?",
        "观点：谈 status symbol / fashion，别说自己买奢侈品。",
        ["I think so", "It depends", "Probably"],
        ["status symbol", "fashion statement", "show success"],
        ["match outfits", "at formal events", "in daily life"],
        ["it depends on the person", "not my style", "understandable"],
    )
    hand(
        "guandian",
        "Do you think it is important to wear a watch? Why?",
        "观点：对学生=守时 punctual；可说不戴也行但方便。",
        ["Yes, quite important", "Quite useful", "It helps"],
        ["stay punctual", "check time quickly", "during class"],
        ["in class and meetings", "every day", "when busy"],
        ["I find it practical", "really convenient", "helps me focus"],
    )

    # === CARS ===
    hand(
        "xihao",
        "Did you enjoy traveling by car when you were a kid?",
        "喜好：童年坐车出游开心，去郊区/回老家。",
        ["Yes, I loved it", "Definitely", "So much fun"],
        ["family road trips", "when I was a child", "during holidays"],
        ["during the holidays", "a few times a year", "often"],
        ["feel relaxed and at ease", "great memories", "so much fun"],
    )
    hand(
        "xihao",
        "What types of cars do you like?",
        "喜好：SUV/舒适轿车，理由=空间/安全，别背参数。",
        ["I prefer SUVs", "Comfortable sedans", "Electric cars"],
        ["more space", "comfortable seats", "feel safer"],
        ["for long trips", "with my family", "in daily life"],
        ["feel safer", "more comfortable", "practical"],
    )
    hand(
        "xihao",
        "Will you buy an expensive car in the future?",
        "喜好：务实→先实用再考虑，或说毕业后努力买。",
        ["Maybe in the future", "Not sure yet", "Perhaps"],
        ["after I graduate", "when I can afford it", "a practical car first"],
        ["not at the moment", "in a few years", "after I start working"],
        ["practical matters more", "quality over price", "it depends"],
    )
    hand(
        "xingwei",
        "What do you usually do when there is a traffic jam?",
        "习惯：堵车时听歌/刷短视频/耐心等。",
        ["I stay calm", "I listen to music", "Usually patient"],
        ["listen to music", "watch short videos", "chat with friends"],
        ["during rush hour", "on the highway", "in the city"],
        ["helps me pass the time", "relieve stress", "stay relaxed"],
    )
    hand(
        "guandian",
        "Do you think car colours are important?",
        "观点：颜色=个性/耐脏，举例白车黑车。",
        ["It depends", "Somewhat", "For some people"],
        ["personality", "easy to keep clean", "white or black cars"],
        ["when buying a car", "in daily life", "for resale value"],
        ["some people care a lot", "not that important to me", "personal taste"],
    )
    hand(
        "duibi",
        "Do you prefer to be a driver or a passenger?",
        "对比：司机=自由；乘客=放松。",
        ["I'd rather be a passenger", "I prefer being a passenger", "Passenger"],
        ["more relaxing", "can rest", "less stressful"],
        ["driver has more control", "more tiring", "need to focus"],
        ["I feel more comfortable as a passenger", "can enjoy the view", "less pressure"],
    )

    # === WEBSITES ===
    hand(
        "shishi",
        "Are there any changes to the websites you often visit?",
        "事实：常用站改版/新功能，如学习网站或小红书。",
        ["Yes, definitely", "Quite a few", "Recently yes"],
        ["new layout", "more short videos", "updated design"],
        ["recently", "in the past year", "from time to time"],
        ["takes time to get used to", "mostly positive", "still useful"],
    )
    hand(
        "shishi",
        "What have you learned from websites that help with your life or studies?",
        "事实：从B站/知乎学技能、查资料。",
        ["Quite a lot", "A fair amount", "Definitely"],
        ["study skills", "cooking tips", "search information"],
        ["when I need help", "almost every day", "before exams"],
        ["really useful", "save me time", "practical"],
    )
    hand(
        "xihao",
        "What is your favourite website?",
        "喜好：B站/小红书/学校平台，说清用途。",
        ["Bilibili", "Xiaohongshu", "Definitely Bilibili"],
        ["watch tutorials", "relax", "learn new skills"],
        ["almost every day", "in my free time", "at night"],
        ["it always cheers me up", "really fun", "very useful"],
    )
    hand(
        "xihao",
        "Would you like to have your own website?",
        "喜好：想有个人博客/作品集，毕业后。",
        ["Yes, I'd love to", "Maybe someday", "Sounds cool"],
        ["share my portfolio", "write blog posts", "in the future"],
        ["not right now", "after graduation", "when I have time"],
        ["sounds cool", "a good idea", "would be fun"],
    )
    hand(
        "xingwei",
        "What kinds of websites do you often visit?",
        "习惯：学习+社交+购物网站。",
        ["Several types", "Quite a few", "Many kinds"],
        ["study resources", "social media", "shopping sites"],
        ["every day", "throughout the day", "whenever online"],
        ["save me a lot of time", "really convenient", "keep me updated"],
    )
    hand(
        "guandian",
        "What kinds of websites are popular in your country?",
        "观点：短视频/电商/外卖平台流行。",
        ["Short video apps", "E-commerce sites", "Social platforms"],
        ["Douyin", "Taobao", "WeChat"],
        ["almost everyone uses them", "every day", "all age groups"],
        ["very convenient", "really popular", "part of daily life"],
    )
    hand(
        "duibi",
        "Do you prefer getting information from websites or books?",
        "对比：网站快更新；书更系统。",
        ["I prefer websites", "Websites for sure", "Mostly websites"],
        ["faster", "up to date", "easy to search"],
        ["books are deeper", "better for focus", "more detailed"],
        ["websites suit my daily needs", "both are useful", "depends on the topic"],
    )

    # === TEACHERS ===
    hand(
        "shishi",
        "Do you have a teacher from your past that you still remember?",
        "事实：一位耐心老师+具体帮助。",
        ["Yes, clearly", "Definitely", "One in particular"],
        ["my high school English teacher", "very patient", "explained clearly"],
        ["years ago", "in high school", "still remember"],
        ["left a deep impression", "really grateful", "changed my attitude"],
    )
    hand(
        "shishi",
        "Are you still in touch with your primary school teachers?",
        "事实：偶尔联系/节日问候，或坦诚很少联系。",
        ["Not really", "Occasionally", "Rarely"],
        ["WeChat messages", "during festivals", "through my parents"],
        ["from time to time", "once a year", "almost never"],
        ["still grateful", "fond memories", "they were caring"],
    )
    hand(
        "shishi",
        "In what way has your favourite teacher helped you?",
        "事实：鼓励+讲题+树立信心。",
        ["In many ways", "Quite a lot", "Several ways"],
        ["encouraged me", "explained concepts clearly", "gave feedback"],
        ["when I struggled", "during exams", "through university prep"],
        ["gave me confidence", "made me believe in myself", "really supportive"],
    )
    hand(
        "xihao",
        "Do you have a favorite teacher?",
        "喜好：最喜欢某科老师，原因耐心有趣。",
        ["Yes, definitely", "Absolutely", "One favourite"],
        ["patient and humorous", "makes class engaging", "explains clearly"],
        ["every week", "in every class", "through the semester"],
        ["I enjoy their classes", "never boring", "learn a lot"],
    )
    hand(
        "xihao",
        "Do you want to be a teacher in the future?",
        "喜好：想当/不想当+原因（分享知识/压力大）。",
        ["Not really", "Maybe", "Haven't decided"],
        ["too much pressure", "love sharing knowledge", "respect the job"],
        ["haven't decided", "maybe later", "not my plan now"],
        ["it depends", "could be rewarding", "admire teachers"],
    )
    hand(
        "duibi",
        "Do you like your primary school teachers more than your high school teachers?",
        "对比：小学亲切 vs 高中严格但专业。",
        ["I prefer high school teachers", "Both were great", "Hard to choose"],
        ["more professional", "deeper knowledge", "better at explaining"],
        ["primary teachers were warmer", "like family", "more playful"],
        ["both mattered to me", "different stages", "each helped me grow"],
    )

    # === PUBLIC GARDENS AND PARKS ===
    hand(
        "xihao",
        "Did you like going to parks as a child?",
        "喜好：童年爱去公园玩/散步。",
        ["Yes, I loved it", "Absolutely", "So much fun"],
        ["play outside", "with my parents", "when I was a child"],
        ["at weekends", "during holidays", "often"],
        ["feel relaxed and at ease", "great memories", "fresh air"],
    )
    hand(
        "xihao",
        "Do you still like going to parks now?",
        "喜好：现在仍爱公园散步/透气。",
        ["Yes, definitely", "Still love it", "Quite often"],
        ["go for a walk", "fresh air", "escape the hustle and bustle"],
        ["at weekends", "after dinner", "when stressed"],
        ["helps me unwind", "feel at peace", "recharge my energy"],
    )
    hand(
        "xihao",
        "Would you like to see more parks in your city?",
        "喜好：希望更多绿地，理由健康休闲。",
        ["Yes, definitely", "Absolutely", "We need more"],
        ["more green space", "for families", "better air quality"],
        ["in my neighbourhood", "near schools", "city planning"],
        ["good for well-being", "everyone benefits", "really important"],
    )
    hand(
        "xihao",
        "Are there any parks you want to go to in the future?",
        "喜好：想去的公园/城市名+理由风景。",
        ["Yes, a few", "Definitely", "Several on my list"],
        ["a famous park", "with lakes", "better scenery"],
        ["during holidays", "next vacation", "when I travel"],
        ["sounds exciting", "on my bucket list", "would love to visit"],
    )
    hand(
        "xihao",
        "What do you like to do when visiting a park?",
        "喜好：散步/聊天/拍照/慢跑。",
        ["Go for a walk", "Hang out", "Several things"],
        ["with friends", "take photos", "go jogging"],
        ["at weekends", "after dinner", "when the weather is nice"],
        ["feel relaxed and at ease", "clear my mind", "enjoy nature"],
    )
    hand(
        "duibi",
        "Would you prefer to play in a personal garden or public garden?",
        "对比：私家花园安静 vs 公园设施多。",
        ["I'd prefer a public garden", "Public garden", "Depends"],
        ["more facilities", "bigger space", "meet more people"],
        ["personal garden is quieter", "more private", "at home"],
        ["public parks are more fun", "easier to access", "more variety"],
    )
    hand(
        "duibi",
        "How are the parks today different from those you visited as a kid?",
        "对比：现在公园更现代/更多健身设施。",
        ["Quite different", "Much better now", "Huge changes"],
        ["more playgrounds", "better paths", "fitness equipment"],
        ["older parks were simpler", "fewer facilities", "more natural"],
        ["both are nice", "prefer the upgrades", "more convenient now"],
    )

    # === SHOPPING ===
    hand(
        "shishi",
        "Have you ever returned anything you bought online?",
        "事实：网购退货经历+原因尺码/质量。",
        ["Yes, once", "A couple of times", "Definitely"],
        ["wrong size", "quality issue", "through online shopping"],
        ["last month", "from time to time", "rarely"],
        ["the process was easy", "a bit annoying", "sellers were helpful"],
    )
    hand(
        "xihao",
        "Do you like shopping?",
        "喜好：喜欢/不喜欢购物+网购方便。",
        ["Yes, I enjoy it", "Sometimes", "Not really"],
        ["shop online", "shopping malls", "pay by phone"],
        ["at weekends", "when I need things", "from time to time"],
        ["really convenient", "fun with friends", "can be tiring"],
    )
    hand(
        "xingwei",
        "How often do you go shopping?",
        "习惯：网购频繁/偶尔逛商场。",
        ["Quite often", "From time to time", "Almost every week"],
        ["shop online", "shopping malls", "buy clothes"],
        ["at weekends", "when I need something", "every few weeks"],
        ["really convenient", "save time", "enjoy browsing sometimes"],
    )
    hand(
        "duibi",
        "Do you prefer online shopping or in-store shopping?",
        "对比：网购方便 vs 实体店可试穿。",
        ["I prefer online shopping", "Online for sure", "Mostly online"],
        ["more convenient", "pay by phone", "delivered to my door"],
        ["can try on clothes", "see the quality", "instant purchase"],
        ["online suits my lifestyle", "both have pros", "depends on the item"],
    )

    # === MIRRORS ===
    hand(
        "shishi",
        "Have you ever bought mirrors?",
        "事实：买过镜子装饰/化妆镜。",
        ["Yes, once", "A few times", "Not really"],
        ["a small mirror", "for my desk", "decorative mirror"],
        ["last year", "when I moved", "rarely"],
        ["practical and cheap", "looks nice", "useful daily"],
    )
    hand(
        "xihao",
        "Do you like looking at yourself in the mirror? How often?",
        "喜好：出门前照镜子+频率每天。",
        ["Yes, I do", "Every day", "Quite often"],
        ["before heading out", "check my look", "when getting dressed"],
        ["every morning", "before parties", "almost daily"],
        ["feel more confident", "part of my routine", "takes a minute"],
    )
    hand(
        "xihao",
        "Would you use mirrors to decorate your room?",
        "喜好：会用镜子装饰/或觉得不需要。",
        ["Maybe", "Yes, I would", "Not really"],
        ["make the room brighter", "modern look", "above the desk"],
        ["if I redecorate", "in the future", "not now"],
        ["looks stylish", "practical too", "personal taste"],
    )
    hand(
        "xingwei",
        "Do you usually take a mirror with you?",
        "习惯：包里小镜子/用手机代替。",
        ["Not usually", "Sometimes", "Rarely"],
        ["use my phone", "small pocket mirror", "only for travel"],
        ["when travelling", "at formal events", "almost never"],
        ["phone is enough", "not necessary", "convenient either way"],
    )

    # === MUSIC ===
    hand(
        "shishi",
        "Have you taken any music classes?",
        "事实：学过音乐课/乐器经历。",
        ["Yes, in school", "A short course", "Not really"],
        ["music class", "learned guitar", "in primary school"],
        ["years ago", "for one semester", "when I was young"],
        ["was fun", "basic skills", "wish I continued"],
    )
    hand(
        "xingwei",
        "Do you listen to music while doing other things?",
        "习惯：学习/运动时听歌。",
        ["Yes, often", "Almost always", "Quite often"],
        ["while studying", "on the subway", "during workouts"],
        ["every day", "when I commute", "in my free time"],
        ["helps me focus", "relieve stress", "makes tasks easier"],
    )
    hand(
        "guandian",
        "Does happy music make you feel more excited?",
        "观点：欢快音乐让人更有活力。",
        ["Yes, definitely", "Absolutely", "Most of the time"],
        ["upbeat songs", "faster tempo", "before exercising"],
        ["when I'm tired", "in the morning", "at parties"],
        ["feel more energetic", "in a better mood", "mood booster"],
    )
    hand(
        "duibi",
        "Do you prefer sad or happy music?",
        "对比：开心音乐解压 vs 慢歌安静。",
        ["I prefer happy music", "Happy music", "Mostly upbeat"],
        ["relieve stress", "feel more positive", "while studying"],
        ["sad songs are emotional", "good when relaxing", "sometimes meaningful"],
        ["happy music fits my mood", "both are fine", "depends on the moment"],
    )

    # === CLOTHING ===
    hand(
        "xihao",
        "What kind of clothes do you like to wear?",
        "喜好：休闲舒适为主，T恤牛仔裤。",
        ["Casual clothes", "Comfortable styles", "Simple outfits"],
        ["t-shirt", "jeans", "sneakers"],
        ["every day", "at university", "on weekdays"],
        ["feel comfortable", "easy to match", "practical"],
    )
    hand(
        "xihao",
        "Do you like wearing T-shirts?",
        "喜好：爱穿T恤，理由舒服百搭。",
        ["Yes, I love them", "Definitely", "All the time"],
        ["comfortable", "easy to wash", "go with everything"],
        ["in summer", "almost every day", "at home too"],
        ["feel relaxed", "my go-to choice", "never go wrong"],
    )
    hand(
        "xihao",
        "What colour clothes do you like?",
        "喜好：颜色偏好+理由（耐脏/显气质）。",
        ["Blue and white", "Dark colours", "Neutral tones"],
        ["easy to match", "look clean", "not too flashy"],
        ["when shopping", "in daily life", "most of my wardrobe"],
        ["feel confident", "practical choice", "personal style"],
    )
    hand(
        "xingwei",
        "Do you spend a lot of time choosing clothes?",
        "习惯：出门前选衣时间长短。",
        ["Not really", "Sometimes", "A few minutes"],
        ["grab my things and head out", "pick quickly", "same style daily"],
        ["every morning", "before class", "on weekdays"],
        ["prefer simplicity", "save time", "not fussy about fashion"],
    )
    hand(
        "duibi",
        "Do you prefer to wear comfortable and casual clothes or smart clothes?",
        "对比：休闲舒服 vs 正式得体。",
        ["Comfortable and casual", "Casual for sure", "Comfort first"],
        ["t-shirt", "sneakers", "soft fabrics"],
        ["smart clothes for interviews", "formal events", "look professional"],
        ["casual fits my lifestyle", "smart when needed", "both have uses"],
    )
    hand(
        "duibi",
        "Do you wear different styles of clothes on weekdays and weekends?",
        "对比：工作日简约 vs 周末更随意。",
        ["Yes, quite different", "A little different", "Somewhat"],
        ["casual on weekends", "sportswear", "more colourful"],
        ["simple on weekdays", "uniform-like", "for class"],
        ["weekends feel freer", "both are comfortable", "depends on plans"],
    )

    # === TIDINESS ===
    hand(
        "xihao",
        "Do you like to keep things tidy?",
        "喜好：爱整洁→桌面整齐更好学习。",
        ["Yes, definitely", "I try to", "Quite important to me"],
        ["study desk", "put things away", "organised space"],
        ["every day", "before studying", "at the end of the day"],
        ["focus better", "feel less stressed", "more productive"],
    )
    hand(
        "xingwei",
        "Did you keep your room tidy as a child?",
        "习惯：童年房间整不整齐+父母督促。",
        ["Not really", "My parents helped", "Sometimes"],
        ["messy desk", "toys everywhere", "needed reminders"],
        ["when I was young", "before exams", "on weekends"],
        ["learned over time", "childhood habit", "got better later"],
    )
    hand(
        "xingwei",
        "How do you keep your work or study space tidy?",
        "习惯：每天收拾桌面/分类收纳。",
        ["I tidy up daily", "Put things away", "A quick clean"],
        ["sort my notes", "clear the desk", "throw out rubbish"],
        ["after studying", "every evening", "before I start work"],
        ["focus better", "feel more organised", "saves time later"],
    )
    hand(
        "guandian",
        "Do you think that it is necessary to be tidy?",
        "观点：整洁提高效率，但不必完美主义。",
        ["Yes, quite necessary", "It helps a lot", "Generally yes"],
        ["focus better", "find things easily", "clear mind"],
        ["for studying", "at work", "in shared spaces"],
        ["good habit", "not obsessive though", "balance is key"],
    )

    # === HEADPHONES ===
    hand(
        "shishi",
        "What type of headphones do you use?",
        "事实：无线/入耳式耳机+主要用途。",
        ["Wireless earbuds", "Over-ear headphones", "Bluetooth ones"],
        ["listen to music", "on the subway", "while studying"],
        ["every day", "when commuting", "in my free time"],
        ["block noise", "really convenient", "good sound quality"],
    )
    hand(
        "xingwei",
        "Do you use headphones?",
        "习惯：经常用耳机听歌/听课。",
        ["Yes, almost every day", "Quite often", "Definitely"],
        ["listen to music", "online lectures", "on the subway"],
        ["when commuting", "in the library", "every day"],
        ["block background noise", "helps me focus", "private listening"],
    )
    hand(
        "xingwei",
        "When would you use headphones?",
        "习惯：通勤/图书馆/运动时戴耳机。",
        ["When commuting", "While studying", "Several situations"],
        ["on the subway", "in the library", "during workouts"],
        ["every morning", "before exams", "at the gym"],
        ["block noise", "stay focused", "enjoy music privately"],
    )
    hand(
        "xingwei",
        "In what conditions would you not use headphones?",
        "习惯：上课/与人交流时不戴。",
        ["In class", "When chatting", "At gatherings"],
        ["need to hear others", "safety on the street", "face-to-face talks"],
        ["during meetings", "with family", "when walking at night"],
        ["stay aware", "be polite", "safety first"],
    )
    hand(
        "guandian",
        "Is wearing headphones comfortable?",
        "观点：短时间舒服，久了耳朵累。",
        ["Mostly yes", "It depends", "For a while"],
        ["soft ear cushions", "wireless is light", "good for commuting"],
        ["after an hour", "long sessions", "cheap ones hurt"],
        ["comfortable enough", "take breaks sometimes", "worth it for music"],
    )

    # === SOCIAL MEDIA ===
    hand(
        "shishi",
        "Have you ever posted anything on social media?",
        "事实：发过照片/动态的经历。",
        ["Yes, many times", "Occasionally", "A few times"],
        ["post photos", "share daily life", "on WeChat"],
        ["at weekends", "during holidays", "from time to time"],
        ["keep in touch", "fun to share", "get reactions from friends"],
    )
    hand(
        "shishi",
        "When did you start using social media?",
        "事实：初中/高中开始用微信等。",
        ["In high school", "Years ago", "Around age 15"],
        ["WeChat", "Xiaohongshu", "with my classmates"],
        ["since high school", "for many years", "early teens"],
        ["part of daily life", "hard to imagine without it", "very common"],
    )
    hand(
        "shishi",
        "Do your friends use social media?",
        "事实：朋友都用社媒聊天发动态。",
        ["Yes, all of them", "Almost everyone", "Definitely"],
        ["WeChat", "post photos", "chat every day"],
        ["every day", "constantly", "all the time"],
        ["easy to connect", "share moments", "stay updated"],
    )
    hand(
        "guandian",
        "Do you think you spend too much time on social media?",
        "观点：承认有点多，但用于学习/社交。",
        ["Sometimes yes", "A bit too much", "It depends"],
        ["watch short videos", "chat with friends", "browse feeds"],
        ["before bed", "during breaks", "too often"],
        ["should cut down", "also useful", "need self-control"],
    )
    hand(
        "guandian",
        "What do people often do on social media?",
        "观点：聊天、刷视频、晒生活。",
        ["Many things", "Quite a lot", "Various activities"],
        ["chat with friends", "watch short videos", "post photos"],
        ["every day", "in their free time", "before bed"],
        ["stay connected", "entertainment", "part of modern life"],
    )

    # === SINGING ===
    hand(
        "shishi",
        "Have you ever learnt how to sing?",
        "事实：学过唱歌/KTV经历。",
        ["Yes, a little", "In music class", "Self-taught"],
        ["sing a song", "at KTV", "with friends"],
        ["years ago", "during holidays", "occasionally"],
        ["was fun", "not very skilled", "enjoyed it"],
    )
    hand(
        "shishi",
        "Have you ever taken a singing class?",
        "事实：是否上过声乐课。",
        ["Yes, briefly", "In school", "Not really"],
        ["music class", "learned basics", "school choir"],
        ["in primary school", "one semester", "years ago"],
        ["interesting experience", "built confidence", "was nervous"],
    )
    hand(
        "xihao",
        "Do you like singing? Why?",
        "喜好：喜欢唱歌因为开心/解压。",
        ["Yes, I love it", "Quite enjoy it", "Sometimes"],
        ["it always cheers me up", "with friends at KTV", "relieve stress"],
        ["at weekends", "with friends", "when I'm happy"],
        ["feel relaxed", "great fun", "express emotions"],
    )
    hand(
        "xihao",
        "Who do you want to sing for?",
        "喜好：想为家人/朋友唱。",
        ["My closest friends", "My family", "Close friends"],
        ["at gatherings", "birthday parties", "casual hangouts"],
        ["on special days", "when we meet", "at KTV"],
        ["share happiness", "create memories", "feel connected"],
    )
    hand(
        "xihao",
        "Do you like listening to others singing?",
        "喜好：听别人唱歌看综艺/比赛。",
        ["Yes, definitely", "Quite enjoy it", "Sometimes"],
        ["music shows", "friends at KTV", "live performances"],
        ["on TV", "at parties", "online videos"],
        ["inspiring", "relaxing", "appreciate their talent"],
    )
    hand(
        "guandian",
        "Do you think singing can bring happiness to people?",
        "观点：唱歌释放情绪、增进感情。",
        ["Yes, absolutely", "Definitely", "I believe so"],
        ["share joy", "relieve stress", "bond with others"],
        ["at parties", "in daily life", "for all ages"],
        ["music heals", "universal language", "simple but powerful"],
    )

    # === OUTER SPACE ===
    hand(
        "shishi",
        "Have you ever learnt about outer space and stars?",
        "事实：学校科学课/纪录片了解太空。",
        ["Yes, in school", "Through documentaries", "A bit"],
        ["science class", "documentaries", "science fiction movies"],
        ["in primary school", "years ago", "from time to time"],
        ["found it fascinating", "sparked curiosity", "still curious"],
    )
    hand(
        "xihao",
        "Do you like science fiction movies? Why?",
        "喜好：爱科幻片因为想象力和视觉震撼。",
        ["Yes, I'm a big fan", "Love them", "Quite enjoy them"],
        ["imagination", "visual effects", "future technology"],
        ["in my free time", "with friends", "on weekends"],
        ["really fun", "mind-blowing", "inspire curiosity"],
    )
    hand(
        "xihao",
        "Do you want to know more about outer space?",
        "喜好：想了解更多宇宙知识。",
        ["Yes, definitely", "Quite curious", "Absolutely"],
        ["documentaries", "books about space", "online videos"],
        ["when I have time", "in the future", "from time to time"],
        ["universe is mysterious", "always learning", "fascinating topic"],
    )
    hand(
        "xihao",
        "Do you want to go into outer space in the future?",
        "喜好：想去/太遥远/看纪录片就够。",
        ["Maybe in dreams", "Not realistically", "Would be amazing"],
        ["if technology allows", "as a tourist", "not for me"],
        ["in the distant future", "not soon", "hard to say"],
        ["sounds thrilling", "too risky", "happy to watch from Earth"],
    )

    # === SCIENCE ===
    hand(
        "shishi",
        "When did you start to learn about science?",
        "事实：小学科学课开始接触。",
        ["In primary school", "Around age 7", "Early years"],
        ["science class", "simple experiments", "with my teacher"],
        ["years ago", "through school", "step by step"],
        ["was interesting", "built curiosity", "foundation for later"],
    )
    hand(
        "shishi",
        "What kinds of interesting things have you done with science?",
        "事实：实验课/参观科技馆经历。",
        ["Several things", "A few experiments", "Quite a few"],
        ["science museum", "lab experiments", "biology projects"],
        ["in school", "during holidays", "years ago"],
        ["really fun", "hands-on learning", "memorable experiences"],
    )
    hand(
        "xihao",
        "Do you like science?",
        "喜好：喜欢/一般+实验有趣。",
        ["Yes, quite a lot", "Somewhat", "Certain topics"],
        ["interesting experiments", "understand the world", "biology"],
        ["in school", "when topics are practical", "from time to time"],
        ["curious mind", "sometimes challenging", "worth learning"],
    )
    hand(
        "xihao",
        "Which science subject is interesting to you?",
        "喜好：生物/物理等+具体原因。",
        ["Biology", "Physics", "Chemistry"],
        ["human body", "how things work", "experiments"],
        ["in high school", "still now", "most classes"],
        ["really fun", "practical knowledge", "easier to relate"],
    )
    hand(
        "xihao",
        "Do you like watching science TV programs?",
        "喜好：看科普节目/纪录片。",
        ["Yes, sometimes", "Quite enjoy them", "Occasionally"],
        ["documentaries", "science channels", "online videos"],
        ["in my free time", "with my family", "before bed"],
        ["learn new things", "relaxing and informative", "well made"],
    )
    hand(
        "guandian",
        "Do Chinese people often visit science museums?",
        "观点：假期带孩子去科技馆很常见。",
        ["Yes, quite often", "Especially families", "Quite popular"],
        ["science museum", "interactive exhibits", "during holidays"],
        ["on weekends", "school trips", "during vacations"],
        ["educational and fun", "good for kids", "worth visiting"],
    )

    # === JOKES & COMEDIES ===
    hand(
        "shishi",
        "Are you good at telling jokes?",
        "事实：坦诚不太会/偶尔讲冷笑话。",
        ["Not really", "A little", "Sometimes"],
        ["forget the punchline", "only simple jokes", "with close friends"],
        ["rarely", "at gatherings", "when mood is right"],
        ["others laugh more", "still fun", "not my strength"],
    )
    hand(
        "shishi",
        "Do your friends like to tell jokes?",
        "事实：朋友爱讲笑话活跃气氛。",
        ["Yes, some do", "Quite a few", "Especially one friend"],
        ["make people laugh", "at parties", "on WeChat"],
        ["when we hang out", "quite often", "to lighten the mood"],
        ["great atmosphere", "have a good laugh", "feel closer"],
    )
    hand(
        "shishi",
        "Have you ever watched a live show?",
        "事实：看过脱口秀/相声现场演出。",
        ["Yes, once", "A couple of times", "Not yet"],
        ["stand-up comedy", "live show", "with friends"],
        ["last year", "during a festival", "rarely"],
        ["have a good laugh", "great atmosphere", "unforgettable night"],
    )
    hand(
        "xihao",
        "Do you like to watch comedies?",
        "喜好：爱看喜剧电影/综艺解压。",
        ["Yes, definitely", "Love comedies", "Quite often"],
        ["watch comedies", "funny TV shows", "stand-up clips"],
        ["at weekends", "after a long day", "with friends"],
        ["have a good laugh", "relieve stress", "feel lighter"],
    )
    hand(
        "guandian",
        "Are comedy shows popular in your country?",
        "观点：脱口秀/喜剧综艺很火。",
        ["Yes, very popular", "Quite popular", "Growing fast"],
        ["stand-up comedy", "TV variety shows", "online clips"],
        ["young people love them", "every weekend", "on streaming apps"],
        ["easy entertainment", "social topic", "good stress relief"],
    )

    # === AREA ===
    hand(
        "shishi",
        "Do you know any famous people in your area?",
        "事实：当地名人/网红或坦诚不认识。",
        ["Not personally", "One or two", "On TV only"],
        ["a local influencer", "historical figure", "community leader"],
        ["in the news", "heard from neighbours", "rarely"],
        ["interesting stories", "not that famous", "part of local culture"],
    )
    hand(
        "shishi",
        "What are some changes in the area recently?",
        "事实：新建商场/地铁/环境变化。",
        ["Quite a few", "Several changes", "Definitely"],
        ["new shopping malls", "subway extension", "more cafes"],
        ["recently", "in the past few years", "ever since I moved here"],
        ["more convenient", "busier now", "better facilities"],
    )
    hand(
        "shishi",
        "Do you know any of your neighbors?",
        "事实：认识几位邻居/偶尔打招呼。",
        ["A few of them", "Some neighbours", "Not many"],
        ["say hello", "elderly couple", "same building"],
        ["when we meet", "in the elevator", "from time to time"],
        ["friendly enough", "peaceful community", "feel safe"],
    )
    hand(
        "shishi",
        "Are the people in your neighborhood nice and friendly?",
        "事实：邻居友善互助或一般。",
        ["Yes, quite friendly", "Most are nice", "Generally yes"],
        ["help each other", "say hello", "quiet community"],
        ["in daily life", "when needed", "always"],
        ["feel safe", "warm atmosphere", "comfortable living here"],
    )
    hand(
        "shishi",
        "Do you live in a noisy or a quiet area?",
        "事实：安静住宅区或临街略吵。",
        ["Quite quiet", "Mostly quiet", "A bit noisy"],
        ["residential area", "away from main road", "near a market"],
        ["at night", "during rush hour", "on weekdays"],
        ["peaceful at night", "can sleep well", "busy in the morning"],
    )

    # === HOME transport ===
    hand(
        "shishi",
        "Are the transport facilities to your home very good?",
        "事实：地铁公交方便/离家近。",
        ["Yes, quite good", "Very convenient", "Pretty decent"],
        ["near the subway", "bus stops nearby", "easy to get around"],
        ["every day", "when commuting", "to university"],
        ["save a lot of time", "really convenient", "rarely late"],
    )

    # === HOMETOWN history/culture ===
    hand(
        "shishi",
        "Did you learn about the history of your hometown at school?",
        "事实：学校历史课讲过家乡。",
        ["Yes, briefly", "In history class", "A little"],
        ["local history", "famous events", "in textbooks"],
        ["in middle school", "years ago", "one chapter"],
        ["interesting", "proud of my hometown", "basic knowledge"],
    )
    hand(
        "shishi",
        "Are there many young people in your hometown?",
        "事实：年轻人多/少+就业吸引力。",
        ["Yes, quite a few", "A good number", "Not that many"],
        ["university students", "young workers", "start-up scene"],
        ["nowadays", "in the city centre", "compared to before"],
        ["lively atmosphere", "more opportunities", "some moved away"],
    )
    hand(
        "shishi",
        "Have you learned anything about the history of your hometown?",
        "事实：博物馆/家人讲述了解历史。",
        ["Yes, some things", "A fair amount", "From family"],
        ["local museum", "grandparents' stories", "history books"],
        ["during holidays", "when I was young", "from time to time"],
        ["proud heritage", "know my roots", "interesting past"],
    )
    hand(
        "shishi",
        "Did you learn about the culture of your hometown in your childhood?",
        "事实：童年节日习俗/地方美食文化。",
        ["Yes, through festivals", "From my family", "Quite a lot"],
        ["local festivals", "traditional food", "folk customs"],
        ["during childhood", "every spring festival", "with grandparents"],
        ["warm memories", "part of who I am", "still practise some"],
    )

    # === CITY ===
    hand(
        "shishi",
        "Are there big changes in this city?",
        "事实：城市变化：新建筑/交通发展。",
        ["Yes, huge changes", "Definitely", "Many changes"],
        ["new skyscrapers", "expanded subway", "more parks"],
        ["in recent years", "since I arrived", "constantly"],
        ["more modern", "more convenient", "hard to recognise some areas"],
    )
    hand(
        "shishi",
        "Are there people of different ages living in this city?",
        "事实：各年龄段都有，老少皆宜。",
        ["Yes, all ages", "Definitely", "Very diverse"],
        ["young professionals", "families with kids", "elderly residents"],
        ["everywhere", "in every district", "in my neighbourhood"],
        ["vibrant mix", "balanced community", "feel inclusive"],
    )
    hand(
        "shishi",
        "Are the people friendly in the city?",
        "事实：城市人友善/忙碌但乐于助人。",
        ["Yes, quite friendly", "Most are helpful", "Generally yes"],
        ["give directions", "help strangers", "polite in shops"],
        ["when you need help", "in daily interactions", "often"],
        ["feel welcome", "warm despite busy life", "positive impression"],
    )

    # === VIEWS ===
    hand(
        "shishi",
        "Have you seen an unforgettable and beautiful view or scenery?",
        "事实：旅行见过的山海/城市夜景。",
        ["Yes, absolutely", "Several times", "One stands out"],
        ["mountain sunrise", "sea at sunset", "city night view"],
        ["while travelling", "last summer", "on vacation"],
        ["unforgettable", "took many photos", "still remember clearly"],
    )

    # === MEMORY ===
    hand(
        "shishi",
        "Are you good at memorising things?",
        "事实：记忆力好/一般+用手机备忘。",
        ["Average", "Pretty good", "Depends on the topic"],
        ["phone notes", "to-do list", "repeat out loud"],
        ["for exams", "daily reminders", "important dates"],
        ["works for me", "still forget sometimes", "need reminders"],
    )
    hand(
        "shishi",
        "Have you ever forgotten something important?",
        "事实：忘带钥匙/证件经历+教训。",
        ["Yes, unfortunately", "Once or twice", "More than once"],
        ["forgot my keys", "missed a deadline", "left my ID at home"],
        ["last semester", "years ago", "recently"],
        ["it taught me to be more careful", "really stressful", "learned a lesson"],
    )
    hand(
        "shishi",
        "What do you need to remember in your daily life?",
        "事实：课程表/作业/约会日程。",
        ["Many things", "Quite a lot", "A long list"],
        ["class schedule", "assignments", "friends' birthdays"],
        ["every day", "every morning", "before leaving home"],
        ["phone reminders help", "sometimes stressful", "part of student life"],
    )
    hand(
        "xingwei",
        "How do you remember important things?",
        "习惯：手机备忘录/清单/重复记忆。",
        ["Phone notes", "To-do lists", "Several methods"],
        ["set reminders", "write them down", "repeat aloud"],
        ["every day", "before exams", "for appointments"],
        ["rarely forget", "really convenient", "saves mental energy"],
    )

    # === LIFE STAGES ===
    hand(
        "shishi",
        "What did you often do with your friends in your childhood?",
        "事实：童年和朋友户外玩/骑车。",
        ["Many things", "Quite a lot", "Played outside"],
        ["play outside", "ride bikes", "play video games"],
        ["after school", "at weekends", "almost every day"],
        ["carefree days", "great memories", "still close friends"],
    )
    hand(
        "shishi",
        "Do you have any plans for the next five years?",
        "事实：五年计划：毕业/工作/提升。",
        ["Yes, definitely", "A rough plan", "Several goals"],
        ["graduate", "find a good job", "improve my skills"],
        ["after university", "step by step", "in the next few years"],
        ["excited about the future", "need to work hard", "clear direction"],
    )
    hand(
        "xihao",
        "Do you enjoy being the age you are now?",
        "喜好：享受当下青春/压力也有。",
        ["Yes, mostly", "Quite enjoy it", "It's okay"],
        ["freedom at university", "learn and grow", "meet new people"],
        ["at this stage of my life", "right now", "these years"],
        ["full of opportunities", "some pressure too", "grateful for now"],
    )
    hand(
        "guandian",
        "How do people remember each stage of their lives?",
        "观点：靠照片/日记/重要事件标记。",
        ["In different ways", "Through memories", "Many methods"],
        ["photos", "diaries", "important milestones"],
        ["birthdays", "graduations", "family trips"],
        ["precious memories", "shape who we are", "look back fondly"],
    )
    hand(
        "guandian",
        "At what age do you think people are the happiest?",
        "观点：童年无忧无虑或青年有自由。",
        ["It varies", "Childhood perhaps", "Hard to say"],
        ["childhood is carefree", "young adults have freedom", "depends on the person"],
        ["different life stages", "for different people", "no single answer"],
        ["each age has joys", "subjective question", "interesting to think about"],
    )

    # === SPARE TIME ===
    hand(
        "xihao",
        "Would you like to have more free time in the future?",
        "喜好：希望更多空闲休息/发展爱好。",
        ["Yes, definitely", "Absolutely", "Would love that"],
        ["develop hobbies", "get proper rest", "travel more"],
        ["after graduation", "when work is stable", "in the future"],
        ["balance is important", "everyone needs downtime", "quality over quantity"],
    )
    hand(
        "xingwei",
        "Do you often have free time?",
        "习惯：空闲时间多不多+学业忙。",
        ["Not much lately", "Some evenings", "At weekends"],
        ["busy with studies", "packed schedule", "after assignments"],
        ["at weekends", "before exams", "rarely on weekdays"],
        ["wish I had more", "use it wisely", "still manage to relax"],
    )
    hand(
        "xingwei",
        "What do you usually do in your spare time?",
        "习惯：刷视频/运动/和朋友聚会。",
        ["Several things", "A few favourites", "Depends on mood"],
        ["watch short videos", "hang out", "do some sports"],
        ["at weekends", "in my free time", "after dinner"],
        ["relieve stress", "helps me unwind", "recharge my energy"],
    )
    hand(
        "duibi",
        "Which day do you have more free time on, Saturday or Sunday?",
        "对比：周六外出周日休息或相反。",
        ["Saturday", "Sunday", "It depends"],
        ["hang out with friends", "go shopping", "more social"],
        ["stay at home", "finish homework", "prepare for Monday"],
        ["Saturday is livelier", "Sunday is calmer", "both are precious"],
    )

    # === GIFTS ===
    hand(
        "shishi",
        "Have you ever sent handmade gifts to others?",
        "事实：送过手工礼物→具体做了什么+对方反应。",
        ["Yes, I have", "A few times", "Definitely"],
        ["a handmade card", "knitted scarf", "DIY gift"],
        ["on birthdays", "for close friends", "from time to time"],
        ["they were touched", "meaningful", "worth the effort"],
    )
    hand(
        "shishi",
        "Have you ever received a great gift?",
        "事实：收到好礼物→谁送的+为什么感动。",
        ["Yes, definitely", "Absolutely", "Sure"],
        ["a thoughtful gift", "from my best friend", "last month"],
        ["on my birthday", "last year", "once in a while"],
        ["really surprised", "made me happy", "unexpected surprise"],
    )
    hand(
        "shishi",
        "What gift have you received recently?",
        "事实：最近礼物→物品+场合+一句感受。",
        ["Yes, recently", "Just last month", "A small gift"],
        ["a book", "from my parents", "birthday present"],
        ["last month", "this year", "not long ago"],
        ["really thoughtful", "practical", "I loved it"],
    )

    hand(
        "xihao",
        "What are your favourite activities?",
        "喜好：现在最爱运动/听歌/阅读等。",
        ["Several favourites", "A few main ones", "Quite a few"],
        ["listen to music", "do some sports", "read"],
        ["in my free time", "at weekends", "almost every day"],
        ["keep me happy", "relieve stress", "good balance"],
    )
    hand(
        "duibi",
        "Are there any differences between the activities you liked when you were a child and those you like now?",
        "对比：童年户外 vs 现在室内/手机。",
        ["Yes, quite different", "Totally different", "Somewhat different"],
        ["play outside as a kid", "more screen time now", "different interests"],
        ["childhood was outdoors", "toys and games", "with neighbourhood friends"],
        ["natural shift", "still enjoy active things", "life changes interests"],
    )

    # === MORNING (childhood why already in clue, add explicit for derived) ===
    # covered by clue tweak

    # === BUILDING (remaining derived) ===
    hand(
        "xihao",
        "Do you want to live in a tall building?",
        "喜好：想住高楼视野好/或担心电梯不方便。",
        ["Maybe", "Not really", "It depends"],
        ["good views", "modern facilities", "near the city centre"],
        ["in the future", "when I work", "not now"],
        ["sounds convenient", "worry about elevators", "prefer lower floors"],
    )

    # === PETS (remaining derived) ===
    hand(
        "xingwei",
        "How often do you visit a zoo?",
        "习惯：偶尔去动物园，假期带孩子或朋友。",
        ["Not very often", "Occasionally", "A few times a year"],
        ["with friends", "see animals", "city zoo"],
        ["during holidays", "once or twice a year", "when I have time"],
        ["fun experience", "learn about animals", "good for a day out"],
    )
    hand(
        "guandian",
        "Are there many people keeping pets in your country?",
        "观点：养宠物越来越普遍，尤其猫狗。",
        ["Yes, more and more", "Quite common", "Definitely growing"],
        ["cats and dogs", "especially in cities", "emotional companions"],
        ["nowadays", "among young people", "in urban areas"],
        ["shows lifestyle change", "pets bring joy", "responsible ownership matters"],
    )
    hand(
        "guandian",
        "Should schools teach students knowledge about pets or animals?",
        "观点：应该教，培养爱心与责任感。",
        ["Yes, they should", "Definitely", "Absolutely"],
        ["animal welfare", "respect nature", "responsible pet care"],
        ["in science class", "through field trips", "at primary school"],
        ["build empathy", "practical knowledge", "good for society"],
    )


def topic_template_words(cat_id: str, topic_en: str, qtext: str) -> tuple[list, list, list, list] | None:
    """Fallback 4-step chip lists from TOPIC_KITS when no hand/clue match."""
    key = topic_en.lower().strip()
    kit = TOPIC_KITS.get(key)
    if not kit:
        for k, v in TOPIC_KITS.items():
            if k in key or key in k:
                kit = v
                break
    if not kit:
        return None
    chips = kit["chips"]
    ql = qtext.lower()
    ans = ["Yes", "Definitely", "Absolutely"]
    if any(x in ql for x in ["not", "dislike", "don't", "never"]):
        ans = ["Not really", "Not often", "Sometimes"]
    freq = ["every day", "from time to time", "at weekends", "in my free time"]
    feel_shishi = ["practical", "really convenient", "quite useful"]
    feel_xihao = ["feel relaxed", "really enjoyable", "it always cheers me up"]
    feel = feel_shishi
    if cat_id == "xihao":
        feel = feel_xihao
    elif cat_id == "xingwei":
        feel = ["helps me stay focused", "saves time", "keeps me organised"]
    elif cat_id == "guandian":
        feel = ["quite important", "makes sense", "understandable"]
    elif cat_id == "duibi":
        feel = ["I prefer", "more comfortable", "which is why"]
    if cat_id == "shishi":
        return ans, chips[:4], freq[:3], feel[:3]
    if cat_id == "xihao":
        return ans, chips[:3] + ["in my free time"], freq[:3], feel[:3]
    if cat_id == "xingwei":
        return ans, chips[:3], ["every morning", "in my free time", chips[0]], feel[:2] + ["helps me focus"]
    if cat_id == "guandian":
        return ["I think so", "It depends", "Yes"], chips[:4], ["in daily life", "for most people", "nowadays"], feel[:2] + ["understandable"]
    return ["I prefer", "It depends", "I'd rather"], chips[:3], chips[2:5], feel[:2] + ["I feel more comfortable"]


def topic_logic(cat_id: str, topic_en: str, qtext: str) -> str:
    key = topic_en.lower().strip()
    kit = TOPIC_KITS.get(key)
    if not kit:
        for k, v in TOPIC_KITS.items():
            if k in key or key in k:
                kit = v
                break
    base = kit.get("logic", "用地点/频次/感受撑满四步，避免编造复杂故事。") if kit else "先直接回答，再举具体例子，补频次，最后感受收束。"
    ql = qtext.lower()
    if cat_id == "shishi":
        if ql.startswith("have you ever"):
            return f"事实：{base.split('；')[0] if '；' in base else base}"
        return f"事实：直接 Yes/No + 具体细节；{base}"
    if cat_id == "xihao":
        return f"喜好：说清喜欢什么+原因；{base}"
    if cat_id == "xingwei":
        return f"习惯：描述日常频率和场景；{base}"
    if cat_id == "guandian":
        return f"观点：先表态再理由；{base}"
    return f"对比：两边各说特点再表态；{base}"


def resolve_one(cat_id: str, topic_en: str, qtext: str, steps: list[str], clue_index: dict) -> dict:
    key = norm_q(qtext)
    logic = ""
    words: dict[str, list[str]] = {}
    source = "derived"

    if key in HAND:
        entry = HAND[key]
        logic = entry["logic"]
        words = {s: list(entry["words"].get(s, [])) for s in steps}
        source = "explicit"
    elif key in clue_index:
        words = {s: list(clue_index[key]["words"].get(s, [])) for s in steps}
        words = tweak_combined(cat_id, qtext, words, steps)
        logic = topic_logic(cat_id, topic_en, qtext)
        source = "clue"
    else:
        alias = CLUE_ALIAS.get(key)
        if alias and alias in clue_index:
            words = {s: list(clue_index[alias]["words"].get(s, [])) for s in steps}
            words = tweak_combined(cat_id, qtext, words, steps)
            logic = topic_logic(cat_id, topic_en, qtext)
            source = "clue-alias"
        else:
            tpl = topic_template_words(cat_id, topic_en, qtext)
            if tpl:
                words = pack(cat_id, *tpl)
                words = {steps[i]: words[steps[i]] for i in range(4)}
            logic = topic_logic(cat_id, topic_en, qtext)
            source = "derived"

    for s in steps:
        words[s] = enrich_step_words(words.get(s, []), cat_id, topic_en, s, steps)
        words[s] = apply_fixes(words[s])

    return {"logic": logic, "words": words, "source": source}


def main() -> None:
    heat = json.loads(HEAT.read_text(encoding="utf-8"))
    clue_index = json.loads(CLUE.read_text(encoding="utf-8"))["index"]
    build_hand_banks()

    out: dict[str, dict] = {}
    stats: dict[str, int] = {}
    for cat in heat:
        steps = cat["steps"]
        for topic in cat["topics"]:
            for qtext in topic["questions"]:
                r = resolve_one(cat["id"], topic["topicEn"], qtext, steps, clue_index)
                out[norm_q(qtext)] = {
                    "cat": cat["id"],
                    "topicEn": topic["topicEn"],
                    "q": qtext,
                    "logic": r["logic"],
                    "words": r["words"],
                    "source": r["source"],
                }
                stats[r["source"]] = stats.get(r["source"], 0) + 1

    OUT.write_text(json.dumps({"questions": out, "stats": stats, "fixes_count": len(FIXES)}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} stats={stats}")


if __name__ == "__main__":
    main()
