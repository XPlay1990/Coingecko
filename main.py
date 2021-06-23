from pycoingecko import CoinGeckoAPI
import locale

locale.setlocale(locale.LC_ALL, '')


def format_float_number(float_number):
    return locale.format_string("%d", round(float_number, 3), grouping=True)

def format_float_number_percentage(float_number):
    return format_float_number(float_number) + "%"


def format_float_number_percentage_igned(float_number):
    # return '{0:+}%'.format(round(float_number, 3)).replace(".", ",")
    return locale.str(round(float_number, 3)) + "%"


class Coin:

    def __init__(self, name, price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency,
                 price_change_percentage_7d_in_currency, current_price, ath):
        self.name = name
        self.price_change_percentage_1h_in_currency = price_change_percentage_1h_in_currency
        self.price_change_percentage_24h_in_currency = price_change_percentage_24h_in_currency
        self.price_change_percentage_7d_in_currency = price_change_percentage_7d_in_currency
        self.current_price = current_price
        self.ath = ath

    def __str__(self):
        return self.name + ", 1h Change: " + format_float_number_percentage_igned(
            self.price_change_percentage_1h_in_currency) + ", 24h Change: " + format_float_number_percentage_igned(
            self.price_change_percentage_24h_in_currency) + ", 7d Change: " + format_float_number_percentage_igned(
            self.price_change_percentage_7d_in_currency) + "; \n ATH Price-Drop: " + format_float_number_percentage(
            (1 - (self.current_price / self.ath)) * 100)


cg = CoinGeckoAPI()

coinIds = "bitcoin,ethereum,binancecoin,cardano,dogecoin,ripple,polkadot,uniswap,solana,chainlink,matic-network," \
          "shiba-inu,aave,bittorrent-2,chiliz,yearn-finance,flow,b20,defichain "

queryResult = cg.get_coins_markets("eur",
                                   # ids=coinIds,
                                   price_change_percentage="1h,24h,7d,14d,30d")

# print(queryResult)

coinNames = []
price_change_percentage_1h_in_currency = 0
price_change_percentage_24h_in_currency = 0
price_change_percentage_7d_in_currency = 0
price_change_percentage_14d_in_currency = 0
price_change_percentage_30d_in_currency = 0
total_market_cap = 0
total_volume = 0

for coin in queryResult:
    try:
        coinNames.append(coin["name"] + " (rank " + str(coin["market_cap_rank"]) + ")")
        price_change_percentage_1h_in_currency += coin["price_change_percentage_1h_in_currency"]
        price_change_percentage_24h_in_currency += coin["price_change_percentage_24h_in_currency"]
        price_change_percentage_7d_in_currency += coin["price_change_percentage_7d_in_currency"]
        price_change_percentage_14d_in_currency += coin["price_change_percentage_14d_in_currency"]
        price_change_percentage_30d_in_currency += coin["price_change_percentage_30d_in_currency"]
        total_market_cap += coin["market_cap"]
        total_volume += coin["total_volume"]
    except Exception as e:
        print("Exception! Coin: " + str(coin))
        print(e)

print(", ".join(coinNames))
print("")
print("Total Market changes: ")
print("1h Change: " + format_float_number_percentage_igned(price_change_percentage_1h_in_currency / len(queryResult)))
print("24h Change: " + format_float_number_percentage_igned(price_change_percentage_24h_in_currency / len(queryResult)))
print("7 day Change: " + format_float_number_percentage_igned(price_change_percentage_7d_in_currency / len(queryResult)))
print("14 day Change: " + format_float_number_percentage_igned(price_change_percentage_14d_in_currency / len(queryResult)))
print("30 day Change: " + format_float_number_percentage_igned(price_change_percentage_30d_in_currency / len(queryResult)))
print("total_market_cap: " + locale.currency(total_market_cap, grouping=True, international=True))
print("total_volume: " + locale.currency(total_volume, grouping=True, international=True))

# top coin 1h / 24h / 7d

topCoins = []
top_price_change_percentage_1h_in_currency = []
top_price_change_percentage_24h_in_currency = []
top_price_change_percentage_7d_in_currency = []
top_price_change_percentage_14d_in_currency = []
top_price_change_percentage_30d_in_currency = []

for coin in queryResult:
    topCoins.append(coin["name"] + " (rank " + str(coin["market_cap_rank"]) + ")")
    top_price_change_percentage_1h_in_currency.append(coin["price_change_percentage_1h_in_currency"])
    top_price_change_percentage_24h_in_currency.append(coin["price_change_percentage_24h_in_currency"])
    top_price_change_percentage_7d_in_currency.append(coin["price_change_percentage_7d_in_currency"])
    top_price_change_percentage_14d_in_currency.append(coin["price_change_percentage_14d_in_currency"])
    top_price_change_percentage_30d_in_currency.append(coin["price_change_percentage_30d_in_currency"])
    # createdCoin = Coin(coin["name"] + " (rank " + str(coin["market_cap_rank"]) + ")",
    #                    coin["price_change_percentage_1h_in_currency"], coin["price_change_percentage_24h_in_currency"],
    #                    coin["price_change_percentage_7d_in_currency"], coin["current_price"], coin["ath"])
    # print(createdCoin)

max1h = max([x for x in top_price_change_percentage_1h_in_currency if x is not None])
max24h = max([x for x in top_price_change_percentage_24h_in_currency if x is not None])
max7d = max([x for x in top_price_change_percentage_7d_in_currency if x is not None])
max14d = max([x for x in top_price_change_percentage_14d_in_currency if x is not None])
max30d = max([x for x in top_price_change_percentage_30d_in_currency if x is not None])

print()
print("Top coins: ")
print("Top Price Change 1h: " + format_float_number_percentage_igned(max1h) + ", Coin: " + topCoins[
    top_price_change_percentage_1h_in_currency.index(max1h)])
print("Top Price Change 24h: " + format_float_number_percentage_igned(max24h) + ", Coin: " + topCoins[
    top_price_change_percentage_24h_in_currency.index(max24h)])
print("Top Price Change 14d: " + format_float_number_percentage_igned(max14d) + ", Coin: " + topCoins[
    top_price_change_percentage_14d_in_currency.index(max14d)])
print("Top Price Change 30d: " + format_float_number_percentage_igned(max30d) + ", Coin: " + topCoins[
    top_price_change_percentage_30d_in_currency.index(max30d)])
