

class EquityInfo:
    def __init__(self, symbol: str, nameOfCompany: str, series: str,
                 dateOfListing: str, isinNumber: str, faceValue: int,
                 marketLot: int, paidUpValue: int) -> None:
        self.symbol = symbol
        self.nameOfCompany = nameOfCompany
        self.series = series
        self.dateOfListing = dateOfListing
        self.isinNumber = isinNumber
        self.faceValue = faceValue
        self.marketLot = marketLot
        self.paidUpValue = paidUpValue
