"""aiohttp example.

Simple web app that checks numbers for primality.

To run this example run workers first:

    python3 -m atq --host localhost --port 12345
    python3 -m atq --host localhost --port 12346

and then run

    python3 examples/web.py

and

    curl http://localhost:8080/17

"""
import json
import sys
sys.path.append('../atq')  # Required to run examples without installation.
import atq
from aiohttp import web

q = atq.Q([
    ("localhost", 12345),
    ('localhost', 12346),
])


def check_prime(number):
    """Checks whether number is prime."""
    return all(number % i for i in range(2, number))


async def is_prime_handler(request):
    """Handles GET requests."""
    number = int(request.match_info['number'])
    is_prime = await q.q(check_prime, number)
    return web.Response(text=json.dumps({
        'number': number,
        'prime': is_prime
    }))


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/{number}', is_prime_handler)
    web.run_app(app)
