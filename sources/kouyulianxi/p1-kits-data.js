// P1 life-material bank (composable; switcher reads .kits)
const P1_KITS_DATA = {
  "kits": [
    {
      "id": "campus_tee_coat",
      "nameZh": "T恤外套穿搭",
      "summary": "PDF衣：t-shirt / coat / sweatshirt；出门 get dressed。",
      "kind": "衣·穿戴"
    },
    {
      "id": "hallway_mirror_routine",
      "nameZh": "出门照镜子",
      "summary": "PDF日常：look at myself in the mirror / get dressed / head out。",
      "kind": "衣·习惯"
    },
    {
      "id": "campus_sweatshirt",
      "nameZh": "卫衣外套",
      "summary": "PDF衣：sweatshirt / coat；冷天校园穿。",
      "kind": "衣·穿戴"
    },
    {
      "id": "campus_sneakers",
      "nameZh": "舒适球鞋",
      "summary": "校园走路/通勤；舒适优先于款式。",
      "kind": "衣·鞋子"
    },
    {
      "id": "style_shoes_weekend",
      "nameZh": "周末好看的鞋",
      "summary": "平时球鞋，周末偶尔穿更有型的鞋。",
      "kind": "衣·鞋子"
    },
    {
      "id": "dressing_mirror_home",
      "nameZh": "房间穿衣镜",
      "summary": "宿舍/租房里的穿衣镜；出门前整理。",
      "kind": "衣·习惯"
    },
    {
      "id": "canteen_and_takeaways",
      "nameZh": "食堂与外卖",
      "summary": "PDF食：breakfast / the school canteen / takeaways / street food。",
      "kind": "食·日常"
    },
    {
      "id": "fruit_groceries",
      "nameZh": "水果生鲜",
      "summary": "PDF食：groceries / food ingredients；水果维生素。",
      "kind": "食·蔬果"
    },
    {
      "id": "dorm_apartment_life",
      "nameZh": "宿舍租房生活",
      "summary": "PDF住：dorms / renting an apartment / residential areas。",
      "kind": "住·居所"
    },
    {
      "id": "tidy_desk_habit",
      "nameZh": "书桌收纳",
      "summary": "宿舍书桌收拾；方便学习。",
      "kind": "住·整洁"
    },
    {
      "id": "parents_tidy_home",
      "nameZh": "父母整理房间",
      "summary": "童年父母整理；整洁题第二套。",
      "kind": "住·整洁"
    },
    {
      "id": "recycle_bins_floor",
      "nameZh": "楼层垃圾分类",
      "summary": "纸壳塑料分开扔；宿舍楼层分类桶。",
      "kind": "住·环保"
    },
    {
      "id": "subway_bus_commute",
      "nameZh": "地铁公交通勤",
      "summary": "PDF行：use the subway / take a bus；rush hour。",
      "kind": "行·出行"
    },
    {
      "id": "family_car_passenger",
      "nameZh": "全家开车出行",
      "summary": "PDF行：drive a car；假期当乘客。",
      "kind": "行·汽车"
    },
    {
      "id": "yellow_bike_gift",
      "nameZh": "黄色小自行车",
      "summary": "可控 Freestyle 核心套装：童年新活动/开学日/公园/疲倦放松/出行；不挂名字折纸拾金。",
      "kind": "行·单车"
    },
    {
      "id": "nearby_park_walk",
      "nameZh": "附近公园散步",
      "summary": "PDF地点：park；万能句 10mins walk。",
      "kind": "地点·公园"
    },
    {
      "id": "mall_street_market",
      "nameZh": "商超与街市",
      "summary": "PDF：shopping malls / street market / pay with my phone。",
      "kind": "地点·购物"
    },
    {
      "id": "study_library_classes",
      "nameZh": "上课与图书馆",
      "summary": "PDF：go to classes / study / library / flip through real books。",
      "kind": "行为·学习"
    },
    {
      "id": "business_major_path",
      "nameZh": "商科专业日常",
      "summary": "学生线：business major + classes + future job。",
      "kind": "行为·学习"
    },
    {
      "id": "handwritten_notes_paper",
      "nameZh": "手写纸质笔记",
      "summary": "PDF：flip through the pages of real books / paper notes。",
      "kind": "行为·学习"
    },
    {
      "id": "phone_xiaohongshu_wechat",
      "nameZh": "手机刷短视频微信",
      "summary": "PDF：douyin / xiaohongshu / wechat / browse videos / shop online。",
      "kind": "行为·媒介"
    },
    {
      "id": "douyin_scroll_habit",
      "nameZh": "刷抖音短视频",
      "summary": "PDF：browse videos / obsessed with short videos。",
      "kind": "行为·媒介"
    },
    {
      "id": "study_websites_search",
      "nameZh": "查资料网站",
      "summary": "PDF学习+网站：search / study resources。",
      "kind": "行为·学习"
    },
    {
      "id": "wireless_earbuds_music",
      "nameZh": "耳机听歌",
      "summary": "PDF：listen to music / headphones；地铁降噪。",
      "kind": "爱好·音乐"
    },
    {
      "id": "focus_wired_headphones",
      "nameZh": "有线耳机专注",
      "summary": "图书馆有线耳机；耳机题第二套，偏专注学习。",
      "kind": "爱好·音乐"
    },
    {
      "id": "school_choir_songs",
      "nameZh": "学校课堂歌曲",
      "summary": "童年课堂歌；唱歌题第二套。",
      "kind": "爱好·唱歌"
    },
    {
      "id": "singing_ktv_songs",
      "nameZh": "唱歌KTV",
      "summary": "PDF：sing a song；童年儿歌到KTV。",
      "kind": "爱好·唱歌"
    },
    {
      "id": "comedy_hang_out",
      "nameZh": "看喜剧和朋友玩",
      "summary": "PDF：watch movies / hang out / enjoy a good laugh。",
      "kind": "爱好·娱乐"
    },
    {
      "id": "light_sports_walk",
      "nameZh": "散步慢跑运动",
      "summary": "PDF运动：go for a walk / go jogging / do some sports / gym。",
      "kind": "爱好·运动"
    },
    {
      "id": "patient_teacher_help",
      "nameZh": "耐心的老师",
      "summary": "PDF：explain concepts / mutually motivate；老师帮助。",
      "kind": "社交·学习"
    },
    {
      "id": "polite_thank_you",
      "nameZh": "说谢谢有礼貌",
      "summary": "家人教导；开门食堂说谢谢。",
      "kind": "社交·礼貌"
    },
    {
      "id": "simple_watch_gift",
      "nameZh": "普通手表礼物",
      "summary": "开学礼物；看时间不用掏手机。",
      "kind": "物品·手表"
    },
    {
      "id": "phone_time_check",
      "nameZh": "手机看时间",
      "summary": "不戴表时用手机看时间；手表题第二套。",
      "kind": "物品·手表"
    },
    {
      "id": "campus_opportunity_notice",
      "nameZh": "校园机会通知",
      "summary": "老师/班级群/实习帖；机会题主素材。",
      "kind": "学习·机会"
    },
    {
      "id": "subway_screen_ads",
      "nameZh": "地铁广告屏",
      "summary": "通勤刷到屏幕广告；有的抓眼有的烦人。",
      "kind": "媒介·广告"
    },
    {
      "id": "school_science_lab",
      "nameZh": "学校科学实验课",
      "summary": "课堂实验、生物兴趣；勿硬套航天纪录片。",
      "kind": "学习·科学"
    },
    {
      "id": "daily_tech_science",
      "nameZh": "日常科技与科学",
      "summary": "手机地图、地铁系统等出行里的科学应用。",
      "kind": "生活·科学"
    },
    {
      "id": "weather_search_tools",
      "nameZh": "天气搜索与在线工具",
      "summary": "查天气、搜索引擎、在线课；家里常用的科学小工具。",
      "kind": "生活·科学"
    },
    {
      "id": "space_docs_night",
      "nameZh": "夜里看航天纪录片",
      "summary": "航天/星空纪录片；仅挂太空与科学节目类题。",
      "kind": "爱好·科普"
    },
    {
      "id": "hometown_local_food",
      "nameZh": "家乡本地小吃",
      "summary": "PDF：street food / local food；记忆与情感。",
      "kind": "食·家乡"
    },
    {
      "id": "name_parents_choice",
      "nameZh": "父母取的名字",
      "summary": "名字含义；父母选择。",
      "kind": "社交·名字"
    },
    {
      "id": "name_nickname_school",
      "nameZh": "学校短昵称",
      "summary": "同学昵称；名字话题第二套。",
      "kind": "社交·名字"
    }
  ],
  "materials": [
    {
      "id": "campus_tee_coat",
      "nameZh": "T恤外套穿搭",
      "kind": "衣·穿戴",
      "module": "衣食住行",
      "summary": "PDF衣：t-shirt / coat / sweatshirt；出门 get dressed。",
      "topics": [
        "clothing"
      ]
    },
    {
      "id": "hallway_mirror_routine",
      "nameZh": "出门照镜子",
      "kind": "衣·习惯",
      "module": "衣食住行",
      "summary": "PDF日常：look at myself in the mirror / get dressed / head out。",
      "topics": [
        "mirrors"
      ]
    },
    {
      "id": "campus_sweatshirt",
      "nameZh": "卫衣外套",
      "kind": "衣·穿戴",
      "module": "衣食住行",
      "summary": "PDF衣：sweatshirt / coat；冷天校园穿。",
      "topics": [
        "clothing"
      ]
    },
    {
      "id": "campus_sneakers",
      "nameZh": "舒适球鞋",
      "kind": "衣·鞋子",
      "module": "衣食住行",
      "summary": "校园走路/通勤；舒适优先于款式。",
      "topics": [
        "shoes"
      ]
    },
    {
      "id": "style_shoes_weekend",
      "nameZh": "周末好看的鞋",
      "kind": "衣·鞋子",
      "module": "衣食住行",
      "summary": "平时球鞋，周末偶尔穿更有型的鞋。",
      "topics": [
        "shoes",
        "shopping"
      ]
    },
    {
      "id": "dressing_mirror_home",
      "nameZh": "房间穿衣镜",
      "kind": "衣·习惯",
      "module": "衣食住行",
      "summary": "宿舍/租房里的穿衣镜；出门前整理。",
      "topics": [
        "mirrors",
        "clothing"
      ]
    },
    {
      "id": "canteen_and_takeaways",
      "nameZh": "食堂与外卖",
      "kind": "食·日常",
      "module": "衣食住行",
      "summary": "PDF食：breakfast / the school canteen / takeaways / street food。",
      "topics": [
        "fruit and vegetables",
        "hometown"
      ]
    },
    {
      "id": "fruit_groceries",
      "nameZh": "水果生鲜",
      "kind": "食·蔬果",
      "module": "衣食住行",
      "summary": "PDF食：groceries / food ingredients；水果维生素。",
      "topics": [
        "fruit and vegetables",
        "shopping",
        "street markets"
      ]
    },
    {
      "id": "dorm_apartment_life",
      "nameZh": "宿舍租房生活",
      "kind": "住·居所",
      "module": "衣食住行",
      "summary": "PDF住：dorms / renting an apartment / residential areas。",
      "topics": [
        "home & accommodation",
        "the area you live in",
        "tidiness",
        "the city you live in"
      ]
    },
    {
      "id": "tidy_desk_habit",
      "nameZh": "书桌收纳",
      "kind": "住·整洁",
      "module": "衣食住行",
      "summary": "宿舍书桌收拾；方便学习。",
      "topics": [
        "tidiness",
        "home & accommodation"
      ]
    },
    {
      "id": "parents_tidy_home",
      "nameZh": "父母整理房间",
      "kind": "住·整洁",
      "module": "衣食住行",
      "summary": "童年父母整理；整洁题第二套。",
      "topics": [
        "tidiness",
        "home & accommodation"
      ]
    },
    {
      "id": "recycle_bins_floor",
      "nameZh": "楼层垃圾分类",
      "kind": "住·环保",
      "module": "衣食住行",
      "summary": "纸壳塑料分开扔；宿舍楼层分类桶。",
      "topics": [
        "rubbish and recycling",
        "paper"
      ]
    },
    {
      "id": "subway_bus_commute",
      "nameZh": "地铁公交通勤",
      "kind": "行·出行",
      "module": "衣食住行",
      "summary": "PDF行：use the subway / take a bus；rush hour。",
      "topics": [
        "the city you live in",
        "the area you live in",
        "travelling",
        "cars"
      ]
    },
    {
      "id": "family_car_passenger",
      "nameZh": "全家开车出行",
      "kind": "行·汽车",
      "module": "衣食住行",
      "summary": "PDF行：drive a car；假期当乘客。",
      "topics": [
        "cars",
        "travelling",
        "hometown"
      ]
    },
    {
      "id": "yellow_bike_gift",
      "nameZh": "黄色小自行车",
      "kind": "行·单车",
      "module": "衣食住行",
      "summary": "可控 Freestyle 核心套装：童年新活动/开学日/公园/疲倦放松/出行；不挂名字折纸拾金。",
      "topics": [
        "opportunities",
        "secondary school",
        "public gardens and parks",
        "tiredness",
        "travelling",
        "feeling bored"
      ]
    },
    {
      "id": "nearby_park_walk",
      "nameZh": "附近公园散步",
      "kind": "地点·公园",
      "module": "衣食住行",
      "summary": "PDF地点：park；万能句 10mins walk。",
      "topics": [
        "public gardens and parks",
        "feeling bored",
        "tiredness",
        "the area you live in",
        "the city you live in"
      ]
    },
    {
      "id": "mall_street_market",
      "nameZh": "商超与街市",
      "kind": "地点·购物",
      "module": "衣食住行",
      "summary": "PDF：shopping malls / street market / pay with my phone。",
      "topics": [
        "shopping",
        "street markets",
        "fruit and vegetables"
      ]
    },
    {
      "id": "study_library_classes",
      "nameZh": "上课与图书馆",
      "kind": "行为·学习",
      "module": "高频行为",
      "summary": "PDF：go to classes / study / library / flip through real books。",
      "topics": [
        "work or studies",
        "secondary school",
        "teachers"
      ]
    },
    {
      "id": "business_major_path",
      "nameZh": "商科专业日常",
      "kind": "行为·学习",
      "module": "高频行为",
      "summary": "学生线：business major + classes + future job。",
      "topics": [
        "work or studies",
        "opportunities"
      ]
    },
    {
      "id": "handwritten_notes_paper",
      "nameZh": "手写纸质笔记",
      "kind": "行为·学习",
      "module": "高频行为",
      "summary": "PDF：flip through the pages of real books / paper notes。",
      "topics": [
        "paper",
        "secondary school",
        "rubbish and recycling"
      ]
    },
    {
      "id": "phone_xiaohongshu_wechat",
      "nameZh": "手机刷短视频微信",
      "kind": "行为·媒介",
      "module": "高频行为",
      "summary": "PDF：douyin / xiaohongshu / wechat / browse videos / shop online。",
      "topics": [
        "social media",
        "websites",
        "advertisements",
        "opportunities"
      ]
    },
    {
      "id": "douyin_scroll_habit",
      "nameZh": "刷抖音短视频",
      "kind": "行为·媒介",
      "module": "高频行为",
      "summary": "PDF：browse videos / obsessed with short videos。",
      "topics": [
        "social media",
        "feeling bored",
        "jokes & comedies"
      ]
    },
    {
      "id": "study_websites_search",
      "nameZh": "查资料网站",
      "kind": "行为·学习",
      "module": "高频行为",
      "summary": "PDF学习+网站：search / study resources。",
      "topics": [
        "websites",
        "opportunities"
      ]
    },
    {
      "id": "wireless_earbuds_music",
      "nameZh": "耳机听歌",
      "kind": "爱好·音乐",
      "module": "高频行为",
      "summary": "PDF：listen to music / headphones；地铁降噪。",
      "topics": [
        "headphones",
        "music",
        "travelling",
        "tiredness"
      ]
    },
    {
      "id": "focus_wired_headphones",
      "nameZh": "有线耳机专注",
      "kind": "爱好·音乐",
      "module": "高频行为",
      "summary": "图书馆有线耳机；耳机题第二套，偏专注学习。",
      "topics": [
        "headphones",
        "music"
      ]
    },
    {
      "id": "school_choir_songs",
      "nameZh": "学校课堂歌曲",
      "kind": "爱好·唱歌",
      "module": "高频行为",
      "summary": "童年课堂歌；唱歌题第二套。",
      "topics": [
        "singing",
        "secondary school",
        "music"
      ]
    },
    {
      "id": "singing_ktv_songs",
      "nameZh": "唱歌KTV",
      "kind": "爱好·唱歌",
      "module": "高频行为",
      "summary": "PDF：sing a song；童年儿歌到KTV。",
      "topics": [
        "singing",
        "music",
        "feeling bored"
      ]
    },
    {
      "id": "comedy_hang_out",
      "nameZh": "看喜剧和朋友玩",
      "kind": "爱好·娱乐",
      "module": "高频行为",
      "summary": "PDF：watch movies / hang out / enjoy a good laugh。",
      "topics": [
        "jokes & comedies",
        "feeling bored",
        "social media"
      ]
    },
    {
      "id": "light_sports_walk",
      "nameZh": "散步慢跑运动",
      "kind": "爱好·运动",
      "module": "高频行为",
      "summary": "PDF运动：go for a walk / go jogging / do some sports / gym。",
      "topics": [
        "tiredness",
        "public gardens and parks",
        "feeling bored"
      ]
    },
    {
      "id": "patient_teacher_help",
      "nameZh": "耐心的老师",
      "kind": "社交·学习",
      "module": "高频行为",
      "summary": "PDF：explain concepts / mutually motivate；老师帮助。",
      "topics": [
        "teachers",
        "secondary school",
        "politeness"
      ]
    },
    {
      "id": "polite_thank_you",
      "nameZh": "说谢谢有礼貌",
      "kind": "社交·礼貌",
      "module": "高频行为",
      "summary": "家人教导；开门食堂说谢谢。",
      "topics": [
        "politeness"
      ]
    },
    {
      "id": "simple_watch_gift",
      "nameZh": "普通手表礼物",
      "kind": "物品·手表",
      "module": "衣食住行",
      "summary": "开学礼物；看时间不用掏手机。",
      "topics": [
        "watch"
      ]
    },
    {
      "id": "phone_time_check",
      "nameZh": "手机看时间",
      "kind": "物品·手表",
      "module": "高频行为",
      "summary": "不戴表时用手机看时间；手表题第二套。",
      "topics": [
        "watch"
      ]
    },
    {
      "id": "campus_opportunity_notice",
      "nameZh": "校园机会通知",
      "kind": "学习·机会",
      "module": "学习工作",
      "summary": "老师/班级群/实习帖；机会题主素材。",
      "topics": [
        "opportunities",
        "social media"
      ]
    },
    {
      "id": "subway_screen_ads",
      "nameZh": "地铁广告屏",
      "kind": "媒介·广告",
      "module": "高频行为",
      "summary": "通勤刷到屏幕广告；有的抓眼有的烦人。",
      "topics": [
        "advertisements",
        "the city you live in",
        "travelling"
      ]
    },
    {
      "id": "school_science_lab",
      "nameZh": "学校科学实验课",
      "kind": "学习·科学",
      "module": "学习工作",
      "summary": "课堂实验、生物兴趣；勿硬套航天纪录片。",
      "topics": [
        "science",
        "secondary school",
        "outer space and stars"
      ]
    },
    {
      "id": "daily_tech_science",
      "nameZh": "日常科技与科学",
      "kind": "生活·科学",
      "module": "高频行为",
      "summary": "手机地图、地铁系统等出行里的科学应用。",
      "topics": [
        "science"
      ]
    },
    {
      "id": "weather_search_tools",
      "nameZh": "天气搜索与在线工具",
      "kind": "生活·科学",
      "module": "高频行为",
      "summary": "查天气、搜索引擎、在线课；家里常用的科学小工具。",
      "topics": [
        "science"
      ]
    },
    {
      "id": "space_docs_night",
      "nameZh": "夜里看航天纪录片",
      "kind": "爱好·科普",
      "module": "高频行为",
      "summary": "航天/星空纪录片；仅挂太空与科学节目类题。",
      "topics": [
        "outer space and stars",
        "science",
        "feeling bored"
      ]
    },
    {
      "id": "hometown_local_food",
      "nameZh": "家乡本地小吃",
      "kind": "食·家乡",
      "module": "衣食住行",
      "summary": "PDF：street food / local food；记忆与情感。",
      "topics": [
        "hometown",
        "street markets",
        "fruit and vegetables",
        "cars",
        "travelling"
      ]
    },
    {
      "id": "name_parents_choice",
      "nameZh": "父母取的名字",
      "kind": "社交·名字",
      "module": "高频行为",
      "summary": "名字含义；父母选择。",
      "topics": [
        "name"
      ]
    },
    {
      "id": "name_nickname_school",
      "nameZh": "学校短昵称",
      "kind": "社交·名字",
      "module": "高频行为",
      "summary": "同学昵称；名字话题第二套。",
      "topics": [
        "name",
        "secondary school",
        "politeness"
      ]
    }
  ]
};

if (typeof window !== 'undefined') {
  window.P1_KITS_DATA = P1_KITS_DATA;
}
