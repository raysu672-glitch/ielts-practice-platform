# -*- coding: utf-8 -*-
"""Feeling bored Freestyle packs (preview-page style)."""


def register(_p):
    _p(
        "Do you often feel bored?",
        "nearby_park_walk",
        logic="先正面回答是否常无聊，再用公园散步举例，补上频次与感受。",
        kitHint="换素材=换一套生活细节；四步名称不变，只换步骤下面的料。",
        words={
            "正面回答": ["Not often", "Sometimes after study", "Not really during term"],
            "来源或举例": ["a nearby park", "evening walks", "fresh air"],
            "频次": ["most evenings after study", "when the weather is fine"],
            "感受": ["practical", "calming", "helps me reset"],
        },
        sample=(
            "Not often. When I feel a bit bored after study, I take a short walk in a nearby park. "
            "Fresh air and a simple route help me reset without scrolling for too long. "
            "I usually go most evenings when the weather is fine. "
            "I find that walk practical and calming."
        ),
        sampleZh=(
            "不常。学习后觉得有点无聊时，我会去附近公园走走。"
            "新鲜空气和简单路线能让我缓过来，也不用刷太久手机。"
            "天气好的傍晚我常去。我觉得这种散步实用又平静。"
        ),
    )
    _p(
        "Do you often feel bored?",
        "yellow_bike_gift",
        logic="承认有时无聊，再落到骑车去公园，说明周末频率与放松效果。",
        kitHint="同一辆黄自行车也可挂到童年机会、开学日、公园等题；这里用来「解闷」。",
        words={
            "正面回答": ["Sometimes", "Especially on weekdays", "Yes, after long classes"],
            "来源或举例": ["my yellow bike", "ride to the park", "a short cycle"],
            "频次": ["at weekends for about an hour", "when I have time"],
            "感受": ["helps me unwind", "gives me something to do"],
        },
        sample=(
            "Sometimes I feel bored, especially during the week when I've been sitting in class all day. "
            "When that happens, I like to take my bike to the park and go for a ride. "
            "I usually do that at weekends, for about an hour. "
            "It gives me something to do, and it also helps me unwind."
        ),
        sampleZh=(
            "有时会无聊，尤其是工作日坐了一整天课的时候。"
            "这时我喜欢骑车去公园转一圈。通常在周末骑大约一小时。"
            "既有事可做，也能放松一下。"
        ),
    )
    _p(
        "Do you often feel bored?",
        "douyin_scroll_habit",
        logic="先说不太容易无聊，再举例短视频/聚会，补上晚上或周末与放松感受。",
        kitHint="短视频或朋友聚会是另一套合法 freestyle；别硬套到无关话题。",
        words={
            "正面回答": ["Not really", "To be honest, not often", "I don't get bored easily"],
            "来源或举例": ["watch short videos", "hang out with friends", "chat after dinner"],
            "频次": ["most evenings", "at weekends if we have time"],
            "感受": ["helps me switch off", "more relaxed"],
        },
        sample=(
            "Not really, to be honest. After a long day I usually watch short videos or hang out with my friends, "
            "so I don't get bored easily. I do this most evenings, or at weekends if we have time. "
            "It helps me switch off and feel more relaxed."
        ),
        sampleZh=(
            "说实话不太会。忙完一天后我常刷短视频或和朋友出去，所以不太容易无聊。"
            "多数在晚上，周末有空也会。这能让我切换状态、更放松。"
        ),
    )
    _p(
        "When do you usually feel bored?",
        "nearby_park_walk",
        logic="先点出通常何时无聊，再说明会去公园缓解，补频率与平静感受。",
        kitHint="本题切「公园解闷」：先答无聊的时间点，再落到散步。",
        words={
            "正面回答": ["On quiet Sunday evenings", "After finishing homework", "When I stay indoors too long"],
            "来源或举例": ["a nearby park", "evening walks", "fresh air"],
            "频次": ["most quiet evenings", "when the weather is fine"],
            "感受": ["calming", "practical", "helps me reset"],
        },
        sample=(
            "I usually feel bored on quiet Sunday evenings after I finish my tasks. "
            "Then I take a short walk in a nearby park to reset. "
            "I do this when the weather is fine. "
            "I find that walk calming and practical."
        ),
        sampleZh=(
            "我通常在安静的周日晚上、事情做完后会觉得无聊。"
            "那时我会去附近公园走走缓一缓。"
            "天气好时会去。"
            "我觉得这种散步平静又实用。"
        ),
    )
    _p(
        "When do you usually feel bored?",
        "yellow_bike_gift",
        logic="先说工作日久坐后容易无聊，再落到骑车，补周末频率与放松。",
        kitHint="本题切「骑车解闷」：无聊时间点在久坐课后，用黄自行车换活动。",
        words={
            "正面回答": ["After long weekday classes", "During long indoor days", "When I sit too much"],
            "来源或举例": ["my yellow bike", "ride to the park", "a short cycle"],
            "频次": ["at weekends", "when I have about an hour"],
            "感受": ["helps me unwind", "gives me something to do"],
        },
        sample=(
            "I usually feel bored after long weekday classes when I have been sitting all day. "
            "Then I like to take my yellow bike to the park for a short ride. "
            "I usually do that at weekends for about an hour. "
            "It gives me something to do and helps me unwind."
        ),
        sampleZh=(
            "我通常在工作日上完一长串课、坐了一整天后会无聊。"
            "那时我会骑黄自行车去公园转一小圈。"
            "多半在周末，骑大约一小时。"
            "既有事可做，也能放松。"
        ),
    )
    _p(
        "When do you usually feel bored?",
        "douyin_scroll_habit",
        logic="先说晚上空闲时容易无聊，再说明会刷短视频或找朋友，补频率与切换状态感受。",
        kitHint="本题切「短视频/聚会」：无聊多在晚上空档，用刷手机或朋友填上。",
        words={
            "正面回答": ["In the evening after study", "When I have free time at night", "On quiet nights"],
            "来源或举例": ["watch short videos", "hang out with friends", "chat after dinner"],
            "频次": ["most evenings", "at weekends"],
            "感受": ["helps me switch off", "more relaxed"],
        },
        sample=(
            "I usually feel bored in the evening after study when everything is quiet. "
            "Then I watch short videos or chat with friends. "
            "I do this most evenings, or at weekends if we have time. "
            "It helps me switch off and feel more relaxed."
        ),
        sampleZh=(
            "我通常在学习后的晚上、周围很安静时会无聊。"
            "那时我会刷短视频或和朋友聊天。"
            "多数晚上如此，周末有空也会。"
            "这能让我切换状态、更放松。"
        ),
    )
    _p(
        "How did you deal with boredom as a child?",
        "nearby_park_walk",
        logic="先说童年解闷方式，再举去公园玩，补当时频率与快乐感受。",
        kitHint="本题切「童年公园」：回答童年如何解闷，散步/户外是合法细节。",
        words={
            "正面回答": ["I went outside", "I played in the park", "I looked for fresh air"],
            "来源或举例": ["a nearby park", "run around", "play with friends"],
            "频次": ["after school", "at weekends"],
            "感受": ["fun", "free", "happy"],
        },
        sample=(
            "As a child I usually went outside when I felt bored. "
            "There was a park near my home, and I ran around with friends there. "
            "We went after school or at weekends. "
            "I find those days fun and free to remember."
        ),
        sampleZh=(
            "小时候觉得无聊时，我通常会出门。"
            "家附近有公园，我会和朋友在那里跑着玩。"
            "放学后或周末常去。"
            "现在回想起来觉得快乐又自由。"
        ),
    )
    _p(
        "How did you deal with boredom as a child?",
        "yellow_bike_gift",
        logic="先说骑车解闷，再点出黄自行车，补童年骑行频率与自由感受。",
        kitHint="本题切「童年骑车」：解闷方式是骑黄自行车，紧扣童年行为。",
        words={
            "正面回答": ["I rode my bike", "I went cycling", "I left the house on my bike"],
            "来源或举例": ["my yellow bike", "ride around the block", "cycle to the park"],
            "频次": ["after school", "most weekends"],
            "感受": ["free", "exciting", "really convenient"],
        },
        sample=(
            "As a child I dealt with boredom by riding my yellow bike. "
            "I cycled around the block or to the park near home. "
            "I did that after school and most weekends. "
            "I find that memory free and exciting."
        ),
        sampleZh=(
            "小时候我觉得无聊就会骑黄色小自行车。"
            "在街区转一圈，或骑到家附近的公园。"
            "放学后和多数周末都会。"
            "现在回想觉得自由又兴奋。"
        ),
    )
    _p(
        "How did you deal with boredom as a child?",
        "douyin_scroll_habit",
        logic="先诚实说童年没有短视频，再用和朋友玩/看简单节目作对比解闷方式。",
        kitHint="本题切「朋友相处」：童年解闷不是刷抖音；用聚会/玩耍回答，短视频素材只作对照习惯。",
        words={
            "正面回答": ["I played with friends", "I watched simple cartoons", "I talked with classmates"],
            "来源或举例": ["hang out with friends", "play outside", "watch light shows"],
            "频次": ["after school", "at weekends"],
            "感受": ["happy", "less bored", "relaxed"],
        },
        sample=(
            "As a child I did not have short videos, so I played with friends when I felt bored. "
            "We hung out after school or watched simple cartoons at weekends. "
            "That filled the empty time quickly. "
            "I find those days happy and relaxed."
        ),
        sampleZh=(
            "小时候没有短视频，觉得无聊时我就和朋友玩。"
            "放学后一起出去，或周末看简单卡通。"
            "空档很快就被填满。"
            "现在回想觉得快乐又轻松。"
        ),
    )
    _p(
        "Why do people today seem to get bored more easily?",
        "douyin_scroll_habit",
        logic="先给原因：短视频让人习惯快速刺激，再举例刷手机，补日常频率与影响感受。",
        kitHint="本题切「短视频习惯」：解释为何更容易无聊，短视频是核心原因，不是跑题。",
        words={
            "正面回答": ["Because of short videos", "Phones make waits feel long", "People want new clips fast"],
            "来源或举例": ["scroll short videos", "switch apps quickly", "endless clips"],
            "频次": ["every evening", "whenever they wait"],
            "感受": ["restless", "hard to focus", "less patient"],
        },
        sample=(
            "I think people get bored more easily because short videos give endless new clips. "
            "When nothing new appears, waiting feels longer than before. "
            "Many people scroll every evening. "
            "I find this habit makes us less patient."
        ),
        sampleZh=(
            "我觉得人们更容易无聊，是因为短视频总能给出新内容。"
            "一旦没有新的，等待就显得更长。"
            "很多人每天晚上都在刷。"
            "我觉得这让人更没耐心。"
        ),
    )
    _p(
        "Why do people today seem to get bored more easily?",
        "nearby_park_walk",
        logic="先给原因：室内时间多、户外少，再对比公园活动，补现代生活频率与感受。",
        kitHint="本题切「缺少户外」：更容易无聊是因为少出门；公园是对照解法。",
        words={
            "正面回答": ["Because people stay indoors more", "Less outdoor time", "Screens replace walks"],
            "来源或举例": ["stay at home", "skip park walks", "less fresh air"],
            "频次": ["most weekdays", "after study"],
            "感受": ["restless", "tired of screens", "need fresh air"],
        },
        sample=(
            "I think people get bored more easily because they stay indoors with screens more often. "
            "A short park walk used to fill empty time, but many people skip it now. "
            "This happens most weekdays after study. "
            "I find less outdoor time makes boredom come faster."
        ),
        sampleZh=(
            "我觉得人们更容易无聊，是因为更多时间待在室内对着屏幕。"
            "以前公园散步就能填空档，现在很多人省略了。"
            "工作日学习后尤其如此。"
            "我觉得户外少了，无聊来得更快。"
        ),
    )
    _p(
        "Why do people today seem to get bored more easily?",
        "yellow_bike_gift",
        logic="先给原因：活动变少、选择太多反而难满意，再举骑车等具体活动作对照。",
        kitHint="本题切「缺少真实活动」：用骑车这类具体活动说明为何现在更容易闷。",
        words={
            "正面回答": ["Because real activities are fewer", "Too many easy options", "People sit more"],
            "来源或举例": ["skip cycling", "stay seated", "choose screens instead of a ride"],
            "频次": ["on busy weekdays", "after class"],
            "感受": ["restless", "unsatisfied", "need movement"],
        },
        sample=(
            "I think people get bored more easily because they sit more and do fewer real activities. "
            "A simple bike ride to the park can fix boredom, but many people choose screens instead. "
            "This is common on busy weekdays after class. "
            "I find less movement makes empty time feel longer."
        ),
        sampleZh=(
            "我觉得人们更容易无聊，是因为坐得更多、真实活动更少。"
            "骑车去公园本能解闷，但很多人改刷屏幕。"
            "工作日课后很常见。"
            "我觉得少活动会让空白时间显得更长。"
        ),
    )
    # Behaviour: What do you do when you feel bored?
    _p(
        "What do you do when you feel bored?",
        "nearby_park_walk",
        logic="先说去公园走走，再补原因与傍晚行动，收束平静影响。",
        kitHint="本题切「公园散步」：无聊时的具体行动是出门透气。",
        words={
            "正面回答": ["I go for a walk", "I leave the dorm for a bit", "I head to a nearby park"],
            "原因": ["I need fresh air", "staying indoors makes it worse", "a short walk resets me"],
            "时间线+行为描述": ["most evenings after study", "when the weather is fine", "for about fifteen minutes"],
            "影响": ["helps me reset", "calming", "beats endless scrolling"],
        },
        sample=(
            "When I feel bored, I usually go for a short walk in a nearby park. "
            "Staying indoors with my phone makes the boredom worse, so fresh air helps. "
            "I do this most evenings after study when the weather is fine. "
            "It helps me reset and beats endless scrolling."
        ),
        sampleZh=(
            "觉得无聊时，我通常去附近公园走走。"
            "闷在宿舍刷手机只会更无聊，所以需要新鲜空气。"
            "多数在学习后的傍晚，天气好就去。"
            "能让我缓过来，也比一直刷手机好。"
        ),
    )
    _p(
        "What do you do when you feel bored?",
        "yellow_bike_gift",
        logic="先说骑车出门，再说明为何比坐着强，补周末频率与放松影响。",
        kitHint="本题切「骑车解闷」：无聊时的行动是骑黄自行车去公园。",
        words={
            "正面回答": ["I take my bike out", "I go for a short ride", "I cycle to the park"],
            "原因": ["sitting makes me restless", "I want light movement", "a ride clears my head"],
            "时间线+行为描述": ["at weekends for about an hour", "after long classes", "when I have time"],
            "影响": ["helps me unwind", "gives me something to do", "more energetic"],
        },
        sample=(
            "When I feel bored, I take my yellow bike and ride to the park. "
            "Sitting all day makes me restless, so light movement clears my head. "
            "I usually do that at weekends for about an hour. "
            "It gives me something to do and helps me unwind."
        ),
        sampleZh=(
            "觉得无聊时，我会骑黄自行车去公园。"
            "坐太久会烦，轻度运动能清醒一下。"
            "多半在周末，骑大约一小时。"
            "既有事可做，也能放松。"
        ),
    )
    _p(
        "What do you do when you feel bored?",
        "douyin_scroll_habit",
        logic="先说刷短视频或找朋友，再说明轻松切换，补晚上频率与放松影响。",
        kitHint="本题切「短视频/聚会」：无聊时的行动是刷手机或聊天。",
        words={
            "正面回答": ["I watch short videos", "I chat with friends", "I hang out for a bit"],
            "原因": ["I want a quick switch-off", "light clips fill empty time", "talking helps"],
            "时间线+行为描述": ["most evenings", "after dinner", "at weekends if we have time"],
            "影响": ["helps me switch off", "more relaxed", "passes the time"],
        },
        sample=(
            "When I feel bored, I usually watch short videos or chat with friends. "
            "Light clips help me switch off after study without much effort. "
            "I do this most evenings, or at weekends if we have time. "
            "It helps me relax and pass the empty time."
        ),
        sampleZh=(
            "觉得无聊时，我通常刷短视频或和朋友聊天。"
            "轻松片段能让我学习后快速切换状态。"
            "多数在晚上，周末有空也会。"
            "能放松，也能打发空档。"
        ),
    )
    # Opinion: Is it ever good to feel bored?
    _p(
        "Is it ever good to feel bored?",
        "nearby_park_walk",
        logic="先承认偶尔有益，再举例无聊会推自己出门散步，补作用与感受。",
        kitHint="本题切「无聊促使出门」：偶尔无聊可以推动去公园，仍正面回答「是否有益」。",
        words={
            "正面回答": ["Yes, sometimes", "In small amounts", "It can be useful"],
            "举例或原因": ["it pushes me outdoors", "a park walk starts from boredom", "I stop scrolling"],
            "作用或影响": ["gives me a reset", "I notice fresh air again", "from time to time"],
            "感受": ["healthy", "calming", "quite useful"],
        },
        sample=(
            "Yes, sometimes it is good to feel a little bored. "
            "That empty feeling pushes me to leave the dorm and walk in a nearby park. "
            "From time to time it gives me a real reset outdoors. "
            "I find a bit of boredom quite useful."
        ),
        sampleZh=(
            "有时有一点点无聊是好事。"
            "那种空档会推我离开宿舍，去附近公园走走。"
            "偶尔能让我在户外真正缓过来。"
            "我觉得一点点无聊其实挺有用。"
        ),
    )
    _p(
        "Is it ever good to feel bored?",
        "yellow_bike_gift",
        logic="先说有时有益，再举例无聊会让自己骑车活动，补作用与感受。",
        kitHint="本题切「无聊促成骑车」：有益之处在于催自己动起来。",
        words={
            "正面回答": ["Yes, sometimes", "A little can help", "Not always bad"],
            "举例或原因": ["it makes me ride my bike", "I stop sitting still", "I go for a short ride"],
            "作用或影响": ["I move more", "I feel less stuck", "at weekends"],
            "感受": ["useful", "better mood", "healthier"],
        },
        sample=(
            "Yes, sometimes boredom can be good. "
            "When I feel stuck indoors, it makes me take my bike out for a short ride. "
            "At weekends that small push helps me move more. "
            "I find it useful and my mood feels better."
        ),
        sampleZh=(
            "有时无聊可以是好事。"
            "闷在室内时，它会催我骑车出去转一圈。"
            "周末这点推力能让我多动动。"
            "我觉得有用，心情也会好一点。"
        ),
    )
    _p(
        "Is it ever good to feel bored?",
        "douyin_scroll_habit",
        logic="先辩证：短暂无聊有益，但别立刻刷短视频；说明偶尔停下来的作用。",
        kitHint="本题切「别急着刷」：承认无聊可有益，并用短视频习惯作反面提醒。",
        words={
            "正面回答": ["Yes, briefly", "Sometimes, if I do not scroll at once", "A short pause can help"],
            "举例或原因": ["I used to open Douyin immediately", "waiting helps ideas come", "not every gap needs clips"],
            "作用或影响": ["I rest my eyes", "I think more clearly", "from time to time"],
            "感受": ["calmer", "more balanced", "healthier"],
        },
        sample=(
            "Yes, briefly — if I do not open short videos at once. "
            "A short pause can help me rest my eyes instead of endless scrolling. "
            "From time to time that quiet gap makes me think more clearly. "
            "I find that kind of boredom calmer and healthier."
        ),
        sampleZh=(
            "可以，但要短，而且别马上打开短视频。"
            "短暂停一下能让眼睛休息，而不是一直刷。"
            "偶尔这段空白反而让我更清醒。"
            "我觉得这种无聊更平静、也更健康。"
        ),
    )
