#!/usr/bin/python
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

import sys
import pycrypto
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
import timeit
import confusion

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

verb = False

sign = lambda x: (1, -1)[x < 0]

#Main paramaters

# security parameter
n = 2048

# number of decimal digits after the point
prec = 3

# prec + 1 means the values of x/s and beta,b are not higher than 10 (10^1)
xmax = 5**(prec+1)
wmax = 10**(prec+1)

# read the linear SVM model
# first line is the scaling factor
# the remaining lines are the predictor vector + bias at the end
with open('demoData/lsvm-ion-model.csv') as csv_file:
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

print "number of features: " + str(feature_count)

N = feature_count + 1

# load the inputs
with open('demoData/lsvm-ion-input.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	input_count = 0
	x = []
	for row in csv_reader:
		xitem = []
		for column in row:
			xitem.append(float(column))
		x.append(xitem);
		input_count += 1

print "sample size: " + str(input_count)

# load the correct classification (for checking)
with open('demoData/lsvm-ion-check.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	check_count = 0
	check = []
	for row in csv_reader:
		check.append(float(row[0]));
		check_count += 1

start_time = timeit.default_timer()
tbo = pycrypto.TBOLinear()
elapsed = timeit.default_timer() - start_time
elapsed *=1000.0
print "Created TBOLinear() {0:5.3f} ms".format(elapsed)

#tokenLimit = N-1
tokenLimit = len(x)
start_time = timeit.default_timer()
tbo.Initialize(N, n, wmax, xmax, tokenLimit);
elapsed = timeit.default_timer() - start_time
elapsed *=1000.0
print "\nInitialized the obfuscator. {0:5.3f} ms".format(elapsed)

start_time = timeit.default_timer()
tbo.KeyGen();
elapsed = timeit.default_timer() - start_time
elapsed *=1000.0
print "Generated the secret keys. {0:5.3f} ms".format(elapsed)

betaInt = [int(round(item*10**prec)) for item in beta]

# print "weights vector: " + str(betaInt)

start_time = timeit.default_timer()
tbo.Obfuscate(betaInt)
elapsed = timeit.default_timer() - start_time
elapsed *=1000.0
print "Obfuscated the program. {0:5.3f} ms".format(elapsed)

print
nruns = 3
nquery = len(x)/2 # number of queries per run

for j in range (nruns):
        TN = 0   #true negative
        FP = 0   #false positive
        TP = 0   #true positive
        FN = 0   #false negative

        
        count = 1
        cum_time = 0.0
	for i in np.random.permutation(range(len(x)))[0:nquery]:
                if count%100 == 0: print "query " + str(count)
		query = [int(round(item/s*10**prec)) for item in x[i]] + [int(10**prec)]
                start_time = timeit.default_timer()                
		tbo.TokenGen(query)
                elapsed = timeit.default_timer() - start_time
                cum_time += elapsed
                if verb:
                        print "\r query #" + str(i),

                
		result1 = tbo.Evaluate(query)
		if sign(result1)==check[i]:
                        if verb: print str(sign(result1)) + ": CORRECT",
			if sign(result1)==1:
                                TP += 1
			else:
                                TN += 1
		else:
                        if verb: print str(sign(result1)) + ": INCORRECT",
			if sign(result1)==1:
                                FP += 1
			else:
                                FN += 1
                result2 = tbo.EvaluateClear(query,betaInt)
                if verb: print "result encrypted: " + str(result1) +" clear: " + str(result2),
                count +=1
                
        cum_time /= (count-1)
        cum_time *=1000
        print "Avg evaluation time. {0:5.3f} ms".format(cum_time)

        print "\nConfusion Table"
        print "TN% = {0:0.1f}".format(float(TN)/float(nquery)*100.0)
        print "TP% = {0:0.1f}".format(float(TP)/float(nquery)*100.0)
        print "FP% = {0:0.1f}".format(float(FP)/float(nquery)*100.0)
        print "FN% = {0:0.1f}".format(float(FN)/float(nquery)*100.0)

        # graphical output of the confusion table
        fig, ax = plt.subplots()
        #plt.cla();
        AN = (TN+FP)
        AP = (FN+TP)
        PN = (TN+FN)
        PP = (FP+TP)
        Tot = (AP+AN)
        array = [[(TN),(FP)],
                 [(FN),(TP)]]

        TruePosRate =  float(TP)/float(AP)*100.0
        TrueNegRate = float(TN)/float(AN)*100.0
        FalsePosRate = float(FP)/float(AN)*100.0
        MissClassRate = float(FN+FP)/float(Tot)*100.0
        Accuracy = float(TP+TN)/float(Tot)*100.0
        Precision = float(TP)/float(PP)*100.0
        Prevalence = float(AP)/float(Tot)*100.0

        print '\nPerformance '
        print 'True Pos Rate % =  {0:0.1f} a.k.a. Sensitivity, Recall'.format(TruePosRate)
        print 'True Neg Rate % =  {0:0.1f}'.format(TrueNegRate)
        print 'False Pos Rate % = {0:0.1f}'.format(FalsePosRate)
        print 'MissClass Rate % = {0:0.1f}'.format(MissClassRate)
        print 'Accuracy % =       {0:0.1f}'.format(Accuracy)
        print 'Precision % =      {0:0.1f}'.format(Precision)
        print 'Prevalence % =     {0:0.1f}'.format(Prevalence)
        

     
        colorarray = [[TrueNegRate,  MissClassRate ],
                      [MissClassRate, TruePosRate]]
        
        truelabel =["<=B: "+str(AN),">=A: "+str(AP)]
        predlabel = ["<=B: "+str(PN),">=A "+str(PP)]
        im, cbar = confusion.draw(colorarray, truelabel, predlabel, ax=ax,
                   cmap="RdYlGn", cbarlabel="percentage")

        texts = confusion.annotate(im, array, valfmt="{x:.0f}")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_title("Confusion Matrix for Ionosphere LSVM Prediction pass "+str(j))
        fig.tight_layout()

        # Annotate 
        offsetbox = TextArea('True Pos Rate % =    {0:2.1f}\nTrue Neg Rate % =   {1:2.1f}\nMissClass Rate % = {2:3.1f}\nAccuracy % =          {3:2.1f}\nPrecision % =          {4:2.1f}'.format(TruePosRate,TrueNegRate,MissClassRate,Accuracy,Precision)
                              , minimumdescent=False)

        ab = AnnotationBbox(offsetbox, (-0.5, 1.2),
                        xybox=(-50, -50),
                        xycoords='data',
                        boxcoords="offset points")
        ax.add_artist(ab)


        plt.show(block=False)
        plt.pause(.5)
        raw_input("Press Enter to continue...")


print "\nDemo completed"

