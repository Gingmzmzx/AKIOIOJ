import collections
import datetime
import functools
import itertools

from vj4 import constant
from vj4.util import version

# Blessings
BLESSING = False # Modify and restart
BLESSING_MESSAGE = "CSP-JS/NOIP 2025 RP++!!!"
BLESSING_CONTENT = "# 祝大家 CSP-JS/NOIP 2025 RP++!"

# Permissions.
PERM_NONE = 0

# Domain settings.
PERM_VIEW = 1 << 0
PERM_EDIT_PERM = 1 << 1
PERM_MOD_BADGE = 1 << 2
PERM_EDIT_DESCRIPTION = 1 << 3
PERM_EDIT_SUGGESTED_PROBLEM = 1 << 60
PERM_EDIT_SWIPER = 1 << 61

# Problem and Record.
PERM_CREATE_PROBLEM = 1 << 4
PERM_EDIT_PROBLEM = 1 << 5
PERM_EDIT_PROBLEM_SELF = 1 << 6
PERM_VIEW_PROBLEM = 1 << 7
PERM_VIEW_PROBLEM_HIDDEN = 1 << 8
PERM_SUBMIT_PROBLEM = 1 << 9
PERM_READ_PROBLEM_DATA = 1 << 10
PERM_READ_PROBLEM_DATA_SELF = 1 << 11
PERM_READ_PROBLEM_DATA_DISABLED_DOWNLOAD = 1 << 62
PERM_READ_RECORD_CODE = 1 << 12
PERM_REJUDGE_PROBLEM = 1 << 13
PERM_REJUDGE = 1 << 14

# Problem Solution.
PERM_VIEW_PROBLEM_SOLUTION = 1 << 15
PERM_CREATE_PROBLEM_SOLUTION = 1 << 16
PERM_VOTE_PROBLEM_SOLUTION = 1 << 17
PERM_EDIT_PROBLEM_SOLUTION = 1 << 18
PERM_EDIT_PROBLEM_SOLUTION_SELF = 1 << 19
PERM_DELETE_PROBLEM_SOLUTION = 1 << 20
PERM_DELETE_PROBLEM_SOLUTION_SELF = 1 << 21
PERM_REPLY_PROBLEM_SOLUTION = 1 << 22
PERM_EDIT_PROBLEM_SOLUTION_REPLY = 1 << 23
PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF = 1 << 24
PERM_DELETE_PROBLEM_SOLUTION_REPLY = 1 << 25
PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF = 1 << 26

# Discussion.
PERM_VIEW_DISCUSSION = 1 << 27
PERM_CREATE_DISCUSSION = 1 << 28
PERM_HIGHLIGHT_DISCUSSION = 1 << 29
PERM_EDIT_DISCUSSION = 1 << 30
PERM_EDIT_DISCUSSION_SELF = 1 << 31
PERM_DELETE_DISCUSSION = 1 << 32
PERM_DELETE_DISCUSSION_SELF = 1 << 33
PERM_REPLY_DISCUSSION = 1 << 34
PERM_EDIT_DISCUSSION_REPLY = 1 << 35
PERM_EDIT_DISCUSSION_REPLY_SELF = 1 << 36
PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION = 1 << 37
PERM_DELETE_DISCUSSION_REPLY = 1 << 38
PERM_DELETE_DISCUSSION_REPLY_SELF = 1 << 39
PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION = 1 << 40

# Contest.
PERM_VIEW_CONTEST = 1 << 41
PERM_VIEW_CONTEST_SCOREBOARD = 1 << 42
PERM_VIEW_CONTEST_HIDDEN_SCOREBOARD = 1 << 43
PERM_CREATE_CONTEST = 1 << 44
PERM_ATTEND_CONTEST = 1 << 45
PERM_EDIT_CONTEST = 1 << 50
PERM_EDIT_CONTEST_SELF = 1 << 51

# Homework.
PERM_VIEW_HOMEWORK = 1 << 52
PERM_VIEW_HOMEWORK_SCOREBOARD = 1 << 53
PERM_VIEW_HOMEWORK_HIDDEN_SCOREBOARD = 1 << 54
PERM_CREATE_HOMEWORK = 1 << 55
PERM_ATTEND_HOMEWORK = 1 << 56
PERM_EDIT_HOMEWORK = 1 << 57
PERM_EDIT_HOMEWORK_SELF = 1 << 58

