# Currently the demo uses three CSV files
# for a given example we need:
# lsvm-[example]-model.csv,  containing the model 
# lsvm-[example]-input.csv,  consaining the input data
# lsvm-[example]-check.csv.  containing the classifier output (-1 or 1)
# They are located in the demoData folder.
#  
# structure of lsvm-[example]-model.csv:
# scaling factor s
# beta vector (one component per line)
# bias
# 
# structure of lsvm-[example]-input.csv:
# input line by line (the bias term is automatically added)
# 
# structure of lsvm-check.csv:
# classification value 
# 1 or -1 (in the same order as records in lsvm-input.csv)

import sys
import argparse
import pycrypto
import random
import csv

import confusion # accesory scripts to compute and draw confusion matricies

######################
#FUNCITONS############
######################

############################################
# computes next smallest power of two >= x

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

############################################
# Reads lsvm-model.csv file and returns:
# beta - scaled beta, i.e. beta/s
# bias - scaled bias, i.e. bias/s
# feature_count - beta length

def read_model_data(model_csv):
    csv_file = open(model_csv)
    csv_reader = csv.reader(csv_file, delimiter=",")
    feature_count = 0
    beta = []
    for row in csv_reader:
        if feature_count == 0:
            s = float(row[0])
            print('s ',s)
        else:
            beta.append(float(row[0])/s)
        feature_count += 1
    feature_count = feature_count - 2
    bias = beta[feature_count:(feature_count+1)]
    beta = beta[0:feature_count]
    return beta, bias, feature_count

############################################
# Reads lsvm-input.csv file and outputs:
# x - list of input vectors
# input_count - x length

def read_input_data(input_csv):
    csv_file = open(input_csv)
    csv_reader = csv.reader(csv_file, delimiter=",")
    input_count = 0
    x = []
    for row in csv_reader:
        xitem = []
        for column in row:
            xitem.append(float(column))
        x.append(xitem);
        input_count += 1
    return x, input_count

############################################
# Reads lsvm-check.csv file and outputs:
# check - check list of +1/-1 
# check_count - check length

def read_check_data(check_csv):        
    csv_file = open(check_csv)
    csv_reader = csv.reader(csv_file, delimiter=",")
    check_count = 0
    check = []
    for row in csv_reader:
        check.append(float(row[0]));
        check_count += 1
    return check, check_count


############################################
# Shuffles the input and check lists
# This function is needed if we test random sublists
def shuffle_data(x, check):
    c = list(zip(x, check))
    random.shuffle(c)
    x, check = zip(*c)
    return x, check


############################################
# Plaintext version of lsvm
# num - number of inputs to be tested
# Outputs prediction list

def lsvm_plain_beta_plain_input(beta, bias, x, num):
    res = []
    for i in range(num):
        betaxi = [a*b for a,b in zip(beta,x[i])]
        ip = sum(betaxi)
        ip = ip + bias[0]
        res.append(ip)
    return res    


############################################
# Encrypt the input to the lsvm
# num - number of inputs to be enrypted

def enc_input(ckks_wrapper, x, num):
    enc_x = []
    for i in range(num):
        enc_x.append(ckks_wrapper.Encrypt(x[i]))
    return enc_x


############################################
# Encrypted version of lsvm with
# encrypted beta and bias and
# unencrypted input
# num - number of inputs to be tested
# Outputs encrypted prediction list

def lsvm_enc_beta_plain_input(ckks_wrapper, enc_beta, enc_bias, x, num):
    enc_res = []
    for i in range(num):
        enc_betaxi = ckks_wrapper.EvalMultConst(enc_beta, x[i])
        enc_ip = ckks_wrapper.EvalSum(enc_betaxi, next_power_of_2(feature_count))
        enc_svm = ckks_wrapper.EvalAdd(enc_ip, enc_bias)        
        enc_res.append(enc_svm)
    return enc_res

############################################
# Encrypted version of lsvm with
# encrypted beta and bias and
# encrypted input
# num - number of inputs to be tested
# Outputs encrypted prediction list
def lsvm_enc_beta_enc_input(ckks_wrapper, enc_beta, enc_bias, enc_x, num):
    enc_res = []
    for i in range(num):          
        enc_betaxi = ckks_wrapper.EvalMult(enc_beta, enc_x[i])
        enc_ip = ckks_wrapper.EvalSum(enc_betaxi, next_power_of_2(feature_count))
        enc_svm = ckks_wrapper.EvalAdd(enc_ip, enc_bias)
        enc_res.append(enc_svm)
    return enc_res

############################################
# Decrypt the output of the LSVM
# num - number of outputs to be decrypted

def dec_output(ckks_wrapper, enc_res, num):
    res = []
    for i in range(num):
        dec_res = ckks_wrapper.Decrypt(enc_res[i])
        res.append(dec_res[0])
    return res

