## Equity Score V2.0.0

### **WORKS WITH CSVs ONLY**

Program specifically now works to take a large amount of geographies and variables to output an Excel file for use in other programs for analysiss. 

#### How to use:
  1. Download repository (good tutorial : https://blog.hubspot.com/website/download-from-github) 
  2. Unzip folder
  3. Open MainCSV.py and start the program (will require a coding editor such as Visual Studio or Eclipse)
  4. Enter inputs as requested
  5. Hit submit
  
#### Limitations:
  * Removed the singular variable/geography feature, just not the best use of the program but will likely add a more refined version later.
  * Does not work with metropolitan areas or zip codes
  * In the CSV only one type of geography is allowed right now, working to make it a smarter
  * Works best with US Census Bureau TIGER Shapefile format as it contains the necessary information for the program to properly work, conversion of a large amount of geographies to FIPS codes is a work in progress

#### Notes:
  * If there are any issues please add them to the issues list
  * Getting a lot of data takes time, if running more than 100 geographies expect it to take 4-5+ minutes
  * Variables used in the presets are in CSV files with those preset names, if custom variables are desired then enter the Census Bureau's code into var_listt list at the top of CDPPandas.py and select test in the GUI
