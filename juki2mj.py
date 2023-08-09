import csv
import argparse

CONVERSION_TABLE_PATH = "data/juki2mj.csv"

def load_conversion_table(csv_path):
    conversion_table = {}
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            juki_char = row[0]
            mj_char = row[1]
            conversion_table[juki_char] = mj_char
    return conversion_table

def convert_juki_to_mj(text, conversion_table):
    converted_text = ""
    for char in text:
        if char in conversion_table:
            converted_text += conversion_table[char]
        else:
            converted_text += char
    return converted_text

def main():
    parser = argparse.ArgumentParser(description='Convert 住基文字コード to 文字情報基盤文字 using a conversion table.')
    parser.add_argument('input_file', help='Path to the input text file containing 住基文字コード.')
    parser.add_argument('-o', '--output', help='Output file path. If not provided, results will be printed to the console.')

    args = parser.parse_args()

    conversion_table = load_conversion_table(CONVERSION_TABLE_PATH)

    with open(args.input_file, 'r', encoding='utf-8') as file:
        juki_text = file.read()

    mj_text = convert_juki_to_mj(juki_text, conversion_table)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as out_file:
            out_file.write(mj_text)
    else:
        print(f"文字情報基盤文字: {mj_text}")

if __name__ == "__main__":
    main()
