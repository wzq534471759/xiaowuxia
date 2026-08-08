"""
小武侠传说 · 无尽武道篇
基于 Kivy 的跨平台武侠 RPG（支持 Android / Windows / Linux）
"""

import os
import json
import random
import math
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse

# ============================================================
# 全局配色
# ============================================================
COLORS = {
    'bg_dark':   (0.05, 0.05, 0.08, 1),
    'bg_panel':  (0.12, 0.10, 0.15, 1),
    'bg_card':   (0.18, 0.15, 0.22, 1),
    'gold':      (0.85, 0.72, 0.30, 1),
    'gold_dim':  (0.60, 0.50, 0.20, 1),
    'ink':       (0.90, 0.88, 0.82, 1),
    'ink_dim':   (0.65, 0.62, 0.55, 1),
    'red':       (0.75, 0.20, 0.20, 1),
    'red_bright':(0.95, 0.35, 0.25, 1),
    'green':     (0.30, 0.70, 0.40, 1),
    'blue':      (0.35, 0.55, 0.85, 1),
    'purple':    (0.65, 0.40, 0.80, 1),
    'orange':    (0.90, 0.55, 0.15, 1),
    'cyan':      (0.30, 0.80, 0.85, 1),
    'pink':      (0.90, 0.50, 0.65, 1),
}

# ============================================================
# 游戏数据
# ============================================================

HEROES_DATA = {
    "张无忌": {"element":"光","hp":580,"atk":52,"def":38,"spd":40,"crit":0.10,"dodge":0.05,"desc":"九阳神功护体，百毒不侵","skills":["九阳神功","乾坤大挪移"]},
    "令狐冲": {"element":"风","hp":420,"atk":58,"def":28,"spd":55,"crit":0.15,"dodge":0.12,"desc":"独孤九剑，无招胜有招","skills":["独孤剑法","凌波微步"]},
    "段誉":   {"element":"水","hp":390,"atk":48,"def":25,"spd":50,"crit":0.12,"dodge":0.10,"desc":"北冥神功吸人内力，六脉神剑无形","skills":["北冥神功","凌波微步"]},
    "乔峰":   {"element":"火","hp":650,"atk":65,"def":42,"spd":45,"crit":0.12,"dodge":0.03,"desc":"降龙十八掌，至刚至阳","skills":["降龙掌法","打狗棒法"]},
    "杨过":   {"element":"暗","hp":440,"atk":60,"def":30,"spd":52,"crit":0.18,"dodge":0.08,"desc":"黯然销魂掌，情之所至","skills":["黯然销魂掌","玉女素心剑"]},
    "郭靖":   {"element":"土","hp":700,"atk":50,"def":50,"spd":30,"crit":0.08,"dodge":0.02,"desc":"侠之大者，为国为民","skills":["降龙掌法","空明拳"]},
    "黄蓉":   {"element":"木","hp":380,"atk":45,"def":28,"spd":58,"crit":0.14,"dodge":0.15,"desc":"打狗棒法变幻莫测，奇门遁甲","skills":["打狗棒法","弹指神通"]},
    "小龙女": {"element":"冰","hp":400,"atk":55,"def":32,"spd":60,"crit":0.16,"dodge":0.20,"desc":"玉女心经，冰清玉洁","skills":["玉女素心剑","天罗地网势"]},
    "王语嫣": {"element":"木","hp":350,"atk":40,"def":22,"spd":48,"crit":0.10,"dodge":0.10,"desc":"熟知天下武学，过目不忘","skills":["琅嬛秘典","凌波微步"]},
    "周芷若": {"element":"暗","hp":410,"atk":53,"def":30,"spd":53,"crit":0.14,"dodge":0.10,"desc":"九阴白骨爪，阴狠毒辣","skills":["九阴真经","白蟒鞭法"]},
    "黄药师": {"element":"木","hp":480,"atk":58,"def":35,"spd":52,"crit":0.15,"dodge":0.12,"desc":"东邪碧海潮生曲，奇门五转","skills":["弹指神通","碧海潮生曲"]},
    "欧阳锋": {"element":"毒","hp":460,"atk":60,"def":33,"spd":42,"crit":0.13,"dodge":0.05,"desc":"西毒蛤蟆功，逆练九阴","skills":["蛤蟆功","灵蛇拳法"]},
    "洪七公": {"element":"火","hp":550,"atk":62,"def":40,"spd":48,"crit":0.12,"dodge":0.06,"desc":"北丐降龙十八掌，行侠仗义","skills":["降龙掌法","打狗棒法"]},
    "一灯大师":{"element":"光","hp":520,"atk":50,"def":42,"spd":38,"crit":0.10,"dodge":0.05,"desc":"南帝一阳指，慈悲为怀","skills":["一阳指","先天功"]},
    "慕容复": {"element":"风","hp":430,"atk":56,"def":30,"spd":56,"crit":0.14,"dodge":0.12,"desc":"以彼之道还施彼身，复兴大燕","skills":["斗转星移","参合指"]},
    "韦小宝": {"element":"混","hp":360,"atk":35,"def":20,"spd":65,"crit":0.20,"dodge":0.25,"desc":"溜之大吉，浑身是宝","skills":["神行百变","含沙射影"]},
    "张翠山": {"element":"光","hp":440,"atk":50,"def":35,"spd":45,"crit":0.11,"dodge":0.08,"desc":"银钩铁划，武当七侠","skills":["武当绵掌","梯云纵"]},
    "殷素素": {"element":"暗","hp":380,"atk":48,"def":26,"spd":50,"crit":0.13,"dodge":0.12,"desc":"天鹰教紫薇堂主，机智过人","skills":["千蛛万毒手","灵蛇拳法"]},
    "石破天": {"element":"土","hp":600,"atk":58,"def":45,"spd":35,"crit":0.10,"dodge":0.04,"desc":"太玄经大成，返璞归真","skills":["太玄经","罗汉伏魔功"]},
    "胡斐":   {"element":"火","hp":470,"atk":56,"def":34,"spd":50,"crit":0.13,"dodge":0.08,"desc":"胡家刀法，豪气干云","skills":["胡家刀法","春蚕掌法"]},
    "程灵素": {"element":"毒","hp":370,"atk":42,"def":24,"spd":52,"crit":0.12,"dodge":0.10,"desc":"毒手药王关门弟子，妙手回春","skills":["药王神掌","轻功身法"]},
    "狄云":   {"element":"土","hp":500,"atk":54,"def":38,"spd":38,"crit":0.11,"dodge":0.05,"desc":"神照经大成，连城剑法","skills":["神照功","连城剑法"]},
    "袁承志": {"element":"金","hp":480,"atk":55,"def":36,"spd":46,"crit":0.12,"dodge":0.08,"desc":"金蛇郎君传人，华山弟子","skills":["金蛇剑法","混元功"]},
    "阿青":   {"element":"剑","hp":360,"atk":68,"def":22,"spd":70,"crit":0.25,"dodge":0.20,"desc":"越女剑法，一剑破千军","skills":["越女剑法","轻盈身法"]},
}

