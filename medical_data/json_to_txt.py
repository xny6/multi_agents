#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把指定 JSON 文件中的 "entity" 列表逐条写入同目录下的 entity.txt
用法：python extract_entity.py  data.json
"""

import json
import sys
from pathlib import Path

def detect_encoding(file_path: Path):
    """优先尝试 UTF-8，失败再用 GBK"""
    for enc in ('utf-8', 'gbk'):
        try:
            file_path.read_text(encoding=enc)
            return enc
        except UnicodeDecodeError:
            continue
    raise RuntimeError("无法识别文件编码，请手动指定")

def extract_entity_to_txt(json_file: Path, txt_file: Path = None):
    """核心逻辑：读取 -> 提取 -> 写入"""
    if txt_file is None:
        txt_file = json_file.with_name('entity.txt')

    enc = detect_encoding(json_file)
    data = json.loads(json_file.read_text(encoding=enc))

    if 'entity' not in data or not isinstance(data['entity'], list):
        raise ValueError('JSON 中缺少 "entity" 字段或其值不是列表')

    # 逐行写入，保持原 JSON 字符串
    with txt_file.open('w', encoding='utf-8') as f:
        for item in data['entity']:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f'已提取 {len(data["entity"])} 条 entity 到 {txt_file.resolve()}')

def main():
    if len(sys.argv) < 2:
        # 如果没带参数，则在当前目录找第一个 .json 文件
        candidates = list(Path.cwd().glob('*.json'))
        if not candidates:
            print('当前目录下找不到 .json 文件，请手动指定路径')
            sys.exit(1)
        json_path = candidates[0]
        print(f'未指定文件，自动选择: {json_path}')
    else:
        json_path = Path(sys.argv[1])

    if not json_path.exists():
        print(f'文件不存在: {json_path}')
        sys.exit(1)

    try:
        extract_entity_to_txt(json_path)
    except Exception as e:
        print('出错:', e)
        sys.exit(1)

if __name__ == '__main__':
    main()