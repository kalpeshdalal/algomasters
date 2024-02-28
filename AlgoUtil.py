import datetime

import pandas as pd
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
import UserConfig as cfg

access_token = cfg.access_token
client_id = cfg.client_id
fyers = fyersModel.FyersModel()
fyers_socket = data_ws.FyersDataSocket(access_token)


def place_order(symb, side):
    global fyers
    data = {
        "symbol": symb,
        "qty": cfg.trade_qty,
        "type": 2,  # 1 => Limit Order 2 => Market Order 3 => Stop Order (SL-M) 4 => Stoplimit Order (SL-L)
        "side": side,  # 1 => Buy -1 => Sell
        "productType": "INTRADAY",
        # CNC => For equity only, INTRADAY => Applicable for all segments., MARGIN => Applicable only for derivatives, CO => Cover Order, BO => Bracket Order
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",  # IOC => Immediate or Cancel, DAY => Valid till the end of the day
        "disclosedQty": 0,
        "offlineOrder": False,  # False => When market is open, True => When placing AMO order
        "stopLoss": 0,  # put stoploss value
        "takeProfit": 0,  # put takeProfit value
        "orderTag": "placedBySetup1"
    }
    response = fyers.place_order(data=data)
    if "Successfully placed order" in response['message'] and "RED:" not in response['message'] and response['id'] is not None:  # Order submitted successfully
        # print(response['message'])
        order_id = response['id']
        print(f">>>>>>>>>>>ORDER PLACED for Symbol: {symb}, Order id: {order_id} <<<<<<<<<<<<<<")
        return order_id
    else:
        print(f"Message: {response['message']}")
        return None


def is_in_order(symb):
    tmp_orders = pd.json_normalize(fyers.orderbook(), record_path=['orderBook'])
    if tmp_orders.empty:
        return False
    else:
        mask1 = (tmp_orders['symbol'] == symb) & (tmp_orders['status'] == 6)
        if tmp_orders[mask1].empty:
            return False
        else:
            return True


def get_order_traded_price(ord_id):
    data = {"id": ord_id}
    tmp_orders = pd.json_normalize(fyers.orderbook(data=data), record_path=['orderBook'])
    if tmp_orders.empty:
        return None
    else:
        return tmp_orders['tradedPrice'].tail(1).to_numpy()[0]


def is_in_position(symb):
    is_pos_flag = False
    tmp_position = fyers.positions().get('netPositions', [])
    # print(tmp_position)
    for position in tmp_position:
        if position.get('symbol') in (symb) and position.get('netQty') > 0:
            # print(f"TRUE:-> Symbol with net qty found: {symb}, {position.get('netQty')}")
            is_pos_flag = True
            break
    # print(f"is pos flag is : {is_pos_flag}")
    return is_pos_flag


def is_position_exist(symb):
    is_pos_exist_flag = False
    tmp_orders = pd.json_normalize(fyers.orderbook(), record_path=['orderBook'])
    if tmp_orders.empty:
        is_pos_exist_flag = False
    else:
        mask1 = (tmp_orders['symbol'] == symb) & (tmp_orders['status'] == 6)
        if tmp_orders[mask1].empty:
            is_pos_exist_flag = False
        else:
            is_pos_exist_flag = True
            return is_pos_exist_flag
    tmp_position = fyers.positions().get('netPositions', [])
    # print(tmp_position)
    for position in tmp_position:
        if position.get('symbol') in (symb) and position.get('netQty') > 0:
            # print(f"TRUE:-> Symbol with net qty found: {symb}, {position.get('netQty')}")
            is_pos_exist_flag = True
            break
    return is_pos_exist_flag


def create_fyr_obj(cl_id, acc_token):
    # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    global fyers
    fyers = fyersModel.FyersModel(client_id=cl_id, token=acc_token, is_async=False, log_path="")
    # print("Fyers obj created")
    return fyers


def main():
    print("This is main function of AlgoUtil class")


if __name__ == '__main__':
    main()
