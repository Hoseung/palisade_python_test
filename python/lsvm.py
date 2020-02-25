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
import csv
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

sign = lambda x: (1, -1)[x < 0]

with open('demoData/lsvm-model.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    beta = []
    for row in csv_reader:
        if line_count == 0:
            s = float(row[0])
        else:
            beta.append(float(row[0]))
        line_count += 1

feature_count = line_count - 2

N = feature_count + 1

with open('demoData/lsvm-input.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    input_count = 0
    x = []
    for row in csv_reader:
        xitem = []
        for column in row:
            xitem.append(float(column))
        x.append(xitem);
        input_count += 1

print ("input size: ",str(input_count))

# load the correct classification (for checking)
with open('demoData/lsvm-check.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    check_count = 0
    check = []
    for row in csv_reader:
        check.append(float(row[0]));
        check_count += 1


max_depth = 1
scale_factor = 50
batch_size = 512;

ckks_wrapper = pycrypto.Crypto()
ckks_wrapper.KeyGen(max_depth, scale_factor, batch_size)

enc_beta = ckks_wrapper.Encrypt(beta[0:feature_count])
enc_bias = ckks_wrapper.Encrypt(beta[feature_count:(feature_count+1)])

# dec_beta = ckks_wrapper.Decrypt(enc_beta)
# dec_beta = [round(v) for v in dec_beta]
# print(dec_beta)

TT = 0
FF = 0
TF = 0
FT = 0

for i in range(len(x)):
    print(i)
    enc_x = ckks_wrapper.Encrypt(x[i])
    enc_betaxi = ckks_wrapper.EvalMult(enc_beta, enc_x)
    enc_ip = ckks_wrapper.EvalSum(enc_betaxi, next_power_of_2(feature_count))
    enc_svm = ckks_wrapper.EvalAdd(enc_ip, enc_bias)
    dec_svm = ckks_wrapper.Decrypt(enc_svm)
    #dec_svm = [round(v) for v in dec_svm]

    if sign(dec_svm[0])==check[i]:
        #print str(sign(result1)) + ": CORRECT"
        if sign(dec_svm[0])==1:
            TT += 1
        else:
            FF += 1
    else:
        #print str(sign(result1)) + ": INCORRECT"
        if sign(dec_svm[0])==1:
            FT += 1
        else:
            TF += 1
            

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

#More sophisticated example from https://stackoverflow.com/questions/35572000/how-can-i-plot-a-confusion-matrix
'''
array = [[13,1,1,0,2,0],
     [3,9,6,0,1,0],
     [0,0,16,2,0,0],
     [0,0,0,13,0,0],
     [0,0,0,0,15,0],
     [0,0,1,0,0,15]]        
df_cm = pd.DataFrame(array, range(6),
                  range(6))
#plt.figure(figsize = (10,7))
sn.set(font_scale=1.4)#for label size
sn.heatmap(df_cm, annot=True,annot_kws={"size": 16})# font size
'''

