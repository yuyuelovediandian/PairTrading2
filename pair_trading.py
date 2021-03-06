# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:09:12 2017

@author: Administrator
"""

import tushare as ts
import statsmodels.tsa.stattools as sts
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os 
import numpy as np
from datetime import datetime
import operator

from scipy.stats.stats import pearsonr
os.chdir('C:/Users/Administrator/Documents/Python Scripts')
def pre_process_data():    
    df_sz500_price = pd.read_excel('price_data.xlsx','Sheet1')   
    df_sz500_price = df_sz500_price.fillna(0)
    df_sz500_price = df_sz500_price.drop(['index'],axis = 1)
    stocks = list(df_sz500_price.columns)
    return stocks
def fill_stock_code(stocks):
    stocks_str = map(str,stocks)
    stocks_filled = []
    for stk in stocks_str:
        if len(stk) == 6:
            stocks_filled.append(stk)
        elif len(stk) == 5:
            stk = '0' + stk
            stocks_filled.append(stk)
        elif len(stk) == 4:
            stk = '00' + stk
            stocks_filled.append(stk)
        elif len(stk) == 3:
            stk = '000' + stk
            stocks_filled.append(stk)
        elif len(stk) == 2:
            stk = '0000' + stk
            stocks_filled.append(stk)
        elif len(stk) == 1:
            stk = '00000' + stk
            stocks_filled.append(stk)
    return stocks_filled

def get_highcorr_pair(stocks):
    rank = {}
    for i in range(len(stocks)):
        for j in range(i+1,len(stocks)):
            if i != j:
                price_of_i = ts.get_hist_data(str(stocks[i]),start='2015-01-01',end='2016-01-01')
                price_of_j = ts.get_hist_data(str(stocks[j]),start='2015-01-01',end='2016-01-01')
                close_pair = pd.concat([price_of_i['close'],price_of_j['close']],axis=1).dropna()
                close_pair.columns = ['close_i','close_j']
                diff_close_i = ((close_pair['close_i'] - close_pair['close_i'].shift(1))
                                /close_pair['close_i'].shift(1)).dropna()
                diff_close_j = ((close_pair['close_j'] - close_pair['close_j'].shift(1))
                                /close_pair['close_j'].shift(1)).dropna()
                if len(diff_close_i) == len(diff_close_j):
                    correlation = np.corrcoef(diff_close_i.tolist(),diff_close_j.tolist())
                    column = str(stocks[i]) + '_' + str(stocks[j])
                    rank[column] = correlation[0,1]
    rank_sorted = sorted(rank.items(),key=operator.itemgetter(1))                                                                                                                                                                                                                                                                                                                                                                                                           
    potentialPair = [list(map(int, item[0].split('_'))) for item in rank_sorted]
    potentialPair = potentialPair[-5:]

    return potentialPair
                


if __name__ == '__main__':
   stocks = pre_process_data()
   stocks_filled = fill_stock_code(stocks)
   close_pair = get_highcorr_pair(stocks_filled)