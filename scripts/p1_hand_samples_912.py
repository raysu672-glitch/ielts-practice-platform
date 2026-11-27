# -*- coding: utf-8 -*-
"""Hand samples for 2026 9-12 season questions that templates still mishandle."""
from __future__ import annotations

from p1_word_banks_core import norm_q

HAND_912: dict[str, str] = {}


def _h(q: str, a: str) -> None:
    HAND_912[norm_q(q)] = " ".join(a.split())


def build() -> dict[str, str]:
    # Shoes
    _h(
        "What kind of shoes did you wear as a child?",
        "As a child I mostly wore simple school shoes. "
        "My parents bought a new pair before each term, and I used them every weekday. "
        "They were plain but sturdy, and I find that childhood memory quite clear even now.",
    )
    # Websites
    _h(
        "What makes a website easy to use?",
        "A clear layout and fast search make a website easy to use. "
        "I like pages where I can find study resources in a few clicks without messy ads. "
        "I find simple navigation really practical for everyday homework and reading.",
    )
    _h(
        "Would you like to have your own website?",
        "Maybe later. I might build a simple site to share study notes or a personal blog after I graduate. "
        "For now I just use other websites every day, so having my own is not urgent. "
        "I find the idea interesting but not necessary for my current routine yet.",
    )
    # Headphones / music
    _h(
        "Do you use headphones?",
        "Yes, almost every day. I use wireless earbuds on the subway to listen to music and block noise. "
        "They are convenient before class and when I want a short break between tasks. "
        "I find them really practical, though long use can feel a bit uncomfortable.",
    )
    _h(
        "Do you listen to music while doing other things?",
        "Yes, often. I listen to soft music while studying or walking, which helps me focus without getting bored. "
        "I usually do this every weekday with headphones on the way to campus. "
        "I find it useful for relieving stress and keeping a steady pace.",
    )
    _h(
        "What kind of music do you like?",
        "I like light pop and some soft instrumental tracks for different parts of the day. "
        "Happy songs cheer me up after class, while quieter music helps when I study at night. "
        "I find this mix practical for switching between focus and rest.",
    )
    _h(
        "Which do you prefer, big headphones or small earbuds?",
        "I'd rather use small earbuds. As for earbuds, they are light and easy to carry on the subway. "
        "By contrast, big headphones feel warmer and block more noise, but they are less convenient. "
        "Overall I find earbuds more suitable for daily commuting and short study breaks.",
    )
    # Tidiness
    _h(
        "Who kept your room tidy when you were a child?",
        "My mum mostly kept my room tidy when I was a child. "
        "She asked me to put toys away, but she still did the deep cleaning every weekend. "
        "I find that habit made me care more about a clear desk later at university.",
    )
    _h(
        "Do you like to keep things tidy?",
        "Yes, I do. I try to keep my study desk tidy before I start homework every evening. "
        "A clear desk helps me focus and reduces small conflicts with roommates in the dorm. "
        "I find tidiness practical for study rather than aiming for a perfect room.",
    )
    _h(
        "Do you think that it is necessary to be tidy?",
        "Yes, to a point. Being tidy saves time when I look for notes, chargers or clothes. "
        "In shared spaces it also shows respect for roommates and keeps arguments down. "
        "I find basic tidiness necessary, though I do not need everything to look perfect.",
    )
    # Singing
    _h(
        "What songs did you sing when you were a child?",
        "As a child I sang simple children's songs and classroom songs in music class. "
        "Sometimes I sang with friends at home for fun after homework was finished. "
        "I find those songs warm to remember, even if I forget some of the lyrics now.",
    )
    _h(
        "Do you like singing?",
        "Yes, I do. I am keen on singing at KTV with friends at weekends because it always cheers me up. "
        "I do not sing every day, but a few songs after exams help me relax and laugh. "
        "I find it enjoyable and a good way to relieve stress after a busy week.",
    )
    _h(
        "Do you think singing can bring happiness to people?",
        "Yes, I think so. Singing together can light up the mood and help people share a good laugh. "
        "Even singing alone with headphones can reduce stress after a long day of classes. "
        "I find it a simple and positive way to feel better without spending much money.",
    )
    # Science / space
    _h(
        "Which area of science interests you the most?",
        "Biology and space science interest me the most among school subjects. "
        "I like simple experiments at school and documentaries about the universe at night. "
        "I find these areas curious and useful for understanding daily life and nature.",
    )
    _h(
        "Did you like science at school?",
        "Yes, especially when we did experiments in science class. "
        "I liked biology more than pure theory, because the lab work felt concrete and clear. "
        "I find those lessons still make me curious about science videos and short docs now.",
    )
    _h(
        "What science programmes or videos do you enjoy?",
        "I enjoy short science videos and space documentaries on my phone. "
        "I watch them a few nights a week before I go to sleep when I want a soft break. "
        "I find them interesting and less stressful than scrolling random social media clips.",
    )
    _h(
        "What did you learn about space when you were a child?",
        "As a child I learned basic facts about planets and stars from school and TV. "
        "I remember documentaries about the moon and the solar system after dinner. "
        "I find that early curiosity still makes me watch space videos from time to time.",
    )
    _h(
        "Have you ever learnt about outer space and stars?",
        "Yes, I have. I learned about stars and planets at school and later through documentaries. "
        "I still watch space programmes from time to time when I want a calm evening. "
        "I find the topic exciting even though I am not an expert in astronomy.",
    )
    _h(
        "Do you like looking at the stars?",
        "Yes, when the sky is clear. In my city I cannot see many stars, so I enjoy them more during trips. "
        "Sometimes I watch space documentaries instead on quiet nights. "
        "I find looking at the real night sky calming and a bit magical.",
    )
    _h(
        "What would you most like to know about outer space?",
        "I would most like to know whether humans can travel farther safely and what other planets are like. "
        "Documentaries make me curious about real discoveries, not only science fiction stories. "
        "I find these questions exciting for the future and for how science may change daily life.",
    )
    _h(
        "How often can you see stars where you live?",
        "Not very often. City lights make it hard to see stars on normal weeknights. "
        "I only see a clear sky when I travel to quieter places outside the city. "
        "I find that a bit disappointing, so I watch space documentaries instead.",
    )
    # Name
    _h(
        "Who chose your name?",
        "My parents chose my name when I was born. "
        "They picked it for a simple meaning and because it was easy for relatives to call. "
        "I find their choice natural, and I am completely used to it now.",
    )
    _h(
        "What did your friends call you when you were a child?",
        "My friends mostly used my given name, and sometimes a short nickname at school. "
        "It was nothing fancy, just easier to shout across the playground after class. "
        "I find those nicknames warm when I look back on childhood friendships.",
    )
    # Rubbish
    _h(
        "What kinds of things do you throw away most often?",
        "I mostly throw away food packaging, paper tissues and empty bottles after meals. "
        "In the dorm we sort paper and plastic into recycling bins every day. "
        "I find sorting small rubbish responsible and easy to keep up as a habit.",
    )
    # Home
    _h(
        "Who do you live with?",
        "I live in campus dorms with my roommate during term time. "
        "In the holidays I go back and live with my parents in our family home. "
        "I find both arrangements practical for study focus and for family time.",
    )
    _h(
        "Which room in your home do you like best?",
        "I like the living room best, or my desk corner when I need to study quietly. "
        "The living room feels loose and comfortable after classes with soft light. "
        "I find a bright, tidy space really helpful for both rest and homework.",
    )
    # Fruit / parks / clothing
    _h(
        "Which vegetables did you dislike as a child?",
        "As a child I disliked bitter vegetables like bitter melon and a few leafy greens. "
        "I preferred fruit and milder vegetables, and my parents had to persuade me at dinner. "
        "I find my taste better now, though I still avoid a couple of bitter ones.",
    )
    _h(
        "What did you do in parks when you were a child?",
        "As a child I played outside in parks with my parents and friends after school. "
        "We ran around, flew a kite sometimes, and bought small snacks near the entrance. "
        "I find those park memories warm, simple and still easy to picture.",
    )
    _h(
        "Did you like going to parks as a child?",
        "Yes, I loved it. Parks meant fresh air and playing outside after school with friends. "
        "I went with my parents at weekends when the weather was good enough for a walk. "
        "I find those trips still make me want short evening walks in green spaces now.",
    )
    _h(
        "Who chose your clothes when you were a child?",
        "My parents chose my clothes when I was a child for school and weekends. "
        "They bought simple t-shirts and coats, and I rarely decided the style by myself. "
        "I find that normal then, though I choose my own clothes carefully now.",
    )
    _h(
        "Do you spend a lot of time choosing clothes?",
        "Not really. I usually pick a simple t-shirt or sweatshirt and a coat if it is cold. "
        "Comfort comes first on campus, so I do not spend long in front of the wardrobe. "
        "I find quick clothing choices more practical on busy weekdays.",
    )
    _h(
        "Do you like wearing T-shirts?",
        "Yes, I do. A simple t-shirt feels loose and comfortable for everyday campus life. "
        "I wear one almost every weekday under a coat or sweatshirt when it turns cool. "
        "I find T-shirts easy to wash and hard to get wrong for casual days.",
    )
    _h(
        "What kind of clothes do you usually wear?",
        "I usually wear casual campus clothes — a t-shirt, sweatshirt and a coat when it is cool. "
        "Comfort matters more than style on weekdays when I move between classes. "
        "I find this look practical and quick to get dressed in the morning.",
    )
    # Shopping
    _h(
        "What was the last thing you bought?",
        "The last thing I bought was a pair of wireless earbuds from an online shop. "
        "I ordered them at the weekend after comparing a few stores on my phone. "
        "I find online shopping convenient for small daily items like that.",
    )
    _h(
        "Who did you go shopping with when you were a child?",
        "I usually went shopping with my parents when I was a child. "
        "Sometimes my mum took me to a mall or a street market at weekends for clothes. "
        "I find those trips memorable because I rarely went to shops alone then.",
    )
    _h(
        "Do you enjoy shopping?",
        "Yes, sometimes. I enjoy short trips to malls or street markets with friends at weekends. "
        "I shop online more often for small things because it is faster after class. "
        "I find shopping fun in moderation, not as something I need every day.",
    )
    _h(
        "Do you like shopping?",
        "Yes, in moderation. I like browsing shops at weekends and paying quickly by phone. "
        "For daily needs I prefer online shopping because it saves time between classes. "
        "I find both ways useful depending on whether I need to try something on.",
    )
    # Ads / area / social
    _h(
        "Which advert do you remember from your childhood?",
        "I remember a food advert on TV with a catchy song from my childhood evenings. "
        "It played often after dinner programmes, so the tune stuck in my head for years. "
        "I find childhood ads strangely memorable even when the product itself is gone.",
    )
    _h(
        "What kind of adverts do you enjoy watching?",
        "I enjoy short, funny adverts more than long hard-sell ones on my phone. "
        "On the subway screens I notice creative clips, but I skip noisy ads while studying. "
        "I find light humour more enjoyable than aggressive marketing that repeats too much.",
    )
    _h(
        "What facilities are there near where you live?",
        "Near where I live there are convenience stores, a subway station and a small park. "
        "I can walk to most daily facilities in about ten minutes from my dorm area. "
        "I find the neighbourhood practical for student life and quick errands.",
    )
    _h(
        "What would you improve about your area if you could?",
        "I would add more recycling bins and quieter walking paths near the main road. "
        "The area is convenient, but some streets feel crowded and noisy in rush hour. "
        "I find small public improvements would make daily commuting more comfortable.",
    )
    _h(
        "What is the area where you live like?",
        "The area where I live is a residential area with shops nearby and fairly good transport links. "
        "It can be a bit noisy in rush hour, but evenings are usually fine for a walk. "
        "I find it practical for studying on campus and getting around the city.",
    )
    _h(
        "Which social media apps do you use most?",
        "I use WeChat and Xiaohongshu the most for daily campus life. "
        "WeChat is for chatting and group notices, while Xiaohongshu is for short tips and videos. "
        "I find both social media apps practical, though I try not to scroll too late.",
    )
    _h(
        "What do people often do on social media?",
        "People often chat, browse short videos and share posts with friends on social media. "
        "Students also use group chats for class notices, homework and weekend plans. "
        "I find these apps useful for contact, though they are easy to overuse at night.",
    )
    _h(
        "Do you think you spend too much time on social media?",
        "Sometimes yes. I can scroll short videos on social media longer than I planned at night. "
        "I try to set limits before sleep so it does not affect the next study day. "
        "I find awareness helps, but the habit is still hard to cut completely.",
    )
    # Cars / paper / politeness / tiredness / jokes / hometown / city / travel / mirrors
    _h(
        "What do you remember about car journeys as a child?",
        "I remember family road trips by car during the holidays when I was a child. "
        "I sat by the window, felt relaxed, and watched the scenery change outside. "
        "I find those car journeys warm and less stressful than adult travel for work.",
    )
    _h(
        "What kind of car would you like to own?",
        "I would like a practical small car that is easy to park and not too expensive. "
        "Comfort and safety matter more to me than a luxury brand or flashy design. "
        "I find that plan realistic after I start working and need weekend trips.",
    )
    _h(
        "What did you use paper for most when you were at school?",
        "At school I used paper mostly for handwritten notes and worksheets in class. "
        "I also flipped through real books after class instead of only looking at screens. "
        "I find paper notes still help memory better for some subjects even now.",
    )
    _h(
        "What do you do with paper you no longer need?",
        "I recycle it when I can. In the dorm we put used paper into the recycling bins on each floor. "
        "For private notes I tear them before throwing them away carefully. "
        "I find recycling paper a small but responsible habit that is easy to keep.",
    )
    _h(
        "What did you like to do with paper as a child?",
        "As a child I liked drawing and folding paper into simple shapes after school. "
        "Sometimes I made cards for family on festivals with coloured paper at home. "
        "I find those paper crafts more fun than I expected when I look back now.",
    )
    _h(
        "Who taught you to be polite when you were a child?",
        "My parents taught me to be polite when I was a child at home and in shops. "
        "They corrected me whenever I forgot to say thank you or please in public. "
        "I find those small manners still automatic when I speak to strangers now.",
    )
    _h(
        "What kind of behaviour do you find rude?",
        "I find interrupting others and not saying thank you quite rude in daily life. "
        "Pushing in lines or speaking loudly on the phone in quiet places also bothers me. "
        "I think basic respect and polite manners make everyday interactions much smoother.",
    )
    _h(
        "What used to make you tired when you were a child?",
        "Long school days and too much homework used to make me tired as a child. "
        "After evening classes I just wanted to rest, take a short walk or sleep early. "
        "I find that tired feeling similar to exam weeks at university now.",
    )
    _h(
        "What do you usually do when you feel tired?",
        "When I feel tired, I usually take a short walk or rest with soft music. "
        "After a long day of classes, ten or fifteen minutes is enough to slow down and recover. "
        "I find this more effective for relieving tiredness than scrolling on my phone.",
    )
    _h(
        "Who is the funniest person you know?",
        "My roommate is the funniest person I know in daily campus life. "
        "He tells light jokes and shares funny clips that make everyone laugh after study. "
        "I find his humour a real stress buster in the dorm when we all feel tired.",
    )
    _h(
        "What made you laugh when you were a child?",
        "As a child I laughed at simple jokes, cartoons and classmates' funny stories. "
        "I did not need sophisticated comedy — silly playground moments were enough. "
        "I find those laughs honest and easy to remember when I think about school days.",
    )
    _h(
        "Do you like telling jokes?",
        "Sometimes. I am not a professional joke-teller, but I share light jokes with friends. "
        "I prefer funny daily stories more than staged punchlines that feel forced. "
        "I find humour useful when everyone feels tired after a long week of classes.",
    )
    _h(
        "What kind of comedy do you enjoy?",
        "I enjoy light comedies and short funny clips more than noisy stand-up shows. "
        "Watching comedies with friends at weekends always cheers me up after exams. "
        "I find gentle humour better for relaxing than comedy that feels too aggressive.",
    )
    _h(
        "What is your hometown best known for?",
        "My hometown is best known for local street food and a few traditional snacks. "
        "People also mention its small-city pace and nearby parks for evening walks. "
        "I find the food the first thing I introduce when friends ask about my town.",
    )
    _h(
        "Which city do you live in now?",
        "I live in a fairly large city for university now during term time. "
        "It has a subway, busy streets and more study resources than my hometown. "
        "I find city life convenient for classes, though it can feel a bit crowded.",
    )
    _h(
        "What is the best way to get around your city?",
        "The subway is usually the best way to get around in my city on weekdays. "
        "It is more reliable than buses in rush hour, and I walk short distances after getting off. "
        "I find public transport practical for daily commuting between dorm and campus.",
    )
    _h(
        "What kind of places do you like to visit?",
        "I like quiet places with nature, and sometimes coastal towns when I can travel. "
        "I also enjoy city parks when I cannot go far during a busy study week. "
        "I find these places better for relaxing than crowded shopping malls.",
    )
    _h(
        "Do you like having lots of mirrors at home?",
        "Not lots. One full-length mirror and a small hallway mirror are enough at home. "
        "Too many mirrors make a small room feel busy and a little distracting. "
        "I find a simple mirror setup more practical for getting dressed each morning.",
    )
    _h(
        "Do you like looking at yourself in the mirror?",
        "Just for a quick check. Before I head out I look at myself in the mirror to make sure I look neat. "
        "I do not spend long on it because mornings are already busy. "
        "I find a short mirror check practical every morning before class.",
    )
    _h(
        "Why do people today seem to get bored more easily?",
        "I think it is because phones give endless short videos, so people get bored when nothing new appears. "
        "Since attention jumps quickly online, quiet moments feel empty compared with constant scrolling. "
        "I find that pattern common among students, including myself after long study days.",
    )
    _h(
        "How do you find out about new opportunities?",
        "I mostly find out about new opportunities through teachers, classmates and campus notices. "
        "I also check WeChat groups and internship posts on study websites every week. "
        "I find these channels practical when I look for part-time work or project chances.",
    )
    _h(
        "Why do some people miss good opportunities?",
        "Some people miss good opportunities because they hesitate too long or do not prepare early. "
        "Since information spreads fast, waiting for a perfect moment can mean the chance is gone. "
        "I find staying curious and applying a bit earlier helps more than overthinking.",
    )
    _h(
        "Why do some shops and restaurants have so many mirrors?",
        "I think shops and restaurants use many mirrors because mirrors make rooms look bigger and brighter. "
        "Since mirrors also let people check their look while shopping or waiting, they feel more comfortable. "
        "I find the design practical for business, though too many mirrors can feel a bit flashy.",
    )
    _h(
        "What kind of clothes do you like to wear?",
        "I like to wear casual campus clothes, especially a simple t-shirt with jeans or a sweatshirt. "
        "Comfort comes first on weekdays when I move between classes and the library. "
        "I find this style practical, easy to wash, and hard to get wrong for student life.",
    )
    return HAND_912


build()
