#!/usr/bin/python3
import argparse
import ast
import json
import os

import colorama
from colorama import Fore, Back, Style  # noqa: F401

theme_dict = {'tn': 'transport',
              'au': 'administrative_units',
              'hy': 'hydrography',
              'ib': 'international_boundaries'}

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, metavar='SCHEMA', dest='input', help='Path to the schema file')
    parser.add_argument('--specs', required=True, metavar='SPECS', dest='specs', help='Directory containing the validation specifications')
    parser.add_argument('--output', required=True, metavar='DIR', dest='output', help='Output directory for storing generated classes')
    return parser

def get_dict(srid: str):
    return {'uuid': 'uuid[notnull]',
            'timestamp': 'timestamp',
            'character varying(8)': 'varchar[length(8)]',
            'character varying(255)': 'varchar[length(255)]',
            'character varying(80)': 'varchar[length(80)]',
            'integer': 'int4',
            'jsonb': 'jsonb',
            'geometry(LineStringZ,${srid})': f'LineStringZ[srid({srid})]',
            'geometry(LineString,${srid})': f'LineString[srid({srid})]',
            'geometry(MultiLineStringZ,${srid})': f'MultiLineStringZ[srid({srid})]',
            'geometry(MultiLineString,${srid})': f'MultiLineString[srid({srid})]',
            'geometry(PointZ,${srid})': f'PointZ[srid({srid})]',
            'geometry(Point,${srid})': f'Point[srid({srid})]',
            'geometry(MultiPolygonZ,${srid})': f'MultiPolygonZ[srid({srid})]',
            'geometry(MultiPolygon,${srid})': f'MultiPolygon[srid({srid})]',
            }


def get_dict_with_primary_key(srid):
    return {'uuid': 'uuid[primary_key, notnull]',
            'timestamp': 'timestamp[primary_key]',
            'character varying(8)': 'varchar[length(8), primary_key]',
            'character varying(255)': 'varchar[length(255), primary_key]',
            'character varying(80)': 'varchar[length(80), primary_key]',
            'integer': 'int4[primary_key]',
            'jsonb': 'jsonb[primary_key]',
            'geometry(LineStringZ,${srid})': f'LineStringZ[srid({srid}), primary_key]',
            'geometry(LineString,${srid})': f'LineString[srid({srid}), primary_key]',
            'geometry(MultiLineStringZ,${srid})': f'MultiLineStringZ[srid({srid}), primary_key]',
            'geometry(MultiLineString,${srid})': f'MultiLineString[srid({srid}), primary_key]',
            'geometry(PointZ,${srid})': f'PointZ[srid({srid}), primary_key]',
            'geometry(Point,${srid})': f'Point[srid({srid}), primary_key]',
            'geometry(MultiPolygonZ,${srid})': f'MultiPolygonZ[srid({srid}), primary_key]',
            'geometry(MultiPolygon,${srid})': f'MultiPolygon[srid({srid}), primary_key]',
            }


def extract_class(path, classname):
    if not os.path.exists(path):
        print(f"File '{path}' does not exist.")
        return ""

    with open(path, 'r') as fh:
        source = fh.read()

    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == classname:
            lines = source.splitlines()
            start = node.lineno - 1
            end = node.end_lineno
            relevant_lines = [
                line for line in lines[start:end]
                if line.strip() and not line.lstrip().startswith('#')
            ]

            return '\n'.join(relevant_lines)

    print(f"Class '{classname}' not found in file '{path}'.")
    return ""


