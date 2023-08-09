import csv
import os
import sys
import re

def load_mapping(file_path):
    """CSVファイルから変換マッピングをロードする"""
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return {row[0]: row[1] for row in reader}

def compare_names_with_fillers(name1, name2, fillers):
    mismatch_count = 0
    for a, b in zip(name1, name2):
        if a in fillers or b in fillers:
            continue
        if a != b:
            mismatch_count += 1
    return mismatch_count

def clean_and_convert(name, itaiji_mapping, gaiji_mapping):
    """氏名のクリーニングと変換を行う"""
    # []内の文字を削除
    name = re.sub(r'\[.*?\]', '', name)
    # 全角半角の空白を削除
    name = re.sub(r'\s', '', name)
    # アルファベットを半角大文字に
    name = name.upper()
    # 異体字と外字の変換
    for k, v in itaiji_mapping.items():
        name = name.replace(k, v)
    for k, v in gaiji_mapping.items():
        name = name.replace(k, v)
    return name

def main(src_file, ref_file, itaiji_file='data/itaiji.csv', gaiji_file='data/gaiji.csv', filler_file='data/filler.csv'):
    itaiji_mapping = load_mapping(itaiji_file)
    gaiji_mapping = load_mapping(gaiji_file)
    fillers = set(load_mapping(filler_file).keys())

    with open(src_file, 'r', encoding='utf-8') as src, open(ref_file, 'r', encoding='utf-8') as ref:
        src_reader = csv.reader(src)
        ref_reader = csv.reader(ref)

        src_data = {row[0]: clean_and_convert(row[1], itaiji_mapping, gaiji_mapping) for row in src_reader}
        ref_data = {row[0]: clean_and_convert(row[1], itaiji_mapping, gaiji_mapping) for row in ref_reader}

        all_keys = set(src_data.keys()).union(set(ref_data.keys()))
        results = []

        for key in sorted(all_keys):
            src_name = src_data.get(key, "該当なし")
            ref_name = ref_data.get(key, "該当なし")
            
            if src_name == ref_name:
                difference = 0
            elif src_name == "該当なし" or ref_name == "該当なし":
                difference = -1
            else:
                difference = compare_names_with_fillers(src_name, ref_name, fillers)

            results.append([key, difference, src_name, ref_name])

    with open(os.path.join(os.path.dirname(src_file), 'name_cmp.csv'), 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python name-cmp.py <src_file.csv> <ref_file.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
