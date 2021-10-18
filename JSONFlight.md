# Project 02 - 

__Bryton Petersen__
__02/06/2021__




## Elevator pitch

According to researchers of Civil and Environmental engineering at UC Berkeley, almost \$33 billion is lost every year due to delayed flights. $16 billion, or nearly half of the total loss, is from the wasted time of patient passengers, with only \$8 billion of the loss coming from the actual airline companies. By taking a look at the delay data from airports across the country, I analyze when and where we can expect to see the most delays.

## TECHNICAL DETAILS

__Grand Question 1__  -  Which airport has the worst delays?

CHART 1 - 


| airport_code   |   num_of_flights_total |   num_of_delays_total |   minutes_delayed_total |   proportion_of_delays |   hours_delayed_average |
|:---------------|-----------------------:|----------------------:|------------------------:|-----------------------:|------------------------:|
| ATL            |                4430047 |                902443 |                408969   |                   0.2  |                 6816.15 |
| DEN            |                2513974 |                468519 |                190707   |                   0.19 |                 3178.46 |
| IAD            |                 851571 |                168467 |                 77905.1 |                   0.2  |                 1298.42 |
| ORD            |                3597588 |                830825 |                426940   |                   0.23 |                 7115.67 |
| SAN            |                 917862 |                175132 |                 62698.8 |                   0.19 |                 1044.98 |
| SFO            |                1630945 |                425604 |                201140   |                   0.26 |                 3352.33 |
| SLC            |                1403384 |                205160 |                 76692.2 |                   0.15 |                 1278.2  |


SFO has the worst delays out of all of the airports in the dataset. Although it doesn't have the most hours of delay on average, it has a much higher proportion of total flights to late delayed flights, at around 26%. ORD has the second to worse proportion of total flights to delayed flights at 23%



__Grand Question 2__ - What is the worst month to fly if you want to avoid delays?

December is the worst month to fly in in terms of proportion of delays at around 25.5% of all flights being delayed. June is the second worse month, with nearly 24% of flights being delayed. September is by far the best month to fly during the year, with only around 15% of flights being delayed. Months were forward filled in order to account for any missing month data.

CHART 2 -

![](worst_month_fly.png)




__Grand Question 3__ - What proportion of flights are caused by weather and unavoidable?

According to the BTS website the Weather category only accounts for severe weather delays. Other “mild” weather delays are included as part of the NAS category and the Late-Arriving Aircraft category. 30% of all delayed flights in the Late-Arriving category are due to weather.From April to August, 40% of delayed flights in the NAS category are due to weather. The rest of the months, the proportion rises to 65%.

Taking those percentages into account we get:

CHART 3 -

| airport_code   |   severe |   mild_late |   mild_nas |   weather |
|:---------------|---------:|------------:|-----------:|----------:|
| ATL            |    32375 |       79596 |   211745   |    323716 |
| DEN            |    13836 |       79596 |    81270.7 |    174703 |
| IAD            |     4794 |       79596 |    26597.6 |    110988 |
| ORD            |    20765 |       79596 |   208144   |    308505 |
| SAN            |     4320 |       79596 |    23420.2 |    107336 |
| SFO            |    10377 |       79596 |   111966   |    201939 |
| SLC            |     6831 |       79596 |    29679.4 |    116106 |

Atlanta has the most delays caused by weather, followed by Chicago O'Hare and San Francisco. 


__Grand Question 4__ - Create a barplot showing the proportion of all flights that are delayed by weather at each airport. What do you learn from this graph (Careful to handle the missing Late Aircraft data correctly)?

CHART 4 -


![](airport_weather.png)

Atlanta is apparently the airport that suffers the most weather delays out of the listed airports, followed by ORD and then SFO. 

__Grand Question 5__ - How do I clean up my data? 


{
         "index": 919,
         "airport_code": "IAD",
         "airport_name": "Washington, DC: Washington Dulles International",
         "month": "December",
         "year": 2015.0,
         "num_of_flights_total": 2799,
         "num_of_delays_carrier": "182",
         "num_of_delays_late_aircraft": 183,
         "num_of_delays_nas": 61,
         "num_of_delays_security": 0,
         "num_of_delays_weather": 17,
         "num_of_delays_total": 443,
         "minutes_delayed_carrier": null,
         "minutes_delayed_late_aircraft": 15438,
         "minutes_delayed_nas": 2826.0,
         "minutes_delayed_security": 0,
         "minutes_delayed_weather": 1825,
         "minutes_delayed_total": 31164
      },

