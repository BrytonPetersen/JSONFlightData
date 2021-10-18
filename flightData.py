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

''' Fix all of the varied NA types in the data to be consistent and save the file back out in the same format that was provided (this file shouldn’t have the missing values replaced with a value). Include one record example from your exported JSON file that has a missing value (No imputation in this file).'''

result = df.to_json(orient="table")
parsed = json.loads(result)
print(json.dumps(parsed,indent=3))




# %% 
#clean up the dataframe 
x = pd.DataFrame(df.isnull().sum())
y = pd.DataFrame(df.isna().sum())

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
#grand question #2

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
    size = 'proportion_of_delayed'
    )
  .properties(width=500, title = "The worst months to Fly")
  .mark_trail()
)



# %%
#grand question #3
''' According to the BTS website the Weather categopry only accounts for severe weather delays. Other “mild” weather delays are included as part of the NAS category and the Late-Arriving Aircraft category. Calculate the total number of flights delayed by weather (either severe or mild) using these two rules:

30% of all delayed flights in the Late-Arriving category are due to weather.
From April to August, 40% of delayed flights in the NAS category are due to weather. The rest of the months, the proportion rises to 65%.'''

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
#grand question #4 -Create a barplot showing the proportion of all flights that are delayed by weather at each airport. What do you learn from this graph (Careful to handle the missing Late Aircraft data correctly)?

df_q4 = (df_q3
    .filter(items = ['airport_code', 'weather']))

df_q4_chart = alt.Chart(df_q4).mark_bar().encode(
    x='weather:Q',
    y = alt.Y('airport_code', sort = '-x')
)




# %%
result = df.to_json(orient="table")
parsed = json.loads(result)
print(json.dumps(parsed,indent=3))
# %%
