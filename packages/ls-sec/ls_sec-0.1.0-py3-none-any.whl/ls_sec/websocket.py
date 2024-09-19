import json
import socket
import time
from enum import Enum
from typing import Optional, Union

import websockets

from .core import LSAPI


class TRType(Enum):
    RegisterAccount = "1"
    UnregisterAccount = "2"
    RegisterEvent = "3"
    UnregisterEvent = "4"


class TRCode(Enum):
    업종별투자자별매매현황 = "BM_"

    ETF호가잔량 = "B7_"
    KOSPI시간외단일가호가잔량 = "DH1"
    KOSDAQ시간외단일가호가잔량 = "DHA"
    KOSDAQ시간외단일가체결 = "DK3"
    KOSPI시간외단일가체결 = "DS3"
    시간외단일가VI발동해제 = "DVI"
    KOSPI호가잔량 = "H1_"
    KOSPI장전시간외호가잔량 = "H2_"
    KOSDAQ호가잔량 = "HA_"
    KOSDAQ장전시간외호가잔량 = "HB_"
    코스피ETF종목실시간NAV = "I5_"
    지수 = "IJ_"
    KOSPI거래원 = "K1_"
    KOSDAQ체결 = "K3_"
    KOSDAQ프로그램매매종목별 = "KH_"
    KOSDAQ프로그램매매전체집계 = "KM_"
    KOSDAQ우선호가 = "KS_"
    KOSDAQ거래원 = "OK_"
    KOSPI프로그램매매종목별 = "PH_"
    KOSPI프로그램매매전체집계 = "PM_"
    KOSPI우선호가 = "S2_"
    KOSPI체결 = "S3_"
    KOSPI기세 = "S4_"
    상하한가근접진입 = "SHC"
    상하한가근접이탈 = "SHD"
    상하한가진입 = "SHI"
    상하한가이탈 = "SHO"
    VI발동해제 = "VI_"
    예상지수 = "YJ_"
    KOSDAQ예상체결 = "YK3"
    KOSPI예상체결 = "YS3"
    뉴ELW투자지표민감도 = "ESN"
    ELW장전시간외호가잔량 = "h2_"
    ELW호가잔량 = "h3_"
    ELW거래원 = "k1_"
    ELW우선호가 = "s2_"
    ELW체결 = "s3_"
    ELW기세 = "s4_"
    ELW예상체결 = "Ys3"
    API사용자조건검색실시간 = "AFR"

    KOSPI200선물체결 = "FC0"
    KOSPI200선물실시간상하한가 = "FD0"
    KOSPI200선물호가 = "FH0"
    KOSPI200선물가격제한폭확대 = "FX0"
    EUREX연계KP200지수옵션선물체결 = "EC0"
    EUREX연계KP200지수옵션선물호가 = "EH0"
    주식선물체결 = "JC0"
    주식선물실시간상하한가 = "JD0"
    주식선물호가 = "JH0"
    주식선물가격제한폭확대 = "JX0"
    상품선물실시간상하한가 = "CD0"
    KOSPI200옵션체결 = "OC0"
    KOSPI200옵션실시간상하한가 = "OD0"
    KOSPI200옵션호가 = "OH0"
    KOSPI200옵션민감도 = "OMG"
    KOSPI200옵션가격제한폭확대 = "OX0"
    상품선물예상체결 = "YC3"
    지수선물예상체결 = "YFC"
    주식선물예상체결 = "YJC"
    지수옵션예상체결 = "YOC"

    해외선물_체결 = "OVC"
    해외선물_호가 = "OVH"
    해외옵션_체결 = "WOC"
    해외옵션_호가 = "WOH"

    장운영정보 = "JIF"
    실시간뉴스제목패킷 = "NWS"

    시간대별투자자매매추이 = "BMT"
    현물정보USD실시간 = "CUR"
    US지수 = "MK2"


class TRAccountCode(Enum):
    주식주문접수 = "SC0"
    주식주문체결 = "SC1"
    주식주문정정 = "SC2"
    주식주문취소 = "SC3"
    주식주문거부 = "SC4"

    선물접수 = "O01"
    선물주문체결 = "C01"
    선물주문정정취소 = "H01"
    EUX접수 = "EU0"
    EUX체결 = "EU1"
    EUX확인 = "EU2"

    해외선물_주문접수 = "TC1"
    해외선물_주문응답 = "TC2"
    해외선물_주문체결 = "TC3"


class LSWebsocketClient:
    def __init__(self, key: str, secret: str, retries=10, backoff_factor=0.1):
        self.api = LSAPI(key, secret)
        self.url = "wss://openapi.ls-sec.co.kr:9443/websocket"
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def __aenter__(self):
        for attempt in range(self.retries):
            try:
                self.connection = await websockets.connect(
                    self.url, ping_timeout=60 * 10
                )
            except socket.gaierror as e:
                if attempt < self.retries - 1:
                    print(f"{e} attempt: {attempt}")
                    time.sleep(self.backoff_factor * (2**attempt))
                else:
                    raise
            else:
                return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    async def request(
        self, tr_type, tr_cd: Union[TRCode, TRAccountCode], tr_key: Optional[str] = None
    ):
        msg = {
            "header": {"token": self.api.token, "tr_type": tr_type.value},
            "body": {"tr_cd": tr_cd.value, "tr_key": tr_key or ""},
        }
        msg_str = json.dumps(msg)
        await self.connection.send(msg_str)

    async def subscribe(self, tr_cd: TRCode, tr_key: str):
        tr_type = TRType.RegisterEvent
        await self.request(tr_type, tr_cd, tr_key)

    async def unsubscribe(self, tr_cd: TRCode, tr_key: str):
        tr_type = TRType.UnregisterEvent
        await self.request(tr_type, tr_cd, tr_key)

    async def subscribe_account(self, tr_cd: TRAccountCode):
        tr_type = TRType.RegisterAccount
        await self.request(tr_type, tr_cd)

    async def unsubscribe_account(self, tr_cd: TRAccountCode):
        tr_type = TRType.UnregisterAccount
        await self.request(tr_type, tr_cd)

    async def recv(self):
        return await self.connection.recv()
