# Program filtrujący informacje o osobach z pliku XML wg zadanych kryteriów
import os
import pandas as pd
import xmlschema
import argparse

# funkcja sprawdzająca czy plik XML
# 1. nie zawiera błędów uniemożliwiających parsowanie
# 2. jest zgodny z przyjętym schematem
def is_xml_valid(xml_schema: xmlschema.XMLSchema, xml_path: str) -> bool:
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

# funkcja filtrująca pd.DataFrame wg zadanych kryteriów
def filter_by_criteria(df_from_xml: pd.DataFrame, args) -> pd.DataFrame:
    if args.rank:
        df_from_xml = df_from_xml[df_from_xml['rank'] == args.rank]
    if args.gender:
        df_from_xml = df_from_xml[df_from_xml['gender'] == args.gender]
    if args.salary_range:
        df_from_xml = df_from_xml[df_from_xml['salary'].between(args.salary_range[0],
                                                                args.salary_range[1])]
    if args.age_range:
        df_from_xml = df_from_xml[df_from_xml['age'].between(args.age_range[0],
                                                             args.age_range[1])]
    if df_from_xml.empty:
        print("Nie znaleziono osób dla podanych kryteriów!")
    else:
        df_from_xml.reset_index(drop=True, inplace=True)
        print(df_from_xml)
    return df_from_xml


def main():
    # stworzenie parsera
    parser = argparse.ArgumentParser(description='Filter people by specified criteria.')
    # dodanie argumentów
    parser.add_argument('--rank', type=str, help='Filter by rank')
    parser.add_argument('--gender', type=str, choices=['Male', 'Female'],
                        help='Filter by gender')
    parser.add_argument('--salary-range', nargs=2, type=int, metavar=('MIN', 'MAX'),
                        help='Filter by salary range')
    parser.add_argument('--age-range', nargs=2, type=int, metavar=('MIN', 'MAX'),
                        help='Filter by age range')
    args = parser.parse_args()

    # pliki ze schematem oraz danymi
    schema_path = "schema_people.xsd"
    xml_path = "example_files/people.xml"

    # sprawdzenie, czy podane ścieżki są poprawne
    if not os.path.exists(schema_path) or not os.path.exists(xml_path):
        print(f"Plik nie istnieje lub podana ścieżka jest błędna.")
        return
    # sprawdzenie, czy plik XML ma prawidłowe rozszerzenie
    if not xml_path.endswith(".xml"):
        return
    # stworzenie obiektu XMLSchema
    xml_schema = xmlschema.XMLSchema(schema_path)
    if not is_xml_valid(xml_schema, xml_path):
        return
    # załadowanie danych z XML do pd.DataFrame
    df_from_xml = pd.read_xml(xml_path)
    # print(df_from_xml)
    # uruchomienie funkcji filtrującej dane
    filter_by_criteria(df_from_xml, args)

if __name__ == "__main__":
    main()

