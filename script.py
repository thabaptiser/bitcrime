import sqlite3
import plotly
from plotly.graph_objs import Scatter
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil import rrule
import urllib2
import json
import uuid

conn = sqlite3.connect('/data/projects/08303-crime/bitcoin-abe-master/abe.sqlite')
conn = sqlite3.connect('/home/bvauthey/bitcrime/abe.sqlite')
req_string = 'http://api.coindesk.com/v1/bpi/historical/close.json?start={start}&end={start}'

c = conn.cursor()


start_date = date(2010, 7, 18)
end_date = date(2016, 1, 1)
date_list = []
money_list = []
all_data = []
created_money_list = False
for day in rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date):
    date_list.append(day)
    week_row = []
    for i in range(0,101):
        if not created_money_list:
            money_list.append(i*100)
        money_start = i*100
        money_end = i*100+99
        print(req_string.format(start=day.strftime("%Y-%m-%d"), end=day.strftime("%Y-%m-%d")))
        response =  urllib2.urlopen(req_string.format(start=day.strftime("%Y-%m-%d"), end=day.strftime("%Y-%m-%d")))
        html = response.read()
        values = json.loads(html)

        BTCUSD = values['bpi'][day.strftime("%Y-%m-%d")]


        t0 = time.mktime(day.timetuple())
        t1 = time.mktime((day + timedelta(days=7)).timetuple())
        QUERY = """SELECT COUNT(*) FROM txout_detail2 WHERE block_nTime >= {t0}
        AND block_nTime <= {t1} AND txout_value >= {v0}
        AND txout_value <= {v1};""".format(v0=100000000*money_start/BTCUSD, v1=100000000*money_end/BTCUSD, t0=t0, t1=t1)
        print(QUERY)
        for row in c.execute(QUERY):
            week_row.append(row[0])
            print(row)
    with open('bitcrime_results' + uuid.uuid4()) as f:
        f.write(','.join(week_row))
	f.write('\n')
    created_money_list = True
    all_data.append(week_row)

z = all_data
x = date_list
y = money_list



data = [go.Heatmap(z=z,x=x,y=y,colorscale='Viridis',)]

layout = go.Layout(
    title='Anonymity set per week and transaction USD amount',
    xaxis = dict(ticks='', nticks=36),
    yaxis = dict(ticks='' )
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='datetime-heatmap')
