# -*- coding: utf-8 -*-
"""Kit-specific hand samples: same question, different material → different answer."""
from __future__ import annotations

from p1_word_banks_core import norm_q

HAND_KIT: dict[tuple[str, str], str] = {}


def _hk(q: str, kit: str, a: str) -> None:
    HAND_KIT[(norm_q(q), kit)] = " ".join(a.split())


def build() -> dict[tuple[str, str], str]:
    # Feeling bored — skill demo: short videos vs yellow bike park ride
    _hk(
        "Do you often feel bored?",
        "douyin_scroll_habit",
        "Not really, to be honest. After a long day I usually watch short videos or hang out with my friends, "
        "so I don't get bored easily. I do this most evenings, or at weekends if we have time. "
        "It helps me switch off and feel more relaxed.",
    )
    _hk(
        "Do you often feel bored?",
        "yellow_bike_gift",
        "Sometimes I feel bored, especially during the week when I've been sitting in class all day. "
        "When that happens, I like to take my bike to the park and go for a ride. "
        "I usually do that at weekends, for about an hour. "
        "It gives me something to do, and it also helps me unwind.",
    )
    _hk(
        "Do you often feel bored?",
        "nearby_park_walk",
        "Not often. When I feel a bit bored after study, I take a short walk in a nearby park. "
        "Fresh air and a simple route help me reset without scrolling for too long. "
        "I usually go most evenings when the weather is fine. "
        "I find that walk practical and calming.",
    )
    # Opportunities — childhood bike vs campus notices
    _hk(
        "Did you have any opportunities to take part in new activities as a child?",
        "yellow_bike_gift",
        "Yes, I did. When I was in junior high, my mum bought me a small yellow bike as a birthday gift, "
        "and that was the first time I really started cycling on my own. "
        "I rode it to school every day after that, even when the weather wasn't great. "
        "It was a new kind of freedom for me, and I found it really convenient.",
    )
    _hk(
        "Did you have any opportunities to take part in new activities as a child?",
        "campus_opportunity_notice",
        "Yes, a few. Teachers sometimes invited us to join clubs or short holiday programmes. "
        "I heard about them through class notices and classmates, then asked my parents. "
        "Those chances felt small but new for me at the time. "
        "I find that early habit of saying yes still helps now.",
    )
    # Secondary school first day — bike story
    _hk(
        "Do you remember your first day at secondary school?",
        "yellow_bike_gift",
        "Yes, I remember it quite clearly. That was around the time my mum bought me a small yellow bike "
        "as a birthday gift, and I rode it to school on the first day. "
        "I was a bit nervous in the morning, but I got there early and didn't get stuck in traffic. "
        "It felt like a fresh start, and the bike made me feel a bit more independent.",
    )
    _hk(
        "Do you remember your first day at secondary school?",
        "study_library_classes",
        "Yes, I do. I remember finding my classroom and meeting new classmates for the first time. "
        "The day felt busy with rules, timetables and a quick campus tour. "
        "I was nervous but also curious about the new subjects. "
        "I find that memory clear because everything felt new that morning.",
    )
    # Parks childhood — park walk vs bike
    _hk(
        "Did you like going to parks as a child?",
        "nearby_park_walk",
        "Yes, I really did. There was a park near my home, and it was a nice place to get some fresh air and run around. "
        "I used to go there quite often after school, especially at weekends. "
        "I have good memories of it, and I still like going to parks now for a short walk.",
    )
    _hk(
        "Did you like going to parks as a child?",
        "yellow_bike_gift",
        "Yes, I really did. There was a park near my home, and I often took my yellow bike there. "
        "I used to ride for about an hour at weekends after school. "
        "It felt free and simple, and I still like cycling in parks when I can. "
        "I find those park rides warm to remember.",
    )
    # Tiredness — walk vs bike
    _hk(
        "What do you usually do when you feel tired?",
        "light_sports_walk",
        "When I feel tired, I usually take a short walk or rest with soft music. "
        "After a long day of classes, ten or fifteen minutes is enough to slow down and recover. "
        "I find this more effective for relieving tiredness than scrolling on my phone.",
    )
    _hk(
        "What do you usually do when you feel tired?",
        "yellow_bike_gift",
        "When I feel tired, I sometimes take my bike out for a short ride if I have time. "
        "A gentle cycle in the evening helps me clear my head better than sitting still. "
        "I usually do this at weekends rather than every weekday. "
        "I find it good for both my mood and my body.",
    )
    _hk(
        "Do you have a car?",
        "family_car_passenger",
        "No, I do not have my own car now. My parents have a family car for holidays and weekend trips. "
        "As a student I usually take the subway, and I only ride as a passenger when we travel. "
        "I may buy a small practical car after I start working. "
        "I find public transport enough for daily campus life.",
    )
    _hk(
        "Do you have a car?",
        "subway_bus_commute",
        "No, I do not drive a car. I get around by subway and bus every weekday. "
        "A car would be convenient for trips, but parking and cost are hard for a student. "
        "I walk short distances after getting off the subway. "
        "I find public transport more practical than owning a car right now.",
    )
    _hk(
        "What kind of car would you like to own?",
        "family_car_passenger",
        "I would like a practical small car that is easy to park and not too expensive. "
        "For now I only ride as a passenger in my parents' car on holiday trips. "
        "Comfort and safety matter more to me than a luxury brand. "
        "I find that plan realistic after I start working and need weekend trips.",
    )
    _hk(
        "What kind of car would you like to own?",
        "subway_bus_commute",
        "I would like a small practical car one day, but I do not need one as a student. "
        "I get around by subway every weekday, so owning a car is not urgent yet. "
        "When I buy one later, ease of parking and fuel cost will matter most. "
        "I find public transport enough now, and a simple car enough later.",
    )
    _hk(
        "What do you remember about car journeys as a child?",
        "family_car_passenger",
        "I remember family road trips by car during the holidays when I was a child. "
        "I sat by the window as a passenger, felt relaxed, and watched the scenery change. "
        "I find those car journeys warm and less stressful than adult travel now.",
    )
    _hk(
        "What do you remember about car journeys as a child?",
        "subway_bus_commute",
        "I remember a few family car journeys, though we also used buses for short city trips. "
        "As a child I liked sitting by the window in the car more than crowded buses. "
        "Those holiday drives felt special compared with everyday commuting. "
        "I find the car memories warmer, even if I take the subway most days now.",
    )
    _hk(
        "How do you think cars will change in the future?",
        "family_car_passenger",
        "I think cars will become more electric and easier to park in crowded cities. "
        "Family trips may still use cars, but short city rides might shift to shared options. "
        "Safety features and quieter engines should improve too. "
        "I find that future realistic, especially for people who still need weekend journeys.",
    )
    _hk(
        "How do you think cars will change in the future?",
        "subway_bus_commute",
        "I think cars will change, but subway and bus will still matter for daily commuting. "
        "Future cars may be electric and self-driving, yet students like me may still prefer the subway. "
        "Owning a car might become less necessary in big cities with good transport. "
        "I find a mix of cleaner cars and stronger public transport most likely.",
    )
    _hk(
        "How is your home different from the one you lived in as a child?",
        "dorm_apartment_life",
        "My home now is quite different. As a child I lived in a family apartment with my parents. "
        "By contrast, I now live in a campus dorm with a roommate during term time. "
        "The dorm is smaller and shared, while my childhood home felt quieter and more private. "
        "Overall I find the dorm more practical for study, though less comfortable.",
    )
    _hk(
        "How is your home different from the one you lived in as a child?",
        "tidy_desk_habit",
        "It feels different mainly in daily routine. As a child my mum kept the rooms tidy for me. "
        "By contrast, now I have to keep my own desk and dorm corner tidy every evening. "
        "The space is smaller, so mess shows up faster than in my childhood home. "
        "Overall I find self-managed tidiness more practical, though it takes more effort.",
    )
    # Shoes comfort vs style
    _hk(
        "Which matters more to you in a pair of shoes, comfort or style?",
        "campus_sneakers",
        "Comfort matters more to me. I wear comfortable sneakers on campus every weekday. "
        "Style is nice, but if my feet hurt I cannot focus in class. "
        "By contrast, fancy shoes are only for weekends sometimes. "
        "Overall I prefer comfort for daily life.",
    )
    _hk(
        "Which matters more to you in a pair of shoes, comfort or style?",
        "style_shoes_weekend",
        "Comfort still comes first, but I care a bit more about style at weekends. "
        "On weekdays I choose easy sneakers; at weekends I may pick a nicer pair. "
        "By contrast, pure fashion shoes are hard for long walks. "
        "Overall I prefer comfort, with a little style when I hang out.",
    )
    # Watch — Band 6, kit-differentiated
    _hk(
        "Do you wear a watch?",
        "simple_watch_gift",
        "Yes, almost every day. I wear a simple watch so I can check the time quickly in class. "
        "My parents gave it to me, and it helps me stay on time in the morning. "
        "I find it useful and easy to wear.",
    )
    _hk(
        "Do you wear a watch?",
        "phone_time_check",
        "Not every day. I usually check the time on my phone instead of wearing a watch. "
        "A phone is enough for class and the subway, so I do not always put a watch on. "
        "I find the phone more convenient for me right now.",
    )
    _hk(
        "Have you ever got a watch as a gift?",
        "simple_watch_gift",
        "Yes. My parents gave me a simple watch as a birthday gift last year. "
        "I still wear it when I need to stay punctual for class. "
        "I find that gift practical, not only nice to look at.",
    )
    _hk(
        "Have you ever got a watch as a gift?",
        "phone_time_check",
        "Not really a watch. People usually give me small phone gadgets, and I check time on my phone. "
        "I have not got a real watch as a gift yet. "
        "I find a phone enough for daily time checks.",
    )
    _hk(
        "Why do some people wear expensive watches?",
        "simple_watch_gift",
        "I think some people wear expensive watches because they want to look stylish or show success. "
        "A nice watch can also be a gift for a special day. "
        "I understand that, but I prefer a simple watch for daily use.",
    )
    _hk(
        "Why do some people wear expensive watches?",
        "phone_time_check",
        "Maybe because an expensive watch looks special, while a phone only shows the time. "
        "Some people care about fashion more than checking the clock. "
        "I usually use my phone, so I do not need a costly watch.",
    )
    _hk(
        "Do you think it is important to wear a watch? Why?",
        "simple_watch_gift",
        "Yes, it can be useful, but it is not always necessary. "
        "I wear a watch because it helps me check time quickly in class and meetings. "
        "If I forget my phone, the watch still keeps me on schedule. "
        "I find it practical for students on busy weekdays.",
    )
    _hk(
        "Do you think it is important to wear a watch? Why?",
        "phone_time_check",
        "Not really important now, because most people check time on their phones. "
        "A watch is nice, but a phone already does the same job for me every day. "
        "I find a phone enough unless someone really likes wearing a watch.",
    )
    # Science daily life packs live in p1_freestyle_packs.py (preview workflow)
    # ---- Who questions: person-first, kit only soft tint ----
    _hk(
        "Who kept your room tidy when you were a child?",
        "parents_tidy_home",
        "My mum mostly kept my room tidy when I was a child. "
        "She asked me to put toys away, but she still did the deep cleaning every weekend at home. "
        "I find that habit warm, and it later made me notice a clear desk at university.",
    )
    _hk(
        "Who kept your room tidy when you were a child?",
        "tidy_desk_habit",
        "My mum kept the room tidy when I was a child, and she also taught me to clear my desk. "
        "Before homework she asked me to put books in order every evening. "
        "I find that early habit practical, because a tidy desk still helps me study now.",
    )
    _hk(
        "Who chose your name?",
        "name_parents_choice",
        "My parents chose my name when I was born. "
        "They picked it for a simple meaning and because relatives could say it easily every day. "
        "I find their choice natural, and I feel connected to my family when people call me.",
    )
    _hk(
        "Who chose your name?",
        "name_nickname_school",
        "My parents chose my formal name, though classmates later used a short nickname at school. "
        "The nickname was easier to shout across the playground after class. "
        "I find both names warm: the formal one from family, and the short one from friends.",
    )
    _hk(
        "Who do you live with?",
        "dorm_apartment_life",
        "I live with my roommate in campus dorms during term time. "
        "In the holidays I go back and live with my parents in our family apartment. "
        "I find both arrangements practical: the dorm helps me focus, and home feels more relaxed.",
    )
    _hk(
        "Who do you live with?",
        "tidy_desk_habit",
        "I live with my roommate in the dorm, and we both try to keep our desks tidy. "
        "Shared space means a clear desk reduces small arguments every evening before study. "
        "I find living with a roommate fine when we keep the room organised and respectful.",
    )
    _hk(
        "Who do you live with?",
        "parents_tidy_home",
        "During term time I live with a roommate, but in holidays I live with my parents. "
        "At home my mum still likes keeping rooms tidy, which feels familiar from childhood. "
        "I find family time warm, even though the dorm is more independent for study.",
    )
    _hk(
        "Who chose your clothes when you were a child?",
        "campus_tee_coat",
        "My parents chose my clothes when I was a child for school and weekends. "
        "They bought simple t-shirts and coats, and I rarely decided the style myself. "
        "I find that normal then; now I pick a comfortable t-shirt myself on weekdays.",
    )
    _hk(
        "Who chose your clothes when you were a child?",
        "campus_sweatshirt",
        "My parents chose my clothes when I was a child, especially warmer pieces for cool weather. "
        "They liked practical sweatshirts and coats more than fashionable items. "
        "I find that habit still shapes me: I prefer a sweatshirt that feels loose and comfortable.",
    )
    _hk(
        "Who chose your clothes when you were a child?",
        "dressing_mirror_home",
        "My parents chose my clothes when I was a child, and they checked me near the dressing mirror. "
        "Before school my mum looked at the outfit quickly every morning. "
        "I find that memory clear; now I use a mirror myself, but I choose my own clothes.",
    )
    _hk(
        "Who did you go shopping with when you were a child?",
        "mall_street_market",
        "I usually went shopping with my parents when I was a child. "
        "My mum often took me to a mall or a street market at weekends for clothes and small things. "
        "I find those trips memorable because I rarely went to shops alone then.",
    )
    _hk(
        "Who did you go shopping with when you were a child?",
        "fruit_groceries",
        "I went shopping with my parents, especially for fruit and groceries after school. "
        "My mum let me help pick fresh fruit most weekdays near our home. "
        "I find those small shopping trips warmer than big mall visits from childhood.",
    )
    _hk(
        "Who taught you to be polite when you were a child?",
        "polite_thank_you",
        "My parents taught me to be polite when I was a child at home and in public. "
        "They reminded me to say thank you and please every day in shops and on the bus. "
        "I find those manners still automatic, and they feel respectful in ordinary life.",
    )
    _hk(
        "Who taught you to be polite when you were a child?",
        "name_nickname_school",
        "My parents taught me to be polite, and teachers reinforced it when classmates used nicknames. "
        "At school we still had to say please and thank you, even in playful chat every day. "
        "I find that mix of home and school manners made polite habits feel natural.",
    )
    _hk(
        "Who is the funniest person you know?",
        "douyin_scroll_habit",
        "My roommate is the funniest person I know in daily campus life. "
        "He shares light Douyin clips and short jokes that make us laugh every evening before sleep. "
        "I find his humour a real stress buster after study, without needing a formal comedy show.",
    )
    _hk(
        "Who is the funniest person you know?",
        "comedy_hang_out",
        "My roommate is the funniest person I know. "
        "He watches comedies with friends and always turns small dorm stories into a good laugh. "
        "Most weekends he keeps the mood light. I find that humour warm and easy to enjoy.",
    )
    _hk(
        "Who was your favourite teacher when you were at school?",
        "patient_teacher_help",
        "My favourite teacher was a patient secondary-school teacher who explained concepts clearly. "
        "She stayed after class when I was confused and encouraged me to ask questions every week. "
        "I find that patience made me less afraid to speak up, and I still appreciate her help.",
    )
    _hk(
        "Who was your favourite teacher when you were at school?",
        "study_library_classes",
        "My favourite teacher was a patient teacher who linked class work to library study habits. "
        "After lunch classes she suggested flipping through real books instead of only screens. "
        "I find her advice practical, because it still helps me complete homework more independently.",
    )
    return HAND_KIT


build()
