from datetime import datetime

from trading_algorithm_framework.validation import *
from trading_algorithm_framework.equities import *

#----------------
# Asset Classes
#----------------

class StockAsset:
    '''
    Create a new instance of the Stock Asset class to handle the users positions for any given symbol.
    '''

    # The positions that the user has entered, and an identical history dictionary
    positions, history = [{

        # Define dictionaries to hold the users long and short positions in the given stock
        'long' : dict(),
        'short' : dict(),

        # Define dictionaries to hold the users call and put for options stocks
        'call' : dict(),
        'put' : dict()

    } for x in range(2)]
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self):
        
        # Set the users exposure and returns to zero
        self.exposure = 0
        self.returns = 0

        # Set a private variable to store the multiplier for options multiplier
        self.__op_mul = 100

    #----------------
    # Get & Set Methods
    #----------------

    def set_opmul(self, new_opmul):
        self.__op_mul = new_opmul

    def get_opmul(self):
        return self.__op_mul
        
    #----------------
    # Private Methods
    #----------------

    def __calculate_stats(self):
        
        # Reset the base statistics first
        self.exposure = 0
        self.returns = 0

        # Calculate the users exposure. This is given by total long positions minus total short positions. 
        # Also calculate the users returns for long positions.
        long_ = self.positions['long']
        short_ = self.positions['short']

        call_ = self.positions['call']
        put_ = self.positions['put']

        for key in long_:
            self.exposure += long_[key].price * long_[key].volume
            self.returns -= long_[key].price * long_[key].volume

        for key in short_:
            self.exposure -= short_[key].price * short_[key].volume

        for key in call_:
            self.exposure += call_[key].price * call_[key].volume * self.__op_mul
            self.returns -= call_[key].price * call_[key].volume * self.__op_mul

        for key in put_:
            self.exposure -= put_[key].price * put_[key].volume * self.__op_mul

        # Calculate the users returns based on the stock purchase history
        long_ = self.history['long']
        short_ = self.history['short']

        call_ = self.history['call']
        put_ = self.history['put']

        for key in long_:
            self.returns += long_[key].exit_price * long_[key].volume

        for key in short_:
            self.returns += (short_[key].entry_price - short_[key].exit_price) * short_[key].volume

        for key in call_:
            self.returns += call_[key].exit_price * call_[key].volume * self.__op_mul

        for key in put_:
            self.returns += (put_[key].entry_price - put_[key].exit_price) * put_[key].volume * self.__op_mul

    def __clean_positions(self):

        # Check that all stocks with volume 0 have been removed
        for pos_type in self.positions.keys():
            for date_key in self.positions[pos_type].keys():
                if self.positions[pos_type][date_key].volume == 0:
                    self.positions[pos_type].pop(date_key)

    #----------------
    # Public Methods
    #----------------

    # Enter a position with a stock or option
    def enter_position(self, asset_type, share, entry_datetime):

        # Append the new share in the relevant list
        self.positions[asset_type][entry_datetime] = share

        # Clear out any unwanted data in the positions dictionary
        self.__clean_positions()

        # Calculate the new statistics
        self.__calculate_stats()        

    # Leave a position with a stock or option
    def leave_position(self, asset_type, current_price, volume, entry_datetime, exit_datetime):
        
        # Get the volume of the share in question
        stored_volume = positions[asset_type][entry_datetime].volume

        # Return if the volume is negative
        if volume <= 0:
            return

        # If the volume is less than the volume stored, deduct the correct volume
        elif volume < stored_volume:
            stored_volume -= volume

        # If the volume is greater than the stored volume, remove the stock
        else:
            volume = stored_volume

            # Set the stored volume to zero so that we can clear it later
            stored_volume = 0

        # If we are only concerned with a regular stock
        if asset_type in ['long', 'short']:

            # Store the transaction in history
            history[asset_type][exit_datetime] = ShareRecord(
                positions[asset_type][entry_datetime].price,
                current_price,
                volume,
                entry_datetime
            )

        # If we are concerned with options
        elif asset_type in ['call', 'put']:

            # Store the transaction in history
            history[asset_type][exit_datetime] = OptionRecord(
                positions[asset_type][entry_datetime].price,
                current_price,
                volume,
                entry_datetime,
                positions[asset_type][entry_datetime].expiry_datetime,
                positions[asset_type][entry_datetime].premium,
                positions[asset_type][entry_datetime].style
            )


        # Clear out any unwanted data in the positions dictionary
        self.__clean_positions()

        # Calculate the new statistics
        self.__calculate_stats()
    
class CurrencyAsset:
    '''
    Create a new instance of the Currency Asset class to handle purchasing currencies. This will utilize instances of the future 'Quote' class.
    '''
    pass

#----------------
# Portfolio Class
#----------------

