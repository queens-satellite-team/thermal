# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 18:35:55 2022

@author: abdla
"""
#=====================================================#
#Asorbitivity
#absorb1 = .14          #Play with this parameter
#Emissivity
#emitAl = 0.22      #Play with this parameter 

'''
Usally spacecraft remain within 126 degrees but this depends on electrical
system temperature operatating requirements. A material with a emissivity of
greater then .3 would keep the space craft below 110 degrees C. 
'''

#=====================================================#
#Simulation Time Step
#dt = 1000 #Time steps                   #Play with this parameter
##Orbital Altitude from Earth's surface: 
#LEO (Low Earth Orbit)
#h = 300 #km



import tkinter as tk 
from tkinter import ttk 
from ThermalAnalysisV1 import runSimulation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')



if __name__ == "__main__":
    #Create gui Window
    gui = tk.Tk()
    # set the background colour of GUI window
    gui.configure(background="grey")
    # set the title of GUI window
    gui.title("SatTemp") # Or 3U CubeSat Thermal Simulator 
    
    gui.geometry('1500x750')
    
    def lift_window():
        gui.lift()
        gui.after(1000, lift_window)
    
    userinputFrame = tk.Frame(master=gui)
    

    t = ToggledFrame(userinputFrame, text='Orbital Parameters', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    
    h_var = tk.IntVar()
    tsteps_var = tk.IntVar()
    


    ttk.Label(t.sub_frame, text= "Orbit Height (km):").pack(side="left", fill="x", expand=1)
    ttk.Entry(t.sub_frame, textvariable = h_var).pack(side="left")
    
    ttk.Label(t.sub_frame, text= "Time Steps:").pack(side="left", fill="x", expand=1)
    ttk.Entry(t.sub_frame, textvariable = tsteps_var).pack(side="left")
    
    
    
    

    
    t2 = ToggledFrame(userinputFrame, text='Thermal Matieral Parameters', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    
    absorb_var = tk.DoubleVar()
    ttk.Label(t2.sub_frame, text= "Effective Absorbitivity:").pack(side="left", expand=1)
    ttk.Entry(t2.sub_frame, textvariable = absorb_var).pack(side="left")
    #absorb = tk.Entry(t2.sub_frame).get()
    
    emitAl_var = tk.DoubleVar()
    ttk.Label(t2.sub_frame, text= "Effective Emissivity").pack(side="left", expand=1)
    ttk.Entry(t2.sub_frame, textvariable = emitAl_var).pack(side="left")
    #emitAl = tk.Entry(t2.sub_frame).get()
    
    
    
    
    t3 = ToggledFrame(userinputFrame, text='Dimensions of CubeSat', relief="raised", borderwidth=1)
    t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    
    mmsquare = tk.Label(userinputFrame, text = 'Approximate area of 1 face [mm' + u'\u00b2' + ']')
    
    Tmax_var = tk.DoubleVar()
    Tmin_var = tk.DoubleVar()
    Length_var = tk.DoubleVar()
    Width_var = tk.DoubleVar()
    Height_var = tk.DoubleVar()
    Qelec_var = tk.DoubleVar()
    #Make a formula so this depends on the above three inputed values and changes the area in gui
    A1f_var = tk.DoubleVar()
    
    '''
    ttk.Label(t3.sub_frame, text= "Length:").pack(side="left", expand=1)
    ttk.Entry(t3.sub_frame, textvariable = Length_var).pack(side="left")
    
    
    
    ttk.Label(t3.sub_frame, text= "Width").pack(side="left", expand=1)
    ttk.Entry(t3.sub_frame, textvariable = Width_var).pack(side="left")
   
    
    
    ttk.Label(t3.sub_frame, text= "Height").pack(side="left", expand=1)
    ttk.Entry(t3.sub_frame, textvariable = Height_var).pack(side="left")
    '''
    
    ttk.Label(t3.sub_frame, text= 'Area of 1 face [mm' + u'\u00b2' + ']').pack(side="left", expand=1)
    ttk.Entry(t3.sub_frame, textvariable = A1f_var).pack(side="left")
    
    
    
    
    t4 = ToggledFrame(userinputFrame, text='Electrical Parameters', relief="raised", borderwidth=1)
    t4.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    
    ttk.Label(t4.sub_frame, text= "Electrical Heat Output (W):").pack(side="left", expand=1)
    ttk.Entry(t4.sub_frame, textvariable = Qelec_var).pack(side="left")
    
    
    ttk.Label(t4.sub_frame, text= "Tmax [C" + u'\u00b0' + ']').pack(side="left", expand=1)
    ttk.Entry(t4.sub_frame, textvariable = Tmax_var).pack(side="left")
    
    
    ttk.Label(t4.sub_frame, text= "Tmin[C" + u'\u00b0' + ']').pack(side="left", expand=1)
    ttk.Entry(t4.sub_frame, textvariable = Tmin_var).pack(side="left")
    
    
    
    
    def sim():
        
        #Orbit Toggle t
        h = h_var.get()
        tsteps = tsteps_var.get()    
        Tmax = Tmax_var.get()
        Tmin = Tmin_var.get()
        #absor. and emiss. toggle t2
        
        #Sat dimen. toggle t3
        '''
        Length = Length_var.get()
        Width = Width_var.get()
        Height = Height_var.get()
        '''
        A1f = A1f_var.get()
        
        absorb1 = absorb_var.get()
        emitAl= emitAl_var.get()
        Qelec = Qelec_var.get()
        #Function call to sim 
        rorb, P, orbVel, t, qs, qt, Ts, Xe, Xa  = runSimulation(h, Tmin, Tmax, absorb1, emitAl, Qelec, A1f, tsteps)
        #Produce Plots
        #=======================================================================#
        fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize =(25,14), dpi = 60)
        plt.subplot(2,2,1)
        plt.plot(t,Xe, 'y', label = r'Sun emitted radiation $X_{emitted}$')
        plt.plot(t, Xa, 'k', label = r'Earth reflected radiation $X_{albedo}$')
        plt.xlabel("Time (s)")
        plt.ylabel(r"View Factor")
        plt.title("View Factor as function of time over one period of a LEO")
        plt.legend()
        #plt.show()
        plt.subplot(2,2,2)
        plt.plot(t, qs, 'b')
        plt.xlabel("Time (s)")
        plt.ylabel(r'Heat flux $(W/m^2)$')
        plt.title("Sun's heat flux as function of time over one period of a LEO")
        #plt.show()
        
        '''
        plt.plot(t, q_earth_emitted , 'r')
        plt.xlabel("Time (s)")
        plt.ylabel(r'Heat flux $(W/m^2)$')
        plt.title("Earths's emitted heat flux as function of time over one full orbit")
        plt.show()
        '''
        '''
        plt.plot(t, q_earth_reflected, 'b')
        plt.xlabel("Time (s)")
        plt.ylabel(r'Heat flux $(W/m^2)$')
        plt.title("Earths's reflected heat flux as function of time over one full orbit")
        plt.show()
        '''
        plt.subplot(2,2,3)
        plt.plot(t, qt, 'r')
        plt.xlabel("Time (s)")
        plt.ylabel(r'Heat flux $(W/m^2)$')
        plt.title("Total heat flux as function of time over one full orbit")
        #plt.show()
        plt.subplot(2,2,4)
        plt.plot(t, Ts)
        plt.plot(t, Tmax*(t/t), 'r--', label = r'$T_{max}$ and $T_{min}$ for Electronics')
        plt.plot(t, Tmin*(t/t), 'r--')
        plt.xlabel("Time (s)")
        plt.ylabel(r'Temperature $(^\circ C)$')
        plt.title("Temperature as function of time over one full orbit")
        plt.legend(loc = 'best')
        #plt.show()
        
        
        #GUI plotting stuff 
        canvas = FigureCanvasTkAgg(fig,
                                   master = gui)  
        canvas.draw()
        

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
      
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       gui)
        toolbar.update()
      
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        
        
        orbitalRadius = tk.Label(userinputFrame, text = "Orbital Radius (km): {0}".format(rorb/1000))
        orbitalRadius.pack()
        orbVel = tk.Label(userinputFrame, text = "Orbital Velocity(m/s): {0}".format(round(int(orbVel), 0)))
        orbVel.pack()
        period = tk.Label(userinputFrame, text = "Orbital Period (s): {0}".format(int(P)))
        period.pack()
        canvas.delete('all')
        return
    runSim = tk.Button(userinputFrame, text = 'Simulate', command = sim, bg='Green')
    runSim.pack()
    userinputFrame.pack(fill=tk.BOTH, side=tk.LEFT)

gui.minsize(1450, 750)
gui.iconbitmap('sattempicon_w4u_icon.ico') 
#lift_window()
gui.mainloop()

#pyinstaller.exe --onefile --windowed --icon=sattempicon_w4u_icon.ico main.py
#this will produce an exe of this file 
#PyInstaller --onefile -i='.\angular.ico' --name "MyApp" ".\main.py"
