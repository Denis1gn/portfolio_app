import requests as req
import datetime as dt
import pandas as pd
import time

def flatten(j: dict, blockname: str):
    columns = j[blockname]['columns']
    return [{k: r[i] for i, k in enumerate(columns)} for r in j[blockname]['data']]

def get_moex_stock_data(secid, start_date, end_date, engine='stock', market='shares', board='TQBR'):
    # Преобразуем строки в даты
    if isinstance(start_date, str):
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()

    # Гарантируем, что конец не в будущем
    today = dt.date.today()
    if end_date > today:
        print(f"🔁 Конец окна {end_date} > сегодня. Заменяем на {today}")
        end_date = today

    # Гарантируем, что начало не позже конца
    if start_date > end_date:
        print(f"Начальная дата {start_date} позже конечной {end_date}. Меняем на год назад.")
        start_date = end_date - dt.timedelta(days=365)

    all_data = []
    current_start_date = start_date

    while current_start_date <= end_date:
        current_end_date = current_start_date + dt.timedelta(days=99)
        if current_end_date > end_date:
            current_end_date = end_date

        url = f"https://iss.moex.com/iss/history/engines/{engine}/markets/{market}/boards/{board}/securities/{secid}.json?from={current_start_date}&till={current_end_date}&iss.meta=off"

        print(f"Запрос {secid}: {current_start_date} → {current_end_date}")
        print(f"URL: {url}")

        try:
            r = req.get(url)
            r.encoding = 'utf-8'
            j = r.json()

            if 'history' not in j or not j['history']['data']:
                print(f"Нет данных по {secid} за период {current_start_date}–{current_end_date}")
            else:
                flattened_data = flatten(j, 'history')
                all_data.extend(flattened_data)

            current_start_date = current_end_date + dt.timedelta(days=1)
            time.sleep(0.5)

        except Exception as e:
            print(f"Ошибка при запросе данных {secid}: {e}")
            break

    return all_data

def get_moex_data_and_prepare(secid, start_date, end_date):
    data = get_moex_stock_data(secid, start_date, end_date)

    if not data:
        print(f"Нет данных для {secid}")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if 'TRADEDATE' not in df.columns or 'CLOSE' not in df.columns:
        print(f"Отсутствуют обязательные поля в данных {secid}: {df.columns.tolist()}")
        return pd.DataFrame()

    df['TRADEDATE'] = pd.to_datetime(df['TRADEDATE'])
    df.set_index('TRADEDATE', inplace=True)
    df = df[['CLOSE']].asfreq("B").fillna(method='ffill')
    df.columns = [f'{secid}_Stock_Price']
    df[f'{secid}_Daily_Return'] = df[f'{secid}_Stock_Price'].pct_change()
    df.dropna(inplace=True)

    return df
