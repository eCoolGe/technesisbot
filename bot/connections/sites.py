import asyncio
import re
import httpx
from lxml import html
from decimal import Decimal
from ..logger import log

async def parse_and_calculate_average(df):
    """
    Асинхронная функция для парсинга сайтов и вычисления средних цен.

    Args:
        df (pandas.DataFrame): DataFrame, содержащий столбцы "title", "url" и "xpath".

    Returns:
        tuple: Кортеж, содержащий словарь средних цен и список цен с сайтов.
    """
    site_prices = []
    tasks = [parse_site(row["title"], row["url"], row["xpath"]) for _, row in df.iterrows()]
    results = await asyncio.gather(*tasks)

    average_prices = {}
    price_counts = {}

    for title, url, price in results:
        if price:
            site_prices.append((title, url, price))
            if title not in average_prices:
                average_prices[title] = 0
                price_counts[title] = 0
            average_prices[title] += price
            price_counts[title] += 1
        else:
            site_prices.append((title, url, "-"))

    for title in average_prices:
        average_prices[title] = round(average_prices[title] / price_counts[title], 2)

    return average_prices, site_prices

async def parse_site(title, url, xpath):
    """
    Асинхронная функция для парсинга одного сайта.

    Args:
        title (str): Название сайта.
        url (str): URL сайта.
        xpath (str): XPath выражение для извлечения цен.

    Returns:
        tuple: Кортеж, содержащий название сайта, URL и среднюю цену (или None в случае ошибки).
    """
    try:
        async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:
            response = await client.get(url)
            response.raise_for_status()
            tree = html.fromstring(response.content)
            elements = tree.xpath(xpath)

            prices = []
            for element in elements:
                text = element.text_content().strip()
                cleaned_text = re.sub(r"[^\d\.]", "", text)
                try:
                    price = Decimal(cleaned_text)
                    prices.append(price)
                except ValueError:
                    pass

            if prices:
                return title, url, sum(prices) / len(prices)
    except Exception as e:
        log.info(f"Ошибка при парсинге {title} ({url}): {e}")

    return title, url, None