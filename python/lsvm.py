# Currently the demo uses three CSV files: 
# lsvm-model.csv, 
# lsvm-input.csv,
# lsvm-check.csv. 
# They are located in the demoData folder.
#  
# structure of lsvm-model.csv:
# scaling factor s
# beta vector (one component per line)
# bias
# 
# structure of lsvm-input.csv:
# input line by line (the bias term is automatically added)
# 
# structure of lsvm-check.csv:
# 1 or -1 (in the same order as records in lsvm-input.csv)

import pycrypto
import random
import csv
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from llvmlite.binding.ffi import OutputString


sign = lambda x: (1, -1)[x < 0]


#smalles power of two >= x
def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()


# Reads lsvm-model.csv file and outputs:
# beta - scaled beta, i.e. beta/s
# bias - scaled bias, i.e. bias/s
# feature_count - beta length
def read_model_data(model_csv):
    csv_file = open(model_csv)
    csv_reader = csv.reader(csv_file, delimiter=',')
    feature_count = 0
    beta = []
    for row in csv_reader:
        if feature_count == 0:
            s = float(row[0])
        else:
            beta.append(float(row[0])/s)
        feature_count += 1
    feature_count = feature_count - 2
    bias = beta[feature_count:(feature_count+1)]
    beta = beta[0:feature_count]
    return beta, bias, feature_count

    
# Reads lsvm-input.csv file and outputs:
# x - list of input vectors
# input_count - x length
def read_input_data(input_csv):
    csv_file = open(input_csv)
    csv_reader = csv.reader(csv_file, delimiter=',')
    input_count = 0
    x = []
    for row in csv_reader:
        xitem = []
        for column in row:
            xitem.append(float(column))
        x.append(xitem);
        input_count += 1
    return x, input_count


# Reads lsvm-check.csv file and outputs:
# check - check list of +1/-1 
# check_count - check length
def read_check_data(check_csv):        
    csv_file = open(check_csv)
    csv_reader = csv.reader(csv_file, delimiter=',')
    check_count = 0
    check = []
    for row in csv_reader:
        check.append(float(row[0]));
        check_count += 1
    return check, check_count


# Shuffles the input and check lists
# This function is needed if we test random sublists
def shuffle_data(x, check):
    c = list(zip(x, check))
    random.shuffle(c)
    x, check = zip(*c)
    return x, check


# Plain version of lsvm
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


# Encrypting input
# num - number of inputs to be enrypted
def enc_input(ckks_wrapper, x, num):
    enc_x = []
    for i in range(num):
        enc_x.append(ckks_wrapper.Encrypt(x[i]))
    return enc_x


# Encrypted version of lsvm with encrypted beta and bias and unencrypted input
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

# Encrypted version of lsvm with encrypted beta and bias and unencrypted input
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


# Decrypting output
# num - number of outputs to be decrypted
def dec_output(ckks_wrapper, enc_res, num):
    res = []
    for i in range(num):
        dec_res = ckks_wrapper.Decrypt(enc_res[i])
        res.append(dec_res[0])
    return res


# Calculate confusion table for lsvm predictions
def confusion_table(res, check): 
    TT, FF, TF, FT = 0, 0, 0, 0
    for i in range(len(res)):
        if sign(res[i])==check[i]:
            if sign(res[i])==1:
                TT += 1
            else:
                FF += 1
        else:
            if sign(res[i])==1:
                FT += 1
            else:
                TF += 1
    return TT, FF, TF, FT    


"""Input 1"""
beta, bias, feature_count = read_model_data('demoData/lsvm-model.csv')
x, input_count = read_input_data('demoData/lsvm-input.csv')
check, check_count = read_check_data('demoData/lsvm-check.csv')

"""Input 2"""
# beta, bias, feature_count = read_model_data('demoData/lsvm-credit-model.csv')
# x, input_count = read_input_data('demoData/lsvm-credit-input.csv')
# check, check_count = read_check_data('demoData/lsvm-credit-check.csv')

"""Input 3"""
# beta, bias, feature_count = read_model_data('demoData/lsvm-ion-model.csv')
# x, input_count = read_input_data('demoData/lsvm-ion-input.csv')
# check, check_count = read_check_data('demoData/lsvm-ion-check.csv')


print("feature_count:", feature_count)
print("input_count:", input_count)
print("check_count:", check_count)


#CKKS related parameters
max_depth = 1
scale_factor = 50
batch_size = 512

print("-----Initializing ckks wrapper-----")
ckks_wrapper = pycrypto.CKKSwrapper()

ckks_wrapper.KeyGen(max_depth, scale_factor, batch_size)
print("-----Keys generated-----")

enc_beta = ckks_wrapper.Encrypt(beta)
enc_bias = ckks_wrapper.Encrypt(bias)
print("-----beta and bias are encrypted-----")

x, check = shuffle_data(x, check)
print("input shuffled")
#num - number of inputs to be tested. After shuffle the inputs will be random.
#num should be <= input_count
num = 50
print_num = 5
print("number of inputs to be tested:", num)


print("-----START LSVM-----")

res_plain = lsvm_plain_beta_plain_input(beta, bias, x, num)

print("res for plain case:      ", ["{0:0.2f}".format(i) for i in res_plain[0:print_num]])

enc_res_plain_input = lsvm_enc_beta_plain_input(ckks_wrapper, enc_beta, enc_bias, x, num)
res_plain_input = dec_output(ckks_wrapper, enc_res_plain_input, num)

print("res for plain input case:", ["{0:0.2f}".format(i) for i in res_plain_input[0:print_num]])

enc_x = enc_input(ckks_wrapper, x, num)
enc_res_enc_input = lsvm_enc_beta_enc_input(ckks_wrapper, enc_beta, enc_bias, enc_x, num)
res_enc_input = dec_output(ckks_wrapper, enc_res_enc_input, num)

print("res for enc input case:  ", ["{0:0.2f}".format(i) for i in res_enc_input[0:print_num]])

print("-----LSVM FINISHED-----")


TT, FF, TF, FT = confusion_table(res_enc_input, check)
print ("\nConfusion Table")

print ("FF = ",str(float(FF)/float(num)))
print ("FT = ",str(float(FT)/float(num)))
print ("TF = ",str(float(TF)/float(num)))
print ("TT = ",str(float(TT)/float(num)))

# graphical output of the confusion table
array = [[float(FF)/float(num)*100.0,float(FT)/float(num)*100.0],
     [float(TF)/float(num)*100.0,float(TT)/float(num)*100.0]]        

df_cm = pd.DataFrame(array, ["F","T"],
                  ["F","T"])

plt.figure(figsize = (10,7))
sn.set(font_scale=1.4) #for label size
ax = sn.heatmap(df_cm, annot=True,annot_kws={"size": 16},cmap="RdYlGn")# font size
ax.set_xlabel("Predicted")
ax.set_ylabel("True")
ax.set_title("Confusion Matrix for LSVM Prediction")

plt.show()

print ("\nDemo completed")

