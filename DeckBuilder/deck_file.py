from libs.client_file import client_class

class deck_class:
    deck_list = []
    client = client_class()
    def __init__(self, name):
        self.deck_name = name

    def get_deck_length(self):
        return len(self.deck_list)
    
    def get_deck_list(self):
        return self.deck_list
    
    def add_card(self, card):
        if self.client.check_card(card):
            self.deck_list.append(card)
            return True
        else:
            return False
        
    def get_type(self, card):
        return self.client.get_card_type(card)
    
    def in_deck(self, card):
        if card in self.deck_list:
            return True
        else:
            return False
        
    def check_card(self, card):
        return self.client.check_card(card)
    
    def count_card(self, card):
        count = 0
        for item in self.deck_list:
            if item == card:
                count += 1
        return count

    def delete_card(self, card):
        if card in self.deck_list:
            self.deck_list.remove(card)