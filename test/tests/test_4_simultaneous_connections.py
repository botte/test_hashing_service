""" Verify POST /shutdown.

    - Shutdown return code 200 OK
    - Shutdown allows in-flight passwords to complete
    - When shutdown pending, no additional password requests should be allowed.
    - Server processes multiple simultaneous connections
"""

import requests
from multiprocessing import Process, Array, Value
import time



def test_simultaneous_connections(baseurl, post, get, get_no_header):
    """ Verify all in-flight POST /hash requests complete. """


    def client(shutdown, count, not_processed, exceptions):

        if not shutdown.value:
            try:
                post_response = post('/hash', 'password'+ str(count.value))

                if post_response.status_code == requests.codes.ok:
                    count.value = count.value + 1

                if post_response.status_code == 503:
                    not_processed.value = not_processed.value + 1

            except Exception as e:
                exceptions.value = 1


    def stat_client(shutdown, exceptions):
        if not shutdown.value:
            try:
                stats = get_no_header('/stats')
            except Exception as e:
                exceptions.value = 2


    def shutdown_server(shutdown, exceptions):
        try:
            shutdown = requests.post(baseurl + '/hash', data = 'shutdown')
            if shutdown.status_code == requests.codes.ok:
                shutdown.value = 1
        except Exception as e:
            exceptions.value = 3


    shutdown = Value('i', 0)
    count = Value('i', 0)
    exceptions = Value('i', 0)
    not_processed = Value('i', 0)
    processes = 10
    reqs = 0

    while reqs < processes:

        reqs = reqs +1

        if reqs == processes // 2:
            server_shutdown = Process(target = shutdown_server, args = (shutdown, exceptions))
            server_shutdown.start()

        req_client = Process(target = client, args = (shutdown, count, not_processed, exceptions))
        req_stat = Process(target = stat_client, args = (shutdown, exceptions))

        req_client.start()
        req_stat.start()

        if reqs == processes:
            req_client.join()


    # Each Process sends one POST /hash requests.
    # Shutdown is sent a mid-point.
    # Requests received when shutdown pending are not processed.
    # Requests after server is shutdown are not counted.
    # 'expected' number of POST /hash requests will be equal to
    #     number of Processes - not processed requests.

    exception = ''
    if exceptions.value == 1:
        exception = 'POST /hash'
    if exceptions.value == 2:
        exception = 'GET /stats'
    if exceptions.value == 3:
        exception = 'POST /shutdown'

    assert exceptions.value == 0, '{} caused an exception'.format(exception)

    expected = processes - not_processed.value
    assert count.value == expected, \
            'In-flight requests processed {}, expected {}'.format(count.value, expected)

    time.sleep(processes)
