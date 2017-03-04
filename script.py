import sqlite3
import plotly
from plotly.graph_objs import Scatter
import time
from datetime import datetime
from datetime import timedelta

conn = sqlite3.connect('abe.sqlite')
trans_val = int(raw_input("Transaction value: "))
trans_fuzz = int(raw_input("Transaction value fuzz: "))
transaction_time = raw_input("Date of start: ")
transaction_time = datetime.strptime(transaction_time, '%m-%d-%Y')
time_fuzz1 = int(raw_input("Days to fuzz 1: "))
time_fuzz2 = int(raw_input("Days to fuzz 2: "))
time_fuzz3 = int(raw_input("Days to fuzz 3: "))

c = conn.cursor()

first_res = []
second_res = []
third_res = []

bottom_axis = []

for i in range(0,5):
  bottom_axis.append(i*trans_fuzz/5)
  v0 = 100000000*(trans_val - i*trans_fuzz/5) 
  v1 = 100000000*(trans_val) 

  t0 = transaction_time - timedelta(days=time_fuzz1) 
  t0 = time.mktime(t0.timetuple())

  t1 = transaction_time + timedelta(days=time_fuzz1) 
  t1 = time.mktime(t1.timetuple())
  print("trying first query")
  QUERY = "SELECT COUNT(*) FROM txout_detail2 WHERE block_nTime >= {t0} AND block_nTime <= {t1} AND txout_value >= {v0} AND txout_value <= {v1} LIMIT 100;".format(v0=v0, v1=v1, t0=t0, t1=t1)
  for row in c.execute(QUERY):
    print(row)
    first_res.append( row[0])
  t0 = transaction_time - timedelta(days=time_fuzz2) 
  t0 = time.mktime(t0.timetuple())

  t1 = transaction_time + timedelta(days=time_fuzz2) 
  t1 = time.mktime(t1.timetuple())
  print("trying second query")
  QUERY = "SELECT COUNT(*) FROM txout_detail2 WHERE block_nTime >= {t0} AND block_nTime <= {t1} AND txout_value >= {v0} AND txout_value <= {v1} LIMIT 100;".format(v0=v0, v1=v1, t0=t0, t1=t1)
  for row in c.execute(QUERY):
    print(row)
    second_res.append( row[0])


  t0 = transaction_time - timedelta(days=time_fuzz3) 
  t0 = time.mktime(t0.timetuple())

  t1 = transaction_time + timedelta(days=time_fuzz3) 
  t1 = time.mktime(t1.timetuple())
  print("trying third query")
  QUERY = "SELECT COUNT(*) FROM txout_detail2 WHERE block_nTime >= {t0} AND block_nTime <= {t1} AND txout_value >= {v0} AND txout_value <= {v1} LIMIT 100;".format(v0=v0, v1=v1, t0=t0, t1=t1)
  for row in c.execute(QUERY):
    print(row)
    third_res.append( row[0])


trace0 = Scatter(
    x = bottom_axis,
    y = first_res,
    name = 'Tf = {t1}'.format(t1=time_fuzz1),
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)
trace1 = Scatter(
    x = bottom_axis,
    y = second_res,
    name = 'Tf = {t2}'.format(t2=time_fuzz2),
    line = dict(
        color = ('rgb(24, 12, 205)'),
        width = 4)
)
trace2 = Scatter(
    x = bottom_axis,
    y = third_res,
    name = 'Tf = {t3}'.format(t3=time_fuzz3),
    line = dict(
        color = ('rgb(12, 205, 24)'),
        width = 4)
)

data = [trace0, trace1, trace2]

# Edit the layout
layout = dict(title = 'Hits vs Bitcoin fuzz given time fuzzes',
              xaxis = dict(title = 'Bitcoin value fuzz'),
              yaxis = dict(title = 'Number of hits'),
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='styled-line')
 
#for row in c.execute(QUERY):
#  print(row)
