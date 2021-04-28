from yahoo_fin import stock_info as si
import time



profit_multiplier = 1.002
stoploss = 0.99
allowed_time = 300

total_spent = 0
ending_money = 0
total_percent = 0
money_percent = 0
profit = 0
number_of_stocks_trading = 9
number_of_stocks_done = 0

start_time = time.time()
time_passed = 0



list_of_profit = []
dict_of_bought_at_prices = {"Apple": 0, 'AMD': 0, 'Microsoft': 0, 'Tesla': 0, 'Bank of America': 0, 'Google': 0, 'AT&T': 0, 'Exxon Mobile': 0, 'Amazon': 0}
dict_of_sold_at_prices = {"Apple": 0, 'AMD': 0, 'Microsoft': 0, 'Tesla': 0, 'Bank of America': 0, 'Google': 0, 'AT&T': 0, 'Exxon Mobile': 0, 'Amazon': 0}
dict_of_companies = {"Apple": "aapl", "AMD": "amd", "Microsoft": "msft", "Tesla": "tsla", "Bank of America": "bac", "Google": "goog", "AT&T": "T", "Exxon Mobile": "xom", "Amazon": "amzn"}
list_of_companies = ["Apple", "AMD", "Microsoft", "Tesla", "Bank of America", "Google", "AT&T", "Exxon Mobile", "Amazon"]


def add_stock(name, tick):
    global number_of_stocks_trading, dict_of_bought_at_prices, dict_of_sold_at_prices, dict_of_companies, list_of_companies
    dict_of_companies[name] = tick
    dict_of_bought_at_prices[name] = 0
    dict_of_sold_at_prices[name] = 0
    list_of_companies.append(name)
    number_of_stocks_trading += 1


def morning():
    global dict_of_bought_at_prices, dict_of_sold_at_prices, dict_of_companies, total_spent, list_of_companies
    x = 0
    for ticker in dict_of_companies.values():
        dict_of_bought_at_prices[list_of_companies[x]] = si.get_live_price(ticker)
        print(list_of_companies[x], "was bought for", dict_of_bought_at_prices[list_of_companies[x]])
        total_spent += dict_of_bought_at_prices[list_of_companies[x]]
        x += 1
    print("total money spent:", total_spent)


def sold_yet(list_position):
    global number_of_stocks_done, number_of_stocks_trading, dict_of_bought_at_prices, dict_of_sold_at_prices, list_of_companies
    global profit_multiplier, stoploss
    if dict_of_sold_at_prices[list_of_companies[list_position]] == 0:
        live_price = si.get_live_price(dict_of_companies[list_of_companies[list_position]])
        if live_price > profit_multiplier * dict_of_bought_at_prices[list_of_companies[list_position]]:
            dict_of_sold_at_prices[list_of_companies[list_position]] = live_price
            print(list_of_companies[list_position], "was sold for", dict_of_sold_at_prices[list_of_companies[list_position]])
            number_of_stocks_done += 1
            print(number_of_stocks_done, "/", number_of_stocks_trading)
        elif live_price < stoploss * dict_of_bought_at_prices[list_of_companies[list_position]]:
            dict_of_sold_at_prices[list_of_companies[list_position]] = live_price
            print(list_of_companies[list_position], "was sold for", dict_of_sold_at_prices[list_of_companies[list_position]])
            number_of_stocks_done += 1
            print(number_of_stocks_done, "/", number_of_stocks_trading)


def live_money():
    global number_of_stocks_done, dict_of_sold_at_prices,  number_of_stocks_trading, number_of_stocks_done, time_passed, allowed_time
    while 0 in dict_of_sold_at_prices.values():
        current_time = time.time()
        time_passed = (current_time - start_time)
        if time_passed > allowed_time:
            for company in dict_of_sold_at_prices:
                if dict_of_sold_at_prices[company] == 0:
                    live_price = si.get_live_price(dict_of_companies[company])
                    dict_of_sold_at_prices[company] = live_price
                    print(company, "was sold for",dict_of_sold_at_prices[company])
                    number_of_stocks_done += 1
                    print(number_of_stocks_done, "/", number_of_stocks_trading)
        else:
            for company in dict_of_sold_at_prices:
                if dict_of_sold_at_prices[company] == 0:
                    sold_yet(list_of_companies.index(company))


def did_i_make_money():
    global total_spent, ending_money, list_of_companies, dict_of_sold_at_prices, total_percent, money_percent
    x = 0
    profit = 0
    while x <= (number_of_stocks_trading - 1):
        ending_money += dict_of_sold_at_prices[list_of_companies[x]]
        total_percent += ((dict_of_sold_at_prices[list_of_companies[x]] - dict_of_bought_at_prices[list_of_companies[x]]) / dict_of_bought_at_prices[list_of_companies[x]])
        x += 1
    profit = ending_money - total_spent
    money_percent = (ending_money - total_spent) / total_spent

    print()
    print()
    print()
    print("total spent:", total_spent)
    print("total END:", ending_money)
    print("Total P/L:", profit)
    print("Percent of each stock change:", total_percent, "%")
    print("Total percent change:", money_percent, "%")


def daily():
        morning()
        live_money()
        did_i_make_money()
        list_of_profit.append(profit)



add_stock("Gamestop", "gme")
#add_stock("UBER", "uber")
#add_stock("Waste Management", "wm")
#add_stock("United", "ual")
#add_stock("Snapchat", "snap")
#add_stock("Haliburton", "hal")
#add_stock("TEVA", "teva")
#add_stock("Kinder Morgan", "kmi")
#add_stock("Penn National Gaming", "penn")
#add_stock("Cable One", "cabo")
#add_stock("Chipotle", "cmg")
#add_stock("Shopify", "shop")
#add_stock("Zoom", "zm")
#add_stock("Netflix", "nflx")
#add_stock("MSCI", "msci")
#add_stock("Ford", "f")
#add_stock("US Oil", "uso")
#add_stock("General Electric", "ge")
daily()


