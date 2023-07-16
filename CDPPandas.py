import csv
import requests
import pandas as pd
import math

# Holder Vars
url = ""
var_list = []
#var_list = ["B01001_001E",'B02008_001E','B02009_001E','B02010_001E','B02011_001E','B02012_001E','B02013_001E','B02014_001E']
#var_list = ["B01001_001E","B17021_002E"]
var_listt = ["B25077_001E"]


#Functions

def TimeEstimate(infile):
    df = pd.read_csv(infile,usecols=[1,2,3])
    csv_length = len(df.index)
    estimated_time = round(0.624220536 * csv_length)

    if estimated_time >= 60:
        estimated_time = estimated_time/60
        time = list(math.modf(estimated_time))
        estimated_time = "Estimated time to process is " + str(time[1])[:-2] + " minutes and " + str(round((time[0]*60))) + ' seconds'
    else:
        estimated_time = str(estimated_time) + " seconds"

    return estimated_time, csv_length

def sorter(GUIDict):

    dfi = pd.read_csv(GUIDict['fileInput'])

    if dfi.columns[4] == 'BLKGRPCE':
        dfi = dfi.iloc[:, 1:5]
        types = 'bg'

    elif dfi.columns[3] == 'TRACTCE':
        dfi = dfi.iloc[:, 1:4]
        types = 't'

    elif dfi.columns[2] == 'COUNTYFP':
        dfi = dfi.iloc[:, 1:3]
        types = 'c'
    
    elif dfi.columns[2] == "PLACEFP":
        dfi = dfi.iloc[:, 1:3]
        types = 'p'

    elif dfi.columns[1] == 'ZCTA5CE20':
        dfi = dfi.iloc[:, 1:2]
        types = 'z'

    elif dfi.columns[1] == 'STATEFP':
        dfi = dfi.iloc[:, 1:2]
        types = 's'
    

    
    if GUIDict['VarList'] == "Basic Demographics":
            with open('Lookup_Tables\Basic_Demographics.csv','r',newline= '') as vl:
                var_sheet = csv.DictReader(vl)
                for row in var_sheet:
                    if row['Code'] != '':
                        var_list.append(row['Code'])
    elif GUIDict['VarList'] == "Test":
        for var in var_listt:
            var_list.append(var)
    
   

    df = pd.concat([dfi,pd.DataFrame(columns=var_list,)], axis=1)
    
    df1 = df.insert(loc=len(df.columns),column= "GEOID", value=0)

    print(df.head(5))

    return [types,var_list,df]

def blockgroup(inputs):
    var_list = inputs[1]
    df = inputs[2]
    chunked_list = list()
    chunk_size = 50

    for i in range(0, len(var_list), chunk_size):
        chunked_list.append(var_list[i:i+chunk_size])

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])

        county = str(row['COUNTYFP']).zfill(3)
        
        geo_list.append(county)

        tract = str(row['TRACTCE']).zfill(6)
        geo_list.append(tract)

        geo_list.append(row["BLKGRPCE"])


        #template: https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=block%20group:2&in=state:37%20county:039%20tract:930501&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
        #error:    
            



        for chunk in range(len(chunked_list)):
            host = 'https://api.census.gov/data/2021/acs/acs5'
            code = str(chunked_list[chunk]).rstrip(']').lstrip('[').replace("'","").replace(" ","")
            g = '?get='
            b = '&for=block%20group:'
            t = '%20tract:'
            s = '&in=state:'
            c = '%20county:'
            key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
            url = f"{host}{g}{code}{b}{geo_list[3]}{s}{geo_list[0]}{c}{geo_list[1]}{t}{geo_list[2]}{key}"
            print(url)


            data = requests.get(url)
            result = data.json()
            result = result[1]
            print(result)

            resultCounter = 0
            for var in chunked_list[chunk]:
                df.at[index,var] = result[resultCounter]
                resultCounter += 1

        
        GeoId = f"{str(geo_list[0])+ str(geo_list[1]).zfill(3) + str(geo_list[2]).zfill(6) + str(geo_list[3])}"
        #print(GeoId)
        df.at[index,'GEOID'] = GeoId
        
    print(df.head(5))
    #print(df.tail(5))

    outputs = [df,var_list]
    return outputs