class Portfolio:
    '''
    Create a new portfolio to purchase shares with.
    
    Takes 2 arguments:

    - balance (optional) : The money that the account begins with. Set to 50 000 by default;
    - symbols (optional) : A list containing all of the symbols that the user wishes to trade with. Set to nothing by default, but can be changed later.
    '''

    # Declare a dictionary for each desired symbol
    positions = dict()
    
    # Declare a variable to store the users total exposure
    exposure = 0
    
    # Declare another dictionary to hold the holdings percentages based on exposure in the market and the users portfolio balance
    __holdings = dict()
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self, balance=50000, symbols=None):
        
        # Validation
        if symbols: type_check(str, symbols)
        gt_zero(balance)
        
        # Set the balance
        self.balance = balance

        # Set the holdings percentage
        self.__calculate_stats()

        # Add the symbols if the user passed in a list
        if type(symbols) == list: 
            for symbol in symbols: 
                self.add_symbol(symbol)

    #----------------
    # Private Methods
    #----------------

    def __calculate_stats(self):
        
        # Loop through the positions asset list
        for key in self.positions.keys():
            if self.positions[key]:
                self.balance += self.positions[key].returns
                self.exposure += self.positions[key].exposure
            
        # Now that we have the total exposure, calculate the holdings percentage
        for key in self.positions.keys():
            self.__holdings[key] = self.positions[key].exposure / (self.exposure + self.balance)
        
        # Finally include the balance in the holdings
        self.__holdings['portfolio'] = self.balance / (self.exposure + self.balance)

    def __check_share_type(self, asset_type, share):

        # Check that the share instance matches the expected class type
        if asset_type in ['long', 'short']:
            return type(share) == Share
        elif asset_type in ['call', 'put']:
            return type(share) == Option
        elif: asset_type in ['currency']:
            return type(share) == Quote
        else:
            return False

    #----------------
    # Getters & Setters
    #----------------

    def get_holdings(self):
        return self.__holdings

    #----------------
    # Public Methods
    #----------------

    def add_symbol(self, symbol, overwrite=False):
        '''
        Add a new symbol to the positions dictionary. Takes 2 arguments:

        - symbol : The name of the symbol to be added;
        - overwrite (optional) : If the symbol exists, set this to true to overwrite it. Set to False by default.
        '''

        # Replace the asset unless the user does not want to overwrite, and the symbol exists
        if not(symbol in self.positions.keys()) or overwrite: self.positions[symbol] = StockAsset()


    def remove_symbol(self, symbol):

        # Check that the symbol is in the keys list
        if symbol in self.positions.keys():

            # Remove the item
            self.positions.pop(symbol)
            
            
    def reset_balance(self, new_balance=50000): 
        '''
        Resets the user balance. Takes 1 argument:

        - new_balance (optional) : Set to 50 000 by default.
        '''

        # Set the balance
        self.balance = new_balance

    #----------------
    # Buying & Selling
    #----------------
     
    def buy(self, symbol, asset_type, share, entry_datetime):
        '''
        Enters a position. Takes 4 arguments:

        - symbol : The stock symbol that the user is buying stock with;
        - asset_type : The type of position that the user wishes to enter. Takes 4 possible values:
            - 'long' : Enter a long position;
            - 'short' : Enter a short position;
            - 'call' : Enter a call option;
            - 'put' : Enter a put option.
        - share : An instance of the share / option class that the user is entering the position with;
        - entry_datetime : The datetime object associated with the time the position was entered.
        '''

        # Validation for asset type and share type
        if not(self.__check_share_type(asset_type, share)): return

        # Add the symbol if it doesn't exist
        self.add_symbol(symbol)
        
        # Purchase a position in that stock
        self.positions[symbol].enter_position(
            asset_type,
            share,
            entry_datetime
        )
        
        # Calculate the statistics for the portfolio
        self.__calculate_stats()

    def sell(self, symbol, asset_type, current_price, volume, entry_datetime, exit_datetime):
        '''
        Leaves a position. Takes 6 arguments:

        - symbol : The symbol of the asset being sold;
        - asset_type : The type of position the user wishes to leave. Takes 2 possible values:
            - 'long' : Leave a long position;
            - 'short' : Leave a short position;
            - 'call' : Leave a call option;
            - 'put' : Leave a put option.
        - current_price : The current price of the stock;
        - volume : The volume of stock that the user wishes to sell.
        - entry_datetime : The datetime object associated with the time that the position was entered;
        - exit_datetime : The datetime object associated with the time that the position is being sold.
        '''
        
        # Validation for asset type and share type
        if not(self.__check_share_type(asset_type, share)): return

        # Check that the symbol actually exists
        if not(symbol in self.positions.keys()): return
        
        # Check that the user isn't trying to leave a european styled option prematurely
        if asset_type in ['call', 'put']:
            option = self.positions[symbol].positions[asset_type][entry_datetime]
            if option.style == 'eu' and option.expiry_datetime != exit_datetime: return

        # Sell the position for that symbol
        self.positions[symbol].leave_position(
            asset_type,
            current_price,
            volume,
            entry_datetime,
            exit_datetime
        )
        
        # Calculate the statistics for the portfolio
        self.__calculate_stats()

    def sell_all(self, symbol, asset_type, current_price, exit_datetime):
        '''
        Leaves all positions of a given flavour for a given 'Asset' class instance. Takes 4 arguments:

        - symbol : The symbol of the asset being sold;
        - asset_type : The type of position the user wishes to leave. Takes 2 possible values:
            - 'long' : Leave a long position;
            - 'short' : Leave a short position;
            - 'call' : Leave a call option;
            - 'put' : Leave a put option.
        - current_price : The current price of the stock;
        - exit_datetime : The datetime object associated with the time that the position is being sold.
        '''
        
        # Validation for asset type and share type
        if not(self.__check_share_type(asset_type, share)): return

        # Check that the symbol actually exists
        if not(symbol in self.positions.keys()): return

        # Sell all of the positions by looping through all of the existing datetime identifiers
        for date_key in self.positions[symbol].positions.keys():
            self.positions[symbol].leave_position(
                asset_type,
                current_price,
                self.positions[symbol].positions[date_key].volume,
                date_key,
                exit_datetime
            )
            
        # Calculate the statistics for the portfolio
        self.__calculate_stats()
