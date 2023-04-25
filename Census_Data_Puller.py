"""
=================================================================================================================================================
Census Data Lookup V1.2 By Adam Fleischer 
    Takes user inputs to create a query using the Census API and outputs a sentance with the result
=================================================================================================================================================
DOCUMANTATION: https://www.census.gov/content/dam/Census/data/developers/api-user-guide/api-guide.pdf
=================================================================================================================================================
CHANGELOG:
V1.2 [04-21-2023]
    * Added multiple geography support

V1.1 [04-17-2023]
    * Converted states list to csv files
    * Fixed bug where result was reading the state code instead of the data
V1.0 [04-16-2023]
    * Added English state and county names conversion into FIPS code (CA and NC only)
    * Added API link
    * Proper formating in functions added
    * Result conversion from JSON to English
=================================================================================================================================================
IDEAS:
    * Add rest of county lists
    * Support for cities? Metro Areas? Tribal Areas? 
    * Support for multiple geographies in one search?
    * 2+ Variable Support
    * Create output to be sent over to other .py files (for final product)
    * Change acs type so that its acs + 1 or 5
=================================================================================================================================================
"""

#Import Statments 
import requests
import csv

#Variable Lookup
variable_dict = {"Population" : 'B01001_001E', 'Poverty' : 'B06012_002E'}


#=================================================================================================================================================#
#                                                                                                                                                 #
#                                                Functions to pull data from Census                                                               #
#                                                                                                                                                 #
#=================================================================================================================================================#
def data(ds):
    """
    Creates the part of the URL dealing with what variables are being pulled

    Returns dictionary containing: data[specific dataset], acs_type[1 or 5 year estimate], year[data collection year], variables_n[english name of variable], variables_api[variable code]
    """
    vars = {}
    vars_l = ds['variables_n'].split(',')
    length = len(vars_l)

    for item in vars_l:
       item = item.strip()
       vars[item] = variable_dict[item]
    
    print(vars)

    ds['variables_api'] = vars
    ds['length'] = length


def geography(ds):
    """
    Creates the part of the URL that specifies location of data

    Returns dictionary containing: state_n[english state name], state_api[state code], county_n[english county name], county_api[county code], tract[census tract number]
    """
    with open('EquityScore/Geo_Codes/StateList.csv','r',newline='') as sl:
        counties_list = csv.DictReader(sl)
        for row in counties_list:
            if row['State'] ==  ds['state_n']:
                code = row['Code']
    ds['state_api'] = code

    county_file = 'EquityScore/Geo_Codes/County_Lists/' + ds['state_api'] + '.csv'
    with open(county_file,'r',newline='') as cl:
        counties_list = csv.DictReader(cl)
        for row in counties_list:
            if row['County Name'] ==  ds['county_n']:
                code = row['Code']

    ds['county_api'] = code.zfill(3)
    return


def link_creation_tract(ds):
    """
    Creates the URL from data and geography functions

    Returns the URL 
    """
    url_var = ""


    host = 'https://api.census.gov/data'
    year = '/' + ds['year']
    dataset = '/' + ds['data'] + '/' + ds['acs_type']
    g = '?get='

    for value in ds['variables_api'].values():
        url_var = url_var + value + ","
    url_var = url_var[0:(len(url_var) - 1)]

    f = '&for=tract:'
    i = '&in=state:'
    c = '%20county:'
    key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'

    url = f"{host}{year}{dataset}{g}{url_var}{f}{ds['tract']}{i}{ds['state_api']}{c}{ds['county_api']}{key}"

    return url

def link_creation_zip_code(ds):
    url_var = ""
    
    host = 'https://api.census.gov/data'
    year = '/' + ds['year']
    dataset = '/' + ds['data'] + '/' + ds['acs_type']
    g = '?get='

    for value in ds['variables_api'].values():
        url_var = url_var + value + ","
    url_var = url_var[0:(len(url_var) - 1)]
    print(url_var)

    f = '&for=zip%20code%20tabulation%20area:'
    key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'


    url = f"{host}{year}{dataset}{g}{url_var}{f}{ds['zip_code']}{key}"    
 
    print(url)
    return url
    

def data_processing(url,ds):
    """
    Gets data using URL from link_creation function and parses it from JSON into a usable string

    Result from query as a string
    """

    data = requests.get(url)
    result = data.json()
    result = result[1]
    print(result)
    result = result[0:int(ds['length'])]

    ds['result'] = result

    return ds

