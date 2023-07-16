"""
=================================================================================================================================================
Excel GUI V1.0 By Adam Fleischer 
    Is the frontfacing input for the Census API for spreadsheet entry
=================================================================================================================================================
CHANGELOG:

=================================================================================================================================================
IDEAS:
    * Create new file after program has run, not at start up
=================================================================================================================================================
"""
#Imports
import tkinter as tk
import customtkinter as ctk
from CDPPandas import TimeEstimate

def GUI_One(GUIDict):
    #inputs / Title Bar
    input = ctk.CTk()
    input.title("Census Data Puller")


    #Empty Var
    EstTime = ctk.StringVar()
    FileInput = ctk.StringVar()
    FileOutput = ctk.StringVar()
    pbLength = 0

    #Functions
    def inputfile():
        infile = ctk.filedialog.askopenfile()
        estTime = TimeEstimate(infile)
        EstTime.set(str(estTime))
        FileInput.set(infile.name)
        return EstTime,FileInput

    def outfile():

        outfile = ctk.filedialog.asksaveasfile(initialfile = 'Census Data.xlsx', defaultextension=".xlsx",filetypes = [("Excel Workbook",".xlsx"),("Text Documents","*.txt")])
        FileOutput.set(outfile.name)

    def Outputs():
        GUIDict['VarList'] = VarDropDown.get()
        GUIDict['fileInput'] = FileInput.get()
        GUIDict['fileOutput'] = FileOutput.get()
        input.quit()

    #Traces and Other Vars
    EstTime.trace_add('write',inputfile)
    varset = ctk.StringVar(value= "Basic Demographics")

    #VarSetFrame
    VarSetFrame = ctk.CTkFrame(master = input, width= 200)
    Varlabel = ctk.CTkLabel(master= VarSetFrame, text= "Choose Variable Set: ")
    VarDropDown = ctk.CTkOptionMenu(VarSetFrame,values= ["Basic Demographics", "Advanced Demographics", "Travel Data", "Test"], variable= varset)
    #VarSetFrame Packing
    Varlabel.grid(row = 0, column = 0)
    VarDropDown.grid(row = 0, column = 1)
    VarSetFrame.grid(row = 0, column = 0, pady = 50)

    #Input File
    InputFrame = ctk.CTkFrame(master=input, width= 200)
    InputLabel = ctk.CTkLabel(master=InputFrame,text= "Choose Spreadsheet to Open: ")
    InputButton = ctk.CTkButton(master= InputFrame, text= "Input File", command= inputfile)
    InputConfirmation = ctk.CTkLabel(master=InputFrame, textvariable= FileInput)
    #InputFile Packing
    InputLabel.grid(row = 0, column = 0, pady = 5)
    InputButton.grid(row = 0, column = 1, pady = 5)
    InputConfirmation.grid(row = 1, column = 0, pady = 5)
    InputFrame.grid(row = 1, column = 0, pady = 50)

    #Output File
    OutputFrame = ctk.CTkFrame(master=input, width= 200)
    OutputLabel = ctk.CTkLabel(master=OutputFrame,text= "Choose Destination for Data: ")
    OutputButton = ctk.CTkButton(master= OutputFrame, text= "Output File", command= outfile)
    OutputConfirmation = ctk.CTkLabel(master= OutputFrame,textvariable = FileOutput)
    #Output Packing
    OutputLabel.grid(row = 0, column = 0, pady = 5)
    OutputButton.grid(row = 0, column = 1, pady = 5)
    OutputConfirmation.grid(row = 1, column = 0, pady = 5)
    OutputFrame.grid(row = 2, column = 0, pady = 50)

    #StartButton
    StartButtonFrame = ctk.CTkFrame(master=input, width= 200)
    EstTimeLabel = ctk.CTkLabel(master= StartButtonFrame, text= "Estimated time is: ")
    EstTimeA = ctk.CTkLabel(master= StartButtonFrame, textvariable = EstTime)
    

    StartButton = ctk.CTkButton(master=StartButtonFrame, text= "Start", command= Outputs)
    #StartButton Packing
    EstTimeA.grid(row = 0,column = 1)
    EstTimeLabel.grid(row = 0, column = 0)
    StartButton.grid(row = 1,column = 0, padx = 25)
    StartButtonFrame.grid(row = 3, column = 0, pady = 50)


    #Mainloop
    input.mainloop()
    input.destroy()
    print(GUIDict)
    
    return GUIDict


