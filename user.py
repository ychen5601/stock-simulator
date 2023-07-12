class User:

    """
    user_id: String of user's discord ID
    bal: float of user's cash balance
    stocks: dictionary with key: stock code to value: amount of stocks held
    """

    def __init__(self, user_id, bal, stocks):
        self.user_id = user_id
        self.bal = bal
        self.stocks = stocks
