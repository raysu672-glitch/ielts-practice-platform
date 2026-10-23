# 句子翻译逐步语义审计（AI）

- 句数：114
- 步骤：302
- 问题条数：62（high=8 medium=32 low=22）
- API 失败批次：0

## HIGH（8）

### #24 Step 2
- 中：印度电影，【例如】，让人们深刻体会到歌唱和舞蹈【对印度文化的】重要性。
- 英：Indian movies, for example, let people know how important singing and dancing is to the Indians.
- 问题：第2步中文“对印度文化的”被译成 to the Indians（对印度人），且“深刻体会到”仅译作 know，语义不对齐。
- 建议：改为 ... how important singing and dancing is to Indian culture，并用 deeply appreciate/realize 体现“深刻体会到”。

### #38 Step 2
- 中：将传统文化作为【营利性】旅游景点可能会破坏其原真性。
- 英：Using traditional cultures as money-making tourist attractions may destroy them.
- 问题：中文“破坏其原真性”英文只作“destroy them”，表示破坏传统文化本身，未表达“原真性”，them 也不能指代原真性。
- 建议：改为 ... may destroy their authenticity。

### #43 Step 1
- 中：最有效的方法之一就是频繁更换雇主。
- 英：One of the most effective ways is believed to hop from one company to another.
- 问题：英文把“据信”写成 One of the most effective ways is believed to hop...，这会让 hop 的逻辑主语变成 ways（方法跳槽），而且本步中文并未出现“据信”，中英不对齐。
- 建议：改为 It is believed that one of the most effective ways to achieve their financial ambition is to hop from one company to another.（或 One of the most effective ways ... is believed to be to hop...），并在本步中文中补出“据信”

### #70 Step 2
- 中：房价已达到历史最高水平，【若完全依赖父母，许多年轻人将无力支付首付款和房贷】。
- 英：Housing prices are higher than ever, and if relying on it would be impossible for many young people to pay a deposit and mortgage.
- 问题：英文 “and if relying on it would be impossible for many young people to pay a deposit and mortgage” 语法错误且语义错位：“it” 指代不明，中文“若完全依赖父母”中的“父母”“完全”均未译出，“许多年轻人将无力支付”也被错写成 “relying on it would be impossible for many young people to pay（许多年轻人支付…将不可能）”
- 建议：改为 Housing prices are higher than ever, and if young people relied entirely on their parents, many of them would be unable to pay a deposit and mortgage.

### #98 Step 2
- 中：儿童需要培养的【不仅是智力】技能，【最佳途径正是】【通过体育运动、游戏以及与其他孩子一起玩耍等】活动。
- 英：Children need to develop skills other than intellectual ones, and the best way to do this is through activities such as sports, games and playing with other kids.
- 问题：“不仅是智力技能”意为除智力技能外还包括其他技能，而 other than intellectual ones 意为“智力技能之外的技能”，语义不对等。
- 建议：改为 not only intellectual skills（或 skills beyond intellectual ones，若原意是后者）。

### #104 Step 1
- 中：他们不太可能讨论价格和款式。
- 英：They are not likely to talk about the price and taste.
- 问题：“款式”译成 taste 不准确，taste 是“品味/审美”，不是衣服的款式；后续步骤也延续此错误。
- 建议：改为 style/design，如 the price and style of clothes。

### #110 Step 1
- 中：这意味着孩子们成长。
- 英：This means that the children grow up.
- 问题：整句的中文（他们的行为也完全按照个人意愿进行）与 finalEnglish（This means that the children grow up without consideration for others）语义完全不对应，各步骤的中英文也都是「这意味着孩子们成长」，与题目所给中文无关。
- 建议：按中文改为 Their behavior is also entirely guided by their own will.（或与之对应的英文，并同步修改各步骤）

