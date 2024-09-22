import sys
from pathlib import Path
import scipy.stats as stats
import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ...mapping import OPTIONS_EXCHANGES
indices_list = ["SPX", "SPXW", "NDX", "VIX", "VVIX"]
from scipy.stats import norm


class UniversalSnapshot:
    def __init__(self, results):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.risk_free_rate=5.37
        self.break_even_price = [i.get('session.break_even_price') for i in results]
        self.change = [i.get('session.change', None) for i in results]
        self.change_percent = [i.get('session.change_percent') for i in results]
        self.early_trading_change = [i.get('session.early_trading_change') for i in results]
        self.early_trading_change_percent = [i.get('session.early_trading_change_percent') for i in results]
        self.close = [i.get('session.close') for i in results]
        self.high = [i.get('session.high') for i in results]
        self.low = [i.get('session.low') for i in results]
        self.open = [i.get('session.open') for i in results]
        self.volume =[i.get('session.volume') for i in results]
        print(self.volume)
        self.prev_close = [i.get('session.previous_close') for i in results]


        self.strike = [i.get('details.strike_price') for i in results]
        self.expiry = [i.get('details.expiration_date') for i in results]
        self.contract_type = [i.get('details.contract_type') for i in results]
        self.exercise_style = [i.get('details.exercise_style') for i in results]
        self.ticker = [i.get('details.ticker') for i in results]

  
        self.theta_values = [i.get('greeks.theta') for i in results]
        self.gamma_values = [i.get('greeks.gamma') for i in results]
        self.vega_values = [i.get('greeks.vega') for i in results]
        self.delta_values = [i.get('greeks.delta') for i in results]

        
        self.implied_volatility = [i.get('implied_volatility') for i in results]
        self.open_interest = [i.get('open_interest') for i in results]

        #last_trade = [i.get('last_trade') for i in results]
        self.sip_timestamp = [i.get('last_trade.timestamp') for i in results]
        self.conditions = [i.get('last_trade.conditions') for i in results]
        self.trade_price = [i.get('last_trade.price') for i in results]
        self.trade_size = [i.get('last_trade.size') for i in results]
        self.exchange = [i.get('last_trade.exchange') for i in results]

    
        self.ask_prices = [i.get('last_quote.ask') for i in results]
        self.bid_prices = [i.get('last_qute.bid') for i in results]
        self.bid_sizes = [i.get('last_quote.bid_size') for i in results]
        self.ask_sizes = [i.get('last_quote.ask_size') for i in results]
        self.midpoints = [i.get('last_quote.midpoint') for i in results]

        self.name = [i.get('name') for i in results]
        self.market_status = [i.get('market_status') for i in results]
        self.ticker = [i.get('ticker') for i in results]
        self.type = [i.get('type') for i in results]


        self.change_to_breakeven = [i.get('underlying_asset.change_to_break_even') for i in results]
        self.underlying_ticker = [i.get('underlying_asset.ticker') for i in results]
        if self.underlying_ticker in indices_list:
            self.underlying_price = [i.get('underlying_asset.value') for i in results]
        else:
            self.underlying_price = [i.get('underlying_asset.price') for i in results]


        # expiry_series = pd.Series(self.expiry)
        # expiry_series = pd.to_datetime(expiry_series)
        # today = pd.Timestamp(datetime.today())
        # self.days_to_expiry = (expiry_series - today).dt.days
        # self.time_value = [p - s + k if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        # self.moneyness = [
        #     'Unknown' if u is None else (
        #         'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
        #             'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
        #         )
        #     ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        # ]


        self.data_dict = {
            
            'Change %': self.change_percent,
            'Close': self.close,
            'High': self.high,
            'Low': self.low,
            'Open': self.open,
            'Vol': self.volume,
            'Prev Close': self.prev_close,
            "cp": self.contract_type,
            'Style': self.exercise_style,
            'Exp': self.expiry,
            'Skew': self.strike,
            'Strike': self.strike,
            'Delta': self.delta,
            'Gamma': self.gamma,
            'Theta': self.theta,
            'Vega': self.vega,
            'IV': self.implied_volatility,
            'Ask': self.ask,
            'Ask Size': self.ask_size,
            'Bid': self.bid,
            'Bid Size': self.bid_size,
            'Mid': self.midpoint,
            'Timestamp': self.sip_timestamp,
            'Conditions': self.conditions,
            'Trade Price': self.trade_price,
            'Size': self.trade_size,
            'Exchange': self.exchange,
            'OI': self.open_interest,
            'Price': self.underlying_price,
            'Sym': self.underlying_ticker,
            'Name': self.name,
            'Ticker': self.ticker,
            'Types': self.type,
        }
        self.database_data_dict = {
            'days_to_expiry': self.days_to_expiry,
            'moneyness': self.moneyness,
            'time_value': self.time_value,
            'break_even_price': self.break_even_price,
            'change_percent': self.change_percent,
            'early_trading_change': self.early_trading_change,
            'early_trading_change_percent': self.early_trading_change_percent,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'open': self.open,
            'volume': self.volume,
            'prev_close': self.prev_close,
            "call_put": self.contract_type,
            'style': self.exercise_style,
            'expiry': self.expiry,
            'strike': self.strike,  # Keep this line and remove the 'Skew' entry
            'delta': self.delta,
            'gamma': self.gamma,
            'theta': self.theta,
            'vega': self.vega,
            'iv': self.implied_volatility,
            'ask': self.ask,
            'ask_size': self.ask_size,
            'bid': self.bid,
            'bid_size': self.bid_size,
            'mid': self.midpoint,
            'timestamp': self.sip_timestamp,
            'conditions': self.conditions,
            'trade_price': self.trade_price,
            'trade_size': self.trade_size,
            'trade_exchange': self.exchange,
            'oi': self.open_interest,
            'underlying_price': self.underlying_price,
            'underlying_symbol': self.underlying_ticker,
            'change_to_break_even': self.change_to_breakeven,
            'change': self.change,
            'name': self.name,
            'ticker': self.ticker,
        }


        self.skew_dict = { 
            "cp": self.contract_type,
            'iv': self.implied_volatility,
            'exp': self.expiry,
            'vol': self.volume,
            'oi': self.open_interest,
            'strike': self.strike,
}
        self.df = pd.DataFrame(self.data_dict)

        self.skew_df = pd.DataFrame(self.skew_dict)

    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value
    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration
