import pandas as pd

data = []
df = pd.read_csv('file1.csv')

#calculating the final needed values by reading the previously created file in Q2
for i in range(len(df)):
    gross_pnl_basis_points = (df.iloc[i, 2]/df.iloc[i, 1])*10000
    gross_pnl_usd = df.iloc[i, 2]/df.iloc[i, 1]
    average_pnl = df.iloc[i, 2]/df.iloc[i, 3]
    number_of_trades = df.iloc[i, 3]
    maximum_drawdown = df.iloc[i, 4]

    data.append([gross_pnl_basis_points, gross_pnl_usd, maximum_drawdown, average_pnl, number_of_trades])

df_0 = pd.DataFrame(data, columns=['Gross PnL in Basis Points', 'Gross PnL in USD', 'Maximum Drawdown', 'Average PnL', 'Number of Trades'])
#creating the final result csv file
df_0.to_csv('Final.csv')