### #111 Step 2
- 中：【当他们开始上学时】，他们尚未学会尊重他人或遵守规则。
- 英：When they begin to go to school, they have not learned to respect others and obey rules.
- 问题：fullChinese 包含两句，「因此，这些孩子在成长过程中缺乏对他人的考虑」这句在 finalEnglish 和各步骤英文中完全缺失，中文已写明而英文没有。
- 建议：补译前半句，如 Therefore, these children grow up without consideration for others. When they begin to go to school, they have not learned to respect others or obey rules.

## MEDIUM（32）

### #9 Step 2
- 中：他们的成年世界将【在技术领域】持续变革，而互联网正是【当今世界所有知识与信息的】【关键载体】。
- 英：Their adult world will be changing constantly in terms of technology and the Internet is the key to all the knowledge and information available in the world today.
- 问题：中文高亮为“关键载体”，英文却写成“the key to all the knowledge and information”（通往知识信息的关键/途径），把“载体”（carrier）的意思改成了“获取途径”，语义不一致。
- 建议：改为 the Internet is the key carrier of all the knowledge and information available in the world today

### #11 Step 2
- 中：一方面，【从某些乐观主义者的角度来看】，【与外星生命体建立联系】可能带来【巨大的】益处。
- 英：On the one hand, from the perspective of some optimists, there may be great benefits to connecting alien life forms.
- 问题：中文“与外星生命体建立联系”，英文“connecting alien life forms”缺介词 with，字面成了“把外星生命体连接起来”，与“与……建立联系”不对应。
- 建议：改为 benefits to connecting with alien life forms

### #17 Step 4
- 中：例如，如果能为幼儿提供更多免费疫苗，婴儿和儿童死亡率能显著降低，【从而为国家发展培养出更健康的下一代人口】。
- 英：For example, if more free vaccines are available to young children, infant and child mortality rates could be remarkably reduced, which contributes a healthier generation of population to the development of a country.
- 问题：第4步中文“培养出更健康的下一代人口”中的“培养出”和“下一代”未在英文中准确体现，contributes ... to 结构也变成“向国家发展贡献人口”，语义偏移。
- 建议：可改为 which helps cultivate a healthier next generation for the country's development.

### #20 Step 3
- 中：一方面，我必须承认，【在媒体的帮助下】，了解世界各地不同文化变得异常便捷。
- 英：On the one hand, I admit that getting acquainted with culture of different places across the world has become incredibly easy and convenient with the help of media.
- 问题：第3步中文新增“我必须承认”，但英文仍只有 I admit，未体现“必须”这一语气。
- 建议：改为 I must admit that ...

### #21 Step 1
- 中：例如，有书籍和杂志生动地描绘了人们的生活。
- 英：For example, there are books and magazines, picturing how people live their daily lives.
- 问题：第1步中文已含“生动地”，但英文没有 vividly，直到第3步才补上，导致第1、2步中英不对齐且高亮新增信息位置不合理。
- 建议：第1、2步中文删去“生动地”，或英文相应补上 vividly。

### #22 Step 2
- 中：【关于饮食传统和节日庆典的】信息【几乎无需耗费时间和金钱】即可获取。
- 英：Information about their food tradition and festival celebration can be accessed at almost no cost of time and money.
- 问题：fullChinese 中的“当地”未准确译出，英文用 their 指代不明，且不等于 local。
- 建议：改为 Information about local food tradition and festival celebration ...

### #23 Step 2
- 中：同样地，观看电影也能让观众身临其境地体验【与自身截然不同的】生活方式。
- 英：In a similar way, watching movies brings viewers close to a lifestyle totally different from their own.
- 问题：第2步中文改为“身临其境地体验”并加了“也能”，但英文仍是 brings viewers close to，未体现“体验/身临其境”和“也能”。
- 建议：改为 can also bring viewers close to / allow viewers to experience immersively a lifestyle ...

### #26 Step 1
- 中：童年时期，我们被教唱歌。
- 英：As children, we are taught songs by our parents and teachers.
- 问题：步骤1中文为“我们被教唱歌”，未写施动者，但英文已加入 by our parents and teachers，导致中英不对齐，且使步骤2中文新增的“父母和老师”在英文中并非新增。
- 建议：步骤1英文改为 As children, we are taught songs. 或在中文步骤1补上“由父母和老师”。

