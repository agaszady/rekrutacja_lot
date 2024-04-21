import os
import pandas as pd
import xmlschema
import argparse


def xml_to_dataframe(xml_path: str, schema_path: str) -> pd.DataFrame:
    if not os.path.exists(xml_path):
        print(f"Plik {xml_path} nie istnieje lub podana ścieżka jest błędna.")
        return False
    if not is_xml_valid(schema_path, xml_path):
        return
    df_from_xml = pd.read_xml(xml_path)
    print(df_from_xml)
    return df_from_xml


def is_xml_valid(schema_path: str, xml_path: str) -> bool:
    if not os.path.exists(schema_path):
        print(f"Plik {schema_path} nie istnieje lub podana ścieżka jest błędna.")
        return False
    xml_schema = xmlschema.XMLSchema(schema_path)
    is_valid = False
    try:
        is_valid = xml_schema.is_valid(xml_path)
    except Exception as e:
        print(f"Błąd parsowania XML {xml_path}:")
        print(e)
        return False
    if is_valid:
        return True
    else:
        try:
            xml_schema.validate(xml_path)
        except xmlschema.XMLSchemaValidationError as e:
            print(f"Błędny schemat pliku XML {xml_path}")
            print(e)
        return False


def main():
    # Tworzenie parsera argumentów
    parser = argparse.ArgumentParser(description='Filter people by specified criteria.')

    # Dodanie argumentów
    parser.add_argument('--rank', type=str, help='Filter by rank')
    parser.add_argument('--gender', type=str, choices=['Male', 'Female'],
                        help='Filter by gender')
    parser.add_argument('--salary-range', nargs=2, type=int, metavar=('MIN', 'MAX'),
                        help='Filter by salary range')

    # Parsowanie argumentów z linii poleceń
    args = parser.parse_args()
    # Wyświetlanie rezultatów
    if args.rank:
        print("Filtering by rank:", args.rank)
    if args.gender:
        print("Filtering by gender:", args.gender)
    if args.salary_range:
        print("Filtering by salary range:", args.salary_range[0], "-", args.salary_range[1])

if __name__ == "__main__":
    main()

# xml_to_dataframe("example_files/people1.xml", "schema_people.xsd")
# xml_to_dataframe("example_files/people2.xml", "schema_people.xsd")
# xml_to_dataframe("example_files/people3.xml", "schema_people.xsd")
# xml_to_dataframe("example_files/people4.xml", "schema_people.xsd")
# ("example_files/people5.xml", "schema_people.xsd")
# xml_to_dataframe("example_files/people6.xml", "schema_people.xsd")
