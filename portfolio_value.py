import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid')

# Paste in file path between quotes
portfolio_file = r''

api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

# Read in the portfolio table
pfdf = pd.read_csv(portfolio_file, sep='\t')

# Loop over the Name column and retrieve the value per coin (vpc)
current_values = []
for coin in pfdf['Name'].unique():
    coin_url = api_url.replace('bitcoin', coin.lower())
    response = requests.get(coin_url)
    response_json = response.json()
    data = response_json[0]
    current_values.append(float(data['price_usd']))
pfdf['Current VPC'] = current_values
pfdf['Current USD Value'] = pfdf['Total Balance'] * pfdf['Current VPC']

# Current portfolio value
PV = pfdf['Current USD Value'].sum()
# Display it
print(pfdf)
print()
print("Current portfolio value: {}".format(PV))

# Make a plot
fig, ax = plt.subplots()
sns.barplot(x='Coin', y='Current USD Value', data=pfdf.sort_values(by='Current USD Value', ascending=False))
txtypos = pfdf['Current USD Value'].max() * 0.95
ax.text(x=len(pfdf.columns), y=txtypos, s='Total value: ${}'.format(round(PV, 2)))
ax.set_title("Portfolio Summary")
sns.despine()
plt.show()
