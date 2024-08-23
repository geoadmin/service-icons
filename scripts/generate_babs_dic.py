import argparse
import json

import pandas as pd


def generate_translation_file(args):
    id_range = slice(0, 3)
    source = args.input
    destination = args.output
    # read by default 1st sheet of an excel file
    df = pd.read_excel(source, sheet_name=0)

    json_dic = {}
    for index, row in df.iterrows():
        string_id = row['Dateiname - D'][id_range]
        icon_dic = {
            "de": row['Text Mouseover - D'],
            "fr": row['Text Mouseover - F'],
            "it": row['Text Mouseover - I']
        }
        json_dic["ICON_" + string_id] = icon_dic

    with open(destination, "w", encoding='utf-8') as outfile:
        json.dump(json_dic, outfile, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Create json translation file from excel file ')
    parser.add_argument('--input', action="store", dest='input', default=None)
    parser.add_argument('--output', action="store", dest='output', default=None)
    args = parser.parse_args()
    generate_translation_file(args)


if __name__ == '__main__':
    main()
