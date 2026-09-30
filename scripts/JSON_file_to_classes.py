#!/usr/bin/python3
import argparse
import ast
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import colorama
from colorama import Back, Fore, Style

# Add the project root to sys.path to allow imports from vrailang
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from vrailang import dataconstraints, datatypes
from vrailang.dataconstraints import DataTypeAnnotation
from vrailang.datatypes import DataType, GeometryType

TAB = ' ' * 4

theme_dict = {'tn': 'transport',
              'au': 'administrative_units',
              'hy': 'hydrography',
              'ib': 'international_boundaries'}


class ArgumentParserColoredMessages(argparse.ArgumentParser):
    def error(self, message):
        print(Style.BRIGHT + Fore.RED, end='')
        print(f"{self.prog}: error: {message}")

        print(Style.NORMAL + Fore.GREEN)
        self.print_help()
        print(Style.RESET_ALL)
    
        self.exit(2, "")
    
    def print_help(self, file=None):
        print(Style.NORMAL + Fore.GREEN)
        super().print_help(file=file)
        print(Style.RESET_ALL)

def handle_cmdline() -> tuple[str, str, str]:
    parser = ArgumentParserColoredMessages()
    parser.add_argument('--input', required=True, metavar='SCHEMA', dest='input', help='Path to the schema file')
    parser.add_argument('--specs', required=True, metavar='SPECS', dest='specs', help='Directory containing the validation specifications')
    parser.add_argument('--output', required=True, metavar='DIR', dest='output', help='Output directory for storing generated classes')
    
    args = parser.parse_args()
    return args.specs, args.output, args.input

@dataclass(frozen=True)
class TypeSpec:
    typ: type[DataType]
    annotations: tuple[DataTypeAnnotation, ...] = field(default=())

    def __init__(
        self,
        typ: type[DataType],
        *annotations: DataTypeAnnotation,
    ):
        object.__setattr__(self, "typ", typ)
        object.__setattr__(self, "annotations", annotations)
    
    def with_prepended_constraints(self, *annotations) -> "TypeSpec":
        return TypeSpec(self.typ, *(annotations + self.annotations))

    def render(self) -> str:
        parts = [
            repr(a)
            for a in self.annotations
        ]

        if parts:
            return f"{self.typ.__name__}[{', '.join(parts)}]"
        return self.typ.__name__

