import pandas as pd
from math import log
import os

# Print the current working directory and its type
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))
print("os.getcwd() returns an object of type {0}".format(type(cwd)))

# Change directory to the location where the CSV file is stored
os.chdir("C:\\Users\\digan\\Desktop\\JP Morgan Chase & Co. Quantitative Research\\Task - 4")

# Load the data
df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# Extract 'default' and 'fico_score' columns
x = df['default'].to_list()
y = df['fico_score'].to_list()
n = len(x)

print(len(x), len(y))

# Initialize lists to count defaults and totals
default = [0 for _ in range(851)]
total = [0 for _ in range(851)]

# Populate 'default' and 'total' lists
for i in range(n):
    y[i] = int(y[i])
    default[y[i] - 300] += x[i]
    total[y[i] - 300] += 1

# Calculate cumulative defaults and totals
for i in range(1, 551):
    default[i] += default[i - 1]
    total[i] += total[i - 1]

# Log-likelihood function
def log_likelihood(n, k):
    p = k / n
    if p == 0 or p == 1:
        return 0
    return k * log(p) + (n - k) * log(1 - p)

# Number of buckets
r = 10

# Initialize dynamic programming table
dp = [[[-float('inf'), 0] for _ in range(551)] for _ in range(r + 1)]

# Dynamic programming to find optimal bucket boundaries
for i in range(r + 1):
    for j in range(551):
        if i == 0:
            dp[i][j][0] = 0
        else:
            for k in range(j):
                if total[j] == total[k]:
                    continue
                if i == 1:
                    dp[i][j][0] = log_likelihood(total[j], default[j])
                else:
                    current_likelihood = log_likelihood(total[j] - total[k], default[j] - default[k]) + dp[i - 1][k][0]
                    if dp[i][j][0] < current_likelihood:
                        dp[i][j][0] = current_likelihood
                        dp[i][j][1] = k

# Print the maximum log-likelihood
print(round(dp[r][550][0], 4))

# Retrieve the bucket boundaries
k = 550
l = []
while r >= 0:
    l.append(k + 300)
    k = dp[r][k][1]
    r -= 1

# Print the bucket boundaries
print(l)