from ls_sec.core import LSAPI


class LSSector(LSAPI):
    def __init__(self, key: str, secret: str):
        super().__init__(key, secret)

    # market
    from ls_sec.sector._market import (
        all_sectors,
        current_ohlc,
        current_ohlc_by_sector,
        expected_index,
        historical_ohlcv_iter,
    )
