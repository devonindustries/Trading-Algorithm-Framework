from datetime import datetime

import pandas as pd

# Define a class to store the data for any given point on the stock chart.
class Point:
    '''
    Describes a point on the stock chart. Used by the Stock class.

    Takes 5 arguments:

    - volume : The number of stocks that were sold on a given date;
    - close_price : The closing price for a given date;
    - open_price : The opening price for a given date;
    - low_price : The low price for a given date;
    - high_price : The high price for a given date;
    '''
    def __init__(
        self,
        volume,
        close_price,
        open_price = None,
        low_price = None,
        high_price = None,
    ):
        self.volume = volume
        self.close_price = close_price
        self.open_price = open_price
        self.high_price = high_price

# Define a class to store an actual stock with all of its data
class Stock:
    '''
    Describes an asset and contains all of its data between any two dates.

    Takes 3 arguments:

    - symbol : The symbol representing the asset;
    - data : A pandas dataframe holding all of the stock information. Explicitly, this dataframe must have column names:
        - date (index) : Each of the dates takes the format of 'date_format'
        - volume
        - close
        - open
        - low
        - high
    - date_format (optional) : Denotes the arrangement of the dates. Set to '%Y-%m-%d' by default;
    '''

    # Declare a variable for checkign the headings
    __headings = ['volume', 'close', 'open', 'low', 'high']

    # Declare the date format just in case we need to change it later on
    __date_format = None

    # Declare a dictionary of dates as keys, and points as the corresponding data
    history = dict()

    # Declare a dataframe version of the history variable
    history_df = None

    #----------------
    # Built-in Methods
    #----------------

    def __init__(
        self,
        symbol,
        data,
        date_format = '%Y-%m-%d'
    ):
        # Store the date format
        self.set_date_format(date_format)
        
        # Verify that the dataframe headings are formatted correctly
        if not(self.__verify_headings(data.columns)): 
            raise ValueError('Headings do not line up!') from None
        
        # Store each point for the stock
        for index, row in data.iterrows():
            
            # Convert the date so that it is a date object
            new_date = datetime.strptime(index, self.get_date_format())

            # Define a new point
            new_point = Point(
                int(row[__headings[0]]),
                int(row[__headings[1]]),
                int(row[__headings[2]]),
                int(row[__headings[3]]),
                int(row[__headings[4]])
            )

            # Store each point in the dictionary
            self.history[new_date] = new_point

        # Store the dataframe as its own object
        history_df = data

    #----------------
    # Get / Set Methods
    #----------------

    # Date format
    def get_date_format(self, date_format):
        return self.__date_format

    def set_date_format(self, date_format):
        if not(self.__date_format): 
            self.__date_format = datetime
    
    #----------------
    # Private Methods
    #----------------

    # A private method to return false if the dataframe headings are not formatted correctly
    def __verify_headings(self, columns):
        
        # Check that the headings line up with the columns
        check = [x in columns for x in headings]

        # If there is a false in there, then the validation has failed
        return(not(False in check))


# Define a class to handle indices (this will be properly implemented later)
class Index:
    pass