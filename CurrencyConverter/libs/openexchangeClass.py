import requests

class openexchangeClient:
    URL = 'https://openexchangerates.org/api'

    def __init__(self, appID):
        self.appID = appID

    def latest(self):
        return requests.get(f"{self.URL}/latest.json?app_id={self.appID}").json()
    
    #openexchangerates API returns currencies in terms of USD, convert allows for x to y currency conversion
    def convert(self, amount, fromCurrency, toCurrency):
        rates = self.latest()["rates"]
        toRate = rates[toCurrency]
        usd = toRate / rates[fromCurrency]
        return round((amount * usd), 2)
    
    def get_rates(self):
        return self.latest()["rates"]
        