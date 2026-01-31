import pandas as pd
import os
import requests
import time

# --- PATH CONFIGURATION ---
# Uses the script's directory to find files, ensuring cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_COMPANIES = os.path.join(BASE_DIR, 'LK-company-finder.xlsx')
FILE_KEYS = os.path.join(BASE_DIR, 'api_keys.xlsx')

def get_linkedin_url(company_name, api_key, search_engine_id):
    """Perform search via Google Custom Search JSON API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': f'"{company_name}" linkedin company',
        'key': api_key,
        'cx': search_engine_id,
        'num': 1 
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            if items:
                link = items[0].get('link')
                if "linkedin.com/company/" in link:
                    return link
            return "Not Found"
        elif response.status_code == 429:
            # Daily quota (100 req/day) reached for this specific key
            return "QUOTA_EXCEEDED"
        else:
            return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # 1. Load API keys and Search Engine ID
    try:
        df_keys = pd.read_excel(FILE_KEYS)
        keys_list = df_keys['key'].tolist()
        cx_id = df_keys['cx'].iloc[0] 
    except Exception as e:
        print(f"Error loading API keys file: {e}")
        return

    # 2. Load company database
    try:
        df_comp = pd.read_excel(FILE_COMPANIES)
    except Exception as e:
        print(f"Error loading company file: {e}")
        return
    
    if 'Linkedin_URL' not in df_comp.columns:
        df_comp['Linkedin_URL'] = ""

    current_key_index = 0
    print(f"Starting process: {len(keys_list)} API keys available (Limit: 100 req/day each).")

    # 3. Iterate through companies
    for index, row in df_comp.iterrows():
        # Only process rows where URL is missing
        if pd.isna(row['Linkedin_URL']) or row['Linkedin_URL'] == "":
            company = row.iloc[0] 
            print(f"Searching for: {company}...")
            
            success = False
            while not success:
                if current_key_index >= len(keys_list):
                    print("⚠️ All API keys exhausted for today!")
                    df_comp.to_excel(FILE_COMPANIES, index=False)
                    return

                result = get_linkedin_url(company, keys_list[current_key_index], cx_id)
                
                if result == "QUOTA_EXCEEDED":
                    print(f"Key {current_key_index + 1} exhausted. Switching to next key...")
                    current_key_index += 1
                else:
                    df_comp.at[index, 'Linkedin_URL'] = result
                    success = True
                    time.sleep(0.5) # Anti-spam / rate limiting delay

    # 4. Final Save
    df_comp.to_excel(FILE_COMPANIES, index=False)
    print("✅ Success: The Excel file has been updated.")

if __name__ == "__main__":
    main()