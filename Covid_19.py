import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")
deaths = pd.read_csv("time_series_covid19_deaths_global.csv")
recover= pd.read_csv("time_series_covid19_recovered_global.csv")
def preprocess(df, value_name):
    df_long = df.drop(['Province/State', 'Lat', 'Long'], axis=1).groupby('Country/Region').sum().reset_index()
    df_long = df_long.melt(id_vars=['Country/Region'], var_name='Date', value_name=value_name)
    df_long['Date'] = pd.to_datetime(df_long['Date'], format="%m/%d/%y")
    return df_long
confirmed_long = preprocess(confirmed, 'Confirmed')
deaths_long = preprocess(deaths, 'Deaths')
merged = confirmed_long.merge(deaths_long, on=['Country/Region', 'Date'])
merged['Recovered'] = merged['Confirmed'] - merged['Deaths']
merged['Recovered'] = merged['Recovered'].clip(lower=0)  
global_daily = merged.groupby('Date')[['Confirmed', 'Recovered', 'Deaths']].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=global_daily, x='Date', y='Confirmed', label='Confirmed')
sns.lineplot(data=global_daily, x='Date', y='Recovered', label='Recovered (Estimated)')
sns.lineplot(data=global_daily, x='Date', y='Deaths', label='Deaths')
plt.title("Global COVID-19 Trends Over Time")
plt.ylabel("Number of Cases")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.show()
global_daily.set_index("Date")[["Confirmed", "Recovered", "Deaths"]].plot.area(
    stacked=True, figsize=(12, 6), alpha=0.6)
plt.title("Global COVID-19 Cumulative Cases Over Time (Stacked Area)")
plt.ylabel("Number of Cases")
plt.xlabel("Date")
plt.grid(True)
plt.tight_layout()
plt.show()
top_countries = merged.groupby('Country/Region')['Confirmed'].max().sort_values(ascending=False).head(5).index
country_data = merged[merged['Country/Region'].isin(top_countries)]

plt.figure(figsize=(12, 6))
for country in top_countries:
    country_group = country_data[country_data['Country/Region'] == country].groupby('Date')['Confirmed'].sum()
    plt.plot(country_group.index, country_group.values, label=country)

plt.title("Top 5 Countries with Highest Confirmed Cases")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
latest_date = merged['Date'].max()
latest_data = merged[merged['Date'] == latest_date]
top_countries = latest_data.sort_values('Confirmed', ascending=False).head(10)

heatmap_data = top_countries[['Country/Region', 'Confirmed', 'Recovered', 'Deaths']].set_index('Country/Region')

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title(f"Top 10 Countries - COVID-19 Summary on {latest_date.strftime('%Y-%m-%d')}")
plt.tight_layout()
plt.show()
#merged.to_csv("covid_country_level_data.csv", index=False)
#global_daily.to_csv("covid_global_daily.csv", index=False)