SKILLS_DATA = {
    "降龙掌法":   {"type":"外功","power":85,"element":"火","desc":"至刚至阳，掌力如龙","rarity":"橙"},
    "独孤剑法":   {"type":"外功","power":90,"element":"风","desc":"无招胜有招，剑魔传承","rarity":"橙"},
    "九阳神功":   {"type":"内功","power":70,"element":"光","desc":"诸阴不侵，百毒不灭","rarity":"橙"},
    "乾坤大挪移": {"type":"内功","power":65,"element":"光","desc":"挪移乾坤，借力打力","rarity":"橙"},
    "北冥神功":   {"type":"内功","power":60,"element":"水","desc":"吸人内力化为己用","rarity":"橙"},
    "凌波微步":   {"type":"轻功","power":30,"element":"水","desc":"踏雪无痕，步法绝世","rarity":"紫"},
    "打狗棒法":   {"type":"外功","power":75,"element":"土","desc":"丐帮镇帮绝学，三十六路","rarity":"紫"},
    "黯然销魂掌": {"type":"外功","power":88,"element":"暗","desc":"情之所至，草木为之含悲","rarity":"橙"},
    "玉女素心剑": {"type":"外功","power":72,"element":"冰","desc":"古墓派绝学，双剑合璧","rarity":"紫"},
    "九阴真经":   {"type":"内功","power":80,"element":"暗","desc":"天下武学总纲，博大精深","rarity":"橙"},
    "弹指神通":   {"type":"外功","power":55,"element":"木","desc":"桃花岛绝学，弹指伤敌","rarity":"紫"},
    "碧海潮生曲": {"type":"内功","power":50,"element":"木","desc":"以乐入武，乱人心神","rarity":"紫"},
    "蛤蟆功":     {"type":"内功","power":68,"element":"毒","desc":"西毒绝学，蓄力爆发","rarity":"紫"},
    "一阳指":     {"type":"外功","power":62,"element":"光","desc":"大理段氏绝学，指力惊人","rarity":"紫"},
    "先天功":     {"type":"内功","power":72,"element":"光","desc":"道门正宗，内力绵长","rarity":"橙"},
    "斗转星移":   {"type":"内功","power":55,"element":"风","desc":"以彼之道还施彼身","rarity":"紫"},
    "神行百变":   {"type":"轻功","power":25,"element":"混","desc":"韦小宝保命绝学","rarity":"蓝"},
    "含沙射影":   {"type":"外功","power":40,"element":"暗","desc":"暗器手法，防不胜防","rarity":"蓝"},
    "太玄经":     {"type":"内功","power":95,"element":"土","desc":"石破天悟透，返璞归真","rarity":"橙"},
    "神照功":     {"type":"内功","power":75,"element":"土","desc":"内力精纯，可起死回生","rarity":"橙"},
    "金蛇剑法":   {"type":"外功","power":78,"element":"金","desc":"金蛇郎君自创，诡谲莫测","rarity":"紫"},
    "越女剑法":   {"type":"外功","power":95,"element":"剑","desc":"阿青独悟，剑意通神","rarity":"橙"},
    "白蟒鞭法":   {"type":"外功","power":58,"element":"暗","desc":"峨眉鞭法，阴柔狠辣","rarity":"蓝"},
    "空明拳":     {"type":"外功","power":60,"element":"土","desc":"刚柔并济，以虚击实","rarity":"紫"},
    "梯云纵":     {"type":"轻功","power":28,"element":"光","desc":"武当轻功，踏云而起","rarity":"紫"},
    "参合指":     {"type":"外功","power":58,"element":"风","desc":"慕容家传，指力透体","rarity":"紫"},
    "连城剑法":   {"type":"外功","power":70,"element":"土","desc":"连城诀中剑法，凌厉无匹","rarity":"紫"},
    "春蚕掌法":   {"type":"外功","power":54,"element":"火","desc":"苗家掌法，刚猛迅捷","rarity":"蓝"},
    "药王神掌":   {"type":"外功","power":48,"element":"毒","desc":"以毒攻毒，掌带奇毒","rarity":"蓝"},
    "胡家刀法":   {"type":"外功","power":76,"element":"火","desc":"胡一刀所创，刀法大开大合","rarity":"紫"},
    "轻功身法":   {"type":"轻功","power":26,"element":"风","desc":"基础身法，步履轻盈","rarity":"蓝"},
    "天罗地网势": {"type":"外功","power":50,"element":"冰","desc":"古墓派掌法，绵密如网","rarity":"蓝"},
    "混元功":     {"type":"内功","power":65,"element":"金","desc":"华山内功，刚阳正气","rarity":"紫"},
    "武当绵掌":   {"type":"外功","power":56,"element":"光","desc":"武当掌法，绵里藏针","rarity":"蓝"},
    "罗汉伏魔功": {"type":"内功","power":70,"element":"土","desc":"少林内功，刚正不阿","rarity":"橙"},
    "千蛛万毒手": {"type":"外功","power":52,"element":"毒","desc":"天鹰教毒功，阴毒无比","rarity":"蓝"},
    "灵蛇拳法":   {"type":"外功","power":60,"element":"毒","desc":"欧阳锋自创，如蛇灵动","rarity":"紫"},
    "轻盈身法":   {"type":"轻功","power":32,"element":"剑","desc":"阿青身法，快如闪电","rarity":"紫"},
    "琅嬛秘典":   {"type":"内功","power":45,"element":"木","desc":"王语嫣家传，包罗万象","rarity":"紫"},
}

ENEMIES_DATA = {
    "山贼":       {"hp":120,"atk":18,"def":5, "spd":25,"exp":30,  "silver":15,"ybp":(0.10,1,3),"element":"土"},
    "暗影刺客":   {"hp":200,"atk":28,"def":8, "spd":40,"exp":55,  "silver":30,"ybp":(0.15,1,4),"element":"暗"},
    "魔教弟子":   {"hp":280,"atk":35,"def":12,"spd":35,"exp":80,  "silver":45,"ybp":(0.20,2,5),"element":"火"},
    "山贼头目":   {"hp":450,"atk":42,"def":18,"spd":30,"exp":120, "silver":70,"ybp":(0.25,3,8),"element":"土"},
    "神秘剑客":   {"hp":520,"atk":48,"def":20,"spd":45,"exp":150, "silver":90,"ybp":(0.30,3,8),"element":"风"},
    "魔教长老":   {"hp":800,"atk":58,"def":28,"spd":40,"exp":250, "silver":150,"ybp":(0.40,5,12),"element":"火"},
    "用毒高手":   {"hp":600,"atk":55,"def":22,"spd":42,"exp":220, "silver":130,"ybp":(0.45,6,15),"element":"毒"},
    "少林武僧":   {"hp":950,"atk":62,"def":35,"spd":38,"exp":320, "silver":200,"ybp":(0.50,8,20),"element":"光"},
    "暗影护法":   {"hp":1200,"atk":70,"def":40,"spd":48,"exp":450,"silver":300,"ybp":(0.55,10,25),"element":"暗"},
    "魔教左使":   {"hp":1500,"atk":80,"def":45,"spd":50,"exp":600,"silver":400,"ybp":(0.60,15,35),"element":"火"},
    "魔教右使":   {"hp":1500,"atk":82,"def":43,"spd":52,"exp":600,"silver":400,"ybp":(0.60,15,35),"element":"暗"},
    "暗影教主":   {"hp":5000,"atk":120,"def":60,"spd":55,"exp":2000,"silver":1500,"ybp":(0.70,30,80),"element":"暗","boss":True},
}

MAP_AREAS = [
    {"name":"江州城","desc":"繁华商贸中心，侠客云集","enemies":["山贼","暗影刺客"],"color":(0.30,0.50,0.70)},
    {"name":"竹林深处","desc":"翠竹掩映，暗藏杀机","enemies":["暗影刺客","魔教弟子"],"color":(0.20,0.60,0.30)},
    {"name":"江边码头","desc":"漕运要道，鱼龙混杂","enemies":["山贼","山贼头目"],"color":(0.20,0.40,0.65)},
    {"name":"山道关隘","desc":"一夫当关，万夫莫开","enemies":["山贼头目","神秘剑客"],"color":(0.55,0.45,0.25)},
    {"name":"古庙遗迹","desc":"残碑断壁，藏有秘籍","enemies":["神秘剑客","魔教弟子"],"color":(0.45,0.35,0.55)},
    {"name":"魔教分舵","desc":"明教旁支，高手如云","enemies":["魔教弟子","魔教长老"],"color":(0.60,0.15,0.15)},
    {"name":"百草毒谷","desc":"瘴气弥漫，毒物遍地","enemies":["用毒高手","魔教长老"],"color":(0.30,0.55,0.20)},
    {"name":"少林寺","desc":"武学圣地，高僧辈出","enemies":["少林武僧","暗影护法"],"color":(0.65,0.60,0.30)},
    {"name":"暗影堡","desc":"暗影教总坛，终极决战之地","enemies":["暗影护法","魔教左使","魔教右使","暗影教主"],"color":(0.20,0.10,0.30)},
]

# ============================================================
# 存档系统
# ============================================================
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.json")

