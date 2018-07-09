""" Verify POST /hash 'password', GET /hash 'job_id.'

    When launched, the application should wait for http connections.
        - It should answer on PORT specified in the PORT environment variable.
        - It should support endpoints
            - POST to /hash should accept a password
            - POST to /hash should return a job identifier immediately
            - The hashing algorithm should be SHA512

            - GET to /hash should accept a job identifier
            - GET to hash should return the base64 encoded password hash
"""

import requests
import time
from test.lib import lib



def test_post_hash_basic(post):
        """ When launched, the application should
                - wait for http connections and
                - answer on the PORT specified in the PORT environment variable.
            POST to /hash should accept a password and return job identifier.
        """

        post_response = post('/hash', 'password')
        assert post_response.status_code == requests.codes.ok, \
                'POST /hash failed {}'.format(post_response.status_code)
        assert post_response.text != '', 'POST did not return job id'



def test_post_hash_immediate_return(post):
        """ POST to /hash should return a job identifier immediately. """
        # This could also be verified using a timeout on the 'requests' POST request.
        # Assumption being return of job-id, in actuality, takes 5 seconds; 1.0 wait should be enough.
        max_time = 4.0
        start = time.time()

        try:
            post_response = post('/hash', 'password')
        except ReadTimeout as e: 
            assert False, 'POST /hash did not return immediately.'

        duration = round(time.time() - start, 2)
        assert duration <= max_time, 'POST /hash did not return immediately, took {}'.format(duration)



def test_get_password_basic(post, get):
        """ GET to /hash should accept a job identifier. """

        post_response = post('/hash', 'password')
        
        get_response = get('/hash/' + str(post_response.text))
        assert get_response.status_code == requests.codes.ok, \
                'GET /hash failed {}'.format(get_response.status_code)
        assert get_response.text != '', 'POST did not return job id'



def test_post_hash_timing(post, get):
    """ POST to /hash should wait 5 seconds and compute the password hash. """

    for i in range(10):
        start = time.time()
        post_response = post('/hash', 'password')
        get_response = get('/hash/' + str(post_response.text))
        res_time = round(time.time() - start, 2)
        assert res_time >= 5.00, 'Password hash computed {}, less than 5 seconds.'.format(res_time)



def test_post_hash_sha512(post, get, random_passwords, generate_sha512):
    """ The hashing algorithm should be SHA512. """

    for password in random_passwords:
        post_response = post('/hash', password)

        get_response = get('/hash/' + str(post_response.text))
        gen_data = generate_sha512(password)
        assert gen_data == get_response.text, 'Password was  not sha512'



def test_post_hash_base_64(post, get, random_passwords):
    """ GET to hash should return the base64 encoded password hash. """

    for password in random_passwords:
        post_response = post('/hash', password)

        get_response = get('/hash/' + str(post_response.text))
        assert lib.is_base64(get_response.text), 'Password was not base64.'
        assert get_response.status_code == requests.codes.ok, \
                'Service did not return hash.'
