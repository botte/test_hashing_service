""" Verify GET /stats TotalRequests.

    - GET to /stats should return total hash requests since the server started.
"""

import requests
from multiprocessing import Process
import json



def test_stats_total_hash(post, get, get_no_header):
    """ GET to /stats should return total hash requests since the server started. """


    # Verify post calls counted and get calls not counted.
    def client_post():
        try:
            post_response = post('/hash', 'password')
            get('/hash/' + str(post_response.text))
        except Exception as e:
            pass


    # Verify stat calls not counted.
    def client_stat():
        try:
            get_no_header('/stats')
        except Exception:
            pass

    processes = 100
    i = 0
    while i < processes:
        i = i + 1

        post_client = Process(target = client_post)
        post_client.start()

        if i == processes:
            post_client.join()

        stat_client = Process(target = client_stat)
        stat_client.start()


    stat_response = get_no_header('/stats')
    as_json = (stat_response.json())
    cnt_reported = as_json['TotalRequests']

    assert str(processes) == str(cnt_reported), \
            'Expected requests: {}, reported requests: {}'.format(processes, cnt_reported)
