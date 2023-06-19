#=============================================================================
# Imports
#=============================================================================
import CDPPandas as CDPP
import ExcelGUI as EGUI

GUIDict = {}

def main():
    #EGUI.GUI_One(GUIDict)
    #print(GUIDict)
    GUIDict = {'VarList': 'Basic Demographics', 'fileInput': 'C:/Users/Weath/Documents/GitHub/EquityScore/Rocky_Mount_CDP.csv', 'fileOutput': 'C:/Users/Weath/Desktop/NewFile.xlsx'}
    CDPP.CensusPanda(GUIDict)

#=============================================================================
# MAIN PROGRAM
#=============================================================================
if __name__ == '__main__':
    main()