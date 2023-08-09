import csv
import os
import sys

def load_itaiji_mapping(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return {row[1]: row[0] for row in reader}

def load_filler(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

def normalize_name(name, itaiji):
    name = name.upper().replace(" ", "").replace("　", "")
    for irregular, standard in itaiji.items():
        name = name.replace(irregular, standard)
    return name

def diff_evaluation(src_name, ref_name, fillers):
    if src_name == "該当なし" or ref_name == "該当なし":
        return -1
    if src_name == ref_name:
        return 0
    wildcards_matched = sum([1 for filler in fillers if filler in src_name and filler in ref_name])
    if wildcards_matched > 0:
        return wildcards_matched
    return 9

def main(src_file, ref_file):
    itaiji = load_itaiji_mapping('data/itaiji.csv')
    fillers = load_filler('data/filler.csv')
    
    with open(src_file, 'r', encoding='utf-8') as src, open(ref_file, 'r', encoding='utf-8') as ref:
        src_reader = csv.reader(src)
        ref_reader = csv.reader(ref)

        src_data = {row[0]: normalize_name(row[1], itaiji) for row in src_reader}
        ref_data = {row[0]: normalize_name(row[1], itaiji) for row in ref_reader}

        all_keys = set(src_data.keys()).union(set(ref_data.keys()))

        output_data = []
        
        for key in sorted(all_keys):
            src_name = src_data.get(key, "該当なし")
            ref_name = ref_data.get(key, "該当なし")
            
            evaluation = diff_evaluation(src_name, ref_name, fillers)
            output_data.append([key, evaluation, src_name, ref_name])

    with open(os.path.join(os.path.dirname(src_file), 'name_cmp.csv'), 'w', encoding='utf-8', newline='') as out:
        writer = csv.writer(out)
        writer.writerows(output_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python name-cmp.py <src_file.csv> <ref_file.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
