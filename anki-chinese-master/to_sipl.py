from hanziconv import HanziConv

str = '''COMMON_WORDS = [
    "一",
    "二",
    "三",
    "四",
    "五",
    "六",
    "七",
    "八",
    "九",
    "十",
    "一些",
    "一定",
    "一樣",
    "上",
    "下",
    "不",
    "不是",
    "不會",
    "不能",
    "中",
    "也",
    "事",
    "人",
    "什麼",
    "他",
    "他們",
    "你",
    "你們",
    "來",
    "個",
    "做",
    "先生",
    "兩",
    "再",
    "分",
    "到",
    "十分",
    "去",
    "又",
    "口",
    "叫",
    "可",
    "可以",
    "可是",
    "告訴",
    "呢",
    "和",
    "啊",
    "嗎",
    "四",
    "因為",
    "在",
    "多",
    "多麼",
    "大",
    "天",
    "她",
    "好",
    "它",
    "對",
    "小",
    "就",
    "就是",
    "已",
    "已經",
    "幾",
    "張",
    "很",
    "後",
    "得",
    "從",
    "應",
    "我",
    "我們",
    "把",
    "是",
    "時",
    "時間",
    "最",
    "會",
    "有",
    "朋友",
    "東西",
    "機會",
    "次",
    "比",
    "沒有",
    "為",
    "現在",
    "的",
    "看",
    "看到",
    "真",
    "知道",
    "第一",
    "給",
    "而",
    "能夠",
    "自己",
    "被",
    "裏",
    "要",
    "見",
    "話",
    "說",
    "讓",
    "起來",
    "跟",
    "這",
    "這樣",
    "過",
    "還",
    "那",
    "那些",
    "那麼",
    "都",
    "馬上",
    "點",
    "能",
    "還是",
    "打",
    "氣",
    "前",
    "車子",
    "二早",
    "明白",
    "這話",
    "往",
    "每個",
    "或",
    "如",
    "杯",
    "作",
    "不得",
    "大小",
    "找到",
    "毛",
    "一下",
    "哪",
    "日",
    "名",
    "一些",
    "成",
    "個人",
    "以",
    "也是",
    "有人",
]'''

with open("anki-chinese-master/aa.txt", 'w') as f:
    f.write(HanziConv.toSimplified(str))