class UniversalOptionSnapshot:
    def __init__(self, results):
        self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]
        self.risk_free_rate=5.37
        
        day = [i['day'] if 'day' in i else 0 for i in results]
        self.volume = [float(i.get('volume',0)) for i in day]
        self.high = [float(i.get('high',0)) for i in day]
        self.low = [float(i.get('low',0)) for i in day]
        self.vwap = [float(i.get('vwap',0)) for i in day]
        self.open = [float(i.get('open',0)) for i in day]
        self.close = [float(i.get('close',0)) for i in day]
        self.change_percent= [round(float(i.get('change_percent',0))) for i in day]



        details = [i['details'] if 'details' in i else 0 for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

        greeks = [i.get('greeks') for i in results]
        self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
        self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
        self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
        self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]


        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]
        self.risk_free_rate = [self.risk_free_rate] * len(self.underlying_price)
        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
        today = pd.Timestamp(datetime.today())
        
        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

        # Calculate days to expiry for each date in the series
        self.days_to_expiry_series = (expiry_series - today).days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
        self.option_velocity = [round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]

        # Option sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]

        # Liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]

        # Risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]

        # Greeks-balance score - curated - finished
        self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]

        # Options profit potential: FINAL - finished
        self.opp = [moneyness_score * oss * ltr * rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]

        iv_series = pd.Series(self.implied_volatility).dropna()
        self.iv_percentile = [round(x, 2) for x in iv_series.rank(pct=True)]

        # Vanna Calculations (with validation for iv, u, d)
        self.vanna = [(v * d / u) if v is not None and d is not None and u is not None and u > 0 else None 
                    for v, d, u in zip(self.vega, self.delta, self.underlying_price)]

        self.vanna_vega = [(d * (v / u)) if d is not None and v is not None and u is not None and u > 0 else None 
                        for d, v, u in zip(self.delta, self.vega, self.underlying_price)]

        self.vanna_delta = [(d / iv) if d is not None and iv is not None and iv > 0 else None 
                            for d, iv in zip(self.delta, self.implied_volatility)]


        # d1 Calculation (with validation for u, s, r, iv, t)
        d1 = [(np.log(u / s) + (r + (iv**2) / 2) * t) / (iv * np.sqrt(t)) if u is not None and u > 0 and s is not None and s > 0 and r is not None and iv is not None and iv > 0 and t > 0 else None 
            for u, s, r, iv, t in zip(self.underlying_price, self.strike, self.risk_free_rate, self.implied_volatility, self.days_to_expiry_series / 365)]

        # Color d1 Calculation (with validation)
        color_d1 = [(np.log(u / s) + (r + (iv**2) / 2) * (t / 365)) / (iv * np.sqrt(t / 365)) if u is not None and u > 0 and s is not None and s > 0 and r is not None and iv is not None and iv > 0 and t > 0 else None 
                    for u, s, r, iv, t in zip(self.underlying_price, self.strike, self.risk_free_rate, self.implied_volatility, self.days_to_expiry_series)]


        # Color Calculation (with validation for iv, t)
        self.color = [(g / (2 * t) * (1 + (r - 0.5 * iv**2) / (iv * np.sqrt(t)) * d1_val)) if g is not None and g > 0 and t > 0 and d1_val is not None and iv is not None and iv > 0 else None 
                    for g, t, r, iv, d1_val in zip(self.gamma, self.days_to_expiry_series / 365, self.risk_free_rate, self.implied_volatility, d1)]



        Nd1_prime = [norm.pdf(d) if d is not None else None for d in d1]

        # Charm Calculation (with validation for iv, t)
        self.charm = [((-nd1p * (r / (iv * np.sqrt(t))) - d * r / t)) if d is not None and nd1p is not None and r is not None and iv is not None and iv > 0 and t > 0 else None 
                    for nd1p, d, r, iv, t in zip(Nd1_prime, self.delta, self.risk_free_rate, self.implied_volatility, self.days_to_expiry_series / 365)]


        # Veta Calculation (with validation for u, t)
        self.veta = [-(u * nd1p * 0.5 / np.sqrt(t)) if u is not None and u > 0 and nd1p is not None and t > 0 else None 
                    for u, nd1p, t in zip(self.underlying_price, Nd1_prime, self.days_to_expiry_series / 365)]


        # Zomma Calculation (with validation for iv, u, d1)
        self.zomma = [(g * (d1_val / (iv * u))) if g is not None and g > 0 and d1_val is not None and iv is not None and iv > 0 and u is not None and u > 0 else None 
                    for g, d1_val, iv, u in zip(self.gamma, d1, self.implied_volatility, self.underlying_price)]

        
        # Speed Calculation (with input validation and edge case handling)
        self.speed = [
            (g * (2 * d)) / (u * iv * np.sqrt(t + 1e-6)) 
            if g is not None and d is not None and u is not None and u > 0 and iv is not None and iv > 0 and t > 0 
            else None 
            for g, d, u, iv, t in zip(self.gamma, d1, self.underlying_price, self.implied_volatility, self.days_to_expiry_series / 365)
        ]

        # Ultima Calculation (with input validation and edge case handling)
        self.ultima = [
            (v * (3 * d1**2 - 1) * u**2) / (max(iv**2, 1e-6)) 
            if v is not None and u is not None and u > 0 and iv is not None and iv > 0 and d1 is not None 
            else None 
            for v, u, iv, d1 in zip(self.vega, self.underlying_price, self.implied_volatility, d1)
        ]


        self.vomma = [
            (v * u**2 * d1 / max(iv, 1e-6)) if v is not None and d1 is not None and u is not None and iv is not None else None 
            for v, d1, u, iv in zip(self.vega, d1, self.underlying_price, self.implied_volatility)
        ]
        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'dte': self.days_to_expiry_series,
            'time_value': self.time_value,
            'moneyness': self.moneyness,
            'liquidity_score': self.liquidity_indicator,
            'cp': self.contract_type,
            'change_ratio': self.change_percent,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'intrinsic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'leverage_ratio': self.leverage_ratio,
            'vwap': self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'iv': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
            'return_on_risk': self.return_on_risk,
            'velocity': self.option_velocity,
            'sensitivity': self.oss,
            'greeks_balance': self.gbs,
            'opp': self.opp,
            'vanna': self.vanna,
            'vanna_delta': self.vanna_delta,
            'vanna_vega': self.vanna_vega,
            'vomma': self.vomma,
            'charm': self.charm,
            'veta': self.veta,
            'speed': self.speed,
            'zomma': self.zomma,
            'color': self.color,
            'ultima': self.ultima
        }

                # Create DataFrame from data_dict
        # Create DataFrame from data_dict
        self.df = pd.DataFrame(self.data_dict)

        # Calculate weighted Greeks by OI for calls and puts
        self.df['weighted_delta'] = self.df['delta'] * self.df['oi']
        self.df['weighted_gamma'] = self.df['gamma'] * self.df['oi']
        self.df['weighted_vega'] = self.df['vega'] * self.df['oi']
        self.df['weighted_theta'] = self.df['theta'] * self.df['oi']
        self.df['weighted_vanna'] = self.df['vanna'] * self.df['oi']
        self.df['weighted_charm'] = self.df['charm'] * self.df['oi']
        self.df['weighted_veta'] = self.df['veta'] * self.df['oi']
        self.df['weighted_speed'] = self.df['speed'] * self.df['oi']
        self.df['weighted_zomma'] = self.df['zomma'] * self.df['oi']
        self.df['weighted_color'] = self.df['color'] * self.df['oi']
        self.df['weighted_ultima'] = self.df['ultima'] * self.df['oi']

        # Introduce weighted_oi as a composite metric
        self.df['weighted_oi'] = (
            self.df['weighted_delta'] +
            self.df['weighted_gamma'] +
            self.df['weighted_vega'] +
            self.df['weighted_theta'] +
            self.df['weighted_vanna'] +
            self.df['weighted_charm'] +
            self.df['weighted_veta'] +
            self.df['weighted_speed'] +
            self.df['weighted_zomma'] +
            self.df['weighted_color'] +
            self.df['weighted_ultima']
        )

        # Calculate the relative position of the option's strike price to the current underlying price
        self.df['strike_distance'] = np.abs(self.df['strike'] - self.df['underlying_price'])

        # Adjust the momentum factor calculation
        self.df['momentum_factor'] = self.df['strike_distance'].apply(lambda x: 1 / x if x > 0 else 1e6)

        # Calculate momentum-adjusted Greeks using the momentum factor derived from strike distance
        self.df['momentum_delta'] = self.df['delta'] * self.df['momentum_factor']
        self.df['momentum_gamma'] = self.df['gamma'] * self.df['momentum_factor']
        self.df['momentum_vega'] = self.df['vega'] * self.df['momentum_factor']
        self.df['momentum_theta'] = self.df['theta'] * self.df['momentum_factor']
        self.df['momentum_vanna'] = self.df['vanna'] * self.df['momentum_factor']
        self.df['momentum_charm'] = self.df['charm'] * self.df['momentum_factor']
        self.df['momentum_veta'] = self.df['veta'] * self.df['momentum_factor']
        self.df['momentum_speed'] = self.df['speed'] * self.df['momentum_factor']
        self.df['momentum_zomma'] = self.df['zomma'] * self.df['momentum_factor']
        self.df['momentum_color'] = self.df['color'] * self.df['momentum_factor']
        self.df['momentum_ultima'] = self.df['ultima'] * self.df['momentum_factor']




        self.df['weighted_liquidity'] = (
            (self.df['bid_size'] + self.df['ask_size']) / (self.df['ask'] - self.df['bid']) * self.df['oi']
        )
        self.df['relative_iv'] = self.df['iv'] / self.df['vwap']  # Assuming vwap as a proxy for historical volatility
        self.df['gamma_exposure'] = self.df['gamma'] * self.df['oi']
        

        # Calculate returns as the percentage change in the underlying price
        self.df['returns'] = self.df['underlying_price'].pct_change()

        # Calculate skewness of returns
        self.df['returns_skewness'] = self.df['returns'].rolling(window=20).apply(stats.skew, raw=True)

        # Calculate skewness of implied volatility
        self.df['iv_skewness'] = self.df['iv'].rolling(window=20).apply(stats.skew, raw=True)


        # Separate DataFrames for calls and puts
        self.call_positioning = self.df[self.df['cp'] == 'call']
        self.put_positioning = self.df[self.df['cp'] == 'put']


        # Aggregate dealer positioning metrics for calls, incorporating volume and OI
        self.call_dealer_positioning = self.call_positioning.groupby('strike').agg({
            'weighted_delta': 'sum',
            'weighted_gamma': 'sum',
            'weighted_vega': 'sum',
            'weighted_theta': 'sum',
            'weighted_vanna': 'sum',
            'weighted_charm': 'sum',
            'weighted_veta': 'sum',
            'weighted_speed': 'sum',
            'weighted_zomma': 'sum',
            'weighted_color': 'sum',
            'weighted_ultima': 'sum',
            'weighted_oi': 'sum',
            'oi': 'sum',
            'vol': 'sum'
        }).reset_index()

        # Normalize by total open interest to get true positioning
        for column in ['weighted_delta', 'weighted_gamma', 'weighted_vega', 'weighted_theta', 'weighted_vanna',
                    'weighted_charm', 'weighted_veta', 'weighted_speed', 'weighted_zomma', 'weighted_color',
                    'weighted_ultima', 'weighted_oi']:
            self.call_dealer_positioning[column] = self.call_dealer_positioning[column] / self.call_dealer_positioning['oi']

        # Repeat the same for puts
        self.put_dealer_positioning = self.put_positioning.groupby('strike').agg({
            'weighted_delta': 'sum',
            'weighted_gamma': 'sum',
            'weighted_vega': 'sum',
            'weighted_theta': 'sum',
            'weighted_vanna': 'sum',
            'weighted_charm': 'sum',
            'weighted_veta': 'sum',
            'weighted_speed': 'sum',
            'weighted_zomma': 'sum',
            'weighted_color': 'sum',
            'weighted_ultima': 'sum',
            'weighted_oi': 'sum',
            'oi': 'sum',
            'vol': 'sum'
        }).reset_index()

        for column in ['weighted_delta', 'weighted_gamma', 'weighted_vega', 'weighted_theta', 'weighted_vanna',
                    'weighted_charm', 'weighted_veta', 'weighted_speed', 'weighted_zomma', 'weighted_color',
                    'weighted_ultima', 'weighted_oi']:
            self.put_dealer_positioning[column] = self.put_dealer_positioning[column] / self.put_dealer_positioning['oi']

    def save_conversations_to_jsonl(self, filename: str):
        """
        Save the options data as a JSONL file formatted for fine-tuning.

        :param filename: The name of the file to save the data to (e.g., 'options_data.jsonl').
        """
        conversations = []

        for index, row in self.df.iterrows():
            conversation = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an assistant specialized in financial data analysis and options trading."
                    },
                    {
                        "role": "user",
                        "content": f"Can you analyze the following option data?\n\n"
                                   f"Strike: {row['strike']}, Expiry: {row['expiry']}, Contract Type: {row['cp']}, "
                                   f"Open Interest: {row['oi']}, Implied Volatility: {row['iv']}, Delta: {row['delta']}, "
                                   f"Gamma: {row['gamma']}, Theta: {row['theta']}, Vega: {row['vega']}, "
                                   f"Moneyness: {row['moneyness']}, Time Value: {row['time_value']}, "
                                   f"Intrinsic Value: {row['intrinsic_value']}, Extrinsic Value: {row['extrinsic_value']}."
                    },
                    {
                        "role": "assistant",
                        "content": f"The option is {row['moneyness']} with a strike price of {row['strike']} and "
                                   f"an expiration date of {row['expiry']}. The current implied volatility is "
                                   f"{row['iv']}, and the delta is {row['delta']}, indicating that the option's "
                                   f"price will move {row['delta'] * 100:.2f}% for every 1% change in the underlying asset's price."
                    }
                ]
            }
            conversations.append(conversation)

        # Save the conversations as a JSONL file
        with open(filename, 'w') as file:
            for conversation in conversations:
                file.write(json.dumps(conversation) + '\n')
    def get_call_dealer_positioning(self):
        """
        Method to get call dealer positioning as a DataFrame.
        """
        return self.call_dealer_positioning

    def get_put_dealer_positioning(self):
        """
        Method to get put dealer positioning as a DataFrame.
        """
        return self.put_dealer_positioning
    def __repr__(self) -> str:
        return f"UniversalOptionSnapshot(break_even={self.break_even}, \
                implied_volatility={self.implied_volatility},\
                open_interest ={self.open_interest}, \
                change={self.exchange}, \
                expiry={self.expiry}, \
                ticker={self.ticker} \
                contract_type={self.contract_type}, \
                exercise_style={self.exercise_style}, \
                theta={self.theta}, \
                delta={self.delta}, \
                gamma={self.gamma}, \
                vega={self.vega}, \
                sip_timestamp={self.sip_timestamp}, \
                conditions={self.conditions}, \
                trade_price={self.trade_price}, \
                trade_size={self.trade_size}, \
                exchange={self.exchange}, \
                ask={self.ask}, \
                bid={self.bid}, \
                bid_size={self.bid_size}, \
                ask_size={self.ask_size}, \
                midpoint={self.midpoint}, \
                change_to_breakeven={self.change_to_breakeven}, \
                underlying_price={self.underlying_price}, \
                underlying_ticker={self.underlying_ticker})"

    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value

    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration

