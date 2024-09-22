import pandas as pd
import numpy as np
import matplotlib as mpl
import scipy as sc


def readCV(filename: str, pH: float, area: float, referencePotential: float): #area is in cm^2
    """Reads .txt file from biologic for cyclic voltammetry data.

    Args:
        filename (str): .txt file from biologic. must be exported using "CV-all"
        pH (float): pH of electrolyte for RHE
        area (float): geometric area of electrode for current density
        referencePotential (float): reference potential for RHE

    Returns:
        pd.DataFrame: dataframe of CV data
    """
    data = pd.read_csv(filename,
                       sep='\s+',
                       skiprows=1,
                       names = ['mode',
                                'ox/red',
                                'error',
                                'control changes',
                                'counter inc.',
                                'time/s',
                                'control/V',
                                'Ewe/V',
                                'I/mA',
                                'cycle number',
                                '(Q-Qo)/C',
                                'I Range',
                                '<Ece>/V',
                                'Analog IN 2/V',
                                'Rcmp/Ohm',
                                'P/W',
                                'Ewe-Ece/V'],
                       index_col=False,
                       dtype = np.float64,
                       engine='python')
    
    data['I/A'] = data['I/mA']/1000
    data['j/mA*cm-2'] = data['I/mA']/area
    data['Ewe/V'] = data['Ewe/V'] + referencePotential + 0.059*pH
    data['Ewe/mV'] = data['Ewe/V']*1000
    data['j/A*m-2'] = data['j/mA*cm-2']*10
    
    return data

def readCA(filename: str, pH: float, area: float, referencePotential: float): #area is in cm^2
    """Reads chronoamperometry data into pandas dataframe.

    Args:
        filename (str): filename of CA .txt. must've been exported using CA-all
        pH (float): pH of solution for RHE
        area (float): geometric area of electrode in cm^2
        referencePotential (float): reference potential for RHE

    Returns:
        _type_: _description_
    """
    data = pd.read_csv(filename,
                       sep='\s+',
                       skiprows=1,
                       names = ['mode',
                                'ox/red',
                                'error',
                                'control changes',
                                'Ns changes',
                                'counter inc.',
                                'Ns',
                                'time/s',
                                'control/V',
                                'Ewe/V',
                                'I/mA',
                                'dQ/C',
                                'I range',
                                'Ece/V',
                                'Analog IN 2/V',
                                'Rcmp/Ohm',
                                'Capacitance charge/muF',
                                'Capacitance discharge/muF',
                                'Efficiency/%',
                                'cycle number',
                                'P/W'],
                       index_col=False,
                       dtype = np.float64,
                       encoding='unicode_escape')
    

    data['j/mA*cm-2'] = data['I/mA']/area
    data['Ewe/V'] = data['Ewe/V'] + referencePotential + 0.059*pH
    data['Ewe/mV'] = data['Ewe/V']*1000
    data['j/A*m-2'] = data['j/mA*cm-2']*10
    
    return data

def readPEISPandas(filename):
    """Reads PEIS into pandas dataframe.

    Args:
        filename (str): filename of PEIS .txt (must be exported using PEIS-all)

    Returns:
        pd.DataFrame: dataframe containing PEIS experiment
    """
    data = pd.read_csv(filename,
                       sep='\s+',
                       skiprows=1,
                       names = ['freq/Hz',
                                'Re(Z)/Ohm',
                                '-Im(Z)/Ohm',
                                '|Z|/Ohm',
                                'Phase(Z)/deg',
                                'time/s',
                                '<Ewe>/V',
                                '<I>/mA',
                                'Cs/uF',
                                'Cp/uF',
                                'cycle number',
                                'I Range',
                                '|Ewe|/V',
                                '|I|/A',
                                'Ns',
                                '(Q-Qo)/mA.h',
                                'Re(Y)/Ohm-1',
                                'Im(Y)/Ohm-1',
                                '|Y|/Ohm-1',
                                'Phase(Y)/deg',
                                'dq/mA.h'],
                       index_col=False,
                       dtype = np.float64,
                       encoding='unicode_escape')
    
    return data

def readPEIS(filename: str):
    """Reads PEIS directly into format that impedance.py can use.

    Args:
        filename (str): filename of PEIS .txt (must be exported using PEIS-all)

    Returns:
        tuple(np.ndarray(float),np.ndarray(complex)): frequency, complex impedance values
    """
    return convertToImpedanceAnalysis(readPEISPandas(filename))

