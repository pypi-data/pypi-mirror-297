import re
import pandas as pd
import asyncio
import time
from fudstop.apis.webull.webull_trading import WebullTrading
trading = WebullTrading()
import httpx
import numpy as np

class WebullTA:
    def __init__(self):
        self.intervals_to_scan = ['m5', 'm30', 'm60', 'm120', 'm240', 'd', 'w', 'm']  # Add or remove intervals as needed
    def parse_interval(self,interval_str):
        pattern = r'([a-zA-Z]+)(\d+)'
        match = re.match(pattern, interval_str)
        if match:
            unit = match.group(1)
            value = int(match.group(2))
            if unit == 'm':
                return value * 60
            elif unit == 'h':
                return value * 3600
            elif unit == 'd':
                return value * 86400
            else:
                raise ValueError(f"Unknown interval unit: {unit}")
        else:
            raise ValueError(f"Invalid interval format: {interval_str}")


    async def async_get_td9(self, ticker, interval, headers):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPXW'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            



            tickerid = await trading.get_webull_id(ticker)
            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())

            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query?tickerIds={tickerid}&type={interval}&timestamp={timeStamp}&count=800&extendTrading=1'

            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval)

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']
                    if data is not None:
                        parsed_data = []
                        for entry in data:
                            values = entry.split(',')
                            if values[-1] == 'NULL':
                                values = values[:-1]
                            parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                        
                        sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                        
                        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                        
                        df = pd.DataFrame(sorted_data, columns=columns)
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)
                        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                        df['Ticker'] = ticker
                        df['timespan'] = timespan


                        return df
                    
        except Exception as e:
            print(e)


    # Simulating async TA data fetching for each timeframe
    async def fetch_ta_data(self, timeframe, data):
        # Simulate an async operation to fetch data (e.g., from an API)

        return data.get(timeframe, {})
    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.

        Parameters:
        - df (pd.DataFrame): DataFrame containing market data with columns ['High', 'Low', 'Open', 'Close', 'Volume', 'Vwap', 'Timestamp']
        - interval (str): Resampling interval based on custom mappings (e.g., 'm5', 'm30', 'd', 'w', 'm')

        Returns:
        - pd.DataFrame: DataFrame with additional columns indicating detected candlestick patterns and their bullish/bearish nature
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
            # Add more mappings as needed
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # Since we want the most recent data first, reverse the DataFrame
        patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df

    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv

    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # No need to reverse the DataFrame; keep it in ascending order
        # patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df.reset_index()
   
    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv
    def detect_patterns(self, ohlcv):
        # Initialize pattern columns
        patterns = ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                     'gravestone_doji', 'butterfly_doji', 'harami_cross', 'tweezer_top', 'tweezer_bottom']



        for pattern in patterns:
            ohlcv[pattern] = False

        ohlcv['signal'] = None  # To indicate Bullish or Bearish signal

        # Iterate over the DataFrame to detect patterns
        for i in range(len(ohlcv)):
            curr_row = ohlcv.iloc[i]
            prev_row = ohlcv.iloc[i - 1] if i >= 1 else None
            prev_prev_row = ohlcv.iloc[i - 2] if i >= 2 else None



            uptrend = self.is_uptrend(ohlcv, i)
            downtrend = self.is_downtrend(ohlcv, i)


            # Single-candle patterns
            if downtrend and self.is_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if downtrend and self.is_inverted_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'inverted_hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_hanging_man(curr_row):
                ohlcv.at[ohlcv.index[i], 'hanging_man'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if uptrend and self.is_shooting_star(curr_row):
                ohlcv.at[ohlcv.index[i], 'shooting_star'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if downtrend and self.is_dragonfly_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'dragonfly_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_gravestone_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'gravestone_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

            # Two-candle patterns
            if prev_row is not None:
                if downtrend and self.is_bullish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_bullish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_piercing_line(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'piercing_line'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_dark_cloud_cover(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'dark_cloud_cover'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_tweezer_bottom(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_bottom'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_tweezer_top(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_top'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_harami_cross(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'harami_cross'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'neutral'

            # Three-candle patterns
            if prev_row is not None and prev_prev_row is not None:
                if downtrend and self.is_morning_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'morning_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_evening_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'evening_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_white_soldiers(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_white_soldiers'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_black_crows(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_black_crows'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_inside_up(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_up'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_inside_down(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_down'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if self.is_abandoned_baby(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'abandoned_baby'] = True
                    if curr_row['Close'] > prev_row['Close']:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                    else:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_rising_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'rising_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_falling_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'falling_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

        return ohlcv
    def is_gravestone_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and lower_shadow == 0 and upper_shadow > 2 * body_length
        
    def is_three_inside_up(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bearish and second_bullish and third_bullish and
                prev_row['Open'] > prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Open'] and
                curr_row['Close'] > prev_prev_row['Open'])


    def is_tweezer_top(self, prev_row, curr_row):
        return (prev_row['High'] == curr_row['High']) and (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open'])

    def is_tweezer_bottom(self, prev_row, curr_row):
        return (prev_row['Low'] == curr_row['Low']) and (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open'])

    def is_dragonfly_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and upper_shadow == 0 and lower_shadow > 2 * body_length


    def is_uptrend(self, df: pd.DataFrame, length: int = 5) -> bool:
        """Check if the dataframe shows an uptrend over the specified length."""
        try:
            for i in range(1, length):
                if df['Close'].iloc[i] <= df['Close'].iloc[i - 1]:
                    return False
            return True
        except Exception as e:
            print(e)
            return False
    def is_downtrend(self, df: pd.DataFrame, length: int = 5) -> bool:
        """Check if the dataframe shows a downtrend over the specified length."""
        try:
            for i in range(1, length):
                if df['Close'].iloc[i] >= df['Close'].iloc[i - 1]:
                    return False
            return True
        except Exception as e:
            print(e)
            return False

    def is_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return (lower_shadow >= 2 * body_length) and (upper_shadow <= body_length)

    def is_inverted_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Open'], row['Close'])
        lower_shadow = min(row['Open'], row['Close']) - row['Low']
        return (upper_shadow >= 2 * body_length) and (lower_shadow <= body_length)

    def is_hanging_man(self, row):
        return self.is_hammer(row)

    def is_shooting_star(self, row):
        return self.is_inverted_hammer(row)

    def is_doji(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range

    def is_bullish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_bearish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bullish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] > prev_row['Close']) and (curr_row['Open'] < curr_row['Close']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bearish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] < prev_row['Close']) and (curr_row['Open'] > curr_row['Close']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_morning_star(self,prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bullish = curr_row['Close'] > curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_above_first_mid = curr_row['Close'] > first_midpoint
        return first_bearish and second_small_body and third_bullish and third_close_above_first_mid

    def is_evening_star(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bearish = curr_row['Close'] < curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_below_first_mid = curr_row['Close'] < first_midpoint
        return first_bullish and second_small_body and third_bearish and third_close_below_first_mid

    def is_piercing_line(self,prev_row, curr_row):
        first_bearish = prev_row['Close'] < prev_row['Open']
        second_bullish = curr_row['Close'] > curr_row['Open']
        open_below_prev_low = curr_row['Open'] < prev_row['Low']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_above_prev_mid = curr_row['Close'] > prev_midpoint
        return first_bearish and second_bullish and open_below_prev_low and close_above_prev_mid
        
    def has_gap_last_4_candles(self, ohlcv, index):
        """
        Checks if there's a gap within the last 4 candles, either up or down.
        A gap up occurs when the current open is higher than the previous close,
        and a gap down occurs when the current open is lower than the previous close.
        
        :param ohlcv: The OHLCV dataframe with historical data.
        :param index: The current index in the dataframe.
        :return: Boolean value indicating whether a gap exists in the last 4 candles.
        """
        # Ensure there are at least 4 candles to check
        if index < 3:
            return False

        # Iterate through the last 4 candles
        for i in range(index - 3, index):
            curr_open = ohlcv.iloc[i + 1]['Open']
            prev_close = ohlcv.iloc[i]['Close']
            
            # Check for a gap (either up or down)
            if curr_open > prev_close or curr_open < prev_close:
                return True  # A gap is found

        return False  # No gap found in the last 4 candles

    def is_abandoned_baby(self, prev_prev_row, prev_row, curr_row):
        # Bullish Abandoned Baby
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        doji = self.is_doji(prev_row)
        third_bullish = curr_row['Close'] > curr_row['Open']
        
        # Check for gaps
        gap_down = prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Low']
        gap_up = curr_row['Open'] > prev_row['Close'] and curr_row['Close'] > prev_row['High']
        
        return first_bearish and doji and third_bullish and gap_down and gap_up

    def is_harami_cross(self, prev_row, curr_row):
        # Harami Cross is a special form of Harami with the second candle being a Doji
        return self.is_bullish_harami(prev_row, curr_row) and self.is_doji(curr_row)

    def is_rising_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Rising Three Methods (Bullish Continuation)
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        small_bearish = prev_row['Close'] < prev_row['Open'] and prev_row['Close'] > prev_prev_row['Open']
        final_bullish = curr_row['Close'] > curr_row['Open'] and curr_row['Close'] > prev_prev_row['Close']
        
        return first_bullish and small_bearish and final_bullish

    def is_falling_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Falling Three Methods (Bearish Continuation)
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        small_bullish = prev_row['Close'] > prev_row['Open'] and prev_row['Close'] < prev_prev_row['Open']
        final_bearish = curr_row['Close'] < curr_row['Open'] and curr_row['Close'] < prev_prev_row['Close']
        
        return first_bearish and small_bullish and final_bearish

    def is_three_inside_down(self, prev_prev_row, prev_row, curr_row):
        # Bearish reversal pattern
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        
        return (first_bullish and second_bearish and third_bearish and
                prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] > prev_prev_row['Open'] and
                curr_row['Close'] < prev_prev_row['Open'])
    def is_dark_cloud_cover(self,prev_row, curr_row):
        first_bullish = prev_row['Close'] > prev_row['Open']
        second_bearish = curr_row['Close'] < curr_row['Open']
        open_above_prev_high = curr_row['Open'] > prev_row['High']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_below_prev_mid = curr_row['Close'] < prev_midpoint
        return first_bullish and second_bearish and open_above_prev_high and close_below_prev_mid

    def is_three_white_soldiers(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bullish and second_bullish and third_bullish and
                prev_row['Open'] < prev_prev_row['Close'] and curr_row['Open'] < prev_row['Close'] and
                prev_row['Close'] > prev_prev_row['Close'] and curr_row['Close'] > prev_row['Close'])

    def is_three_black_crows(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        return (first_bearish and second_bearish and third_bearish and
                prev_row['Open'] > prev_prev_row['Close'] and curr_row['Open'] > prev_row['Close'] and
                prev_row['Close'] < prev_prev_row['Close'] and curr_row['Close'] < prev_row['Close'])
    

    async def get_ta(self, ticker, headers):
        try:
            # Dictionary to collect patterns for each interval
            ticker_patterns = {}

            # Iterate through each interval for the ticker
            for interval in self.intervals_to_scan:
                # Fetch the DataFrame asynchronously
                df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)

                # Call the asynchronous scan_candlestick_patterns function
                patterns_df = await self.async_scan_candlestick_patterns(df, interval)

                # Since the DataFrame is in ascending order (oldest first), the last row is the most recent data
                last_row = patterns_df.iloc[-1]

                # Identify patterns that are True
                pattern_columns = ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                    'gravestone_doji', 'butterfly_doji', 'harami_cross', 'tweezer_top', 'tweezer_bottom']

                true_patterns = [pattern for pattern in pattern_columns if last_row[pattern]]

                if true_patterns:
                    signal = last_row['signal']
                    # Store the patterns and signal for this interval
                    ticker_patterns[interval] = {
                        'patterns': true_patterns,
                        'signal': signal
                    }

            # Return the ticker patterns
            return ticker_patterns

        except Exception as e:
            print(f"Exception in processing {ticker}: {e}")
            return None
        
    async def detect_ascending_triangle(self, df):
        """
        Detects ascending triangle patterns in a stock price DataFrame across multiple timespans.

        Parameters:
        - df (pd.DataFrame): DataFrame containing stock data with at least 'Timestamp', 'Close', 'High', 'Low', 'timespan', and 'Ticker' columns.

        Returns:
        - pd.DataFrame: Original DataFrame with an additional 'AscendingTriangle' column indicating pattern detection.
        """
        try:
            import numpy as np
            from scipy.signal import find_peaks

            # Define parameter mappings based on timespans
            timespan_params = {
                'm5':    {'window': 20,  'threshold': 0.005},
                'm30':   {'window': 25,  'threshold': 0.007},
                'm60':   {'window': 30,  'threshold': 0.007},
                'm120':  {'window': 40,  'threshold': 0.008},
                'm240':  {'window': 50,  'threshold': 0.008},
                'd':     {'window': 60,  'threshold': 0.009},
                'w':     {'window': 70,  'threshold': 0.01},
                'm':     {'window': 80,  'threshold': 0.012}
            }

            # Initialize the 'AscendingTriangle' column
            df['AscendingTriangle'] = False

            # Ensure the DataFrame is sorted by 'Ticker', 'timespan', and 'Timestamp' in ascending order
            df = df.sort_values(['Ticker', 'timespan', 'Timestamp']).reset_index(drop=True)

            # Group the DataFrame by 'Ticker' and 'timespan'
            grouped = df.groupby(['Ticker', 'timespan'])

            for (ticker, timespan), group in grouped:
                params = timespan_params.get(timespan, {'window': 30, 'threshold': 0.005})
                window = params['window']
                threshold = params['threshold']

                if len(group) < window:
                    continue

                high_prices = group['High'].values
                low_prices = group['Low'].values
                indices = group.index

                # Use the last 'window' data points
                recent_highs = high_prices[-window:]
                recent_lows = low_prices[-window:]
                recent_indices = indices[-window:]

                # Find peaks in recent_highs (horizontal resistance)
                peaks, _ = find_peaks(recent_highs, distance=window//5)
                if len(peaks) < 2:
                    continue

                # Check if peak prices are within threshold (forming horizontal resistance)
                peak_prices = recent_highs[peaks]
                resistance_level = np.mean(peak_prices)
                resistance_diff = np.abs(peak_prices - resistance_level) / resistance_level

                if np.max(resistance_diff) < threshold:
                    # Find troughs in recent_lows (ascending support)
                    troughs, _ = find_peaks(-recent_lows, distance=window//5)
                    if len(troughs) < 2:
                        continue

                    # Check if troughs are ascending
                    trough_prices = recent_lows[troughs]
                    x = np.arange(len(trough_prices))
                    slope, _ = np.polyfit(x, trough_prices, 1)

                    if slope > 0:
                        # All conditions met, mark 'AscendingTriangle' at the latest index
                        df.at[indices[-1], 'AscendingTriangle'] = True

            return df
        except Exception as e:
            print(f"Error in detect_ascending_triangle: {e}")
            return df

    async def detect_rounding_bottom_dynamic(self, df):
        """
        Detects rounding bottom patterns in a stock price DataFrame across multiple timespans.

        Parameters:
        - df (pd.DataFrame): DataFrame containing stock data with at least 'Timestamp', 'Close', 'timespan', and 'Ticker' columns.

        Returns:
        - pd.DataFrame: Original DataFrame with an additional 'RoundingBottom' column indicating pattern detection.
        """
        try:
            # Define parameter mappings based on timespans
            timespan_params = {
                'm5':    {'window': 10,  'threshold': 0.002},  # Short-term patterns with smaller windows
                'm30':   {'window': 15,  'threshold': 0.003},
                'm60':   {'window': 20,  'threshold': 0.003},
                'm120':  {'window': 30,  'threshold': 0.004},
                'm240':  {'window': 40,  'threshold': 0.004},  # Higher volatility might need larger thresholds
                'd':     {'window': 50,  'threshold': 0.005},  # Daily chart requires a wider window to capture significant trends
                'w':     {'window': 60,  'threshold': 0.007},  # Weekly patterns require even wider windows and higher thresholds
                'm':     {'window': 80,  'threshold': 0.01}    # Monthly charts might need the largest window/threshold
            }

            # Initialize the 'RoundingBottom' column
            df['RoundingBottom'] = False

            # Ensure the DataFrame is sorted by 'Ticker', 'timespan', and 'Timestamp' in ascending order
            df = df.sort_values(['Ticker', 'timespan', 'Timestamp']).reset_index(drop=True)

            # Group the DataFrame by 'Ticker' and 'timespan'
            grouped = df.groupby(['Ticker', 'timespan'])

            for (ticker, timespan), group in grouped:
                params = timespan_params.get(timespan, {'window': 20, 'threshold': 0.005})
                window = params['window']
                threshold = params['threshold']

                close = group['Close'].values
                indices = group.index

                # Define the number of candles to confirm the uptrend after the trough
                trend_confirm_candles = 1  # Mark the second candle after trough

                # Iterate over the group to find troughs
                # Start from 'window' to len(close) - trend_confirm_candles to avoid index errors
                for i in range(window, len(close) - trend_confirm_candles):
                    # Define the current trough candidate
                    current_trough = close[i]

                    # Define the window for trough comparison
                    trough_window = close[i - window:i + window + 1]

                    # Check if current_trough is the minimum in the trough_window
                    if current_trough == min(trough_window):
                        # Ensure left side is in a downtrend (last ten candles decreasing)
                        left_trend = close[i - 10:i]
                        if left_trend[1] < left_trend[0]:
                            # Ensure right side is in an uptrend (next two candles increasing)
                            right_trend = close[i + 1:i + trend_confirm_candles + 1]
                            is_uptrend = all(right_trend[j] > right_trend[j - 1] for j in range(1, len(right_trend)))

                            if is_uptrend:
                                # Calculate percentage increase from trough to confirmation candle
                                confirmation_price = close[i + 1]  # second candle after trough
                                pct_increase = (confirmation_price - current_trough) / current_trough

                                if pct_increase >= threshold:
                                    # Mark 'RoundingBottom' at confirmation candle
                                    confirmation_index = i + 2  # first candle after trough
                                    if confirmation_index < len(close):
                                        df.at[indices[confirmation_index], 'RoundingBottom'] = True

            return df
        except Exception as e:
            print(f"Error in detect_rounding_bottom_dynamic: {e}")
            return df  # Return the original df in case of error


    async def detect_rounding_top_dynamic(self, df):
        """
        Detects rounding top patterns in a stock price DataFrame across multiple timespans.

        Parameters:
        - df (pd.DataFrame): DataFrame containing stock data with at least 'Timestamp', 'Close', 'timespan', and 'Ticker' columns.

        Returns:
        - pd.DataFrame: Original DataFrame with an additional 'RoundingTop' column indicating pattern detection.
        """
        try:
            # Define parameter mappings based on timespans
            timespan_params = {
                'm5':    {'window': 10,  'threshold': 0.002},  # Short-term patterns with smaller windows
                'm30':   {'window': 15,  'threshold': 0.003},
                'm60':   {'window': 20,  'threshold': 0.003},
                'm120':  {'window': 30,  'threshold': 0.004},
                'm240':  {'window': 40,  'threshold': 0.004},  # Higher volatility might need larger thresholds
                'd':     {'window': 50,  'threshold': 0.005},  # Daily chart requires a wider window to capture significant trends
                'w':     {'window': 60,  'threshold': 0.007},  # Weekly patterns require even wider windows and higher thresholds
                'm':     {'window': 80,  'threshold': 0.01}    # Monthly charts might need the largest window/threshold
            }

            # Initialize the 'RoundingTop' column
            df['RoundingTop'] = False

            # Ensure the DataFrame is sorted by 'Ticker', 'timespan', and 'Timestamp' in ascending order
            df = df.sort_values(['Ticker', 'timespan', 'Timestamp']).reset_index(drop=True)

            # Group the DataFrame by 'Ticker' and 'timespan'
            grouped = df.groupby(['Ticker', 'timespan'])

            for (ticker, timespan), group in grouped:
                params = timespan_params.get(timespan, {'window': 20, 'threshold': 0.005})
                window = params['window']
                threshold = params['threshold']

                close = group['Close'].values
                indices = group.index

                # Define the number of candles to confirm the downtrend after the peak
                trend_confirm_candles = 1  # User wants to mark the second candle after peak

                # Iterate over the group to find peaks
                # Start from 'window' to len(close) - trend_confirm_candles to avoid index errors
                for i in range(window, len(close) - trend_confirm_candles):
                    # Define the current peak candidate
                    current_peak = close[i]

                    # Define the window for peak comparison
                    peak_window = close[i - window:i + window + 1]

                    # Check if current_peak is the maximum in the peak_window
                    if current_peak == max(peak_window):
                        # Ensure left side is in an uptrend (last ten candles increasing)
                        left_trend = close[i - 10:i]
                        if left_trend[1] > left_trend[0]:
                            # Ensure right side is in a downtrend (next two candles decreasing)
                            right_trend = close[i + 1:i + trend_confirm_candles + 1]
                            is_downtrend = all(right_trend[j] < right_trend[j - 1] for j in range(1, len(right_trend)))

                            if is_downtrend:
                                # Calculate percentage decrease from peak to confirmation candle
                                confirmation_price = close[i + 1]  # second candle after peak
                                pct_decrease = (current_peak - confirmation_price) / current_peak

                                if pct_decrease >= threshold:
                                    # Mark 'RoundingTop' at confirmation candle
                                    confirmation_index = i + 2 # first candle after peak
                                    if confirmation_index < len(close):
                                        df.at[indices[confirmation_index], 'RoundingTop'] = True

            return df
        except Exception as e:
            print(f"Error in detect_rounding_top_dynamic: {e}")
            return df  # Return the original df in case of erro
        


    async def detect_cup_and_handle(self, df):
        """
        Detects cup and handle patterns that end at the latest data point.

        Returns:
        - pd.DataFrame: Original DataFrame with an additional 'CupAndHandle' column.
        """
        try:
            import numpy as np
            from scipy.signal import find_peaks

            df['CupAndHandle'] = False
            df = df.sort_values(['Ticker', 'timespan', 'Timestamp']).reset_index(drop=True)
            grouped = df.groupby(['Ticker', 'timespan'])

            for (ticker, timespan), group in grouped:
                close_prices = group['Close'].values
                indices = group.index

                window = 20  # Adjust as needed for different timespans

                if len(close_prices) < 3 * window:
                    continue

                # Use the last 3*window data points
                recent_prices = close_prices[-3 * window:]
                recent_indices = indices[-3 * window:]

                x = np.arange(len(recent_prices))

                # Fit quadratic curve to recent_prices
                coeffs = np.polyfit(x, recent_prices, 2)
                a = coeffs[0]

                # Check if the quadratic coefficient is positive (U-shaped cup)
                if a <= 0:
                    continue

                # Handle is the last window data points
                handle_prices = recent_prices[-window:]

                # Check if handle is a small retracement from the right lip of the cup
                right_lip = recent_prices[-window - 1]
                min_handle = np.min(handle_prices)
                retracement = (right_lip - min_handle) / right_lip

                if 0.02 <= retracement <= 0.05:
                    # All conditions met, mark 'CupAndHandle' at the latest index
                    df.at[indices[-1], 'CupAndHandle'] = True

            return df
        except Exception as e:
            print(f"Error in detect_cup_and_handle: {e}")
            return df
