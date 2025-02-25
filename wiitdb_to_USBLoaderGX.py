from lxml import builder as xmlb
from lxml import etree as xmlt
from lxml.etree import SubElement as xmlse
from untangle import parse as up
from googletrans import Translator
from httpcore._exceptions import ConnectTimeout, ConnectError
from ssl import SSLEOFError
import xml.etree.ElementTree as ET

# 游戏类型映射到对应的ID
gameTypeMap = {
    'GameCube': '1',
    'Programs': '2',
    'Third-Party': '3',
    'VC-Arcade': '4',
    'VC-Commodore 64': '5',
    'VC-MSX': '6',
    'VC-N64': '7',
    'VC-NeoGeo': '8',
    'VC-NES': '9',
    'VC-Sega Genesis': '10',
    'VC-SEGA Master System': '11',
    'VC-SNES': '12',
    'VC-Turbo Grafx 1.6': '13',
    'Wii': '14',
    'WiiWare': '15',
    'software': '16',
    '运动': '17',
    '冒险': '18',
    '动作': '19',
    '解谜': '20',
    '恐怖游戏': '21',
    '音乐': '22',
    '跳舞': '23',
    '节奏': '24',
    '跳台游戏': '25',
    '聚会': '26',
    '探险': '27',
    '平衡板': '28',
    '篮球': '29',
    '赛车': '30',
    '足球': '31',
    '街机': '32',
    '网球': '33',
    '射击': '34',
    '第一人称射击': '35',
    '模拟': '36',
    '角色扮演': '37',
    '桌面游戏': '38',
    '钓鱼': '39',
    '动作 RPG': '40',
    '虚拟宠物': '41',
    '拳击': '42',
    '卡丁车 赛车': '43',
    '高尔夫': '44',
    '冰球': '45',
    '滑雪橇': '46',
    '标枪': '47',
    '搏斗': '48',
    '对战': '49',
    '轨道射击': '50',
    '战术 RPG': '51',
    '交互故事': '52',
    '弹球游戏': '53',
    '台球': '54',
    '智力测验': '55',
    '第一人称 射击': '56',
    '教育': '57',
    '打猎': '58',
    '模拟人生': '59',
    '健康': '60',
    '减肥': '61',
    '健身教练': '62',
    '运动练习': '63',
    '越野车赛': '64',
    '施工模拟': '65',
    '策略': '66',
    '智力解谜': '67',
    '卡拉OK': '68',
    '隐藏 游戏': '69',
    '板球': '70',
    '滑雪板': '71',
    '保龄球': '72',
    '第三人称射击': '73',
    '基础 战略游戏': '74',
    '烹饪': '75',
    '卡牌': '76',
    '滚球': '77',
    '商业 模拟': '78',
    '排球运动': '79',
    '即时战略': '80',
    '飞行模拟': '81',
    '轨道 射击': '82',
    '枪战暴力': '83',
    '策略 rpg': '84',
    '滑板': '85'
}

# 创建XML文档的基础结构
xmldocBase = xmlb.ElementMaker()
USBLoaderGX = xmldocBase.USBLoaderGX
Revision = xmldocBase.Revision
Categories = xmldocBase.Categories
GameCategories = xmldocBase.GameCategories

# 初始化XML文档布局
xmldocLayout = USBLoaderGX(
    Revision('1281'),
    Categories(),
    GameCategories()
)

# 添加默认类别
defaultCategory = xmlse(xmldocLayout[1], 'Category')
defaultCategory.set('ID', '00')
defaultCategory.set('Name', 'All')

# 初始化翻译器
translator = Translator()

# 解析wiitdb.xml文件
wiitdb_xml = up('wiitdb.xml')

# 提取并添加新的游戏类型和ID到gameTypeMap
genre_id = 86  # 从86开始分配新的ID
for game in wiitdb_xml.datafile.game:
    if hasattr(game, 'genre'):
        genres = game.genre.cdata.split(',')
        for genre in genres:
            genre = genre.strip()
            if genre and genre not in gameTypeMap:
                gameTypeMap[genre] = str(genre_id)
                genre_id += 1

# 根据游戏类型映射自动生成类别
for gameType, gameID in gameTypeMap.items():
    autogenCategory = xmlse(xmldocLayout[1], 'Category')
    autogenCategory.set('ID', gameID)
    autogenCategory.set('Name', gameType)

