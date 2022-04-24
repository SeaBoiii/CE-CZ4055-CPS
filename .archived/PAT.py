from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import freeze_support
from scipy import stats
import matplotlib.pyplot as plot
import os

import numpy as np
import pandas as pd

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# Calculate the number of ones in a byte
def hw(int_no):
    count = 0
    for i in format(int_no, "08b"):
        if i == '1':
            count += 1
    
    return count

# Prints the key in HEX & String
def print_key(actual_key):
    print("Correct Key: ")
    for i in actual_key:
        print("{}".format(hex(int(i)))[2:], end =" ")
    
    print()
    print("Decoded Key: ")
    for i in actual_key:
        print("{}".format(chr(i)), end = "")
        
# Solves the specific byte for the key        
def getByteKey(args):
    cycle, data_arr, no_of_possible_values_of_key_byte, no_of_traces, no_of_power_trace, power_model_matrix, actual_power_model_matrix, plot_graph = args
    
    plaintext_bytes = []
    # Array containing the specific byte of all the plain texts
    for i in range(0,len(data_arr)):
        plaintext_bytes.append(int(data_arr[i][cycle:cycle+2],16))

    # Hypothetical power model for all values of k
    # - Power model matrix
    for key_byte_guess in range(0,no_of_possible_values_of_key_byte):
        k = key_byte_guess

        leaky_sbox_output_value_array = []

        # Fill up the leaky_sbox_output_value_array with Sbox(x xor k)
        for byte in plaintext_bytes:
            byte_now = int(byte ^ k)
            leaky_sbox_output_value_array.append(Sbox[byte_now])

        hamming_weight_of_leaky_sbox_bytes = []
        for byte in range(0,no_of_traces):
            hamming_weight_of_leaky_sbox_bytes.append(hw(leaky_sbox_output_value_array[byte]))

        power_model_matrix[key_byte_guess] = hamming_weight_of_leaky_sbox_bytes

    correlation_matrix = []
    # Compute correlation between model trace of every possible value of key byte and the actual trace
    # and fill up the correlation_values array
    for key_byte_guess in range(0, no_of_possible_values_of_key_byte):
        correlation_values = []
        model_trace = power_model_matrix[key_byte_guess]
        for i in range(0,no_of_power_trace):
            power_trace = actual_power_model_matrix[i]
            corr_value = stats.pearsonr(power_trace, model_trace)
            correlation_values.append(corr_value[0])
        correlation_matrix.append(correlation_values)

    (x1,y1) = np.where(correlation_matrix == np.amax(correlation_matrix))

    best_correlation_values = []
    x_index = []
    # get the largest correlation value in every column of the correlation matrix
    for i in range(0, no_of_possible_values_of_key_byte):
        x_index.append(i)
        x = np.where(correlation_matrix[i] == np.amax(correlation_matrix[i]))
        best_correlation_values.append(correlation_matrix[i][x[0][0]])
        #best_correlation_values.append(correlation_matrix[i][y[0]])

    # Sorting the correlation values and identifying which key byte has the largest correlation
    sorting_order = np.argsort(best_correlation_values)
    sorting_order = sorting_order[::-1]
    
    # Prints the graph for each key byte
    best_pos = np.where(best_correlation_values == correlation_matrix[x1[0]][y1[0]])
    if (plot_graph):
        plot.figure()
        plot.title("Correct Key Byte : {}".format(sorting_order[0]))
        plot.xlabel('Value of key byte')
        plot.ylabel('Correlation Value')
        plot.plot(x_index, best_correlation_values)
        plot.plot(x1[0], best_correlation_values[best_pos[0][0]],'r*')
        plot.show()
    
    #print("Correct Key Byte (hex): {}".format(hex(sorting_order[0])[2:]))
    key = sorting_order[0]
    return key

# Define function to run mutiple processors and pool the results together
def run_multiprocessing(func, i, n_processors):
    with Pool(processes=n_processors) as pool:
        return pool.map(func, i)
    
# Setup multiprocessing instance    
def main(data, no_of_traces, plot_graph):
    '''
    set up parameters required by the task
    '''
    n_processors = cpu_count()-1
    actual_key_byte = 16
    no_of_possible_values_of_key_byte = 256
    no_of_power_trace = 2500

    data_arr = data[0].to_numpy()
    power_model_matrix = [[]]*no_of_possible_values_of_key_byte
    actual_power_model_matrix = data.iloc[:,2:2502].to_numpy()
    actual_power_model_matrix = np.transpose(actual_power_model_matrix[0:no_of_traces])
    
    key_bytes = []
    for i in range(0, actual_key_byte*2, 2):
        process = []
        process.append(i)
        process.append(data_arr)
        process.append(no_of_possible_values_of_key_byte)
        process.append(no_of_traces)
        process.append(no_of_power_trace)
        process.append(power_model_matrix)
        process.append(actual_power_model_matrix)
        process.append(plot_graph)
        key_bytes.append(process)

    '''
    pass the task function, followed by the parameters to processors
    '''    
    actual_key = run_multiprocessing(getByteKey, key_bytes, n_processors)

    #print("Input length: {}".format(len(key_bytes)))
    #print("Output length: {}".format(len(actual_key)))
    #print(actual_key)
    print_key(actual_key)

# The console GUI
if __name__ == "__main__":
    freeze_support()   # required to use multiprocessing
    #clear_console()
    
    print("█▀█ █▀█ █░█░█ █▀▀ █▀█   ▄▀█ █▄░█ ▄▀█ █░░ █▄█ █▀ █ █▀   ▀█▀ █▀█ █▀█ █░░")
    print("█▀▀ █▄█ ▀▄▀▄▀ ██▄ █▀▄   █▀█ █░▀█ █▀█ █▄▄ ░█░ ▄█ █ ▄█   ░█░ █▄█ █▄█ █▄▄")
    print("Welcome  to Power Analysis Tool (PAT)")
    print("Current Cipher: AES128")
    print()
    while True:
        print("|---- Trace File ----|")
        print("Open a trace file to begin")
        print("Either the full path or the name of the file in your current directory")
        print("Default: 'waveform.csv'")
        file_csv = input(">> ")
        try:
            if file_csv == "":
                file_csv = 'waveform.csv'
            data = pd.read_csv(file_csv, header=None)
            break
        except:
            #clear_console()
            print("[ERROR] Please enter the correct file name!")
            print()
    
    #clear_console()
    while True:
        print("|---- No. of Traces ----|")
        print("Please select the no of traces to be used")
        print("Default: 100")
        no_traces = input(">> ")
        try:
            if no_traces == "":
                no_traces = 100
            no_traces = int(no_traces)
            if no_traces > 100 or no_traces < 0:
                raise Exception
            break
        except TypeError:
            #clear_console()
            print("[ERROR] Only integers are allowed!")
            print()
        except: 
            #clear_console()
            print("[ERROR] Please select another number (>0 & <100")
            print()
    #clear_console()
    while True:
        print("|---- Plot graph? ----|")
        print("Do you want to plot graphs?")
        print("!!NOTE!! It will open many windows")
        print("Default: False")
        plot_graph = input(">> ").lower()
        try:
            if plot_graph == "":
                plot_graph = False
                break
            if plot_graph == 'true' or plot_graph == 't':
                plot_graph = True
                break
            if plot_graph == 'false' or plot_graph == 'f':
                plot_graph = False
                break
            else:
                raise Exception
        except:
            #clear_console()
            print("[ERROR] Invalid input. True or False only!")
            print()
    main(data, no_traces, plot_graph)