class CallsOrPuts:
    def __init__(self, data):
        self.cfi = [i['cfi'] if 'cfi' in i else None for i in data]
        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in data]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in data]
        self.expiration_date = [i['expiration_date'] if 'expiration_date' in i else None for i in data]
        self.primary_exchange = [i['primary_exchange'] if 'primary_exchange' in i else None for i in data]
        self.shares_per_contract = [i['shares_per_contract'] if 'shares_per_contract' in i else None for i in data]
        self.strike_price = [i['strike_price'] if 'strike_price' in i else None for i in data]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in data]
        self.underlying_ticker = [i['underlying_ticker'] if 'underlying_ticker' in i else None for i in data]


        self.data_dict = { 
            'ticker': self.ticker,
            'strike': self.strike_price,
            'expiry': self.expiration_date

        }


        self.df = pd.DataFrame(self.data_dict).sort_values(by='expiry')

class MultipleUniversalOptionSnapshot:
    def __init__(self, results):
        self.break_even = results.get('break_even_price', None)
     
        self.implied_volatility = results.get('implied_volatility', None)
        self.open_interest = results.get('open_interest', None)

        day = results.get('day', None)
        self.volume = day.get('volume', None)
        self.high = day.get('high', None)
        self.low = day.get('low', None)
        self.vwap = day.get('vwap', None)
        self.open = day.get('open', None)
        self.close = day.get('close', None)




        details = results.get('details', None)
        self.strike = details.get('strike_price', None)
        self.expiry =  details.get('expiration_date', None)
        self.contract_type =  details.get('contract_type', None)
        self.exercise_style =  details.get('exercise_style', None)
        self.ticker =  details.get('ticker', None)

        greeks = results.get('greeks', None)
        self.theta = greeks.get('theta', None)
        self.delta = greeks.get('delta', None)
        self.gamma = greeks.get('gamma', None)
        self.vega = greeks.get('vega', None)


        last_trade = results.get('last_trade', None)
        self.sip_timestamp = last_trade.get('sip_timestamp', None)
        self.conditions = last_trade.get('conditions', None)
        self.trade_price = last_trade.get('price', None)
        self.trade_size = last_trade.get('size', None)
        self.exchange = last_trade.get('exchange', None)

        last_quote = results.get('last_quote', None)
        self.ask = last_quote.get('ask', None)
        self.bid = last_quote.get('bid', None)
        self.bid_size = last_quote.get('bid_size', None)
        self.ask_size = last_quote.get('ask_size', None)
        self.midpoint = last_quote.get('midpoint', None)


        underlying_asset = results.get('underlying_asset', None)
        self.change_to_breakeven = underlying_asset.get('change_to_breakeven', None)
        self.underlying_price = underlying_asset.get('underlying_price', None)
        self.underlying_ticker = underlying_asset.get('underlying_ticker', None)

        self.data_dict = {
            'strike': self.strike,
            'exp': self.expiry,
            'type': self.contract_type,
            'exercise_style': self.exercise_style,
            'ticker': self.ticker,
            'theta': self.theta,
            'delta': self.delta,
            'gamma': self.gamma,
            'vega': self.vega,
            'sip_timestamp': self.sip_timestamp,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'vwap':self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'Size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'IV': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'entryCost': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'price': self.underlying_price,
            'sym': self.underlying_ticker
        }

        self.df = pd.DataFrame(self.data_dict)





