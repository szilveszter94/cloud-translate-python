import csv
import os
from google.cloud import translate_v2

EXISTING_FIELDS = ['COLLECTION', 'DELIVERY_METHOD_DEFINITION', 'EMAIL_TEMPLATE', 'LINK', 'METAFIELD',
                   'ONLINE_STORE_ARTICLE', 'ONLINE_STORE_BLOG', 'ONLINE_STORE_MENU', 'ONLINE_STORE_PAGE',
                   'ONLINE_STORE_THEME', 'PACKING_SLIP_TEMPLATE', 'PAYMENT_GATEWAY', 'PRODUCT', 'PRODUCT_OPTION',
                   'PRODUCT_VARIANT']

TARGET_LANGUAGE = 'de'
OUTPUT_FILE_NAME = 'german.csv'
INPUT_FILE_NAME = 'data_to_translate.csv'

# here you can choose which field you want to translate (from the 'EXISTING_FIELDS')
FIELDS_TO_TRANSLATE = ['COLLECTION', 'DELIVERY_METHOD_DEFINITION',
                       'LINK', 'METAFIELD', 'ONLINE_STORE_BLOG',
                       'ONLINE_STORE_MENU', 'PAYMENT_GATEWAY', 'PRODUCT',
                       'PRODUCT_OPTION', 'PRODUCT_VARIANT']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'google_key.json'
translate_client = translate_v2.Client()

with open(INPUT_FILE_NAME, 'r', encoding='utf-8') as file, open(OUTPUT_FILE_NAME, 'w', encoding='utf-8',
                                                                newline='') as output_file:
    csv_reader = csv.reader(file)
    csv_writer = csv.writer(output_file)
    # Write the header row to the output file
    header = next(csv_reader)
    csv_writer.writerow(header)
    already_translated_dict = {}
    hashmap_for_long_text_to_translate = {}
    counter = 0
    for row in csv_reader:
        counter += 1
        # Get the default content from the row
        default_content = row[6]
        if len(default_content) and row[0] in FIELDS_TO_TRANSLATE:
            if default_content.isalpha():
                lowercase = default_content.lower()
                if already_translated_dict.get(lowercase) is not None:
                    row[7] = already_translated_dict[lowercase]
                else:
                    translated_content = translate_client.translate(default_content, target_language=TARGET_LANGUAGE)
                    already_translated_dict[lowercase] = (translated_content['translatedText'])
                    row[7] = translated_content['translatedText']
            else:
                if not default_content.isnumeric():
                    hash_key = hash(default_content)
                    if hashmap_for_long_text_to_translate.get(hash_key) is not None:
                        row[7] = hashmap_for_long_text_to_translate[hash_key]
                    else:
                        translated_content = translate_client.translate(default_content,
                                                                        target_language=TARGET_LANGUAGE)
                        hashmap_for_long_text_to_translate[hash_key] = translated_content['translatedText']
                        row[7] = translated_content['translatedText']
        csv_writer.writerow(row)
        counter += 1
        print(175569, counter)
