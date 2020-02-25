# Currently the demo uses three CSV files: lsvm-model.csv, lsvm-input.csv,
# and lasvm-check.csv. They are located in the demoData folder.
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

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

sign = lambda x: (1, -1)[x < 0]

def read_model_data(model_csv):
    csv_file = open(model_csv)
    csv_reader = csv.reader(csv_file, delimiter=',')
    feature_count = 0
    beta = []
    for row in csv_reader:
        if feature_count == 0:
            s = float(row[0])
        else:
            beta.append(float(row[0]))
        feature_count += 1
    feature_count = feature_count - 2
    bias = beta[feature_count:(feature_count+1)]
    beta = beta[0:feature_count]
    return beta, bias, s, feature_count
    
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

def read_check_data(check_csv):        
    csv_file = open(check_csv)
    csv_reader = csv.reader(csv_file, delimiter=',')
    check_count = 0
    check = []
    for row in csv_reader:
        check.append(float(row[0]));
        check_count += 1
    return check, check_count

def shuffle_data(x, check):
    c = list(zip(x, check))
    random.shuffle(c)
    x, check = zip(*c)
    return x, check
    
def lsvm_plain_beta_plain_input(beta, bias, x, num):
    res = []
    for i in range(num):
        betaxi = [a*b for a,b in zip(beta,x[i])]
        ip = sum(betaxi)
        ip = ip + bias[0]
        res.append(ip)
    return res    

def enc_input(ckks_wrapper, x, num):
    enc_x = []
    for i in range(num):
        enc_x.append(ckks_wrapper.Encrypt(x[i]))
    return enc_x

def lsvm_enc_beta_plain_input(ckks_wrapper, enc_beta, enc_bias, x, num):
    res = []
    for i in range(num):
        enc_betaxi = ckks_wrapper.EvalMultConst(enc_beta, x[i])
        enc_ip = ckks_wrapper.EvalSum(enc_betaxi, next_power_of_2(feature_count))
        enc_svm = ckks_wrapper.EvalAdd(enc_ip, enc_bias)
        
        dec_svm = ckks_wrapper.Decrypt(enc_svm)
        #dec_svm = [round(v) for v in dec_svm]
        res.append(dec_svm[0])
    return res

def lsvm_enc_beta_enc_input(ckks_wrapper, enc_beta, enc_bias, enc_x, num):
    res = []
    for i in range(num):          
        enc_betaxi = ckks_wrapper.EvalMult(enc_beta, enc_x[i])
        enc_ip = ckks_wrapper.EvalSum(enc_betaxi, next_power_of_2(feature_count))
        enc_svm = ckks_wrapper.EvalAdd(enc_ip, enc_bias)
        
        dec_svm = ckks_wrapper.Decrypt(enc_svm)
        #dec_svm = [round(v) for v in dec_svm]
        res.append(dec_svm[0])
    return res

def confusion_table(res, check): 
    TT = 0
    FF = 0
    TF = 0
    FT = 0
    for i in range(len(res)):
        if sign(res[i])==check[i]:
            #print str(sign(result1)) + ": CORRECT"
            if sign(res[i])==1:
                TT += 1
            else:
                FF += 1
        else:
            #print str(sign(result1)) + ": INCORRECT"
            if sign(res[i])==1:
                FT += 1
            else:
                TF += 1
    return TT, FF, TF, FT    

#beta, bias, s, feature_count = read_model_data('demoData/lsvm-model.csv')
#x, input_count = read_input_data('demoData/lsvm-input.csv')
#check, check_count = read_check_data('demoData/lsvm-check.csv')

beta, bias, s, feature_count = read_model_data('demoData/lsvm-credit-model.csv')
x, input_count = read_input_data('demoData/lsvm-credit-input.csv')
check, check_count = read_check_data('demoData/lsvm-credit-check.csv')

#beta, bias, s, feature_count = read_model_data('demoData/lsvm-ion-model.csv')
#x, input_count = read_input_data('demoData/lsvm-ion-input.csv')
#check, check_count = read_check_data('demoData/lsvm-ion-check.csv')

#beta, bias, s, feature_count = read_model_data('demoData/lsvm-ovarian-model.csv')
#x, input_count = read_input_data('demoData/lsvm-ovarian-input.csv')
#check, check_count = read_check_data('demoData/lsvm-ovarian-check.csv')

shuffle_data(x, check)

print("feature_count:", feature_count)
print("input_count:", input_count)
print("check_count:", check_count)


max_depth = 1
scale_factor = 50
batch_size = 512

ckks_wrapper = pycrypto.Crypto()
ckks_wrapper.KeyGen(max_depth, scale_factor, batch_size)

print("keys generated")

enc_beta = ckks_wrapper.Encrypt(beta)
enc_bias = ckks_wrapper.Encrypt(bias)

print("beta and bias encrypted")

num = 10
print_num = 5

plain_res = lsvm_plain_beta_plain_input(beta, bias, x, num)

print("plain:", ["{0:0.2f}".format(i) for i in plain_res[0:print_num]])

enc_res = lsvm_enc_beta_plain_input(ckks_wrapper, enc_beta, enc_bias, x, num)

print("enc:  ", ["{0:0.2f}".format(i) for i in enc_res[0:print_num]])

enc_x = enc_input(ckks_wrapper, x, num)
enc_res2 = lsvm_enc_beta_enc_input(ckks_wrapper, enc_beta, enc_bias, enc_x, num)

print("enc2: ", ["{0:0.2f}".format(i) for i in enc_res2[0:print_num]])

TT, FF, TF, FT = confusion_table(enc_res2, check)

print ("\nConfusion Table")
print ("FF = ",str(float(FF)/float(len(x))))
print ("FT = ",str(float(FT)/float(len(x))))
print ("TF = ",str(float(TF)/float(len(x))))
print ("TT = ",str(float(TT)/float(len(x))))

# graphical output of the confusion table

array = [[float(FF)/float(len(x))*100.0,float(FT)/float(len(x))*100.0],
     [float(TF)/float(len(x))*100.0,float(TT)/float(len(x))*100.0]]        

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

