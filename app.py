# firstly, create virtual environment in an ide, ensure latest version of python is installed, and in terminal of virtual environment run 'pip install cassiopeia', 'pip install pandas', and 'pip install numpy', and then run this script. Remove dash from last line to download csv of data.
import cassiopeia as cass
import pandas as pd
import numpy as np

# paste api key below, to be retrived from gcp secret manager in future
cass.set_riot_api_key("")

# specify region and summoner name
region="EUW"
summoner_name = "SpicyChickenTodd"
summoner = cass.get_summoner(name=summoner_name, region=region)

champion_id_to_name_mapping = {
        champion.id: champion.name for champion in cass.get_champions(region=region)
    }

champions = {"champion":[], "games":[], "kda":[], "csm":[], "deaths":[]}

# specify number of matches to look back at with right hand number, 5 for example looks at last 5 matches
matches = summoner.match_history[0:100]
for m in matches:
  champion_name = champion_id_to_name_mapping[m.participants[summoner].champion.id]
  if m.participants[summoner].stats.kills == 0:
    kda = 0
  elif m.participants[summoner].stats.deaths == 0:
    kda = m.participants[summoner].stats.kills
  else:
    kda = round((m.participants[summoner].stats.kills / m.participants[summoner].stats.deaths), 2)
  kills = m.participants[summoner].stats.kills
  deaths = m.participants[summoner].stats.deaths
  creeps = int(m.participants[summoner].stats.total_minions_killed)+int(m.participants[summoner].stats.neutral_minions_killed)
  minutes = round(float(m.duration.seconds/60), 3)
  csm = round(creeps/minutes, 1)

  champions["champion"].append(champion_name)
  champions["games"].append(1)
  champions["kda"].append(kda)
  champions["csm"].append(csm)
  champions["deaths"].append(deaths)

df = pd.DataFrame (champions, columns = ['champion', 'games', 'kda', 'csm', 'deaths'])

df = round(df.groupby("champion").agg({"games": [np.sum], "csm": [np.mean], "kda": [np.mean], "deaths": [np.mean]}), 2)
df = df.set_axis(['games', 'csm', 'kda', 'deaths'], axis=1, inplace=False)
df = df.sort_values(by='games', ascending=False)
print(df.head(5))

# df.to_csv('data.csv')