# Training.
PERM_VIEW_TRAINING = 1 << 46
PERM_CREATE_TRAINING = 1 << 47
PERM_EDIT_TRAINING = 1 << 48
PERM_EDIT_TRAINING_SELF = 1 << 49

# Ranking.
PERM_VIEW_RANKING = 1 << 59

PERM_ALL = -1

Permission = collections.namedtuple('Permission',
                                    ['family', 'key', 'desc'])

PERMS = [
    Permission('perm_general', PERM_VIEW, 'View this domain'),
    Permission('perm_general', PERM_EDIT_PERM, 'Edit permissions of a role'),
    Permission('perm_general', PERM_MOD_BADGE, 'Show MOD badge'),
    Permission('perm_general', PERM_EDIT_DESCRIPTION, 'Edit description of this domain'),
    Permission('perm_general', PERM_EDIT_SUGGESTED_PROBLEM, 'Edit suggested problems of this domain'),
    Permission('perm_general', PERM_EDIT_SWIPER, 'Edit swiper images of this domain'),
    Permission('perm_problem', PERM_CREATE_PROBLEM, 'Create problems'),
    Permission('perm_problem', PERM_EDIT_PROBLEM, 'Edit problems'),
    Permission('perm_problem', PERM_EDIT_PROBLEM_SELF, 'Edit own problems'),
    Permission('perm_problem', PERM_VIEW_PROBLEM, 'View problems'),
    Permission('perm_problem', PERM_VIEW_PROBLEM_HIDDEN, 'View hidden problems'),
    Permission('perm_problem', PERM_SUBMIT_PROBLEM, 'Submit problem'),
    Permission('perm_problem', PERM_READ_PROBLEM_DATA, 'Read data of problem'),
    Permission('perm_problem', PERM_READ_PROBLEM_DATA_SELF, 'Read data of own problems'),
    Permission('perm_problem', PERM_READ_PROBLEM_DATA_DISABLED_DOWNLOAD, 'Read data of problems that disable downloading'),
    Permission('perm_record', PERM_READ_RECORD_CODE, 'Read record codes'),
    Permission('perm_record', PERM_REJUDGE_PROBLEM, 'Rejudge problems'),
    Permission('perm_record', PERM_REJUDGE, 'Rejudge records'),
    Permission('perm_problem_solution', PERM_VIEW_PROBLEM_SOLUTION, 'View problem solutions'),
    Permission('perm_problem_solution', PERM_CREATE_PROBLEM_SOLUTION, 'Create problem solutions'),
    Permission('perm_problem_solution', PERM_VOTE_PROBLEM_SOLUTION, 'Vote problem solutions'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION, 'Edit problem solutions'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION_SELF, 'Edit own problem solutions'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION, 'Delete problem solutions'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_SELF, 'Delete own problem solutions'),
    Permission('perm_problem_solution', PERM_REPLY_PROBLEM_SOLUTION, 'Reply problem solutions'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION_REPLY, 'Edit problem solution replies'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF, 'Edit own problem solution replies'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_REPLY, 'Delete problem solution replies'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF, 'Delete own problem solution replies'),
    Permission('perm_discussion', PERM_VIEW_DISCUSSION, 'View discussions'),
    Permission('perm_discussion', PERM_CREATE_DISCUSSION, 'Create discussions'),
    Permission('perm_discussion', PERM_HIGHLIGHT_DISCUSSION, 'Highlight discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION, 'Edit discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_SELF, 'Edit own discussions'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION, 'Delete discussions'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_SELF, 'Delete own discussions'),
    Permission('perm_discussion', PERM_REPLY_DISCUSSION, 'Reply discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY, 'Edit discussion replies'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY_SELF, 'Edit own discussion replies'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION, 'Edit discussion replies of own discussion'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY, 'Delete discussion replies'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY_SELF, 'Delete own discussion replies'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION, 'Delete discussion replies of own discussion'),
    Permission('perm_contest', PERM_VIEW_CONTEST, 'View contests'),
    Permission('perm_contest', PERM_VIEW_CONTEST_SCOREBOARD, 'View contest scoreboard'),
    Permission('perm_contest', PERM_VIEW_CONTEST_HIDDEN_SCOREBOARD, 'View hidden contest submission status and scoreboard'),
    Permission('perm_contest', PERM_CREATE_CONTEST, 'Create contests'),
    Permission('perm_contest', PERM_ATTEND_CONTEST, 'Attend contests'),
    Permission('perm_contest', PERM_EDIT_CONTEST, 'Edit any contests'),
    Permission('perm_contest', PERM_EDIT_CONTEST_SELF, 'Edit own contests'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK, 'View homework'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK_SCOREBOARD, 'View homework scoreboard'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK_HIDDEN_SCOREBOARD, 'View hidden homework submission status and scoreboard'),
    Permission('perm_homework', PERM_CREATE_HOMEWORK, 'Create homework'),
    Permission('perm_homework', PERM_ATTEND_HOMEWORK, 'Claim homework'),
    Permission('perm_homework', PERM_EDIT_HOMEWORK, 'Edit any homework'),
    Permission('perm_homework', PERM_EDIT_HOMEWORK_SELF, 'Edit own homework'),
    Permission('perm_training', PERM_VIEW_TRAINING, 'View training plans'),
    Permission('perm_training', PERM_CREATE_TRAINING, 'Create training plans'),
    Permission('perm_training', PERM_EDIT_TRAINING, 'Edit training plans'),
    Permission('perm_training', PERM_EDIT_TRAINING_SELF, 'Edit own training plans'),
    Permission('perm_ranking', PERM_VIEW_RANKING, 'View ranking'),
]

PERMS_BY_FAMILY = collections.OrderedDict(
    (f, list(g)) for f, g in itertools.groupby(PERMS, key=lambda p: p.family))
PERMS_BY_KEY = collections.OrderedDict(zip((s.key for s in PERMS), PERMS))

# Privileges.
PRIV_NONE = 0
PRIV_SET_PRIV = 1 << 0
PRIV_SET_PERM = 1 << 1
PRIV_USER_PROFILE = 1 << 2
PRIV_REGISTER_USER = 1 << 3
PRIV_READ_PROBLEM_DATA = 1 << 4
PRIV_READ_PRETEST_DATA = 1 << 5
PRIV_READ_PRETEST_DATA_SELF = 1 << 6
PRIV_READ_RECORD_CODE = 1 << 7
PRIV_VIEW_HIDDEN_RECORD = 1 << 8
PRIV_WRITE_RECORD = 1 << 9
PRIV_CREATE_DOMAIN = 1 << 10
PRIV_VIEW_ALL_DOMAIN = 1 << 11
PRIV_MANAGE_ALL_DOMAIN = 1 << 12
PRIV_REJUDGE = 1 << 13
PRIV_VIEW_USER_SECRET = 1 << 14
PRIV_VIEW_JUDGE_STATISTICS = 1 << 15
PRIV_CREATE_FILE = 1 << 16
PRIV_UNLIMITED_QUOTA = 1 << 17
PRIV_DELETE_FILE = 1 << 18
PRIV_DELETE_FILE_SELF = 1 << 19
PRIV_USER_SET_CHEAT = 1 << 20
PRIV_USER_SET_MEMORIAL_ACCOUNT = 1 << 22
PRIV_ADMIN = 1 << 21
PRIV_BENBENOP = 1 << 23
PRIV_ALL = -1

Privilege = collections.namedtuple('Privilege',
                                    ['family', 'key', 'desc'])

PRIVS = [
    Privilege("priv_none", PRIV_NONE, "Basic privileges"),
    Privilege("priv_set_priv", PRIV_SET_PRIV, "Modifying User Privileges"),
    Privilege("priv_set_perm", PRIV_SET_PERM, "Modifying User Permissions"),
    Privilege("priv_user_profile", PRIV_USER_PROFILE, "Use Profile"),
    Privilege("priv_register_user", PRIV_REGISTER_USER, "Register User"),
    Privilege("priv_read_problem_data", PRIV_READ_PROBLEM_DATA, "View problem data"),
    Privilege("priv_read_pretest_data", PRIV_READ_PRETEST_DATA, "View pretest data"),
    Privilege("priv_read_pretest_data_self", PRIV_READ_PRETEST_DATA_SELF, "View your own self-test data"),
    Privilege("priv_read_record_code", PRIV_READ_RECORD_CODE, "View Submitted Code"),
    Privilege("priv_view_hidden_record", PRIV_VIEW_HIDDEN_RECORD, "View hidden record"),
    Privilege("priv_write_record", PRIV_WRITE_RECORD, "Write Record"),
    Privilege("priv_create_domain", PRIV_CREATE_DOMAIN, "Create Domain"),
    Privilege("priv_view_all_domain", PRIV_VIEW_ALL_DOMAIN, "View All Domains"),
    Privilege("priv_manage_all_domain", PRIV_MANAGE_ALL_DOMAIN, "Manage All Domains"),
    Privilege("priv_rejudge", PRIV_REJUDGE, "Rejudge"),
    Privilege("priv_view_user_secret", PRIV_VIEW_USER_SECRET, "View User Secret"),
    Privilege("priv_view_judge_statistics", PRIV_VIEW_JUDGE_STATISTICS, "View judge statistics"),
    Privilege("priv_create_file", PRIV_CREATE_FILE, "Create File"),
    Privilege("priv_unlimited_quota", PRIV_UNLIMITED_QUOTA, "File space unlimited"),
    Privilege("priv_delete_file", PRIV_DELETE_FILE, "Delete File"),
    Privilege("priv_delete_file_self", PRIV_DELETE_FILE_SELF, "Delete yourself file"),
    Privilege("priv_user_set_cheat", PRIV_USER_SET_CHEAT, "Cheater Manager"),
    Privilege("priv_user_set_memorial_account", PRIV_USER_SET_MEMORIAL_ACCOUNT, "Memorial Account Manager"),
    Privilege("priv_admin", PRIV_ADMIN, "Use Admin Dashboard"),
    Privilege("priv_benbenop", PRIV_BENBENOP, "Updates Manager"),
]

PRIVS_BY_FAMILY = collections.OrderedDict(
    (f, list(g)) for f, g in itertools.groupby(PRIVS, key=lambda p: p.family))
PRIVS_BY_KEY = collections.OrderedDict(zip((s.key for s in PRIVS), PRIVS))

DEFAULT_PRIV = PRIV_USER_PROFILE | PRIV_CREATE_DOMAIN | PRIV_CREATE_FILE | PRIV_DELETE_FILE_SELF
JUDGE_PRIV = (PRIV_USER_PROFILE
              | PRIV_VIEW_ALL_DOMAIN
              | PRIV_READ_PROBLEM_DATA
              | PRIV_READ_PRETEST_DATA
              | PRIV_READ_RECORD_CODE
              | PRIV_WRITE_RECORD)

# Domains.
DOMAIN_ID_SYSTEM = 'system'
BASIC_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_VIEW_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_VIEW_TRAINING |
    PERM_VIEW_RANKING
)
DEFAULT_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_EDIT_PROBLEM_SELF |
    PERM_SUBMIT_PROBLEM |
    PERM_READ_PROBLEM_DATA |
    PERM_READ_PROBLEM_DATA_SELF |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_CREATE_PROBLEM_SOLUTION |
    PERM_VOTE_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_SELF |
    PERM_REPLY_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_VIEW_DISCUSSION |
    PERM_CREATE_DISCUSSION |
    PERM_EDIT_DISCUSSION_SELF |
    PERM_REPLY_DISCUSSION |
    PERM_EDIT_DISCUSSION_REPLY_SELF |
    # PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_DELETE_DISCUSSION_REPLY_SELF |
    PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_ATTEND_CONTEST |
    PERM_EDIT_CONTEST_SELF |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_ATTEND_HOMEWORK |
    PERM_EDIT_HOMEWORK_SELF |
    PERM_VIEW_TRAINING |
    PERM_CREATE_TRAINING |
    PERM_EDIT_TRAINING_SELF |
    PERM_VIEW_RANKING
)
ADMIN_PERMISSIONS = PERM_ALL
TCA_PERMISSIONS = PERM_ALL ^ PERM_EDIT_PERM


