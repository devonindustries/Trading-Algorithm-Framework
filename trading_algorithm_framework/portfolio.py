# Define a class to handle a share in a stock
class Share:
    '''
    Create a new share in a stock that can be added to the users portfolio. Takes 2 arguments:

    - price : The price at the time of purchasing the share;
    - volume : The volume of shares purchased.
    '''
    
    #----------------
    # Built-in Methods
    #----------------
    
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume


# Define a class to store all of the record information regarding shares
class ShareRecord:
    '''
    Create a new share record to handle the users portfolio history for a given asset. Takes 3 arguments:

    - entry_price : The price when the position was entered;
    - exit_price : The price when the position was exited;
    - volume : The volume of stocks during the transaction;
    - entry_datetime : The datetime object associated with the time that the position was entered.
    '''
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self, entry_price, exit_price, volume, entry_datetime):
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.volume = volume
        self.entry_datetime = entry_datetime



# Define a class to handle the positions for a given symbol. This will be handled by the Portfolio class
class Asset:
    '''
    Create a new instance of the asset class to handle the users positions for any given symbol
    '''

    # The users statistics for a given ticker
    exposure = 0
    gains = 0

    # The positions that the user has entered, and an identical history dictionary
    positions, history = {

        # Define dictionaries to hold the users long and short positions in the given stock
        'long' : dict(),
        'short' : dict(),

        # Define dictionaries for call and put options (support will be added in future versions)
        'call' : dict(),
        'put' : dict(),
    }
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self):
        pass

    #----------------
    # Private Methods
    #----------------

    def __calculate_stats():
        pass

    #----------------
    # Public Methods
    #----------------

    def enter_position(self, asset_type, share, entry_datetime):

        # Append the new share in the relevant list
        self.positions[asset_type][entry_datetime] = share


    def leave_position(self, asset_type, current_price, volume, entry_datetime, exit_datetime):

        stored_volume = positions[asset_type][entry_datetime].volume

        # 1. Return if the volume is negative
        if volume <= 0:
            return

        # 2. If the volume is less than the volume stored, deduct the correct volume
        elif volume < stored_volume:
            positions[asset_type][entry_datetime].volume -= volume

        # 3. If the volume is greater than the stored volume, remove the stock
        else:
            volume = stored_volume

        # 4. Store the transaction in history
        history[asset_type][exit_datetime] = ShareRecord(
            positions[asset_type][entry_datetime].price,
            current_price,
            volume,
            entry_datetime
        )

        # 5. Calculate the new statistics
        self.__calculate_stats()

        pass



