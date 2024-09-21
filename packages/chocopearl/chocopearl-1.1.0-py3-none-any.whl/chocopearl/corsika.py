import numpy as np
import pandas as pd
import warnings

def corsikatxt_to_df(path,xlims=None,ylims=None,inclined=False,add_detector_column=False):
    '''
    corsikatxt_to_df() reads a corsika DAT file that is already in txt format and organizes the particle entries in a Pandas DataFrame.
    
    path                     : Path of the dat#.txt file
    xlims=(x_low, x_high)    : Two item tupple containing lower and upper limits of the position value along X axis (in metres)
    ylims=(y_low, y_high)    : Two item tupple containing lower and upper limits of the position value along Y axis (in metres)
    inclined=False           : Boolean value. indicates wether or not the dat#.txt file corresponds to an inclined observation plane.
                               if True, it will change the X and Y axis (read documentation for visual reference). Note that this change
                               must be taken into account when specifying xlims and ylims
    add_detector_column=False: Boolean value. Adds a column called 'detector' with the default value np.nan
    '''
    # Lists to save the data
    ids = []
    x_values = []
    y_values = []
    t_values = []
    px_values = []
    py_values = []
    pz_values = []
    ek_values = []
    w_values = []
    lev_values = []

    # accessing the .txt
    with open(path, 'r') as file:
        file=list(file)
        dat_header_end = file.index('---------------------------------\n') + 1
        shower_header_end = file.index('---------------------------------\n', dat_header_end)
        particles_info_lines = file[shower_header_end:]

        for linea in particles_info_lines:
            try:
                # Divides each line in its parts using spaces as separators
                partes = linea.split()

                # gets the values of 'x=', 'y=', 't=', etc.
                id_valor = int(partes[1])
                x_valor = float(partes[2].split('=')[1])/(100)   #en metros
                y_valor = float(partes[3].split('=')[1])/(100)   #en metros          
                t_valor = float(partes[4].split('=')[1])
                px_valor = float(partes[5].split('=')[1])
                py_valor = float(partes[6].split('=')[1])
                pz_valor = float(partes[7].split('=')[1])
                if inclined==True:
                    x_valor,y_valor= (-y_valor),x_valor
                    px_valor,py_valor= (-py_valor),px_valor
                    pz_valor=-pz_valor
                    #Now Y means upwards the inclined plane and X means to the right 
                ek_valor = float(partes[8].split('=')[1])
                w_valor = float(partes[9].split('=')[1])
                lev_valor = int(partes[10].split('=')[1])

                #if (det_X_inf<=x_valor<=det_X_sup) and (det_Y_inf<=y_valor<=det_Y_sup):
                    # adds values to the lists (not efficient)
                ids.append(id_valor)
                x_values.append(x_valor)
                y_values.append(y_valor)
                t_values.append(t_valor)
                px_values.append(px_valor)
                py_values.append(py_valor)
                pz_values.append(pz_valor)
                ek_values.append(ek_valor)
                w_values.append(w_valor)
                lev_values.append(lev_valor)
            except:
                pass

    # Creates a Pandas Dataframe
    if add_detector_column:
        data = {
            'id': ids,
            'x': x_values,
            'y': y_values,
            't': t_values,
            'px': px_values,
            'py': py_values,
            'pz': pz_values,
            'ek': ek_values,
            'w': w_values,
            'lev': lev_values,
            'detector': np.nan
        }
        all_data = pd.DataFrame(data).astype({'detector':object})
    else:
        data = {
            'id': ids,
            'x': x_values,
            'y': y_values,
            't': t_values,
            'px': px_values,
            'py': py_values,
            'pz': pz_values,
            'ek': ek_values,
            'w': w_values,
            'lev': lev_values,
        }
        all_data = pd.DataFrame(data)
    # filters data 
    if xlims != None:
        all_data = all_data[(all_data['x']>= xlims[0]) & (all_data['x']<= xlims[1])].reset_index(drop=True)
    if ylims != None:
        all_data = all_data[(all_data['y']>= ylims[0]) & (all_data['y']<= ylims[1])].reset_index(drop=True)
    
    return all_data

