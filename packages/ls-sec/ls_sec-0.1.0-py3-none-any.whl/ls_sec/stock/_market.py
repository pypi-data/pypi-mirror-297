from typing import Literal

_PATH = "/stock/market-data"


def current_orderbook(self, shcode):
    """주식현재가호가조회: t1101"""
    return self.fetch_pandas(_PATH, "t1101", block={"shcode": shcode})


def current_ohlcv(self, shcode):
    """주식현재가(시세)조회: t1102"""
    return self.fetch_pandas(_PATH, "t1102", block={"shcode": shcode})


def current_memo(self, shcode):
    """주식현재가시세메모: t1104"""
    raise NotImplementedError
    return self.fetch_pandas(_PATH, "t1104", block={"shcode": shcode})


"""주식피봇/디마크조회: t1105"""


def after_hours_volume(
    self,
    shcode: str,
):
    """시간외체결량: t1109"""
    return self.fetch_pandas(
        _PATH, "t1109", block={"shcode": shcode, "dan_chetime": "", "idx": 0}
    )


def tick_iter(
    self,
    shcode: str,
    *,
    starttime="",
    endtime="",
    cvolume=0,
):
    """주식시간대별체결조회: t1301"""
    block = {
        "shcode": shcode,
        "cvolume": cvolume,
        "starttime": starttime,
        "endtime": endtime,
        "cts_time": "",
    }
    return self._iter(_PATH, "t1301", block, "cts_time")


"""주식분별주가조회: t1302"""
"""기간별주가: t1305"""
"""주식시간대별체결조회챠트: t1308"""
"""주식당일전일분틱조회: t1310"""
"""관리/불성실/투자유의조회: t1404"""
"""투자경고/매매정지/정리매매조회: t1405"""
"""초저유동성조회: t1410"""
"""상/하한: t1422"""
"""상/하한가직전: t1427"""
"""신고/신저가: t1442"""
"""가격대별매매비중조회: t1449"""
"""시간대별호가잔량추이: t1471"""
"""체결강도추이: t1475"""
"""시간별예상체결가: t1486"""
"""예상체결가등락율상위조회: t1488"""
"""API용주식멀티현재가조회: t8407"""


def stock_master(self, gubun: Literal["1", "2"] = "1"):
    """주식마스터조회API: t9945"""
    return self.fetch_pandas(_PATH, "t9945", block={"gubun": gubun})