def tract(inputs):
    var_list = inputs[1]
    df = inputs[2]
    chunked_list = list()
    chunk_size = 50

    for i in range(0, len(var_list), chunk_size):
        chunked_list.append(var_list[i:i+chunk_size])

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])

        county = str(row['COUNTYFP']).zfill(3)
        geo_list.append(county)

        tract = str(row['TRACTCE']).zfill(6)
        geo_list.append(tract)

        vars_url = ""
        for var in var_list:
            vars_url = vars_url + str(var) + ","
        
        vars_url = vars_url[:-1]

        #template: https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=tract:020400&in=state:37%20county:039&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
        for chunk in range(len(chunked_list)):
            host = 'https://api.census.gov/data/2021/acs/acs5'
            code = str(chunked_list[chunk]).rstrip(']').lstrip('[').replace("'","").replace(" ","")
            g = '?get='
            t = '&for=%20tract:'
            s = '&in=state:'
            c = '%20county:'
            key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
            url = f"{host}{g}{code}{t}{geo_list[2]}{s}{geo_list[0]}{c}{geo_list[1]}{key}"
            print(url)

            data = requests.get(url)
            result = data.json()
            result = result[1]
            print(result)

            result_counter = 0
            for var in var_list:
                df.at[index,var] = result[result_counter]
                result_counter += 1
            
            GeoId = f"{str(geo_list[0])+ str(geo_list[1]).zfill(3) + str(geo_list[2]).zfill(6)}"
            #print(GeoId)
            df.at[index,'GEOID'] = GeoId  

    print(df.head(5))
    print(df.tail(5))
    outputs = [df,var_list]
    return outputs

def county(inputs):
    var_list = inputs[1]
    df = inputs[2]
    chunked_list = list()
    chunk_size = 50

    for i in range(0, len(var_list), chunk_size):
        chunked_list.append(var_list[i:i+chunk_size])

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])

        county = str(row['COUNTYFP']).zfill(3)
        geo_list.append(county)

        vars_url = ""
        for var in var_list:
            vars_url = vars_url + str(var) + ","
        
        vars_url = vars_url[:-1]

        #template: https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=county:039&in=state:37&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
        for chunk in range(len(chunked_list)):
            host = 'https://api.census.gov/data/2021/acs/acs5'
            code = str(chunked_list[chunk]).rstrip(']').lstrip('[').replace("'","").replace(" ","")
            g = '?get='
            c = '&for=%20county:'
            s = '&in=state:'
            key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
            url = f"{host}{g}{code}{c}{geo_list[1]}{s}{geo_list[0]}{key}"
            #print(url)

            data = requests.get(url)
            result = data.json()
            result = result[1]
            #print(result)

            result_counter = 0
            for var in var_list:
                df.at[index,var] = result[result_counter]
                result_counter += 1
            
            GeoId = f"{str(geo_list[0])+ str(geo_list[1]).zfill(3)}"
            #print(GeoId)
            df.at[index,'GEOID'] = GeoId  

    print(df.head(5))
    print(df.tail(5))
    outputs = [df,var_list]
    return outputs