def search_detector(x,y,detector_grid_list,tol):
    '''
    ---|Geometric Filtering|---
    search_detector(x,y,detector_grid_array,tol) finds which circular detector does a particle hit (in case it hits a detector) 
    and returns it's position or np.Nan (if the particle does not hit a detector)
    
    the parameters are:
    x:                    the position x of the particle
    y:                    the position y of the particle
    detector_grid_list:   a list of tuples containing the detector positions
    tol:                  radius of the detector
    
    '''
    detector_grid_list=np.asarray(detector_grid_list)
    
    first=detector_grid_list[detector_grid_list[:,0]<x+80]
    second=first[first[:,0]>x-80]
    third=second[second[:,1]<y+130 ]
    possible_dets=third[third[:,1]>y-130]
    
    for det in possible_dets:
        if (np.sqrt((det[0]-x)**2 + (det[1]-y)**2)<=tol**2):
            return (det[0],det[1])
    return np.nan
   
def assign_to_detector(det_position,df,tol,pf_tol=(None,None)):
    '''
    ---|Geometric Filtering|---
    given a detector position and a tolerance (radius), assign_to_detector(det_position,df,tol) filters the particles that fall
    inside that given detector and updates the dataframe of particles, assigning the
    detector position to the 'detector' column of those entries that fall inside the detector
    
    it also deletes the entries that are in the neighbourhood of the detector but do not fall inside the detector
    
    the parameters are:
    det_position:              a tuple that contains the position (x,y) of the detector
    df:                        the DataFrame of all entries
    tol:                       a tolerance for particle detection (radius of the detector)
    pf_tol=(pf_tolx,pf_toly):  [IGNORE] a tolerance for a preliminary filtering of particles in a rectangular neighbourhood of the detector 
                               (dimensions: 2*pf_tolx by 2*pf_toly) centered at the detector.
                               it is necesary that tol<=pf_tol(both components). large values will cause problems if the rectangular
                               neighbourhood is too big and overlaps with the bounds of other detectors 
    
    the function returns the updated DataFrame
                          
    '''
    if pf_tol==(None,None):
        pf_tol=(1.01*tol,1.01*tol)
    
    det_x,det_y=det_position
    pf_tolx,pf_toly=pf_tol
    possible_particles_index=df.index[(df['x']<=det_x+pf_tolx) & (df['x']>=det_x-pf_tolx) & (df['y']<=det_y+pf_toly) & (df['y']>=det_y-pf_toly)].tolist()
    for index in possible_particles_index:
        x,y=df.loc[index,'x'],df.loc[index,'y']
        if (x-det_x)**2 + (y-det_y)**2 <= tol**2:
            df.at[index,'detector']= det_position
        else:
            df.drop(index, inplace=True, axis=0)
    return df    

def get_shower_info(file_path,keywords=None):
    '''
    Reads a corsika txt file and outputs the shower parameters
    The corsika txt file must be modified 

    Credits: Fiorella Ortiz
    '''
    if keywords is None:
        keywords = ["PRMPAR =", "PRME =", "THETAP =", "PHIP ="]
    else:
        for i in range(len(keywords)):
            keywords[i]=keywords[i]+' ='

    shower_info = {}

    # Open the file and read it line by line
    with open(file_path, 'r') as file:
        for line in file:
            for keyword in keywords:
                # Look for the keyword followed by a number
                if keyword in line:
                    # Find the number next to the keyword
                    keyword_index = line.index(keyword)
                    number_start = keyword_index + len(keyword)
                    
                    # Find the number after the keyword
                    number = ""
                    for char in line[number_start:]:
                        if char.isdigit() or char == '.':
                            number += char
                        else:
                            break
                    if number:
                        shower_info[keyword[:-2]] = float(number) if '.' in number else int(number)
                        
    return shower_info

