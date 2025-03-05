import re
import xml.etree.ElementTree as ET

def is_chinese(text):
    """改进的中文检测函数，包含全角标点"""
    return bool(re.search(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))

# 读取原始文件并保留元数据
header = ""
original_entries = []
with open('wiitdb.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('TITLES'):
            header = line.strip()
            continue
        if '=' in line:
            parts = line.split('=', 1)
            original_entries.append((parts[0].strip(), parts[1].strip()))

# 构建需要查询的ID列表
query_ids = {id: name for id, name in original_entries if not is_chinese(name)}

# 解析XML数据库
tree = ET.parse('wiitdb.xml')
name_mapping = {}

for game in tree.findall('game'):
    # 提取游戏ID
    game_id_elem = game.find('id')
    if game_id_elem is None or game_id_elem.text is None:
        continue
    game_id = game_id_elem.text.strip()
    
    # 仅处理需要替换的ID
    if game_id not in query_ids:
        continue
    
    # 查找中文标题
    zhcn_title = None
    for locale in game.findall('locale'):
        if locale.get('lang') == 'ZHCN':
            title_elem = locale.find('title')
            if title_elem is not None and title_elem.text:
                zhcn_title = title_elem.text.strip()
                break
    
    # 记录找到的中文名称
    if zhcn_title:
        name_mapping[game_id] = zhcn_title

# 生成新内容
new_content = []
for id, name in original_entries:
    if not is_chinese(name) and id in name_mapping:
        new_content.append(f"{id} = {name_mapping[id]}")
    else:
        new_content.append(f"{id} = {name}")

# 写入新文件
with open('gametitle.txt', 'w', encoding='utf-8') as f:
    f.write(header + "\n")
    f.write("\n".join(new_content))

print("文件生成成功，共处理 {} 个条目，其中 {} 个被替换为中文名称".format(
    len(original_entries), len(name_mapping)))