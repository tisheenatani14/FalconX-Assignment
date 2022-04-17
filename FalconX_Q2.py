import pandas as pd
import os
import glob

path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
data = []
for f in csv_files:
    df = pd.read_csv(f)

    # df = pd.read_csv("BTCUSDT-trades-2022-03-03.csv")
    print(len(df))

    holdings = 0
    final_trade_value = 0
    trade_value = 1000
    mid_market_price = df.iloc[0, 1]
    last_traded = 0
    trades = 0
    for i in range(1, len(df)):
        if 5000 >= final_trade_value >= -5000:

            if df.iloc[i, 1] >= mid_market_price + 1.5:
                mid_market_price = df.iloc[i, 1]
                trade_value = min(df.iloc[i, 3], 1000)
                final_trade_value -= trade_value
                holdings -= df.iloc[i, 2]
                trades += 1
                # print(trade_value, 's')

            elif df.iloc[i, 1] <= mid_market_price - 1.5:
                mid_market_price = df.iloc[i, 1]
                trade_value = min(df.iloc[i, 3], 1000)
                final_trade_value += trade_value
                holdings += df.iloc[i, 2]
                trades += 1
                # print(trade_value, 'b')
        else:
            last_traded = i
            break
    if final_trade_value <= -5000:
        for j in range(last_traded, len(df)):
            trade_value = min(df.iloc[j, 3], 1000)
            final_trade_value += trade_value
            holdings += df.iloc[j, 2]
            trades += 1
            if final_trade_value >= 0:
                last_traded = j
                final_trade_value = df.iloc[len(df) - 1, 3] - final_trade_value
                holdings -= df.iloc[len(df) - 1, 2]
                break


    elif final_trade_value >= 5000:
        for j in range(last_traded, len(df)):
            trade_value = min(df.iloc[j, 3], 1000)
            final_trade_value -= trade_value
            holdings -= df.iloc[j, 2]
            trades += 1
            if final_trade_value <= 0:
                last_traded = j
                final_trade_value = final_trade_value - df.iloc[len(df) - 1, 3]
                holdings += df.iloc[len(df) - 1, 2]
                break

    print(holdings, "Volume")
    print(final_trade_value, 'Final trade notional')
    print(trades + 1, 'Number of trades')

    max_draw_down = 0
    draw_down = 0
    t = 0
    for i in range(1, len(df)):
        if df.iloc[i, 1] < df.iloc[i - 1, 1]:
            draw_down = abs(df.iloc[i, 1] - df.iloc[t, 1])
            if draw_down > max_draw_down:
                max_draw_down = draw_down
        elif df.iloc[i, 1] < df.iloc[t, 1]:
            continue
        else:
            t = i

    data.append([holdings, final_trade_value, trades + 1, max_draw_down])

df = pd.DataFrame(data, columns=['Volume', 'Final Trade Notional', 'Number of Trades', 'Maximum Drawdown'])
print(df)
df.to_csv('file1.csv')