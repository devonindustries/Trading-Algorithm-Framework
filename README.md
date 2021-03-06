# Trading Algorithm Framework

A module containing useful packages for testing and writing trading algorithms. The idea of this package is to simulate a stock exchange allowing an algorithm to enter or leave positions. The user will be able to evaluate the performance of the algorithm using various tools available in this package.

## Portfolios

To test a trading algorithm, we must first define an instance of the ‘Portfolio’ class:

```
from portfolio import *

pf = Portfolio(balance=50000)
```

This will define a new instance of the ‘Portfolio’ class. Normally we don’t need to specify the starting balance as it defaults to 50k on declaration.

The Portfolio class has a number of attributes associated with it, but the ones that we are most interested in are the `buy`, `sell`, and `sell_all` methods.

We can buy and sell stocks from the ‘Stock’ class. For now this is a bit messy, but will be taken care of for the user later in development. 

## Stocks

New instances of the ‘Stock’ class require a Pandas data frame for their data. We’ll use the Apple Inc. stock data for this example:

```
import pandas as pd
from stock import *

aapl_data = pd.read_csv(‘AAPL_data.csv’, index_col=0)

aapl_stock = Stock(‘AAPL’, aapl_data)
```

Now with the `Stock` class defined, we can enter and exit different positions. The stock class uses instances of the ‘Point’ class to store each data point, so any time we want to enter a position we will need to convert one of them to an instance of either the `Share` or `Option` classes.

```
entry_datetime = aapl_data.history.keys()[0]

pf.buy(aapl_stock, 'long', entry_datetime, 10)
```

Now that we’ve entered a long position, we can check the portfolio `balance`, as well as its open positions, exposure, and its percentage holdings in each stock (which is accessed using `get_holdings()`).
