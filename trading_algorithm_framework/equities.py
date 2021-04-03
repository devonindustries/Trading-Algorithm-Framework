from datetime import datetime

from trading_algorithm_framework.validation import *

#----------------
# Stocks
#----------------

class Share:
    '''
    Create a new share in a stock that can be added to the users portfolio. Takes 6 arguments:

    - price : The price at the time of purchasing the share;
    - volume : The volume of shares purchased;
    - stop_loss (optional) : Set a stop-loss for a given stock;
    - take_profit (optional) : Set a take profit for a given stock;
    - sensitivity (optional) : The smallest distance between the share price and the SL / TP. Measured in pips and set to 100 by default;
    - ratio (optional) : The multiplier of sensitivity for either bound of the SL or TP. The SL sensitivity = 2 * sensitivity * (1 - ratio), and the TP sensitivity = 2 * sensitivity * ratio. Set to 0.5 by default.
    '''
    
    #----------------
    # Built-in Methods
    #----------------
    
    def __init__(self, price, volume, stop_loss=None, take_profit=None, sensitivity=100, ratio=0.5):
        
        # Validation
        type_check(int, volume)
        gt_zero(price, volume, sensitivity, ratio)
        
        # Store the stock price and volume
        self.price = price
        self.volume = volume

        # Calculate the sensitivity for both values
        sen_sl = 2 * sensitivity * (1 - ratio)
        sen_tp = 2 * sensitivity * ratio

        # Check that the user has entered an SL or TP and adjust so that it fits the sensitivity
        if stop_loss != None:
            gt_zero(stop_loss)
            if price - stop_loss < sen_sl:
                stop_loss = price - sen_sl

        if take_profit != None:
            gt_zero(take_profit)
            if take_profit - price < sen_tp:
                take_profit = price + sen_tp

        # Store the SL and TP
        self.stop_loss = stop_loss
        self.take_profit = take_profit


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
        
        # Validation
        type_check(datetime, entry_datetime)
        type_check(int, volume)
        gt_zero(entry_price, exit_price, volume)
        
        # Store values
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.volume = volume
        self.entry_datetime = entry_datetime

#----------------
# Options
#----------------

class Option(Share):
    '''
    Create a new option order for a stock that can be added to the users portfolio. Inherits from the Share class, and takes 9 arguments:

    - price : The strike price for the option;
    - volume : The number of options contracts that the user wishes to enter. One contract equates to 100 shares;
    - expiry_datetime : The datetime object associated with the expiration date of the stock;
    - premium (optional) : The premium that the user pays for the call, or recieves for the put. Set to zero by default;
    - style (optional) : The type of option that the user is trading with. Takes two possible values:
        - 'us' : (default) American style option;
        - 'eu' : European style option;
    - stop_loss (optional) : Set a stop-loss for a given stock;
    - take_profit (optional) : Set a take profit for a given stock;
    - sensitivity (optional) : The smallest distance between the share price and the SL / TP. Measured in pips and set to 100 by default;
    - ratio (optional) : The multiplier of sensitivity for either bound of the SL or TP. The SL sensitivity = 2 * sensitivity * (1 - ratio), and the TP sensitivity = 2 * sensitivity * ratio. Set to 0.5 by default.
    '''
    
    #----------------
    # Built-in Methods
    #----------------

    def __init__(self, price, volume, expiry_datetime, premium=0, style='us', stop_loss=None, take_profit=None, sensitivity=100, ratio=0.5):

        # Initiate as in the Share class
        super().__init__(price, volume, stop_loss, take_profit, sensitivity, ratio)
        
        # Validation
        type_check(datetime, expiry_datetime)
        type_check(str, style)
        gt_zero(premium)

        # Additional extras that are specific to an option
        self.expiry_datetime = expiry_datetime
        self.premium = premium
        self.style = style


class OptionRecord(ShareRecord):
    '''
    Create a new option record to handle the users portfolio history for a given option. Takes 7 arguments:

    - entry_price : The strike price for the option;
    - exit_price : The price that the user left the option position at;
    - volume : The number of contracts that the user pulled out from. One contract equates to 100 shares;
    - entry_datetime : The date that the user bought the option;
    - expiry_datetime : The expiry date of the option;

    See the docstring for the 'Option' class for information about the optional 'premium' and 'style' arguments.
    '''
    def __init__(self, entry_price, exit_price, volume, entry_datetime, expiry_datetime, premium=0, style='us'):

        # Initiate as per the ShareRecord class
        super().__init__(entry_price, exit_price, volume, entry_datetime)

        # Validation
        type_check(datetime, expiry_datetime)
        type_check(str, style)
        gt_zero(premium)
    
        # Store the arguments that are specific to options.
        self.expiry_datetime = expiry_datetime
        self.premium = premium
        self.style = style
        
#----------------
# Currencies (support to be added in future verisons)
#----------------

class Quote:
    pass
    
class QuoteRecord(Quote):
    pass
