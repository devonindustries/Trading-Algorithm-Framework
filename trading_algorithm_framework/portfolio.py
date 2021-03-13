#----------------
# Data Structures
#----------------


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


class ShareRecord:
    '''
    Create a new share record to handle the users portfolio history for a given asset. Takes 4 arguments:

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


class Option:
    '''
    Create a new option order for a stock that can be added to the users portfolio. Takes 5 arguments:

    - price : The strike price for the option;
    - expiry_datetime : The datetime object associated with the expiration date of the stock;
    - volume : The number of options contracts that the user wishes to enter. One contract equates to 100 shares;
    - premium (optional) : The premium that the user pays for the call, or recieves for the put. Set to zero by default;
    - style (optional) : The type of option that the user is trading with. Takes two possible values:
        - 'us' : (default) American style option;
        - 'eu' : (currently not supported!) European style option.
    '''
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self, price, volume, expiry_datetime, premium=0, style='us'):

        # Keep consistent with the share class
        self.price = price
        self.volume = volume

        # Additional extras that are specific to an option
        self.expiry_datetime = expiry_datetime
        self.premium = premium
        self.style = style


class OptionRecord:
    '''
    Create a new option record to handle the users portfolio history for a given option. Takes 7 arguments:

    - price : The strike price for the option;
    - exit_price : The price that the user left the option position at;
    - volume : The number of contracts that the user pulled out from. One contract equates to 100 shares;
    - entry_datetime : The date that the user bought the option;
    - expiry_datetime : The expiry date of the option;

    See the docstring for the 'Option' class for information about the optional 'premium' and 'style' arguments.
    '''
    def __init__(self, price, exit_price, volume, entry_datetime, expiry_datetime, premium=0, style='us'):
        self.price = price
        self.exit_price = exit_price
        self.volume = volume
        self.entry_datetime = entry_datetime
        self.expiry_datetime = expiry_datetime
        self.premium = premium
        self.style = style 
        

#----------------
# Portfolio Classes
#----------------


class Asset:
    '''
    Create a new instance of the asset class to handle the users positions for any given symbol.
    '''

    # The positions that the user has entered, and an identical history dictionary
    positions, history = {

        # Define dictionaries to hold the users long and short positions in the given stock
        'long' : dict(),
        'short' : dict(),

        # Define dictionaries to hold the users call and put for options stocks
        'call' : dict(),
        'put' : dict()
    }
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self):
        self.exposure = 0
        self.returns = 0

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

        for key in long_:
            self.exposure += long_[key].price * long_[key].volume
            self.returns -= long_[key].price * long_[key].volume

        for key in short_:
            self.exposure -= short_[key].price * short_[key].volume

        # Calculate the users returns based on the stock purchase history
        long_ = self.history['long']
        short_ = self.history['short']

        for key in long_:
            self.returns += long_[key].exit_price * long_[key].volume

        for key in short_:
            self.returns += (short_[key].entry_price - short_[key].exit_price) * short_[key].volume


    #----------------
    # Public Methods
    #----------------

    # Enter a position with a stock or option
    def enter_position(self, asset_type, share, entry_datetime):

        # Append the new share in the relevant list
        self.positions[asset_type][entry_datetime] = share


    # Leave a position with a stock or option
    def leave_position(self, asset_type, current_price, volume, entry_datetime, exit_datetime):
        
        # Get the volume of the share in question
        stored_volume = positions[asset_type][entry_datetime].volume

        # Return if the volume is negative
        if volume <= 0:
            return

        # If the volume is less than the volume stored, deduct the correct volume
        elif volume < stored_volume:
            positions[asset_type][entry_datetime].volume -= volume

        # If the volume is greater than the stored volume, remove the stock
        else:
            volume = stored_volume

        if asset_type in ['long', 'short']:

            # Store the transaction in history
            history[asset_type][exit_datetime] = ShareRecord(
                positions[asset_type][entry_datetime].price,
                current_price,
                volume,
                entry_datetime
            )

        elif asset_type in ['call', 'put']:

            # Store an option transaction in history


        # Calculate the new statistics
        self.__calculate_stats()


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
        - asset_type : The type of position that the user wishes to enter. Takes 4 possible values:
            - 'long' : Enter a long position;
            - 'short' : Enter a short position;
            - 'call' : Enter a call option;
            - 'put' : Enter a put option.
        - share : An instance of the share class that the user is entering the position with;
        - entry_datetime : The datetime object associated with the time the position was entered.
        '''

        # Add the symbol if it doesn't exist
        self.add_symbol(symbol)

        # Check which type of position the user wishes to enter
        if asset_type in ['long', 'short']:

            # Purchase a position in that stock
            self.positions[symbol].enter_position(
                asset_type,
                share,
                entry_datetime
            )

        elif asset_type in ['call', 'put']:
            pass


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
        
        # Check that the symbol actually exists
        if not(symbol in self.positions.keys()): return

        # Check which type of position the user wishes to enter
        if asset_type in ['long', 'short']:

            # Sell the position for that symbol
            self.positions[symbol].leave_position(
                asset_type,
                current_price,
                volume,
                entry_datetime,
                exit_datetime
            )

        elif asset_type in ['call', 'put']:
            pass


    def sell_all(self, symbol, asset_type, current_price, exit_datetime):
        '''
        Leaves all positions. Takes 4 arguments:

        - symbol : The symbol of the asset being sold;
        - asset_type : The type of position the user wishes to leave. Takes 2 possible values:
            - 'long' : Leave a long position;
            - 'short' : Leave a short position;
            - 'call' : Leave a call option;
            - 'put' : Leave a put option.
        - current_price : The current price of the stock;
        - exit_datetime : The datetime object associated with the time that the position is being sold.
        '''
        
        # Check that the symbol actually exists
        if not(symbol in self.positions.keys()): return

        # Check which type of position the user wishes to enter
        if asset_type in ['long', 'short']:

            # Sell all of the positions by looping through all of the existing datetime identifiers
            for date_key in self.positions[symbol].positions.keys()
                self.positions[symbol].leave_position(
                    asset_type,
                    current_price,
                    self.positions[symbol].positions[date_key].volume,
                    date_key,
                    exit_datetime
                )

        elif asset_type in ['call', 'put']:
            pass