#Required improts
import requests
import json
import time
import pandas as pd
import numpy as np

#Riot API information
api_key = ""
region_f1 = "EUW1"
region_f2 = "EUROPE"

#Getting some Summuners IDs
def summ_ID_puller(tier,division,page):
    url_pull = "https://{}.api.riotgames.com/tft/league/v1/entries/{}/{}?page={}&api_key={}".format(region_f1,tier,division,page,api_key)
    profile_list = requests.get(url_pull).json()
    num_profiles = len(profile_list)
    summID_list = []
    
    for profile in range(0,num_profiles):
        summID_list.append(profile_list[profile]['summonerId'])
        
    df = pd.DataFrame(summID_list,columns = ["Summoner ID"])
    df.to_csv('summID.csv',mode = 'a')


for division in ["I","II","III","IV"]:
    for page in range(1,20):
        time.sleep(1.5)
        print('Capturing Diamond elo, division: ', division, ' page: ', page)
        summ_ID_puller("DIAMOND",division,page)

print('Finished Capturing summuners IDs.')
summoner_IDs = pd.read_csv("summID.csv")
PuuID_list = []

#Getting puuids from Summunder IDs
def acct_puuID_puller(summID):
    url_acct_pull = "https://{}.api.riotgames.com/tft/summoner/v1/summoners/{}?api_key={}".format(region_f1,summID,api_key)
    account_info = requests.get(url_acct_pull).json()
    PuuID_list.append(account_info["puuid"])

print('Getting Summuners PuuIds!')
t = 0
summID_list = summoner_IDs["Summoner ID"]

for summID_idx in range(0,10000):
    time.sleep(1.5)
    if summID_list[summID_idx] == "Summoner ID":
        pass
    
    else:
        try:
            acct_puuID_puller(summID_list[summID_idx])
            t += 1
            print(t, "/10000")
        except KeyError:
            print("keyerror")

print('Finished getting summuners PuuIDs, we Got : ', t, '!')
df = pd.DataFrame(PuuID_list, columns = ["PuuId"])
df.to_csv('accountPuuId.csv',mode = 'a')

#Getting last 7 matches for each player
account_PuuIDs = pd.read_csv("accountPuuId.csv")
account_PuuIDs_list = account_IDs["PuuId"]

matchID_list = []
pull_errors = []

def match_ID_puller(acctpuuid):    
    url_match_pull = "https://{}.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids?count=10&api_key={}".format(region_f2,acctpuuid,api_key)
    match_history = requests.get(url_match_pull).json()
    for i in range(0,7):        
        try:
            match_id = match_history[i]
            matchID_list.append(match_id)
            
        except KeyError:
            print(match_history)
            print("KeyError occured with account:",acctpuuid) 
            pull_errors.append(match_history)

t = 0
for acct_puuid in account_PuuIDs_list:
    time.sleep(1.5)
    if acct_id == "PuuId":
        pass
    else:
        match_ID_puller(acct_id)
        t += 1
        print(t, "/", len(account_PuuIDs_list))

df = pd.DataFrame(matchID_list, columns = ["MatchId"])
df.to_csv('MatchId.csv',mode = 'a')
print("Done pulling matchIDs!")

#Getting match details
match_ids = pd.read_csv('MatchId.csv')
match_data = []
def get_match_json(matchid):
    url_pull_match = "https://{}.api.riotgames.com/tft/match/v1/matches/{}?api_key={}".format(region_f2,matchid,api_key)
    match_data_all = requests.get(url_pull_match).json()
    
    try:
        for i in range(8):
            match_data.append(match_data_all["info"]["participants"][i])
    
    except IndexError:
        return ["Skipping."]

match_ids = pd.read_csv('MatchId.csv')
#Taking from 20 match, the possible sets in the current patch
match_data_traits = []
match_data_traits_final = []
for i in range(20):
    matchid = match_ids["MatchId"][i]
    url_pull_match = "https://{}.api.riotgames.com/tft/match/v1/matches/{}?api_key={}".format(region_f2,matchid,api_key)
    match_data_all = requests.get(url_pull_match).json()
    for i in range(8):
        match_data_traits.append(match_data_all["info"]["participants"][i]["traits"])

for i in range(8):
    for j in match_data_traits[i]:
        match_data_traits_final.append(j["name"])
match_data_traits_final = list(dict.fromkeys(match_data_traits_final))

trait_counter = 0
match_data_traits = []
for trait in match_data_traits_final:
    trait_index = trait.find("_")
    print("trait number:",trait_counter + 1, "is:", trait[trait_index+1:])
    match_data_traits.append(trait[trait_index+1:])
    trait_counter += 1

match_ids = pd.read_csv('MatchId.csv')

column_titles = match_data_traits + ["placement"]

match_data = []

def match_info_puller(matchid):
    url_pull_match = "https://{}.api.riotgames.com/tft/match/v1/matches/{}?api_key={}".format(region_f2,matchid,api_key)
    match_data_all = requests.get(url_pull_match).json()
    for player in range(8):
        draft = match_data_all["info"]["participants"][player]
        placement = draft["placement"]
        i = 0
        new_list_element = [0] * len(column_titles[:-1])
        for i in range(len(draft["traits"])):
            trait_name = draft["traits"][i]["name"]
            column_index = 0
            r = -1
            for column in column_titles[:-1]:
                if column in trait_name:
                    r = column_index
                    break
                else:
                    column_index += 1
            if (r != -1):
                new_list_element[r] = draft["traits"][i]["num_units"]
            else:
                pass
        new_list_element += [placement]
        match_data.append(new_list_element)

match_ids = pd.read_csv('MatchId.csv')
match_ids = match_ids["MatchId"].drop_duplicates()
current = 0
end = len(match_ids)
for matchid in match_ids:
    time.sleep(1.5)
    if matchid == 'MatchId':
        pass
        
    else:
        current += 1
        try:
            match_info_puller(matchid)
            print(current, "/", end)
        except KeyError:
            print("KeyError")

match_data = np.array(match_data)
match_data.shape = -1,27 #may cause problems

df = pd.DataFrame(match_data, columns = column_titles)
df.to_csv('Match_data.csv',mode = 'a')

match_info = pd.read_csv('Match_data.csv')

x = list(match_info.columns[1:-1])

y = match_info.columns[-1]


trainX = match_info[x][:int((len(match_info)*80)/100)]
trainY = match_info[y][:int((len(match_info)*80)/100)]


testX = match_info[x][int((len(match_info)*80)/100)+1:]
testY = match_info[y][int((len(match_info)*80)/100)+1:]

clf = RandomForestClassifier(n_estimators=100)
clf = clf.fit(trainX,trainY)

correct = 0
incorrect = 0
difference = 0

for i in range(len(testX)):
    holder = [0] * 26
    for j in range(26):
        holder[j] = testX.iloc[i][j]
    x = int(clf.predict([holder]))
    if x == int(testY.iloc[i]):
        correct += 1
    else:
        incorrect += 1
        difference += abs(int(testY.iloc[i]) - x)


print ("correct : ",correct)
print ("incorrect : ",incorrect)
print ("incorrect : ",difference/incorrect)