############################################
# Timing utilities
############################################
# check the default timer and return the start time in uSec
def tic():
    import timeit
    start_time = timeit.default_timer()
    return start_time

############################################
# check the default timer return elapsed time from start_t
def toc(start_time):
    import timeit
    elapsed = timeit.default_timer() - start_time
    return elapsed
    
############################################
# same as toc except the result is printed and no value returned
def print_toc(start_time, printstring,units = "msec"):
    import timeit
    elapsed = timeit.default_timer() - start_time
    if units == "msec":
        elapsed *=1000.0
        print(printstring," {0:5.3f} ms".format(elapsed))
    else:
        print("unknown units")
        exit()

############################################
# Main Program
############################################

print("Number of arguments:", len(sys.argv), "arguments.")
print("Argument List:", str(sys.argv))

# constrruct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-v", "--verbose", required=False,
                help="verbose flag (default false)", action="store_true")
ap.add_argument("-m", "--model", required=True,
                help="one of  {simple|credit|ion|ovarian} ")
ap.add_argument("-n", "--num_test", required=True, type=int,
                help="number of inputs to test (-1 = all)")

args = ap.parse_args()
model = args.model
verbose = args.verbose
num_test = args.num_test

print("verbose ", verbose)
print("model ", model)

if (model == "ovarian") or (model == "credit"):
    print("models credit and ovarian require data normalization which is not yet supported");
    exit()

beta, bias, feature_count = read_model_data("demoData/lsvm-"+model+"-model.csv")
x, input_count = read_input_data("demoData/lsvm-"+model+"-input.csv")
check, check_count = read_check_data("demoData/lsvm-"+model+"-check.csv")

print("feature_count:", feature_count)
print("input_count:", input_count)
print("check_count:", check_count)

if num_test > input_count:
    num_test = input_count

if num_test == -1:
    num_test = input_count

print("number to test:", num_test)

#CKKS related parameters
max_depth = 1
scale_factor = 50
batch_size = 512

print("-----Initializing ckks wrapper-----")
st = tic()
ckks_wrapper = pycrypto.CKKSwrapper()
print_toc(st,"Initialized wrapper")

st = tic()
ckks_wrapper.KeyGen(max_depth, scale_factor, batch_size)
print_toc(st,"Keys generated")

st = tic()
enc_beta = ckks_wrapper.Encrypt(beta)
print_toc(st,"Betas encrypted")
st = tic()
enc_bias = ckks_wrapper.Encrypt(bias)
print_toc(st,"Bias encrypted")

x, check = shuffle_data(x, check)
print("input shuffled")
#num - number of inputs to be tested. After shuffle the inputs will be random.
#num should be <= input_count
num = 50
print_num = 5



print("-----START LSVM-----")
st = tic()
res_plain = lsvm_plain_beta_plain_input(beta, bias, x, num_test)
print_toc(st,"Plaintext LSVM runtime")
if verbose:
    print("res for plain case:      ", ["{0:0.2f}".format(i) for i in res_plain[0:print_num]])

st = tic()
enc_res_plain_input = lsvm_enc_beta_plain_input(ckks_wrapper, enc_beta, enc_bias, x, num_test)
res_plain_input = dec_output(ckks_wrapper, enc_res_plain_input, num_test)
print_toc(st,"enc beta plain input LSVM runtime")
if verbose:
    print("res for plain input case:", ["{0:0.2f}".format(i) for i in res_plain_input[0:print_num]])

st = tic()
enc_x = enc_input(ckks_wrapper, x, num_test)
enc_res_enc_input = lsvm_enc_beta_enc_input(ckks_wrapper, enc_beta, enc_bias, enc_x, num_test)
res_enc_input = dec_output(ckks_wrapper, enc_res_enc_input, num_test)
print_toc(st,"enc beta enc input LSVM runtime")
if verbose:
    print("res for enc input case:  ", ["{0:0.2f}".format(i) for i in res_enc_input[0:print_num]])

print("-----LSVM FINISHED-----")

TP, TN, FN, FP = confusion.calculate(res_plain, check)
if verbose:
    print ("\nGround truth Confusion Table")
    print ("TN = {0:0.1f}".format(float(TN)/float(num_test)*100.0))
    print ("FP = {0:0.1f}".format(float(FP)/float(num_test)*100.0))
    print ("FN = {0:0.1f}".format(float(FN)/float(num_test)*100.0))
    print ("TP = {0:0.1f}".format(float(TP)/float(num_test)*100.0))

# graphical output of the confusion table

confusion.display(res_plain, check, "res_plain")
confusion.display(res_plain_input, check, "res_enc_model_plain_input")
confusion.display(res_enc_input, check, "res_enc")

input("Press Enter to remove plots and continue...")



    
print ("\nDemo completed")

