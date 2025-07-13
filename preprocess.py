import csv
import os
from collections import Counter
import matplotlib.pyplot as plt

csv_filename = "brain_scan_dataset.csv"

if not os.path.exists(csv_filename):
    print(f"❌ CSV file not found: {csv_filename}")
    exit()

# Initialize counters
total_images = 0
scan_type_counter = Counter()
description_lengths = []
bottom_lines = set()

with open(csv_filename, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_images += 1

        scan_types = [s.strip() for s in row["Scan Type(s)"].split(",") if s.strip()]
        scan_type_counter.update(scan_types)

        desc_len = len(row["Description"].strip())
        if desc_len > 0:
            description_lengths.append(desc_len)

        bottom_line = row["Bottom Line"].strip()
        if bottom_line and bottom_line.lower() != "no bottom line":
            bottom_lines.add(bottom_line)

# Output basic stats
print(f"\n📊 Total Images: {total_images}")
print(f"✍️ Average Description Length: {sum(description_lengths) / len(description_lengths):.2f} characters" if description_lengths else "✍️ Average Description Length: 0.00 characters")
print(f"🔍 Top 5 Scan Types: {scan_type_counter.most_common(5)}")
print(f"📝 Unique Bottom Lines: {len(bottom_lines)}")

# Only plot if data exists
if scan_type_counter:
    types, counts = zip(*scan_type_counter.most_common(10))

    plt.figure(figsize=(10, 6))
    plt.bar(types, counts, color='purple')
    plt.title("Top 10 Scan Types")
    plt.xlabel("Scan Type")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ No scan type data to plot.")