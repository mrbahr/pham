import sys
import requests
import csv
import time

base_api_url = "https://sallyapi.witheldokan.com/api/customer/products/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def get_active_ingredient(slug):
    detail_url = f"https://sallyapi.witheldokan.com/api/customer/products/{slug}/slug?ignore_similar_products=1"
    try:
        res = requests.get(detail_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            product_data = data.get('data', {}).get('product', {})
            for attr in product_data.get('details', {}).get('attributes', []):
                if attr.get('option_en') == 'Active Ingredients':
                    return attr.get('value_ar') or attr.get('value_en', 'N/A')
    except:
        pass
    return "N/A"

def start_automated_scraper():
    filename = 'phpri.csv'
    print(f"🚀 Automated Scrape Started. Saving to {filename}")
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['Name_AR', 'Name_EN', 'Price', 'Brand', 'Category', 'Active_Ingredients', 'Stock', 'Slug'])
            
            page_num = 1
            total_items = 0
            
            while True:
                params = {"enable_search_side_filters": "1", "page": page_num}
                try:
                    response = requests.get(base_api_url, headers=headers, params=params, timeout=25)
                    if response.status_code != 200:
                        break
                    
                    data = response.json()
                    products = data.get('data', {}).get('products', [])
                    
                    if not products:
                        break
                    
                    for p in products:
                        name_ar = p.get('name_ar', 'N/A')
                        name_en = p.get('name_en', 'N/A')
                        price = p.get('price', 0)
                        stock = p.get('stock', 0)
                        slug = p.get('slug', '')
                        
                        brand_data = p.get('brand')
                        brand = brand_data.get('name_en', 'N/A') if isinstance(brand_data, dict) else "N/A"
                        
                        cat_data = p.get('category')
                        cat = cat_data.get('name_en', 'N/A') if isinstance(cat_data, dict) else "N/A"
                        
                        ingred = get_active_ingredient(slug) if slug else "N/A"
                        
                        writer.writerow([name_ar, name_en, price, brand, cat, ingred, stock, slug])
                        total_items += 1
                        time.sleep(0.4)
                    
                    print(f"Page {page_num} finished. Total items: {total_items}")
                    page_num += 1
                    
                except requests.exceptions.RequestException:
                    time.sleep(5)
                    continue
            
        print(f"Successfully saved {total_items} items.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_automated_scraper()
