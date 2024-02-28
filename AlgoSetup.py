import pandas as pd
import UserConfig as cfg


def chk_for_setup(df, symb):
    # define your setup here
    # derive indicator values

    lst_close = df['close'].tail(1).to_numpy()[0]
    lst_high = df['high'].tail(1).to_numpy()[0]
    lst_vwap = df['vwap'].tail(1).to_numpy()[0]
    lst_time = df['timestamp'].tail(1).to_numpy()[0]

    print("----------------------------------------------------------------------------------------------------")
    print(f"Time: {lst_time}, Symbol: {symb} :-> Lst Close: {lst_close} Lst VWAP: {lst_vwap}")

    # ----- temp setup
    if lst_close >= lst_vwap and cfg.symb_min_price < lst_close < cfg.symb_max_price :
        return True
    else:
        return False
    # =======================================================
