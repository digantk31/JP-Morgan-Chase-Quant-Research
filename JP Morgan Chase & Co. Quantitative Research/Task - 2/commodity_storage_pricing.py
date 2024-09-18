import pandas as pd
from datetime import datetime
import math

def price_contract(in_dates, in_prices, out_dates, out_prices, rate, storage_cost_rate, total_vol, injection_withdrawal_cost_rate):
    volume = 0
    buy_cost = 0
    cash_in = 0
    last_date = min(min(in_dates), min(out_dates))
    
    # Ensure dates are in sequence
    all_dates = sorted(set(in_dates + out_dates))
    
    for i in range(len(all_dates)):
        start_date = all_dates[i]

        if start_date in in_dates:
            if volume <= total_vol - rate:
                volume += rate
                buy_cost += rate * in_prices[in_dates.index(start_date)]
                injection_cost = rate * injection_withdrawal_cost_rate
                buy_cost += injection_cost
                print('Injected gas on %s at a price of %s' % (start_date, in_prices[in_dates.index(start_date)]))
            else:
                print('Injection is not possible on date %s as there is insufficient space in the storage facility' % start_date)
        elif start_date in out_dates:
            if volume >= rate:
                volume -= rate
                cash_in += rate * out_prices[out_dates.index(start_date)]
                withdrawal_cost = rate * injection_withdrawal_cost_rate
                cash_in -= withdrawal_cost
                print('Extracted gas on %s at a price of %s' % (start_date, out_prices[out_dates.index(start_date)]))
            else:
                print('Extraction is not possible on date %s as there is insufficient volume of gas stored' % start_date)
                
    store_cost = math.ceil((max(out_dates) - min(in_dates)).days // 30) * storage_cost_rate
    return cash_in - store_cost - buy_cost

# Load data
price_data_file = 'Nat_Gas.csv'  # Path to your CSV file

# Read data from CSV
df = pd.read_csv(price_data_file, parse_dates=['Dates'], index_col='Dates', date_format='%m/%d/%y')

# Extract columns
in_dates = df.index[df.index < datetime(2024, 1, 1)].to_list()
in_prices = df.loc[df.index < datetime(2024, 1, 1), 'Prices'].tolist()

out_dates = df.index[df.index >= datetime(2024, 1, 1)].to_list()
out_prices = df.loc[df.index >= datetime(2024, 1, 1), 'Prices'].tolist()

# Parameters
rate = 100000  # Rate of gas in cubic feet per day
storage_cost_rate = 10000  # Monthly storage cost
injection_withdrawal_cost_rate = 0.0005  # Cost per cubic foot for injection/withdrawal
max_storage_volume = 500000  # Maximum storage volume

# Calculate contract value
result = price_contract(in_dates, in_prices, out_dates, out_prices, rate, storage_cost_rate, max_storage_volume, injection_withdrawal_cost_rate)
print()
print(f"The value of the contract is: ${result}")