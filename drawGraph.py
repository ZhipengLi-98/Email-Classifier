import dataparser
import json
from matplotlib import pyplot as plt
import math

xAxis = []
accuracy = []
precision = []
recall = []
f1_measure = []


def draw(data):
    plt.scatter(xAxis, data)
    plt.ylabel('Accuracy Percent')
    plt.show()


if __name__ == '__main__':
    file = open(dataparser.dirPath + '/laplace1.result', 'r')
    data = json.load(file)
    lastAc = 0.0
    lastPr = 0.0
    lastRe = 0.0
    lastF1 = 0.0
    for i in range(-50, 51):
        result = data[str(i)]
        xAxis.append(math.log(float('1e%d' % i)))
        accuracy.append(result[0])
        precision.append(result[1])
        recall.append(result[2])
        f1_measure.append(result[3])
        lastAc = result[0]
        lastPr = result[1]
        lastRe = result[2]
        lastF1 = result[3]

    draw(accuracy)
    draw(precision)
    draw(recall)
    draw(f1_measure)
