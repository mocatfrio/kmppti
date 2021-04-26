import sys
import os
import matplotlib.pyplot as plt


effect = sys.argv[1]
dataset_type = sys.argv[2]
metrics = sys.argv[3]

export_filepath = "/Users/mocatfrio/Google Drive/Thesis - Hafara Firdausi/Publikasi/img/"

if effect == "cardinality":
    x_label = "Number of Data"
    x = [1000, 2000, 5000, 7000, 10000]
elif effect == "grid_size":
    x_label = "Grid Size"
    x = [3, 5, 7, 9]
elif effect == "dimension":
    x_label = "Number of Dimensions"
    x = [2, 3, 4]
elif effect == "k":
    x_label = "k"
    x = [20, 50, 100, 200]
elif effect == "ratio":
    x_label = "Data Ratio"
    x = ["1 : 1.4", "1 : 2", "1 : 1", "1.4 : 1", "2 : 1"]

if metrics == "time":
    y_label = "Execution Times (Secs)"
else:
    y_label = "Memory Usage (MB)"

if effect == "cardinality":
    if dataset_type == "ind":
        if metrics == "time":
            # kmppti 
            y1 = [86, 349.58, 2622.74, 4933.74, 10635.75]
            # kmppti-nr
            y2 = [98.29, 476.78, 3424.86, 7162.64, 13662.53]
            # naive
            y3 = [131.00, 787.93, 8594.83, 55566.46, 119894.16]
            # limit
            ylim = [0, 25000]
        elif metrics == "memory":
            # kmppti 
            y1 = [57.90234375, 46.6953125, 66.484375, 79.0703125, 97.04296875]
            # kmppti-nr
            y2 = [38.984375, 46.3828125, 66.21484375, 78.98828125, 97.30078125]
            # naive 
            y3 = [46.80, 91.64, 295.59, 1123.00, 1380.23]
            # limit
            ylim = [0, 1000]

    elif dataset_type == "ant":
        if metrics == "time":
            # kmppti 
            y1 = [12.18, 51.69, 266.31, 426.22, 768.07]
            # kmppti-nr
            y2 = [20.78, 89.85, 527.35, 983.2, 2061.59]
            # naive
            y3 = [64.47, 385.35, 3022.90, 19016.51, 34282]
            # limit
            ylim = [0, 25000]
        elif metrics == "memory":
            # kmppti 
            y1 = [44.4609375, 58.84765625, 99.35742188, 122.5039063, 148.453125]
            # kmppti-nr
            y2 = [39.15625, 45.49609375, 65.47265625, 76.2734375, 87.51953125]
            # naive
            y3 = [39.44, 67.26, 238.03, 902.76, 1094]
            # limit
            ylim = [0, 1000]


    elif dataset_type == "fc":
        if metrics == "time":
            # kmppti 
            y1 = [150.71, 876.73, 5859.07, 12291.44, 23393.43]
            # kmppti-nr
            y2 = [161.08, 743.11, 5966.48, 12446.7, 23202.47]
            # naive
            y3 = [1949.10, 6358.52, 30000, 30000, 30000]
            # limit
            ylim = [0, 25000]
        elif metrics == "memory":
            # kmppti 
            y1 = [58.1171875, 78.54296875, 142.375, 141.4335938, 190.8007813]
            # kmppti-nr
            y2 = [38.125, 44.37109375, 63.59375, 74.75, 92.7109375]
            # naive
            y3 = [89.10, 165.08, 298.47, 1045.65, 2000]
            # limit
            ylim = [0, 1000]
             
