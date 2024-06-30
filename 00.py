import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table  = soup.find('table', {'class': 'table'})

# rows = table.find_all('tr')
rows = table.find_all('tr')


data=[]
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=['Party', 'Won', 'Leading', 'Total'])

df.to_csv('lok_sabha_elections.csv', index=False)

print(df)
df['Won'] = pd.to_numeric(df['Won'])
df['Total'] = pd.to_numeric(df['Total'])

insights = []

most_seats = df.loc[df['Won'].idxmax()]
# insights.append(f'The party with most seats is {most_seats['Party']} with {most_seats['Won']}')
insights.append(f"The party with most seats is {most_seats['Party']} with {most_seats['Won']} seats.")

for i, insights in enumerate(insights, 1):
    print(f"insights {i}: {insights}")

with open('lok_sabha_elections.txt', 'w') as f:
    for i, insights in enumerate(insights, 1):
        f.write(f"Insight{i}:{insights}")

