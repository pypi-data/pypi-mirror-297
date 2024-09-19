import os

import pytest
from dotenv import load_dotenv

from ls_sec.stock import LSStock

SAMSUNG = "005930"


@pytest.fixture(scope="session")
def api():
    load_dotenv()
    KEY = os.environ["LS_KEY"]
    SECRET = os.environ["LS_SECRET"]
    return LSStock(KEY, SECRET)


def test_stocks(api: LSStock):
    # df = api.get_time()
    # df = api.current_orderbook(SAMSUNG)
    # df = api.stock_master()
    for df in api.tick_iter(SAMSUNG):
        breakpoint()
