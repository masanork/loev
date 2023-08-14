import csv
import os
import sys
from dateutil import parser
from datetime import datetime

def days_difference(date1, date2):
    if date1 == "該当なし" or date2 == "該当なし":
        return -1
    d1 = parser.parse(date1)
    d2 = parser.parse(date2)
    return abs((d1 - d2).days)

def main(src_file, ref_file):
    with open(src_file, 'r', encoding='utf-8') as src, open(ref_file, 'r', encoding='utf-8') as ref:
        src_reader = csv.reader(src)
        ref_reader = csv.reader(ref)

        src_data = {row[0]: row[1] for row in src_reader}
        ref_data = {row[0]: row[1] for row in ref_reader}

        all_keys = set(src_data.keys()).union(set(ref_data.keys()))

        output_data = []
        
        for key in sorted(all_keys):
            src_date = src_data.get(key, "該当なし")
            ref_date = ref_data.get(key, "該当なし")
            
            difference = days_difference(src_date, ref_date)
            output_data.append([key, difference, src_date, ref_date])

    with open(os.path.join(os.path.dirname(src_file), 'date_cmp.csv'), 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(output_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python date-cmp.py <src_file.csv> <ref_file.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
