# -*- coding: utf-8 -*-
"""Extra hand samples for leftover template dumps / Q-mismatches."""
from __future__ import annotations

from p1_word_banks_core import norm_q

HAND_FIX: dict[str, str] = {}


def _h(q: str, a: str) -> None:
    HAND_FIX[norm_q(q)] = " ".join(a.split())


def build() -> dict[str, str]:
    # Science daily-life samples are curated in p1_freestyle_packs.py (per kit)
    _h(
        "When did you start to learn about science?",
        "I started to learn about science in primary school. "
        "We had simple science lessons and a few experiments that made the subject feel concrete. "
        "Later in secondary school I learned more biology and watched short science videos. "
        "I find that early start still keeps me curious about how things work.",
    )
    _h(
        "How does tiredness affect your work or studies?",
        "Tiredness mainly hurts my focus when I study or finish assignments. "
        "When I am exhausted, I read more slowly and make more small mistakes in class notes. "
        "That is why I try to rest early before busy study days. "
        "I find managing tiredness important for keeping my work quality steady.",
    )
    _h(
        "When did you get your first pair of headphones?",
        "I got my first pair of headphones in secondary school as a birthday gift. "
        "They were simple wired ones, and I used them to listen to music on the way to school. "
        "Later I switched to wireless earbuds for commuting. "
        "I find that first pair started my habit of listening with headphones every day.",
    )
    _h(
        "Are you a tidy person?",
        "Yes, fairly tidy. I keep my study desk clear before homework and put clothes away after washing. "
        "I am not perfect, but a tidy room helps me focus and reduces small arguments in the dorm. "
        "I find basic tidiness practical for student life.",
    )
    _h(
        "Do you use headphones?",
        "Yes, almost every day. I use headphones — usually wireless earbuds — on the subway to listen to music. "
        "They help me block noise before class and during short breaks between lectures. "
        "I find headphones really convenient for commuting and quiet study focus.",
    )
    _h(
        "Does your name have a special meaning?",
        "Yes, it has a simple positive meaning that my parents liked. "
        "They chose the name because it sounded clear and was easy for relatives to remember. "
        "I do not think about the meaning every day, but I appreciate their choice. "
        "I find it natural and easy to live with.",
    )
    _h(
        "Do you often forget people's names?",
        "Sometimes, yes. If I meet many new classmates at once, I may forget a name after one chat. "
        "I usually repeat the name quietly or check WeChat later to remember it. "
        "With people I see every week I rarely forget. "
        "I find name memory improves when I use the name in conversation.",
    )
    _h(
        "Do you recycle at home?",
        "Yes, we do. At home and in the dorm we sort paper, plastic bottles and food waste into different bins. "
        "It only takes a few seconds after meals, so the habit is easy to keep. "
        "I find recycling a small but responsible part of daily life.",
    )
    _h(
        "Do you often feel bored?",
        "Not often during term time, because classes and assignments keep me busy. "
        "I feel bored more on quiet Sunday evenings when I have finished my tasks. "
        "Then I usually take a short walk or watch light videos. "
        "I find a little boredom normal, but I try not to scroll for too long.",
    )
    _h(
        "Do people often grow vegetables by themselves?",
        "Some people do, especially older relatives with a small garden or balcony. "
        "In cities most young people buy vegetables from markets or apps instead. "
        "Growing your own takes time and space that students usually do not have. "
        "I find home-grown vegetables nice, but buying fresh ones is more practical for me.",
    )
    _h(
        "Is there a park near your home?",
        "Yes, there is a small park about ten minutes' walk from where I live. "
        "I go there for fresh air after study, especially in the evening. "
        "It is not huge, but it has paths and a few trees. "
        "I find that nearby park really convenient for a short break.",
    )
    _h(
        "Do you prefer sitting by the window when you travel?",
        "Yes, I prefer the window seat when I travel by train or coach. "
        "I like watching the scenery change, and it helps the journey feel shorter. "
        "On short subway rides I do not mind so much. "
        "I find a window seat more relaxing on longer trips.",
    )
    _h(
        "Did you learn to play an instrument as a child?",
        "No, not seriously. I had a few music lessons at school, but I never practised an instrument for long. "
        "I mostly sang simple songs in class and listened to music at home. "
        "I sometimes wish I had learned the piano, but it is not a big regret. "
        "I find listening to music enough for me now.",
    )
    _h(
        "Do you have a car?",
        "No, I do not have a car now. As a student I use the subway and walk for short trips. "
        "My parents have a family car for holidays and weekend visits. "
        "I may buy a small practical car after I start working. "
        "I find public transport enough for daily campus life.",
    )
    _h(
        "Do you still keep in touch with your classmates from secondary school?",
        "Yes, with a few close ones. We chat on WeChat and meet when we are all back home. "
        "I am not in touch with the whole class, only friends I studied with most. "
        "A short message during holidays is usually enough. "
        "I find those friendships warm even if we talk less during term time.",
    )
    _h(
        "Is there anything you miss about your secondary school?",
        "Yes, I miss the simple routine and seeing the same classmates every day. "
        "Secondary school felt busy but familiar, with clubs and short breaks between classes. "
        "University is freer, but sometimes lonelier. "
        "I find those school memories warm when I look back.",
    )
    _h(
        "Do you often get tired?",
        "Yes, especially during exam weeks. Long classes and late homework make me feel tired by evening. "
        "On normal days I feel better if I sleep on time and take a short walk. "
        "I try not to scroll on my phone when I am already exhausted. "
        "I find early rest the simplest way to handle tiredness.",
    )
    _h(
        "Are you good at telling jokes?",
        "Not really. I can share light funny stories with friends, but I often forget the punchline. "
        "I am better at laughing at other people's jokes than inventing my own. "
        "In the dorm we mostly watch short comedy clips together. "
        "I find humour useful even if I am not a great joke-teller.",
    )
    _h(
        "When was the last time you went to a street market?",
        "The last time was during the holiday when I went home. "
        "I walked through a local street market with my parents for breakfast snacks and fruit. "
        "It felt noisy but lively, and cheaper than a big supermarket. "
        "I find street markets fun for short visits, not for weekly shopping.",
    )
    _h(
        "Are there many street markets in your country?",
        "Yes, there are still many street markets in my country, especially near residential areas. "
        "People go for fresh food, snacks and small daily goods. "
        "In big cities some markets are smaller than before, but they have not disappeared. "
        "I find them a practical part of everyday local life.",
    )
    _h(
        "Are there many street markets in China?",
        "Yes, China still has many street markets in towns and city neighbourhoods. "
        "People buy vegetables, fruit and breakfast food there, often early in the morning. "
        "Some traditional markets sit next to modern shops and subway stations. "
        "I find them convenient when I want fresh food quickly.",
    )
    _h(
        "How often do you buy new shoes?",
        "Not very often. I usually buy a new pair of sneakers once a year, or when the old ones wear out. "
        "Comfort matters more than fashion, so I do not chase every new style. "
        "I sometimes check online shops before I decide. "
        "I find buying shoes only when needed more practical for a student budget.",
    )
    _h(
        "How often do you use headphones?",
        "Almost every day. I use wireless earbuds on the subway and sometimes while studying. "
        "They help me listen to music and block noisy surroundings. "
        "I try not to wear them for too many hours in a row. "
        "I find headphones a daily tool rather than just a weekend gadget.",
    )
    _h(
        "How often do you tidy your room?",
        "I do a quick tidy every couple of days, and a deeper clean at the weekend. "
        "I clear my study desk before homework and put clothes away after washing. "
        "In a shared dorm, regular tidying also keeps conflicts down. "
        "I find this rhythm easy to keep without becoming obsessive.",
    )
    _h(
        "When do you usually sing?",
        "I usually sing at KTV with friends at weekends, not every day. "
        "Sometimes I sing quietly along with headphones when I am in a good mood. "
        "After exams it feels especially relaxing. "
        "I find singing a social activity more than a daily habit.",
    )
    _h(
        "When do you usually feel bored?",
        "I usually feel bored on quiet evenings after I finish homework and have nothing planned. "
        "Long waits on the subway can feel boring too if I forget my headphones. "
        "Then I take a short walk or watch a light video. "
        "I find boredom comes more from empty time than from hard study itself.",
    )
    _h(
        "How often do you eat vegetables?",
        "Almost every day. I eat vegetables at lunch in the canteen and often with dinner. "
        "I try to keep a mix of greens and some fruit during the week. "
        "When I am busy I may eat simpler dishes, but I still include vegetables. "
        "I find this habit practical for energy and everyday health.",
    )
    _h(
        "How often do you go to parks?",
        "About two or three times a week when the weather is fine. "
        "I usually go for a short evening walk after study to get fresh air. "
        "At weekends I may stay longer if I go with friends. "
        "I find nearby parks an easy way to reset without travelling far.",
    )
    _h(
        "How often do you go shopping?",
        "I go shopping maybe once or twice a week, mostly for small daily needs. "
        "Bigger mall trips are more for weekends with friends. "
        "For clothes or earbuds I often shop online instead. "
        "I find a mix of short local shopping and online orders most convenient.",
    )
    _h(
        "Do you usually take an opportunity when it comes along?",
        "Usually yes, if the opportunity fits my study plan and I am prepared enough. "
        "I check internship or campus notices carefully before I say yes. "
        "I do not jump at every chance, but I try not to hesitate too long either. "
        "I find a quick, realistic decision better than waiting for a perfect moment.",
    )
    _h(
        "Would you like to live in your hometown in the future?",
        "Maybe for a while. I would like to live in my hometown after graduation for family time. "
        "But for work or further study in the future I may need to stay in a bigger city. "
        "I find both options possible, depending on the job I get.",
    )
    _h(
        "Where would you take a friend who was visiting your city?",
        "I would take a friend to a nearby park first, then to a street market for local snacks. "
        "If we have more time, we might visit a museum or walk around the old campus area. "
        "I find those places more welcoming for a short city visit than only shopping malls.",
    )
    _h(
        "Where would you most like to travel in the future?",
        "I would most like to travel to a quieter coastal town or a mountain area in the future. "
        "I want fresh air and a slower pace after busy exam weeks in the city. "
        "I find nature trips more relaxing than only big shopping destinations.",
    )
    _h(
        "How often do you travel?",
        "Not very often during term time. I usually travel back home in the holidays, and sometimes take a short city trip. "
        "Long trips need time and money, so I plan them carefully. "
        "With friends I prefer nearby places first. "
        "I find a few well-planned trips more enjoyable than constant travelling.",
    )
    _h(
        "When do you usually listen to music?",
        "I usually listen to music on the subway and while walking between classes. "
        "In the evening I may play soft tracks when I want a break from study. "
        "I rarely listen during serious reading because it distracts me. "
        "I find music most useful for commuting and short rest moments.",
    )
    _h(
        "How do you usually discover new music?",
        "I usually discover new music through short videos and friends' playlists. "
        "Sometimes a song in a cafe or on the subway catches my ear, and I search for it later. "
        "I also follow a few artists I already like. "
        "I find recommendations from people I know more reliable than random charts.",
    )
    _h(
        "How do you usually get around your city?",
        "I usually take the subway and walk the last few minutes. "
        "For short distances near campus I just walk, and I rarely take taxis. "
        "Buses are a backup when the subway is too crowded. "
        "I find public transport the most practical way around my city.",
    )
    _h(
        "How often do you use paper in your daily life?",
        "I still use paper every weekday for handwritten notes and worksheets. "
        "I also print a few pages when I revise for exams, though much reading is on screens. "
        "After class I recycle paper I no longer need. "
        "I find paper useful for memory, even in a mostly digital daily life.",
    )
    _h(
        "How did you usually spend your breaks at school?",
        "At secondary school I usually spent breaks chatting with classmates or walking in the corridor. "
        "Sometimes we bought a snack, and on longer breaks we played simple games outside. "
        "I rarely stayed alone at my desk the whole time. "
        "I find those short breaks were important for resetting before the next class.",
    )
    _h(
        "When do you usually feel tired?",
        "I usually feel tired in the late evening after a full day of classes and homework. "
        "Exam weeks are worse because I sleep less and keep reviewing. "
        "After lunch I sometimes feel a short dip as well. "
        "I find an early night and a short walk the simplest ways to recover.",
    )
    _h(
        "What do people in your hometown usually do at the weekend?",
        "At the weekend people in my hometown often visit local food stalls and nearby parks. "
        "Families go shopping together, and young people meet friends in cafes or small plazas. "
        "The pace feels slower than in big cities. "
        "I find weekend life there simple, social and focused on local food.",
    )
    _h(
        "What do people usually buy on the street market?",
        "People usually buy fresh vegetables, fruit, breakfast snacks and small household goods. "
        "Some stalls also sell local street food that is hard to find in big malls. "
        "Shoppers often go early for better prices and fresher produce. "
        "I find street markets practical for everyday food shopping.",
    )
    _h(
        "How often do you look in the mirror each day?",
        "I look in the mirror a few times a day, mostly for a quick check. "
        "In the morning I make sure I look neat before class, and sometimes again before I go out. "
        "I do not spend long staring at myself. "
        "I find a short mirror check practical rather than a habit I overdo.",
    )
    _h(
        "How do you feel about your name?",
        "I feel fine about my name. It is simple, easy to say, and I am used to it. "
        "My parents chose it for a clear meaning, so I do not wish for a different one. "
        "Sometimes friends use a short nickname, but I still like my real name. "
        "I find it natural and comfortable in daily life.",
    )
    _h(
        "How do you think social media will change in the future?",
        "I think social media will become more video-based and more personalised. "
        "Apps like WeChat and short-video platforms may add clearer study or work tools, not only entertainment. "
        "At the same time, people may care more about privacy and screen-time limits. "
        "I find the direction convenient, but users will still need self-control.",
    )
    _h(
        "How do you think cars will change in the future?",
        "I think cars will become cleaner and more connected, with more electric models in cities. "
        "Navigation and safety systems should get smarter, so daily driving feels less stressful. "
        "Owning a car may still be expensive, so shared options could grow as well. "
        "I find that future practical if public transport stays strong too.",
    )
    _h(
        "How do you think our use of paper will change in the future?",
        "I think we will use less paper for everyday printing, because screens are already common. "
        "But handwritten notes and some books will not disappear completely for study. "
        "Recycling should also become more automatic in schools and offices. "
        "I find a mixed future likely: less waste paper, but paper still useful for memory.",
    )
    _h(
        "Where did you go on holiday when you were a child?",
        "As a child I usually went to nearby towns or a coastal city with my parents in the summer. "
        "We stayed with relatives sometimes, or visited parks and small local markets. "
        "I find those childhood holidays warm, simple and easy to remember.",
    )
    _h(
        "What kind of home would you like to have in the future?",
        "I would like a bright apartment with a quiet study corner and a small living room. "
        "It does not need to be huge, but it should feel tidy and comfortable after work. "
        "I find a practical home more important than a luxury one.",
    )
    _h(
        "What kind of opportunity would you like to have in the next few years?",
        "I would like an internship related to my major, or a short exchange programme if possible. "
        "Those chances would help me test real work skills before graduation. "
        "I find practical opportunities more useful than only classroom experience.",
    )
    _h(
        "What do you like most about your neighbourhood?",
        "I like that shops, a subway station and a small park are all within a short walk. "
        "It is convenient for daily errands and for a quick evening stroll after study. "
        "I find the neighbourhood practical for student life, even if it can be noisy in rush hour.",
    )
    _h(
        "Why did you choose that job or that subject?",
        "I chose my subject because it matches my strengths and leads to clearer career options. "
        "I also like the practical courses and group projects we do every weekday. "
        "I find the choice useful for both study now and work later.",
    )
    return HAND_FIX


build()