def save_game(data):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_game():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ============================================================
# 全局游戏状态
# ============================================================
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.silver = 1000
        self.yuanbao = 200
        self.insight_points = 0
        self.ng_plus = 0
        self.difficulty = 1  # 0简单 1普通 2困难 3地狱
        self.tower_floor = 0
        self.tower_highest = 0
        self.party = ["张无忌","令狐冲","段誉"]
        self.roster = list(HEROES_DATA.keys())
        self.hero_data = {}  # 每个侠客的运行时数据
        for name in HEROES_DATA:
            h = HEROES_DATA[name]
            self.hero_data[name] = {
                "level": 1, "exp": 0,
                "meridians": {},  # 8条经脉
                "refine": 0,
                "insight": 0,
                "skills": list(h["skills"]),
                "equipment": {"weapon":None,"armor":None},
                "favor": 0,
            }
            for m in ["ren","du","chong","dai","yangqiao","yinqiao","yangwei","yinwei"]:
                self.hero_data[name]["meridians"][m] = False
        self.inventory = {
            "items": {"回血丹":5,"内力丹":3,"醒酒汤":2},
            "materials": {"千年灵芝":0,"玄铁精金":0,"天山朱果":0},
            "skills_owned": [],
        }
        self.buffs = {}  # 临时buff
        self.achievements = []
        self.story_flags = {}
        self.current_area = 0
        self.ending_seen = False

    def get_diff_mult(self):
        return [1.0, 1.2, 1.5, 2.0][self.difficulty]

    def get_rare_mult(self):
        return [1.0, 1.5, 3.0, 5.0][self.difficulty]

    def get_yb_mult(self):
        return [1.0, 1.2, 1.5, 2.0][self.difficulty]

    def calc_hero_stat(self, name, stat):
        """计算侠客某属性（含所有加成）"""
        base = HEROES_DATA[name]
        hd = self.hero_data[name]
        lv = hd["level"]
        ng = 1.0 + self.ng_plus * 0.10

        if stat == "max_hp":
            val = base["hp"] + (lv-1)*20
        elif stat == "atk":
            val = base["atk"] + (lv-1)*3
        elif stat == "def":
            val = base["def"] + (lv-1)*2
        elif stat == "spd":
            val = base["spd"] + (lv-1)*1
        elif stat == "crit":
            val = base["crit"]
        elif stat == "dodge":
            val = base["dodge"]
        else:
            val = 0

        # 经脉 +5% each
        meridian_count = sum(1 for v in hd["meridians"].values() if v)
        meridian_mult = 1.0 + meridian_count * 0.05
        # 全通额外 +40%
        if meridian_count >= 8:
            meridian_mult += 0.40

        # 悟性
        insight_mult = 1.0 + hd["insight"] * 0.01
        # 精铸
        refine_mult = 1.0 + hd["refine"] * 0.10
        # 装备
        equip_mult = 1.0
        if stat in ("atk","max_hp"):
            w = hd["equipment"].get("weapon")
            if w: equip_mult += 0.15
            a = hd["equipment"].get("armor")
            if a: equip_mult += 0.10

        # 临时buff
        buff_mult = 1.0
        if "atk_buff" in self.buffs and stat == "atk":
            buff_mult += self.buffs["atk_buff"]
        if "def_buff" in self.buffs and stat == "def":
            buff_mult += self.buffs["def_buff"]

        final = val * meridian_mult * insight_mult * refine_mult * equip_mult * buff_mult * ng
        return int(final) if stat not in ("crit","dodge") else min(final, 0.95)

    def add_exp(self, name, amount):
        hd = self.hero_data[name]
        hd["exp"] += amount
        msgs = []
        while hd["exp"] >= 100 * (hd["level"] ** 1.5):
            hd["exp"] -= 100 * (hd["level"] ** 1.5)
            hd["level"] += 1
            msgs.append(f"{name} 突破至 {hd['level']} 级！")
        return msgs

    def to_dict(self):
        return {
            "silver":self.silver,"yuanbao":self.yuanbao,
            "insight_points":self.insight_points,"ng_plus":self.ng_plus,
            "difficulty":self.difficulty,"tower_floor":self.tower_floor,
            "tower_highest":self.tower_highest,"party":self.party,
            "roster":self.roster,"hero_data":self.hero_data,
            "inventory":self.inventory,"buffs":self.buffs,
            "achievements":self.achievements,"story_flags":self.story_flags,
            "current_area":self.current_area,"ending_seen":self.ending_seen,
        }

    def from_dict(self, d):
        for k,v in d.items():
            if hasattr(self, k):
                setattr(self, k, v)

# ============================================================
# UI 辅助
# ============================================================
def C(color, alpha=1.0):
    """将0-1范围的RGBA颜色转为Kivy格式"""
    if len(color) == 4:
        return color
    return (color[0], color[1], color[2], alpha)

def make_label(text, size=18, color=None, halign="center", bold=False, **kw):
    if color is None: color = COLORS['ink']
    return Label(text=text, font_size=size, color=color, halign=halign,
                 valign="middle", bold=bold, text_size=(kw.pop("width",400),None),
                 size_hint_y=None, height=size+12, **kw)

def make_btn(text, on_press=None, bg=None, color=None, size_hint=(1, None), height=50, font_size=18, **kw):
    if bg is None: bg = COLORS['gold_dim']
    if color is None: color = (0.1,0.1,0.1,1)
    btn = Button(text=text, size_hint=size_hint, height=height,
                 font_size=font_size, color=color, background_color=bg,
                 background_normal='', background_down='', **kw)
    if on_press: btn.bind(on_press=on_press)
    return btn

def make_panel(padding=12, spacing=8, **kw):
    p = BoxLayout(orientation="vertical", padding=padding, spacing=spacing, **kw)
    return p

# ============================================================
# 场景：主菜单
# ============================================================
class MainMenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = make_panel(padding=30, spacing=15)
        layout.add_widget(Widget(size_hint=(1, 0.1)))

        # 标题
        title = make_label("小武侠传说", size=52, color=COLORS['gold'], bold=True)
        layout.add_widget(title)
        subtitle = make_label("无尽武道篇", size=28, color=COLORS['gold_dim'])
        layout.add_widget(subtitle)
        layout.add_widget(Widget(size_hint=(1, 0.05)))

        # 难度选择
        diff_layout = BoxLayout(size_hint=(1,None), height=55, spacing=10)
        diff_layout.add_widget(make_label("难度：", size=18, halign="right", width=80))
        self.diff_btns = []
        diff_names = ["简单","普通","困难","地狱"]
        diff_colors = [COLORS['green'], COLORS['blue'], COLORS['orange'], COLORS['red']]
        for i,n in enumerate(diff_names):
            b = make_btn(n, bg=diff_colors[i], height=40, font_size=16, width=80)
            b.bind(on_press=lambda btn,i=i: self._set_diff(i))
            self.diff_btns.append(b)
            diff_layout.add_widget(b)
        layout.add_widget(diff_layout)
        layout.add_widget(Widget(size_hint=(1, 0.02)))

        # 主按钮
        for text, action in [
            ("▶ 开始游戏", self._start),
            ("⚔ 继续游戏", self._continue),
            ("📖 游戏说明", self._help),
            ("❌ 退出", self._quit),
        ]:
            layout.add_widget(make_btn(text, on_press=action, height=56, font_size=22,
                                       bg=COLORS['red'] if "退出" in text else COLORS['gold_dim']))

        layout.add_widget(Widget(size_hint=(1, 0.1)))
        self.add_widget(layout)
        self._set_diff(1)

    def _set_diff(self, idx):
        gs.difficulty = idx
        for i,b in enumerate(self.diff_btns):
            b.background_color = [COLORS['green'],COLORS['blue'],COLORS['orange'],COLORS['red']][i]
            if i != idx:
                b.opacity = 0.4
            else:
                b.opacity = 1.0

    def _start(self, *a):
        gs.reset()
        gs.difficulty = self._selected_diff
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

    def _continue(self, *a):
        d = load_game()
        if d:
            gs.from_dict(d)
            self.manager.get_screen("world").refresh()
            self.manager.current = "world"
        else:
            popup("暂无存档", "还没有存档，请先开始新游戏")

    def _help(self, *a):
        popup("游戏说明",
              "《小武侠传说·无尽武道篇》\n\n"
              "操作：点击按钮进行游戏\n\n"
              "核心玩法：\n"
              "· 探索地图 → 随机遇敌 → 回合制战斗\n"
              "· 打怪掉落银两/元宝/材料/秘籍\n"
              "· 元宝商城购买丹药/装备/材料\n"
              "· 经脉修炼/悟性提升/装备精铸\n"
              "· 挑战塔无限爬层，每层有奖励\n"
              "· 通关结局后进入NG+，属性永久+10%\n"
              "· 难度越高，经验/银两/元宝/极品率越高\n\n"
              "祝你在江湖中闯出一番天地！")

    def _quit(self, *a):
        App.get_running_app().stop()

    @property
    def _selected_diff(self):
        return gs.difficulty

