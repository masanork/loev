import csv
import sys
import os

def split_csv(input_file):
    with open(input_file, 'r', newline='') as fin:
        reader = csv.reader(fin)
        
        first_row = next(reader)  # 最初の行を取得
        num_attrs = len(first_row) - 1

        # 2番目以降のカラムについて、各属性用のCSVファイルを作成
        for idx in range(1, num_attrs + 1):
            output_file = f"{os.path.splitext(input_file)[0]}_{idx}.csv"
            with open(output_file, 'w', newline='') as fout:
                writer = csv.writer(fout)
                writer.writerow([first_row[0], first_row[idx]])

                # 元のCSVから行を読み取り、新しいCSVに書き込む
                for row in reader:
                    writer.writerow([row[0], row[idx]])
                
                # リーダーの位置をリセットして次の属性用のファイルを作成するために準備
                fin.seek(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python csv-split.py <input-file>")
        sys.exit(1)

    split_csv(sys.argv[1])
