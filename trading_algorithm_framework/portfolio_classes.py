from stock_classes import *

# Define a class to handle a share in a stock
class Share:
    '''
    Create a new share in a stock that can be added to the users portfolio

    
    '''
    
    def __init__(self, price, volume, date, symbol=None):
        self.price = price
        self.volume = volume
        self.date = date
        self.symbol = symbol
        
# Define a class to handle the stock information in the users portfolio
class Portfolio:
    '''
    Create a new portfolio to purchase shares with

    Values that may be allocated when calling this class:

    - starting_balance = 50 000 (by default)

    Methods:

    - reset_balance : Resets the user balance. Takes one argument.
        - (new_balance) : Set to 50 000 by default.

    - buy : Enters a position. Takes two arguments.
        - share : An instance of the share class for the stock you wish to purchase;
        - is_long : A boolean which tells the portfolio to store the share as a long or short position.

    - sell : Leaves a postion. Takes four arguments.
        - date : The date that the share was purchased;
        - volume : The number of shares that the user wishes to purchase;
        - current_price : The value of the share on the date assigned;
        - 
    '''
    
    # Store all of the portfolio short and long positions
    short_ = []
    long_ = []

    # Define a private attribute to dynamically allocate IDs to shares
    __id = 0
    
    # An initiation function with $50k start money
    def __init__(self, balance=50000):
        self.balance = balance
        
    # A function to reset the user cash
    def reset_balance(self, new_balance=50000): 
        self.balance = new_balance
        
    # A function to add a share to the users portfolio
    def buy(self, share, is_long):
        if is_long:
            self.long_.append(share)
            self.balance -= share.price * share.volume
        else:
            self.short_.append(share)
            
    # A function to sell a position that was entered on a given date
    def sell(self, date, volume, current_price, is_long):
        
        # Get the correct list
        shlo = self.long_ if is_long else self.short_
        
        # Find the desired date value
        for i in range(0, len(shlo)):
            
            # If we find a share with the correct date, sell the desired volume
            if shlo[i].date == date:
                
                # Bound the volume by the maximum available
                if shlo[i].volume > volume: volume = shlo[i].volume
                
                # Now adjust the values accordingly
                shlo[i].volume -= volume
                
                # Adjust the price
                if is_long:
                    self.balance += current_price * volume
                else:
                    self.balance += (shlo[i].price - current_price) * volume
                
                # Delete the share
                shlo.pop(i)
                
                # Return prematurely
                return
            
    def sell_all(self, current_price, is_long):
        
        # Get the correct list
        shlo = self.long_ if is_long else self.short_
        
        # Check that the list is not empty
        if len(shlo) == 0: return
        
        # Sell all of the positions
        for i in range(0, len(shlo)):
            
            # Call the sell function
            self.sell(shlo[0].date, shlo[0].volume, current_price, is_long)