# ============================================================
# 场景：世界地图
# ============================================================
class WorldMapScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.main_layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.main_layout)

    def refresh(self):
        self.main_layout.clear_widgets()
        # 顶部状态栏
        top = BoxLayout(size_hint=(1,None), height=70, spacing=10)
        top.add_widget(make_label(f"💰 {gs.silver}", size=20, color=COLORS['gold'], width=120))
        top.add_widget(make_label(f"💎 {gs.yuanbao}", size=20, color=COLORS['cyan'], width=120))
        top.add_widget(make_label(f"🧠 {gs.insight_points}", size=20, color=COLORS['purple'], width=100))
        top.add_widget(make_label(f"🔄 NG+{gs.ng_plus}", size=20, color=COLORS['pink'], width=100))
        diff_name = ["简单","普通","困难","地狱"][gs.difficulty]
        top.add_widget(make_label(f"⚙ {diff_name}", size=18, color=COLORS['orange'], width=80))
        self.main_layout.add_widget(top)

        # 队伍信息
        party_box = BoxLayout(size_hint=(1,None), height=100, spacing=8)
        for name in gs.party:
            hd = gs.hero_data[name]
            card = BoxLayout(orientation="vertical", size_hint=(1,None), height=90,
                            padding=6, spacing=2)
            card.add_widget(make_label(name, size=16, color=COLORS['gold'], bold=True, width=120))
            card.add_widget(make_label(f"Lv.{hd['level']} HP:{gs.calc_hero_stat(name,'max_hp')}", size=13, width=120))
            card.add_widget(make_label(f"ATK:{gs.calc_hero_stat(name,'atk')} DEF:{gs.calc_hero_stat(name,'def')}", size=12, color=COLORS['ink_dim'], width=120))
            party_box.add_widget(card)
        self.main_layout.add_widget(party_box)

        # 地图区域
        self.main_layout.add_widget(make_label("🗺️ 江湖地图", size=22, color=COLORS['gold'], height=36))
        areas_grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        areas_grid.bind(minimum_height=areas_grid.setter('height'))
        for i, area in enumerate(MAP_AREAS):
            btn = make_btn(f"{area['name']}\n<{area['desc']}>", height=80, font_size=15,
                           bg=area["color"])
            btn.bind(on_press=lambda b,i=i: self._enter_area(i))
            areas_grid.add_widget(btn)
        self.main_layout.add_widget(areas_grid)

        # 功能按钮
        self.main_layout.add_widget(Widget(size_hint=(1, 0.02)))
        func_grid = GridLayout(cols=3, spacing=10, size_hint=(1,None), height=55)
        for text, screen in [
            ("⚔ 战斗", "battle"), ("🗼 挑战塔", "tower"),
            ("🏪 商城", "shop"), ("🔮 经脉", "meridian"),
            ("🧠 悟性", "insight"), ("⚒ 精铸", "equip"),
            ("📜 武学", "skill_book"), ("💊 背包", "inventory"),
            ("💾 存档", None),
        ]:
            if screen:
                b = make_btn(text, height=50, font_size=16, bg=COLORS['bg_card'])
                b.bind(on_press=lambda b,s=screen: self._goto(s))
                func_grid.add_widget(b)
            else:
                b = make_btn(text, height=50, font_size=16, bg=COLORS['green'])
                b.bind(on_press=self._save)
                func_grid.add_widget(b)
        self.main_layout.add_widget(func_grid)

    def _enter_area(self, idx):
        gs.current_area = idx
        self.manager.get_screen("battle").set_explore_mode(idx)
        self.manager.current = "battle"

    def _goto(self, screen):
        if screen == "battle":
            self.manager.get_screen("battle").set_explore_mode(gs.current_area)
        elif screen == "tower":
            self.manager.get_screen("tower").refresh()
        elif screen == "shop":
            self.manager.get_screen("shop").refresh()
        elif screen == "meridian":
            self.manager.get_screen("meridian").refresh()
        elif screen == "insight":
            self.manager.get_screen("insight").refresh()
        elif screen == "equip":
            self.manager.get_screen("equip").refresh()
        elif screen == "skill_book":
            self.manager.get_screen("skill_book").refresh()
        elif screen == "inventory":
            self.manager.get_screen("inventory").refresh()
        self.manager.current = screen

    def _save(self, *a):
        save_game(gs.to_dict())
        popup("存档成功", "游戏已保存到本地")

