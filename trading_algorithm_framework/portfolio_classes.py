# Define a class to handle a share in a stock
class Stock:
    
    def __init__(self, price, volume, date):
        self.price = price
        self.volume = volume
        self.date = date
        
# Define a class to handle the stock information in the users portfolio
class Portfolio:
    
    # Store all of the portfolio short and long positions
    short_ = []
    long_ = []
    
    # An initiation function with $50k start money
    def __init__(self, balance=50000):
        self.balance = balance
        
    # A function to reset the user cash
    def reset_balance(self, new_balance=50000): 
        self.balance = new_balance
        
    # A function to add a share to the users portfolio
    def buy(self, stock, is_long):
        if is_long:
            self.long_.append(stock)
            self.balance -= stock.price * stock.volume
        else:
            self.short_.append(stock)
            
    # A function to sell a position that was entered on a given date
    def sell(self, date, volume, current_price, is_long):
        
        # Get the correct list
        shlo = self.long_ if is_long else self.short_
        
        # Find the desired date value
        for i in range(0, len(shlo)):
            
            # If we find a stock with the correct date, sell the desired volume
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
                
                # Delete the stock
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
                