# 解析wiitdb.xml文件
for game in wiitdb_xml.datafile.game:
    gameType = ''
    if game.type.cdata == '':
        gameType = 'Wii'
    elif game.type.cdata == 'Channel':
        gameType = 'Programs'
    elif game.type.cdata == 'Homebrew':
        gameType = 'Third-Party'
    elif game.type.cdata == 'VC-NEOGEO':
        gameType = 'VC-NeoGeo'
    elif game.type.cdata == 'CUSTOM':
        gameType = 'Third-Party'
    elif game.type.cdata == 'VC-C64':
        gameType = 'VC-Commodore 64'
    elif game.type.cdata == 'VC-MD':
        gameType = 'VC-Sega Genesis'
    elif game.type.cdata == 'VC-PCE':
        gameType = 'VC-Turbo Grafx 1.6'
    elif game.type.cdata == 'VC-SMS':
        gameType = 'VC-SEGA Master System'
    else:
        gameType = game.type.cdata

    # 为每个游戏生成XML元素
    autogenGame = xmlse(xmldocLayout[2], 'Game')
    autogenGame.set('ID', game.id.cdata)
    
    # 检查并设置游戏标题
    if hasattr(game, 'locale'):
        zhcn_title = None
        en_title = None
        for locale in game.locale:
            if locale['lang'] == 'ZHCN':
                zhcn_title = locale.title.cdata
                break
            elif locale['lang'] == 'EN':
                en_title = locale.title.cdata
        if zhcn_title:
            autogenGame.set('Title', zhcn_title)
        elif en_title:
            autogenGame.set('Title', en_title)
        else:
            try:
                autogenGame.set('Title', game.locale.title.cdata)
            except:
                autogenGame.set('Title', game.locale[0].title.cdata)
    else:
        autogenGame.set('Title', 'Unknown Title')

    # 添加默认类别
    autogenGameDefaultCategory = xmlse(autogenGame, 'Category')
    autogenGameDefaultCategory.set('ID', '00')
    autogenGameDefaultCategory.set('Name', 'All')

    # 添加自动生成的type类别
    if gameType in gameTypeMap:
        autogenGameTypeCategory = xmlse(autogenGame, 'Category')
        autogenGameTypeCategory.set('ID', gameTypeMap[gameType])
        autogenGameTypeCategory.set('Name', gameType)

    # 添加自动生成的genre类别
    if hasattr(game, 'genre'):
        genres = game.genre.cdata.split(',')
        for genre in genres:
            genre = genre.strip()
            if genre in gameTypeMap:
                autogenGameGenreCategory = xmlse(autogenGame, 'Category')
                autogenGameGenreCategory.set('ID', gameTypeMap[genre])
                autogenGameGenreCategory.set('Name', genre)

# 生成XML数据并写入文件
xmlData = b''.join([b'<?xml version="1.0" encoding="UTF-8"?>\n', xmlt.tostring(xmldocLayout, encoding="UTF-8", xml_declaration=False, pretty_print=True)])
with open('GXGameCategories.xml', 'wb') as f:
    f.write(xmlData)

# 将新的gameTypeMap写入结果文件
with open('gameTypeMap.txt', 'w', encoding='utf-8') as f:
    for gameType, gameID in gameTypeMap.items():
        f.write(f'{gameType}: {gameID}\n')

# 读取生成的GXGameCategories.xml文件并检索英文标题
tree = xmlt.parse('GXGameCategories.xml')
root = tree.getroot()
# 读取生成的GXGameCategories.xml文件并检索英文标题,并且存入英文标题和ID的文件到GXGameCategories-new.txt
with open('GXGameCategories-new.txt', 'w', encoding='utf-8') as f:
    for game in root.findall('.//Game'):
        title = game.get('Title')
        if title and title.isascii():  # 检查标题是否为英文
            game_id = game.get('ID')
            f.write(f'ID={game_id} Title={title}\n')

# 解析 wiitdb.xml 文件并处理解析错误
try:
    wiitdb_xml = up('wiitdb.xml')
except ET.ParseError as e:
    print(f"Error parsing wiitdb.xml: {e}")
    exit(1)

# 检索 wiitdb.xml 中 game中input中control 的 type='balanceboard' 的游戏（排除game.type=Homebrew的游戏  ），把符合 game 的id 和 name(输出lang="ZHCN",如果没有则输出lang="EN") 输出到 balanceboard.txt
with open('balanceboard.txt', 'w', encoding='utf-8') as f:
    for game in wiitdb_xml.datafile.game:
        # 排除game.type=Homebrew和game.type=Channel的游戏
        if game.type.cdata != 'Homebrew' and game.type.cdata != 'Channel': 
            for input in game.input:
                if hasattr(input, 'control'):
                    for control in input.control:
                        if control['type'] == 'balanceboard':
                            id = game.id.cdata
                            name = None
                            # 检索中文标题功能注释掉
                            # for locale in game.locale:
                            #     if locale['lang'] == 'ZHCN':
                            #         name = locale.title.cdata
                            #         break
                            if hasattr(game, 'locale'):
                                for locale in game.locale:
                                    if locale['lang'] == 'EN':
                                        name = locale.title.cdata
                                        break
                            if name:
                                f.write(f'ID={id} Name={name}\n')
                            else:
                                if game.locale and hasattr(game.locale[0], 'title'):
                                    f.write(f'ID={id} Name={game.locale[0].title.cdata}\n')
                                else:
                                    f.write(f'ID={id} Name=Unknown\n')
# 检索 wiitdb.xml 中 game中input中control 的 type='dancepad' 的游戏（排除game.type=Homebrew的游戏  ），把符合 game 的id 和 name(输出lang="ZHCN",如果没有则输出lang="EN") 输出到 dancepad.txt
with open('dancepad.txt', 'w', encoding='utf-8') as f:
    for game in wiitdb_xml.datafile.game:
        # 排除game.type=Homebrew和game.type=Channel的游戏
        if game.type.cdata != 'Homebrew' and game.type.cdata != 'Channel': 
            for input in game.input:
                if hasattr(input, 'control'):
                    for control in input.control:
                        if control['type'] == 'dancepad':
                            id = game.id.cdata
                            name = None
                            # 检索中文标题功能注释掉
                            # for locale in game.locale:
                            #     if locale['lang'] == 'ZHCN':
                            #         name = locale.title.cdata
                            #         break
                            if hasattr(game, 'locale'):
                                for locale in game.locale:
                                    if locale['lang'] == 'EN':
                                        name = locale.title.cdata
                                        break
                            if name:
                                f.write(f'ID={id} Name={name}\n')
                            else:
                                if game.locale and hasattr(game.locale[0], 'title'):
                                    f.write(f'ID={id} Name={game.locale[0].title.cdata}\n')
                                else:
                                    f.write(f'ID={id} Name=Unknown\n')                                   