# ============================================================
# 战斗系统
# ============================================================
class BattleScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mode = "explore"  # explore / tower
        self.enemy = None
        self.turn = 0
        self.log_lines = []
        self.layout = make_panel(padding=12, spacing=8)
        self.add_widget(self.layout)

    def set_explore_mode(self, area_idx):
        self.mode = "explore"
        self.area_idx = area_idx
        self._start_battle()

    def set_tower_mode(self, floor):
        self.mode = "tower"
        self.tower_floor = floor
        self._start_tower_battle(floor)

    def _gen_enemy(self, area_idx):
        area = MAP_AREAS[area_idx]
        name = random.choice(area["enemies"])
        # Boss only in final area
        if area_idx == len(MAP_AREAS)-1 and random.random() < 0.15:
            name = "暗影教主"
        e = dict(ENEMIES_DATA[name])
        e["name"] = name
        diff_m = gs.get_diff_mult()
        for k in ["hp","atk","def"]:
            e[k] = int(e[k] * diff_m)
        return e

    def _start_battle(self):
        self.enemy = self._gen_enemy(self.area_idx)
        self.turn = 0
        self.log_lines = [f"遭遇 【{self.enemy['name']}】！"]
        self._refresh_ui()

    def _start_tower_battle(self, floor):
        # 塔敌人指数增长
        base_names = list(ENEMIES_DATA.keys())
        base_names.remove("暗影教主")
        name = random.choice(base_names)
        if floor % 10 == 0:
            name = "暗影教主"
        e = dict(ENEMIES_DATA[name])
        e["name"] = f"塔{floor}层·{name}"
        growth = 1.08 if floor % 10 != 0 else 1.15
        mult = 1.0
        if floor > 10:
            mult = (growth ** (floor-10))
        else:
            mult = 1.0 + (floor-1)*0.2
        mult *= (1.0 + gs.ng_plus * 0.10)
        for k in ["hp","atk","def"]:
            e[k] = int(e[k] * mult)
        if floor % 10 == 0:
            e["hp"] *= 5; e["atk"] *= 2
        self.enemy = e
        self.turn = 0
        self.log_lines = [f"🗼 第 {floor} 层 — 迎战 【{e['name']}】！"]
        self._refresh_ui()

    def _refresh_ui(self):
        self.layout.clear_widgets()
        # 敌人信息
        e = self.enemy
        enemy_box = BoxLayout(size_hint=(1,None), height=90, spacing=10)
        enemy_box.add_widget(make_label(f"👹 {e['name']}", size=20, color=COLORS['red_bright'], bold=True, width=300))
        enemy_box.add_widget(make_label(f"HP: {e['hp']}", size=18, color=COLORS['ink'], width=150))
        enemy_box.add_widget(make_label(f"ATK:{e['atk']} DEF:{e['def']}", size=14, color=COLORS['ink_dim'], width=200))
        self.layout.add_widget(enemy_box)

        # 我方信息
        party_box = BoxLayout(size_hint=(1,None), height=100, spacing=8)
        for name in gs.party:
            hd = gs.hero_data[name]
            hp = gs.calc_hero_stat(name,"max_hp")
            atk = gs.calc_hero_stat(name,"atk")
            card = BoxLayout(orientation="vertical", size_hint=(1,None), height=90, padding=5, spacing=2)
            card.add_widget(make_label(f"{name} Lv.{hd['level']}", size=14, color=COLORS['gold'], width=130))
            card.add_widget(make_label(f"HP:{hp} ATK:{atk}", size=12, width=130))
            card.add_widget(make_label(f"DEF:{gs.calc_hero_stat(name,'def')} SPD:{gs.calc_hero_stat(name,'spd')}", size=11, color=COLORS['ink_dim'], width=130))
            party_box.add_widget(card)
        self.layout.add_widget(party_box)

        # 战斗日志
        log_text = "\n".join(self.log_lines[-6:])
        self.layout.add_widget(make_label(log_text, size=14, color=COLORS['ink_dim'], halign="left", width=600, height=100))

        # 操作按钮
        btn_box = BoxLayout(size_hint=(1,None), height=55, spacing=10)
        for text, action in [
            ("⚔ 攻击", self._do_attack),
            ("🛡 防御", self._do_defend),
            ("💨 逃跑", self._do_flee),
        ]:
            b = make_btn(text, height=50, font_size=18, bg=COLORS['red'] if "攻击" in text else COLORS['bg_card'])
            b.bind(on_press=action)
            btn_box.add_widget(b)
        self.layout.add_widget(btn_box)

        # 返回按钮
        back = make_btn("← 返回地图" if self.mode=="explore" else "← 退出挑战塔",
                        height=40, font_size=14, bg=COLORS['bg_card'])
        back.bind(on_press=self._go_back)
        self.layout.add_widget(back)

    def _do_attack(self, *a):
        if not self.enemy: return
        self.turn += 1
        # 我方攻击
        total_dmg = 0
        for name in gs.party:
            atk = gs.calc_hero_stat(name,"atk")
            spd = gs.calc_hero_stat(name,"spd")
            crit_rate = gs.calc_hero_stat(name,"crit")
            # 速度影响连击
            hits = 1 + int(spd / 50)
            dmg = 0
            for _ in range(hits):
                is_crit = random.random() < crit_rate
                base_dmg = max(1, atk - self.enemy["def"]//2)
                if is_crit: base_dmg = int(base_dmg * 1.5)
                dmg += base_dmg
            total_dmg += dmg
            if is_crit:
                self.log_lines.append(f"  {name} 暴击！造成 {dmg} 伤害")
            else:
                self.log_lines.append(f"  {name} 攻击造成 {dmg} 伤害")
        self.enemy["hp"] -= total_dmg
        self.log_lines.append(f"合计造成 {total_dmg} 伤害，敌人剩余 HP: {max(0,self.enemy['hp'])}")

        if self.enemy["hp"] <= 0:
            self._battle_win()
            return

        # 敌人反击
        self._enemy_attack()

    def _do_defend(self, *a):
        self.log_lines.append("我方全力防御，本回合伤害减半")
        self._enemy_attack(defense_mode=True)

    def _do_flee(self, *a):
        if random.random() < 0.5:
            self.log_lines.append("成功逃脱！")
            self._go_back()
        else:
            self.log_lines.append("逃跑失败！")
            self._enemy_attack()

    def _enemy_attack(self, defense_mode=False):
        e = self.enemy
        dmg = e["atk"]
        if defense_mode: dmg = dmg // 2
        # 分摊伤害给全队
        per = dmg // len(gs.party) if gs.party else dmg
        self.log_lines.append(f"👹 {e['name']} 反击，造成 {dmg} 伤害")
        self._refresh_ui()
        # 检查死亡（简化：不真的扣血，只看回合）
        if self.turn >= 20:
            self.log_lines.append("战斗超时，双方罢手")
            self._go_back()

    def _battle_win(self):
        e = self.enemy
        diff_m = gs.get_diff_mult()
        yb_m = gs.get_yb_mult()
        rare_m = gs.get_rare_mult()

        exp_gain = int(e.get("exp",50) * diff_m)
        silver_gain = int(e.get("exp",50) * diff_m * 0.8)
        yb_chance, yb_min, yb_max = e.get("ybp", (0.1,1,3))
        yb_gain = 0
        if random.random() < yb_chance * yb_m:
            yb_gain = random.randint(yb_min, yb_max)

        gs.silver += silver_gain
        gs.yuanbao += yb_gain

        msgs = [f"🎉 击败 【{e['name']}】！"]
        msgs.append(f"  获得经验: {exp_gain}")
        msgs.append(f"  获得银两: {silver_gain}")
        if yb_gain > 0:
            msgs.append(f"  💎 掉落元宝: {yb_gain}")

        # 分配经验
        for name in gs.party:
            lvl_msgs = gs.add_exp(name, exp_gain)
            msgs.extend(lvl_msgs)

        # 掉落物品
        drops = []
        # 丹药
        if random.random() < 0.30:
            item = random.choice(["回血丹","内力丹","醒酒汤"])
            gs.inventory["items"][item] = gs.inventory["items"].get(item,0) + 1
            drops.append(item)
        # 材料
        if random.random() < 0.20 * rare_m:
            mat = random.choice(["千年灵芝","玄铁精金","天山朱果"])
            gs.inventory["materials"][mat] = gs.inventory["materials"].get(mat,0) + 1
            drops.append(mat)
        # 秘籍
        if random.random() < 0.05 * rare_m:
            skill = random.choice(list(SKILLS_DATA.keys()))
            if skill not in gs.inventory["skills_owned"]:
                gs.inventory["skills_owned"].append(skill)
                drops.append(f"📖{skill}")

        if drops:
            msgs.append(f"  掉落物品: {', '.join(drops)}")

        # 幸运符buff
        if "lucky" in gs.buffs:
            gs.yuanbao += yb_gain  # 翻倍
            msgs.append(f"  🍀 幸运符触发，元宝翻倍！")

        # 塔模式奖励
        if self.mode == "tower":
            floor = self.tower_floor
            gs.tower_floor = floor + 1
            gs.tower_highest = max(gs.tower_highest, gs.tower_floor)
            insight_gain = 1
            gs.insight_points += insight_gain
            msgs.append(f"  🧠 获得悟性点 +{insight_gain}")
            if floor % 5 == 0:
                gs.inventory["materials"]["玄铁精金"] += 2
                msgs.append(f"  ⭐ 每5层奖励：玄铁精金+2")
            if floor % 10 == 0:
                gs.yuanbao += int(50 * yb_m)
                gs.inventory["materials"]["千年灵芝"] += 3
                msgs.append(f"  🏆 每10层大礼包！元宝+{int(50*yb_m)}，千年灵芝+3")
            # 检查是否到100层
            if floor == 100:
                msgs.append("  🎊 百层通关！获得【武神】称号！")

        self.log_lines.extend(msgs)
        self._refresh_ui()

        # 检查结局
        if e["name"] == "暗影教主" and self.mode == "explore":
            Clock.schedule_once(lambda dt: self._trigger_ending(), 1.5)

        # 探索模式自动继续
        if self.mode == "explore":
            Clock.schedule_once(lambda dt: self._next_explore(), 2.0)

    def _next_explore(self):
        # 随机奇遇
        r = random.random()
        if r < 0.25:
            self._trigger_event()
        else:
            self._start_battle()

    def _trigger_event(self):
        events = [
            ("陌路道人", "一位道人拦住你去路：\"小友，可愿品尝老道炼制的丹药？\"",
             lambda: self._event_reward("丹药", "千年灵芝", 1)),
            ("受伤侠客", "一位侠客倒在路边，气息微弱...",
             lambda: self._event_reward("救助", "回血丹", 3)),
            ("古朴木箱", "路边发现一个布满灰尘的木箱！",
             lambda: self._event_reward("开启", "银两", random.randint(50,200))),
            ("醉卧桥头", "桥头一位醉汉对你招手：\"来...喝酒！\"",
             lambda: self._event_reward("共饮", "醒酒汤", 2)),
            ("神秘商人", "一位行脚商人神神秘秘地掏出一件物品...",
             lambda: self._event_reward("购买", "玄铁精金", 1)),
            ("竹林隐士", "竹林深处一位隐士正在打坐，睁开眼看向你...",
             lambda: self._event_reward("论道", "天山朱果", 1)),
        ]
        name, desc, action = random.choice(events)
        self.log_lines.append(f"💬 【{name}】{desc}")
        action()
        self._refresh_ui()

    def _event_reward(self, kind, item, amount):
        if item == "银两":
            gs.silver += amount
            self.log_lines.append(f"  获得银两 +{amount}")
        else:
            if item in gs.inventory["items"]:
                gs.inventory["items"][item] += amount
            elif item in gs.inventory["materials"]:
                gs.inventory["materials"][item] += amount
            else:
                gs.inventory["items"][item] = amount
            self.log_lines.append(f"  获得 {item} +{amount}")

    def _trigger_ending(self):
        gs.ending_seen = True
        self.manager.current = "ending"

    def _go_back(self, *a):
        if self.mode == "tower":
            self.manager.get_screen("tower").refresh()
            self.manager.current = "tower"
        else:
            self.manager.get_screen("world").refresh()
            self.manager.current = "world"

# ============================================================
# 挑战塔
# ============================================================
class TowerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("🗼 武神塔 — 无限挑战", size=26, color=COLORS['gold'], bold=True, height=40))
        self.layout.add_widget(make_label(f"当前层数: {gs.tower_floor}  |  最高纪录: {gs.tower_highest}", size=18, color=COLORS['cyan'], height=30))

        info = (
            "规则：每层消耗1点体力（或5元宝），击败守卫获得奖励\n"
            "每5层：必掉紫装材料 | 每10层：传说大礼包\n"
            "每100层：专属称号奖励 | 层数无限，属性指数增长"
        )
        self.layout.add_widget(make_label(info, size=14, color=COLORS['ink_dim'], height=60))

        # 挑战按钮
        btn_box = BoxLayout(size_hint=(1,None), height=60, spacing=10)
        challenge = make_btn(f"⚔ 挑战第 {gs.tower_floor+1} 层", height=55, font_size=20, bg=COLORS['red'])
        challenge.bind(on_press=self._challenge)
        btn_box.add_widget(challenge)

        sweep = make_btn(f"⏩ 扫荡5层 (50元宝)", height=55, font_size=18, bg=COLORS['purple'])
        sweep.bind(on_press=self._sweep)
        btn_box.add_widget(sweep)
        self.layout.add_widget(btn_box)

        # 返回
        back = make_btn("← 返回江湖", height=45, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _challenge(self, *a):
        floor = gs.tower_floor + 1
        # 检查体力/元宝
        if floor > 1 and random.random() < 0.3:
            if gs.yuanbao >= 5:
                gs.yuanbao -= 5
            else:
                # 没有元宝也能打，只是消耗"体力"
                pass
        self.manager.get_screen("battle").set_tower_mode(floor)
        self.manager.current = "battle"

    def _sweep(self, *a):
        if gs.yuanbao < 50:
            popup("元宝不足", "扫荡需要50元宝")
            return
        gs.yuanbao -= 50
        start = gs.tower_floor
        end = min(start + 5, start + 5)
        msgs = [f"⏩ 扫荡第 {start+1}~{end} 层..."]
        for f in range(start+1, end+1):
            gs.tower_floor = f
            gs.tower_highest = max(gs.tower_highest, f)
            gs.insight_points += 1
            gs.silver += f * 10
            if f % 5 == 0:
                gs.inventory["materials"]["玄铁精金"] = gs.inventory["materials"].get("玄铁精金",0) + 2
                msgs.append(f"  第{f}层 ★ 玄铁精金+2")
            if f % 10 == 0:
                gs.yuanbao += 50
                gs.inventory["materials"]["千年灵芝"] = gs.inventory["materials"].get("千年灵芝",0) + 3
                msgs.append(f"  第{f}层 🏆 大礼包！元宝+50，灵芝+3")
        msgs.append(f"扫荡完成！当前层数: {gs.tower_floor}")
        popup("扫荡结果", "\n".join(msgs))
        self.refresh()

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 商城
# ============================================================
class ShopScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)
        self.category = "丹药"

    def refresh(self):
        self.layout.clear_widgets()
        top = BoxLayout(size_hint=(1,None), height=55, spacing=10)
        top.add_widget(make_label(f"💰 {gs.silver}", size=20, color=COLORS['gold'], width=150))
        top.add_widget(make_label(f"💎 {gs.yuanbao}", size=20, color=COLORS['cyan'], width=150))
        self.layout.add_widget(top)

        cats = ["丹药","材料","装备","秘籍","特殊"]
        cat_box = BoxLayout(size_hint=(1,None), height=45, spacing=8)
        for c in cats:
            b = make_btn(c, height=40, font_size=15, bg=COLORS['purple'] if c==self.category else COLORS['bg_card'])
            b.bind(on_press=lambda b,c=c: self._set_cat(c))
            cat_box.add_widget(b)
        self.layout.add_widget(cat_box)

        # 商品列表
        scroll = ScrollView(size_hint=(1,1))
        goods_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=6)
        goods_box.bind(minimum_height=goods_box.setter('height'))

        items = self._get_goods(self.category)
        for item in items:
            row = BoxLayout(size_hint=(1,None), height=55, spacing=8)
            row.add_widget(make_label(item["name"], size=16, color=item.get("color",COLORS['ink']), width=180))
            row.add_widget(make_label(item["desc"], size=12, color=COLORS['ink_dim'], width=250))
            price_text = f"💎{item['price']}"
            buy = make_btn(price_text, height=42, font_size=14, width=80,
                           bg=COLORS['gold'] if gs.yuanbao >= item['price'] else COLORS['bg_card'])
            buy.bind(on_press=lambda b,item=item: self._buy(item))
            row.add_widget(buy)
            goods_box.add_widget(row)
        scroll.add_widget(goods_box)
        self.layout.add_widget(scroll)

        back = make_btn("← 返回江湖", height=45, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _set_cat(self, cat):
        self.category = cat
        self.refresh()

    def _get_goods(self, cat):
        all_goods = {
            "丹药": [
                {"name":"九转还魂丹","desc":"复活阵亡侠客，恢复50%HP","price":50,"effect":"revive","color":COLORS['red']},
                {"name":"暴击神丹","desc":"全局暴击率+10%，持续5场","price":30,"effect":"crit_buff","color":COLORS['orange']},
                {"name":"金刚神丹","desc":"全局防御+20%，持续5场","price":30,"effect":"def_buff","color":COLORS['green']},
                {"name":"回血丹","desc":"恢复200点HP","price":5,"effect":"heal","color":COLORS['green']},
                {"name":"内力丹","desc":"恢复100点内力","price":8,"effect":"mana","color":COLORS['blue']},
                {"name":"醒酒汤","desc":"解除醉酒状态","price":3,"effect":"sober","color":COLORS['ink_dim']},
            ],
            "材料": [
                {"name":"千年灵芝","desc":"经脉修炼必备材料","price":40,"effect":"material_灵芝","color":COLORS['green']},
                {"name":"玄铁精金","desc":"装备精铸核心材料","price":60,"effect":"material_精金","color":COLORS['gold']},
                {"name":"天山朱果","desc":"增加1点悟性","price":100,"effect":"insight","color":COLORS['purple']},
                {"name":"龙鳞碎片","desc":"合成神兵材料","price":80,"effect":"material_龙鳞","color":COLORS['cyan']},
            ],
            "装备": [
                {"name":"屠龙刀","desc":"攻击+150，屠龙之威","price":500,"effect":"equip_屠龙刀","color":COLORS['red']},
                {"name":"倚天剑","desc":"攻击+140，削铁如泥","price":450,"effect":"equip_倚天剑","color":COLORS['blue']},
                {"name":"软猬甲","desc":"防御+100，荆棘反伤","price":300,"effect":"equip_软猬甲","color":COLORS['green']},
                {"name":"金丝手套","desc":"暴击率+8%","price":200,"effect":"equip_金丝手套","color":COLORS['gold']},
                {"name":"夜行衣","desc":"闪避率+10%","price":180,"effect":"equip_夜行衣","color":COLORS['purple']},
            ],
            "秘籍": [
                {"name":"《九阴真经》","desc":"内功绝学，全属性+15%","price":300,"effect":"skill_九阴真经","color":COLORS['orange']},
                {"name":"《独孤九剑》","desc":"外功绝学，无视防御30%","price":350,"effect":"skill_独孤剑法","color":COLORS['red']},
                {"name":"秘籍碎片×10","desc":"合成随机紫色秘籍","price":150,"effect":"skill_fragments","color":COLORS['purple']},
                {"name":"抽卡券×3","desc":"用于秘籍十连抽","price":200,"effect":"gacha_ticket","color":COLORS['cyan']},
            ],
            "特殊": [
                {"name":"幸运符","desc":"下一场战斗所有掉落翻倍","price":25,"effect":"lucky","color":COLORS['gold']},
                {"name":"传功卷轴","desc":"指定侠客直接升5级","price":120,"effect":"level_up","color":COLORS['pink']},
                {"name":"洗髓丹","desc":"重置一条经脉，返还50%材料","price":80,"effect":"reset_meridian","color":COLORS['cyan']},
                {"name":"悟性丹","desc":"全体侠客悟性+1","price":200,"effect":"all_insight","color":COLORS['purple']},
            ],
        }
        return all_goods.get(cat, [])

    def _buy(self, item):
        if gs.yuanbao < item["price"]:
            popup("元宝不足", f"需要 {item['price']} 元宝，当前只有 {gs.yuanbao}")
            return
        gs.yuanbao -= item["price"]
        eff = item["effect"]
        if eff == "insight":
            gs.insight_points += 1
        elif eff == "heal":
            popup("购买成功", f"获得 {item['name']}")
        elif eff == "lucky":
            gs.buffs["lucky"] = True
        elif eff == "crit_buff":
            gs.buffs["atk_buff"] = gs.buffs.get("atk_buff",0) + 0.10
            gs.buffs["crit_buff_battles"] = 5
        elif eff == "def_buff":
            gs.buffs["def_buff"] = gs.buffs.get("def_buff",0) + 0.20
            gs.buffs["def_buff_battles"] = 5
        elif eff.startswith("material_"):
            mat = eff.split("_",1)[1]
            mat_map = {"灵芝":"千年灵芝","精金":"玄铁精金","龙鳞":"龙鳞碎片"}
            real_name = mat_map.get(mat, mat)
            gs.inventory["materials"][real_name] = gs.inventory["materials"].get(real_name,0)+1
        elif eff.startswith("equip_"):
            equip = eff.split("_",1)[1]
            # 给第一个侠客装备
            name = gs.party[0]
            slot = "weapon" if equip in ["屠龙刀","倚天剑","金丝手套"] else "armor"
            gs.hero_data[name]["equipment"][slot] = equip
        elif eff.startswith("skill_"):
            skill = eff.split("_",1)[1]
            if skill not in gs.inventory["skills_owned"]:
                gs.inventory["skills_owned"].append(skill)
        elif eff == "skill_fragments":
            gs.inventory["materials"]["秘籍碎片"] = gs.inventory["materials"].get("秘籍碎片",0)+10
        elif eff == "gacha_ticket":
            gs.inventory["materials"]["抽卡券"] = gs.inventory["materials"].get("抽卡券",0)+3
        elif eff == "level_up":
            for name in gs.party:
                gs.hero_data[name]["level"] += 5
        elif eff == "all_insight":
            for name in gs.party:
                gs.hero_data[name]["insight"] += 1
        elif eff == "reset_meridian":
            gs.inventory["materials"]["洗髓丹"] = gs.inventory["materials"].get("洗髓丹",0)+1
        popup("购买成功", f"✅ {item['name']}\n{item['desc']}")
        self.refresh()

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 经脉系统
# ============================================================
class MeridianScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)
        self.selected_hero = 0

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("🔮 经脉修炼", size=24, color=COLORS['purple'], bold=True, height=36))

        # 选择侠客
        hero_box = BoxLayout(size_hint=(1,None), height=55, spacing=8)
        for i, name in enumerate(gs.party):
            b = make_btn(name, height=45, font_size=14,
                         bg=COLORS['gold'] if i==self.selected_hero else COLORS['bg_card'])
            b.bind(on_press=lambda b,i=i: self._select(i))
            hero_box.add_widget(b)
        self.layout.add_widget(hero_box)

        name = gs.party[self.selected_hero]
        hd = gs.hero_data[name]
        meridians = hd["meridians"]
        lingzhi = gs.inventory["materials"].get("千年灵芝",0)

        opened = sum(1 for v in meridians.values() if v)
        self.layout.add_widget(make_label(f"{name} — 已通 {opened}/8 条经脉 | 灵芝: {lingzhi}", size=16, color=COLORS['ink'], height=30))

        # 经脉网格
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        meridian_names = {
            "ren":"任脉","du":"督脉","chong":"冲脉","dai":"带脉",
            "yangqiao":"阳跷脉","yinqiao":"阴跷脉","yangwei":"阳维脉","yinwei":"阴维脉",
        }
        for mid, mname in meridian_names.items():
            unlocked = meridians.get(mid, False)
            cost = 1 + opened * 2  # 递增
            row = BoxLayout(size_hint=(1,None), height=50, spacing=8)
            color = COLORS['green'] if unlocked else COLORS['ink_dim']
            row.add_widget(make_label(f"{'✅' if unlocked else '🔒'} {mname}", size=15, color=color, width=120))
            row.add_widget(make_label(f"消耗: {cost}灵芝", size=12, color=COLORS['ink_dim'], width=100))
            if not unlocked:
                can_afford = 灵芝 >= cost
                b = make_btn(f"打通", height=40, font_size=14,
                             bg=COLORS['green'] if can_afford else COLORS['bg_card'])
                b.bind(on_press=lambda b,mid=mid,cost=cost: self._open_meridian(mid,cost))
                row.add_widget(b)
            grid.add_widget(row)
        self.layout.add_widget(grid)

        # 全通奖励提示
        if opened >= 8:
            self.layout.add_widget(make_label("🌟 八脉全通！全属性额外 +40%", size=16, color=COLORS['gold'], height=30))

        # 洗髓
        reset_btn = make_btn(f"洗髓重置 (返还50%灵芝)", height=45, font_size=15, bg=COLORS['red'])
        reset_btn.bind(on_press=self._reset)
        self.layout.add_widget(reset_btn)

        back = make_btn("← 返回", height=40, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _select(self, idx):
        self.selected_hero = idx
        self.refresh()

    def _open_meridian(self, mid, cost):
        name = gs.party[self.selected_hero]
        hd = gs.hero_data[name]
        if gs.inventory["materials"].get("千年灵芝",0) >= cost:
            gs.inventory["materials"]["千年灵芝"] -= cost
            hd["meridians"][mid] = True
            popup("经脉打通", f"{name} 的 {mid} 已打通！全属性 +5%")
            self.refresh()
        else:
            popup("灵芝不足", f"需要 {cost} 个千年灵芝")

    def _reset(self, *a):
        name = gs.party[self.selected_hero]
        hd = gs.hero_data[name]
        opened = sum(1 for v in hd["meridians"].values() if v)
        if opened == 0: return
        refund = opened // 2
        gs.inventory["materials"]["千年灵芝"] = gs.inventory["materials"].get("千年灵芝",0) + refund
        for m in hd["meridians"]: hd["meridians"][m] = False
        popup("洗髓完成", f"返还 {refund} 个千年灵芝，经脉已重置")
        self.refresh()

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 悟性系统
# ============================================================
class InsightScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("🧠 悟性提升", size=24, color=COLORS['purple'], bold=True, height=36))
        self.layout.add_widget(make_label(f"💎 元宝: {gs.yuanbao}  |  🧠 悟性点: {gs.insight_points}", size=18, color=COLORS['ink'], height=30))

        # 选择侠客
        self.layout.add_widget(make_label("选择侠客：", size=16, color=COLORS['gold'], height=26))
        hero_box = BoxLayout(size_hint=(1,None), height=55, spacing=8)
        self.selected = getattr(self, 'selected', 0)
        for i, name in enumerate(gs.party):
            b = make_btn(name, height=45, font_size=14,
                         bg=COLORS['gold'] if i==self.selected else COLORS['bg_card'])
            b.bind(on_press=lambda b,i=i: self._select(i))
            hero_box.add_widget(b)
        self.layout.add_widget(hero_box)

        name = gs.party[self.selected]
        hd = gs.hero_data[name]
        bonus = hd["insight"] * 1  # 每点+1%
        self.layout.add_widget(make_label(f"{name} 当前悟性加成: 全属性 +{bonus}%", size=16, color=COLORS['green'], height=30))

        # 加点按钮
        btn_box = BoxLayout(size_hint=(1,None), height=55, spacing=10)
        for text, amount in [("+1",1),("+10",10),("+50",50)]:
            can = gs.insight_points >= amount
            b = make_btn(f"{text} 悟性", height=48, font_size=16,
                         bg=COLORS['purple'] if can else COLORS['bg_card'])
            b.bind(on_press=lambda b,amt=amount: self._add(amt))
            btn_box.add_widget(b)
        self.layout.add_widget(btn_box)

        # 倾囊
        all_btn = make_btn(f"倾囊投入 (全部 {gs.insight_points} 点)", height=48, font_size=16, bg=COLORS['red'])
        all_btn.bind(on_press=lambda *a: self._add(gs.insight_points))
        self.layout.add_widget(all_btn)

        # 重置
        reset_btn = make_btn(f"重置悟性 (返还50%)", height=42, font_size=14, bg=COLORS['bg_card'])
        reset_btn.bind(on_press=self._reset)
        self.layout.add_widget(reset_btn)

        back = make_btn("← 返回", height=40, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _select(self, idx):
        self.selected = idx
        self.refresh()

    def _add(self, amount):
        if amount <= 0: return
        name = gs.party[self.selected]
        if gs.insight_points < amount:
            popup("悟性点不足", f"只有 {gs.insight_points} 点")
            return
        gs.insight_points -= amount
        gs.hero_data[name]["insight"] += amount
        popup("悟性提升", f"{name} 全属性 +{amount}%！")
        self.refresh()

    def _reset(self, *a):
        name = gs.party[self.selected]
        hd = gs.hero_data[name]
        if hd["insight"] == 0: return
        refund = hd["insight"] // 2
        hd["insight"] = 0
        gs.insight_points += refund
        popup("重置完成", f"返还 {refund} 悟性点")
        self.refresh()

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 装备精铸
# ============================================================
class EquipScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)
        self.selected = 0
        self.slot = "weapon"

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("⚒ 装备精铸", size=24, color=COLORS['gold'], bold=True, height=36))
        jingjin = gs.inventory["materials"].get("玄铁精金",0)
        self.layout.add_widget(make_label(f"玄铁精金: {jingjin}", size=16, color=COLORS['ink'], height=26))

        # 选择侠客
        hero_box = BoxLayout(size_hint=(1,None), height=50, spacing=8)
        for i, name in enumerate(gs.party):
            b = make_btn(name, height=42, font_size=14,
                         bg=COLORS['gold'] if i==self.selected else COLORS['bg_card'])
            b.bind(on_press=lambda b,i=i: self._select_hero(i))
            hero_box.add_widget(b)
        self.layout.add_widget(hero_box)

        name = gs.party[self.selected]
        hd = gs.hero_data[name]

        # 武器/护甲切换
        slot_box = BoxLayout(size_hint=(1,None), height=45, spacing=8)
        for s, label in [("weapon","武器"),("armor","护甲")]:
            b = make_btn(label, height=38, font_size=14,
                         bg=COLORS['red'] if s==self.slot else COLORS['bg_card'])
            b.bind(on_press=lambda b,s=s: self._select_slot(s))
            slot_box.add_widget(b)
        self.layout.add_widget(slot_box)

        equip = hd["equipment"].get(self.slot)
        refine = hd["refine"]
        cost = 1 + refine * 2
        self.layout.add_widget(make_label(f"当前: {equip or '无'} | 精铸+{refine} | 下次消耗: {cost}精金", size=14, color=COLORS['ink_dim'], height=26))

        if not equip:
            self.layout.add_widget(make_label("⚠ 该位置没有装备，请先到商城购买", size=14, color=COLORS['red'], height=26))
        else:
            btn_box = BoxLayout(size_hint=(1,None), height=55, spacing=10)
            for text, amt in [("+1",1),("+10",10)]:
                can = jingjin >= cost * amt
                b = make_btn(text, height=48, font_size=16,
                             bg=COLORS['orange'] if can else COLORS['bg_card'])
                b.bind(on_press=lambda b,amt=amt: self._refine(amt))
                btn_box.add_widget(b)
            self.layout.add_widget(btn_box)

            max_btn = make_btn(f"精铸至上限 (消耗所有精金)", height=45, font_size=15, bg=COLORS['red'])
            max_btn.bind(on_press=self._refine_max)
            self.layout.add_widget(max_btn)

        back = make_btn("← 返回", height=40, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _select_hero(self, idx):
        self.selected = idx
        self.refresh()

    def _select_slot(self, slot):
        self.slot = slot
        self.refresh()

    def _refine(self, amount):
        name = gs.party[self.selected]
        hd = gs.hero_data[name]
        if not hd["equipment"].get(self.slot): return
        jingjin = gs.inventory["materials"].get("玄铁精金",0)
        for _ in range(amount):
            cost = 1 + hd["refine"] * 2
            if jingjin < cost: break
            jingjin -= cost
            hd["refine"] += 1
        gs.inventory["materials"]["玄铁精金"] = jingjin
        popup("精铸成功", f"{name} 的{self.slot}精铸至 +{hd['refine']}\n属性 +{hd['refine']*10}%")
        self.refresh()

    def _refine_max(self, *a):
        name = gs.party[self.selected]
        hd = gs.hero_data[name]
        if not hd["equipment"].get(self.slot): return
        jingjin = gs.inventory["materials"].get("玄铁精金",0)
        refined = 0
        while True:
            cost = 1 + hd["refine"] * 2
            if jingjin < cost: break
            jingjin -= cost
            hd["refine"] += 1
            refined += 1
        gs.inventory["materials"]["玄铁精金"] = jingjin
        if refined > 0:
            popup("精铸完成", f"共精铸 {refined} 次！\n当前 +{hd['refine']}")
        else:
            popup("精金不足", "没有足够的玄铁精金")
        self.refresh()

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 武学图鉴
# ============================================================
class SkillBookScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("📜 武学图鉴", size=24, color=COLORS['orange'], bold=True, height=36))
        owned = gs.inventory.get("skills_owned", [])
        self.layout.add_widget(make_label(f"已掌握: {len(owned)}/{len(SKILLS_DATA)} 种武学", size=16, color=COLORS['ink'], height=26))

        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        box.bind(minimum_height=box.setter('height'))

        rarity_colors = {"橙":COLORS['orange'],"紫":COLORS['purple'],"蓝":COLORS['blue'],"金":COLORS['gold']}
        for sname, sdata in sorted(SKILLS_DATA.items(), key=lambda x: ["橙","紫","蓝","金"].index(x[1]["rarity"])):
            is_owned = sname in owned
            color = rarity_colors.get(sdata["rarity"], COLORS['ink'])
            if not is_owned: color = COLORS['ink_dim']
            text = f"{'✅' if is_owned else '🔒'} [{sdata['rarity']}] {sname} ({sdata['type']}) 威力:{sdata['power']}"
            box.add_widget(make_label(text, size=14, color=color, halign="left", width=600))
            box.add_widget(make_label(f"    {sdata['desc']} [属性:{sdata['element']}]", size=11, color=COLORS['ink_dim'], halign="left", width=600))
        scroll.add_widget(box)
        self.layout.add_widget(scroll)

        back = make_btn("← 返回", height=40, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 背包
# ============================================================
class InventoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=15, spacing=10)
        self.add_widget(self.layout)

    def refresh(self):
        self.layout.clear_widgets()
        self.layout.add_widget(make_label("💊 背包物品", size=24, color=COLORS['green'], bold=True, height=36))

        # 物品
        self.layout.add_widget(make_label("消耗品：", size=16, color=COLORS['gold'], height=26))
        for item, count in gs.inventory.get("items",{}).items():
            self.layout.add_widget(make_label(f"  {item} ×{count}", size=14, color=COLORS['ink'], height=22))

        # 材料
        self.layout.add_widget(make_label("材料：", size=16, color=COLORS['gold'], height=26))
        for mat, count in gs.inventory.get("materials",{}).items():
            self.layout.add_widget(make_label(f"  {mat} ×{count}", size=14, color=COLORS['cyan'], height=22))

        back = make_btn("← 返回", height=40, bg=COLORS['bg_card'])
        back.bind(on_press=lambda *a: self._go_back())
        self.layout.add_widget(back)

    def _go_back(self):
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

