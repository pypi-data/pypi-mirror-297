from datetime import datetime, timezone
from typing import Literal
import requests
import io
import pandas as pd
import numpy as np

from .schema import EquityInfo


class NSEClient:
    def __init__(self):
        self.baseURL = "https://www.nseindia.com/"
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.cookies = {}
        self.equityQuotes = {}
        self.initialRequest()

    def setCookies(self, response: requests.Response):
        self.cookies.update(response.cookies.get_dict())

    def initialRequest(self):
        response = requests.request("GET", self.baseURL, headers={
                                    "User-Agent": self.userAgent})
        if response.ok:
            self.setCookies(response=response)
        else:
            print(response.text)

    def getEquityList(self) -> list[EquityInfo]:
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        response = requests.request("GET", url, headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        newList = []
        if response.ok:
            df = pd.read_csv(io.StringIO(response.text))
            df = df.replace({np.nan: None})
            for each in df.to_dict("records"):
                eachEquityData = EquityInfo(symbol=each["SYMBOL"], nameOfCompany=each["NAME OF COMPANY"], series=each[" SERIES"],
                                            dateOfListing=each[" DATE OF LISTING"], paidUpValue=each[" PAID UP VALUE"],
                                            marketLot=each[" MARKET LOT"], isinNumber=each[" ISIN NUMBER"],
                                            faceValue=each[" FACE VALUE"])
                newList.append(eachEquityData)
            return newList
        else:
            print(response.text)
            return None
