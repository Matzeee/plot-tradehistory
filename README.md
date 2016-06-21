# plot-tradehistory
Unofficial: Evaluate and plot transactionhistory[…].csv from Ayondo® TradeHub® 

##Requires
- Python3
- Pandas
- Bokeh
- Matplotlib

## Usage
Download tradehistory[…].csv from TradeHub® with desired timespan (all languages should work).
The script searches for the latest file in its folder and evaluates:
- Paid-in money
- Absolute balance
- Normalised balance for 100€ paid-in at the beginning
- Absolute profit/loss

The output will be a pdf using matplotlib and a [Bokeh-chart](http://bokeh.pydata.org/en/0.11.0/docs/reference/charts.html#timeseries)

###For Beginners
- Under windows, probably the easiest way to set everything is [Anaconda](https://www.continuum.io/downloads). Choose **Python3**
- After installation run cmd as admin:
  - `conda install bokeh`
- Just execute the script or create a `start.bat` containing:
```
python plot-tradehistory.py
pause
```
