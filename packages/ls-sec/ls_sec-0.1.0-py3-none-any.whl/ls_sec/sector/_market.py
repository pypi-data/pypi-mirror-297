from typing import Literal

_PATH = "/indtp/market-data"


def historical_ohlcv_iter(self, upcode: str):
    """업종기간별추이: t1514"""
    block = {
        "upcode": upcode,
        "gubun1": " ",
        "gubun2": "1",
        "cts_date": " ",
        "cnt": 900,
        "rate_gbn": "1",
    }
    return self._iter(_PATH, "t1514", block, "cts_date")


def all_sectors(self):
    """전체업종: t8424"""
    return self.fetch_pandas(_PATH, "t8424", block={"gubun1": ""})


def expected_index(self, upcode: str, gubun: Literal["1", "2"] = "1"):
    """예상지수: t1485"""
    return self.fetch_pandas(_PATH, "t1485", block={"upcode": upcode, "gubun": gubun})


def current_ohlc(self, upcode: str):
    """업종현재가: t1511"""
    return self.fetch_pandas(_PATH, "t1511", block={"upcode": upcode})


def current_ohlc_by_sector(self, upcode: str, gubun: Literal["1", "2", "3"]):
    """업종별종목시세: t1516"""
    return self.fetch_pandas(
        _PATH, "t1516", block={"upcode": upcode, "gubun": gubun, "shcode": ""}
    )
