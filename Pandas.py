import csv
import requests
import numpy as np
import pandas as pd
import math

# Holder Vars
url = ""

#Functions
def link_creation_tract(geo_list,var_list):
    """
    Creates the URL from data and geography functions

    Returns the URL 
    """
    vars_url = ""
    for var in var_list:
        vars_url = vars_url + str(var) + ","
    
    vars_url = vars_url[:-1]
    
    county = str(geo_list[1])
    county = county.zfill(3)

    tract = str(geo_list[2])
    tract = tract.zfill(6)


    host = 'https://api.census.gov/data/2021/acs/acs5'
    code = vars_url
    g = '?get='
    f = '&for=tract:'
    i = '&in=state:'
    c = '%20county:'
    key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
    url = f"{host}{g}{code}{f}{tract}{i}{geo_list[0]}{c}{county}{key}"

    # https://api.census.gov/data/2021/acs/acs5?get=B01001_001E,B06012_002E&for=tract:020400&in=state:37%20county:065&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
    
    data = requests.get(url)
    result = data.json()
    result = result[1]
    return result


#Making the DataFrame and getting a time estimate
df = pd.read_csv('NC_CT.csv',usecols=[1,2,3])
estimated_time = round(0.624220536 * len(df.index))

if estimated_time >= 60:
    estimated_time = estimated_time/60
    time = list(math.modf(estimated_time))
    print("Estimated time to process is " + str(time[1])[:-2] + " minutes and", str(round((time[0]*60))) + ' seconds')
else:
    print(str(estimated_time) + " seconds")

var_list = ["B01001_001E","B06012_002E",'B08015_001E']


for item in var_list:
    df1 = df.insert(loc=len(df.columns),column=item,value=0)


#Obtaining Data
for index,row in df.iterrows():
    geo_list = []
    tract = str(row['TRACTCE']).zfill(6)
    df.at[index,'TRACTCE'] = tract
    geo_list.append(row["STATEFP"])
    geo_list.append(row["COUNTYFP"])
    geo_list.append(row["TRACTCE"])

    result = link_creation_tract(geo_list,var_list)

    df.at[index,'B01001_001E'] = result[0]
    df.at[index,'B06012_002E'] = result[1]

var_list = ["B01001_001E","B06012_002E"]
column_names = {}
for name in var_list:
    with open('Lookup_Tables/Variable_List.csv','r',newline= '') as vl:
        var_sheet = csv.DictReader(vl)
        for row in var_sheet:
            if row['Code'] == name:
                v = row["Variable"]
                column_names[name] = v

print(column_names)

for var in var_list:
    df[var] = df[var].astype(float)

df2 = df.rename(columns=column_names)

print(df2.head(5))

df2.to_excel('RockyMountData.xlsx')
