from pickle import NONE
import time
import requests
import pytz
import json
import math
from datetime import datetime
from pytz import timezone
import numpy as np
import pandas as pd
import pytz
import logging
import yfinance as yf

now = datetime.now()
format = "%d-%m-%Y %H:%M:%S %Z%z"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
ocTime = now_asia.strftime(format)
fName = now_asia.strftime(format)
tdate = fName.split(" IST")
nowTime = tdate[0]
print(nowTime)
curWeekday = datetime.today().weekday()
dtTime = fName.split(" IST")
dt = dtTime[0].split(" ")
dtWithOutTime = dt[0].split(" ")
dateWithOutTime = dtWithOutTime[0]
isHolidayNxtDay = ""
reqTime = ocTime[11:16]
reqMin = ocTime[14:16]
intTime = int(reqTime[0:2])
intMin = int(reqMin)
print("Int min : ", intMin)
counter = 0
logFileName = dateWithOutTime+"-"+"MagicLevel.log"

#b_token = '5817461626:AAHp1IIIMkQGWFTqIuu84lYOoxlO8KS7CZo'
#nse_ch_token = '5771720913:AAH0A70f0BPtPjrOCTrhAb9LR7IGFBVt-oM'
#channel_id = '@swingTradeScreenedStocks'
#nse_ch_id = '-703180529'
my_token = 'bot5771720913:AAH0A70f0BPtPjrOCTrhAb9LR7IGFBVt-oM'
chat_id = '-703180529'

#Fetch Updated Index values from csv file
nsedf_risky_ce = pd.read_csv('./four_magical_lines.csv',usecols=['CE_Risky_Range'],nrows=1)
nsedf_safe_ce = pd.read_csv('./four_magical_lines.csv',usecols=['CE_Safe_Range'],nrows=1)
nsedf_risky_pe = pd.read_csv('./four_magical_lines.csv',usecols=['PE_Risky_Range'],nrows=1)
nsedf_safe_pe = pd.read_csv('./four_magical_lines.csv',usecols=['PE_Safe_Range'],nrows=1)
nse_ce_risky_levels = nsedf_risky_ce['CE_Risky_Range'].loc[nsedf_risky_ce.index[0]]
nse_ce_safe_levels = nsedf_safe_ce['CE_Safe_Range'].loc[nsedf_safe_ce.index[0]]
nse_pe_risky_levels = nsedf_risky_pe['PE_Risky_Range'].loc[nsedf_risky_pe.index[0]]
nse_pe_safe_levels = nsedf_safe_pe['PE_Safe_Range'].loc[nsedf_safe_pe.index[0]]

 #Notify Index values To Telegram Channel after 9:15AM
if intTime==9 and intMin in range(19,30):
#if intTime==16 and intSec in range(15,55):
    t_url = f"https://api.telegram.org/{my_token}/sendMessage?chat_id={chat_id}&text="+"======================\n"+nowTime+"\n======================"+"\nWELCOME TO AI BOT TRADING"+"\n======================"+"\nBOT STARTED SUCCESSFULLY..!"+"\n======================\n"+"TODAY's FOUR MAGICAL LINES\n"+"======================\n"+"NIFTY CE RISKY LEVEL: "+str(nse_ce_risky_levels)+"\n"+"-------------------------------------\n"+"NIFTY CE SAFE LEVEL: "+str(nse_ce_safe_levels)+"\n"+"=========================\n"+"NIFTY PE RISKY LEVEL: "+str(nse_pe_risky_levels)+"\n--------------------------------------\n"+"NIFTY PE SAFE LEVEL: "+str(nse_pe_safe_levels)+"\n"+"=========================\n"+"TRADE AT YOUR OWN RISK..!"+"\n---------------------------------\n"+"WISH YOU PROFITABLE DAY..!"
    requests.post(t_url)
else: 
    print("Not yet 9AM to run the program...!")

data = yf.download("^NSEI", period="1mo", interval="5m")

def get_live_price(data):
    """Fetch the current live price of an index from the last row of data."""
    return float(data['Close'].iloc[-1])

live_price = round(get_live_price(data),2)

print("live nifty price : ", live_price)

def get_nearest_strike_price(live_price, step):
    """Calculate the nearest strike price for a given index price."""
    return round(live_price / step) * step

nearest_strike_nf = get_nearest_strike_price(live_price, 50)

print("Nearest Nifty Strike : ", nearest_strike_nf)

