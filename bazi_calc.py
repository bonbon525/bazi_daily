from datetime import date, timedelta

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
WUXING_STEM = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
               '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
WUXING_BRANCH = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
                 '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
                 '戌': '土', '亥': '水'}
YINYANG = {'甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
           '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'}

# Oct 1, 1949 = 甲子日 (verified: 1949 PRC founding day)
REFERENCE_DATE = date(1949, 10, 1)

# Natal chart (Anqi Luo, 2001-05-25 15:55, Anhui Chuzhou, Female)
NATAL = {
    'name': '安琪',
    'birthday': date(2001, 5, 25),
    'birth_time': '15:55 (申时)',
    'birthplace': '安徽滁州',
    'gender': '女',
    'pillars': {
        '年柱': ('辛', '巳'),
        '月柱': ('癸', '巳'),
        '日柱': ('戊', '子'),
        '时柱': ('庚', '申'),
    },
    'day_master': '戊',
    'day_master_wx': '土',
    'strength': '身旺',
    'xiyong': ['水', '木', '金'],   # 喜用神
    'ji': ['火', '土'],              # 忌神
    'dayun_start_age': 4,
    'dayun_start_year': 2005,
    'dayun': [
        # (stem, branch, start_age, start_year)
        ('甲', '午', 4,  2005),
        ('乙', '未', 14, 2015),
        ('丙', '申', 24, 2025),
        ('丁', '酉', 34, 2035),
        ('戊', '戌', 44, 2045),
        ('己', '亥', 54, 2055),
        ('庚', '子', 64, 2065),
        ('辛', '丑', 74, 2075),
    ],
}

# Zanggan (hidden stems) - main qi only for simplicity
ZANGGAN = {
    '子': [('癸', '本气')],
    '丑': [('己', '本气'), ('癸', '中气'), ('辛', '余气')],
    '寅': [('甲', '本气'), ('丙', '中气'), ('戊', '余气')],
    '卯': [('乙', '本气')],
    '辰': [('戊', '本气'), ('乙', '中气'), ('癸', '余气')],
    '巳': [('丙', '本气'), ('庚', '中气'), ('戊', '余气')],
    '午': [('丁', '本气'), ('己', '中气')],
    '未': [('己', '本气'), ('丁', '中气'), ('乙', '余气')],
    '申': [('庚', '本气'), ('壬', '中气'), ('戊', '余气')],
    '酉': [('辛', '本气')],
    '戌': [('戊', '本气'), ('辛', '中气'), ('丁', '余气')],
    '亥': [('壬', '本气'), ('甲', '中气')],
}


def get_shishen(day_stem, other_stem):
    day_wx = WUXING_STEM[day_stem]
    other_wx = WUXING_STEM[other_stem]
    day_yang = YINYANG[day_stem] == '阳'
    other_yang = YINYANG[other_stem] == '阳'
    same = day_yang == other_yang

    gen = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    ctrl = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}

    if day_wx == other_wx:
        return '比肩' if same else '劫财'
    if gen[day_wx] == other_wx:
        return '食神' if same else '伤官'
    if gen[other_wx] == day_wx:
        return '偏印' if same else '正印'
    if ctrl[day_wx] == other_wx:
        return '偏财' if same else '正财'
    if ctrl[other_wx] == day_wx:
        return '偏官' if same else '正官'
    return '—'


def get_day_ganzhi(target_date=None):
    if target_date is None:
        target_date = date.today()
    delta = (target_date - REFERENCE_DATE).days
    return STEMS[delta % 10], BRANCHES[delta % 12]


def get_year_ganzhi(year):
    return STEMS[(year - 4) % 10], BRANCHES[(year - 4) % 12]


def get_month_ganzhi(target_date=None):
    if target_date is None:
        target_date = date.today()
    m, d = target_date.month, target_date.day

    # Solar terms (节) → branch index
    jie = [
        (1, 6, 1), (2, 4, 2), (3, 6, 3), (4, 5, 4),
        (5, 6, 5), (6, 6, 6), (7, 7, 7), (8, 7, 8),
        (9, 8, 9), (10, 8, 10), (11, 7, 11), (12, 7, 0),
    ]
    branch_idx = 0
    for jm, jd, bidx in jie:
        if m > jm or (m == jm and d >= jd):
            branch_idx = bidx

    # Year stem for month (based on 立春)
    y = target_date.year
    stem_year = y if (m > 2 or (m == 2 and d >= 4)) else y - 1
    ysi = (stem_year - 4) % 10
    yin_stem = [2, 4, 6, 8, 0][ysi % 5]  # stem index for 寅月
    month_stem_idx = (yin_stem + (branch_idx - 2) % 12) % 10

    return STEMS[month_stem_idx], BRANCHES[branch_idx]