# Roles.
ROLE_ROOT = 'root'
ROLE_GUEST = 'guest'
ROLE_DEFAULT = 'default'
ROLE_MEMBER = 'member'
ROLE_ADMIN = 'admin'

BuiltinRoleDescriptor = functools.partial(
    collections.namedtuple('BuiltinRoleDescriptor',
                           ['modifiable', 'default_permission', 'description']))

# Built-in roles cannot be deleted.
BUILTIN_ROLE_DESCRIPTORS = {
    ROLE_ROOT: BuiltinRoleDescriptor(False, PERM_ALL, 'Always granted all privileges'),
    ROLE_GUEST: BuiltinRoleDescriptor(True, BASIC_PERMISSIONS, 'Valid for visitors'),
    ROLE_DEFAULT: BuiltinRoleDescriptor(True, DEFAULT_PERMISSIONS, 'Valid for registered users who are not members of the domain'),
}

BUILTIN_DOMAIN_BULLETIN = '''
# 欢迎来到AKIOI OJ
AKIOI OJ由XzyStudio运营维护，是一款自由优雅的在线评测系统，欢迎每一位OIer使用。
本OJ主域为原创题目以及其他内容，您可以创建您自己的域，添加题目、题单和比赛等。
更多内容请 **务必** 阅读[帮助](/wiki/help)
在每次CCF举办的大型考试前后，本OJ都会有很多独特的祝福。您需要自己发现！
'''