class UniversalOptionSnapshot2:
    def __init__(self, results):

        session = [i['session'] if 'session' in i else 0 for i in results]


        self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]

        day = [i['day'] if 'day' in i else 0 for i in results]
        self.volume = [float(i.get('volume',0)) for i in day]
        self.high = [float(i.get('high',0)) for i in day]
        self.low = [float(i.get('low',0)) for i in day]
        self.vwap = [float(i.get('vwap',0)) for i in day]
        self.open = [float(i.get('open',0)) for i in day]
        self.close = [float(i.get('close',0)) for i in day]
        self.change_percent= [round(float(i.get('change_percent',0))*100,2) for i in day]



        details = [i['details'] for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

        greeks = [i.get('greeks') for i in results]
        self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
        self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
        self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
        self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        #self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]
        #self.exchange = [OPTIONS_EXCHANGES.get(i) for i in self.exchange]

        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]

        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
        today = pd.Timestamp(datetime.today())
        
        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

        # Calculate days to expiry for each date in the series
        self.days_to_expiry_series = (expiry_series - today).days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
        self.option_velocity =[round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]
        #option_sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]
        #liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]
        #risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]
        #greeks-balance score - curated - finished
        self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]
        #options profit potential: FINAL - finished
        self.opp = [moneyness_score*oss*ltr*rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]



                


















        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'dte': self.days_to_expiry_series,
            'time_value': self.time_value,
            'moneyness': self.moneyness,
            'liquidity_score': self.liquidity_indicator,
            "cp": self.contract_type,
            "change_ratio": self.change_percent,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'intrinstic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'leverage_ratio': self.leverage_ratio,
            'vwap':self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'iv': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
            'return_on_risk': self.return_on_risk,
            'velocity': self.option_velocity,
            'sensitivity': self.oss,
            'greeks_balance': self.gbs,
            'opp': self.opp
            
        }


        # Create DataFrame from data_dict
        self.df = pd.DataFrame(self.data_dict)
    def __repr__(self) -> str:
        return f"UniversalOptionSnapshot(break_even={self.break_even}, \
                implied_volatility={self.implied_volatility},\
                open_interest ={self.open_interest}, \
                change={self.exchange}, \
                expiry={self.expiry}, \
                ticker={self.ticker} \
                contract_type={self.contract_type}, \
                exercise_style={self.exercise_style}, \
                theta={self.theta}, \
                delta={self.delta}, \
                gamma={self.gamma}, \
                vega={self.vega}, \
                sip_timestamp={self.sip_timestamp}, \
                conditions={self.conditions}, \
                trade_price={self.trade_price}, \
                trade_size={self.trade_size}, \
                exchange={self.exchange}, \
                ask={self.ask}, \
                bid={self.bid}, \
                bid_size={self.bid_size}, \
                ask_size={self.ask_size}, \
                midpoint={self.midpoint}, \
                change_to_breakeven={self.change_to_breakeven}, \
                underlying_price={self.underlying_price}, \
                underlying_ticker={self.underlying_ticker})"
    
    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value
    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration
        


