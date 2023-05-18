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


#=================================================================================================================================================#
#                                                                                                                                                 #
#                                                Functions to pull data from Census                                                               #
#                                                                                                                                                 #
#=================================================================================================================================================#
def data(var_dict):
    """
    Creates the part of the URL dealing with what variables are being pulled

    Returns dictionary containing: data[specific dataset], acs_type[1 or 5 year estimate], year[data collection year], variables_n[english name of variable], variables_api[variable code]
    """
    vars = []
    variables = {}

    vars = var_dict['name'].split(",")

    for name in vars:
        name = name.strip()
        with open('Lookup_Tables/Variable_List.csv','r',newline= '') as vl:
            var_list = csv.DictReader(vl)
            for row in var_list:
                list1 = []
                if row['Variable'] == name:
                    list1.append(row['Code'])
                    list1.append(row['Survey'])
                    variables[name] = list1

    var_dict["variables"] = variables
    print(variables)

def geography(geo_dict):
    """
    Creates the part of the URL that specifies location of data

    Returns dictionary containing: state_n[english state name], state_api[state code], county_n[english county name], county_api[county code], tract[census tract number]
    """
    with open('Geo_Codes/StateList.csv','r',newline='') as sl:
        counties_list = csv.DictReader(sl)
        for row in counties_list:
            if row['State'] ==  geo_dict['state_n']:
                code = row['Code']
    geo_dict['state_api'] = code

    county_file = 'Geo_Codes/County_Lists/' + geo_dict['state_api'] + '.csv'
    with open(county_file,'r',newline='') as cl:
        counties_list = csv.DictReader(cl)
        for row in counties_list:
            if row['County Name'] ==  geo_dict['county_n']:
                code = row['Code']

    geo_dict['county_api'] = code.zfill(3)
    return


def link_creation_tract(geo_dict,var_dict,urls):
    """
    Creates the URL from data and geography functions

    Returns the URL 
    """
    for variable in var_dict["variables"]:
        
        host = 'https://api.census.gov/data'
        year = var_dict['year']
        year = '/' + year
        survey = var_dict["variables"][variable][1]
        if survey == 'acs5' or 'acs1':
            dataset = '/acs/' + survey
        else:
            dataset = '/' + survey
        code = var_dict["variables"][variable][0]
        g = '?get='
        f = '&for=tract:'
        i = '&in=state:'
        c = '%20county:'
        key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'

        url = f"{host}{year}{dataset}{g}{code}{f}{geo_dict['tract']}{i}{geo_dict['state_api']}{c}{geo_dict['county_api']}{key}"
        urls[variable] = url
    
    print(urls)
    return urls

def link_creation_zip_code(geo_dict,var_dict,urls):
    for variable in var_dict["variables"]:
        host = 'https://api.census.gov/data'
        year = '/' + var_dict['year']
        survey = var_dict["variables"][variable][1]
        if survey == 'acs5' or 'acs1':
            dataset = '/acs/' + survey
        else:
            dataset = '/' + survey
        code = var_dict["variables"][variable][0]
        g = '?get='
        f = '&for=zip%20code%20tabulation%20area:'
        key = '&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'
       
        url = f"{host}{year}{dataset}{g}{code}{f}{geo_dict['zip_code']}{key}"
        urls[variable] = url 
 
    print(urls)
    return urls
    

def data_processing(urls,var_dict,results):
    """
    Gets data using URL from link_creation function and parses it from JSON into a usable string

    Result from query as a string
    """
    
    for variable in var_dict["variables"]:
        data = requests.get(urls[variable])
        result = data.json()
        result = result[1]
        result = result[0]
        print(result)
        results[variable] = result
        print(results)

    return results