def main() -> None:
    parser = get_parser()
    print(Style.BRIGHT + Fore.RED, end='')
    try:
        args = parser.parse_args()
    except SystemExit:
        print(Style.NORMAL + Fore.GREEN)
        parser.print_help()
        print(Style.RESET_ALL)
        return
    
    colorama.init(autoreset=True)

    path_to_file = args.specs
    path_to_save_classes = args.output
    path_to_schema = args.input

    if not os.path.exists(path_to_save_classes):
        os.makedirs(path_to_save_classes)

    with open(path_to_schema, 'r') as file:
        data = json.load(file)

    srid = data['srid']
    dict_text_to_type = get_dict(srid=srid)
    dict_text_to_type_with_primary_key = get_dict_with_primary_key(srid=srid)

    common_part = []

    for x in data['common']:
        for attribute_name in data['common'][x]:
            attribute_type_text = data['common'][x][attribute_name]['sql_type'].split('DEFAULT')[0].split('without')[
                0].strip()

            if data['common'][x][attribute_name].get('pkey') is True:
                attribute_type = dict_text_to_type_with_primary_key[attribute_type_text]
            else:
                attribute_type = dict_text_to_type[attribute_type_text]

            common_part.append(f"{attribute_name}: {attribute_type}")

    dict_theme_to_tables = {}

    for theme in data['themes']:
        dict_table_to_class_attributes = {}
        for y in data['themes'][theme]['tables']:
            theme_part = []
            for attribute_name in data['themes'][theme]['tables'][y]['fields']:
                attribute_type_text = \
                data['themes'][theme]['tables'][y]['fields'][attribute_name]['sql_type'].split('DEFAULT')[0].split(
                    'without')[0].strip()

                if data['themes'][theme]['tables'][y]['fields'][attribute_name].get('pkey') is True:
                    attribute_type = dict_text_to_type_with_primary_key[attribute_type_text]
                else:
                    attribute_type = dict_text_to_type[attribute_type_text]

                theme_part.append(f"{attribute_name}: {attribute_type}")
            dict_table_to_class_attributes[y] = common_part + theme_part

        dict_theme_to_tables[theme] = dict_table_to_class_attributes

    for theme in dict_theme_to_tables:
        theme_name = theme_dict[theme]
        print(f"\n{Style.BRIGHT}{Back.GREEN}{Fore.CYAN}{theme_name}")
        path_to_file_theme = os.path.join(path_to_file, f"{theme_name}.py")
        path_to_save_classes_theme = os.path.join(path_to_save_classes, f"{theme_name}.txt")

        with open(path_to_save_classes_theme, 'w', encoding='utf-8') as f:
            f.write("")

        for table in dict_theme_to_tables[theme]:
            print(f'\n{Style.BRIGHT}{Fore.GREEN}{table}')
            string_for_table = f"class {table}(feature): \n"
            class_from_file = extract_class(path=path_to_file_theme, classname=table)

            list_of_attributes = dict_theme_to_tables[theme][table]
            for attribute in list_of_attributes:
                string_for_table += f"\t{attribute} \n"

            with open(path_to_save_classes_theme, 'a', encoding='utf-8') as f:
                f.write(string_for_table + '\n')

            #compare
            if class_from_file == "":
                print(f"{Fore.YELLOW}No existing class for {table}")
                continue

            string_for_table_as_lines = string_for_table.splitlines()
            class_from_file_as_lines = class_from_file.splitlines()

            print(f"#Features in json {len(string_for_table_as_lines) - 1}")
            print(f"#Features in current class {len(class_from_file_as_lines) - 1}")

            number_of_found_matches = 0
            for line_current in class_from_file_as_lines[1:]:
                line_current_split = line_current.strip().split(':')
                found_match = False
                for line_new in string_for_table_as_lines[1:]:
                    line_new_split = line_new.strip().split(':')
                    if line_current_split[0] == line_new_split[0]:
                        found_match = True
                        if line_current_split[1] == line_new_split[1]:
                            number_of_found_matches += 1
                        else:
                            number_of_found_matches += 1
                            print(f"{Style.BRIGHT}{Fore.RED}Different types for {line_current_split[0]}. Current type is {line_current_split[1].strip()} and new type: {line_new_split[1].strip()}.")
                        continue
                if not found_match:
                    print(f"{Fore.RED}Feature {line_current.strip()} is not in json.")

            if number_of_found_matches < len(string_for_table_as_lines) - 1:
                for line_new in string_for_table_as_lines[1:]:
                    line_new_split = line_new.strip().split(':')
                    found_match = False
                    for line_current in class_from_file_as_lines[1:]:
                        line_current_split = line_current.strip().split(':')

                        if line_current_split[0] == line_new_split[0]:
                            found_match = True
                            continue
                    if not found_match:
                        print(f"{Fore.RED}Feature {line_new.strip()} is not in current class.")


if __name__ == "__main__":
    main()
