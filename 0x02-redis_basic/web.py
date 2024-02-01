#!/usr/bin/env python3
'''
    In this tasks, we will implement a get_page
    function (prototype: def get_page(url: str) -> str:).
    The core of the function is very simple. It uses the
    requests module to obtain the HTML content of a particular
    URL and returns it.

    Start in a new file named web.py and do not reuse the code
    written in exercise.py.

    Inside get_page track how many times a particular URL was
    accessed in the key "count:{url}" and cache the result with
    an expiration time of 10 seconds.

    Tip: Use http://slowwly.robertomurray.co.uk to simulate a
    slow response and test your caching.

    Bonus: implement this use case with decorators.
'''
from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator for counting """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = redis_.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        redis_.incr(count_key)
        redis_.set(cached_key, html)
        redis_.expire(cached_key, 10)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a  URL """
    req = requests.get(url)
    return req.text