DOMAIN_SYSTEM = {
    '_id': DOMAIN_ID_SYSTEM,
    'owner_uid': 0,
    'roles': {ROLE_GUEST: BASIC_PERMISSIONS,
              ROLE_DEFAULT: DEFAULT_PERMISSIONS,
              ROLE_MEMBER: DEFAULT_PERMISSIONS,
              ROLE_ADMIN: TCA_PERMISSIONS},
    'gravatar': '',
    'name': 'AKIOI OJ',
    'bulletin': BUILTIN_DOMAIN_BULLETIN
}
DOMAINS = [DOMAIN_SYSTEM]

# Users.
UID_SYSTEM = 0
UNAME_SYSTEM = 'AKIOI OJ'
USER_SYSTEM = {
    '_id': UID_SYSTEM,
    'uname': UNAME_SYSTEM,
    'uname_lower': UNAME_SYSTEM.strip().lower(),
    'mail': '',
    'mail_lower': '',
    'salt': '',
    'hash': 'vj4|',
    'gender': constant.model.USER_GENDER_OTHER,
    'regat': datetime.datetime.utcfromtimestamp(0),
    'regip': '',
    'priv': PRIV_NONE,
    'loginat': datetime.datetime.utcnow(),
    'loginip': '',
    'gravatar': ''
}
UID_GUEST = 1
UNAME_GUEST = 'Guest'
USER_GUEST = {
    '_id': UID_GUEST,
    'uname': UNAME_GUEST,
    'uname_lower': UNAME_GUEST.strip().lower(),
    'mail': '',
    'mail_lower': '',
    'salt': '',
    'hash': 'vj4|',
    'gender': constant.model.USER_GENDER_OTHER,
    'regat': datetime.datetime.utcfromtimestamp(0),
    'regip': '',
    'priv': PRIV_REGISTER_USER,
    'loginat': datetime.datetime.utcnow(),
    'loginip': '',
    'gravatar': ''
}
DOMAIN_USER_GUEST = {
    # in every domain:
    'rp': 0.0,
    'rank': 0,
    'role': ROLE_GUEST,
    'level': 0,
    'num_submit': 0,
    'num_accept': 0
}
USERS = [USER_SYSTEM, USER_GUEST]

