# Authors: David Bruce Cousins NJIT 2020
# confusion matrix and statistics plotting 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

#################################################################
# functions to plot and annotate a confusion matrix


def sign(x): return (1, -1)[x < 0]

#################################################################


def draw(indata, row_labels, col_labels, ax=None,
         cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a confusion heatmap from a numpy array and two lists of labels.

    Arguments:
        data       : A 2D  array of shape (N,M)
        row_labels : A list or array of length N with the labels
                     for the rows
        col_labels : A list or array of length M with the labels
                     for the columns
    Optional arguments:
        ax         : A matplotlib.axes.Axes instance to which the heatmap
                     is plotted. If not provided, use current axes or
                     create a new one.
        cbar_kw    : A dictionary with arguments to
                     :meth:`matplotlib.Figure.colorbar`.
        cbarlabel  : The label for the colorbar
    All other arguments are directly passed on to the imshow call.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    # make off diagonal values actually 100 - value since zero is good
    data = np.array(indata)
    newdata = 100.0 - data
    for (x, y), value in np.ndenumerate(newdata):
        if (x == y):
            newdata[x, y] = data[x, y]

    # and use that for the display
    im = ax.imshow(newdata, vmin=0.0, vmax=100.0, **kwargs)

    # Create colorbar

    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on bottom.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="left",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    if cbarlabel == "":
        return im
    else:
        return im, cbar

#################################################################


def annotate(im, indata=None, valfmt="{x:.2f}",
             textcolors=["black", "black"],
             threshold=None, **textkw):
    """
    A function to annotate a confusion matrix .

    Arguments:
        im         : The AxesImage to be labeled.
    Optional arguments:
        data       : Data used to annotate. If None, the image's data is used.
        valfmt     : The format of the annotations inside the heatmap.
                     This should either use the string format method, e.g.
                     "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
        textcolors : A list or array of two color specifications. The first is
                     used for values below a threshold, the second for those
                     above.
        threshold  : Value in data units according to which the colors from
                     textcolors are applied. If None (the default) uses the
                     middle of the colormap as separation.

    Further arguments are passed on to the created text labels.
    """

    data = np.array(indata)
    # if not isinstance(indata, (list, np.ndarray)):
    #    data = (list, im.get_array())

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

############################################
# Calculate confusion table and statistics for lsvm predictions
# TP true positive
# TN true negative
# FP false positive
#


def calculate(res, check):
    TP, TN, FN, FP = 0, 0, 0, 0
    for i in range(len(res)):
        if sign(res[i]) == check[i]:
            if sign(res[i]) == 1:
                TP += 1
            else:
                TN += 1
        else:
            if sign(res[i]) == 1:
                FP += 1
            else:
                FN += 1
    return TP, TN, FN, FP


############################################
# display confusion table and statistics for lsvm predictions
# TP true positive
# TN true negative
# FP false positive
#
def display(res, check, title_str):
    TP, TN, FN, FP = 0, 0, 0, 0
    for i in range(len(res)):
        if sign(res[i]) == check[i]:
            if sign(res[i]) == 1:
                TP += 1
            else:
                TN += 1
        else:
            if sign(res[i]) == 1:
                FP += 1
            else:
                FN += 1

    fig, ax = plt.subplots()
    # plt.cla();
    AN = (TN + FP)
    AP = (FN + TP)
    PN = (TN + FN)
    PP = (FP + TP)
    Tot = (AP + AN)
    array = [[(TN), (FP)],
             [(FN), (TP)]]

    TruePosRate = float(TP) / float(AP) * 100.0
    TrueNegRate = float(TN) / float(AN) * 100.0
    FalsePosRate = float(FP) / float(AN) * 100.0
    MissClassRate = float(FN + FP) / float(Tot) * 100.0
    Accuracy = float(TP + TN) / float(Tot) * 100.0
    Precision = float(TP) / float(PP) * 100.0
    Prevalence = float(AP) / float(Tot) * 100.0

    print("\nPerformance " + title_str)
    print(
        "True Pos Rate % =  {0:0.1f} a.k.a. Sensitivity, Recall".format(TruePosRate))
    print("True Neg Rate % =  {0:0.1f}".format(TrueNegRate))
    print("False Pos Rate % = {0:0.1f}".format(FalsePosRate))
    print("MissClass Rate % = {0:0.1f}".format(MissClassRate))
    print("Accuracy % =       {0:0.1f}".format(Accuracy))
    print("Precision % =      {0:0.1f}".format(Precision))
    print("Prevalence % =     {0:0.1f}".format(Prevalence))

    colorarray = [[TrueNegRate, MissClassRate],
                  [MissClassRate, TruePosRate]]

    truelabel = ["<=B: " + str(AN), ">=A: " + str(AP)]
    predlabel = ["<=B: " + str(PN), ">=A: " + str(PP)]
    im, cbar = draw(colorarray, truelabel, predlabel, ax=ax,
                    cmap="RdYlGn", cbarlabel="percentage")

    texts = annotate(im, array, valfmt="{x:.0f}")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    title_str = "Confusion Matrix for LSVM Prediction " + title_str
    ax.set_title(title_str)

    fig.tight_layout()

    # Annotate
    offsetbox = TextArea(
        "True Pos Rate % =    {0:2.1f}\nTrue Neg Rate % =   {1:2.1f}\nMissClass Rate % = {2:3.1f}\nAccuracy % =          {3:2.1f}\nPrecision % =          {4:2.1f}".format(
            TruePosRate,
            TrueNegRate,
            MissClassRate,
            Accuracy,
            Precision),
        minimumdescent=False)

    ab = AnnotationBbox(offsetbox, (-0.45, 1.2),
                        xybox=(-50, -50),
                        xycoords="data",
                        boxcoords="offset points")
    ax.add_artist(ab)

    plt.show(block=False)
    plt.pause(.1)
