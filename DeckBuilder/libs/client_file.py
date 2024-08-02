import requests
class client_class():
    URL = "https://api.scryfall.com/cards/"

    def __init__(self):
        pass

    def check_card(self, card):
        result = requests.get(f"{self.URL}named?exact={card}").json()
        if result ["object"] == "error":
            print("The requested card does not exist, check input")
            return False
        elif result ["object"] == "card":
            return True
        else:
            print("Unknown Error")
            return False
        
    def get_card_type(self, card):
        result = requests.get(f"{self.URL}named?exact={card}").json()
        return result ["type_line"]