#=============================================================================
# Imports
#=============================================================================
import CDPPandas as CDPP
import ExcelGUI as EGUI
GUIDict = {}
#GUIDict = {'VarList': 'Test', 'fileInput': 'PalmBeachCountyPlaces.csv', 'fileOutput': 'C:/Users/Weath/Desktop/PalmBeachPlacesHomeValue.xlsx'}
var_list = []

def main():
    EGUI.GUI_One(GUIDict)

    inputs = CDPP.sorter(GUIDict)

    if inputs[0] == 'bg':
        outputs = CDPP.blockgroup(inputs)
 
    elif inputs[0] == 't':
        outputs = CDPP.tract(inputs)

    elif inputs[0] == 'c':
        outputs = CDPP.county(inputs)

    elif inputs[0] == 'p':
        outputs = CDPP.places(inputs)
    
    elif inputs[0] == 's':
        outputs = CDPP.state(inputs)
    
    elif inputs[0] == 'z':
        outputs = CDPP.ZCTA(inputs)


    CDPP.cleaner(GUIDict,outputs)
 
    
#=============================================================================
# MAIN PROGRAM
#=============================================================================
if __name__ == '__main__':
    main()