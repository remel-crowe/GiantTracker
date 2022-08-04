import environs
from pycoingecko import CoinGeckoAPI
from telebot import TeleBot
#CryptoAPI = coingecko
#TeleAPI = telebot


#Ensure to create a .env file in the same directory as this file, include your own token from BotFather
env = environs.Env()
env.read_env()
TOKEN = env("BOT_TOKEN")


bot = TeleBot(token=TOKEN)
coin_client = CoinGeckoAPI()

@bot.message_handler(content_types=['text'])
def priceHandler(message):
    try:
        crypto_id = (message.text).lower()
        data = coin_client.get_price(ids = crypto_id, vs_currencies= 'usd',include_market_cap= True, include_24hr_vol = True, include_24hr_change = True)
        info = coin_client.get_coin_ticker_by_id(id=crypto_id)

        price, mcap = data[crypto_id]['usd'] , round(data[crypto_id]['usd_market_cap'],0)
        volume = round(data[crypto_id]['usd_24h_vol'],2)
        change = round(data[crypto_id]['usd_24h_change'],2)
        ticker = info['tickers'][0]['base']
        name = info['name']

    
        final = (f"{name} - ${ticker} \n"
                f"💰 Price [USD]: ${price}\n"
                f"📦 MarketCap: ${mcap}\n"
                f"📊 Volume: ${volume}\n"
                f"📈 24hr Change: {change}"
                 )
        bot.send_message(chat_id=message.chat.id, text = final)

    except ValueError:
        bot.send_message(chat_id=message.chat.id, text = "🪫 Oops! I don't know that coin. Please try again.")

if __name__ == '__main__':
    bot.polling()
