import json


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


def main() -> None:
    with open(r'../json/example.json', 'r') as file:
        data = json.load(file)

    srid = data['srid']
    dict_text_to_type = get_dict(srid=srid)

    common_part = []

    for x in data['common']:
        for y in data['common'][x]:
            attribute_name = y

            attribute_type_text = data['common'][x][y]['sql_type'].split('DEFAULT')[0].split('without')[0].strip()
            attribute_type = dict_text_to_type[attribute_type_text]

            common_part.append(f"{attribute_name}: {attribute_type}")

    dict_theme_to_tables = {}

    for x in data['themes']:
        dict_table_to_class_attributes = {}

        for y in data['themes'][x]['tables']:
            theme_part = []
            for z in data['themes'][x]['tables'][y]['fields']:
                attribute_name = z
                attribute_type_text = \
                data['themes'][x]['tables'][y]['fields'][z]['sql_type'].split('DEFAULT')[0].split('without')[0].strip()
                attribute_type = dict_text_to_type[attribute_type_text]
                theme_part.append(f"{attribute_name}: {attribute_type}")
            dict_table_to_class_attributes[y] = common_part + theme_part

        dict_theme_to_tables[x] = dict_table_to_class_attributes

    for theme in dict_theme_to_tables:
        print(f"{theme} \n")
        for table in dict_theme_to_tables[theme]:
            string_for_table = f"class {table}(feature): \n"
            list_of_attributes = dict_theme_to_tables[theme][table]
            for attribute in list_of_attributes:
                string_for_table += f"\t{attribute} \n"
            print(string_for_table)


if __name__ == "__main__":
    main()
