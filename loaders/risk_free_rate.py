import requests as req

def get_rf_moex(date, engine='stock'):
    url = f"https://iss.moex.com/iss/engines/{engine}/zcyc.json?date={date}&iss.meta=off"
    r = req.get(url)
    r.encoding = 'utf-8-sig'
    return r.json()

def get_risk_free_rate(date, period=1):
    response_json = get_rf_moex(date)
    yearyields_data = response_json.get('yearyields', {})
    columns = yearyields_data.get('columns', [])
    data = yearyields_data.get('data', [])

    for row in data:
        yield_info = {columns[i]: row[i] for i in range(len(columns))}
        if yield_info.get('period') == period:
            return round(yield_info.get('value') / 100, 3)

    return None