import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import requests
import httpx
from typing import List
from .paper_models import WebullContractData
load_dotenv()




import pandas as pd
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
import os
import hashlib
from .screener_models import ScreenerResults,OptionScreenerResults
import time
import uuid
from imps import *
import pickle
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
load_dotenv()
import httpx
import asyncio
class PaperTrader:
    def __init__(self, headers):
        self.headers=headers
        self.id = 16067985
        self.db = PolygonDatabase()
        #miscellaenous
                #sessions
        self.ticker_df = pd.read_csv('ticker_csv.csv')
        self.ticker_to_id_map = dict(zip(self.ticker_df['ticker'], self.ticker_df['id']))
        self._region_code = 6
        self.zone_var = 'dc_core_r001'
        self.timeout = 15
        self.db = PolygonDatabase(host='localhost', user='chuck', database='market_data', password='fud', port=5432)
        self.device_id = "gldaboazf4y28thligawz4a7xamqu91g"
        self.account_id = 15765933
        self.most_active_tickers = ['SNOW', 'IBM', 'DKNG', 'SLV', 'NWL', 'SPXS', 'DIA', 'QCOM', 'CMG', 'WYNN', 'PENN', 'HLF', 'CCJ', 'WW', 'NEM', 'MOS', 'SRPT', 'MS', 'DPST', 'AG', 'PAA', 'PANW', 'XPEV', 'BHC', 'KSS', 'XLP', 'LLY', 'MDB', 'AZN', 'NVO', 'BOIL', 'ZM', 'HUT', 'VIX', 'PDD', 'SLB', 'PCG', 'DIS', 'TFC', 'SIRI', 'TDOC', 'CRSP', 'BSX', 'BITF', 'AAL', 'EOSE', 'RIVN', 'X', 'CCL', 'SOXS', 'NOVA', 'TMUS', 'HES', 'LI', 'NVAX', 'TSM', 'CNC', 'IAU', 'GDDY', 'CVX', 'TGT', 'MCD', 'GDXJ', 'AAPL', 'NKLA', 'EDR', 'NOK', 'SPWR', 'NKE', 'HYG', 'FSLR', 'SGEN', 'DNN', 'BAX', 'CRWD', 'OSTK', 'XLC', 'RIG', 'SEDG', 'SNDL', 'RSP', 'M', 'CD', 'UNG', 'LQD', 'TTD', 'AMGN', 'EQT', 'YINN', 'MULN', 'FTNT', 'WBD', 'MRNA', 'PTON', 'SCHW', 'ABNB', 'EW', 'PM', 'UCO', 'TXN', 'DLR', 'KHC', 'MMAT', 'QQQ', 'GOOGL', 'AEM', 'RTX', 'AVGO', 'RBLX', 'PAAS', 'UUP', 'OXY', 'SQ', 'PLUG', 'CLF', 'GOEV', 'BKLN', 'ALB', 'BALL', 'SMH', 'CVE', 'F', 'KRE', 'TWLO', 'ARCC', 'ARM', 'U', 'SOFI', 'SBUX', 'FXI', 'BMY', 'HSBC', 'EFA', 'SVXY', 'VALE', 'GOLD', 'MSFT', 'OIH', 'ARKK', 'AMD', 'AA', 'DXCM', 'ABT', 'WOLF', 'FDX', 'SOXL', 'MA', 'KWEB', 'BP', 'SNAP', 'NLY', 'KGC', 'URA', 'UVIX', 'KMI', 'ACB', 'NET', 'W', 'GRAB', 'LMT', 'EPD', 'FCX', 'STNE', 'NIO', 'SU', 'ET', 'CVS', 'ADBE', 'MXL', 'HOOD', 'FUBO', 'RIOT', 'CRM', 'TNA', 'DISH', 'XBI', 'VFS', 'GPS', 'NVDA', 'MGM', 'MRK', 'ABBV', 'LABU', 'BEKE', 'VRT', 'LVS', 'CPNG', 'BA', 'MTCH', 'PEP', 'EBAY', 'GDX', 'XLV', 'UBER', 'GOOG', 'COF', 'XLU', 'BILI', 'XLK', 'VXX', 'DVN', 'MSOS', 'KOLD', 'XOM', 'BKNG', 'SPY', 'RUT', 'CMCSA', 'STLA', 'NCLH', 'GRPN', 'ZION', 'UAL', 'GM', 'NDX', 'TQQQ', 'COIN', 'WBA', 'CLSK', 'NFLX', 'FREY', 'AFRM', 'NAT', 'EEM', 'IYR', 'KEY', 'OPEN', 'DM', 'TSLA', 'BXMT', 'T', 'TZA', 'BAC', 'MARA', 'UVXY', 'LOW', 'COST', 'HL', 'CHTR', 'TMF', 'ROKU', 'DOCU', 'PSEC', 'XHB', 'VMW', 'SABR', 'USB', 'DDOG', 'DB', 'V', 'NOW', 'XRT', 'SMCI', 'PFE', 'NYCB', 'BIDU', 'C', 'SPX', 'ETSY', 'EMB', 'SQQQ', 'CHPT', 'DASH', 'VZ', 'DNA', 'CL', 'ANET', 'WMT', 'MRO', 'WFC', 'MO', 'USO', 'ENVX', 'INTC', 'GEO', 'VFC', 'WE', 'MET', 'CHWY', 'PBR', 'KO', 'TH', 'QS', 'BTU', 'GLD', 'JD', 'XLY', 'KR', 'ASTS', 'WDC', 'HTZ', 'XLF', 'COP', 'PATH', 'SHEL', 'MXEF', 'SE', 'SPCE', 'UPS', 'RUN', 'DOW', 'ASHR', 'ONON', 'DAL', 'SPXL', 'SAVE', 'LUV', 'HD', 'JNJ', 'LYFT', 'UNH', 'BBY', 'CZR', 'NEE', 'STNG', 'SPXU', 'MMM', 'VNQ', 'IMGN', 'MSTR', 'AXP', 'TMO', 'XPO', 'FEZ', 'ENPH', 'AX', 'NVCR', 'GS', 'MRVL', 'ADM', 'GILD', 'IBB', 'FTCH', 'PARA', 'PINS', 'JBLU', 'SNY', 'BITO', 'PYPL', 'FAS', 'GME', 'LAZR', 'URNM', 'BX', 'MPW', 'UPRO', 'HPQ', 'AMZN', 'SAVA', 'TLT', 'ON', 'CAT', 'VLO', 'AR', 'IDXX', 'SWN', 'META', 'BABA', 'ZS', 'EWZ', 'ORCL', 'XOP', 'TJX', 'XP', 'EL', 'HAL', 'IEF', 'XLI', 'UPST', 'Z', 'TELL', 'LRCX', 'DLTR', 'BYND', 'PACW', 'CVNA', 'GSAT', 'CSCO', 'NU', 'KVUE', 'JPM', 'LCID', 'TLRY', 'AGNC', 'CGC', 'XLE', 'VOD', 'TEVA', 'JETS', 'UEC', 'FSR', 'ZIM', 'ABR', 'IQ', 'AMC', 'ALLY', 'HE', 'OKTA', 'ACN', 'MU', 'FLEX', 'SHOP', 'PLTR', 'CLX', 'LUMN', 'WHR', 'PAGP', 'IWM', 'WPM', 'TTWO', 'AI', 'ALGN', 'SPOT', 'BTG', 'IONQ', 'GE', 'DG', 'AMAT', 'XSP', 'PG', 'LULU', 'DE', 'MDT', 'RCL', 'RDDT']
    async def get_webull_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_id = self.ticker_to_id_map.get(symbol)
        return ticker_id

    def to_decimal(self, value: Optional[str]) -> str:
        """
        Convert percentage string to decimal string if needed.
        """
        if value is not None and float(value) > 1:
            return str(float(value) / 100)
        return value


    async def get_account_id(self):
        new_acc_url = f"https://act.webullfintech.com/webull-paper-center/api/paper/v1/account/myaccounts?isInit=true&version=v1&supportAccountTypes=CASH%2CMARGIN_FUTURES"

        async with httpx.AsyncClient() as client:
            data = await client.get(new_acc_url, headers=self.headers)
            if data.status_code == 200:
                data = data.json()
                paper_id = data[0].get('id')
                print(paper_id)
                return paper_id

    async def get_option_id(self, ticker):
        
        try:
            if ticker == 'SPX':
                ticker = 'SPXW'
            df = await self.____(ticker)
            await self.db.batch_insert_dataframe(df, table_name='ids', unique_columns='option_id', )
            return df
        except Exception as e:
            print(e)

    async def update_option_ids(self):
        
        await self.db.connect()
        tasks = [self.get_option_id(i) for i in self.most_active_tickers]

        await asyncio.gather(*tasks)
        await self.db.disconnect()


    async def ____(self, ticker):
        """TABLE NAME = ids"""
      
        try:
            ticker_id = await self.get_webull_id(ticker)
            payload = {"expireCycle":[3,2,4],"type":0,"quoteMultiplier":100,"count":-1,"direction":"all", 'tickerId': ticker_id}
            url = f"https://quotes-gw.webullfintech.com/api/quote/option/strategy/list"
            async with httpx.AsyncClient(headers=self.headers) as client:
                data = await client.post(url, json=payload)

                if data.status_code == 200:
                    data = data.json()
                    expireDateList = data['expireDateList']
                    data = [i.get('data') for i in expireDateList]
                    flat_data = [item for sublist in data for item in sublist]
                    option_ids = [i.get('tickerId') for i in flat_data]
                    strike = [float(i.get('strikePrice')) for i in flat_data]
                    call_put = [i.get('direction') for i in flat_data]
                    expiry = [i.get('expireDate') for i in flat_data]
                    dict = { 
                        'option_id': option_ids,
                        'ticker': ticker,
                        'strike': strike,
                        'call_put': call_put,
                        'expiry': expiry,
                        
                    }
                    df = pd.DataFrame(dict)
                    return df
        except Exception as e:
            print(e)


    async def reset_account(self, amount:str='4000'):
        account_id = await self.get_account_id()
        url = f"https://act.webullfintech.com/webull-paper-center/api/paper/1/acc/reset/{account_id}/{amount}"
        async with httpx.AsyncClient() as client:
            data = await client.get(url, headers=self.headers)
            print(data.text)
            print(data)

    async def get_contract_data(self, option_id:str='1044771278'):
        try:
            url=f"https://quotes-gw.webullfintech.com/api/quote/option/quotes/queryBatch?derivativeIds={option_id}"
            async with httpx.AsyncClient() as client:
                data = await client.get(url, headers=self.headers)
                if data.status_code == 200:
                    data = data.json()
                    data = WebullContractData(data)

                    return data
        except Exception as e:
            print(e)
    async def get_price_for_trade(self, option_id,db=None):
        try:
            price_query = f"""SELECT mid from master_all_two where option_id = '{option_id}'"""
            results = await db.fetch(price_query)
            df = pd.DataFrame(results, columns=['mid'])
            mid = df['mid'].to_list()[0]
            return mid
        except Exception as e:
            print(e)


    async def option_trade(self, quantity:int=1, action:str='BUY', option_id:str='1044771278'):
        try:
            price = await self.get_price_for_trade(option_id, db)
            url = f"https://act.webullfintech.com/webull-paper-center/api/paper/v1/order/optionPlace"
            payload = {"accountId":await self.get_account_id(),"orderType":"MKT","timeInForce":"GTC","quantity":quantity,"action":action,"tickerId":option_id,"lmtPrice":price,"paperId":1,"orders":[{"action":action,"quantity":quantity,"tickerId":option_id,"tickerType":"OPTION"}],"tickerType":"OPTION","optionStrategy":"Single","serialId": str(uuid.uuid4()) }

            async with httpx.AsyncClient() as client:
                data = await client.post(url, headers=self.headers, json=payload)
                if data.status_code == 200:
                    data = data.json()
                    print(data)

        except Exception as e:
            print(e)