### #33 Step 1
- 中：最明显的例证是射击比赛。
- 英：One of the most obvious examples of this is the shooting competition.
- 问题：中文“最明显的例证”被译为“One of the most obvious examples”，多出“之一”，改变了范围。
- 建议：改为 The most obvious example is...，或把中文改为“最明显的例证之一”。

### #35 Step 3
- 中：就前者而言，数百万人被吸引到主办国观看世界级体育赛事或体验当地文化，【这两项活动均能带来数十亿美元的经济收益并创造大量就业机会】。
- 英：With regard to the former, millions of people are attracted to the host country either to watch world-class sports games or to experience local culture, both of which bring in billions of dollars in cash and create a large number of job opportunities.
- 问题：中文“数十亿美元的经济收益”译为“billions of dollars in cash”，把经济收益具体化为现金收入，且 in cash 为原文没有的增义。
- 建议：删去 in cash，或改为 billions of dollars in economic benefits/revenue。

### #36 Step 4
- 中：【举办这一国际赛事还能】另一贡献是能为大多数民众激发对体育运动的兴趣，促使他们增加身体活动量。
- 英：The other contribution made by hosting this international event is that an interest in sports can be developed for most citizens, and they would become more physically active.
- 问题：第4步中文高亮“举办这一国际赛事还能”与英文“made by hosting this international event”不对应：英文表达“由举办该赛事所作的另一贡献”，没有体现“还能”，且中文“还能另一贡献是”结构不通。
- 建议：中文改为“举办这一国际赛事所做出的另一贡献是……”，或英文改为 Hosting this international event can also arouse...

### #39 Step 2
- 中：这是因为【传统的】表演方式需要被改编。
- 英：This is because the way that they are originally performed needs to be altered.
- 问题：中文新增“传统的”（传统表演方式），英文用“that they are originally performed”（最初被表演的方式），未体现 traditional。
- 建议：改为 traditional performance forms 或 the way traditional performances are performed。

### #43 Step 2
- 中：【实现财务目标的】最有效的方法之一就是频繁更换雇主。
- 英：One of the most effective ways to achieve their financial ambition is believed to hop from one company to another.
- 问题：中文“实现财务目标”并无物主，英文 their financial ambition 中的 their 缺少指代对象；且上一步的 hop 主语错位问题仍然存在。
- 建议：可改为 to achieve financial ambitions，并把全句改为 It is believed that one of the most effective ways to achieve financial ambitions is to hop from one company to another.

### #44 Step 2
- 中：【私营企业】【参与某些技术的研发】必须受到【严格】限制。
- 英：Private companies' involvement in the research of some technologies must be restricted.
- 问题：中文新增了【严格】限制，但英文只有 must be restricted，未体现“严格（strictly）”。
- 建议：改为 must be strictly restricted

### #49 Step 2
- 中：【首先，】居家办公能显著节省员工的时间。
- 英：Firstly, it is time-saving for employees to work at home.
- 问题：第二步中文加入了“显著”，但英文只有 time-saving，未体现“显著”这一程度修饰，导致中英不对齐。
- 建议：可改为 Firstly, it is significantly time-saving for employees to work at home. 或 Firstly, working at home can significantly save employees' time.

### #54 Step 2
- 中：【然而，】我认为这种【非传统的】工作方式【反而】会引发更多问题。
- 英：However, I am of the opinion that this unconventional way of working causes more problems.
- 问题：第二步中文加入了“反而”，英文仅用 However 表达“然而”，未体现“反而/相反”的转折递进含义。
- 建议：可改为 However, I am of the opinion that this unconventional way of working instead causes more problems.

### #56 Step 1
- 中：他们更容易患上肥胖症或高血压。
- 英：They are more likely to be attacked by obesity or hypertension.
- 问题：“患上肥胖症或高血压”译为 be attacked by obesity or hypertension 搭配不自然且语义不够准确，obesity/hypertension 不是 attack 的对象。
- 建议：可改为 They are more likely to suffer from / develop obesity or hypertension.

