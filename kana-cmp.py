import csv
import os
import sys
import re
import unicodedata
import mojimoji

def normalize_kana(kana):
    # ひらがな、半角カタカナを全角カタカナに変換
    kana = mojimoji.han_to_zen(kana, ascii=False, digit=False)
    kana = mojimoji.hira_to_kata(kana)

    # 濁点、半濁点を取り除く
    kana = kana.replace("゛", "").replace("゜", "")

    # 特定の文字の変換
    kana = kana.replace("ヰ", "イ").replace("ヱ", "エ").replace("ヲ", "オ")
    
    # 拗音や長音記号の大きなカタカナに変換
    for small, large in [("ァ", "ア"), ("ィ", "イ"), ("ゥ", "ウ"), ("ェ", "エ"), ("ォ", "オ"), ("ッ", "ツ"), ("ャ", "ヤ"), ("ュ", "ユ"), ("ョ", "ヨ"), ("ー", "－")]:
        kana = kana.replace(small, large)

    # スペースを取り除く
    kana = kana.replace(" ", "").replace("　", "")

    return kana

def main(src_file, ref_file):
    with open(src_file, 'r', encoding='utf-8') as src, open(ref_file, 'r', encoding='utf-8') as ref:
        src_reader = csv.reader(src)
        ref_reader = csv.reader(ref)

        src_data = {row[0]: normalize_kana(row[1]) for row in src_reader}
        ref_data = {row[0]: normalize_kana(row[1]) for row in ref_reader}

        all_keys = set(src_data.keys()).union(set(ref_data.keys()))
        results = []

        for key in sorted(all_keys):
            src_kana = src_data.get(key, "該当なし")
            ref_kana = ref_data.get(key, "該当なし")

            if src_kana == ref_kana:
                flag = 0
            elif src_kana == "該当なし" or ref_kana == "該当なし":
                flag = -1
            else:
                flag = 1

            results.append([key, flag, src_kana, ref_kana])

    with open(os.path.join(os.path.dirname(src_file), 'kana_cmp.csv'), 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python kana-cmp.py <src_file.csv> <ref_file.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