This is an example entry in JSON of the data I was dealing with. As you can see the 'minutes_delayed_carrier' column is filled with an "null" which causes problems when trying to manipulate the dataset using pandas. There were also entries of "n/a" and "null" in the minutes_delayed_nas, month, year, and num_of_delays_late_aircraft columns. Using the code shown here:
```python
# make all empty cells of num_of_delays_late_aircraft the average for that airport
df.num_of_delays_late_aircraft = (df
   .groupby('airport_code')
   .transform(lambda x: x.fillna(x.mean())
   )
)
# make all empty cells of minutes_delayed_carrier the average for that airport
df.minutes_delayed_carrier = (df
    .groupby('airport_code')
    .transform(lambda x: x.fillna(x.mean())
     )
)
# make all empty cells of minutes_delayed_nas the average for that airport
df.minutes_delayed_nas = (df
    .groupby('airport_code')
    .transform(lambda x: x.fillna(x.mean())
    )
)
# forward the data from previous cells of 'year' column into empty cells
df.year = df.year.fillna(method = "ffill").sum()

```
I was able to replace those empty cells with the average number for that column or forward fillthem so as to not disturb the data too much.

Shown below is the modified JSON entry for the same index (919) after cleaning up the data:

 {
         "index": 919,
         "airport_code": "IAD",
         "airport_name": "Washington, DC: Washington Dulles International",
         "month": "December",
         "year": 1857236.0,
         "num_of_flights_total": 2799,
         "num_of_delays_carrier": "182",
         "num_of_delays_late_aircraft": 2015.0,
         "num_of_delays_nas": 61,
         "num_of_delays_security": 0,
         "num_of_delays_weather": 17,
         "num_of_delays_total": 443,
         "minutes_delayed_carrier": 2015.0,
         "minutes_delayed_late_aircraft": 15438,
         "minutes_delayed_nas": 2015.0,
         "minutes_delayed_security": 0,
         "minutes_delayed_weather": 1825,
         "minutes_delayed_total": 31164
      },

## APPENDIX A (FULL PYTHON SCRIPT)

```python
# %%
import pandas as pd 
import numpy as np
import altair as alt
import urllib3
import json



# %%
url = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json"
http = urllib3.PoolManager()
response = http.request('GET', url)
data_json = json.loads(response.data.decode('utf-8'))
df = pd.DataFrame.from_records(data_json)
columns = list(df)



# %%
#grand question # 5

result = df.to_json(orient="table")
parsed = json.loads(result)
print(json.dumps(parsed,indent=3))


# %%
#grand question #1
# get help on this ____>>

df_q1 = df.groupby('airport_code').agg({'num_of_flights_total' : 'sum', 'num_of_delays_total' : 'sum', 'minutes_delayed_total' : 'mean'})
    
#df_q2 = df_q1.assign(proportion_of_delays = df.num_of_delays_total / df.num_of_flights_total, hours_delayed_av = df.minutes_delayed_total / 60)

df_q1['proportion_of_delays'] = round(df_q1['num_of_delays_total'] / df_q1['num_of_flights_total'],2)
df_q1['hours_delayed_average'] = round(df_q1['minutes_delayed_total'] / 60, 2)


dtype = df_q1.convert_dtypes(convert_string = True).to_markdown()
print(dtype)


# %%

# grand question #2

list_of_months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
clean_month = df.assign(month = df.month.replace('n/a', np.nan) )
drop_month = clean_month.dropna(subset = ['month']) #then drop the NAs
month_assign =  drop_month.assign(
    proportion_of_delayed = drop_month.num_of_delays_total/drop_month.num_of_flights_total,
)
month = month_assign.groupby('month').proportion_of_delayed.mean().reset_index()
month_prop = (alt.Chart(month)
  .encode(
    x = alt.X("month", sort= list_of_months , title = "Month"),
    y = alt.Y("proportion_of_delayed", axis=alt.Axis(format="%"), title = "Proportion of delayed flights", scale = alt.Scale(zero = False)),
    )
  .properties(width=500, title = "The worst months to Fly")
  .mark_bar(size = 5, color = "black")
)



# %%
#grand question #3

df_q3 = df.assign(
    late_aircraft_na = lambda x: x.num_of_delays_late_aircraft.replace(-999, 0), # bad example
    severe = lambda x: x.num_of_delays_weather,
    mild_late = lambda x: x.late_aircraft_na * 0.3,
    mild_nas = lambda x: np.where(
        x.month.isin(["April", "May","June","July","August"]),
        x.num_of_delays_nas * 0.4,
        x.num_of_delays_nas * 0.65),
    weather = lambda x: x.severe + x.mild_late + x.mild_nas
).filter(['airport_code','month','severe','mild_late',
'mild_nas','weather'])

df_q3_md = df_q3.groupby("airport_code").agg({'severe' : 'sum', 'mild_late' : 'sum', 'mild_nas' : 'sum', 'weather' : 'sum'})
dtape = df_q3_md.convert_dtypes(convert_string = True).to_markdown()
print(dtape)


# %% 
#grand question #4

df_q4 = (df_q3
    .filter(items = ['airport_code', 'weather']))

df_q4_chart = alt.Chart(df_q4).mark_bar().encode(
    x = 'airport_code',
    y = 'weather'
)


```