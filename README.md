# LinkedIn Company Finder (Google API Integration) 🚀

This Python-based tool automates the process of finding official LinkedIn Company Page URLs using the **Google Custom Search JSON API**. It was specifically designed to handle bulk data enrichment for business intelligence and CRM optimization tasks.

Originally developed to streamline sales operations and data cleaning workflows in a corporate environment.

## 🌟 Key Features
* **Automated Enrichment**: Seamlessly converts a list of company names in Excel into validated LinkedIn URLs.
* **Smart API Key Rotation**: Implements a failover system that automatically switches to the next available Google API key when daily quotas (100 requests/key) are reached.
* **Cross-Platform Compatibility**: Uses path-agnostic logic to run seamlessly on macOS, Windows, and Linux.
* **Robust Data Handling**: Powered by `pandas`, it prevents duplicate processing by skipping already enriched rows and saving progress incrementally.

## ⚠️ Quota Management & Scalability
The Google Custom Search API (Free Tier) has a strict limit of **100 queries per day per API key**. This script is engineered to overcome this limitation for professional use:

* **Multi-Key Support**: Dynamically cycles through a pool of keys stored in `api_keys.xlsx`.
* **Automatic Handover**: Detects `429 Too Many Requests` errors and immediately switches to the next credential.
* **Persistence**: If all keys are exhausted, the script saves current progress and terminates cleanly, allowing for a seamless resume.

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Libraries:** `pandas`, `requests`, `openpyxl`
* **Environment:** Optimized for **VS Code** with virtual environment (`.venv`) support.
* **Search Strategy:** Advanced dorking queries (`"Company Name" linkedin company`) via Google JSON API.

## 📁 Project Structure
* `linkedin_scraper.py`: Core automation engine.
* `LK-company-finder.xlsx`: Input/Output database (Column A: Company Names | Column B: LinkedIn URLs).
* `api_keys.xlsx`: Credential storage for multiple API keys and Search Engine IDs (`cx`).

## ⚙️ How it Works
1. **Targeting**: The script identifies files relative to its execution directory, ensuring portability.
2. **Quota Management**: Loads a credential pool to bypass the 100-search daily limit.
3. **Pattern Validation**: Parses JSON responses to ensure extracted links match the `linkedin.com/company/` pattern.
4. **Auto-Save**: Updates the Excel file after each successful find to prevent data loss.

## 📝 Setup & Usage
1. **API Credentials**: Generate your API keys via the [Google Cloud Console](https://console.cloud.google.com/).
2. **Search Engine ID**: Create a Programmable Search Engine [here](https://programmablesearchengine.google.com/) and set it to "Search the entire web".
3. **Configuration**: 
    * Add your keys to `api_keys.xlsx`.
    * Place your company list in `LK-company-finder.xlsx`.
4. **Run**:
   ```bash
   pip install pandas requests openpyxl
   python linkedin_scraper.py
