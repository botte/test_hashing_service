""" Verify GET /stats.  

    GET to /stats should
        - Accept no data
        - Return a JSON data structure
        - Total hash requests since the server started.
        - Average time of a hash requests in milliseconds since server started.
"""

import requests
import json



def test_stats_with_data(get_with_data):
    """ GET to /stats should accept no data. """
    stats = get_with_data('/stats')
    assert stats.status_code != requests.codes.ok, 'GET /stats should not accept data.'



def test_stats_json_data_structure_as_json_object(get_no_header):
    """ GET to /stats should return as JSON data structure. """

    stats = get_no_header('/stats')
    assert stats.status_code == requests.codes.ok, 'GET/stats status_code not OK.'

    try:
        as_json = stats.json()
    except ValueError as e:
        assert False, 'GET /stats did not return a JSON Object.'



def test_stats_json_no_posts(get_no_header):
    """ GET to /stats should return
        - Total hash requests since the server started.
        - Average time of a hash requests in milliseconds since server started.
    """

    stats = get_no_header('/stats')
    as_json = stats.json()

    total_requests = as_json['TotalRequests']

    assert isinstance(total_requests, int),\
            'GET /stats TotalRequests did not return integer.'
    assert total_requests == 0,\
            'GET /stats TotalRequests when no POST /hash did not return 0.' + str(total_requests)

    average_time = as_json['AverageTime']

    assert isinstance(average_time, int),\
            'GET /stats AverageTime did not return integer.'
    assert average_time == 0,\
            'GET /stats AverageTime when no POST /hash did not return 0.' + str(average_time)



def test_stats_with_posts(get_no_header, post):
    """ GET to /stats should return
        - Total hash requests since the server started.
        - Average time of a hash requests in milliseconds since server started.
    """

    for i in range(10):

        post_response = post('/hash', 'password')
        stats = get_no_header('/stats')
        assert stats.status_code == requests.codes.ok, 'GET/stats status_code not OK.'

        as_json = stats.json()

        total_requests = as_json['TotalRequests']

        assert isinstance(total_requests, int),\
                'GET /stats TotalRequests did not return integer.'
        assert total_requests >= 0,\
                'GET /stats TotalRequests when POST /hash not positive.' + str(total_requests)

        average_time = as_json['AverageTime']

        assert isinstance(average_time, int),\
                'GET /stats AverageTime did not return integer.'
        assert average_time >= 0,\
                'GET /stats AverageTime when POST /hash did not positive.' + str(average_time)



def test_stats_average_time(get_no_header, post):
    """ GET to /stats should return average time of a hash request in milliseconds. """

    # Expected time for one hash request is ~ 5 seconds + some milliseconds.
    # Assumed max time in milliseconds for POST /hash: 5 seconds * factor * 1000.
    assumed_max_avg = 5 * 10 * 1000 

    for i in range(10):

        post_response = post('/hash', 'password')

        stats = get_no_header('/stats')
        as_json = stats.json()
        average_time = as_json['AverageTime']

        assert average_time <= assumed_max_avg,\
                'Average time hash request {} > assumed max milliseconds {}'.format(average_time, assumed_max_avg)
