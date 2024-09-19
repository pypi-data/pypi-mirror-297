from typing import Literal

_PATH = "/stock/etc"

"""
예탁담보융자가능종목현황조회	CLNAQ00100	1
신규상장종목조회	t1403	1
증거금율별종목조회	t1411	1
종목별잔량/사전공시	t1638	1
신용거래동향	t1921	1
종목별신용정보	t1926	1
공매도일별추이	t1927	1
종목별대차거래일간추이	t1941	1
주식종목조회	t8430	2
주식종목조회 API용	t8436	2
"""

"""예탁담보융자가능종목현황조회: CLNAQ00100"""
"""신규상장종목조회: t1403"""
"""증거금율별종목조회: t1411"""
"""종목별잔량/사전공시: t1638"""
"""신용거래동향: t1921"""
"""종목별신용정보: t1926"""
"""공매도일별추이: t1927"""
"""종목별대차거래일간추이: t1941"""


'''
def stock_list(self, gubun: Literal["0", "1", "2"] = "0"):
    """주식종목조회: t8430"""
    return self.fetch_pandas(_PATH, "t8430", block={"gubun": gubun})
'''


def stock_list(self, gubun: Literal["0", "1", "2"] = "0"):
    """주식종목조회 API용: t8436"""
    return self.fetch_pandas(_PATH, "t8436", block={"gubun": gubun})
