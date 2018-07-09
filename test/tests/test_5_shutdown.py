""" Verify POST /shutdown.

    - Shutdown return code 200 OK
    - Shutdown allows in-flight passwords to complete
    - When shutdown pending, no additional password requests should be allowed.
    - Server processes multiple simultaneous connections
"""

import requests
from multiprocessing import Process, Value
import time



def test_shutdown_no_data(baseurl):
    """ Verify shutdown return code 200 OK. """
    try:
        shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
        assert shutdown.status_code == requests.codes.ok, 'Shutdown no data response not 200'
    except Exception as e:
        assert False, 'Shutdown raised exception. {}'.format(e)



def test_shutdown_with_data(start_server_manual, baseurl, post):
    """ Verify shutdown return code 200 OK. """

    for i in range(5):
        post_response = post('/hash', 'password')

    try:
        shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
        assert shutdown.status_code == requests.codes.ok, 'Shutdown no data response not 200'
    except Exception as e:
        assert False, 'Shutdown raised exception. {}'.format(e)



def test_shutdown_when_requests(start_server_manual, baseurl, post, get):
    """ Verify shutdown return code 200 OK. """

    count = 10
    for i in range(count):
        try:
            post_response = post('/hash', 'password')
            get('/hash/' + str(post_response.text))
            get_with_data('/stats')

            if i == count//2:
                try:
                    shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
                    assert shutdown.status_code == requests.codes.ok, 'Shutdown no data response not 200'
                except Exception as e:
                    assert False, 'Shutdown raised exception. {}'.format(e)
        except Exception as e:
            pass



def test_stats_inflight_hash(start_server_manual, baseurl, post):
    """ Verify all in-flight POST /hash requests complete. """

    def client_post(token, count):

        if not token.value:
            try:
                post_response = post('/hash', 'password')
                count.value = count.value + 1
            except Exception as e:
                pass


    def shutdown_server(token):
        try:
            shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
            if shutdown.status_code == requests.codes.ok:
                token.value = 1
        except Exception as e:
            assert False, 'Shutdown raised exception. {}'.format(e)


    token = Value('i', 0)
    count = Value('i', 0)
    processes = 10
    # Each Process sends two POST /hash requests. Shutdown is sent a mid-point.
    # 'expected' number of POST /hash requests will be equal to number of Processes / 2.
    expected = processes // 2
    reqs = 0


    while not token.value:
        post_client = Process(target = client_post, args = (token, count))
        post_client.start()
        reqs = reqs +1

        if reqs == processes // 2:
            post_client.join()

            server_shutdown = Process(target = shutdown_server, args = ([token]))
            server_shutdown.start()
            server_shutdown.join()

    assert count.value == expected, \
            'In-flight requests processed {}, expected {}'.format(count.value, expected)



def test_shutdown_reject_any_new_requests(start_server_manual, baseurl, get_no_header, post):
    """ When shutdown pending, no additional password requests should be allowed. """

    def post_request():
        try:
            response = post('/hash', 'password')
        except Exception as e:
            pass


    # Queue in-flight password requests.
    num = 40
    for i in range(num):
        req = Process(target = post_request)
        req.start()


    # Send shutdown.
    try:
        shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
        assert shutdown.status_code == requests.codes.ok, 'Error, shutdown failed.'
    except Exception as e:
        assert False, 'Shutdown raised exception. {}'.format(e)


    # If response to shutdown OK then shutdown is pending.
    if shutdown.status_code == requests.codes.ok:

        stat_response = get_no_header('/stats')
        assert stat_response.status_code != requests.codes.ok, \
                'New request (GET /stats) accepted when shutdown pending.'



def test_shutdown_no_additional_pasword_reqs(start_server_manual, baseurl, get, post):
    """ When shutdown pending, no additional password requests should be allowed. """

    def post_request():
        try:
            response = post('/hash', 'password')
        except requests.ConnectionError:
            pass


    # Queue in-flight password requests.
    num = 40
    for i in range(num):
        req = Process(target = post_request)
        req.start()


    # Send shutdown.
    try:
        shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
        assert shutdown.status_code == requests.codes.ok, 'Error, shutdown failed.'
    except Exception as e:
        assert False, 'Shutdown raised exception. {}'.format(e)


    # If response to shutdown OK then shutdown is pending.
    if shutdown.status_code == requests.codes.ok:

        get_response = post('/hash', 'shouldfail')
        assert get_response.status_code != requests.codes.ok, \
                'Password request accepted when shutdown pending.'
