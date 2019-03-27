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
    plt.scatter(xAxis, data)
    plt.title(comment)
    plt.show()


if __name__ == '__main__':

    file = open(dataparser.dirPath + '/laplace.result', 'r')
    data = json.load(file)
    lastAc = 0.0
    lastPr = 0.0
    lastRe = 0.0
    lastF1 = 0.0
    for i in range(-30, 31):
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

    draw(accuracy, "Accuracy")
    draw(precision, "Precision")
    draw(recall, "Recall")
    draw(f1_measure, "F1-Measure")
    '''
    plt.plot([0.1, 1, 5, 50, 100], [0.7692, 0.9019, 0.9343, 0.9439, 0.9448], color="orange", label="Min", marker='o')
    plt.plot([0.1, 1, 5, 50, 100], [0.8866, 0.9518, 0.9545, 0.9485, 0.9481], color="yellow", label="Max", marker='o')
    plt.plot([0.1, 1, 5, 50, 100], [0.8468, 0.9253, 0.9436, 0.9460, 0.9467], color="red", label="Ave", marker='o')
    plt.title("F1-Measure")
    plt.xticks([0.1, 1, 5, 50, 100])
    plt.legend()
    plt.show()
    '''
