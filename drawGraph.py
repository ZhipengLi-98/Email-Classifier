import dataparser
import json
from matplotlib import pyplot as plt
import math

xAxis = []
accuracy = []
precision = []
recall = []
f1_measure = []


def draw(data, comment):
    plt.plot(xAxis, data, marker='o')
    plt.xlabel("Weight")
    plt.title(comment)
    plt.show()


if __name__ == '__main__':

    file = open(dataparser.dirPath + '/laplace.result', 'r')
    data = json.load(file)
    lastAc = 0.0
    lastPr = 0.0
    lastRe = 0.0
    lastF1 = 0.0
    for i in range(1, 20):
        result = data[str(i)]
        xAxis.append(i)
        accuracy.append(result[0])
        precision.append(result[1])
        recall.append(result[2])
        f1_measure.append(result[3])
        lastAc = result[0]
        lastPr = result[1]
        lastRe = result[2]
        lastF1 = result[3]
    '''
    draw(accuracy, "Accuracy")
    draw(precision, "Precision")
    draw(recall, "Recall")
    draw(f1_measure, "F1-Measure")
    '''
    plt.plot(["Baseline", "Numercial Calc Optimize", "Words + Laplace", "Other Optimize"], [0.3095, 0.9465, 0.9941, 0.9990], marker='o')
    # plt.bar(["Baseline", "Numercial Calc Optimize", "Words + Laplace", "Other Optimize"], [0.4550, 0.9682, 0.9540, 0.9983], width=0.5)
    plt.title("Compare F1-Measure")
    plt.legend()
    plt.show()
