import pandas as pd
import numpy as np
import csv
from scipy.signal import find_peaks

import inputs

############### *************** OPEN ACCELEROGRAMS FILE *************** ###############
df0 = []
rcsv0 = []
try:
    ds = open(inputs.filepath, 'r', newline='')   
    with ds as file:
        rcsv = csv.reader(file, delimiter = ',')
        for i in range(inputs.h_cor):
            next(rcsv)     #ignore header
        for row in rcsv:
            rcsv0.append(pd.to_numeric(row))
        df0 = pd.DataFrame(rcsv0) 
        if len(df0) <= 1:
            raise Exception("File event with issues - Error: it seems empty")
except Exception as e:  
    print("Problems opening event file {} - Error: {}".format(inputs.filepath, e))  


############### *************** CALCULATE FFT; FIND PEAKS AND CREATE LIST FILE *************** ###############
df0_col_list = []
for j in range(len(df0.columns)):                                                                                                                               
    df0_c = df0.iloc[:,j]
    df0_c.reset_index(inplace=True, drop=True)
    n = len(df0_c) 

    # Frequencies
    Ts = 1/inputs.Freq  
    frq = np.fft.fftfreq(n=n, d=Ts)     
    frq = frq[range(0,int(n/2))]  
    # Peaks limited between min and max pre-defined range
    for k in range(len(frq)): 
        aux_f = float(frq[k])
        if (aux_f <= inputs.freq_r_L): #range LOW
            f_min = k  
        if (aux_f <= inputs.freq_r_H): #range HIGH
            f_max = k   
    frq_mm = frq[range(f_min,f_max+1)]                                                  
    # Magnitude
    Y = np.fft.fft(df0_c)/n      
    Y = Y[range(0,int(n/2))]
    Y[0] = 0
    mY = np.abs(Y)                                    
    mY_mm = mY[range(f_min,f_max+1)]  
    # Find max peak
    peakY = np.max(mY_mm)  #max amplitude
    if np.isnan(peakY) == False:
        locY = np.where(mY_mm == peakY)[0][0]  #peak location
    else:
        locY = 0
    frqY = []
    frqY0 = "%.3f" % frq_mm[locY]   #peak frequency value - three decimal places 
    frqY.append(frqY0)                                                                                       
    # Find other peaks
    peaks, _ = find_peaks(mY_mm, distance = inputs.dist)
    aux_p = 0
    harm = False
    #List of all peaks - importance descending in steps according to p_peak (percentages from main peak)
    p_peak = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3]
    for k0 in range(1,len(p_peak)):
        for k in range(0,len(peaks)):           
            frqYz = "%.3f" % frq_mm[peaks[k]]      # Get the actual frequency value  
            #if it larger in the next step of importance, and if it is between range LOW and range HIGH
            if (mY_mm[peaks[k]] >= p_peak[k0]*peakY and mY_mm[peaks[k]] < p_peak[k0-1]*peakY and float(frqYz) >= inputs.freq_r_L and float(frqYz) <= inputs.freq_r_H):
                #Ignore harmonics and append Frequency value to list
                harm = False
                for f0 in frqY:
                    for hf in range(1,6): #not equal nor one of first 5 harmonics:
                        if (float(frqYz) == float(f0)*hf):
                            harm = True
                if harm == False:        
                    aux_p = aux_p + 1
                    if aux_p <= inputs.limit_frq-1:
                        frqY.append(frqYz)                                                
    df0_col_list.append(frqY)            

df1 = pd.DataFrame(df0_col_list).T
print(df1)

try:
    df1.to_csv('result.csv',index=False) 
except Exception as e: 
    print('Problem saving file - Error:', e) 
