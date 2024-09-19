import json
import logging
import time
from typing import Literal

import pandas as pd
import requests

logger = logging.getLogger(__name__)


class LSAPI:
    def __init__(self, key: str, secret: str):
        self.base_url = "https://openapi.ls-sec.co.kr:8080"
        self.session = requests.Session()
        self._key = key
        self._secret = secret

        self._token = None
        self._token_expiry = 0
        self.issue_token()

    def post(
        self,
        path,
        tr_cd: str,
        data=None,
        json=None,
        *,
        headers=None,
        tr_cont: Literal["Y", "N"] = "N",
        tr_cont_key="",
        update_default_header=True,
        content_type="application/json; charset=utf-8",
    ):
        headers = headers or {}
        if update_default_header:
            headers.update(
                {
                    "authorization": f"Bearer {self.token}",
                    "content-type": content_type,
                    "tr_cd": tr_cd,
                    "tr_cont": tr_cont,
                    "tr_cont_key": tr_cont_key,
                }
            )
        url = self.base_url + path
        retries = 5
        backoff_factor = 0.1

        for attempt in range(retries + 1):
            try:
                response = self.session.post(url, data=data, json=json, headers=headers)
            except requests.ConnectionError as e:
                logger.warning(f"Attempt {retries} failed due to {e}")
                time.sleep(backoff_factor * (2**attempt))
            else:
                return response

    def fetch_pandas(
        self,
        path: str,
        tr_cd,
        *,
        body=None,
        block=None,
        tr_cont: Literal["Y", "N"] = "N",
    ):
        body = {}
        if block is not None:
            body[tr_cd + "InBlock"] = block
        response = self.post(path, tr_cd, json.dumps(body), tr_cont=tr_cont)
        data = response.json()

        out_block = tr_cd + "OutBlock"
        out_block1 = out_block + "1"
        out_block2 = out_block + "2"

        def to_frame(cur_data):
            if isinstance(cur_data, dict):
                return pd.Series(cur_data)
            else:
                return pd.DataFrame(cur_data)

        res = [
            to_frame(r)
            for r in (
                data.get(out_block, None),
                data.get(out_block1, None),
                data.get(out_block2, None),
            )
            if r is not None
        ]

        if len(res) == 1:
            return res[0]
        elif len(res) == 0:
            logger.warn(f'{data["rsp_cd"]}: {data["rsp_msg"]}')
            return None
        else:
            return res

    def _iter(self, path, tr_cd, block, key):
        res = self.fetch_pandas(path, tr_cd, block=block)
        if res is None:
            return
        sr, df = res
        yield df
        value = sr.get(key)
        while value != "":
            block[key] = value
            res = self.fetch_pandas(path, tr_cd, block=block, tr_cont="Y")
            if res is None:
                return
            sr, df = res
            yield df

    def issue_token(self):
        path = "/oauth2/token"
        body = {
            "grant_type": "client_credentials",
            "appkey": self._key,
            "appsecretkey": self._secret,
            "scope": "oob",
        }
        res = self.post(
            path,
            None,
            body,
            headers={"content-type": "application/x-www-form-urlencoded"},
            update_default_header=False,
        )
        data = res.json()
        self._token = data["access_token"]
        self._token_expiry = time.time() + data["expires_in"] - 60 * 60

    @property
    def token(self):
        if self._token_expiry < time.time():
            self.issue_token()
        return self._token

    def get_time(self):
        return self.fetch_pandas("/etc/time-search", "t0167", block={"id": ""})