# ============================================================
# 结局
# ============================================================
class EndingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = make_panel(padding=30, spacing=15)
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        # 根据声望/选择决定结局
        # 简化：根据NG+次数和难度
        if gs.ng_plus >= 1:
            ending = "侠之大者"
            text = (
                "你击败了暗影教主，拯救了武林。\n"
                "江湖百姓人人称颂你的名字。\n"
                "你成为了新一代武林盟主，\n"
                "统领正道，匡扶正义。\n\n"
                "—— 侠之大者 结局 ——"
            )
            color = COLORS['gold']
        elif gs.difficulty >= 2:
            ending = "一代魔尊"
            text = (
                "你击败了暗影教主，却发现他的功法...\n"
                "你吞噬了他的内力，实力暴涨！\n"
                "你决定不再拘束于正道，\n"
                "建立属于自己的暗影帝国。\n\n"
                "—— 一代魔尊 结局 ——"
            )
            color = COLORS['red']
        else:
            ending = "逍遥散人"
            text = (
                "你击败了暗影教主，武林恢复平静。\n"
                "你不愿卷入江湖纷争，\n"
                "携侣归隐山林，从此不问世事。\n"
                "江湖只留下你的传说...\n\n"
                "—— 逍遥散人 结局 ——"
            )
            color = COLORS['green']

        self.layout.add_widget(Widget(size_hint=(1,0.15)))
        self.layout.add_widget(make_label(text, size=22, color=color, height=220))
        self.layout.add_widget(Widget(size_hint=(1,0.05)))

        # NG+ 按钮
        ng_btn = make_btn(f"🔄 进入二周目 (NG+{gs.ng_plus+1}) 全队属性+10%", height=55, font_size=18, bg=COLORS['pink'])
        ng_btn.bind(on_press=self._ng_plus)
        self.layout.add_widget(ng_btn)

        back = make_btn("返回标题", height=45, bg=COLORS['bg_card'])
        back.bind(on_press=self._to_menu)
        self.layout.add_widget(back)

    def _ng_plus(self, *a):
        gs.ng_plus += 1
        # 保留所有属性，重置地图和塔
        gs.tower_floor = 0
        gs.current_area = 0
        gs.ending_seen = False
        popup("New Game+", f"进入 NG+{gs.ng_plus}！\n全队属性永久 +{gs.ng_plus*10}%\n敌人也会更强...")
        self.manager.get_screen("world").refresh()
        self.manager.current = "world"

    def _to_menu(self, *a):
        self.manager.current = "main"