# Define a class to handle the stock information in the users portfolio
class Portfolio:
    '''
    Create a new portfolio to purchase shares with.
    
    Takes 2 arguments:

    - balance (optional) : The money that the account begins with. Set to 50 000 by default;
    - symbols (optional) : A list containing all of the symbols that the user wishes to trade with. Set to nothing by default, but can be changed later.
    '''

    # Declare a dictionary for each desired symbol
    positions = dict()

    #----------------
    # Built-in Methods
    #----------------

    def __init__(self, balance=50000, symbols=None):
        self.balance = balance

        # Add the symbols if the user passed in a list
        if type(symbols) == list: 
            for symbol in symbols: 
                self.add_symbol(symbol)
          
    #----------------
    # Public Methods
    #----------------

    def reset_balance(self, new_balance=50000): 
        '''
        Resets the user balance. Takes 1 argument:

        - new_balance (optional) : Set to 50 000 by default.
        '''

        # Set the balance
        self.balance = new_balance


    def add_symbol(self, symbol, overwrite=False):
        '''
        Add a new symbol to the positions dictionary. Takes 2 arguments:

        - symbol : The name of the symbol to be added;
        - overwrite (optional) : If the symbol exists, set this to true to overwrite it. Set to False by default.
        '''

        # Replace the asset unless the user does not want to overwrite, and the symbol exists
        if not(symbol in self.positions.keys()) or overwrite: self.positions[symbol] = Asset()


    def remove_symbol(self, symbol):

        # Check that the symbol is in the keys list
        if symbol in self.positions.keys():

            # Remove the item
            self.positions.pop(symbol)

    
    def buy(self, symbol, asset_type, share, entry_datetime):
        '''
        Enters a position. Takes 4 arguments:

        - symbol : The stock symbol that the user is buying stock with;
        - asset_type : The type of position that the user wishes to enter. Takes 2 possible values:
            - 'long' : Enter a long position;
            - 'short' : Enter a short position;
        - share : An instance of the share class that the user is entering the position with;
        - entry_datetime : The datetime object associated with the time the position was entered.
        '''
        pass


    def sell(self, symbol, asset_type, current_price, volume, entry_datetime, sell_datetime):
        '''
        Leaves a position. Takes 4 arguments:

        - symbol : The symbol of the asset being sold;
        - asset_type : The type of position the user wishes to leave. Takes 2 possible values:
            - 'long' : Enter a long position;
            - 'short' : Enter a short position;
        - current_price : The current price of the stock;
        - volume : The volume of stock that the user wishes to sell.
        - entry_datetime : The datetime object associated with the time that the position was entered;
        - sell_datetime : The datetime object associated with the time that the position is being sold.
        '''
        pass


    def sell_all(self, symbol, asset_type, sell_datetime):
        '''
        Leaves all positions. Takes 2 arguments:

        - symbol : The symbol of the asset being sold;
        - asset_type : The type of position the user wishes to leave. Takes 2 possible values:
            - 'long' : Enter a long position;
            - 'short' : Enter a short position;
        - sell_datetime : The datetime object associated with the time that the position is being sold.
        '''
        pass

    


#     # A function to add a share to the users portfolio
#     def buy(self, share, is_long):
#         '''
#         Enters a position. Takes two arguments:
#         - share : An instance of the share class for the stock you wish to purchase;
#         - is_long : A boolean which tells the portfolio to store the share as a long or short position.
#         '''     
#         # Reference the array in question
#         shlo = self.long_ if is_long else self.short_      
#         # Set the id incrementer
#         temp_id = self.__long_id if is_long else self.__short_id      
#         # Set the id of the share
#         share.set_id(temp_id)     
#         # Increment the correct id
#         self.__increment_id(is_long)      
#         # Append to the correct array
#         shlo.append(share)
#         # If the position is long, deduct from the balance
#         if is_long:
#             self.balance -= share.price * share.volume
#     # A function to sell a position with a given id
#     def sell(self, share_id, volume, current_price, is_long):
#         '''
#         Leaves a postion. Takes four arguments:
#         - share_id : The id of the share that the user wishes to sell;
#         - volume : The number of shares that the user wishes to purchase. Max volume will be sold if this exceeds the existing volume;
#         - current_price : The value of the share on the date assigned;
#         - is_long : A boolean which tells the portfolio to store the share as a long or short position.
#         '''      
#         # Reference the array in question
#         shlo = self.long_ if is_long else self.short_      
#         # Get the position in the array that holds the desired stock
#         pos = self.__get_from_id(share_id, is_long)     
#         # Bound the volume if it is too high
#         if volume > shlo[pos].volume: volume = shlo[pos].volum
#         # Now sell the stock depending on the position
#         balance += volume * current_price if is_long else volume * (shlo[pos].price - current_price)
#         # Remove the stock from the users portfolio if the maximum volume was sold, or adjust the volume
#         if volume == shlo[pos].volume:
#             shlo.pop(pos)
#         else:
#             shlo[pos].volume -= volume
#     # Sell all the stock held by the portfolio
#     def sell_all(self, current_price, is_long):
#         '''
#         Leaves all positions for a given position type. Takes two arguments:
#         - current_price : The value of the share when the method is called
#         '''     
#         # Reference the array in question
#         shlo = self.long_ if is_long else self.short_
#         # If the array is empty, then return
#         if len(shlo) == 0: return
#         # Loop through all of the positions in the array
#         for i in range(0, len(shlo)):
#             # Get the stock id
#             temp_id = shlo[0].get_id()
#             # Delete the stock with that id
#             self.sell(temp_id, shlo[0].volume, current_price, is_long)