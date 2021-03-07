# Define a class to handle a share in a stock
class Share:
    '''
    Create a new share in a stock that can be added to the users portfolio. Takes four arguments:

    - price : The price at the time of purchasing the share;
    - volume : The volume of shares purchased;
    - date : The date that the stock was purchased;
    - symbol (optional) : The symbol of the stock. Empty by default.
    '''
    
    # Declare the id attribute before assignment for validation
    __id = None
    
    #----------------
    # Built-in Methods
    #----------------
    
    def __init__(self, price, volume, stock_date, symbol=None):
        self.price = price
        self.volume = volume
        self.stock_date = stock_date
        self.symbol = symbol
    
    #----------------
    # Public Methods
    #----------------
                
    # Set a private id attribute using a public method to avoid overwriting
    def set_id(self, id):
        if not(self.__id):
            self.__id = id
          
    # Public method to return the id
    def get_id(self):
        return self.__id
          
        
# Define a class to handle the stock information in the users portfolio
class Portfolio:
    '''
    Create a new portfolio to purchase shares with.
    
    ! Note: Currently there is no suppoprt for stock timestamps, only dates. Support may be added in later versions.

    Values that may be allocated when calling this class:

    - starting_balance = 50 000 (by default)
    '''
    
    # Store all of the portfolio short and long positions
    short_ = []
    long_ = []

    # Define private attributes to dynamically allocate IDs to shares
    # This will start at zero, and will only ever be incremented
    __short_id = 0
    __long_id = 0
    
    #----------------
    # Private Methods
    #----------------
    
    # An initiation function with $50k start money
    def __init__(self, balance=50000):
        self.balance = balance
        
    # Call this every time a position is entered
    def __increment_id(self, is_long):
        if is_long:
            self.__long_id += 1
        else:
            self.__short_id += 1
    
    # Call this to get the position of a share with a given id    
    def __get_from_id(self, search_id, is_long):
        
        # Get the array in question
        shlo = self.long_ if is_long else self.short_
        
        # Return position in array 
        i = 0
        
        # Loop until we find a stock with the given id
        while not(pos):
          
          # Return if the id matches
          if shlo[i].get_id() == search_id:
            return i
          
    
    #----------------
    # Public Methods
    #----------------
    
    # A function to reset the user cash
    def reset_balance(self, new_balance=50000): 
        '''
        Resets the user balance. Takes one argument:

        - (new_balance) : Set to 50 000 by default.
        '''
        self.balance = new_balance
        
    # A function to add a share to the users portfolio
    def buy(self, share, is_long):
        '''
        Enters a position. Takes two arguments:

        - share : An instance of the share class for the stock you wish to purchase;
        - is_long : A boolean which tells the portfolio to store the share as a long or short position.
        '''
      
        # Reference the array in question
        shlo = self.long_ if is_long else self.short_
        
        # Set the id incrementer
        temp_id = self.__long_id if is_long else self.__short_id
        
        # Set the id of the share
        share.set_id(temp_id)
        
        # Increment the correct id
        self.__increment_id(is_long)
        
        # Append to the correct array
        shlo.append(share)
        
        # If the position is long, deduct from the balance
        if is_long:
            self.balance -= share.price * share.volume
            
    # A function to sell a position with a given id
    def sell(self, share_id, volume, current_price, is_long):
        '''
        Leaves a postion. Takes four arguments:

        - share_id : The id of the share that the user wishes to sell;
        - volume : The number of shares that the user wishes to purchase. Max volume will be sold if this exceeds the existing volume;
        - current_price : The value of the share on the date assigned;
        - is_long : A boolean which tells the portfolio to store the share as a long or short position.
        '''
        
        # Reference the array in question
        shlo = self.long_ if is_long else self.short_
        
        # Get the position in the array that holds the desired stock
        pos = self.__get_from_id(share_id, is_long)
        
        # Bound the volume if it is too high
        if volume > shlo[pos].volume: volume = shlo[pos].volume

        # Now sell the stock depending on the position
        balance += volume * current_price if is_long else volume * (shlo[pos].price - current_price)

        # Remove the stock from the users portfolio if the maximum volume was sold, or adjust the volume
        if volume == shlo[pos].volume:
            shlo.pop(pos)
        else:
            shlo[pos].volume -= volume
  
    # Sell all the stock held by the portfolio
    def sell_all(self, current_price, is_long):
        '''
        Leaves all positions for a given position type. Takes two arguments:

        - current_price : The value of the share when the method is called
        '''
        
        # Reference the array in question
        shlo = self.long_ if is_long else self.short_

        # If the array is empty, then return
        if len(shlo) == 0: return

        # Loop through all of the positions in the array
        for i in range(0, len(shlo)):

            # Get the stock id
            temp_id = shlo[0].get_id()

            # Delete the stock with that id
            self.sell(temp_id, shlo[0].volume, current_price, is_long)