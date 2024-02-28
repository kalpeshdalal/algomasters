import datetime
import json

from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
import UserConfig as cfg
import AlgoUtil as utl
import pandas as pd
import AlgoSetup as stp
import os
import signal
import time
# Message store
messages = []


symbols = cfg.symbols
symbol = cfg.symbol_1
# symbol_1 = cfg.symbol_1
# symbol_2 = cfg.symbol_2

fyers = fyersModel.FyersModel()
fyers_socket = data_ws.FyersDataSocket(cfg.access_token)

ltp = curr_ltp_1 = curr_ltp_2 = 0.00
df_data = pd.DataFrame()
curr_order_id = None

is_setup_appear = is_order_in_place = is_position_exist = False

traded_price = sl_price = brkevn_price = final_trg_price = 0.00

def onmessage(message):
    global ltp, df_data, symbol, curr_order_id, is_setup_appear, is_order_in_place, is_position_exist
    global traded_price, sl_price, brkevn_price, final_trg_price

    if message.get('ltp') is not None:
        ltp = message['ltp']
        time_stamp = datetime.datetime.fromtimestamp(message['last_traded_time'])
        volume = message['last_traded_qty']
        instrument = message['symbol']
        vwap = message['avg_trade_price']
        print("----------------------------------------------------------------------------------------------------")
        print(f"Time: {time_stamp}, Symbol: {instrument}, Ltp: {ltp}")

        messages.append(f"----------------------------------------------------------------------------------------------------")
        messages.append(f"Time: {time_stamp}, Symbol: {instrument}, Ltp: {ltp}")

        tmp_df = pd.DataFrame([[time_stamp, instrument, ltp, ltp, ltp, ltp, volume, vwap]],
                              columns=['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'vwap'])
        df_data = pd.concat([df_data, tmp_df])

        is_setup_appear = stp.chk_for_setup(df_data, symbol)
        print(f"Setup flag: {is_setup_appear}, Curr ord id: {curr_order_id}")
        messages.append(f"Setup flag: {is_setup_appear}, Curr ord id: {curr_order_id}")

        if is_order_in_place:
            if ltp >= brkevn_price:
                if sl_price <= traded_price:
                    sl_price = traded_price + cfg.brkevn_surplus_pts
                    brkevn_price = ltp
                    print(f"New Prices for {symbol}, Curr: {ltp}, SL: {sl_price}, Brkevn:{brkevn_price}")
                    messages.append(f"New Prices for {symbol}, Curr: {ltp}, SL: {sl_price}, Brkevn:{brkevn_price}")

                else:
                    sl_price = sl_price + (ltp - brkevn_price)
                    brkevn_price = ltp
                    print(f"New Prices for {symbol}, Curr: {ltp}, SL: {sl_price}, Brkevn:{brkevn_price}")
                    messages.append(f"New Prices for {symbol}, Curr: {ltp}, SL: {sl_price}, Brkevn:{brkevn_price}")
    
            elif (ltp < sl_price) or (ltp >= final_trg_price):
                sell_order_id = utl.place_order(symbol, -1)
                print(f"SL/TARGET Hit for {symbol}>>>>>> P/L is: {sl_price - traded_price} points!!!!")
                messages.append(f"SL/TARGET Hit for {symbol}>>>>>> P/L is: {sl_price - traded_price} points!!!!")

                if sell_order_id is not None:
                    curr_order_id = None
                    traded_price = None
                    sl_price = None
                    brkevn_price = None
                    final_trg_price = None
                    is_order_in_place = None
        elif is_setup_appear and (not is_order_in_place) and (not is_position_exist):
            # curr_order_id = utl.place_order(symbol, 1)
            is_order_in_place = True if curr_order_id is not None else False
            print(f"Order placed virtually for {fyers.orderbook()} ...!!!")
            messages.append(f"Order placed virtually for {fyers.orderbook()} ...!!!")
            tmp_trd_prc = utl.get_order_traded_price(curr_order_id)
            if tmp_trd_prc is None:
                traded_price = ltp
            else:
                traded_price = tmp_trd_prc
            sl_price = traded_price - cfg.sl_pts
            brkevn_price = traded_price + cfg.brkevn_pts
            final_trg_price = traded_price + cfg.trg_final_pts
            print(f"For {symbol}-> Traded Price:{traded_price}, SL:{sl_price}, Brkevn:{brkevn_price}, Final Target:{final_trg_price}")
            messages.append(f"For {symbol}-> Traded Price:{traded_price}, SL:{sl_price}, Brkevn:{brkevn_price}, Final Target:{final_trg_price}")

        else:
            print(f"Setup does not appeared or Order is already placed/in queue, wait......")
            messages.append(f"Setup does not appeared or Order is already placed/in queue, wait......")



def onerror(message):
    print("Error:", message)
    messages.append("Error: " + str(message["message"] ))



def onclose(message):
    messages.append("Connection closed: " + str(message["message"]))

    print("Connection closed:", message)


def onopen():
    messages.append("Connection opened....")
    print("Connection opened....")


# Create a FyersDataSocket instance with the provided parameters
def get_socket_data():
    global fyers_socket
    fyers_socket = data_ws.FyersDataSocket(
        access_token=cfg.access_token,  # Access token in the format "appid:accesstoken"
        log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
        litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
        write_to_file=True,  # Save response in a log file instead of printing it.
        reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
        on_connect=onopen,  # Callback function to subscribe to data upon connection.
        on_close=onclose,  # Callback function to handle WebSocket connection close events.
        on_error=onerror,  # Callback function to handle WebSocket errors.
        on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
        reconnect_retry=10  # Number of times reconnection will be attempted in case
    )
    fyers_socket.connect()
    data_type = "SymbolUpdate"
    fyers_socket.subscribe(symbols=symbols, data_type=data_type)
    fyers_socket.keep_running()


def stop_websocket():
    print("Stopping WebSocket connection to stop receiving data...")
    messages.append("Stopping WebSocket connection...")
    try:
        fyers_socket.close_connection()
        print("WebSocket connection closed.")
        messages.append("WebSocket connection closed.")
    except Exception as e:
        print(f"Error stopping WebSocket connection: {e}")
        messages.append(f"Error stopping WebSocket connection: {e}")
    
    



def get_messages():
    global messages
    current_messages = list(messages)  # Make a copy if you want to preserve original messages # Clear original list after copying
    return current_messages



def main():
    ## get access token ###############################
    # access_token = getAccessToken.main()
    ##################################################
    global fyers
    fyers = utl.create_fyr_obj(cfg.client_id, cfg.access_token)
    get_socket_data()

if __name__ == '__main__':
    main()