def get_type_map(srid: str | int) -> dict[str, TypeSpec]:
    srid = int(srid)
    return {
        'uuid': TypeSpec(datatypes.uuid, dataconstraints.notnull),
        'timestamp': TypeSpec(datatypes.timestamp),
        'character varying(8)': TypeSpec(datatypes.varchar, dataconstraints.length(8)),
        'character varying(255)': TypeSpec(datatypes.varchar, dataconstraints.length(255)),
        'character varying(80)': TypeSpec(datatypes.varchar, dataconstraints.length(80)),
        'integer': TypeSpec(datatypes.int4),
        'jsonb': TypeSpec(datatypes.jsonb),
        'geometry(LineStringZ,${srid})': TypeSpec(datatypes.LineStringZ, dataconstraints.srid(srid)),
        'geometry(LineString,${srid})': TypeSpec(datatypes.LineString, dataconstraints.srid(srid)),
        'geometry(MultiLineStringZ,${srid})': TypeSpec(datatypes.MultiLineStringZ, dataconstraints.srid(srid)),
        'geometry(MultiLineString,${srid})': TypeSpec(datatypes.MultiLineString, dataconstraints.srid(srid)),
        'geometry(PointZ,${srid})': TypeSpec(datatypes.PointZ, dataconstraints.srid(srid)),
        'geometry(Point,${srid})': TypeSpec(datatypes.Point, dataconstraints.srid(srid)),
        'geometry(MultiPolygonZ,${srid})': TypeSpec(datatypes.MultiPolygonZ, dataconstraints.srid(srid)),
        'geometry(MultiPolygon,${srid})': TypeSpec(datatypes.MultiPolygon, dataconstraints.srid(srid)),           
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
    specs_dir, output_dir, path_to_schema = handle_cmdline()
    colorama.init(autoreset=True)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(path_to_schema, 'r') as file:
        schema: dict[str, Any] = json.load(file)

    type_map = get_type_map(schema['srid'])

    common_part = construct_common_part(schema, type_map)

    dict_theme_to_tables: dict[str, dict[str, list[str]]] = {}

    themes: dict[str, Any] = schema['themes']
    for theme_name in themes:
        dict_table_to_class_attributes: dict[str, list[str]] = {}

        tables: dict[str, Any] = themes[theme_name]['tables']
        for table_name in tables:  # noqa: PLC0206
            table_part, has_geometry = construct_table_part(tables[table_name], type_map)

            if has_geometry:
                dict_table_to_class_attributes[table_name] = common_part + table_part
            else:
                print(f"\n{Style.BRIGHT}{Fore.YELLOW}*** Skipping {table_name} as it has no geometry columns...")

        dict_theme_to_tables[theme_name] = dict_table_to_class_attributes

    for theme in dict_theme_to_tables:  # noqa: PLC0206
        theme_name = theme_dict[theme]
        print(f"\n{Style.BRIGHT}{Back.GREEN}{Fore.CYAN}{theme_name}")
        path_to_file_theme = os.path.join(specs_dir, f"{theme_name}.py")
        path_to_save_classes_theme = os.path.join(output_dir, f"{theme_name}.txt")

        with open(path_to_save_classes_theme, 'w', encoding='utf-8') as f:
            f.write("")

        for table_name in dict_theme_to_tables[theme]:
            print(f'\n{Style.BRIGHT}{Fore.GREEN}{table_name}')
            string_for_table = f"class {table_name}(feature):\n"
            class_from_file = extract_class(path=path_to_file_theme, classname=table_name)

            list_of_attributes = dict_theme_to_tables[theme][table_name]
            for attribute in list_of_attributes:
                string_for_table += f"{TAB}{attribute}\n"

            with open(path_to_save_classes_theme, 'a', encoding='utf-8') as f:
                f.write(string_for_table + '\n')

            #compare
            if class_from_file == "":
                print(f"{Fore.YELLOW}No existing class for {table_name}")
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


def construct_common_part(schema: dict[str, Any], type_map: dict[str, TypeSpec]) -> list[str]:
    common_part: list[str] = []
    for x in schema['common']:
        for attribute_name in schema['common'][x]:
            attribute_type_text = schema['common'][x][attribute_name]['sql_type'].split('DEFAULT')[0].split('without')[
                0].strip()

            type_spec = type_map[attribute_type_text]
            if schema['common'][x][attribute_name].get('pkey') is True:
                type_spec = type_spec.with_prepended_constraints(dataconstraints.primary_key)
            attribute_type = type_spec.render()
            
            common_part.append(f"{attribute_name}: {attribute_type}")
    
    return common_part


def construct_table_part(table: dict[Literal['fields'], dict[str, Any]], type_map: dict[str, TypeSpec]) -> tuple[list[str], bool]:
    table_part: list[str] = []

    has_geometry = False
    for attribute_name in table['fields']:
        attribute_type_text: str = \
                table['fields'][attribute_name]['sql_type'].split('DEFAULT')[0].split(
                    'without')[0].strip()

        type_spec = type_map[attribute_type_text]
        if table['fields'][attribute_name].get('pkey') is True:
            type_spec = type_spec.with_prepended_constraints(dataconstraints.primary_key)
        attribute_type = type_spec.render()

        table_part.append(f"{attribute_name}: {attribute_type}")

        if issubclass(type_spec.typ, GeometryType):
            has_geometry = True
    
    return table_part,has_geometry



if __name__ == "__main__":
    main()
