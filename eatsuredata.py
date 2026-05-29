from curl_cffi import requests
import json
import jmespath
import time

headers = {
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.eatsure.com/',
    'user-agent': 'Mozilla/5.0',
}

brand_ids = [
    20,   
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34
]

all_products = []


for brand_id in brand_ids:

    print(f"\nSCRAPING BRAND: {brand_id}")

    url = f"https://www.eatsure.com/v1/api/get_all_products/brand_id/{brand_id}/store_id/10162/source_id/3"

    response = requests.get(
        url,
        impersonate="chrome120",
        headers=headers,
    )

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        continue

    data = response.json()


    query = """
    data.collections[].{
        collection_name: collection_name,
        products: products[].{
            brand_name: brand_name,
            product_name: product_name,
            image_url: product_imageUrl,
            small_description: small_description,
            rating: rating,
            price: price,

            calories: details.nutritional_information[?name=='Calories']|[0].value,
            protein: details.nutritional_information[?name=='Proteins']|[0].value,
            fats: details.nutritional_information[?name=='Fats']|[0].value
        }
    }
    """

    result = jmespath.search(query, data)

    if result:
        all_products.extend(result)

    time.sleep(1)


with open("all_brands_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=4, ensure_ascii=False)

print("\nALL DATA SAVED")