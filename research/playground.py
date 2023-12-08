import easyocr
reader= easyocr.Reader(['en'])
result= reader.readtext('research/receipt.jpeg')


for item in result:
    print(item[1])