import csv


def generate_merge_csv(csv_file, items):
    columns = list(items[0].keys())
    with open(csv_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in items:
            writer.writerow(i)
