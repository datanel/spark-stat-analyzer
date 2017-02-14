import pytest
from datetime import date
from analyzers.requests_calls import AnalyzeRequest
import os

pytestmark = pytest.mark.usefixtures("spark")


def same_list_tuple(list_tuple_1, list_tuple_2):
    if len(list_tuple_1) != len(list_tuple_2):
        return False
    for i, item in enumerate(list_tuple_1):
        if cmp(item, list_tuple_2[i]) != 0:
            return False
    return True


def test_requests_calls(spark):
    path = os.getcwd() + "/tests/fixtures/requests_calls"
    start_date = date(2017, 1, 1)
    end_date = date(2017, 1, 1)

    analyze_request = AnalyzeRequest(storage_path=path,
                                     start_date=start_date,
                                     end_date=end_date,
                                     spark_context=spark,
                                     database=None)

    files = analyze_request.get_files_to_analyze()

    expected_files = [path + '/2017/01/01/requests_calls.json.log']

    assert len(files) == len(expected_files)
    assert len(set(files) - set(expected_files)) == 0
    result = analyze_request.get_data()
    expected_results = [(u'fr-auv', u'v1.journeys', 22, u'test filbleu', 0, u'2017-01-01', 1, 1, 0, 0),
                        (u'region:2', u'v1.pt_objects', 25, u'', 0, u'2017-01-01', 1, 2, 2, 0),
                        (u'', u'v1.coverage', 51, u'', 0, u'2017-01-01', 1, 1, 1, 0),
                        (u'region:2', u'v1.networks.collection', 25, u'', 0, u'2017-01-01', 1, 1, 1, 4),
                        (u'region:1', u'v1.stop_areas.collection', 51, u'', 0, u'2017-01-01', 1, 3, 3, 75)]

    assert same_list_tuple(result, expected_results)


def test_requests_calls_without_journeys(spark):
    path = os.getcwd() + "/tests/fixtures/requests_calls"
    start_date = date(2017, 1, 2)
    end_date = date(2017, 1, 2)

    analyze_request = AnalyzeRequest(storage_path=path,
                                     start_date=start_date,
                                     end_date=end_date,
                                     spark_context=spark,
                                     database=None)

    files = analyze_request.get_files_to_analyze()

    expected_files = [path + '/2017/01/02/requests_calls.json.log']

    assert len(files) == len(expected_files)
    assert len(set(files) - set(expected_files)) == 0
    result = analyze_request.get_data()
    expected_results = [(u'region:2', u'v1.pt_objects', 25, u'', 0, u'2017-01-01', 1, 2, 2, 0),
                        (u'', u'v1.coverage', 51, u'', 0, u'2017-01-01', 1, 1, 1, 0),
                        (u'region:2', u'v1.networks.collection', 25, u'', 0, u'2017-01-01', 1, 1, 1, 4),
                        (u'region:1', u'v1.stop_areas.collection', 51, u'', 0, u'2017-01-01', 1, 3, 3, 75)]
    assert same_list_tuple(result, expected_results)
