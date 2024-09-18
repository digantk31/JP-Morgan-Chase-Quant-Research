import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import date, timedelta

# Print the current working directory
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))
print("os.getcwd() returns an object of type {0}".format(type(cwd)))

# Change directory to where the CSV file is located
# Note: Ensure this path is correct and use raw string notation to avoid escape sequence issues
os.chdir(r"C:\Users\digan\Desktop\JP Morgan Chase & Co. Quantitative Research\Task - 1")

# Load data
df = pd.read_csv('Nat_Gas.csv', dtype={'Dates': 'object'})
df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')

# Extract prices and dates
prices = df['Prices'].values
dates = df['Dates'].values

# Plot prices against dates
fig, ax = plt.subplots()
ax.plot(dates, prices, marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Natural Gas Prices')
ax.tick_params(axis='x', rotation=45)
plt.show()

# Linear regression for trend analysis
start_date = date(2020, 10, 31)
end_date = date(2024, 9, 30)
months = []
year = start_date.year
month = start_date.month + 1

while True:
    current = date(year, month, 1) + timedelta(days=-1)
    months.append(current)
    if current.month == end_date.month and current.year == end_date.year:
        break
    else:
        month = ((month + 1) % 12) or 12
        if month == 1:
            year += 1

days_from_start = [(day - start_date).days for day in months]

def simple_regression(x, y):
    xbar = np.mean(x)
    ybar = np.mean(y)
    slope = np.sum((x - xbar) * (y - ybar)) / np.sum((x - xbar)**2)
    intercept = ybar - slope * xbar
    return slope, intercept

time = np.array(days_from_start)
slope, intercept = simple_regression(time, prices)

# Plot linear trend
plt.plot(time, prices, marker='o', linestyle='-', label='Actual Prices')
plt.plot(time, time * slope + intercept, linestyle='--', color='red', label='Linear Trend')
plt.xlabel('Days from start date')
plt.ylabel('Price')
plt.title('Linear Trend of Monthly Input Prices')
plt.legend()
plt.show()

# Fit sine function for intra-year variation
sin_prices = prices - (time * slope + intercept)
sin_time = np.sin(time * 2 * np.pi / 365)
cos_time = np.cos(time * 2 * np.pi / 365)

def bilinear_regression(y, x1, x2):
    slope1 = np.sum(y * x1) / np.sum(x1 ** 2)
    slope2 = np.sum(y * x2) / np.sum(x2 ** 2)
    return slope1, slope2

slope1, slope2 = bilinear_regression(sin_prices, sin_time, cos_time)

# Recover amplitude and phase shift
amplitude = np.sqrt(slope1 ** 2 + slope2 ** 2)
shift = np.arctan2(slope2, slope1)

# Plot smoothed estimate of full dataset
plt.plot(time, amplitude * np.sin(time * 2 * np.pi / 365 + shift), label='Smoothed Estimate')
plt.plot(time, sin_prices, marker='o', linestyle='-', label='Sin Prices')
plt.title('Smoothed Estimate of Monthly Input Prices')
plt.xlabel('Days from start date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Define interpolation/extrapolation function
def interpolate(date):
    days = (date - pd.Timestamp(start_date)).days
    return amplitude * np.sin(days * 2 * np.pi / 365 + shift) + days * slope + intercept

# Create a range of continuous dates from start date to end date
continuous_dates = pd.date_range(start=pd.Timestamp(start_date), end=pd.Timestamp(end_date), freq='D')

# Plot the smoothed estimate of the full dataset using interpolation
plt.plot(continuous_dates, [interpolate(date) for date in continuous_dates], label='Smoothed Estimate')

# Fit the monthly input prices to the sine curve
x = np.array(days_from_start)
y = np.array(prices)
fit_amplitude = np.sqrt(slope1 ** 2 + slope2 ** 2)
fit_shift = np.arctan2(slope2, slope1)
fit_slope, fit_intercept = simple_regression(x, y - fit_amplitude * np.sin(x * 2 * np.pi / 365 + fit_shift))
plt.plot(dates, y, 'o', label='Monthly Input Prices')
plt.plot(continuous_dates, fit_amplitude * np.sin((continuous_dates - pd.Timestamp(start_date)).days * 2 * np.pi / 365 + fit_shift) + (continuous_dates - pd.Timestamp(start_date)).days * fit_slope + fit_intercept, label='Fit to Sine Curve')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Natural Gas Prices')
plt.legend()
plt.show()