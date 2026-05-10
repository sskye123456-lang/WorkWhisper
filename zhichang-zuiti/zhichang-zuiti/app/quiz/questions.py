"""
职场嘴替 - 22道测试题数据
"""
from app.models.user import QuizQuestion, PersonaType

# 22道测试题
QUIZ_QUESTIONS = [
    # 第1题
    QuizQuestion(
        id=1,
        scene="📱 晚上10点，同事发消息让你帮忙改个方案，明天要用。",
        question="你会怎么回？",
        options=[
            {"text": "\"好的呢，我看看哈～如果实在来不及明天一早优先弄！\"（然后默默加班到凌晨两点）", "persona": PersonaType.SHA_SENG},
            {"text": "\"这个需求今天才提，之前没排期哦。要不你跟Leader确认一下优先级？\"（打完字关掉手机，睡了）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"这个方案涉及好几个模块，我先把涉及我负责的部分梳理一下，其他部分可能需要XX配合，要不咱们拉个会对齐一下？\"（成功把锅分散到三个人头上）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "已读。放下手机。闭上眼睛。世界安静了。明天回：\"昨晚手机没电了，才看到。\"", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟喂，这么晚还干活呢？您这是要拿年度最佳员工啊！我可比不了，我脑子早下线了，明天见！\"（发完还配了个搞笑表情包）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"你白天干嘛去了？现在才想起来？自己想办法吧。\"（然后截图发朋友圈：\"有些人真是绝了\"）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第2题
    QuizQuestion(
        id=2,
        scene="开会时领导当众批评你的方案\"不够用心\"。",
        question="你的反应是？",
        options=[
            {"text": "\"是我考虑不周，我会重新做的...\"（心里委屈但不敢反驳，晚上回家偷偷哭）", "persona": PersonaType.SHA_SENG},
            {"text": "\"具体是哪些方面不够用心？可以明确说一下吗？我的产出是达标的。\"（说完全场安静了三秒）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"领导说得对，确实有改进空间。不过这个方案的背景是...，当时考虑到...，您觉得哪个方向调整比较好？\"（用了一分钟把领导绕晕了）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"好的。\"（内心OS：他说他的，我改我的，两码事。下班照样去吃火锅）", "persona": PersonaType.YU_HUA},
            {"text": "\"领导您说得对！我这就回去面壁思过！（假装抹泪）不过您看在我这么诚恳的份上，能不能给指条明路？\"（全场笑场，气氛缓和）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"您倒是说说哪里不用心？我改了三版您都不满意，您自己做一个我看看？\"（全场倒吸一口凉气）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第3题
    QuizQuestion(
        id=3,
        scene="你听说同事在背后说你\"爱表现\"\"抢功劳\"。",
        question="你的反应是？",
        options=[
            {"text": "当没听见，继续笑脸相迎，但心里很难受，开始自我怀疑：我是不是真的做错了？", "persona": PersonaType.SHA_SENG},
            {"text": "直接找对方摊牌：\"听说你在背后说我？有什么问题当面聊。\"（对方吓了一跳）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "找机会在领导面前不经意地澄清，让对方自己露出马脚。整个过程行云流水", "persona": PersonaType.ZHEN_HUAN},
            {"text": "无所谓，用业绩打脸。顺便把对方的名字记在小本本上——第48个", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，说我爱表现？那我得再表现表现，不能辜负他的期望啊！\"（然后真的在群里更活跃了）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"他也就这点本事了，自己不行还不让别人行。\"（当着其他同事的面大声说）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第4题
    QuizQuestion(
        id=4,
        scene="领导让你做一个完全不在你职责范围内的工作，而且没资源没时间。",
        question="你的反应是？",
        options=[
            {"text": "\"好的好的，我尽量...\"（然后默默加班做，一边做一边骂自己为什么不拒绝）", "persona": PersonaType.SHA_SENG},
            {"text": "\"这个不在我的职责范围内，而且目前没有资源支持。要不重新评估一下可行性？\"", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"这个工作确实重要，不过目前我的排期已经满了。要不我先把手头的工作梳理一下，您看哪个优先级更高？\"", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"做不了。\"（领导：你什么态度？你：做不了的态度。然后下班去吃烧烤了）", "persona": PersonaType.YU_HUA},
            {"text": "\"领导您太看得起我了！我这小身板哪扛得住啊！要不您给我配个助手？\"（装可怜博同情）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"这活凭什么给我？我看您是觉得我太好欺负了吧？\"（直接怼回去）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第5题
    QuizQuestion(
        id=5,
        scene="不太熟的同事问你：\"你工资多少啊？涨了多少？\"",
        question="你的回答是？",
        options=[
            {"text": "\"还好吧...就那样...也没多少...\"（不想说但不好意思拒绝，说完又后悔说多了）", "persona": PersonaType.SHA_SENG},
            {"text": "\"这个不太方便说。公司有规定的。\"（说完对方说\"哎呀我就随便问问\"，你心想那你别问）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"哎呀，也没多少，跟行业平均水平差不多吧。你呢？你们部门待遇怎么样？最近有没有什么新动态？\"（成功把话题引向八卦）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"保密。\"（两个字，结束战斗。对方愣了三秒，走了）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，别提了，够吃够喝吧！您这是要接济我吗？那我就不客气了！\"（打哈哈糊弄过去）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"关你什么事？你工资多少？你先说你再说我。\"（反将一军）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第6题
    QuizQuestion(
        id=6,
        scene="公司年会，HR让你表演节目。",
        question="你的反应是？",
        options=[
            {"text": "硬着头皮上，不想扫大家的兴。表演完获得\"最积极参与奖\"，内心OS：这辈子再也不想唱歌了", "persona": PersonaType.SHA_SENG},
            {"text": "\"我不会表演。找别人吧。\"（HR：大家都要参加的。你：那我不参加。）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"我负责后勤吧，给你们准备道具，订餐，布置场地，表演就算了哈哈\"（成功躲过表演）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "不去。年会当天请假。理由：肠胃炎。（其实在家打游戏，真香）", "persona": PersonaType.YU_HUA},
            {"text": "\"我表演可以啊！但我只会说相声，得有人给我捧哏！HR您来给我捧一个？\"（HR：算了算了）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"我又不是卖艺的，凭什么让我表演？你们怎么不表演？\"（当场拒绝）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第7题
    QuizQuestion(
        id=7,
        scene="项目出了问题，同事在群里说\"这块是XX负责的\"，把锅甩给你。",
        question="你的反应是？",
        options=[
            {"text": "\"是我没跟进好...\"（默默背锅，晚上回家偷偷哭，第二天还主动帮甩锅的同事带了杯咖啡）", "persona": PersonaType.SHA_SENG},
            {"text": "直接把邮件/聊天记录截图发群里：\"这块我上周已经确认过了，最终版本是XX调整的。@XX 你要不要补充一下？\"", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"这块确实涉及好几个环节，要不咱们拉个会对齐一下完整的流转记录？\"（开会时当着所有人的面把记录过一遍，甩锅的人当场社死）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "私下收集证据，整理成文档，抄送所有相关方。标题：《关于XX项目问题的完整时间线》。对方看完后主动辞职了", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，这锅甩得，比我奶奶烙的饼还圆！您这手艺不去杂技团可惜了！\"（群里发完还配了个鼓掌表情）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"你放屁！明明是你改的，现在赖我？要不要脸？\"（直接在群里开骂）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第8题
    QuizQuestion(
        id=8,
        scene="公司组织周末团建，占用休息时间。",
        question="你的反应是？",
        options=[
            {"text": "去，虽然不想去但不好意思拒绝。全程假笑，发的朋友圈里每张图笑容都不一样，但没有一张是真的", "persona": PersonaType.SHA_SENG},
            {"text": "\"周末有安排了，去不了。\"（其实没安排，安排就是睡觉。睡到下午两点，真爽）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"这次可能去不了，下次一定参加！\"（每次都这么说，从来没去过）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "不回消息。团建当天手机关机。周一上班领导问你怎么没去，你说\"不知道有团建\"", "persona": PersonaType.YU_HUA},
            {"text": "\"哎呀，我周末得去相亲！终身大事啊领导！您总不能拦着我脱单吧？\"（其实在家躺尸）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"周末是我的私人时间，凭什么占用？给加班费吗？\"（直接拒绝）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第9题
    QuizQuestion(
        id=9,
        scene="领导跟你说：\"好好干，年底给你涨薪/升职。\"",
        question="你的内心OS是？",
        options=[
            {"text": "\"好的领导，我会努力的！\"（信了。年底发现没涨薪。领导又说\"明年一定\"。这是你第五年信了）", "persona": PersonaType.SHA_SENG},
            {"text": "\"好的。那我们把这个写入绩效考核标准吧，方便年底评估。\"（领导愣了一下，说\"这个不用这么正式吧\"）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"谢谢领导认可！不过目前手头有几个项目，您看优先推进哪个更有利于团队目标？\"（成功把话题转移）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"嗯。\"（内心OS：饼吃多了会消化不良。你上一次吃饼是2019年，到现在还没消化完）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎呀领导，您这饼画得，我隔着屏幕都闻到香味了！那我可就等着年底吃大餐了啊！\"（表面配合，心里门儿清）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"您去年也是这么说的。我录音了，要放给您听听吗？\"（当场拆穿）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第10题
    QuizQuestion(
        id=10,
        scene="不太熟的同事找你借钱，理由是\"月底周转一下\"。",
        question="你的反应是？",
        options=[
            {"text": "借了，虽然心里不情愿。然后对方再也没提还钱的事，三个月后你发现对方朋友圈发了条新手机的开箱照", "persona": PersonaType.SHA_SENG},
            {"text": "\"最近手头也紧，不好意思。\"（直接拒绝。对方说\"就借一点点\"，你说\"一点点也没有\"）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"我回去跟我对象商量一下，回头跟你说哈。\"（然后就没有然后了）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"不借。\"（对方愣了三秒，说\"就周转一下\"。你：\"不借。\"对方走了。你继续工作）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，您太看得起我了！我月底还等着别人周转我呢！要不您先借我点？\"（反客为主）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"凭什么借你？我们很熟吗？你找银行借去啊。\"（直接怼）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第11题
    QuizQuestion(
        id=11,
        scene="17:55，领导说：\"大家留一下，开个短会。\"",
        question="你的内心OS是？",
        options=[
            {"text": "留下来开会。开完会已经19:00，默默收拾东西回家。地铁上刷到朋友圈：\"下班后的时间才是自己的生活\"。你看了看时间，19:47", "persona": PersonaType.SHA_SENG},
            {"text": "\"领导，我今晚有安排了，这个会能不能明天开？\"（领导：\"什么安排？\"你：\"私人安排。\"你走了）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"好的。不过这个会涉及XX部门，要不咱们先把相关方拉齐再开？不然可能效率不高。\"（成功把会推迟到明天）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"我18:00有安排。\"（领导：\"什么安排？\"你：\"下班。\"全场沉默。你走了）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎呀，我18点约了医生！再不去挂号就作废了！您看我这身体...\"（装病开溜）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"短会是吧？那我定个18点的闹钟，到点我就走。\"（当着全场面说）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第12题
    QuizQuestion(
        id=12,
        scene="领导布置任务时说：\"这个你看着办就行。\"",
        question="你的内心OS是？",
        options=[
            {"text": "\"好的。\"（然后焦虑一整天，不知道怎么办。做了三个版本让领导选，领导选了最差的那一个）", "persona": PersonaType.SHA_SENG},
            {"text": "\"领导，具体期望是什么？有没有参考标准？我需要明确一下再推进。\"（领导：\"就是...你看着办。\"你：\"那我需要明确的指标。\"）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"好的，我先出一个方案，到时候跟您对齐一下方向。\"（给自己留了退路。出了问题可以说\"当时对齐过\"）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "按自己的理解做。出了问题就说\"你当时说看着办\"。领导：\"我说的看着办不是这个办。\"你：\"你没说不能这么办。\"", "persona": PersonaType.YU_HUA},
            {"text": "\"好嘞！那我就按我的想法来了！到时候您别嫌弃啊！\"（先打预防针，给自己留余地）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"看着办是什么意思？您说清楚，不然我不做。\"（当场要求明确）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第13题
    QuizQuestion(
        id=13,
        scene="同事说：\"哎呀，你今天又准时下班啊，真羡慕你工作轻松。\"",
        question="你的回应是？",
        options=[
            {"text": "\"没有没有，我还有好多没做完呢...\"（尴尬地笑，然后假装很忙地留下来加班）", "persona": PersonaType.SHA_SENG},
            {"text": "\"工作做完了就下班，这有什么问题吗？\"（同事被噎住了）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"哈哈，今天确实顺利。对了，你那个项目进展怎么样了？我看你最近天天加班，挺辛苦的，领导知道吗？\"（成功转移话题）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"嗯。\"（走了。留下同事一个人站在原地，对着空气完成了他的表演）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，您这是夸我呢还是损我呢？我脑子笨，听不出来，您直说呗！\"（装傻充愣）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"是啊，我效率高，不像某些人，加班是因为白天摸鱼。\"（当场反击）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第14题
    QuizQuestion(
        id=14,
        scene="同事发来一个50页的PPT，说：\"你有空帮我看看呗，提提意见。\"",
        question="你的反应是？",
        options=[
            {"text": "\"好的好的，我看看哈...\"（然后花了一下午看，自己的活没干完。同事说\"还是原来的好\"。你：血压180）", "persona": PersonaType.SHA_SENG},
            {"text": "\"这个工作量比较大，我目前排期比较满。要不你先列出具体想让我看哪些部分？\"", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"好的，我抽空看看。不过最近手头项目比较紧，可能要下周才能给你反馈，你着急吗？\"（把时间线拉长到下周）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "\"没空。\"（对方：\"就帮忙看一下嘛。\"你：\"没空。\"对方：\"很快的。\"你：\"没空。\"）", "persona": PersonaType.YU_HUA},
            {"text": "\"50页？您这是要让我写读后感啊！要不您先给我讲讲重点，我听听就行？\"（讨价还价）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"你自己的活凭什么让我看？我又不是你助理。\"（直接拒绝）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第15题
    QuizQuestion(
        id=15,
        scene="开会时领导问：\"大家对这个方案有没有意见？\"",
        question="你的反应是？",
        options=[
            {"text": "\"没有没有，挺好的。\"（心里有一堆意见，但一个字都没说。散会后跟同事吐槽了半小时）", "persona": PersonaType.SHA_SENG},
            {"text": "有意见就直说。说完领导脸色不太好看，但你说的确实有道理。其他同事在心里给你鼓掌", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"整体方向挺好的。我有几个小问题想请教一下...\"（先肯定再提问，问题包装成\"请教\"。领导觉得你在认真学习，其实你在质疑他）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "沉默。全场沉默。领导说\"那没有意见就散会\"。你站起来第一个走了", "persona": PersonaType.YU_HUA},
            {"text": "\"领导您这方案太完美了！我哪敢有意见啊！我就是来学习学习的！\"（拍马屁糊弄过去）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"有。这个预算不合理、这个时间线不现实、这个需求是拍脑袋定的。\"（当场指出所有问题）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第16题 - 终极灵魂拷问
    QuizQuestion(
        id=16,
        scene="深夜11点，你一个人坐在工位上。窗外是城市的灯火，桌上是凉了的外卖。手机亮了，是妈妈发来的消息：\"在忙吗？记得吃饭。\"\n\n你看着这条消息，又看了看电脑上还没做完的方案，突然开始思考一个哲学问题：\n\n\"我这辈子，到底在图什么？\"",
        question="你的反应是？",
        options=[
            {"text": "回复妈妈：\"在忙呢，吃了吃了放心吧😊\"然后放下手机，继续加班。眼泪掉在键盘上，你擦了擦，怕把电脑弄坏了赔不起", "persona": PersonaType.SHA_SENG},
            {"text": "回复妈妈：\"刚下班。这个破班我迟早不上了。\"然后关掉电脑，收拾东西回家。第二天准时上班，继续上这个破班", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "回复妈妈：\"在忙呢，最近项目比较多。对了妈，你上次说想买那个什么来着？我给你看看。\"成功把话题转移", "persona": PersonaType.ZHEN_HUAN},
            {"text": "看了一眼消息。没有回复。关掉手机。关掉电脑。关掉灯。第二天早上8:59打卡，一秒不差", "persona": PersonaType.YU_HUA},
            {"text": "回复妈妈：\"妈！您这消息来得太及时了！我正饿着呢！您给我转点钱点外卖呗？\"（撒娇卖萌）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "回复妈妈：\"在加班，这破公司天天压榨我，我迟早辞职。\"（直接吐槽）", "persona": PersonaType.XIAO_S},
        ],
    ),
    # 第17题 - 鬼畜场景：便秘题
    QuizQuestion(
        id=17,
        scene="🚽 你因便秘坐在马桶上（已长达30分钟），拉不出很难受。",
        question="此时你更像？",
        options=[
            {"text": "再坐三十分钟看看，说不定就有了。（忍一忍就过去了，就像职场里的委屈一样）", "persona": PersonaType.SHA_SENG},
            {"text": "用力拍打自己的屁股并说：\"死屁股，快拉啊！\"（跟自己的身体硬刚，就像跟职场PUA硬刚一样）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "使用开塞露，快点拉出来才好。（找到工具解决问题，就像用话术解决职场难题一样）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "算了，不拉了。提裤子走人。明天再说。（解决不了就放弃，反正活着就行）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟喂，我这肚子跟我作对呢！您倒是给点面子啊！\"（跟自己的肚子对话，像说相声一样）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"这破肚子，关键时刻掉链子！\"（骂骂咧咧地站起来，然后发朋友圈吐槽）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="便秘",
    ),
    # 第18题 - 鬼畜场景：外卖迟到
    QuizQuestion(
        id=18,
        scene="🍱 你点的午饭，预计12点送达，现在12:45了，外卖还没来，你饿得前胸贴后背。",
        question="此时你？",
        options=[
            {"text": "算了，再等等吧，外卖小哥也不容易。（继续饿着，默默忍受）", "persona": PersonaType.SHA_SENG},
            {"text": "直接打电话催：\"我的外卖什么时候到？已经超时45分钟了！\"（态度强硬）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "先给商家打电话：\"你们家出餐是不是有问题？\"再给骑手打电话：\"是不是订单太多？\"成功搞清楚是谁的锅", "persona": PersonaType.ZHEN_HUAN},
            {"text": "取消订单，下楼吃。不饿了，气饱了。（不纠结，直接换方案）", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟，我的饭啊！你是不是迷路了？要不要我给你导航？\"（给骑手发搞笑语音）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"什么破服务！我要投诉！\"（直接给差评，然后发朋友圈骂）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="外卖迟到",
    ),
    # 第19题 - 鬼畜场景：地铁被踩
    QuizQuestion(
        id=19,
        scene="👟 早高峰地铁上，你的白鞋被旁边的人狠狠踩了一脚，对方看了你一眼，没道歉，继续玩手机。",
        question="你的反应是？",
        options=[
            {"text": "算了，地铁上挤，也不是故意的。（自己默默心疼鞋，不敢出声）", "persona": PersonaType.SHA_SENG},
            {"text": "\"你踩到我了。\"（盯着对方，直到对方道歉）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"哎呀，没事没事，地铁是挺挤的。\"（表面大度，但声音大到让周围人都听见，让对方尴尬）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "看了对方一眼，没说话。心里默念：算了，不值得为这种事生气。然后继续听歌", "persona": PersonaType.YU_HUA},
            {"text": "\"哎哟！我的鞋！您这一脚下去，我的鞋都喊疼了！\"（夸张地叫，逗笑周围人）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"你瞎啊？踩了人不道歉？\"（当场开骂）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="地铁被踩",
    ),
    # 第20题 - 鬼畜场景：理发翻车
    QuizQuestion(
        id=20,
        scene="💇 你去理发店，跟Tony老师说\"稍微修一下\"，结果他给你剪了个超级短的头发，你看着镜子里的自己，像颗卤蛋。",
        question="你的反应是？",
        options=[
            {"text": "\"还好吧...也还行...\"（心里在滴血，但不好意思表现出来，还给了Tony好评）", "persona": PersonaType.SHA_SENG},
            {"text": "\"这跟我说的不一样吧？我说的是稍微修一下，不是剃光。\"（当场要求说法）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "\"这个发型...挺特别的。不过我觉得可能不太适合我，能不能再调整一下？\"（委婉表达不满，但给对方台阶）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "看着镜子里的卤蛋，笑了。然后拍照发朋友圈：\"新造型，请叫我卤蛋侠。\"（自嘲化解尴尬）", "persona": PersonaType.YU_HUA},
            {"text": "\"Tony老师，您这是要让我出道啊！这发型，我明天就能去演喜剧了！\"（自嘲+调侃）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"你会不会剪啊？这什么鬼东西！赔钱！\"（当场发飙）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="理发翻车",
    ),
    # 第21题 - 鬼畜场景：手机没电
    QuizQuestion(
        id=21,
        scene="🔋 你在外面办事，手机只剩5%的电，而你现在还找不到地方充电，接下来还有重要的电话要打。",
        question="你的反应是？",
        options=[
            {"text": "赶紧把该发的消息发了，然后关机，希望能撑到回家。（焦虑但没办法）", "persona": PersonaType.SHA_SENG},
            {"text": "直接找附近的店：\"能不能借我充个电？我付钱。\"（主动解决问题）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "先给重要的人发消息：\"我手机快没电了，有事留言，我找到充电器就回。\"（提前告知，管理预期）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "算了，没电就没电吧。正好清静一下。（关机，享受没有手机的时光）", "persona": PersonaType.YU_HUA},
            {"text": "\"手机啊手机，你再坚持一下！回去给你吃大餐！\"（跟手机对话，像哄孩子一样）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "\"这破手机，关键时刻掉链子！\"（骂骂咧咧，然后发朋友圈吐槽）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="手机没电",
    ),
    # 第22题 - 终极选择：荒岛
    QuizQuestion(
        id=22,
        scene="🏝️ 假设你要去荒岛生存一年，只能带一样东西。",
        question="你会带？",
        options=[
            {"text": "一本《如何与人相处》的书。（怕孤独，怕没人喜欢自己）", "persona": PersonaType.SHA_SENG},
            {"text": "一把刀。（有刀就有主动权，谁敢欺负我就跟谁拼命）", "persona": PersonaType.HANZAWA_NAOKI},
            {"text": "一部卫星电话。（可以联系外界，随时求援，永远有退路）", "persona": PersonaType.ZHEN_HUAN},
            {"text": "一本空白笔记本。（记录生活，自己跟自己对话，不依赖外界）", "persona": PersonaType.YU_HUA},
            {"text": "一副扑克牌。（一个人也能玩，还能跟自己说话，不无聊）", "persona": PersonaType.YUE_YUNPENG},
            {"text": "一个录音笔。（记录下所有的不满，回去之后慢慢算账）", "persona": PersonaType.XIAO_S},
        ],
        is_ghost=True,
        ghost_theme="荒岛选择",
    ),
]


def get_question(question_id: int) -> QuizQuestion:
    """获取指定题目"""
    if 1 <= question_id <= len(QUIZ_QUESTIONS):
        return QUIZ_QUESTIONS[question_id - 1]
    return None


def calculate_persona_scores(answers: list) -> dict:
    """根据答案计算人设得分"""
    from app.models.user import PersonaType
    
    scores = {p: 0 for p in PersonaType}
    
    for i, answer in enumerate(answers):
        if i >= len(QUIZ_QUESTIONS):
            break
        
        question = QUIZ_QUESTIONS[i]
        for option in question.options:
            if option["text"].startswith(answer) or answer in option["text"]:
                persona = option["persona"]
                if persona in scores:
                    scores[persona] += 1
                break
    
    return scores


def get_dominant_persona(scores: dict) -> PersonaType:
    """获取主导人设"""
    if not scores:
        return PersonaType.SHA_SENG
    
    max_score = max(scores.values())
    dominant = [p for p, s in scores.items() if s == max_score]
    
    # 如果有并列，按优先级返回
    priority = [
        PersonaType.HANZAWA_NAOKI,
        PersonaType.ZHEN_HUAN,
        PersonaType.YU_HUA,
        PersonaType.YUE_YUNPENG,
        PersonaType.XIAO_S,
        PersonaType.SHA_SENG,
    ]
    
    for p in priority:
        if p in dominant:
            return p
    
    return dominant[0]
