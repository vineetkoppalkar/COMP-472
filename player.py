class Player:
    name = ""
    token = ""
    number_of_tokens = 0
    is_ai = False

    def __init__(self, name, token, number_of_tokens):
        self.name = name
        self.token = token
        self.number_of_tokens = number_of_tokens