elif effect == "grid_size":
    if dataset_type == "ind":
        if metrics == "time":
            # kmppti 
            y1 = [2622.74, 2463.21, 3261.72, 4937.18]
            # kmppti-nr
            y2 = [3424.86, 3467.13, 3485.28, 3462.2]
            # limit
            ylim = [0, 10000]
        elif metrics == "memory":
            # kmppti 
            y1 = [148.484375, 144.5429688, 152.5859375, 159.9023438]
            # kmppti-nr
            y2 = [66.21484375, 65.54296875, 66.66015625, 65.1953125]
            # limit
            ylim = [0, 200]

    elif dataset_type == "ant":
        if metrics == "time":
            # kmppti 
            y1 = [266.31, 226.83, 232.98, 246.64]
            # kmppti-nr
            y2 = [527.35, 441.1, 443.3, 457.63]
            # limit
            ylim = [0, 10000]
        elif metrics == "memory":
            # kmppti 
            y1 = [99.35742188, 99.16015625, 98.7421875, 76.5234375]
            # kmppti-nr
            y2 = [65.47265625, 63.875, 64.21484375, 64.41796875]
            # limit
            ylim = [0, 200]

    elif dataset_type == "fc":
        if metrics == "time":
            # kmppti 
            y1 = [5859.07, 5863.78, 5690.31, 6135.32]
            # kmppti-nr
            y2 = [5966.48, 5895.4, 5334.68, 5940.82]
            # limit
            ylim = [0, 10000]
        elif metrics == "memory":
            # kmppti 
            y1 = [142.375, 107.9335938, 111.4609375, 113.3476563]
            # kmppti-nr
            y2 = [63.59375, 62.92578125, 63.11328125, 63.3984375]
            # limit
            ylim = [0, 200]

elif effect == "k":
    if dataset_type == "ind":
        if metrics == "time":
            # kmppti 
            y1 = [2314.66, 2311.855, 2295.11, 2313.73]
            # kmppti-nr
            y2 = [3424.86, 3441.13, 3431.21, 3428.45]
            # limit
            ylim = [0, 7000]
        elif metrics == "memory":
            # kmppti 
            y1 = [131.59375, 134.2753906, 134.8183594, 134.0019531]
            # kmppti-nr
            y2 = [66.21484375, 70.51268291, 68.18201873, 65.62351781]
            # limit
            ylim = [0, 200]

    elif dataset_type == "ant":
        if metrics == "time":
            # kmppti 
            y1 = [206.62, 217.59, 215.04, 214.74]
            # kmppti-nr
            y2 = [522.35, 511.12, 523.18, 516.11]
            # limit
            ylim = [0, 7000]
        elif metrics == "memory":
            # kmppti 
            y1 = [100.2539063, 98.671875, 100.4179688, 99.9140625]
            # kmppti-nr
            y2 = [65.47265625, 62.87283108, 60.11920002, 64.10239471]
            # limit
            ylim = [0, 200]

    elif dataset_type == "fc":
        if metrics == "time":
            # kmppti 
            y1 = [5757.66, 5742.12, 5745.78, 5753.42]
            # kmppti-nr
            y2 = [5966.48, 5961.19, 6029.4, 6033.18]
            # limit
            ylim = [0, 7000]
        elif metrics == "memory":
            # kmppti 
            y1 = [142.0390625, 140.372869, 138.632615, 141.928372]
            # kmppti-nr
            y2 = [61.223431, 63.012189, 65.012176, 67.259375]
            # limit
            ylim = [0, 200]