### #58 Step 1
- 中：这是因为人们容易被许多事物分散注意力。
- 英：This is because people are easily distracted and disturbed by many things.
- 问题：中文只说了“被许多事物分散注意力”，英文却加了“and disturbed”，多出“打扰”的意思，导致中英不对齐。
- 建议：改为 This is because people are easily distracted by many things.

### #60 Step 1
- 中：难以在现实生活中与他人有效交流。
- 英：It is difficult for them to communicate with others in real life.
- 问题：中文“有效交流”里的“有效”在英文里缺失，最后只译成 communicate with others，关键修饰信息没有译出。
- 建议：改为 It is difficult for them to communicate effectively with others in real life.

### #65 Step 1
- 中：孩子更不易变得自私，也更能体验到分享的重要性。
- 英：Children are less likely to be selfish and have more experience of sharing.
- 问题：中文“更能体验到分享的重要性”中的“重要性”在英文 “have more experience of sharing” 里丢失，语义变成“有更多分享的经历”
- 建议：改为 have a better understanding of the importance of sharing 或 are more aware of the importance of sharing

### #65 Step 2
- 中：【在这样的家庭环境中成长的】孩子更不易变得自私，也更能体验到分享的重要性。
- 英：Children who grow up in such a family are less likely to be selfish and have more experience of sharing.
- 问题：定语从句步骤里，“分享的重要性”仍未译出，finalEnglish 同样遗留该问题
- 建议：…and are more aware of the importance of sharing.

### #67 Step 1
- 中：有两个原因说明人们彼此依赖的程度更高。
- 英：There are two reasons why some people say we are more dependent on each other now.
- 问题：第一步英文多出 “some people say” 和 “now”，但该步中文（及后续步骤）都没有对应内容，属于英文超出中文；同时，全句中文的“有人认为”“当今”在英文里也没有独立步骤加入
- 建议：第一步英文改为 There are two reasons why people are more dependent on each other，或在该步中文中补出“有人认为”“当今”

### #75 Step 2
- 中：这种负面情绪即使对成年人来说也难以应对，【对年幼的孩子而言更是巨大的挑战】。
- 英：Such a negative emotion is difficult to deal with even for adults, so it is a larger challenge for young children.
- 问题：中文“即使……对年幼的孩子而言更是巨大的挑战”是让步／递进关系，英文用“so”表因果，改变了逻辑关系；且“larger”不如“even greater”贴合“更巨大”。
- 建议：改为“..., and for young children it is an even greater challenge.”或“..., while for young children it is an even bigger challenge.”

### #77 Step 1
- 中：他们很难进入学校。
- 英：It would be impossible for them to go to a school.
- 问题：中文“很难／难以”被译为“impossible（不可能）”，语气明显过强，属程度错译；且后续步骤沿用该错误。
- 建议：改为“It would be very difficult for them to go to a school.”，后续步骤相应改为“it would be very difficult for them to go to a normal school very soon”。

### #84 Step 3
- 中：【如果游客能提前制定详细计划，在一个国家最重要的节日期间前往游览】，就能更深入地体验当地文化，从而获得更加难忘的旅行体验。
- 英：If tourists make a precise plan to pay a visit to a country during its most important festivals, then they will be able to engage more in local culture and therefore have more memorable experience.
- 问题：中文“提前制定详细计划”中的“提前”，英文未译出（make a precise plan未体现in advance）
- 建议：改为make a precise plan in advance to pay a visit to...

### #86 Step 4
- 中：【随着越来越多的人选择在大城市生活和工作】，政府不得不持续建造现代化高层建筑，以满足居民和企业对更多空间的需求。
- 英：As more and more people choose to live and work in big cities, the government has to keep building modern high-rise buildings to meet the needs of more space for either residence or business.
- 问题：第4步中文改为“满足居民和企业对更多空间的需求”，但英文仍是for either residence or business（居住/商业），没有译出“居民和企业”
- 建议：改为to meet residents' and businesses' need for more space，或把中文回改为“无论是居住还是商业”

