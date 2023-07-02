from tkinter import *
import tkinter.scrolledtext as st

class GDC(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("GDC - Doo Jia Hui")
        self.master.geometry("350x300") #width by height dimension

        #Create components
        #Swing Speed; label, entry, radio buttons
        self._lblSS = Label(self, text="Swing Speed")
        self._etySS = Entry(self, width=10)

        self._unitSS = StringVar() #common variable for Radio buttons for Swing Speed
        self._rbSS1 = Radiobutton(self,text="mph",variable=self._unitSS,value="mph")
        self._rbSS2 = Radiobutton(self,text="kph",variable=self._unitSS,value="kph")
        self._unitSS.set("mph") #value of radiobutton, this is to set default selection

        #Club Length; label, entry, radio buttons
        self._lblCL = Label(self, text="Club Length")
        self._etyCL = Entry(self, width=10)

        self._unitCL = StringVar() #common variable for Radio buttons for Club Length
        self._rbCL1 = Radiobutton(self,text="inch",variable=self._unitCL,value="inch")
        self._rbCL2 = Radiobutton(self,text="cm",variable=self._unitCL,value="cm")
        self._unitCL.set("inch") #value of radiobutton, this is to set default selection

        # Club Loft (degree)
        self._lblCLD = Label(self, text="Club Loft (degree)")
        self._etyCLD = Entry(self, width=10)

        #Create buttons
        self._btnCalc = Button(self, text="Calculate", command=self.calcDistance)
        #clear button; initial state to be disabled 
        self._btnClear = Button(self, text="Clear", state="disabled", command=self.clearAll)

        #Create ScrolledText
        #initial state to be disabled
        self._stxt = st.ScrolledText(self, width=40, height=15, state="disabled")

        #Place onto the window use grid layout
        self._lblSS.grid(row=1,column=0)
        self._etySS.grid(row=1,column=1)
        self._rbSS1.grid(row=1,column=2)
        self._rbSS2.grid(row=1,column=3)

        self._lblCL.grid(row=2,column=0)
        self._etyCL.grid(row=2,column=1)
        self._rbCL1.grid(row=2,column=2)
        self._rbCL2.grid(row=2,column=3)

        self._lblCLD.grid(row=3,column=0)
        self._etyCLD.grid(row=3,column=1)

        self._btnCalc.grid(row=4,column=0,columnspan=2)
        self._btnClear.grid(row=4,column=1,columnspan=2)

        self._stxt.grid(row=5,column=0,columnspan=4)
        self.grid()    

    def calcDistance(self):
        '''calculate distance, how far the golf ball can travel 
        based on the swing speed (in mph), club length (in inch) and club loft (in degree)'''
        
        '''return error message if it violates any of the
        input checks:
        1. is not empty value
        2. is in numeric value
        3. swing speed is positive number 
        4. club length is between 30 and 48 inches
        5. club loft is between 8 to 64 degree '''
        errorFlag = False

        #Get Swing Speed 
        #if unit in kph, convert to mph, else, default unit is mph
        try:
            swingSpeed = float(self._etySS.get()) * 0.621371 if self._unitSS.get() == "kph" else float(self._etySS.get())
        except ValueError: 
            errorFlag = True
        
        #Get club length 
        #if unit in cm, convert to inch, else, default unit is inch
        try:
            clubLength = float(self._etyCL.get()) * 0.393701 if self._unitCL.get() == "cm" else float(self._etyCL.get())
        except ValueError:
            errorFlag = True

        #Get club loft
        #unit in degree
        try:
            clubLoft = float(self._etyCLD.get())
        except:
            errorFlag = True
        
        #if no input check is violated, further check on the values
        if errorFlag == False:
            if swingSpeed < 0 or clubLength < 30 or clubLength > 48 or clubLoft < 8 or clubLoft > 64:
                errorFlag = True
        
        #return error message when any of the input checks is violated
        if errorFlag:
            msg = "Error(s) in input values\nPlease <clear> and try again\n"
        
        else: #input checks not violated
            distance = (280 - abs(clubLength-48)*10 - abs(clubLoft-10)*1.25) * swingSpeed/96
            msg = f"Estimated Distance: {round(distance)} yards\n"

        #enable ScrolledText to insert display message
        self._stxt.configure(state="normal")
        #insert display message
        self._stxt.insert(END, msg)
        #disable after insert
        self._stxt.configure(state="disabled")

        #enable Clear action button
        self._btnClear.configure(state="normal")

    def clearAll(self):
        '''Reset all entries, Clear populated text, 
        Reset radio buttons, and Disable Clear button'''

        #Clear 3 text fields
        self._etySS.delete(0,END)
        self._etyCL.delete(0,END)
        self._etyCLD.delete(0,END)

        #Clear ScrolledText
        self._stxt.configure(state="normal")
        self._stxt.delete('1.0',END)
        self._stxt.configure(state="disabled")

        #Reset radioButtons to default
        self._unitSS.set("mph")
        self._unitCL.set("inch")

        #Disable Clear button
        self._btnClear.configure(state="disabled")

def main():
    app = GDC()
    app.mainloop()

'''main()'''