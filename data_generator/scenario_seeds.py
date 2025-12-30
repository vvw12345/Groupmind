"""
场景种子库 - 预定义的多样化场景方向
每个场景包含：
- scene: 场景的核心定义（人物和场所）
- core_atmospheres: 核心适配氛围（最常见、最合理的氛围）
- optional_atmospheres: 可选氛围（可以使用但不是最典型的）
- 未列出的氛围将被排除（不合理的组合）
"""

# 氛围类型定义
ATMOSPHERES = [
    "合作",      # 多方协同工作，共同目标
    "对抗",      # 明确的对立关系，利益冲突
    "劝说",      # 一方试图说服另一方
    "迁就",      # 一方妥协退让以维持关系
    "同盟",      # 结成联盟，共同对抗第三方
    "排斥",      # 排挤、孤立某一方
    "支持",      # 给予帮助和鼓励
    "冲突",      # 激烈的矛盾和争执
    "妥协",      # 各方让步达成平衡
    "领导服从",  # 明确的上下级或权威关系
]

SCENARIO_SEEDS = [
    # 艺术与创作类
    {
        "scene": "一场地下先锋艺术展的开幕酒会，策展人、艺术家、评论家和神秘买家",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "同盟", "劝说"],
        "optional_atmospheres": ["合作", "支持","妥协"],
    },
    {
        "scene": "一个独立纪录片首映礼，导演、被拍摄对象和观众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "冲突", "对抗"],
        "optional_atmospheres": ["劝说", "妥协"],
    },
    {
        "scene": "一场拍卖会的预展现场，几位竞拍者",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "同盟", "排斥"],
        "optional_atmospheres": ["合作", "妥协"],
    },
    {
        "scene": "一个音乐节后台的化妆间，不同风格的乐队成员",
        "category": "创意表达",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场行为艺术表演现场，艺术家、观众和保安",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "对抗", "劝说"],
        "optional_atmospheres": ["支持", "妥协"],
    },
    {
        "scene": "一个画廊开幕式，艺术家本人隐藏身份混入人群",
        "category": "创意表达",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["劝说", "合作"],
    },
    {
        "scene": "一场街头涂鸦创作，几位涂鸦艺术家、城管和路人",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "劝说"],
        "optional_atmospheres": ["支持", "妥协"],
    },
    {
        "scene": "一个雕塑工作室的开放日，雕塑家和访客",
        "category": "创意表达",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一场实验戏剧的排练场，导演、演员和编剧",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "领导服从"],
    },
    {
        "scene": "一个摄影暗房，几位摄影师讨论冲洗技巧",
        "category": "创意表达",
        "core_atmospheres": ["合作", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    
    # 科研与学术类
    {
        "scene": "一个深夜的实验室，几位科研人员",
        "category": "专业决策",
        "core_atmospheres": ["合作", "冲突", "对抗"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一场学术会议的电梯，几位陌生学者",
        "category": "专业决策",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["同盟", "排斥"],
    },
    {
        "scene": "一个考古发掘现场的午餐时间，团队成员",
        "category": "专业决策",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场博物馆导览，讲解员、参观者和文物修复师",
        "category": "专业决策",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一个天文观测站的观星夜，几位天文爱好者",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "同盟"],
        "optional_atmospheres": ["对抗", "冲突"],
    },
    {
        "scene": "一场科普讲座后，讲者和几位听众",
        "category": "教育成长",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一个图书馆的古籍修复室，修复师和访客",
        "category": "专业决策",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说","冲突","对抗"],
    },
    {
        "scene": "一场博士论文答辩会，答辩人和答辩委员会",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "劝说"],
        "optional_atmospheres": ["支持", "领导服从"],
    },
    {
        "scene": "一个田野考古现场，考古队员们",
        "category": "专业决策",
        "core_atmospheres": ["合作", "冲突", "领导服从"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场跨学科研讨会的茶歇，不同领域的学者",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "支持", "合作"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    
    # 医疗与生命类
    {
        "scene": "一个器官移植协调会议，医生、家属和伦理委员会成员",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "妥协", "劝说"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场临终关怀病房，几位家属",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个心理咨询室，团体治疗中几位陌生人",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "迁就"],
        "optional_atmospheres": ["合作", "排斥"],
    },
    {
        "scene": "一场医学伦理研讨会，几位医生",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一个献血车，几位献血者",
        "category": "公共协调",
        "core_atmospheres": ["支持", "合作", "妥协"],
        "optional_atmospheres": ["冲突", "迁就"],
    },
    {
        "scene": "一场医学伦理讨论会，医生、哲学家和家属",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "对抗", "劝说"],
        "optional_atmospheres": ["妥协", "迁就"],
    },
    {
        "scene": "一个医院的夜间急诊室，医护人员和患者家属",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "支持", "领导服从"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场医疗事故调解，医院代表和患者家属",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "迁就"],
    },
    
    # 法律与正义类
    {
        "scene": "一个陪审团休息室，陪审员们",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "劝说"],
    },
    {
        "scene": "一场离婚调解会，夫妻、律师和调解员",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "迁就"],
    },
    {
        "scene": "一个法律援助中心，几位志愿律师",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一场模拟法庭比赛后台，参赛学生",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "合作"],
        "optional_atmospheres": ["同盟", "妥协"],
    },
    {
        "scene": "一个社区矫正中心，几位服刑人员和社工",
        "category": "公共协调",
        "core_atmospheres": ["领导服从", "支持", "对抗"],
        "optional_atmospheres": ["劝说", "迁就"],
    },
    {
        "scene": "一场法律咨询热线，律师和来电者",
        "category": "专业决策",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    {
        "scene": "一个法庭的证人保护室，证人和警员",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "领导服从"],
        "optional_atmospheres": ["支持", "劝说"],
    },
    
    # 教育与成长类
    {
        "scene": "一场家长会，几位家长和老师",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "支持"],
    },
    {
        "scene": "一个自习室，几位考研学生",
        "category": "教育成长",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["迁就", "排斥"],
    },
    {
        "scene": "一场支教团队的总结会，志愿者们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一个辩论社团，成员们",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "合作"],
        "optional_atmospheres": ["同盟", "妥协"],
    },
    {
        "scene": "一场毕业典礼彩排，几位即将毕业的学生",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["妥协", "同盟"],
    },
    {
        "scene": "一个留学中介机构，顾问和家长、学生",
        "category": "专业决策",
        "core_atmospheres": ["劝说", "对抗", "支持"],
        "optional_atmospheres": ["妥协", "同盟"],
    },
    {
        "scene": "一场大学宿舍的卧谈会，几位室友",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "合作"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个特殊教育学校，教师和家长",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["劝说", "领导服从"],
    },
    
    # 体育与竞技类
    {
        "scene": "一个职业电竞战队的训练室，队员们",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一场马拉松比赛前夜，几位跑者",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["同盟", "冲突"],
    },
    {
        "scene": "一个攀岩馆，几位攀岩爱好者",
        "category": "教育成长",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["劝说", "支持"],
    },
    {
        "scene": "一场围棋比赛的复盘室，棋手、教练和解说员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "对抗"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一个健身房的更衣室，几位健身者",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["迁就", "劝说"],
    },
    {
        "scene": "一场拳击馆的陪练训练，拳手和陪练",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "合作", "领导服从"],
        "optional_atmospheres": ["冲突", "支持"],
    },
    {
        "scene": "一个滑板公园，几位滑板爱好者",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    {
        "scene": "一场业余足球赛的更衣室，队员们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "冲突", "领导服从"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    
    # 美食与餐饮类
    {
        "scene": "一场米其林评审前夜，餐厅主厨、副厨和侍酒师",
        "category": "创意表达",
        "core_atmospheres": ["合作", "领导服从", "冲突"],
        "optional_atmospheres": ["支持", "对抗"],
    },
    {
        "scene": "一个美食评论家聚会，几位评论家",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一场厨艺比赛后台，参赛者们",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "同盟"],
        "optional_atmospheres": ["支持", "妥协"],
    },
    {
        "scene": "一个深夜食堂，老板和几位常客",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一场品酒会，侍酒师、酒商和收藏家",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["合作", "妥协"],
    },
    {
        "scene": "一场厨艺比赛的评委席，几位评委",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一个分子料理实验室，主厨和助手",
        "category": "创意表达",
        "core_atmospheres": ["合作", "领导服从", "冲突"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场美食博主探店，博主和餐厅老板",
        "category": "创意表达",
        "core_atmospheres": ["支持", "对抗", "劝说"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    
    # 时尚与设计类
    {
        "scene": "一场时装周后台，设计师、模特和造型师",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "领导服从"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    {
        "scene": "一个独立设计师工作室，合伙人",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "支持"],
    },
    {
        "scene": "一场时尚杂志编辑部会议，编辑们",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一个服装定制店，裁缝、客户和设计师",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "妥协", "劝说"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场珠宝展览的布展现场，策展人和设计师",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一场时尚买手的选品会，买手和品牌方",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    {
        "scene": "一个服装定制工作室，裁缝和顾客",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    
    # 传媒与娱乐类
    {
        "scene": "一个播客录制室，几位主播",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一场真人秀节目的剪辑室，导演和剪辑师",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "领导服从", "妥协"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一个电台直播间，主持人和嘉宾",
        "category": "创意表达",
        "core_atmospheres": ["支持", "对抗", "合作"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一场脱口秀演出后台，演员们",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "劝说"],
    },
    {
        "scene": "一个影评人放映会，几位影评人",
        "category": "创意表达",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["妥协", "同盟"],
    },
    {
        "scene": "一场综艺节目的策划会，制片人和编导",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一个音乐制作室，制作人和歌手",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "合作"],
        "optional_atmospheres": ["领导服从", "妥协"],
    },
    {
        "scene": "一场网络直播的幕后，主播和运营团队",
        "category": "创意表达",
        "core_atmospheres": ["合作", "冲突", "领导服从"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    
    # 环保与自然类
    {
        "scene": "一个野生动物救助站，志愿者们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场观鸟活动，几位观鸟爱好者",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一个环保组织会议，成员们",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一个潜水俱乐部，潜水员们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一场垃圾分类推广活动，志愿者和社区居民",
        "category": "公共协调",
        "core_atmospheres": ["劝说", "冲突", "支持"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一个有机农场的参观日，农场主和访客",
        "category": "公共协调",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    
    # 科技与互联网类
    {
        "scene": "一个开源项目的线上会议，核心贡献者",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一场黑客马拉松，几位参赛者",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "妥协", "合作"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一个科技公司的产品评审会，工程师、设计师和产品经理",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "合作"],
    },
    {
        "scene": "一场网络安全会议，几位白帽黑客",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一个AI伦理研讨会，研究者们",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一场区块链项目路演，创始团队和投资人",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "劝说", "妥协"],
        "optional_atmospheres": ["冲突", "支持"],
    },
    {
        "scene": "一个游戏开发工作室，程序员和策划",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一场技术社区的线下聚会，开发者们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    
    # 宗教与信仰类
    {
        "scene": "一个寺庙的禅修营，几位学员",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场跨宗教对话会，不同信仰背景的人士",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "妥协", "支持"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    {
        "scene": "一个教堂的志愿者会议，成员们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "排斥"],
    },
    {
        "scene": "一场宗教艺术展的策展会，策展人和宗教人士",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "妥协", "劝说"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一个朝圣团队，成员们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "对抗"],
    },
    {
        "scene": "一场宗教经典研读会，几位信众",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "支持", "冲突"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    {
        "scene": "一个宗教慈善组织的筹款会，组织者和捐赠者",
        "category": "公共协调",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    
    # 社区与邻里类
    {
        "scene": "一个共享花园的管理会议，居民们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["合作", "迁就"],
    },
    {
        "scene": "一场社区图书漂流活动，几位参与者",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "劝说"],
    },
    {
        "scene": "一个老旧小区的电梯改造听证会，不同楼层住户",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "排斥"],
    },
    {
        "scene": "一场社区集市的摇位分配会，摇主们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["同盟", "劝说"],
    },
    {
        "scene": "一个邻里互助群的线下聚会，成员们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一场小区宠物管理听证会，养宠和不养宠的住户",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "排斥"],
    },
    {
        "scene": "一个社区共享工具库，几位借用者",
        "category": "公共协调",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 交通与旅行类
    {
        "scene": "一辆长途大巴，几位乘客",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["迁就", "劝说"],
    },
    {
        "scene": "一个青年旅舍的公共厨房，背包客们",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "妥协", "合作"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场拼车旅行，几位陌生人",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一个火车卧铺车厢，乘客们",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "妥协", "迁就"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场自驾游团队，成员们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    {
        "scene": "一个机场贵宾室，几位候机旅客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场邮轮上的餐桌，陌生乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 收藏与爱好类
    {
        "scene": "一个古董市场的鉴定会，几位收藏家",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["支持", "合作"],
    },
    {
        "scene": "一场手办展的交换会，爱好者们",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一个邮票收藏俱乐部，会员们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["排斥", "支持"],
    },
    {
        "scene": "一场黑胶唱片交流会，收藏家们",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一个模型制作工作室，爱好者们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一场球鞋交易会，球鞋爱好者们",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一个钱币收藏展，几位藏家",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    
    # 宠物与动物类
    {
        "scene": "一个宠物医院的候诊室，几位宠物主人",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "支持"],
        "optional_atmospheres": ["妥协", "劝说"],
    },
    {
        "scene": "一场宠物选美比赛后台，参赛者们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "同盟"],
        "optional_atmospheres": ["支持", "妥协"],
    },
    {
        "scene": "一个流浪动物救助站，志愿者们",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "妥协", "支持"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场宠物训练课，主人们",
        "category": "教育成长",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "劝说"],
    },
    {
        "scene": "一个宠物公墓的管理会议，工作人员",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一场宠物领养日，领养人和志愿者",
        "category": "公共协调",
        "core_atmospheres": ["支持", "劝说", "冲突"],
        "optional_atmospheres": ["对抗", "合作"],
    },
    {
        "scene": "一个猫咖啡馆，几位顾客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 婚恋与情感类
    {
        "scene": "一场相亲角，几位家长",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["妥协", "劝说"],
    },
    {
        "scene": "一个婚礼策划会，新人和双方父母",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["迁就", "劝说"],
    },
    {
        "scene": "一个单身派对，几位朋友",
        "category": "情感维系",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["妥协", "劝说"],
    },
    {
        "scene": "一场婚姻咨询，咨询师和来访夫妻",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "对抗"],
    },
    {
        "scene": "一个婚恋交友APP的线下活动，单身男女",
        "category": "情感维系",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["合作", "妥协"],
    },
    {
        "scene": "一场订婚宴，双方亲友",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "对抗"],
        "optional_atmospheres": ["合作", "妥协"],
    },
    
    # 职场与行业类
    {
        "scene": "一个自由职业者共享办公室，几位创作者",
        "category": "专业决策",
        "core_atmospheres": ["冲突", "妥协", "对抗"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一场行业协会年会，几位从业者",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一个猎头公司的候选人面试，面试官和候选人",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "领导服从", "劝说"],
        "optional_atmospheres": ["支持", "冲突"],
    },
    {
        "scene": "一场职业规划讲座，几位迷茫的职场人",
        "category": "教育成长",
        "core_atmospheres": ["支持", "冲突", "劝说"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个工会代表会议，代表们",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一场创业路演，创始人和投资人",
        "category": "资源竞争",
        "core_atmospheres": ["劝说", "对抗", "妥协"],
        "optional_atmospheres": ["冲突", "支持"],
    },
    {
        "scene": "一个职场导师计划，导师和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    
    # 金融与投资类
    {
        "scene": "一个投资俱乐部的月度会议，会员们",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一场私募基金路演，投资人和创始人",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "支持"],
    },
    {
        "scene": "一个理财沙龙，理财师和客户",
        "category": "专业决策",
        "core_atmospheres": ["劝说", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "妥协"],
    },
    {
        "scene": "一场股东大会前夜，小股东们",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "同盟", "冲突"],
        "optional_atmospheres": ["妥协", "排斥"],
    },
    {
        "scene": "一个众筹项目的支持者见面会，支持者们",
        "category": "资源竞争",
        "core_atmospheres": ["冲突", "对抗", "支持"],
        "optional_atmospheres": ["妥协", "同盟"],
    },
    {
        "scene": "一场保险产品说明会，保险顾问和客户",
        "category": "专业决策",
        "core_atmospheres": ["劝说", "对抗", "支持"],
        "optional_atmospheres": ["冲突", "妥协"],
    },
    {
        "scene": "一个家族信托规划会，家族成员和律师",
        "category": "资源竞争",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["同盟", "排斥"],
    },
    
    # 日常生活与偶遇类
    {
        "scene": "一个深夜便利店，店员、夜班工人和失眠者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场暴雨中的公交站台，几位陌生人",
        "category": "临时互动",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["迁就", "对抗"],
    },
    {
        "scene": "一个24小时书店的深夜，几位读者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    {
        "scene": "一场停电的电梯，被困的陌生人",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个候机大厅的延误夜晚，几位旅客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场婚礼宴席，被安排在同桌的陌生宾客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个洗衣店，等待衣服烘干的顾客们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场社区超市的排队结账，几位顾客",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "迁就"],
        "optional_atmospheres": ["支持", "妥协"],
    },
    {
        "scene": "一个共享充电宝归还点，几位用户",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场小区快递柜前，几位取件人",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "支持", "合作"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 特殊职业与工作场景类
    {
        "scene": "一个殡仪馆的化妆间，化妆师和实习生",
        "category": "教育成长",
        "core_atmospheres": ["领导服从", "支持", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场深夜出租车，司机和乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一个消防站的值班夜，消防员们",
        "category": "专业决策",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["领导服从", "对抗"],
    },
    {
        "scene": "一场婚礼现场，摄影师和策划师",
        "category": "专业决策",
        "core_atmospheres": ["合作", "冲突", "妥协"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一个宠物美容店，美容师、宠物主人和其他客人",
        "category": "临时互动",
        "core_atmospheres": ["支持", "冲突", "合作"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场快递分拣中心的夜班，几位快递员",
        "category": "专业决策",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个电影院放映结束后，放映员和清洁工",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场急救培训课，培训师和学员",
        "category": "教育成长",
        "core_atmospheres": ["领导服从", "支持", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一个夜班保安室，几位保安",
        "category": "专业决策",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场外卖配送站的晨会，配送员们",
        "category": "专业决策",
        "core_atmospheres": ["合作", "领导服从", "冲突"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    
    # 兴趣爱好与社群类
    {
        "scene": "一场桌游店的开放夜，几位陌生玩家",
        "category": "临时互动",
        "core_atmospheres": ["合作", "冲突", "对抗"],
        "optional_atmospheres": ["支持", "同盟"],
    },
    {
        "scene": "一个摄影外拍活动，摄影师们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场密室逃脱游戏，陌生队友",
        "category": "临时互动",
        "core_atmospheres": ["合作", "冲突", "领导服从"],
        "optional_atmospheres": ["支持", "对抗"],
    },
    {
        "scene": "一个手工艺市集，手作者们",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "妥协"],
    },
    {
        "scene": "一场线下读书会，书友们",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    {
        "scene": "一个剧本杀馆，玩家们",
        "category": "临时互动",
        "core_atmospheres": ["对抗", "冲突", "合作"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一场Cosplay展会后台，Coser们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个飞盘社群的训练日，队员们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场魔术爱好者聚会，魔术师们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "对抗", "合作"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    {
        "scene": "一个乐高搭建俱乐部，成员们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 公共空间与城市生活类
    {
        "scene": "一个公园的晨练时间，太极拳队和广场舞队",
        "category": "公共协调",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["排斥", "劝说"],
    },
    {
        "scene": "一场跳蚤市场，买家和卖家",
        "category": "临时互动",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    {
        "scene": "一个共享单车维修点，维修工和市民",
        "category": "公共协调",
        "core_atmospheres": ["支持", "冲突", "合作"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场街头艺人表演，艺人和围观者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个社区菜市场的早晨，常客们和摆主",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场城市徒步活动，领队和参与者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个天台花园，几位住户",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场城市广场的快闪活动，组织者和路人",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个公共图书馆的自习区，几位读者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场社区义诊，医生和居民",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    
    # 节日与庆典类
    {
        "scene": "一场跨年夜的倒数现场，陌生人",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个中秋赏月活动，几个家庭",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场社区春节联欢会后台，表演者们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个万圣节派对，几位戴着面具的陌生人",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场元宵灯会，几位游客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个圣诞集市的摆位，顾客和摆主",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场烟花大会的观赏点，几位观众",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场端午龙舟赛，几支队伍",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["合作", "支持"],
    },
    {
        "scene": "一个庙会的游戏摆位，摆主和游客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一场七夕相亲会，单身男女",
        "category": "情感维系",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["合作", "妥协"],
    },
    {
        "scene": "一场登山途中的休息点，几位登山者",
        "category": "临时互动",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个露营地的篱火夜，露营者们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场海边日出观赏，游客和当地渔民",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一个森林徒步，几位徒步者",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "妥协", "合作"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一场温泉旅馆的公共浴池，陌生泡汤者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个滑雪场的缆车，滑雪者们",
        "category": "临时互动",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场野外观星活动，天文爱好者和游客",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一场徒步穿越沙漠，队员们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "冲突", "领导服从"],
        "optional_atmospheres": ["对抗", "支持"],
    },
    {
        "scene": "一个钓鱼俱乐部的出海日，钓友们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    {
        "scene": "一场山地骑行活动，骑行者们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    
    # 交通工具与旅途类
    {
        "scene": "一趟跨国列车的餐车，不同国籍乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一艘游轮的甲板，几位乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场长途飞机的经济舱，邻座乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一辆夜间巴士，乘客们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个火车站的候车室，几位候车旅客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场拼车旅行的休息站，司机和乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一艘渡轮的观景台，几位乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场高铁商务座，几位乘客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个房车营地，几位房车旅行者",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场摩托车骑行团，骑手们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    
    # 学习与成长类
    {
        "scene": "一个语言交换活动，母语不同的学习者",
        "category": "教育成长",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "领导服从"],
    },
    {
        "scene": "一场TED式演讲的茶歇，演讲者和听众",
        "category": "教育成长",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一个写作工作坊，几位作者",
        "category": "教育成长",
        "core_atmospheres": ["对抗", "冲突", "支持"],
        "optional_atmospheres": ["妥协", "合作"],
    },
    {
        "scene": "一场技能分享会，参与者们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个冥想课程，学员们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场烹饪课堂，学员们",
        "category": "教育成长",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "领导服从"],
    },
    {
        "scene": "一个舞蹈工作室的课间，不同水平学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场编程训练营，学员们",
        "category": "教育成长",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个音乐理论课，老师和学生",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场职业技能认证考试后，考生们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    
    # 医疗健康与关怀类
    {
        "scene": "一个康复中心的理疗室，患者们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场产检候诊室，几位准妈妈",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个牙科诊所的等候区，患者们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场健康讲座，参与者和医生",
        "category": "教育成长",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一个戒烟互助小组，成员们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个视力检查中心，几位配眼镜的顾客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场心理咨询小组，参与者们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个中医诊所，医生和患者",
        "category": "专业决策",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一场营养师咨询会，营养师和客户",
        "category": "专业决策",
        "core_atmospheres": ["支持", "劝说", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    
    # 志愿服务与公益类
    {
        "scene": "一场海滩清洁活动，志愿者们",
        "category": "公共协调",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个社区食物银行，志愿者和受助者",
        "core_atmospheres": ["支持", "合作", "劝说"],
        "optional_atmospheres": ["对抗", "冲突"],
    },
    {
        "scene": "一个敬老院的探访活动，志愿者和老人",
        "category": "公共协调",
        "core_atmospheres": ["支持", "合作", "领导服从"],
        "optional_atmospheres": ["冲突", "迁就"],
    },
    {
        "scene": "一场植树节活动，参与者们",
        "category": "公共协调",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场献血活动现场，献血者们",
        "category": "公共协调",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一场社区支教活动，志愿者教师和学生",
        "category": "公共协调",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一个公益图书馆的整理日，志愿者们",
        "category": "公共协调",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场环保宣传活动，志愿者和市民",
        "category": "公共协调",
        "core_atmospheres": ["劝说", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    
    # 文化体验与传统类
    {
        "scene": "一场茶道体验课，茶艺师和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一个传统手工艺作坊，匠人和访客",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场书法展览的现场，书法家和观众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一个古琴演奏会，演奏者和听众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一场传统戏曲的后台，演员和观众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "领导服从"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一个香道体验馆，香道师和体验者",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场民俗节庆活动，本地人和外地游客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "劝说"],
        "optional_atmospheres": ["冲突", "对抗"],
    },
    {
        "scene": "一个陶艺工作室，陶艺师和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场传统乐器演奏会，演奏者和听众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一个剪纸艺术展，艺术家和参观者",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "劝说"],
        "optional_atmospheres": ["对抗", "冲突"],
    },
    
    # 科技与数字生活类
    {
        "scene": "一个VR体验馆，玩家们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场数码产品发布会排队现场，粉丝们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个修手机的小店，顾客和老板",
        "category": "临时互动",
        "core_atmospheres": ["支持", "冲突", "对抗"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一场线下网友见面会，网络好友",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场电子竞技比赛观赛现场，粉丝们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一个无人便利店，顾客们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场智能家居体验会，销售和客户",
        "category": "专业决策",
        "core_atmospheres": ["劝说", "支持", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一个3D打印工作坊，创客们",
        "category": "创意表达",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "同盟"],
    },
    {
        "scene": "一场无人机飞行俱乐部，飞手们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    
    # 美食文化与品鉴类
    {
        "scene": "一场葡萄酒品鉴会，侍酒师和品酒者",
        "category": "创意表达",
        "core_atmospheres": ["支持", "领导服从", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一个咖啡烘焙工作坊，咖啡师和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场私房菜晚宴，主厨和食客",
        "category": "创意表达",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一个农夫市集，农户和顾客",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "劝说"],
        "optional_atmospheres": ["对抗", "冲突"],
    },
    {
        "scene": "一场巧克力制作课程，学员们",
        "category": "教育成长",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "领导服从"],
    },
    {
        "scene": "一个传统糕点店，老师傅和年轻学徒",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一场美食纪录片的观影会，观众和美食家",
        "category": "创意表达",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一个威士忌品鉴会，品酒师和爱好者",
        "category": "创意表达",
        "core_atmospheres": ["支持", "领导服从", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一场火锅店的试吃会，食客们",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个烘焙比赛的评审席，评委们",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一场米其林餐厅的预约等位区，等位客人",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "迁就"],
    },
    
    # 心理与情绪类
    {
        "scene": "一场情绪管理工作坊，参与者们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    {
        "scene": "一个冥想静修营，学员们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场压力释放团体活动，参与者们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
    {
        "scene": "一个心理剧工作坊，演员和观众",
        "category": "教育成长",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    
    # 亲子与家庭类
    {
        "scene": "一场亲子运动会，家长和孩子",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "领导服从"],
    },
    {
        "scene": "一个家庭会议，家庭成员们",
        "category": "情感维系",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["支持", "劝说"],
    },
    {
        "scene": "一场育儿讲座，父母们",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "对抗"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    {
        "scene": "一个儿童游乐场，几位家长",
        "category": "临时互动",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场家庭聚餐的餐桌，几代人",
        "category": "情感维系",
        "core_atmospheres": ["支持", "冲突", "妥协"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    
    # 房产与居住类
    {
        "scene": "一场房产中介的看房团，购房者们",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["同盟", "支持"],
    },
    {
        "scene": "一个装修公司的方案讨论会，业主和设计师",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    {
        "scene": "一场业主委员会选举，候选人和业主",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "劝说"],
        "optional_atmospheres": ["同盟", "排斥"],
    },
    {
        "scene": "一个租房中介所，房东和租客",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "迁就"],
    },
    {
        "scene": "一场物业费调整听证会，业主和物业",
        "category": "公共协调",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "同盟"],
    },
    
    # 保险与理赔类
    {
        "scene": "一场车险理赔现场，车主和保险员",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "支持"],
    },
    {
        "scene": "一个保险纠纷调解室，投保人和保险公司",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "迁就"],
    },
    
    # 求职与招聘类
    {
        "scene": "一场招聘会现场，求职者和HR",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "劝说", "支持"],
        "optional_atmospheres": ["冲突", "妥协"],
    },
    {
        "scene": "一个群面现场，几位候选人",
        "category": "资源竞争",
        "core_atmospheres": ["对抗", "冲突", "同盟"],
        "optional_atmospheres": ["合作", "排斥"],
    },
    {
        "scene": "一场离职面谈，员工和主管",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "支持"],
    },
    {
        "scene": "一个职业测评中心，测评师和求职者",
        "category": "专业决策",
        "core_atmospheres": ["支持", "领导服从", "劝说"],
        "optional_atmospheres": ["合作", "对抗"],
    },
    
    # 消费与购物类
    {
        "scene": "一个奢侈品店，销售和顾客",
        "category": "临时互动",
        "core_atmospheres": ["劝说", "支持", "对抗"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一场商场退换货柜台，顾客和店员",
        "category": "临时互动",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "迁就"],
    },
    {
        "scene": "一个二手交易市场，买家和卖家",
        "category": "临时互动",
        "core_atmospheres": ["对抗", "妥协", "劝说"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    {
        "scene": "一场直播带货现场，主播和观众",
        "category": "临时互动",
        "core_atmospheres": ["劝说", "支持", "对抗"],
        "optional_atmospheres": ["冲突", "合作"],
    },
    
    # 法律咨询与维权类
    {
        "scene": "一个消费者协会投诉窗口，消费者和工作人员",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "支持", "劝说"],
        "optional_atmospheres": ["冲突", "妥协"],
    },
    {
        "scene": "一场劳动仲裁庭，员工和公司代表",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "迁就"],
    },
    {
        "scene": "一个法律援助中心，律师和求助者",
        "category": "专业决策",
        "core_atmospheres": ["支持", "劝说", "领导服从"],
        "optional_atmospheres": ["合作", "冲突"],
    },
    {
        "scene": "一场知识产权纠纷调解，双方当事人",
        "category": "专业决策",
        "core_atmospheres": ["对抗", "冲突", "妥协"],
        "optional_atmospheres": ["劝说", "同盟"],
    },
    
    # 老年生活类
    {
        "scene": "一个老年大学的课堂，老师和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "合作", "领导服从"],
        "optional_atmospheres": ["冲突", "劝说"],
    },
    {
        "scene": "一场老年人广场舞队的排练，队员们",
        "category": "情感维系",
        "core_atmospheres": ["合作", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一个养老院的活动室，几位老人",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "妥协"],
    },
    {
        "scene": "一场老年人旅行团，团员们",
        "category": "情感维系",
        "core_atmospheres": ["支持", "合作", "冲突"],
        "optional_atmospheres": ["对抗", "迁就"],
    },
    
    # 补充艺术与创作类
    {
        "scene": "一场诗歌朗读会，诗人和听众",
        "category": "创意表达",
        "core_atmospheres": ["支持", "对抗", "冲突"],
        "optional_atmospheres": ["合作", "劝说"],
    },
    {
        "scene": "一个动漫工作室，原画师和编剧",
        "category": "创意表达",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["合作", "同盟"],
    },
    
    # 补充体育与竞技类
    {
        "scene": "一场瑜伽馆的会员课，教练和学员",
        "category": "教育成长",
        "core_atmospheres": ["支持", "领导服从", "合作"],
        "optional_atmospheres": ["劝说", "冲突"],
    },
    {
        "scene": "一个台球厅，几位球友",
        "category": "情感维系",
        "core_atmospheres": ["对抗", "合作", "支持"],
        "optional_atmospheres": ["冲突", "同盟"],
    },
    
    # 补充教育与成长类
    {
        "scene": "一场考研自习室的占座纠纷，考生们",
        "category": "临时互动",
        "core_atmospheres": ["冲突", "对抗", "妥协"],
        "optional_atmospheres": ["迁就", "劝说"],
    },
    {
        "scene": "一个课外辅导班，老师、学生和家长",
        "category": "教育成长",
        "core_atmospheres": ["领导服从", "支持", "冲突"],
        "optional_atmospheres": ["对抗", "劝说"],
    },
]

def get_random_seed():
    """随机获取一个场景种子（返回完整的字典）"""
    import random
    return random.choice(SCENARIO_SEEDS)

def get_seed_by_index(index):
    """根据索引获取场景种子（支持循环，返回完整的字典）"""
    if len(SCENARIO_SEEDS) == 0:
        return None
    # 使用取模运算支持循环使用种子
    actual_index = index % len(SCENARIO_SEEDS)
    return SCENARIO_SEEDS[actual_index]

def get_all_seeds():
    """获取所有场景种子"""
    return SCENARIO_SEEDS.copy()

def get_seeds_count():
    """获取场景种子总数"""
    return len(SCENARIO_SEEDS)

def get_random_atmosphere(seed_dict, prefer_core=True, core_weight=0.7):
    """
    为给定场景随机选择一个适配的氛围
    
    Args:
        seed_dict: 场景字典，包含scene, core_atmospheres, optional_atmospheres
        prefer_core: 是否优先选择核心氛围
        core_weight: 核心氛围的权重（0-1之间），默认0.7表示70%概率选择核心氛围
    
    Returns:
        str: 选中的氛围
    """
    import random
    
    if not prefer_core:
        # 不偏好核心氛围，从所有适配氛围中均匀选择
        all_atmospheres = seed_dict["core_atmospheres"] + seed_dict["optional_atmospheres"]
        return random.choice(all_atmospheres)
    
    # 按权重选择核心或可选氛围
    if random.random() < core_weight:
        return random.choice(seed_dict["core_atmospheres"])
    else:
        return random.choice(seed_dict["optional_atmospheres"])

def get_scene_with_atmosphere(seed_dict=None, atmosphere=None):
    """
    获取场景和氛围的组合
    
    Args:
        seed_dict: 场景字典，如果为None则随机选择
        atmosphere: 指定的氛围，如果为None则根据场景随机选择适配的氛围
    
    Returns:
        dict: 包含scene和atmosphere的字典
    """
    import random
    
    if seed_dict is None:
        seed_dict = get_random_seed()
    
    if atmosphere is None:
        atmosphere = get_random_atmosphere(seed_dict)
    else:
        # 验证氛围是否适配该场景
        all_atmospheres = seed_dict["core_atmospheres"] + seed_dict["optional_atmospheres"]
        if atmosphere not in all_atmospheres:
            raise ValueError(f"氛围 '{atmosphere}' 不适配场景 '{seed_dict['scene']}'")
    
    return {
        "scene": seed_dict["scene"],
        "atmosphere": atmosphere,
        "is_core_atmosphere": atmosphere in seed_dict["core_atmospheres"]
    }

def get_all_atmospheres():
    """获取所有定义的氛围类型"""
    return ATMOSPHERES.copy()