# Key represents level
# Value represents percent
# E.g. (10, 1) means that people whose rank is less than 1% will get Level 10
LEVELS = collections.OrderedDict([(10, 1),
                                  (9, 2),
                                  (8, 10),
                                  (7, 20),
                                  (6, 30),
                                  (5, 40),
                                  (4, 70),
                                  (3, 90),
                                  (2, 95),
                                  (1, 100)])

# Footer extra HTMLs.
FOOTER_EXTRA_HTMLS = ['© 2024 <a href="https://oj.xzynb.top">oj.xzynb.top</a>', "Powered by <a href='https://github.com/Gingmzmzx/AKIOIOJ'>AKIOIOJ</a> and <a href='https://github.com/vijos/vj4'>Vijos</a>"]

PROBLEM_CATEGORIES = collections.OrderedDict([
    ('动态规划', [
        'LCS',
        'LIS',
        '背包',
        '单调性DP',
        '环形DP',
        '树形DP',
        '状态压缩DP',
        '容斥DP'
    ]),
    ('搜索', [
        '枚举',
        '搜索与剪枝',
        '启发式搜索',
        'DLX',
        '双向搜索',
        '折半搜索',
        '记忆化搜索',
        '模拟退火'
    ]),
    ('计算几何', [
        '半平面交',
        '凸包',
        '几何图形的交与并',
        '旋转卡壳',
        '点定位',
        '坐标变换',
        '离散化与扫描',
        '反演',
        'Voronoi图',
        '平面图的对偶图',
        '三角剖分',
        '梯形剖分',
        '几何知识'
    ]),
    ('贪心', []),
    ('树结构', [
        '最近公共祖先',
        '生成树',
        'DFS序列',
        '树上倍增',
        '树的分治',
        '树链剖分',
        'Link-Cut-Tree'
    ]),
    ('图结构', [
        '平面图',
        '二分图',
        '二分图匹配',
        '最短路',
        '差分约束',
        '拓扑排序',
        '网络流',
        '强连通分量',
        '割点割边',
        '欧拉回路',
        '2-SAT'
    ]),
    ('数论', [
        '素数判定',
        '欧几里得算法',
        '不定方程',
        '数位统计',
        '解线性同余方程',
        'baby-step-giant-step',
        'Pell方程',
        '大整数质因数分解',
        '勾股方程',
        '积性函数',
        'Fibonacci数列'
    ]),
    ('模拟', []),
    ('数据结构', [
        '栈',
        '队列',
        '链表',
        '单调队列',
        '并查集',
        '堆',
        '平衡树',
        '线段树',
        '树状数组',
        '树套树',
        '四分树',
        '划分树',
        '归并树',
        'k-d树',
        '块状链表',
        'Hashing',
        '函数式编程'
    ]),
    ('博弈论', []),
    ('字符串', [
        'KMP',
        '后缀数据结构',
        'Trie树',
        'AC自动机',
        'Manacher',
        '表达式处理',
        '最小表示法'
    ]),
    ('组合数学', [
        '生成函数',
        '容斥原理',
        '康托展开',
        'Catalan数列',
        'Stirling数',
        '差分',
        'Polya定理'
    ]),
    ('线性代数', [
        '矩阵乘法',
        '高斯消元',
        '线性规划'
    ]),
    ('高精度', [
        'FFT'
    ]),
    ('递推', []),
    ('概率论', [
        '随机化'
    ]),
    ('NPC', []),
    ('其他', [
        '二分查找',
        '三分查找',
        '双指针扫描',
        '分治',
        '分块',
        'RMQ',
        '快速幂',
        '数学',
        '排序',
        '构造'
    ])
])
PROBLEM_SUB_CATEGORIES = {}
for category, sub_categories in PROBLEM_CATEGORIES.items():
  assert ' ' not in category
  assert ',' not in category
  for sub_category in sub_categories:
    assert ' ' not in sub_category
    assert ',' not in sub_category
    assert sub_category not in PROBLEM_SUB_CATEGORIES
    PROBLEM_SUB_CATEGORIES[sub_category] = category


