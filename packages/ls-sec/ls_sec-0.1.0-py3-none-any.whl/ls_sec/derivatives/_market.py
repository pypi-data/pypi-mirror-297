from typing import List, Literal

_PATH = "/futureoption/market-data"


def current_ohlcv(self, focode: str):
    """선물/옵션현재가(시세)조회: t2101"""
    return self.fetch_pandas(_PATH, "t2101", block={"focode": focode})


def current_orderbook(self, shcode: str):
    """선물/옵션현재가호가조회: t2105"""
    return self.fetch_pandas(_PATH, "t2105", block={"shcode": shcode})


def current_memo(self, code: str, conds: List):
    """선물/옵션현재가시세메모: t2106"""
    raise NotImplementedError
    return self.fetch_pandas(_PATH, "t2106", block={"code": code, "nrec": ""})


def trade_iter(
    self, focode: str, stime: str = "0900", etime: str = "1600", *, cvolume=0
):
    """선물옵션시간대별체결조회: t2201"""
    block = {
        "focode": focode,
        "cvolume": cvolume,
        "stime": stime,
        "etime": etime,
        "cts_time": "",
    }
    return self._tick_iter(_PATH, "t2201", block)


def get_historical_ohlcv(self):
    """기간별주가: t2203"""


def get_trade_single(self):
    """선물옵션시간대별체결조회(단일출력용): t2210"""


def options_board(self, expiry: str = "", gubun: Literal["", "M", "G"] = ""):
    """옵션전광판: t2301"""
    return self.fetch_pandas(_PATH, "t2301", block={"yyyymm": expiry, "gubun": gubun})


def order_balance(self):
    """선물옵션호가잔량비율챠트: t2405"""
    raise NotImplementedError
    # return self.fetch_pandas(_PATH, "t2405", block={"yyyymm": expiry, "gubun": gubun})


def open_interest(self, focode: str):
    """미결제약정추이: t2421"""
    return self.fetch_pandas(
        _PATH,
        "t2421",
        block={"focode": focode, "bdgubun": "0", "nmin": 0, "tcgubun": "0", "cnt": 20},
    )


def get_eurex_ohlcv(self):
    """EUREXKOSPI200옵션선물현재가(시세)조회: t2830"""


def get_eurex_orderbook(self):
    """EUREXKOSPI200옵션선물호가조회: t2831"""


def get_eurex_trade(self):
    """EUREX야간옵션선물시간대별체결조회: t2832"""


def get_eurex_historical(self):
    """EUREX야간옵션선물기간별추이: t2833"""


def get_eurex_board(self):
    """EUREX옵션선물시세전광판: t2835"""


def stock_futures_master(self):
    """주식선물마스터조회(API용): t8401"""
    return self.fetch_pandas(_PATH, "t8401", block={"dummy": ""})


def stock_futures_current(self, focode):
    """주식선물현재가조회(API용): t8402"""
    return self.fetch_pandas(_PATH, "t8402", block={"focode": focode})


def stock_futures_orderbook(self, focode):
    """주식선물호가조회(API용): t8403"""
    return self.fetch_pandas(_PATH, "t8403", block={"focode": focode})


def stock_futures_trade_iter(
    self, focode, stime: str = "0900", etime: str = "1600", *, cvolume=0
):
    """주식선물시간대별체결조회(API용): t8404"""
    block = {
        "focode": focode,
        "cvolume": cvolume,
        "stime": stime,
        "etime": etime,
        "cts_time": "",
    }
    return self._tick_iter(_PATH, "t8404", block)


def stock_futures_historical_ohlcv(self):
    """주식선물기간별주가(API용): t8405"""


def stock_futures_tick_historical(self, focode: str):
    """주식선물틱분별체결조회(API용): t8406"""
    block = {"focode": focode, "cgubun": "T", "bgubun": 0, "cnt": 20}
    return self.fetch_pandas(_PATH, "t8406", block=block)


def product_master(self):
    """상품선물마스터조회(API용): t8426"""
    return self.fetch_pandas(_PATH, "t8426", block={"dummy": " "})


def historical_ohlcv(
    self,
    focode: str,
    fo_gbn: Literal["F", "O"],
    year,
    month,
    cp_gbn: Literal["2", "3"] = "2",
    actprice: float = 0.00,
):
    """과거데이터시간대별조회: t8427"""
    block = {
        "fo_gbn": fo_gbn,
        "yyyy": year,
        "mm": month,
        "cp_gbn": cp_gbn,
        "actprice": actprice,
        "focode": focode,
        "dt_gbn": "M",
        "min_term": "",
        "date": "",
        "time": "",
    }
    return self.fetch_pandas(_PATH, "t8427", block=block)


def index_futures_master(self, gubun: Literal["", "V", "S"] = ""):
    """지수선물마스터조회API용: t8432"""
    return self.fetch_pandas(_PATH, "t8432", block={"gubun": gubun})


def index_options_master(self, gubun: Literal["", "V", "S"] = ""):
    """지수옵션마스터조회API용: t8433"""
    return self.fetch_pandas(_PATH, "t8433", block={"gubun": gubun})


def multi_ohlc(self, focodes: List[str]):
    """선물/옵션멀티현재가조회: t8434"""
    return self.fetch_pandas(
        _PATH, "t8434", block={"qrycnt": len(focodes), "focode": "".join(focodes)}
    )


def derivatives_master(self, gubun: Literal["MF", "MO", "WK", "SF"]):
    """파생종목마스터조회API용: t8435"""
    return self.fetch_pandas(_PATH, "t8435", block={"gubun": gubun})


def cme_eurex_master(self):
    """CME/EUREX마스터조회(API용): t8437"""


'''
def index_futures_master(self, gubun: Literal["", "V", "S"] = ""):
    """지수선물마스터조회API용: t9943"""
    return self.fetch_pandas(_PATH, "t9943", block={"gubun": gubun})

def index_options_master(self):
    """지수옵션마스터조회API용: t9944"""
    return self.fetch_pandas(_PATH, "t9944", block={"dummy": ""})
'''
