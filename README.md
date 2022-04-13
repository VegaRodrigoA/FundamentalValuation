# FundamentalValuation
Hello. 
The objective of this project is to create a sofftware, based on Python, that can help us to make a fundamental valuation of companies.
Basically, it will scrap data, add it to a SQLite database and then analize it.
Thanks for reading.

History
1. First I wrote a script to create the tables of income, balance and cash flow. Then I realized that I could create them faster and with less code using pandas to sql. I still haven't resolve when the ticker to load is new or has data already. So, for the I will keep using this script.
2. The "loads.py" is gonna be the class that we invoque to load new data. 
    The first function allow us to add the income statement. It could work much better adding data directly from pandas, but I prefer to keep advancing with the other statement
