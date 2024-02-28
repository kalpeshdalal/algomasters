# ===================================================================================
# Fyers APi Details
# ===================================================================================
broker = 'Fyers'
redirect_uri = "https://www.google.com/"  ## redircet_uri you entered while creating APP.
client_id = "CT3VFVIIHT-100"  ## Client_id here refers to APP_ID of the created app
secret_key = "LIM58G8U3A"  ## app_secret key which you got after creating the app
grant_type = "authorization_code"  ## The grant_type always has to be "authorization_code"
response_type = "code"  ## The response_type always has to be "code"
state = "sample"
TokenUrl = "https://api-t1.fyers.in/api/v3/generate-authcode?client_id=CT3VFVIIHT-100&redirect_uri=https%3A%2F%2Fwww.google.com%2F&response_type=code&state=sample"
auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MDcwMzA5NDIsImV4cCI6MTcwNzA2MDk0MiwibmJmIjoxNzA3MDMwMzQyLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzA0NjQ0Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiYWE0NDY0MGY0MWE0MDc3NmM1NGE1YTVjZjM5MjFhYjlhNTAzOWI1M2IzYTI2ZWFmZWVkNTlkOWEiLCJub25jZSI6IiIsImFwcF9pZCI6IkNUM1ZGVklJSFQiLCJ1dWlkIjoiYWYwNmI4MTQ5ZDI5NGVhYjkyN2ZkNDYwZWNiYjhhN2QiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.u9mcoqhk4VvXj6tVIWZIypd5nyZjjkuatYuPtKRaoRo"
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MDkwOTMwNDgsImV4cCI6MTcwOTE2NjYwOCwibmJmIjoxNzA5MDkzMDQ4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbDNyQzR6RWpFVzdIb3QtVy1aUGNSNGw0LURBUm5WcnlJMjVfWXUyaUNvWEVVQXliV2Q4QXVSc25jZHFZbFI0Y0VQdUNJbVZ0bmRCT01ZWkd3c2o5ZTNpcG9UNGZ5OVYySWNGc2RhUHJ2Mmc1cW15WT0iLCJkaXNwbGF5X25hbWUiOiJTVVNISUwgU1VOSUwgS0FWQURFIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjBjZDEyNzkwNDViN2E1MmVhNmVkNThhYjcxNmQ4MTNkZjU5NTIzMTdiMDc1YTZiYTFhMGY2MjMiLCJmeV9pZCI6IllTMDQ2NDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.xuetiHXz8CGjbWssMLA3WIpHw_P45mOr9n5XAzibOiM'
# Setup Related Configs
# ===================================================================================
ORB_timeFrame = 60  # in seconds
symbols = ['NSE:BANKNIFTY24FEB47900CE', 'NSE:BANKNIFTY24FEB46500PE']
symbol_1 = symbols[0]
symbol_2 = symbols[1]
fut_symbol = 'NSE:BANKNIFTY24FEBFUT'
# ===================================================================================
# Define strategy
# ===================================================================================
sl_pts = 20
brkevn_pts = 5
brkevn_surplus_pts = 3
trg_final_pts = 50
symb_max_price = 450
symb_min_price = 50
max_day_loss = 2000
max_day_profit = 5000
trade_qty = 15
order_placement_type = 0  # 0-> place order immediately after candle close, 1-> place order after candle high/low break
wait_after_position_close = 180  # in seconds
wait_after_setup_appeared = 180  # in seconds