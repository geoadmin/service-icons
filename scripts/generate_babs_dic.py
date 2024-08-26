import argparse
import json

# pylint: disable=import-error
import pandas as pd


def generate_translation_file(args):
    id_range = slice(0, -4)
    source = args.input
    destination = args.output
    df = pd.read_excel(source, sheet_name=0)
    for filename in ['Dateiname - D', 'Dateiname - F', 'Dateiname - I']:
        # read by default 1st sheet of an excel file
        json_dic = {}
        for index, row in df.iterrows():
            string_id = row[filename][id_range]
            icon_dic = {
                "de": row['Text Mouseover - D'],
                "fr": row['Text Mouseover - F'],
                "it": row['Text Mouseover - I']
            }
            json_dic[string_id] = icon_dic

        with open(
            destination + '-' + filename[-1] + '-dictionary.json', "w", encoding='utf-8'
        ) as outfile:
            json.dump(json_dic, outfile, indent=4)


def main():
    # example command:
    # python3 generate_babs_dic.py --input=../../tmp/babs.xlsx --output=../metadata/description/babs
    # (do not specify filetype for output since it creates a file for every language)
    parser = argparse.ArgumentParser(description='Create json translation file from excel file ')
    parser.add_argument('--input', action="store", dest='input', default=None)
    parser.add_argument('--output', action="store", dest='output', default=None)
    args = parser.parse_args()
    generate_translation_file(args)


if __name__ == '__main__':
    main()
