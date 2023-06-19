"""
=================================================================================================================================================
Census GUI V1.0 By Adam Fleischer 
    Is the frontfacing input for the Census API
=================================================================================================================================================
CHANGELOG:
V1.0 [04-24-2023]
    * Added all entry methods to program
    * Is able to move inputs to main program
=================================================================================================================================================
IDEAS:
    * Make GUI more modern
=================================================================================================================================================
"""
# Importing Tkinter module
from tkinter  import *


def GUI_input(var_dict,geo_dict):
    # Creating master Tkinter window
    root = Tk()
    root.geometry("300x450")
    root.resizable(False,False)
    root.title("Equity Score V1.0")

    #Top Message
    l1 = Label(root,text="Welcome to Equity Score!")
    l1a = Label(root,text="Please Enter Information Below:")
    l1.pack()
    l1a.pack()

    #Type of Geo [rb1,rb2,l1]
    v = StringVar(value='')

    rb1 = Radiobutton(root, text= "Tract", variable= v , value= "Tract")
    rb2 = Radiobutton(root, text= "Zip Code", variable= v, value= "Zip Code")

    l1 = Label(root, text= "Enter Geography Type:")


    l1.place(x=0, y=50)
    rb1.place(x=20,y=70)
    rb2.place(x=20,y=90)

    #Input Survey [e1,l2]
    data = StringVar()

    e1 = Entry(root, width=20, font=('Times New Roman',11),textvariable= data)
    l2 = Label(root,text='Enter Survey Type: ')

    l2.place(x=0,y=120)
    e1.place(x=125,y=120)

    #Input Survey Type [e2,l3]
    acs_type = StringVar()

    e2 = Entry(root, width=20, font=('Times New Roman',11),textvariable= acs_type)
    l4 = Label(root,text='Enter ACS Type: ')

    l4.place(x=0,y=150)
    e2.place(x=125,y=150)

    #Input Year [e3,l4]
    year = StringVar()

    e3 = Entry(root, width=20, font=('Times New Roman',11),textvariable= year)
    l4 = Label(root,text='Enter Data Year: ')

    l4.place(x=0,y=180)
    e3.place(x=125,y=180)

    #Input Variables [e4,l5]
    variables_n = StringVar()

    e4 = Entry(root, width=20, font=('Times New Roman',11),textvariable= variables_n)
    l5 = Label(root,text='Enter Variable: ')

    l5.place(x=0,y=210)
    e4.place(x=125,y=210)

    #Input State [l6,l7,e5]
    state_n =StringVar()

    l6 = Label(root,text="If you selected 'Zip Code' then only fill in the last box")
    l7 = Label(root,text="State:")
    e5 = Entry(root, width=20, font=('Times New Roman',11),textvariable= state_n)

    l6.place(x=0,y=260)
    l7.place(x=0,y=290)
    e5.place(x=125,y=290)

    #Input County [l8,e6]
    county_n = StringVar()

    l8 = Label(root,text="County:")
    e6 = Entry(root, width=20, font=('Times New Roman',11),textvariable= county_n)

    l8.place(x=0,y=320)
    e6.place(x=125,y=320)

    #Input Tract [l9,e7]
    tract = StringVar()

    l9 = Label(root,text="Census Tract:")
    e7 = Entry(root, width=20, font=('Times New Roman',11),textvariable= tract)

    l9.place(x=0,y=350)
    e7.place(x=125,y=350)

    #Input Zip Code [l10,e8]
    zip_code = StringVar()

    l10 = Label(root,text="Zip Code")
    e8 = Entry(root, width=20, font=('Times New Roman',11), textvariable= zip_code)

    l10.place(x=0,y=380)
    e8.place(x=125,y=380)

    #Submit Button [b1]
    def callback():
        geo_dict['gtype'] = v.get()
        var_dict['year'] = year.get()
        var_dict['name'] = variables_n.get()
        geo_dict['state_n'] = state_n.get()
        geo_dict['county_n'] = county_n.get()
        geo_dict['tract'] = tract.get()
        geo_dict['zip_code'] = zip_code.get()

        root.quit()
    
    b1 = Button(root, text= "Submit", command=callback, bg= "Red", fg= "White")
    b1.pack(side= BOTTOM, anchor= CENTER,pady= 10)

    #Loop
    root.mainloop()
    #root.quit()
    root.destroy()
    return geo_dict,var_dict

def GUI_Result(answer_GUI):
    #Create new Window
    root2 = Tk()

    # Creating master Tkinter window
    root2.geometry("400x200")
    root2.title("Equity Score V1.0")

    #Print Result [l11]
    l11 = Label(root2,text="Results:")
    l12 = Label(root2,text= answer_GUI)

    l11.pack()
    l12.pack()

    #Loop
    root2.mainloop()