def convertToImpedanceAnalysis(data: pd.DataFrame):
    """Converts to format that impedance.py can use.

    Args:
        filename (pd.DataFrame): Output of readPEISPandas(filename).

    Returns:
        tuple: (np.ndarray(float),np.ndarray(complex))
    """
    frequency = data['freq/Hz'].to_numpy()
    dataLength = len(frequency)
    realImpedance = data['Re(Z)/Ohm'].to_numpy()
    imagImpedance = -data['-Im(Z)/Ohm'].to_numpy()
    impedance = np.zeros(dataLength,dtype=np.complex_)
    
    for i in range(0,dataLength):
        impedance[i] = complex(realImpedance[i],
                               imagImpedance[i])
    
    return (frequency,impedance)

def readOSC(filename: str,pH: float, area: float, referencePotential: float, irange: str, stretch: float = 1):
    """Reads oscilloscope .csv from Picoscope.

    Args:
        filename (str): filename of oscilloscope .csv from Picoscope
        pH (float): pH of electrolyte for RHE
        area (float): geometric area of electrode in cm^2
        referencePotential (float): reference potential for RHE
        irange (str): irange of measurement, '1 A', '100 mA', '10 mA' are acceptable
        stretch (float, optional): For 1 Hz, typically 4, for 10 Hz, typically 2. Defaults to 1.

    Returns:
        pd.DataFrame: dataframe containing oscilloscope values
    """
    with open(filename,'r') as file:
        lines = file.readlines()
        timeUnit = lines[1][1:3]
        firstChannel = lines[0][33]
        
    if firstChannel == 'A':
        names = ['Time (xs)','discard1','discard2','Voltage (V)','Current (A)']
    else:
        names = ['Time (xs)','discard1','discard2','Current (A)','Voltage (V)']
    
    data = pd.read_csv(filename,
                       skiprows=3,
                       sep=',',
                       names=names,
                       index_col=False,
                       dtype=float)
    
    #ensures time starts at 0
    data['Time (xs)'] = data['Time (xs)'] - data['Time (xs)'].loc[0]
    
    if timeUnit == 'ms':
        data['Time (ms)'] = data['Time (xs)']
    elif timeUnit == 'us':
        data['Time (ms)'] = data['Time (xs)']/1000
    
    data['Time (ms)'] *= stretch
    data = data[data['Time (ms)'] < (data['Time (ms)'].max()/stretch)]
    data['Time (s)'] = data['Time (ms)']/1000

    data['Voltage (V)'] = data['Voltage (V)'] + referencePotential + 0.059*pH
    if irange == '1 A':
        data['Current (A)'] = data['Current (A)']
    elif irange == '100 mA':
        data['Current (A)'] = data['Current (A)']*0.1
    elif irange == '10 mA':
        data['Current (A)'] = data['Current (A)']*0.01
    
    chargeArray = sc.integrate.cumulative_trapezoid(data['Current (A)'],
                                                    x = data['Time (s)'])
    chargeArray = np.insert(chargeArray,0,0)
    data['Charge (C)'] = pd.Series(chargeArray)
    data['Charge Density (mC/cm^2)'] = data['Charge (C)']*1000/area
    
    data['Current (mA)'] = data['Current (A)']*1000
    data['Current Density (mA/cm^2)'] = data['Current (mA)']/area
    
    data = data.drop(['discard1','discard2','Time (xs)'],axis=1)

    return data

def readRawWaveform(filename: str, pH: float, referencePotential: float):
    """Reads waveform generated by makeWaveform.py

    Args:
        filename (str): filename of waveform .csv
        pH (float): pH of solution for RHE
        referencePotential (float): reference potential for RHE

    Returns:
        pd.DataFrame: dataframe with 'Time (s)', 'Time (ms)', 'RawVoltage (V)', 'Voltage (V)'
    """
    with open(filename,'r') as file:
        lines = file.readlines()
        dataLength = float(lines[0][12:])
        frequency = float(lines[1][10:])
    
    data = pd.read_csv(filename,
                       skiprows=12,
                       sep=',',
                       dtype=float)
    data['Time (s)'] = (data['xpos']-1)/(frequency*dataLength)
    data['Time (ms)'] = data['Time (s)']*1000
    data['RawVoltage (V)'] = data['value']
    data['Voltage (V)'] = data['value'] + referencePotential + 0.059*pH
    
    return data

def colorFader(c1: str,c2: str,mix: float):
    """Yields mix between c1 and c2.

    Args:
        c1 (str): matplotlib color
        c2 (str): matplotlib color
        mix (float): 0-1, degree of mixture

    Returns:
        color: matplotlib mixed color, hexadecimal
    """
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)