### #87 Step 2
- 中：【结论是】传统建筑的数量【逐渐】减少。
- 英：As a result, there has been a decrease in the number of traditional buildings.
- 问题：中文高亮的“逐渐”在英文中无对应（decrease只是一般现在完成，没有gradually的对应），且第3步中文也保留“逐渐”
- 建议：改为there has been a gradual decrease in the number of traditional buildings

### #97 Step 2
- 中：这些活动【对孩子们而言】绝非【只是】浪费时间。
- 英：Such activities are far from being a waste of time for the children.
- 问题：中文高亮“只是”在英文中没有对应，far from being a waste of time 只表示“绝非浪费时间”；final 中的 simply because 是“仅仅因为”，不能补足“只是”。
- 建议：改为 far from being merely/just a waste of time，或删去中文“只是”。

### #97 Step 2
- 中：这些活动【对孩子们而言】绝非【只是】浪费时间。
- 英：Such activities are far from being a waste of time for the children.
- 问题：中文/英文增加了“对孩子们而言 / for the children”，但 fullChinese 没有这一信息，final 因此多出限定对象。
- 建议：删除 for the children 与中文“对孩子们而言”，或在 fullChinese 中补出该信息。

### #100 Step 1
- 中：他们如何掌握协调能力或领悟道理？
- 英：How can they learn physical coordination or learn important social lessons?
- 问题：第1步英文已出现 physical、important、social 等修饰信息，而第1步中文没有；这些本应在第2步作为新增内容出现，导致递进不对应。
- 建议：第1步英文改为 How can they learn coordination or lessons? 或把 physical/important/social 留到第2步再加入。

### #105 Step 2
- 中：【这样一来】，没有人会产生优越感或受到歧视。
- 英：As a result, no one would feel as a sense of superiority or being prejudiced.
- 问题：第二步英文把第一步正确的 "feel a sense of superiority" 写成了 "feel as a sense of superiority"，这是语法错误，英文里多出的 as 在中文中没有对应。
- 建议：改为 As a result, no one would feel a sense of superiority or being prejudiced.

### #109 Step 2
- 中：他们可以【随心所欲地】获取任何东西，【且不受任何约束】。
- 英：They are allowed to have whatever they want regardless of price and to behave as they please.
- 问题：中文的「且不受任何约束」被译成 regardless of price（不顾价格），没有表达出「不受约束」的意思；同时 behave as they please 的「行为举止」在中文里没有，而中文的「随心所欲地获取任何东西」在英文中变成了不管价格。
- 建议：可改为 They are allowed to have whatever they want and behave as they please, without any restriction.

## LOW（22）

### #2 Step 3
- 中：例如，留学的学生不会受到思乡之情带来的困扰，【因为他们可以通过即时通讯工具与家人保持日常联系】。
- 英：For example, when some students study abroad, they would not be bothered by the problem of homesickness, as they can use instant communication tools, such as FaceTime, to talk with their families on a daily basis.
- 问题：该步英文新增“such as FaceTime”，但本步中文只写“即时通讯工具”，未标出【如FaceTime等】，新增信息在中文侧缺失。
- 建议：中文改为“……通过【如FaceTime等】即时通讯工具与家人保持日常联系”。

### #3 Step 1
- 中：人们能够建立社区。
- 英：In addition, people are able to establish a community.
- 问题：英文步骤1已含“In addition（此外）”，但该步中文未出现“此外”，且步骤2也未把它标为【新增】，中英步骤内容不对齐。
- 建议：步骤1中文改为“此外，人们能够建立社区。”，或把 In addition 移到后续步骤并在中文相应处用【】标出。

