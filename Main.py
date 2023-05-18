"""
=================================================================================================================================================
Equity Score V1.0 By Adam Fleischer 
    Runs all other assoicated programs
=================================================================================================================================================
CHANGELOG:
V1.0 [04-24-2023]
    * Created main program
    * Added answer processing outputed through the GUI versus the CLI
=================================================================================================================================================
IDEAS:
    *
=================================================================================================================================================
"""
import ESGUI as g
import Census_Data_Puller as cdp


#Main var storage

var_dict = {}
geo_dict = {}
results = {}
urls = {}
answer_GUI = {}


#tracts: 018700 (ca) , 051400 (wake) , 930401 (cherokee)

def main(): 
    g.GUI_input(var_dict,geo_dict)
    cdp.data(var_dict)

    if geo_dict['gtype'] == 'Zip Code':
        print(geo_dict)
        cdp.link_creation_zip_code(geo_dict,var_dict,urls)
        cdp.data_processing(urls,var_dict,results)
        for variable in var_dict["variables"]:
            a = variable
            print(a)
            b = geo_dict['zip_code']
            result = results[variable]
            c = str(result[variable])
            answer = f"The total {a} in Zip Code {b} is {c}"
            answer_GUI[variable] = answer
            print(answer_GUI)
        g.GUI_Result(answer_GUI)

    if geo_dict['gtype'] == 'Tract':
        cdp.geography(geo_dict)
        print(geo_dict)
        cdp.link_creation_tract(geo_dict,var_dict,urls)
        cdp.data_processing(urls,var_dict,results)
        for variable in var_dict["variables"]:
            a = variable
            b = geo_dict['tract']
            c = geo_dict['county_n']
            d = geo_dict['state_n']
            e = str(results[variable])
            answer = f"The total {a} in tract {b}, {c} County, {d} is {e}."
            answer_GUI[variable] = answer
        print(answer_GUI)
        g.GUI_Result(answer_GUI)



   
#=============================================================================
# MAIN PROGRAM
#=============================================================================
if __name__ == '__main__':
    main()



#=============================================================================
# NOTES
#=============================================================================

'Sample URL - https://api.census.gov/data/2021/acs/acs5?get=B01001_001E&for=tract:930401&in=state:37%20county:039&key=c894b42f112755eaca5d3957f0b7b7de6a47b16f'