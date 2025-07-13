from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import csv
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- CONFIG ---------- #
SAVE_DIR = "brain_scan_images"
CSV_FILE = "brain_scan_dataset.csv"
NUM_PAGES = 12
MAX_WORKERS = 6  # Number of parallel threads
# ---------------------------- #

# Setup
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(20)

# Base URL
BASE_URL = "https://openi.nlm.nih.gov/gridquery?coll=mc&it=xg&q=brain%20scan&m={m}&n={n}"

# Scan types to check for
SCAN_TYPES = ["CT", "MRI", "X-ray", "Ultrasound", "PET", "Microscopy", "Graphics",
              "Photographs", "Video", "Tomography", "Magnetic resonance", "FDG-PET",
              "MR", "computed-tomography"]

# Make directory
os.makedirs(SAVE_DIR, exist_ok=True)

# Load previously downloaded image names
downloaded_images = set()
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            downloaded_images.add(row[0])

# CSV for writing
write_header = not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0

csv_file = open(CSV_FILE, "a", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)

# ✅ Write header if new or empty file
if write_header:
    csv_writer.writerow(["Image Name", "Scan Type(s)", "Description", "Bottom Line", "Image URL"])
    csv_file.flush()

# ------------- DOWNLOAD FUNCTION ------------- #
def download_image(info):
    idx, page, elem = info
    try:
        img_tag = elem.find_element(By.TAG_NAME, "img")
        src_attr = img_tag.get_attribute("src")
        img_url = src_attr if src_attr.startswith("http") else "https://openi.nlm.nih.gov" + src_attr
        img_name = f"image{(page * 100) + idx + 1:04d}.png"
        img_path = os.path.join(SAVE_DIR, img_name)

        if img_name in downloaded_images:
            print(f"⏭️ Skipped (already downloaded): {img_name}")
            return

        try:
            desc_elem = elem.find_element(By.CLASS_NAME, "imageToolTipCaption")
            scan_description = desc_elem.get_attribute("innerText").strip()
        except NoSuchElementException:
            scan_description = "No description"

        try:
            bottom_elem = elem.find_element(By.CLASS_NAME, "imageToolTipBottomLine")
            bottom_line = bottom_elem.get_attribute("innerText").strip()
        except NoSuchElementException:
            bottom_line = "No bottom line"

        scan_types_found = [scan for scan in SCAN_TYPES if scan.lower() in scan_description.lower()]
        scan_type_str = ", ".join(scan_types_found) if scan_types_found else "Unknown"

        # # 🛑 Skip if no useful metadata
        # if scan_description == "No description" or bottom_line == "No bottom line" or scan_type_str == "Unknown":
        #     print(f"🚫 Skipped poor metadata: {img_name}")
        #     return

        # Download image
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        with open(img_path, "wb") as img_file:
            img_file.write(response.content)

        # Save metadata
        csv_writer.writerow([img_name, scan_type_str, scan_description, bottom_line, img_url])
        csv_file.flush()  # Make sure it's written immediately
        print(f"✅ Downloaded: {img_name}")
    except Exception as e:
        print(f"⚠️ Failed: image on page {page + 1} - {e}")
# ---------------------------------------------- #

# Process each page
for page in range(NUM_PAGES):
    m = page * 100 + 1
    n = (page + 1) * 100
    url = BASE_URL.format(m=m, n=n)
    print(f"\n🔍 Scraping Page {page + 1}: {url}")

    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jg-entry"))
        )
    except:
        print("⚠️ Timeout: No images found on page.")
        continue

    try:
        image_elements = driver.find_elements(By.CLASS_NAME, "jg-entry")
        if not image_elements:
            print(f"⚠️ No entries found on Page {page + 1}")
            continue
    except Exception as e:
        print(f"⚠️ Could not find images: {e}")
        continue

    # Create task list for this page
    tasks = [(idx, page, elem) for idx, elem in enumerate(image_elements)]

    # Run download tasks in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_image, tasks)

# Cleanup
csv_file.close()
driver.quit()
print(f"\n🎉 Scraping complete! Metadata saved in {CSV_FILE}")