### #4 Step 2
- 中：科技能够【有效】助力【传统技能与生活方式的】传承。
- 英：Technology can positively contribute to the keeping alive of traditional skills and ways of life.
- 问题：中文“有效地”与英文 positively（积极地、正面地）语义不完全对应，属轻微改译。
- 建议：若要保留“有效”，可用 effectively；若保留 positively，中文宜写“积极地/正面地”。

### #8 Step 1
- 中：尽管如此，益处不容忽视。
- 英：In spite of this, the benefits cannot be denied.
- 问题：中文“不容忽视”与英文 cannot be denied（不容否认）语义有偏差，属教学简化但意思略有偏移。
- 建议：可改为 cannot be ignored / should not be overlooked，或中文写“不容否认”。

### #10 Step 2
- 中：因此，儿童应【尽早】学会【热情且自信地】使用【各类】设备。
- 英：Therefore, it is important that children learn at an early age to use the equipment enthusiastically and with confidence.
- 问题：中文新增“各类”设备，英文仍为“the equipment”，未体现“各类/各种”。
- 建议：可改为 to use various kinds of equipment 或 to use equipment of all kinds

### #12 Step 1
- 中：很可能会分享技术。
- 英：It is likely that our neighbours would lend us their technologies.
- 问题：步骤1 中文只有“很可能会分享技术”，英文却已出现“our neighbours”和“lend us”；而中文把“我们的太空邻居”标为步骤2 的新增内容，导致递进关系错位。
- 建议：步骤1 英文改为 It is likely that technologies would be shared，或把 our neighbours/lend us 留到步骤2 再加

### #13 Step 2
- 中：例如，【威胁生命的】疾病也能被治愈，【如果我们能通过外星友人的技术支持实现自身进步】。
- 英：For example, environmental pollution could be eradicated and life-threatening diseases could be cured if we are technologically improved by our alien friends.
- 问题：步骤2 中文删掉了前一步的“环境污染能被消除”，但英文仍保留 environmental pollution could be eradicated，中英步骤内容不一致。
- 建议：中文步骤2 补回“环境污染能被消除”，如“环境污染能被消除，威胁生命的疾病也能被治愈，如果我们……”

### #47 Step 3
- 中：这是因为担心【用于制造原子弹等大规模杀伤性武器的放射性材料纯化】技术可能会落入不法之徒手中。
- 英：This is due to the fear that the technology of purifying radioactive materials which can be used to produce powerful weapons of massive destruction may fall into wrong hands.
- 问题：“大规模杀伤性武器”的固定说法是 weapons of mass destruction，英文写成 weapons of massive destruction（且加 powerful 语义重复），与中文术语不对齐。
- 建议：改为 weapons of mass destruction（删去 powerful 或改为 lethal 等）

### #64 Step 2
- 中：【当哥哥给弟弟妹妹读睡前故事时，】父母就能自由地做自己想做的事。
- 英：When the elder brother reads bed stories to the younger ones, their parents are free to do what they want.
- 问题：“睡前故事”译成 bed stories 不符合英语习惯说法，应为 bedtime stories，与中文原意不一致。
- 建议：改为 when the elder brother reads bedtime stories to the younger ones

### #69 Step 2
- 中：年轻人【在租房或购房时】往往需要依靠父母提供经济支持。
- 英：Young adults have to rely on their parents for financial help when renting a flat or buying a house.
- 问题：中文“往往”在英文中缺失，英文仅有 have to
- 建议：改为 Young adults often have to rely on their parents for financial help when renting a flat or buying a house.

### #76 Step 2
- 中：【此外】，学习外语【也】【颇为】难度。
- 英：In addition, learning a foreign language is rather challenging.
- 问题：高亮的“也”在英文中没有对应（“In addition”只对应“此外”，kw 也未列 also）。
- 建议：可改为“In addition, learning a foreign language is also rather challenging.”

### #76 Step 2
- 中：【此外】，学习外语【也】【颇为】难度。
- 英：In addition, learning a foreign language is rather challenging.
- 问题：该步中文有笔误：“颇为难度”应为“颇具难度／颇有难度”。
- 建议：中文改为“此外，学习外语也颇具难度。”

