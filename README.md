# 🧠 NeuroScrape

**NeuroScrape** is a Python-based tool that scrapes brain scan metadata from the [Open-i biomedical image search engine](https://openi.nlm.nih.gov/), cleans and processes the data using NLP and pattern recognition techniques, and prepares a high-quality corpus of medical imaging data for downstream machine learning applications.

---

## 🚀 Features

- 🔎 **Automated scraping** of 1000+ brain scan image entries using Selenium and BeautifulSoup.
- 🧹 **Data cleaning pipeline** with regex filters and rule-based filtering to remove collage-type or diagrammatic images based on metadata patterns.
- 📊 **Metadata analysis** including scan type frequency, description length, and bottom line extraction.
- 📁 **Structured CSV output** with labeled columns ready for model training or annotation.

---

## 🛠️ Tech Stack

- **Python** for backend scripting
- **Selenium + BeautifulSoup** for web scraping
- **Pandas + Regex** for data processing and filtering
- **Jupyter Notebook** for data cleaning and exploration

---

## 📁 Project Structure

```plaintext
NeuroScrape/
├── project.py             # Scrapes image data and metadata into a CSV
├── preprocess.py          # Cleans and analyzes the scraped data
├── data_cleaning.ipynb    # Jupyter notebook for deeper inspection and manual filtering
├── scans/                 # Downloaded images
├── output.csv             # Final cleaned metadata
├── .gitignore             # File exclusions
└── README.md              # Project overview and usage
```

---

## 📊 Example Output Stats

- ✅ Total scraped entries: 1200
- 🧹 Post-cleaning corpus size: ~843
- 🖼️ Scan Types: CT, MR, MRI, Tomography
- ⚠️ Collage images filtered using NLP patterns: (a), (b), etc.

---

## 📌 How to Use

`1. Clone the repo:`
```bash
git clone https://github.com/your-username/NeuroScrape.git
cd NeuroScrape
```

`2. 
