"""
场景种子库 - 预定义的多样化场景方向
每个场景包含：
- scene: 场景的核心定义（人物和场所）
- category: 场景类别（7个粗粒度分类）
  * Professional Decision (专业决策)
  * Creative Expression (创意表达)
  * Educational Growth (教育成长)
  * Emotional Bonding (情感维系)
  * Resource Competition (资源竞争)
  * Public Coordination (公共协调)
  * Casual Interaction (临时互动)
- core_atmospheres: 核心适配氛围（最常见、最合理的氛围）
- optional_atmospheres: 可选氛围（可以使用但不是最典型的）
- 未列出的氛围将被排除（不合理的组合）
"""

# 氛围类型定义
ATMOSPHERES = [
    "cooperation",      # 多方协同工作，共同目标
    "confrontation",    # 明确的对立关系，利益冲突
    "persuasion",       # 一方试图说服另一方
    "accommodation",    # 一方妥协退让以维持关系
    "alliance",         # 结成联盟，共同对抗第三方
    "exclusion",        # 排挤、孤立某一方
    "support",          # 给予帮助和鼓励
    "conflict",         # 激烈的矛盾和争执
    "compromise",       # 各方让步达成平衡
    "authority",        # 明确的上下级或权威关系
]

SCENARIO_SEEDS = [
    # 艺术与创作类
    {
        "scene": "An opening reception for an underground avant-garde art exhibition, with curators, artists, critics, and mysterious buyers",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "alliance", "persuasion"],
        "optional_atmospheres": ["cooperation", "support", "compromise"],
    },
    {
        "scene": "A premiere of an independent documentary, with the director, subjects, and audience",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "conflict", "confrontation"],
        "optional_atmospheres": ["persuasion", "compromise"],
    },
    {
        "scene": "A preview at an auction house, with several bidders",
        "category": "Resource Competition",
        "core_atmospheres": ["confrontation", "alliance", "exclusion"],
        "optional_atmospheres": ["cooperation", "compromise"],
    },
    {
        "scene": "A dressing room backstage at a music festival, with band members of different styles",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A performance art event, with the artist, audience, and security guards",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "persuasion"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A gallery opening, with the artist anonymously mingling in the crowd",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["persuasion", "cooperation"],
    },
    {
        "scene": "A street graffiti session, with graffiti artists, city officials, and passersby",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "An open day at a sculpture studio, with the sculptor and visitors",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A rehearsal for experimental theater, with the director, actors, and playwright",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "authority"],
    },
    {
        "scene": "A photography darkroom, with photographers discussing development techniques",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    
    # 科研与学术类
    {
        "scene": "A late-night laboratory, with several researchers",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "conflict", "confrontation"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "An elevator at an academic conference, with several unfamiliar scholars",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["alliance", "exclusion"],
    },
    {
        "scene": "Lunchtime at an archaeological dig site, with team members",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A museum tour, with the guide, visitors, and artifact restorers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A stargazing night at an observatory, with astronomy enthusiasts",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "alliance"],
        "optional_atmospheres": ["conflict", "confrontation"],
    },
    {
        "scene": "A thesis defense, with the candidate and review committee",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "authority", "support"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A funding application meeting for a research project, with researchers and review experts",
        "category": "Professional Decision",
        "core_atmospheres": ["persuasion", "confrontation", "support"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "An interdisciplinary symposium, with scholars from different fields",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "An equipment usage conflict in a lab, with several graduate students",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "accommodation"],
    },
    {
        "scene": "An editorial meeting for an academic journal, with editors",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    
    # 医疗与生命类
    {
        "scene": "An organ transplant ethics hearing, with doctors, patient families, and ethics committee members",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A late night in the emergency room, with medical staff and patient families",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["authority", "accommodation"],
    },
    {
        "scene": "A family meeting in a hospice ward, with doctors, patients, and family members",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "accommodation", "conflict"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A waiting area outside the delivery room, with several expectant fathers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A medical malpractice investigation, with hospital management, doctors, and patient representatives",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "alliance"],
    },
    {
        "scene": "A therapy room in a rehabilitation center, with therapists and patients",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A medical ethics seminar, with doctors and ethicists",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "cooperation", "support"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A hemodialysis center, with several patients",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    
    # 法律与正义类
    {
        "scene": "A divorce mediation session, with the couple, lawyers, and mediator",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    {
        "scene": "A jury deliberation room, with jurors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "persuasion"],
    },
    {
        "scene": "An inheritance dispute trial, with heirs",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["exclusion", "compromise"],
    },
    {
        "scene": "A prison visiting room, with inmates and family members",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "accommodation", "conflict"],
        "optional_atmospheres": ["persuasion", "cooperation"],
    },
    {
        "scene": "A criminal trial, with prosecutors, defense attorneys, and defendants",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A consultation room at a legal aid center, with lawyers and help-seekers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "persuasion", "authority"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A labor dispute mediation, with union representatives and company management",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "alliance"],
    },
    {
        "scene": "A small claims court, with plaintiffs and defendants",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    
    # 教育与成长类
    {
        "scene": "A hallway after a parent-teacher conference, with several parents",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["alliance", "cooperation"],
    },
    {
        "scene": "An academic dishonesty hearing, with students, teachers, and academic affairs office",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "authority"],
        "optional_atmospheres": ["persuasion", "support"],
    },
    {
        "scene": "A roommate conflict mediation in a college dorm, with the dorm supervisor and students",
        "category": "Educational Growth",
        "core_atmospheres": ["conflict", "compromise", "authority"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    {
        "scene": "Pick-up time at a kindergarten, with several parents",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A scholarship review committee, with judges",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A break at a tutoring center, with students",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A school bullying investigation, with students, parents, and school officials",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["persuasion", "authority"],
    },
    {
        "scene": "A thesis supervision meeting, with advisors and students",
        "category": "Educational Growth",
        "core_atmospheres": ["authority", "support", "conflict"],
        "optional_atmospheres": ["persuasion", "cooperation"],
    },
    {
        "scene": "A teacher tenure review, with review committee members",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A student council election, with candidates",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["alliance", "exclusion"],
    },
    
    # 体育与竞技类
    {
        "scene": "A professional esports team's training room, with team members",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["compromise", "exclusion"],
    },
    {
        "scene": "A marathon aid station, with volunteers and runners",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["authority", "accommodation"],
    },
    {
        "scene": "A boxing gym locker room, with several boxers",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "support", "alliance"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    {
        "scene": "Halftime at an amateur soccer match, with team members",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "conflict", "authority"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A gym locker room, with several gym-goers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["accommodation", "persuasion"],
    },
    {
        "scene": "A game review room at a Go tournament, with players and coaches",
        "category": "Creative Expression",
        "core_atmospheres": ["authority", "support", "conflict"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "After swimming team practice, with team members",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "The scorer's table at a basketball game, with referees and scorekeepers",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "authority", "conflict"],
        "optional_atmospheres": ["support", "confrontation"],
    },
    {
        "scene": "A climbing gym, with several climbing enthusiasts",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "Court allocation at a badminton club, with members",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A member class at a yoga studio, with instructors and students",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A billiards hall, with several players",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "cooperation", "support"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    
    # 美食与餐饮类
    {
        "scene": "A Michelin-starred restaurant kitchen during service, with chefs",
        "category": "Creative Expression",
        "core_atmospheres": ["authority", "cooperation", "conflict"],
        "optional_atmospheres": ["support", "confrontation"],
    },
    {
        "scene": "A food truck festival, with several vendors",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "Backstage at a culinary competition, with contestants",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "alliance"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A restaurant reservation dispute, with the host and waiting customers",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "conflict", "accommodation"],
        "optional_atmospheres": ["persuasion", "compromise"],
    },
    {
        "scene": "A food critic's table, with the critic and restaurant staff",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "support", "persuasion"],
        "optional_atmospheres": ["cooperation", "compromise"],
    },
    {
        "scene": "The judges' table at a culinary competition, with several judges",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A shared table at a hot pot restaurant, with strangers",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A cooking class, with students",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "authority"],
    },
    {
        "scene": "A coffee shop during peak hours, with customers waiting for seats",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "accommodation"],
        "optional_atmospheres": ["compromise", "cooperation"],
    },
    
    # 时尚与设计类
    {
        "scene": "Backstage at a fashion show, with models and stylists",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "conflict", "authority"],
        "optional_atmospheres": ["support", "confrontation"],
    },
    {
        "scene": "A design studio pitch meeting, with designers and clients",
        "category": "Creative Expression",
        "core_atmospheres": ["persuasion", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A vintage clothing market, with vendors and buyers",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "persuasion", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A fashion magazine editorial meeting, with editors",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["alliance", "cooperation"],
    },
    {
        "scene": "A makeup artist competition, with contestants",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["support", "cooperation"],
    },
    {
        "scene": "An interior design consultation, with the designer and homeowners",
        "category": "Creative Expression",
        "core_atmospheres": ["persuasion", "compromise", "conflict"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A fashion design critique, with professors and students",
        "category": "Creative Expression",
        "core_atmospheres": ["authority", "support", "conflict"],
        "optional_atmospheres": ["persuasion", "cooperation"],
    },
    {
        "scene": "A jewelry design workshop, with artisans",
        "category": "Public Coordination",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    
    # 传媒与娱乐类
    {
        "scene": "A film set during a break, with the director, actors, and crew",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "conflict", "authority"],
        "optional_atmospheres": ["support", "confrontation"],
    },
    {
        "scene": "A reality show confessional room, with contestants",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["exclusion", "support"],
    },
    {
        "scene": "A press conference, with celebrities and journalists",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "persuasion", "support"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    {
        "scene": "A radio studio during a live broadcast, with the host and guests",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "confrontation", "cooperation"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "Backstage at a stand-up comedy show, with comedians",
        "category": "Public Coordination",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["support", "persuasion"],
    },
    {
        "scene": "A film critics' screening, with several critics",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["compromise", "alliance"],
    },
    {
        "scene": "A variety show planning meeting, with producers and directors",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A music production studio, with the producer and singer",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "cooperation"],
        "optional_atmospheres": ["authority", "compromise"],
    },
    {
        "scene": "Behind the scenes of a live stream, with the streamer and operations team",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "conflict", "authority"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    
    # 环保与自然类
    {
        "scene": "A wildlife rescue center, with volunteers",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "compromise", "support"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A birdwatching excursion, with several birdwatching enthusiasts",
        "category": "Resource Competition",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "An environmental organization meeting, with members",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["compromise", "exclusion"],
    },
    {
        "scene": "A diving club, with divers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A waste sorting promotion campaign, with volunteers and community residents",
        "category": "Emotional Bonding",
        "core_atmospheres": ["persuasion", "conflict", "support"],
        "optional_atmospheres": ["confrontation", "cooperation"],
    },
    {
        "scene": "An open day at an organic farm, with the farmer and visitors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    
    # 科技与互联网类
    {
        "scene": "An online meeting for an open-source project, with core contributors",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["compromise", "exclusion"],
    },
    {
        "scene": "A hackathon, with several participants",
        "category": "Creative Expression",
        "core_atmospheres": ["conflict", "compromise", "cooperation"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    {
        "scene": "A product review meeting at a tech company, with engineers, designers, and product managers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "cooperation"],
    },
    {
        "scene": "A cybersecurity conference, with several white-hat hackers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "An AI ethics symposium, with researchers",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A blockchain project pitch, with the founding team and investors",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "persuasion", "compromise"],
        "optional_atmospheres": ["conflict", "support"],
    },
    {
        "scene": "A game development studio, with programmers and planners",
        "category": "Public Coordination",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A tech startup pitch competition, with entrepreneurs",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A data privacy debate, with experts",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    
    # 宗教与信仰类
    {
        "scene": "An interfaith dialogue, with religious leaders",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A temple volunteer meeting, with volunteers",
        "category": "Public Coordination",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["authority", "accommodation"],
    },
    {
        "scene": "A religious study group, with participants",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A church committee meeting, with committee members",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A meditation retreat, with participants",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    
    # 社区与邻里类
    {
        "scene": "A community owners' meeting, with homeowners",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "persuasion"],
    },
    {
        "scene": "A neighborhood watch patrol, with volunteers",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["authority", "alliance"],
    },
    {
        "scene": "A community garden allocation meeting, with residents",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A property management hearing on pet policies, with pet owners and non-pet owners",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "exclusion"],
    },
    {
        "scene": "A neighborhood noise complaint mediation, with neighbors",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    {
        "scene": "A community event planning meeting, with volunteers",
        "category": "Resource Competition",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A shared courtyard cleanup day, with residents",
        "category": "Resource Competition",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    
    # 交通与旅行类
    {
        "scene": "A tour group bus, with tourists and the guide",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "compromise", "authority"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A hostel common room, with backpackers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A carpool trip, with several strangers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "compromise", "confrontation"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A train sleeper car, with passengers",
        "category": "Resource Competition",
        "core_atmospheres": ["conflict", "compromise", "accommodation"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A road trip group, with members",
        "category": "Resource Competition",
        "core_atmospheres": ["conflict", "compromise", "confrontation"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "An airport VIP lounge, with several waiting travelers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A dining table on a cruise ship, with stranger passengers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    
    # 收藏与爱好类
    {
        "scene": "An appraisal session at an antique market, with several collectors",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["support", "cooperation"],
    },
    {
        "scene": "A trading session at a figure exhibition, with enthusiasts",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A stamp collecting club, with members",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["exclusion", "support"],
    },
    {
        "scene": "A vinyl record exchange meeting, with collectors",
        "category": "Public Coordination",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A model-making workshop, with hobbyists",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A sneaker trading event, with sneaker enthusiasts",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A coin collecting exhibition, with several collectors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["compromise", "cooperation"],
    },
    
    # 宠物与动物类
    {
        "scene": "A veterinary clinic waiting room, with several pet owners",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "support"],
        "optional_atmospheres": ["compromise", "persuasion"],
    },
    {
        "scene": "Backstage at a pet beauty pageant, with contestants",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "alliance"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A stray animal rescue center, with volunteers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "compromise", "support"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A pet training class, with owners",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["support", "persuasion"],
    },
    {
        "scene": "A pet cemetery management meeting, with staff",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "compromise", "confrontation"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A pet adoption day, with adopters and volunteers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "persuasion", "conflict"],
        "optional_atmospheres": ["confrontation", "cooperation"],
    },
    {
        "scene": "A cat café, with several customers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    
    # 婚恋与情感类
    {
        "scene": "A matchmaking corner, with several parents",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["compromise", "persuasion"],
    },
    {
        "scene": "A wedding planning meeting, with the couple and both sets of parents",
        "category": "Public Coordination",
        "core_atmospheres": ["conflict", "compromise", "confrontation"],
        "optional_atmospheres": ["accommodation", "persuasion"],
    },
    {
        "scene": "A divorce mediation, with the couple, lawyers, and mediator",
        "category": "Resource Competition",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "accommodation"],
    },
    {
        "scene": "A bachelor party, with several friends",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["compromise", "persuasion"],
    },
    {
        "scene": "Marriage counseling, with the counselor and visiting couple",
        "category": "Resource Competition",
        "core_atmospheres": ["support", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "confrontation"],
    },
    {
        "scene": "An offline event for a dating app, with single men and women",
        "category": "Resource Competition",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["cooperation", "compromise"],
    },
    {
        "scene": "An engagement party, with relatives and friends from both sides",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "conflict", "confrontation"],
        "optional_atmospheres": ["cooperation", "compromise"],
    },
    
    # 职场与行业类
    {
        "scene": "A freelancer coworking space, with several creators",
        "category": "Resource Competition",
        "core_atmospheres": ["conflict", "compromise", "confrontation"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "An industry association annual meeting, with several practitioners",
        "category": "Resource Competition",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A corporate team-building activity, with colleagues",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "An annual performance review, with the manager and employee",
        "category": "Resource Competition",
        "core_atmospheres": ["authority", "confrontation", "support"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A startup founding team meeting, with co-founders",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["alliance", "cooperation"],
    },
    {
        "scene": "A labor union negotiation, with union representatives and management",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "alliance"],
    },
    {
        "scene": "An office relocation discussion, with employees",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    
    # 金融与投资类
    {
        "scene": "A venture capital pitch meeting, with entrepreneurs and investors",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "persuasion", "support"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "A stock trading floor, with several traders",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["compromise", "exclusion"],
    },
    {
        "scene": "A private equity fund roadshow, with investors and founders",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "support"],
    },
    {
        "scene": "A wealth management salon, with financial advisors and clients",
        "category": "Casual Interaction",
        "core_atmospheres": ["persuasion", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "The night before a shareholders' meeting, with minority shareholders",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "alliance", "conflict"],
        "optional_atmospheres": ["compromise", "exclusion"],
    },
    {
        "scene": "A crowdfunding project supporters' meetup, with supporters",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "support"],
        "optional_atmospheres": ["compromise", "alliance"],
    },
    {
        "scene": "An insurance product presentation, with insurance consultants and clients",
        "category": "Casual Interaction",
        "core_atmospheres": ["persuasion", "confrontation", "support"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "A family trust planning meeting, with family members and lawyers",
        "category": "Educational Growth",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["alliance", "exclusion"],
    },
    
    # 日常生活与偶遇类
    {
        "scene": "A late-night convenience store, with the clerk, night shift workers, and insomniacs",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A bus stop during a rainstorm, with several strangers",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["accommodation", "confrontation"],
    },
    {
        "scene": "A 24-hour bookstore late at night, with several readers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    {
        "scene": "A stuck elevator during a power outage, with trapped strangers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "An airport terminal during a delayed night, with several travelers",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A wedding banquet table, with stranger guests seated together",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A laundromat, with customers waiting for their clothes to dry",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A checkout line at a community supermarket, with several customers",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "accommodation"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A shared power bank return point, with several users",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "In front of a community parcel locker, with several people picking up packages",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "support", "cooperation"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    
    # 特殊职业与工作场景类
    {
        "scene": "A funeral home makeup room, with the makeup artist and intern",
        "category": "Emotional Bonding",
        "core_atmospheres": ["authority", "support", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A late-night taxi ride, with the driver and passenger",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A night shift at a fire station, with firefighters",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["authority", "confrontation"],
    },
    {
        "scene": "A wedding venue, with the photographer and event planner",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "conflict", "compromise"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    {
        "scene": "A pet grooming salon, with the groomer, pet owners, and other customers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "conflict", "cooperation"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A night shift at a courier sorting center, with several couriers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "After a movie screening, with the projectionist and cleaning staff",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A first aid training class, with the trainer and students",
        "category": "Emotional Bonding",
        "core_atmospheres": ["authority", "support", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A night shift security office, with several guards",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A morning meeting at a food delivery station, with delivery workers",
        "category": "Public Coordination",
        "core_atmospheres": ["cooperation", "authority", "conflict"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    
    # 兴趣爱好与社群类
    {
        "scene": "An open night at a board game café, with several stranger players",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "conflict", "confrontation"],
        "optional_atmospheres": ["support", "alliance"],
    },
    {
        "scene": "A photography outing, with photographers",
        "category": "Public Coordination",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "An escape room game, with stranger teammates",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "conflict", "authority"],
        "optional_atmospheres": ["support", "confrontation"],
    },
    {
        "scene": "A handicraft market, with artisans",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "An offline book club meeting, with book lovers",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["compromise", "cooperation"],
    },
    {
        "scene": "A murder mystery game venue, with players",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "cooperation"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "Backstage at a cosplay convention, with cosplayers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A frisbee community training day, with team members",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A magic enthusiasts' gathering, with magicians",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "confrontation", "cooperation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    {
        "scene": "A LEGO building club, with members",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    
    # 公共空间与城市生活类
    {
        "scene": "A park during morning exercise time, with tai chi and square dancing groups",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["exclusion", "persuasion"],
    },
    {
        "scene": "A flea market, with buyers and sellers",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    {
        "scene": "A public library reading room, with several readers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A city square fountain, with several street performers",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    {
        "scene": "A community bulletin board, with residents posting and reading notices",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A public restroom queue, with several people waiting",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "accommodation", "confrontation"],
        "optional_atmospheres": ["support", "compromise"],
    },
    {
        "scene": "A rooftop garden, with several residents",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A flash mob in a city square, with organizers and passersby",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A study area in a public library, with several readers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "accommodation", "compromise"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    {
        "scene": "A community health clinic, with doctors and residents",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "authority"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    
    # 节日与庆典类
    {
        "scene": "A New Year's Eve countdown, with strangers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A Mid-Autumn moon viewing event, with several families",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "Backstage at a community Spring Festival gala, with performers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "authority"],
    },
    {
        "scene": "A Halloween party, with several masked strangers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A Lantern Festival, with several tourists",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A Christmas market stall, with customers and vendors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A fireworks viewing spot, with several spectators",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A Dragon Boat Festival race, with several teams",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["cooperation", "support"],
    },
    {
        "scene": "A game stall at a temple fair, with the vendor and visitors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A Qixi Festival matchmaking event, with single men and women",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["cooperation", "compromise"],
    },
    
    # 自然与户外类
    {
        "scene": "A rest stop during a mountain climb, with several hikers",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A campfire night at a campsite, with campers",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A seaside sunrise viewing, with tourists and local fishermen",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A forest hike, with several hikers",
        "category": "Casual Interaction",
        "core_atmospheres": ["conflict", "compromise", "cooperation"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    {
        "scene": "A public bath at a hot spring inn, with stranger bathers",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A ski lift at a ski resort, with skiers",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A wilderness stargazing event, with astronomy enthusiasts and tourists",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A desert trekking expedition, with team members",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "conflict", "authority"],
        "optional_atmospheres": ["confrontation", "support"],
    },
    {
        "scene": "A fishing club's sea outing day, with fishing buddies",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    {
        "scene": "A mountain biking event, with cyclists",
        "category": "Educational Growth",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    
    # 交通工具与旅途类
    {
        "scene": "A dining car on an international train, with passengers of different nationalities",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A cruise ship deck, with several passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "Economy class on a long-haul flight, with neighboring passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A night bus, with passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A train station waiting room, with several waiting travelers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A rest stop during a carpool trip, with the driver and passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "An observation deck on a ferry, with several passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "High-speed rail business class, with several passengers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "An RV campground, with several RV travelers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A motorcycle riding group, with riders",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    
    # 学习与成长类
    {
        "scene": "A language exchange event, with learners of different native languages",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "authority"],
    },
    {
        "scene": "A tea break at a TED-style talk, with speakers and audience",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A writing workshop, with several authors",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "support"],
        "optional_atmospheres": ["compromise", "cooperation"],
    },
    {
        "scene": "A skill-sharing session, with participants",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A meditation course, with students",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A break at a dance studio, with students of different skill levels",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A coding bootcamp, with students",
        "category": "Professional Decision",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A music theory class, with the teacher and students",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "After a professional certification exam, with test-takers",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    
    # 医疗健康与关怀类
    {
        "scene": "A physical therapy room at a rehabilitation center, with patients",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A prenatal checkup waiting room, with several expectant mothers",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A dental clinic waiting area, with patients",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A health seminar, with participants and doctors",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A smoking cessation support group, with members",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "An optometry center, with several customers getting glasses",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A group therapy session, with participants",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A traditional Chinese medicine clinic, with the doctor and patients",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A nutritionist consultation, with the nutritionist and clients",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "persuasion", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    
    # 志愿服务与公益类
    {
        "scene": "A beach cleanup activity, with volunteers",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A community food bank, with volunteers and recipients",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "cooperation", "authority"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A nursing home visit, with volunteers and elderly residents",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "authority"],
        "optional_atmospheres": ["conflict", "accommodation"],
    },
    {
        "scene": "A tree-planting event, with participants",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A blood donation drive, with donors",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A community tutoring program, with volunteer teachers and students",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A charity library organizing day, with volunteers",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "An environmental awareness campaign, with volunteers and citizens",
        "category": "Casual Interaction",
        "core_atmospheres": ["persuasion", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    
    # 文化体验与传统类
    {
        "scene": "A tea ceremony class, with the tea master and students",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A traditional handicraft workshop, with the artisan and visitors",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "Backstage at a traditional opera performance, with performers and audience",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "authority"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "An incense ceremony experience hall, with the incense master and participants",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A folk festival celebration, with locals and out-of-town visitors",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "persuasion"],
        "optional_atmospheres": ["conflict", "confrontation"],
    },
    {
        "scene": "A pottery studio, with the potter and students",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A traditional instrument concert, with performers and listeners",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A paper-cutting art exhibition, with the artist and visitors",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "cooperation", "persuasion"],
        "optional_atmospheres": ["confrontation", "conflict"],
    },
    
    # 科技与数字生活类
    {
        "scene": "A VR experience center, with players",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A queue at a digital product launch event, with fans",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A phone repair shop, with customers and the owner",
        "category": "Creative Expression",
        "core_atmospheres": ["support", "conflict", "confrontation"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "An offline meetup for online friends, with internet buddies",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "An esports match viewing party, with fans",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "An unmanned convenience store, with customers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A smart home experience event, with salespeople and customers",
        "category": "Creative Expression",
        "core_atmospheres": ["persuasion", "support", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A 3D printing workshop, with makers",
        "category": "Creative Expression",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "alliance"],
    },
    {
        "scene": "A drone flying club, with pilots",
        "category": "Casual Interaction",
        "core_atmospheres": ["cooperation", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    
    # 美食文化与品鉴类
    {
        "scene": "A wine tasting event, with the sommelier and tasters",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "authority", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A coffee roasting workshop, with the barista and students",
        "category": "Casual Interaction",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A private dining dinner, with the chef and diners",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A farmers market, with farmers and customers",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "persuasion"],
        "optional_atmospheres": ["confrontation", "conflict"],
    },
    {
        "scene": "A chocolate-making class, with students",
        "category": "Emotional Bonding",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "authority"],
    },
    {
        "scene": "A traditional pastry shop, with the master baker and young apprentice",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "authority", "cooperation"],
        "optional_atmospheres": ["persuasion", "conflict"],
    },
    {
        "scene": "A food documentary screening, with the audience and food experts",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "A whiskey tasting event, with the tasting expert and enthusiasts",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "authority", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A hot pot restaurant tasting session, with diners",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A baking competition judges' table, with judges",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A waiting area for a Michelin restaurant reservation, with waiting guests",
        "category": "Emotional Bonding",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["support", "accommodation"],
    },
    
    # 心理与情绪类
    {
        "scene": "An emotional management workshop, with participants",
        "category": "Resource Competition",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    {
        "scene": "A meditation retreat, with students",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A stress relief group activity, with participants",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
    {
        "scene": "A psychodrama workshop, with actors and audience",
        "category": "Resource Competition",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    
    # 亲子与家庭类
    {
        "scene": "A parent-child sports day, with parents and children",
        "category": "Public Coordination",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "authority"],
    },
    {
        "scene": "A family meeting, with family members",
        "category": "Professional Decision",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["support", "persuasion"],
    },
    {
        "scene": "A parenting seminar, with parents",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "confrontation"],
        "optional_atmospheres": ["conflict", "alliance"],
    },
    {
        "scene": "A children's playground, with several parents",
        "category": "Professional Decision",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A family dinner table, with multiple generations",
        "category": "Resource Competition",
        "core_atmospheres": ["support", "conflict", "compromise"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    
    # 房产与居住类
    {
        "scene": "A property viewing tour, with prospective buyers",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["alliance", "support"],
    },
    {
        "scene": "A renovation design discussion, with the homeowner and designer",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    {
        "scene": "A homeowners' association election, with candidates and residents",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "persuasion"],
        "optional_atmospheres": ["alliance", "exclusion"],
    },
    {
        "scene": "A rental agency office, with landlords and tenants",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "accommodation"],
    },
    {
        "scene": "A property management fee adjustment hearing, with residents and property management",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "alliance"],
    },
    
    # 保险与理赔类
    {
        "scene": "A car insurance claim scene, with the car owner and insurance adjuster",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "support"],
    },
    {
        "scene": "An insurance dispute mediation room, with the policyholder and insurance company",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    
    # 求职与招聘类
    {
        "scene": "A job fair, with job seekers and HR representatives",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "persuasion", "support"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "A group interview, with several candidates",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "alliance"],
        "optional_atmospheres": ["cooperation", "exclusion"],
    },
    {
        "scene": "An exit interview, with the employee and supervisor",
        "category": "Professional Decision",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "support"],
    },
    {
        "scene": "A career assessment center, with the assessor and job seeker",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "authority", "persuasion"],
        "optional_atmospheres": ["cooperation", "confrontation"],
    },
    
    # 消费与购物类
    {
        "scene": "A luxury goods store, with salespeople and customers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["persuasion", "support", "confrontation"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "A mall return and exchange counter, with customers and staff",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    {
        "scene": "A secondhand trading market, with buyers and sellers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["confrontation", "compromise", "persuasion"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    {
        "scene": "A live shopping broadcast, with the host and viewers",
        "category": "Creative Expression",
        "core_atmospheres": ["persuasion", "support", "confrontation"],
        "optional_atmospheres": ["conflict", "cooperation"],
    },
    
    # 法律咨询与维权类
    {
        "scene": "A consumer association complaint window, with consumers and staff",
        "category": "Creative Expression",
        "core_atmospheres": ["confrontation", "support", "persuasion"],
        "optional_atmospheres": ["conflict", "compromise"],
    },
    {
        "scene": "A labor arbitration hearing, with employees and company representatives",
        "category": "Educational Growth",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "accommodation"],
    },
    {
        "scene": "A legal aid center, with lawyers and help-seekers",
        "category": "Emotional Bonding",
        "core_atmospheres": ["support", "persuasion", "authority"],
        "optional_atmospheres": ["cooperation", "conflict"],
    },
    {
        "scene": "An intellectual property dispute mediation, with both parties",
        "category": "Casual Interaction",
        "core_atmospheres": ["confrontation", "conflict", "compromise"],
        "optional_atmospheres": ["persuasion", "alliance"],
    },
    
    # 老年生活类
    {
        "scene": "A seniors' university classroom, with the teacher and students",
        "category": "Educational Growth",
        "core_atmospheres": ["support", "cooperation", "authority"],
        "optional_atmospheres": ["conflict", "persuasion"],
    },
    {
        "scene": "A square dancing group rehearsal, with team members",
        "core_atmospheres": ["cooperation", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A nursing home activity room, with several elderly residents",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "compromise"],
    },
    {
        "scene": "A seniors' tour group, with group members",
        "core_atmospheres": ["support", "cooperation", "conflict"],
        "optional_atmospheres": ["confrontation", "accommodation"],
    },
    
    # 补充艺术与创作类
    {
        "scene": "A poetry recital, with poets and listeners",
        "core_atmospheres": ["support", "confrontation", "conflict"],
        "optional_atmospheres": ["cooperation", "persuasion"],
    },
    {
        "scene": "An animation studio, with animators and scriptwriters",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["cooperation", "alliance"],
    },
    
    # 补充教育与成长类
    {
        "scene": "A seat dispute in a graduate school study room, with students",
        "core_atmospheres": ["conflict", "confrontation", "compromise"],
        "optional_atmospheres": ["accommodation", "persuasion"],
    },
    {
        "scene": "An after-school tutoring class, with teachers, students, and parents",
        "core_atmospheres": ["authority", "support", "conflict"],
        "optional_atmospheres": ["confrontation", "persuasion"],
    },
]

def get_random_seed():
    """随机获取一个场景种子（返回完整的字典）"""
    import random
    return random.choice(SCENARIO_SEEDS)

def get_seed_by_index(index):
    """根据索引获取场景种子（支持循环，返回完整的字典）"""
    if len(SCENARIO_SEEDS) == 0:
        raise ValueError("SCENARIO_SEEDS is empty")
    return SCENARIO_SEEDS[index % len(SCENARIO_SEEDS)]

def get_all_seeds():
    """获取所有场景种子"""
    return SCENARIO_SEEDS.copy()

def get_random_atmosphere(seed_dict, prefer_core=True, core_weight=0.7):
    """
    从场景字典中随机选择一个适配的氛围
    
    Args:
        seed_dict: 场景字典，包含scene、core_atmospheres和optional_atmospheres
        prefer_core: 是否偏好核心氛围，默认True
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