### #77 Step 5
- 中：因此，当这些孩子抵达异国他乡后，他们很难立即进入普通学校就读，这很可能引发更多负面影响，【例如社交孤立和抑郁情绪】。
- 英：Therefore, when these children arrive in a foreign country, it would be impossible for them to go to a normal school very soon, which probably leads to more negative impacts, such as isolation and depression.
- 问题：中文“社交孤立”中的“社交”在英文“isolation”中未体现。
- 建议：改为“such as social isolation and depression”。

### #80 Step 4
- 中：然而如今，邻居们几乎不再见面交谈，【因为他们更热衷于在线分享八卦和照片】。
- 英：Today, however, neighbours barely meet and talk with each other, as they are more addicted to online sharing of gossips and pictures.
- 问题：“热衷于”译为“addicted to”，语义偏强（“上瘾／沉溺”），与中文程度不完全对齐。
- 建议：可改为“as they are more keen on sharing gossips and pictures online.”

### #81 Step 1
- 中：规划旅行至关重要。
- 英：It is important to plan a holiday trip.
- 问题：第1步英文已含holiday（假期），但第1步中文只有“规划旅行”；“假期”到第2步才出现且未标注【】，导致中英递进不对应
- 建议：第1步英文改为It is important to plan a trip，或第1步中文补上“假期”

### #88 Step 2
- 中：【学生行为不良的】首要原因是出生率【持续】下降。
- 英：The first reason for students' poor behavior is that the birth rate is decreasing.
- 问题：中文高亮的“持续”在英文中无对应（is decreasing未体现持续下降）
- 建议：改为the birth rate continues to decrease或is continuously decreasing

### #103 Step 1
- 中：要求穿校服有助于减轻压力。
- 英：Requiring students to wear uniforms helps reduce peer pressure.
- 问题：第1步中文只说“减轻压力”，英文已写成 peer pressure（同伴压力），多出“同伴”这一限定。
- 建议：第1步中文改为“同伴压力”，或英文改为 helps reduce pressure。

### #106 Step 2
- 中：【此外】，校服制度【还能】保障校园安全。
- 英：In addition, the rule of wearing school uniforms keeps the campus safe.
- 问题：第二步中文新增的高亮「还能」，在英文里没有对应增补（缺少 can also 之类的表达），并且英文与第一步完全相同，看不出递进。
- 建议：可改为 In addition, the rule of wearing school uniforms can also keep the campus safe.

### #108 Step 2
- 中：这些孩子【往往】【被过度】溺爱。
- 英：These children are often spoilt.
- 问题：第二步中文新增高亮「被过度」，但英文只有 often spoilt，没有体现「过度（excessively/over-）」这一层意思。
- 建议：可改为 These children are often excessively spoilt.

### #112 Step 2
- 中：【某些地区的】危险与荒野【环境】【对普通人而言】构成了【天然】屏障。
- 英：The danger and wilderness of some places set up a barrier for ordinary people.
- 问题：第二步中文新增高亮「天然」，但英文 The danger and wilderness of some places set up a barrier 中没有对应词（缺 natural）。
- 建议：可改为 The natural danger and wilderness of some places set up a barrier for ordinary people.

### #113 Step 2
- 中：【有些旅游目的地】【游客可能遭遇绑架或抢劫】。
- 英：There are some destinations where tourists may be kidnapped or robbed.
- 问题：本步中文新增了「旅游」，但英文只写成 some destinations，未体现「旅游」，与中文不对齐
- 建议：改为 There are some tourist destinations where tourists may be kidnapped or robbed.

### #114 Step 1
- 中：有些地方徒步旅行者极易感染疾病。
- 英：There are also places where trekkers are vulnerable to diseases.
- 问题：本步中文为「极易感染疾病」，但英文只写成 are vulnerable to diseases，没有体现「极」的程度，导致第1步与中文语义偏弱
- 建议：改为 There are also places where trekkers are highly vulnerable to diseases.