elif effect == "ratio":
    if dataset_type == "ind":
        if metrics == "time":
            # kmppti 
            y1 = [3173.6, 4514.62, 2622.74, 3275.9, 4525.78]
            # kmppti-nr
            y2 = [4787.12, 6079.48, 3424.86, 4702.47, 6838.38]
            # limit
            ylim = [0, 13000]
        elif metrics == "memory":
            # kmppti 
            y1 = [149.2421875, 159.2695313, 135.484375, 153.0429688, 167.7929688]
            # kmppti-nr
            y2 = [68.72265625, 75.0859375, 66.21484375, 75.08984375, 88.08203125]
            # limit
            ylim = [0, 200]

    elif dataset_type == "ant":
        if metrics == "time":
            # kmppti 
            y1 = [303.72, 433.15, 264.46, 227.89, 312.1]
            # kmppti-nr
            y2 = [721.04, 1070.29, 527.35, 695.58, 997.56]
            # limit
            ylim = [0, 13000]
        elif metrics == "memory":
            # kmppti 
            y1 = [88.1015625, 120.1953125, 98.5234375, 106.4882813, 121.8515625]
            # kmppti-nr
            y2 = [65.3828125, 73.6171875, 65.47265625, 73.3359375, 85.76171875]
            # limit
            ylim = [0, 200]

    elif dataset_type == "fc":
        if metrics == "time":
            # kmppti 
            y1 = [8147.28, 10930.26, 5859.07, 8517.5, 12340.68]
            # kmppti-nr
            y2 = [8464.92, 11302.43, 5966.48, 8649.44, 12268.53]
            # limit
            ylim = [0, 13000]
        elif metrics == "memory":
            # kmppti 
            y1 = [128.9726563, 178.8476563, 142.375, 151.0859375, 154.0351563]
            # kmppti-nr
            y2 = [73.76953125, 84.57421875, 63.59375, 67.2109375, 71.63671875]
            # limit
            ylim = [0, 200]

elif effect == "dimension":
    if dataset_type == "ind":
        if metrics == "time":
            # kmppti 
            y1 = [153.71, 2622.74, 24534.8]
            # kmppti-nr
            y2 = [254.91, 3424.86, 36001.51]
            # limit
            ylim = [0, 40000]
        elif metrics == "memory":
            # kmppti 
            y1 = [78.85742188, 98.7623, 199.5195313]
            # kmppti-nr
            y2 = [64.46484375, 66.21484375, 73.3671875]
            # limit
            ylim = [0, 200]

    elif dataset_type == "ant":
        if metrics == "time":
            # kmppti 
            y1 = [56.91, 264.46, 876.59]
            # kmppti-nr
            y2 = [113.29, 527.35, 1967.72]
            # limit
            ylim = [0, 40000]
        elif metrics == "memory":
            # kmppti 
            y1 = [71.4609375, 98.5234375, 103.4257813]
            # kmppti-nr
            y2 = [60.625, 65.47265625, 66.765625]
            # limit
            ylim = [0, 200]

    elif dataset_type == "fc":
        if metrics == "time":
            # kmppti 
            y1 = [874.2, 5859.07, 62544]
            # kmppti-nr
            y2 = [997.17, 5966.48, 48047]
            # limit
            ylim = [0, 40000]
        elif metrics == "memory":
            # kmppti 
            y1 = [61.6328125, 142.375, 286]
            # kmppti-nr
            y2 = [53.62890625, 63.59375, 288]
            # limit
            ylim = [0, 200]

# plotting the line 1  
plt.plot(x, y1, label = "k-MPPTI", color='coral', linestyle='dashed', marker='o',
     markerfacecolor='coral', markersize=5)
# plotting the line 2  
plt.plot(x, y2, label = "k-MPPTI without RSL", color='blue', linestyle='dashed', marker='v',
     markerfacecolor='blue', markersize=5)
if 'y3' in locals():
    # plotting the line 3  
    plt.plot(x, y3, label = "k-MPPTI without R-Tree", color='forestgreen', linestyle='dashed', marker='s',
        markerfacecolor='forestgreen', markersize=5)
# try to limit 
plt.ylim(ylim)
# naming the x axis
plt.xlabel(x_label)
# naming the y axis
plt.ylabel(y_label)
# show a legend on the plot
plt.legend()
  
# # function to show the plot
# plt.show()

# save the plot 
export_filepath += effect + "/"
if not os.path.exists(export_filepath):
    os.makedirs(export_filepath)
filename = export_filepath + "_".join([dataset_type, effect, metrics]) + ".png"
plt.savefig(filename, format='png', dpi=300)