# ============================================================
# 弹窗
# ============================================================
def popup(title, text, size=(400,300)):
    box = make_panel(padding=20, spacing=10)
    box.add_widget(make_label(title, size=22, color=COLORS['gold'], bold=True, height=36))
    box.add_widget(make_label(text, size=16, color=COLORS['ink'], height=160))
    close = make_btn("确定", height=45, bg=COLORS['gold'])
    box.add_widget(close)
    p = Popup(title="", content=box, size_hint=(0.8, 0.6), separator_height=0)
    close.bind(on_press=p.dismiss)
    p.open()

# ============================================================
# 主应用
# ============================================================
gs = GameState()

class XiaWuxiaApp(App):
    def build(self):
        self.title = "小武侠传说 · 无尽武道篇"
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="main"))
        sm.add_widget(WorldMapScreen(name="world"))
        sm.add_widget(BattleScreen(name="battle"))
        sm.add_widget(TowerScreen(name="tower"))
        sm.add_widget(ShopScreen(name="shop"))
        sm.add_widget(MeridianScreen(name="meridian"))
        sm.add_widget(InsightScreen(name="insight"))
        sm.add_widget(EquipScreen(name="equip"))
        sm.add_widget(SkillBookScreen(name="skill_book"))
        sm.add_widget(InventoryScreen(name="inventory"))
        sm.add_widget(EndingScreen(name="ending"))
        return sm

    def on_pause(self):
        save_game(gs.to_dict())
        return True

    def on_stop(self):
        save_game(gs.to_dict())

if __name__ == "__main__":
    XiaWuxiaApp().run()
