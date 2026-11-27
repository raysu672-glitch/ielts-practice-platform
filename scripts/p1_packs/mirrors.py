# -*- coding: utf-8 -*-
"""Mirrors topic Freestyle packs."""


def register(_p):
    _p(
        "Why do some shops and restaurants have so many mirrors?",
        "hallway_mirror_routine",
        logic="先答镜子让空间显大、方便整理仪容，再举自己出门前照镜习惯作类比，补常见场景与理解感受。",
        kitHint="出门照镜习惯：用「检查仪容」理解商铺镜子，不是只讲穿衣。",
        words={
            "正面回答": ["To look bigger", "For customers to check themselves", "Bright and open"],
            "来源或举例": ["full-length mirrors", "hallway-style checks", "see outfit quickly"],
            "频次": ["when people walk in", "before they pay", "in busy malls"],
            "感受": ["makes sense", "feels brighter", "easy to understand"],
        },
        sample=(
            "I think they use mirrors to make the place look bigger and brighter. "
            "Customers can also check their hair or clothes quickly, a bit like I do by the door before I leave home. "
            "You notice that in busy malls and cafés quite often. "
            "It makes sense to me because people like to look presentable."
        ),
        sampleZh=(
            "我觉得是用镜子让店面看起来更开阔、更亮。"
            "顾客也能快速看看头发或衣服，有点像我每天出门前在门口检查一下。"
            "商场和咖啡馆里挺常见的。"
            "我能理解，因为大家都想得体一点。"
        ),
    )
    _p(
        "Why do some shops and restaurants have so many mirrors?",
        "dressing_mirror_home",
        logic="先扣店铺用途（显大、试看全身），再联系宿舍穿衣镜体验，说明常去场所与实用感受。",
        kitHint="房间穿衣镜：从「看全身效果」理解商铺多镜，紧扣镜子功能。",
        words={
            "正面回答": ["Bigger feel", "Try how things look", "Better lighting"],
            "来源或举例": ["full-length mirror", "check the whole outfit", "dorm dressing mirror"],
            "频次": ["in clothing stores", "near the entrance", "when people sit down"],
            "感受": ["practical", "not surprising", "helps shopping"],
        },
        sample=(
            "They probably want the space to feel larger and let people see how they look. "
            "In clothing stores a full-length mirror helps, kind of like the dressing mirror I keep in my dorm room. "
            "You see that near entrances or fitting areas quite a lot. "
            "I find it practical, not surprising at all."
        ),
        sampleZh=(
            "可能是想让空间显得更大，也让人看清自己的样子。"
            "服装店尤其需要全身镜，有点像我宿舍里那面穿衣镜。"
            "入口或试衣区附近很常见。"
            "我觉得挺实用，也不意外。"
        ),
    )
    _p(
        "How did you feel about looking in the mirror as a teenager?",
        "hallway_mirror_routine",
        logic="先答青少年时略在意形象，再述出门前快照镜细节，补每天频率与别扭又正常的感受。",
        kitHint="出门照镜：谈青春期对镜子的感觉，落脚在检查外表而非只聊衣服。",
        words={
            "正面回答": ["A bit self-conscious", "Cared more about looks", "Checked more often"],
            "来源或举例": ["quick check by the door", "hair and collar", "before school"],
            "频次": ["most mornings", "before going out with friends"],
            "感受": ["a bit awkward", "normal at that age", "less now"],
        },
        sample=(
            "As a teenager I felt a bit self-conscious about how I looked. "
            "I often did a quick check in the hallway mirror before school, especially my hair and collar. "
            "That was most mornings, and again before meeting friends. "
            "It felt a bit awkward, but pretty normal for that age."
        ),
        sampleZh=(
            "青少年时我对自己的形象有点在意。"
            "上学前常在门口镜子前快看一眼，尤其是头发和衣领。"
            "多数早上都会，见朋友前也是。"
            "有点别扭，但那个年纪挺正常的。"
        ),
    )
    _p(
        "How did you feel about looking in the mirror as a teenager?",
        "dressing_mirror_home",
        logic="先说青春期更关注全身形象，再写房间穿衣镜前纠结穿搭，补周末频率与长大后的变化。",
        kitHint="穿衣镜：青春期「站镜前看全身」合法扣题，不只讲买衣服。",
        words={
            "正面回答": ["Quite sensitive", "Worried about outfits", "Looked longer"],
            "来源或举例": ["full-length mirror", "try different tops", "check from head to toe"],
            "频次": ["before weekends out", "when photos mattered"],
            "感受": ["nervous sometimes", "less pressure now", "part of growing up"],
        },
        sample=(
            "I was quite sensitive about my appearance as a teenager. "
            "I would stand in front of the full-length mirror and change tops two or three times before going out. "
            "That happened often at weekends when photos mattered. "
            "I felt nervous sometimes, though I worry much less about mirrors now."
        ),
        sampleZh=(
            "青春期我对形象比较敏感。"
            "出门前常站在全身镜前换两三件上衣。"
            "周末要拍照时尤其会这样。"
            "有时紧张，不过现在对镜子没那么大压力了。"
        ),
    )
    _p(
        "Do you like having lots of mirrors at home?",
        "hallway_mirror_routine",
        logic="先答不必太多，一处够用，再举门口快镜例子，说每天用途与轻松感受。",
        kitHint="门口镜：回答家里镜子数量，强调「够用即可」。",
        words={
            "正面回答": ["Not too many", "One by the door is enough", "Simple is fine"],
            "来源或举例": ["hallway mirror", "quick check", "before heading out"],
            "频次": ["once or twice a day", "on busy mornings"],
            "感受": ["less clutter", "comfortable", "practical"],
        },
        sample=(
            "Not really — I do not need lots of mirrors at home. "
            "One by the door for a quick check before I head out is enough for me. "
            "I use it once or twice a day, usually on busy mornings. "
            "I feel more comfortable with a simple setup and less clutter."
        ),
        sampleZh=(
            "不太需要——家里镜子不用太多。"
            "门口有一面，出门前快照一下就够了。"
            "一天用一两次，早上忙的时候居多。"
            "简单一点我更自在，也不显得乱。"
        ),
    )
    _p(
        "Do you like having lots of mirrors at home?",
        "dressing_mirror_home",
        logic="先表态有一面全身镜就好，说明租房后添置原因，补使用频率与方便感受。",
        kitHint="房间穿衣镜：讨论「要不要很多镜」，全身镜一枚即可。",
        words={
            "正面回答": ["One full-length mirror", "Not everywhere", "Enough in the bedroom"],
            "来源或举例": ["dressing mirror", "get dressed properly", "small dorm room"],
            "频次": ["most mornings", "when I change outfits"],
            "感受": ["handy", "not overwhelming", "fits the room"],
        },
        sample=(
            "I like having one good mirror, but not mirrors everywhere. "
            "A full-length dressing mirror in the bedroom is handy when I get dressed in a small dorm. "
            "I use it most mornings and when I change outfits. "
            "One mirror feels enough — more would make the room look busy."
        ),
        sampleZh=(
            "有一面好镜子就行，不用到处都是。"
            "卧室里放一面全身穿衣镜，小宿舍换衣服很方便。"
            "多数早上和换装时会用。"
            "一面就够，再多房间会显得挤。"
        ),
    )
    _p(
        "Do you like looking at yourself in the mirror?",
        "hallway_mirror_routine",
        logic="先答会用但不爱久盯，再描述出门前快扫一眼，补频次与自然感受。",
        kitHint="快照习惯：喜欢程度=实用检查，非自恋。",
        words={
            "正面回答": ["Sometimes", "A quick look", "Not for long"],
            "来源或举例": ["hallway mirror", "hair and face", "before leaving"],
            "频次": ["most days", "twice if I go out again"],
            "感受": ["normal routine", "not obsessed", "fine with it"],
        },
        sample=(
            "I do, but only for a short time — I am not staring at myself for ages. "
            "I usually take a quick look in the hallway mirror to fix my hair before leaving. "
            "That is most days, maybe twice if I go out again in the evening. "
            "It feels like a normal routine, nothing special."
        ),
        sampleZh=(
            "会看，但不久——不会一直盯着。"
            "出门前在门口镜子里快理一下头发。"
            "几乎每天都这样，晚上再出门可能再看一次。"
            "像日常习惯，没什么特别的。"
        ),
    )
    _p(
        "Do you like looking at yourself in the mirror?",
        "dressing_mirror_home",
        logic="先答需要时看全身，再写房间镜前整理细节，补使用场景与坦然感受。",
        kitHint="全身镜：回答喜不喜欢看镜=必要时检查仪态。",
        words={
            "正面回答": ["When I need to", "For a full view", "Yes, briefly"],
            "来源或举例": ["dressing mirror", "straighten clothes", "check shoes too"],
            "频次": ["before class", "before meeting people"],
            "感受": ["confident enough", "practical", "not vain"],
        },
        sample=(
            "Yes, when I need to check the whole outfit. "
            "I stand in front of the dressing mirror to straighten my clothes and see if my shoes match. "
            "I do that before class or meeting people, not all day long. "
            "It helps me feel confident enough without being vain."
        ),
        sampleZh=(
            "需要看全身的时候会看。"
            "站在穿衣镜前拉平衣服，也看看鞋搭不搭。"
            "上课前或见人前会照一下，不是整天都照。"
            "让我心里踏实一点，也不算臭美。"
        ),
    )
    _p(
        "How often do you look in the mirror each day?",
        "hallway_mirror_routine",
        logic="先给频率（一天一两次），再写固定出门前动作链，补晚间是否再看与习惯感受。",
        kitHint="行为习惯类：时间线=早起门口快镜+偶尔晚上出门前。",
        words={
            "正面回答": ["Once or twice", "Every morning", "Sometimes again at night"],
            "原因": ["want to look neat", "quick habit", "before I leave"],
            "时间线+行为描述": ["get dressed", "hallway mirror", "fix hair", "grab my bag"],
            "影响": ["saves embarrassment", "fast routine", "feels automatic"],
        },
        sample=(
            "Usually once or twice a day. "
            "I want to look neat before people see me, so it became a quick habit. "
            "After I get dressed I check the hallway mirror, fix my hair, then grab my bag — and I might repeat that if I go out again at night. "
            "It only takes seconds and saves small embarrassment later."
        ),
        sampleZh=(
            "一般一天一两次。"
            "想在别人面前得体一点，就变成小习惯。"
            "穿好衣服后在门口镜前理头发、拿包；晚上再出门可能再来一次。"
            "就几秒，能避免一些小尴尬。"
        ),
    )
    _p(
        "How often do you look in the mirror each day?",
        "dressing_mirror_home",
        logic="先答早上必看、傍晚有时看，再述全身镜步骤，说明对穿搭信心的影响。",
        kitHint="穿衣镜频次：行为链=站镜前整理全身。",
        words={
            "正面回答": ["Every morning", "Maybe once more", "Not constantly"],
            "原因": ["small room", "see full outfit", "before campus"],
            "时间线+行为描述": ["open wardrobe", "dressing mirror", "turn side to side", "leave"],
            "影响": ["less second-guessing", "saves time", "calmer start"],
        },
        sample=(
            "Pretty much every morning, and sometimes once more in the evening. "
            "In a small dorm I like to see the full outfit in the dressing mirror before campus. "
            "I open the wardrobe, check from the front and side, then leave — the whole thing is under a minute. "
            "It stops me second-guessing my clothes and starts the day calmer."
        ),
        sampleZh=(
            "基本每天早上都会，傍晚有时再看一次。"
            "宿舍小，去学校前想在穿衣镜里看全套搭配。"
            "开衣柜、正面侧面看一下就走，不到一分钟。"
            "少纠结穿搭，早上心态也稳一点。"
        ),
    )
    _p(
        "How have phone cameras changed the way people use mirrors?",
        "hallway_mirror_routine",
        logic="先答手机自拍部分取代镜子，再对比实物镜快检与相机修图，说个人更偏哪边。",
        kitHint="对比类：手机自拍 vs 门口实物镜，仍围绕镜子用途。",
        words={
            "正面回答": ["People check phones more", "Mirrors less sometimes", "Both still matter"],
            "选项1的特点与作用": ["phone camera", "selfies", "filters", "instant share"],
            "选项2的特点与作用": ["real mirror", "true reflection", "faster before leaving"],
            "个人感受": ["I still use a mirror", "phones for photos", "mirror for daily rush"],
        },
        sample=(
            "I think people rely on phone cameras more, especially for selfies and filters. "
            "A phone lets you take a photo, edit it, and share it straight away. "
            "A real mirror still gives a true reflection in seconds when you rush out the door. "
            "Personally I still use a hallway mirror daily, and only use the phone camera when I want a photo."
        ),
        sampleZh=(
            "我觉得大家更依赖手机镜头，尤其自拍和滤镜。"
            "手机能拍、能修、能马上发。"
            "实物镜出门前几秒就能看真实样子。"
            "我个人每天还是用门口镜，拍照才用手机。"
        ),
    )
    _p(
        "How have phone cameras changed the way people use mirrors?",
        "dressing_mirror_home",
        logic="先概括镜子看全身、手机看照片的不同，再各举使用场景，收束个人偏好。",
        kitHint="对比全身镜与前置镜头：选项对比扣镜子话题。",
        words={
            "正面回答": ["Cameras replaced some mirror time", "Not completely", "Different jobs"],
            "选项1的特点与作用": ["front camera", "outfit photos", "social media"],
            "选项2的特点与作用": ["full-length mirror", "head-to-toe check", "no battery needed"],
            "个人感受": ["mirror for dressing", "phone for records", "both useful"],
        },
        sample=(
            "Phone cameras have taken over some mirror time, but not completely. "
            "People film outfits or use the front camera before posting online, which mirrors cannot do. "
            "A full-length mirror is still better for a quick head-to-toe check with no battery or angle tricks. "
            "I use the dressing mirror when I get ready, and the phone when I want a picture to keep."
        ),
        sampleZh=(
            "手机镜头占了一部分照镜时间，但没完全取代。"
            "拍穿搭、发帖会靠前置镜头，镜子做不到。"
            "全身镜更适合几秒从头到脚看清楚，也不用琢磨角度。"
            "我换装用镜，想留照片才用手机。"
        ),
    )