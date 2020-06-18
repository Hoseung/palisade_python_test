# This code converts ovarian data sets to a format 
# that is compatible with the other data sets:
#
# lsvm-ovarian-model.csv,  containing the model 
# lsvm-ovarian-input.csv,  consaining the input data
# lsvm-ovarian-check.csv.  containing the classifier output (-1 or 1)
# They are written to the demoData folder.
#
# This code has already been run, no need to do it again.

import sys
import csv
import numpy as np

############################################
# Reads ovarian input data from multiple 
# files and returns 
# x - list of input vectors

def read_ovarian_input_data(input_dat_prefix, input_dat_postfix, N):    
    x = []
    for i in range(N) :
        csv_file = open(input_dat_prefix+str(i+1)+input_dat_postfix)
        csv_reader = csv.reader(csv_file)
        xitem = []
        for row in csv_reader:
            xitem.append(float(row[0]))
        x.append(xitem)
    return x

############################################
# Writes ovarian input data to a format
# comparable with other data sets 

def write_ovarian_input_data(input_csv, x):
    with open(input_csv, 'w') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerows(x)

############################################
# Reads ovarian check data from check_dat and returns 
# check - check list of +1/-1

def read_ovarian_check_data(check_dat):        
    csv_file = open(check_dat)
    csv_reader = csv.reader(csv_file, delimiter=' ', skipinitialspace=True)
    check = []
    for row in csv_reader:
        for item in row:        
            check.append(float(item));
    return check
       
############################################
# Writes ovarian check data to a format
# comparable with other data sets 
# Note that ovarian check data is reverted

def write_ovarian_check_data(check_csv, check): 
    with open(check_csv, 'w') as csv_out:
        csv_writer = csv.writer(csv_out)
        for item in check:
            csv_writer.writerow([-item])

############################################
# Reads ovarian model data from model_txt and returns 
# scaling factor, bias, beta, mu, sigma

def read_ovarian_model_data(model_txt):
    scaling_factor = []
    bias = []
    beta = []
    mu = []
    sigma = []
    with open(model_txt) as txt_file:
        line = txt_file.readline()
        while line:
            sp = line.split("=")
            if sp[0].startswith("beta"):
                beta.append(sp[1].strip())
            elif sp[0].startswith("b"):
                bias.append(sp[1].strip())
            elif sp[0].startswith("mu"):
                mu.append(sp[1].strip())
            elif sp[0].startswith("sigma"):
                sigma.append(sp[1].strip())
            elif sp[0].startswith("s"):
                scaling_factor.append(sp[1].strip())            
            line = txt_file.readline()
    return scaling_factor, bias, beta, mu, sigma

############################################
# Writes ovarian model data to a format
# comparable with other data sets 

def write_ovarian_model_data(model_csv, scaling_factor, bias, beta, mu, sigma):
    bms = []
    bms.append(beta)
    bms.append(mu)
    bms.append(sigma)
    bms = np.array(bms).T.tolist()
    scaling_factor.append("")
    scaling_factor.append("")
    bias.append("0")
    bias.append("1")
    with open(model_csv, 'w') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerow(scaling_factor)
        csv_writer.writerows(bms)
        csv_writer.writerow(bias)
        
############################################
# Main Program
############################################

# Number of features is number of input dat files
N = 216

input_dat_prefix = "demoData/cancerSVM/cancerdata"
input_dat_postfix = ".dat"
x = read_ovarian_input_data(input_dat_prefix, input_dat_postfix, N)
input_csv = "demoData/lsvm-ovarian-input.csv"
write_ovarian_input_data(input_csv, x)

check_dat = "demoData/cancerSVM/cancerlabels.dat"
check = read_ovarian_check_data(check_dat)
check_csv = "demoData/lsvm-ovarian-check.csv"
write_ovarian_check_data(check_csv, check)

model_txt = "demoData/cancerSVM/cancerSVMparams.txt"
scaling_factor, bias, beta, mu, sigma = read_ovarian_model_data(model_txt)
model_csv = "demoData/lsvm-ovarian-model.csv"
write_ovarian_model_data(model_csv, scaling_factor, bias, beta, mu, sigma)

