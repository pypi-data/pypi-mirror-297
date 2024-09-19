from ls_sec.core import LSAPI


class LSStock(LSAPI):
    def __init__(self, key: str, secret: str):
        super().__init__(key, secret)

    from ls_sec.stock._etc import stock_list
    from ls_sec.stock._market import current_orderbook, stock_master, tick_iter
