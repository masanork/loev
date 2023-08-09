# loev: List of Entity Verifier

loevは2つの同じ項目を持ったリストの比較を行うツールです。それぞれのカラムを別々に正規化して中間生成ファイルを記録に残し、最終的にはそれらを統合して検証結果を出力します。カラムはプログラムの呼び出し方で柔軟に追加削除できるようになっています。中間生成ファイルを記録に全て残すことで、処理の流れを容易に追うことができ、仮に不具合があった場合の障害の切り分けの手がかりを提供します。

## ファイル構成

### プログラム

- csv-split.py: CSVファイルを番号をキーとして属性毎に分割
- name-cmp.py: 名前を正規化して比較、違う行の先頭カラムにフラグを立てる
- geo-cat.py: 番号をキーとして2つの住所ファイルを統合
- geo-cmp.py: 住所を正規化して比較、距離を計算して先頭カラムに書き込む
- date-cmp.py: 日付を比較、日数差を先頭カラムに追記
- kana-cmp.py: カナを正規化して比較、違う行の先頭カラムにフラグを立てる
- cmp-cat.py: 各比較結果ファイルを結合してチェックリストを作成

### データ

- filler.csv: 代替文字の定義
- gaiji.csv: 独自外字の定義
- itaiji.csv: 異体字の定義
- juki2mj.csv: 住基統一文字コードの変換表

## 使い方

ツールを使って比較確認したいCSVファイルとして src.csv と ref.csv を準備します。どのカラムをどの比較モジュールに渡すかは、実際のCSVファイルのカラム構造を踏まえて、必要に応じて修正してください。最終的に内容が異なる行がdiff.csvとして出力されるので、Excelなどで開いて確認してください。

``` bash
$ python csv-split.py src.csv
# output: src_1.csv, src_2.csv src_3.csv src_4.csv ...
$ python csv-split.py ref.csv
# output: ref_1.csv, ref_2.csv ref_3.csv src_4.csv ...
$ python name-cmp.py src_1.csv ref_1.csv
# output: name_cmp.csv
$ python geo-cat.py src_2.csv ref_2.csv
# output: geo_cat.csv, address.csv
$ abr-geocoder normalize --format=json --fuzzy address.csv > address.json
$ python geo-cmp.py geo_cat.csv address.json
# output: geo_cmp.csv
$ python date-cmp.py src_3.csv ref_3.csv
# output: date_cmp.csv
$ python kana-cmp.py src_4.csv ref_4.csv
$ python cmp-cat.py name_cmp.csv address_cmp.csv date_cmp.csv kana_cmp.csv
# output: all.csv, diff.csv
```
