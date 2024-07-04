import sqlite3


def get_unbroken_pairs():
    conn = sqlite3.connect('trading_pairs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pairs WHERE is_broken = 0')
    pairs = cursor.fetchall()
    conn.close()
    return pairs


def get_broken_pairs():
    conn = sqlite3.connect('trading_pairs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pairs WHERE is_broken = 1')
    pairs = cursor.fetchall()
    conn.close()
    return pairs


# Функция для обновления статуса связки
def update_pair_status(pair_id, is_broken):
    conn = sqlite3.connect('trading_pairs.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pairs
        SET is_broken = ?
        WHERE id = ?
    ''', (is_broken, pair_id))
    conn.commit()
    conn.close()
    return True


# Функция для получения цен пары
def get_spot_price(session, symbol):
    try:
        response = session.get_tickers(category="spot", symbol=symbol)
        if 'result' in response and 'list' in response['result'] and len(response['result']['list']) > 0:
            ticker_info = response['result']['list'][0]
            return {
                'bid': float(ticker_info['bid1Price']),
                'ask': float(ticker_info['ask1Price']),
                'last': float(ticker_info['lastPrice'])
            }
        else:
            raise Exception("Invalid response format")
    except Exception as e:
        print(f"An error occurred while fetching price for {symbol}: {e}")
    return None


# Функция для проверки связок
def check_pairs(session, initial_amount):
    pairs = get_unbroken_pairs()

    pairs_data = []

    for pair in pairs:
        pair_id, currency1, currency2, currency3, is_broken = pair
        amount = initial_amount
        currencies = [currency1, currency2, currency3]
        pairs_to_check = [
            (currencies[0], currencies[1]),
            (currencies[1], currencies[2]),
            (currencies[2], currencies[0])
        ]

        broken = False

        for base, quote in pairs_to_check:
            pair1 = base + quote
            pair2 = quote + base

            price_info1 = get_spot_price(session, pair1)
            price_info2 = get_spot_price(session, pair2)

            if price_info1:
                amount /= price_info1['ask']
            elif price_info2:
                amount *= price_info2['bid']
            else:
                broken = True
                break

        if broken:
            update_pair_status(pair_id, 1)
        else:
            operation = "+" if amount >= initial_amount else ""
            pairs_data.append({
                'name': f"{currency1}-{currency2}-{currency3}",
                'value': f"{operation}{(amount / initial_amount * 100 - 100):.2f}"
            })

    return pairs_data

# add_pair("USDT", "ETH", "EUR")

# Начальная сумма
# initial_amount = 500

# Проверка связок
# check_pairs(session, initial_amount)