class OptionData:
    def __init__(self, results):
        self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]
        self.name = [i.get('name') for i in results]
        session = [i.get('session', {}) for i in results]
        print(session)
        self.volume = [float(session_data.get('volume', 0)) for session_data in session]
        self.high = [float(session_data.get('high', 0)) for session_data in session]
        self.low = [float(session_data.get('low', 0)) for session_data in session]
        self.vwap = [float(session_data.get('vwap', 0)) for session_data in session]
        self.open = [float(session_data.get('open', 0)) for session_data in session]
        self.close = [float(session_data.get('close', 0)) for session_data in session]
        self.change_percent = [round(float(session_data.get('change_percent', 0)),2) for session_data in session]
        self.early_change_percent = [round(float(session_data.get('early_trading_change_percent', 0)),2) for session_data in session]
        self.late_change_percent = [round(float(session_data.get('late_trading_change_percent', 0)),2) for session_data in session]
        details = [i.get('details', {}) for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in results]

        greeks = [i.get('greeks', {}) for i in results]
        self.theta = [round(float(i.get('theta', 0)), 4) for i in greeks if i is not None and i.get('theta') is not None]
        self.delta = [round(float(i.get('delta', 0)), 4) for i in greeks if i is not None and i.get('delta') is not None]
        self.gamma = [round(float(i.get('gamma', 0)), 4) for i in greeks if i is not None and i.get('gamma') is not None]
        self.vega = [round(float(i.get('vega', 0)), 4) for i in greeks if i is not None and i.get('vega') is not None]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]
        self.exchange = [OPTIONS_EXCHANGES.get(i) for i in self.exchange]

        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]

        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
        today = pd.Timestamp(datetime.today())
        
        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

        # Calculate days to expiry for each date in the series
        self.days_to_expiry_series = (expiry_series - today).days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
        self.option_velocity =[round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]
        #option_sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]
        #liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]
        #risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]
        #greeks-balance score - curated - finished
        self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]
        #options profit potential: FINAL - finished
        self.opp = [moneyness_score*oss*ltr*rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]

        self.vol_oi_ratio = [
            f"{iv / oi:.6f}" if oi and iv is not None else None 
            for iv, oi in zip(self.implied_volatility, self.open_interest)
        ]




        total_oi = sum(filter(None, self.open_interest))  # Sum of all non-None open interest values
        self.weighted_iv = round(sum(iv * oi for iv, oi in zip(self.implied_volatility, self.open_interest) if iv is not None and oi is not None) / total_oi, 6)

  
        self.avg_theta_decay = round(sum(filter(None, self.theta)) / len(self.theta), 2)

        # IV Percentile
        iv_series = pd.Series(self.implied_volatility).dropna()
        self.iv_percentile = [round(x, 2) for x in iv_series.rank(pct=True)]













        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'dte': self.days_to_expiry_series,
            'time_value': self.time_value,
            'moneyness': self.moneyness,
            'liquidity_score': self.liquidity_indicator,
            "cp": self.contract_type,
            "change_percent": self.change_percent,
            "late_change_percent": self.late_change_percent,
            "early_change_percent": self.early_change_percent,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'intrinsic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'leverage_ratio': self.leverage_ratio,
            'vwap':self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'iv': self.implied_volatility,
            'iv_percentile': self.iv_percentile,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
            'return_on_risk': self.return_on_risk,
            'velocity': self.option_velocity,
            'sensitivity': self.oss,
            'greeks_balance': self.gbs,
            'opp': self.opp,
            'vol_oi_ratio': self.vol_oi_ratio,

            
        }


        # Check and correct the data lengths
        for key, value in self.data_dict.items():
            if len(value) < 25:
                # Fill in missing data with None for keys with length 24
                self.data_dict[key] += [None] * (25 - len(value))

        # Create the DataFrame
        self.as_dataframe = self.ensure_uniform_length(self.data_dict)
    def ensure_uniform_length(self, data_dict):
        # Determine the maximum length among all lists in the dictionary
        max_length = max(len(value) for value in data_dict.values())

        # Pad shorter lists with None to match the maximum length
        for key, value in data_dict.items():
            additional_length = max_length - len(value)
            if additional_length > 0:
                data_dict[key] = value + [None] * additional_length

        # Now, all lists in data_dict have the same length and can be safely converted to a DataFrame
        return pd.DataFrame(data_dict)
    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value
    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.as_dataframe.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration
    def pad_data(self, target_length=250, pad_value=None):
        for key, value in self.data_dict.items():
            if isinstance(value, list) and len(value) < target_length:
                additional_length = target_length - len(value)
                self.data_dict[key].extend([pad_value] * additional_length)
    def check_data_consistency(self):
        lengths = {key: len(value) for key, value in self.data_dict.items() if isinstance(value, list)}
        if len(set(lengths.values())) != 1:
            # Find and print out the inconsistencies
            print("Inconsistent lengths found in the following fields:")
            for key, length in lengths.items():
                print(f"{key}: Length {length}")
        else:
            print("All lists are of the same length.")