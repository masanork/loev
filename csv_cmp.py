import csv_split
import name_cmp
import geo_cat
import geo_cmp
import date_cmp
import kana_cmp
import cmp_cat
import subprocess
import sys

def main(src_file, ref_file):
    print(f"実行中: csv-split.pyで{src_file}を分割")
    csv_split.main([src_file])
    
    print(f"実行中: csv-split.pyで{ref_file}を分割")
    csv_split.main([ref_file])

    print("実行中: name-cmp.pyで名前を比較")
    name_cmp.main([f"{src_file}_1.csv", f"{ref_file}_1.csv"])

    print("実行中: geo-cat.pyで住所を結合")
    geo_cat.main([f"{src_file}_2.csv", f"{ref_file}_2.csv"])

    # abr-geocoder コマンドの部分は subprocess を使用して呼び出します。
    print("実行中: abr-geocoderで住所を正規化")
    subprocess.Popen("abr-geocoder normalize --format=json --fuzzy address.csv > address.json", shell=True).wait()

    print("実行中: geo-cmp.pyで住所を比較")
    geo_cmp.main(["geo_cat.csv", "address.json"])

    print("実行中: date-cmp.pyで日付を比較")
    date_cmp.main([f"{src_file}_3.csv", f"{ref_file}_3.csv"])

    print("実行中: kana-cmp.pyで振り仮名を比較")
    kana_cmp.main([f"{src_file}_4.csv", f"{ref_file}_4.csv"])

    print("実行中: cmp-cat.pyで比較結果を結合")
    cmp_cat.main(["name_cmp.csv", "address_cmp.csv", "date_cmp.csv", "kana_cmp.csv"])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python <script_name> <src_file_path> <ref_file_path>")
        sys.exit(1)
    
    src_path = sys.argv[1]
    ref_path = sys.argv[2]
    main(src_path, ref_path)