#Keep Running below code from 9AM to 3PM
if intTime >= 9 and intTime < 12:
#if intTime >= 18 and intTime < 54:
    while(intTime<12):
        c = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
        runTime = c.strftime('%H:%M:%S')
        current_hour = int(c.strftime('%H'))
        current_minute = int(c.strftime('%M'))
        if current_hour>12:
            print(f"Exiting the script at {runTime}, as it's past 12 PM.")
            break;
        print("Running task at:", runTime)
        print("Nifty CE RISKY Levels : ",nse_ce_risky_levels)
        print("Nifty CE SAFE Levels : ",nse_ce_safe_levels)
        print("Nifty PE RISKY Levels : ",nse_pe_risky_levels)
        print("Nifty PE SAFE Levels : ",nse_pe_safe_levels)

        nifty_ce_risky_minus_range = int(nse_ce_risky_levels - 10)
        print("nifty_ce_risky_minus_range : ",nifty_ce_risky_minus_range)
        nifty_ce_risky_plus_range = int(nse_ce_risky_levels + 10)
        print("nifty_ce_risky_plus_range : ", nifty_ce_risky_plus_range)
        nifty_ce_safe_minus_range = int(nse_ce_safe_levels - 10 )
        print("nifty_ce_safe_minus_range : ",nifty_ce_safe_minus_range)
        nifty_ce_safe_plus_range = int(nse_ce_safe_levels + 10)
        print("nifty_ce_safe_plus_range : ", nifty_ce_safe_plus_range)
        nifty_pe_risky_minus_range = int(nse_pe_risky_levels - 10 )
        print("nifty_pe_risky_minus_range : ",nifty_pe_risky_minus_range)
        nifty_pe_risky_plus_range = int(nse_pe_risky_levels + 10)
        print("nifty_pe_risky_plus_range : ", nifty_pe_risky_plus_range)
        nifty_pe_safe_minus_range = int(nse_pe_safe_levels - 10) 
        print("nifty_pe_safe_minus_range : ",nifty_pe_safe_minus_range)
        nifty_pe_safe_plus_range = int(nse_pe_safe_levels + 10)
        print("nifty_pe_safe_plus_range : ", nifty_pe_safe_plus_range)

    
        #nf_risky_level_range = range(nse_pe_levels, nse_ce_levels)
        nf_ce_risky_minus_plus_range = range(nifty_ce_risky_minus_range, nifty_ce_risky_plus_range)
        nf_ce_safe_minus_plus_range = range(nifty_ce_safe_minus_range, nifty_ce_safe_plus_range)
        nf_pe_risky_minus_plus_range = range(nifty_pe_risky_minus_range, nifty_pe_risky_plus_range)
        nf_pe_safe_minus_plus_range = range(nifty_pe_safe_minus_range, nifty_pe_safe_plus_range)

        niftyLastPrice = int(live_price)
        print("NIFTY CMP : ",niftyLastPrice)
        print("Run Time : ", runTime)
        counter= counter+1
        print("Counter : ", counter)

       # niftyCELog = dt[0]+'-'+runTime+'\t'+'NIFYT CMP : '+str(niftyLastPrice)+'\t'+'NIFTY TRADING NEAR CE BO LEVEL: '+str(nifty_ce_plus_range)+'\t'
       # niftyPELog = dt[0]+'-'+runTime+'\t'+'NIFYT CMP : '+str(niftyLastPrice)+'\t'+'NIFTY TRADING NEAR PE BO LEVEL: '+str(nifty_pe_minus_range)+'\t'

        
    
        if nifty_ce_risky_minus_range <= niftyLastPrice <= nifty_ce_risky_plus_range :
            buy = 'RISKY PE'
            t_url = f"https://api.telegram.org/{my_token}/sendMessage?chat_id={chat_id}&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's NIFTY 4 Magical LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR RISKY PE BO LEVEL: "+str(nifty_ce_risky_plus_range)+"\n"+"=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf)+" "+buy+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"---------------------------------\n"+"I AM NOT SEBI REG..!"+"\n----------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)

        if nifty_ce_safe_minus_range <= niftyLastPrice <= nifty_ce_safe_plus_range :
            buy = "SAFE PE"
            t_url = f"https://api.telegram.org/{my_token}/sendMessage?chat_id={chat_id}&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's NIFTY 4 Magical LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR SAFE PE BO LEVEL: "+str(nifty_ce_safe_minus_range)+"\n"+"=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf)+" "+buy+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"-----------------------------------\n"+"I AM NOT SEBI REG..!"+"\n---------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)

        if nifty_pe_risky_minus_range <= niftyLastPrice <= nifty_pe_risky_plus_range:
            buy = "RISKY CE"
            t_url = f"https://api.telegram.org/{my_token}/sendMessage?chat_id={chat_id}&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's NIFTY 4 Magical LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR RISKY CE BO LEVEL: "+str(nifty_pe_risky_minus_range)+"\n"+"=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf)+" "+buy+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"-----------------------------------\n"+"I AM NOT SEBI REG..!"+"\n---------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)     

        if nifty_pe_safe_minus_range <= niftyLastPrice <= nifty_pe_safe_plus_range :
            buy = "SAFE CE"
            t_url = f"https://api.telegram.org/{my_token}/sendMessage?chat_id={chat_id}&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's NIFTY LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR SAFE CE BO LEVEL: "+str(nifty_pe_safe_minus_range)+"\n"+"=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf)+" "+buy+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"-----------------------------------\n"+"I AM NOT SEBI REG..!"+"\n---------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)        
   

        time.sleep(180)
