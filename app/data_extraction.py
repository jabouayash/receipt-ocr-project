import re

def extract_item_price_pairs(texts):
    pattern = r'([0-9]+\.[0-9]+)'

    for row in texts.split('\n'):
        match = re.search(pattern, row)
        if match:
            print(row)