def get_current_dayun(target_date=None):
    if target_date is None:
        target_date = date.today()
    age = (target_date - NATAL['birthday']).days / 365.25
    current = None
    for stem, branch, start_age, start_year in NATAL['dayun']:
        if age >= start_age:
            current = (stem, branch, start_age, start_year)
    return current


def get_week_preview(start_date=None):
    if start_date is None:
        start_date = date.today()
    result = []
    for i in range(8):
        d = start_date + timedelta(days=i)
        s, b = get_day_ganzhi(d)
        wx = WUXING_STEM[s]
        colors = {'木': '#52B788', '火': '#E05C5C', '土': '#C9A84C', '金': '#A8B8C8', '水': '#4A90D9'}
        score_map = {'水': 5, '木': 4, '金': 3, '火': 2, '土': 1}
        emojis = {'水': '💧', '木': '🌿', '金': '✨', '火': '🔥', '土': '⚖️'}
        result.append({
            'date': d, 'stem': s, 'branch': b,
            'wx': wx, 'color': colors[wx],
            'score': score_map[wx], 'emoji': emojis[wx],
            'shishen': get_shishen(NATAL['day_master'], s),
        })
    return result


def get_shichen_guide():
    shichen = [
        ('子', '水', '23-01', '夜半'), ('丑', '土', '01-03', '鸡鸣'),
        ('寅', '木', '03-05', '平旦'), ('卯', '木', '05-07', '日出'),
        ('辰', '土', '07-09', '食时'), ('巳', '火', '09-11', '隅中'),
        ('午', '火', '11-13', '日中'), ('未', '土', '13-15', '日昳'),
        ('申', '金', '15-17', '晡时'), ('酉', '金', '17-19', '日入'),
        ('戌', '土', '19-21', '黄昏'), ('亥', '水', '21-23', '人定'),
    ]
    result = []
    for branch, wx, time_range, name in shichen:
        if wx in NATAL['xiyong']:
            quality, stars = 'good', 3
        elif wx in NATAL['ji']:
            quality, stars = 'bad', 1
        else:
            quality, stars = 'neutral', 2
        result.append({'branch': branch, 'wx': wx, 'time': time_range,
                       'name': name, 'quality': quality, 'stars': stars})
    return result


def day_recommendation(day_stem, day_branch):
    wx = WUXING_STEM[day_stem]
    shishen = get_shishen(NATAL['day_master'], day_stem)
    branch_wx = WUXING_BRANCH[day_branch]

    recs = {
        '水': {
            'score': 5,
            'emoji': '💧',
            'title': '财运日 · 水旺',
            'summary': '今日水气旺盛，为安琪喜用神当令。财星有力，思维灵动。',
            'actions': ['适合谈判、签约、处理财务事项', '社交互动、建立人脉效果佳',
                        '学习新知识、钻研技术', '向上级汇报工作'],
            'caution': '注意不要情绪化，保持理性判断。',
            'color': '#4A90D9',
        },
        '木': {
            'score': 4,
            'emoji': '🌿',
            'title': '事业日 · 木旺',
            'summary': '木为戊土之官杀，今日官杀当令，有压力亦有机遇，宜主动进取。',
            'actions': ['积极推进工作项目，争取晋升机会', '与领导沟通，展示成果',
                        '处理规则、制度相关事务', '规划中长期目标'],
            'caution': '压力较大，注意劳逸结合，避免强硬冲突。',
            'color': '#52B788',
        },
        '金': {
            'score': 3,
            'emoji': '✨',
            'title': '才艺日 · 金旺',
            'summary': '金为戊土之食伤，才思泉涌，表达力强，适合创作与输出。',
            'actions': ['写作、汇报、演讲效果出色', '学习技能、研究数据', '整理文件、分析报告', '发挥专业特长'],
            'caution': '食伤泄秀，精力消耗较大，记得补充体力。',
            'color': '#C9A84C',
        },
        '火': {
            'score': 2,
            'emoji': '🔥',
            'title': '静养日 · 火旺',
            'summary': '火为戊土之印，命局火本已旺，今日火气再强，宜静不宜动。',
            'actions': ['整理思路、复盘回顾', '阅读学习，吸收知识', '室内静态活动为主', '照顾身体，早休息'],
            'caution': '忌大动作投资或重要决策，情绪易波动，注意心血管健康。',
            'color': '#E05C5C',
        },
        '土': {
            'score': 1,
            'emoji': '⚖️',
            'title': '平稳日 · 土旺',
            'summary': '土为戊土之比劫，同类相聚，竞争暗藏，格局略显壅滞。',
            'actions': ['处理日常琐事，维持现状', '整理空间、清理旧物', '与老朋友叙旧', '独立完成任务'],
            'caution': '忌大额财务支出，注意同事竞争，低调行事。',
            'color': '#A0785A',
        },
    }

    rec = recs[wx].copy()
    rec['shishen'] = shishen
    rec['wx'] = wx
    rec['branch_wx'] = branch_wx
    return rec
