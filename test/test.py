import os
import pytest
import pandas as pd
import xmlschema
import argparse
from rekrutacja_lot.task_python import is_xml_valid, filter_by_criteria

schema = xmlschema.XMLSchema("../schema_people.xsd")

@pytest.mark.parametrize("schema, xml_path, expected_result", [
    (schema, "../example_files/people.xml", True),  # poprawny plik XML
    (schema, "../example_files/people_empty.xml", False),  # pusty plik XML
    (schema, "../example_files/people_empty_spaces.xml", False),  # plik XML z pustymi wartościami
    (schema, "../example_files/people1.xml", False),  # niepoprawny plik XML-brak znacznika
    (schema, "../example_files/people2.xml", False),  # niepoprawny plik XML-zła wartość gender
    (schema, "../example_files/people3.xml", False),  # niepoprawny plik XML-zła wartość salary
    (schema, "../example_files/people4.xml", False),  # niepoprawny plik XML-dodatkowy tag
    (schema, "../example_files/people5.xml", False),  # niepoprawny plik XML-brak znacznika
    (schema, "../example_files/people6.xml", False),  # zamieniona kolejność
])
def test_is_xml_valid(schema, xml_path, expected_result):
    assert is_xml_valid(schema, xml_path) == expected_result


@pytest.mark.parametrize("data, args, expected_result", [
    (pd.DataFrame({
        'rank': [],
        'gender': [],
        'salary': [],
        'age': []
    }),
     argparse.Namespace(rank='Manager', gender=None, salary_range=None, age_range=None),
     pd.DataFrame({
         'rank': [],
         'gender': [],
         'salary': [],
         'age': []
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank='Manager', gender=None, salary_range=None, age_range=None),
     pd.DataFrame({
        'rank': ['Manager'],
        'gender': ['Female'],
        'salary': [50000],
        'age': [40]
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
      argparse.Namespace(rank='Manager', gender='Male', salary_range=None, age_range=None),
      pd.DataFrame({
        'rank': [],
        'gender': [],
        'salary': [],
        'age': []
      })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank='Tester', gender='Female', salary_range=None, age_range=None),
     pd.DataFrame({
         'rank': ['Tester'],
         'gender': ['Female'],
         'salary': [55000],
         'age': [29]
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank=None, gender=None, salary_range=None, age_range=None),
     pd.DataFrame({
         'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
         'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
         'salary': [50000, 60000, 70000, 55000, 65000],
         'age': [40, 35, 30, 29, 25]
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank=None, gender=None, salary_range=(75000, 90000), age_range=None),
     pd.DataFrame({
         'rank': [],
         'gender': [],
         'salary': [],
         'age': []
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank=None, gender=None, salary_range=(50000, 60000), age_range=None),
     pd.DataFrame({
         'rank': ['Manager', 'Developer', 'Tester'],
         'gender': ['Female', 'Male', 'Female'],
         'salary': [50000, 60000, 55000],
         'age': [40, 35, 29]
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank=None, gender=None, salary_range=(50000, 60000), age_range=(30, 40)),
     pd.DataFrame({
         'rank': ['Manager', 'Developer'],
         'gender': ['Female', 'Male'],
         'salary': [50000, 60000],
         'age': [40, 35]
     })
    ),
    (pd.DataFrame({
        'rank': ['Manager', 'Developer', 'Tester', 'Tester', 'Designer'],
        'gender': ['Female', 'Male', 'Male', 'Female', 'Female'],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'age': [40, 35, 30, 29, 25]
    }),
     argparse.Namespace(rank=None, gender=None, salary_range=None, age_range=(40, 30)),
     pd.DataFrame({
         'rank': [],
         'gender': [],
         'salary': [],
         'age': []
     })
    ),
])
def test_filter_by_criteria(data, args, expected_result):
    result = filter_by_criteria(data, args)
    if len(result) == 0:
        assert len(result) == len(expected_result)
    else:
        pd.testing.assert_frame_equal(result, expected_result)