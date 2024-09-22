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

        self.boardMarketIndicesList = [
            "Nifty 50", "Nifty Next 50", "Nifty 100", "Nifty 200", "Nifty Total Market",
            "Nifty 500", "Nifty 500 Multicap 50 25 25", "Nifty Midcap 150", "Nifty Midcap 50",
            "Nifty Midcap Select", "Nifty Midcap 100", "Nifty Smallcap 250",
            "Nifty Smallcap 50", "Nifty Smallcap 100", "Nifty Microcap 250", "Nifty Largemidcap 250",
            "Nifty Midsmallcap 400"
        ]
        self.sectorIndicesList = [
            "Nifty Auto Index", "Nifty Bank Index", "Nifty Financial Services Index", "Nifty Financial Services 25/50 Index",
            "Nifty Financial Services Ex-Bank index", "Nifty FMCG Index", "Nifty Healthcare Index", "Nifty IT Index",
            "Nifty Media Index", "Nifty Metal Index", "Nifty Pharma Index", "Nifty Private Bank Index", "Nifty PSU Bank Index",
            "Nifty Realty Index", "Nifty Consumer Durables Index", "Nifty Oil and Gas Index", "Nifty MidSmall Financial Services Index",
            "Nifty MidSmall Healthcare Index", "Nifty MidSmall IT & Telecom Index"
        ]
        self.initialRequest()

    def equityUrlParser(self, url: str):
        parsed_url = url.replace("&", "%26")
        return parsed_url

    def setCookies(self, response: requests.Response):
        self.cookies.update(response.cookies.get_dict())

    def initialRequest(self):
        response = requests.request("GET", self.baseURL, headers={
                                    "User-Agent": self.userAgent})
        self.setCookies(response=response)

    def getEquityQuote(self, symbol: str):
        url = f"https://www.nseindia.com/api/quote-equity?symbol={
            symbol.upper()}"
        response = requests.request("GET", self.equityUrlParser(url), headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        self.setCookies(response=response)
        self.equityQuotes: dict = response.json()
        # print(self.equityQuotes)
        return self.equityQuotes

    def getEquityQuoteItem(self, itemName: Literal['info', 'metadata', 'securityInfo', 'sddDetails', 'priceInfo', 'industryInfo', 'preOpenMarket']):
        if self.equityQuotes:
            return self.equityQuotes[itemName]
        else:
            raise Exception("equityQuotes is empty")

    def getFinalEquityQuote(self):
        stockInfo: dict = self.getEquityQuoteItem("info")
        stockIndustryInfo: dict = self.getEquityQuoteItem("industryInfo")
        stockMetaData: dict = self.getEquityQuoteItem("metadata")
        stockSecurityInfo: dict = self.getEquityQuoteItem("securityInfo")

        timezone_info = timezone.utc
        try:
            listingData = datetime.strptime(stockMetaData.get(
                "listingDate"), '%d-%b-%Y').replace(tzinfo=timezone_info)
        except Exception as error:
            listingData = None
        try:
            lastUpdateTime = datetime.strptime(
                stockMetaData.get("lastUpdateTime"), '%d-%b-%Y %H:%M:%S')
        except Exception as error:
            lastUpdateTime = None

        return {"macro": str(stockIndustryInfo.get("macro")).strip(),
                "sector": str(stockIndustryInfo.get("sector")).strip(),
                "industry": str(stockIndustryInfo.get("industry")).strip(),
                "basicIndustry": str(stockIndustryInfo.get("basicIndustry")).strip(),
                "companyName": str(stockInfo.get("companyName")).strip(),
                "isin": stockMetaData.get("isin"),
                "symbol": stockMetaData.get("symbol"),
                "series": stockMetaData.get("series"),
                "status": stockMetaData.get("status"),
                "listingDate": listingData,
                "pdSectorInd": str(stockMetaData.get("pdSectorInd")).strip(),
                "lastUpdateTime": lastUpdateTime,
                "faceValue": stockSecurityInfo.get("faceValue"),
                "issuedSize": stockSecurityInfo.get("issuedSize")}

    def getEquityList(self) -> list[EquityInfo]:
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        response = requests.request("GET", url, headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        newList = []

        df = pd.read_csv(io.StringIO(response.text))
        df = df.replace({np.nan: None})
        for each in df.to_dict("records"):
            eachEquityData = EquityInfo(symbol=each["SYMBOL"], nameOfCompany=each["NAME OF COMPANY"], series=each[" SERIES"],
                                        dateOfListing=each[" DATE OF LISTING"], paidUpValue=each[" PAID UP VALUE"], 
                                        marketLot=each[" MARKET LOT"], isinNumber=each[" ISIN NUMBER"], 
                                        faceValue=each[" FACE VALUE"])
            newList.append(eachEquityData)
        return newList

    def getBoardMarketIndicesList(self, indicesName: Literal[
        "Nifty 50", "Nifty Next 50", "Nifty 100", "Nifty 200", "Nifty Total Market",
        "Nifty 500", "Nifty 500 Multicap 50 25 25", "Nifty Midcap 150", "Nifty Midcap 50",
        "Nifty Midcap Select", "Nifty Midcap 100", "Nifty Smallcap 250",
        "Nifty Smallcap 50", "Nifty Smallcap 100", "Nifty Microcap 250", "Nifty Largemidcap 250",
        "Nifty Midsmallcap 400"
    ]):
        url_dict = {
            "Nifty 50": "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv",
            "Nifty Next 50": "https://nsearchives.nseindia.com/content/indices/ind_niftynext50list.csv",
            "Nifty 100": "https://nsearchives.nseindia.com/content/indices/ind_nifty100list.csv",
            "Nifty 200": "https://nsearchives.nseindia.com/content/indices/ind_nifty200list.csv",
            "Nifty Total Market": "https://nsearchives.nseindia.com/content/indices/ind_niftytotalmarket_list.csv",
            "Nifty 500": "https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv",
            "Nifty 500 Multicap 50 25 25": "https://nsearchives.nseindia.com/content/indices/ind_nifty500Multicap502525_list.csv",
            "Nifty Midcap 150": "https://nsearchives.nseindia.com/content/indices/ind_niftymidcap150list.csv",
            "Nifty Midcap 50": "https://nsearchives.nseindia.com/content/indices/ind_niftymidcap50list.csv",
            "Nifty Midcap Select": "https://nsearchives.nseindia.com/content/indices/ind_niftymidcapselect_list.csv",
            "Nifty Midcap 100": "https://nsearchives.nseindia.com/content/indices/ind_niftymidcap100list.csv",
            "Nifty Smallcap 250": "https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap250list.csv",
            "Nifty Smallcap 50": "https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap50list.csv",
            "Nifty Smallcap 100": "https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap100list.csv",
            "Nifty Microcap 250": "https://nsearchives.nseindia.com/content/indices/ind_niftymicrocap250_list.csv",
            "Nifty Largemidcap 250": "https://nsearchives.nseindia.com/content/indices/ind_niftylargemidcap250list.csv",
            "Nifty Midsmallcap 400": "https://nsearchives.nseindia.com/content/indices/ind_niftymidsmallcap400list.csv"
        }

        url = url_dict[indicesName]
        response = requests.request("GET", url, headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        return pd.read_csv(io.StringIO(response.text)).to_dict("records")

    def getSectoralIndicesList(self, indicesName: Literal[
        "Nifty Auto Index", "Nifty Bank Index", "Nifty Financial Services Index", "Nifty Financial Services 25/50 Index",
        "Nifty Financial Services Ex-Bank index", "Nifty FMCG Index", "Nifty Healthcare Index", "Nifty IT Index",
        "Nifty Media Index", "Nifty Metal Index", "Nifty Pharma Index", "Nifty Private Bank Index", "Nifty PSU Bank Index",
        "Nifty Realty Index", "Nifty Consumer Durables Index", "Nifty Oil and Gas Index", "Nifty MidSmall Financial Services Index",
        "Nifty MidSmall Healthcare Index", "Nifty MidSmall IT & Telecom Index"
    ]):
        url = {
            "Nifty Auto Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyautolist.csv",
            "Nifty Bank Index": "https://www.niftyindices.com/IndexConstituent/ind_niftybanklist.csv",
            "Nifty Financial Services Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyfinancelist.csv",
            "Nifty Financial Services 25/50 Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyfinancialservices25-50list.csv",
            "Nifty Financial Services Ex-Bank index": "https://www.niftyindices.com/IndexConstituent/ind_niftyfinancialservicesexbank_list.csv",
            "Nifty FMCG Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyfmcglist.csv",
            "Nifty Healthcare Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyhealthcarelist.csv",
            "Nifty IT Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyitlist.csv",
            "Nifty Media Index": "https://www.niftyindices.com/IndexConstituent/ind_niftymedialist.csv",
            "Nifty Metal Index": "https://www.niftyindices.com/IndexConstituent/ind_niftymetallist.csv",
            "Nifty Pharma Index": "https://www.niftyindices.com/IndexConstituent/ind_niftypharmalist.csv",
            "Nifty Private Bank Index": "https://www.niftyindices.com/IndexConstituent/ind_nifty_privatebanklist.csv",
            "Nifty PSU Bank Index": "https://www.niftyindices.com/IndexConstituent/ind_niftypsubanklist.csv",
            "Nifty Realty Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyrealtylist.csv",
            "Nifty Consumer Durables Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyconsumerdurableslist.csv",
            "Nifty Oil and Gas Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyoilgaslist.csv",
            "Nifty MidSmall Financial Services Index": "https://www.niftyindices.com/IndexConstituent/ind_niftymidsmallfinancailservice_list.csv",
            "Nifty MidSmall Healthcare Index": "https://www.niftyindices.com/IndexConstituent/ind_niftymidsmallhealthcare_list.csv",
            "Nifty MidSmall IT & Telecom Index": "https://www.niftyindices.com/IndexConstituent/ind_niftymidsmallitAndtelecom_list.csv",
        }[indicesName]
        response = requests.request("GET", url, headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        return pd.read_csv(io.StringIO(response.text)).to_dict("records")

    def securitiesInEquitySegment(self):
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        response = requests.request(
            "GET", url, headers={"User-Agent": self.userAgent}, cookies=self.cookies)
        return pd.read_csv(io.StringIO(response.text)).to_dict("records")
