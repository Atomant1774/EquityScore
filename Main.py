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
ds = {}


#tracts: 018700 (ca) , 051400 (wake) , 930401 (cherokee)

def main(): 
    g.GUI_input(ds)
    print(ds)
    cdp.data(ds)

    if ds['gtype'] == 'Zip Code':
        url = cdp.link_creation_zip_code(ds)
        cdp.data_processing(url,ds)
        a = ds['variables_n']
        b = ds['zip_code']
        c = ds['result']
        answer = f"The total {a} in Zip Code {b} is {c}"
        print(answer)
        g.GUI_Result(answer)

    if ds['gtype'] == 'Tract':
        cdp.geography(ds)
        url = cdp.link_creation_tract(ds)
        cdp.data_processing(url,ds)
        a = ds['variables_n']
        b = ds['tract']
        c = ds['county_n']
        d = ds['state_n']
        e = ds['result']
        answer = f"The total {a} in tract {b}, {c} County, {d} is {e}."
        g.GUI_Result(answer)



   
#=============================================================================
# MAIN PROGRAM
#=============================================================================
if __name__ == '__main__':
    main()




