import csv
import sys

def read_csv_files(filenames):
    csv_data = []
    for filename in filenames:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            csv_data.append(list(reader))
    return csv_data

def write_output_files(all_rows, diff_rows):
    with open('all.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in all_rows:
            writer.writerow(row)

    with open('diff.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in diff_rows:
            writer.writerow(row)

def main(filenames):
    csv_data = read_csv_files(filenames)
    
    all_rows = []
    diff_rows = []
    
    # Assuming all files have the same number of rows
    for i in range(len(csv_data[0])):
        all_row = []
        diff_row = []
        
        has_diff = False
        for data in csv_data:
            all_row.append(data[i][0])  # Add difference indicator
            all_row.extend(data[i][1:])  # Add other columns
            
            if int(data[i][0]) != 0:
                has_diff = True

        diff_row = all_row[:]
        if has_diff:
            diff_rows.append(diff_row)
        
        all_rows.append(all_row)

    write_output_files(all_rows, diff_rows)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cmp-concat.py <csv1> <csv2> ...")
    else:
        main(sys.argv[1:])