def state(inputs):
    var_list = inputs[1]
    df = inputs[2]
    chunked_list = list()
    chunk_size = 50

    for i in range(0, len(var_list), chunk_size):
        chunked_list.append(var_list[i:i+chunk_size])

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])

        vars_url = ""
        for var in var_list:
            vars_url = vars_url + str(var) + ","
        
        vars_url = vars_url[:-1]

        #template: https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=state:37&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
        for chunk in range(len(chunked_list)):
            host = 'https://api.census.gov/data/2021/acs/acs5'
            code = str(chunked_list[chunk]).rstrip(']').lstrip('[').replace("'","").replace(" ","")
            g = '?get='
            s = '&for=state:'
            key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
            url = f"{host}{g}{code}{s}{geo_list[0]}{key}"
            print(url)

            data = requests.get(url)
            result = data.json()
            result = result[1]
            print(result)

            result_counter = 0
            for var in var_list:
                df.at[index,var] = result[result_counter]
                result_counter += 1
            
            GeoId = f"{str(geo_list[0])}"
            #print(GeoId)
            df.at[index,'GEOID'] = GeoId  

    print(df.head(5))
    print(df.tail(5))
    outputs = [df,var_list]
    return outputs

def ZCTA(inputs):
    var_list = inputs[1]
    df = inputs[2]

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])
        geo_list.append(row["ZCTA5CE20"])

        vars_url = ""
        for var in var_list:
            vars_url = vars_url + str(var) + ","
        
        vars_url = vars_url[:-1]

        #template: https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=zip%20code%20tabulation%20area:28905&in=state:37&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f

        host = 'https://api.census.gov/data/2021/acs/acs5'
        code = vars_url
        g = '?get='
        z = '&for=zip%20code%20tabulation%20area:'
        s = '&for=state:'
        key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
        url = f"{host}{g}{code}{z}{geo_list[1]}{s}{geo_list[0]}{key}"
        print(url)

        data = requests.get(url)
        result = data.json()
        result = result[1]
        print(result)

        result_counter = 0
        for var in var_list:
            df.at[index,var] = result[result_counter]
            result_counter += 1
        
        GeoId = f"{str(geo_list[1])}"
        #print(GeoId)
        df.at[index,'GEOID'] = GeoId 

    print(df.head(5))
    print(df.tail(5))
    outputs = [df,var_list]
    return outputs

def places(inputs):
    var_list = inputs[1]
    df = inputs[2]
    chunked_list = list()
    chunk_size = 50

    for i in range(0, len(var_list), chunk_size):
        chunked_list.append(var_list[i:i+chunk_size])

    for index,row in df.iterrows():
        geo_list = []
        
        geo_list.append(row["STATEFP"])

        place = str(row['PLACEFP']).zfill(5)
        geo_list.append(place)

        vars_url = ""
        for var in var_list:
            vars_url = vars_url + str(var) + ","
        
        vars_url = vars_url[:-1]

        #template: https://api.census.gov/data/2021/acs/acs5?get=NAME,B01001_001E&for=place:75812&in=state:12&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f
        
        for chunk in range(len(chunked_list)):
            host = 'https://api.census.gov/data/2021/acs/acs5'
            code = str(chunked_list[chunk]).rstrip(']').lstrip('[').replace("'","").replace(" ","")
            g = '?get='
            c = '&for=place:'
            s = '&in=state:'
            key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
            url = f"{host}{g}{code}{c}{geo_list[1]}{s}{geo_list[0]}{key}"
            print(url)

            data = requests.get(url)
            result = data.json()
            result = result[1]
            print(result)

            result_counter = 0
            for var in var_list:
                df.at[index,var] = result[result_counter]
                result_counter += 1
            
            GeoId = f"{str(geo_list[0])+ str(geo_list[1]).zfill(5)}"
            #print(GeoId)
            df.at[index,'GEOID'] = GeoId  

    print(df.head(5))
    print(df.tail(5))
    outputs = [df,var_list]
    return outputs


def cleaner(GUIDict,outputs):
    df = outputs[0]
    var_list = outputs[1]
    
    column_names = {}
    for name in var_list:
        with open('Lookup_Tables\Basic_Demographics.csv','r',newline= '') as vl:
            var_sheet = csv.DictReader(vl)
            for row in var_sheet:
                if row['Code'] == name:
                    v = row["By"]
                    column_names[name] = v

    for var in var_list:
        df[var] = df[var].astype(float)

    df2 = df.rename(columns=column_names)

    #print(df2.head(5))

    df2.to_excel(GUIDict["fileOutput"])