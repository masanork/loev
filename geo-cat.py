import csv
import os
import sys

def main(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        data1 = {row[0]: row[1] for row in reader1}
        data2 = {row[0]: row[1] for row in reader2}

        all_keys = set(data1.keys()).union(set(data2.keys()))

        geo_cat_data = []
        geo_address_data = []
        
        for key in sorted(all_keys):
            address1 = data1.get(key, "該当なし")
            address2 = data2.get(key, "該当なし")
            
            geo_cat_data.append([key, address1, address2])
            geo_address_data.extend([address1, address2])

    with open(os.path.join(os.path.dirname(file1), 'geo_cat.csv'), 'w', encoding='utf-8', newline='') as out1, \
         open(os.path.join(os.path.dirname(file1), 'geo_address.csv'), 'w', encoding='utf-8', newline='') as out2:
        
        writer1 = csv.writer(out1)
        writer1.writerows(geo_cat_data)

        for addr in geo_address_data:
            out2.write(addr + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python geo-cat.py <address_file1.csv> <address_file2.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
