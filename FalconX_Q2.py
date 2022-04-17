import pandas as pd
import os
import glob

path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
data = []
for f in csv_files:
    df = pd.read_csv(f)
    
    #initializing volume, final trade value, and number of trades
    holdings = 0
    final_trade_value = 0
    trade_value = 1000      #trade value cannot exceed 1000 as given bid and offer size = 1000 USD notional
    mid_market_price = df.iloc[0, 1]   #price from which we the buy and sell margin of 3 basis points
    last_traded = 0       #the last traded column
    trades = 0
    for i in range(1, len(df)):
        #as we have to hedge the position as 5000 USD notionals, so ran an if loop while the final trade value is between [-5000, 5000]
        if 5000 >= final_trade_value >= -5000:
               
            #if the traded price exceeds the mid market price by 1.5(since the margin is 3) we sell the position and record the volume, number of trades and final traded value
            if df.iloc[i, 1] >= mid_market_price + 1.5:
                mid_market_price = df.iloc[i, 1]
                trade_value = min(df.iloc[i, 3], 1000)
                #since we sell the position so substraced from the final trade value and holdings
                final_trade_value -= trade_value 
                holdings -= df.iloc[i, 2] 
                trades += 1
                # print(trade_value, 's')
                
            #if the traded price subseed the mid market price by 1.5(since the margin is 3) we buy the position and record the volume, number of trades and final traded value
            elif df.iloc[i, 1] <= mid_market_price - 1.5:
                mid_market_price = df.iloc[i, 1]
                trade_value = min(df.iloc[i, 3], 1000)
                #since we sell the position so add to the final trade value and holdings
                final_trade_value += trade_value
                holdings += df.iloc[i, 2]
                trades += 1
                # print(trade_value, 'b')
        else:
            last_traded = i     #record the last traded column
            break
    #if the trade value goes below -5000 i.e. maximum sell position has been reached, so we buy the positions till the final trade value becomes 0 or greater than 0 
    if final_trade_value <= -5000:
        for j in range(last_traded, len(df)):
            trade_value = min(df.iloc[j, 3], 1000)
            final_trade_value += trade_value
            holdings += df.iloc[j, 2]
            trades += 1
            if final_trade_value >= 0:
                last_traded = j
                final_trade_value = df.iloc[len(df) - 1, 3] - final_trade_value  #finding the profit/loss when the position exits at the last row
                holdings -= df.iloc[len(df) - 1, 2]   #noting down the final holdings
                break

    #if the trade value goes above 5000 i.e. maximum buy position has been reached, so we sell the positions till the final trade value becomes 0 or less than 0
    elif final_trade_value >= 5000:
        for j in range(last_traded, len(df)):
            trade_value = min(df.iloc[j, 3], 1000)
            final_trade_value -= trade_value
            holdings -= df.iloc[j, 2]
            trades += 1
            if final_trade_value <= 0:
                last_traded = j
                final_trade_value = final_trade_value - df.iloc[len(df) - 1, 3]   #finding the profit/loss when the position exits at the last row
                holdings += df.iloc[len(df) - 1, 2]   #noting down the final holdings
                break

    #print(holdings, "Volume")
    #print(final_trade_value, 'Final trade notional')
    #print(trades + 1, 'Number of trades')
    
    
    #finding the maximum drawdown, i.e. the maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained
    max_draw_down = 0
    draw_down = 0
    t = 0  #row with the highest traded price
    for i in range(1, len(df)):
        #if the next traded price is less than the previous one the drawdown = the absolute difference between the highest traded price till then and the next traded price 
        if df.iloc[i, 1] < df.iloc[i - 1, 1]:
            draw_down = abs(df.iloc[i, 1] - df.iloc[t, 1])
            # the drawdown > max drawdown, assign max drawdown
            if draw_down > max_draw_down:
                max_draw_down = draw_down
        
        #if the next traded price is greater than the previous traded price but less than the highest traded price we continue to the next traded price
        elif df.iloc[i, 1] < df.iloc[t, 1]:
            continue
        
        #if the next trade price is greater than the highest traded price, we assign the row to t and go to the next row for the next traded price
        else:
            t = i
    
    #appending the required values to a list to create a data frame
    data.append([holdings, final_trade_value, trades + 1, max_draw_down])

df = pd.DataFrame(data, columns=['Volume', 'Final Trade Notional', 'Number of Trades', 'Maximum Drawdown'])
print(df)

#updating the dataframe to csv file 
df.to_csv('file1.csv')