VNODE_MISSING = {'title': '(missing)'}
DEFAULT_VNODES = collections.OrderedDict([
  ('探索', [
    {'pic': 'qa', 'name': '问答'},
    {'pic': 'share', 'name': '分享'},
    {'pic': 'solution', 'name': '题解'}
  ]),
  ('数据结构', [
    {'pic': None, 'name': '散列表'},
    {'pic': None, 'name': '搜索树'},
    {'pic': None, 'name': '栈和队列'},
    {'pic': None, 'name': '图'},
    {'pic': None, 'name': '堆'}
  ]),
  ('算法', [
    {'pic': None, 'name': '数论'},
    {'pic': None, 'name': '几何'},
    {'pic': None, 'name': '图论'},
    {'pic': None, 'name': '网络流'},
    {'pic': None, 'name': '动态规划'},
    {'pic': None, 'name': '背包'},
    {'pic': None, 'name': '排序'},
    {'pic': None, 'name': '搜索'},
    {'pic': None, 'name': '并查集'},
    {'pic': None, 'name': '贪心'},
    {'pic': None, 'name': '博弈论'}
  ]),
  ('泛', [
    {'pic': None, 'name': '数学'},
    {'pic': None, 'name': '编程'},
    {'pic': None, 'name': '数据库'},
    {'pic': None, 'name': 'C'},
    {'pic': None, 'name': 'C++'},
    {'pic': None, 'name': 'Pascal'},
    {'pic': None, 'name': 'Java'},
    {'pic': None, 'name': 'PHP'},
    {'pic': None, 'name': 'Python'},
    {'pic': None, 'name': '游戏'},
    {'pic': None, 'name': '保送'},
    {'pic': None, 'name': 'ACM'}
  ]),
  ('AKIOI OJ', [
    {'pic': None, 'name': '比赛'},
    {'pic': None, 'name': '题目'},
    {'pic': None, 'name': '数据'},
    {'pic': None, 'name': '管理'},
    {'pic': None, 'name': '维护'},
    {'pic': None, 'name': '反馈'},
    {'pic': None, 'name': '建议'}
  ])
])
