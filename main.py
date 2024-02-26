import argparse
import aiohttp
import asyncio
from datetime import datetime, timedelta

async def fetch_currency_rate(date, currency_codes):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            rates = {currency: None for currency in currency_codes}
            
            for rate in data.get('exchangeRate', []):
                currency = rate.get('currency')
                if currency in currency_codes:
                    rates[currency] = {
                        'sale': rate.get('saleRate'),
                        'purchase': rate.get('purchaseRate')
                    }
            return {date.strftime('%d.%m.%Y'): rates}
        
async def main(days, currencies):
    tasks = [fetch_currency_rate(datetime.now() - timedelta(), currencies) for day in range(days)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get currency rates for the last N days.')
    parser.add_argument('days', type=int, help='Number of days to fetch rates for, up to 10.')
    parser.add_argument('--currencies', nargs='+', default=['USD', 'EUR'], help='List of currencies to fetch (default: USD EUR).')
    args = parser.parse_args()

    if args.days > 10 or args.days < 1:
        print("Error: Number of days shoould be beetween 1 and 10.")
    else:
        asyncio.run(main(args.days, args.currencies))