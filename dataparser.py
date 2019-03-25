import os
import random

dirPath = 'D:/trec06c-utf8_692204712/trec06c-utf8'


def readLabels():
    labels = {}
    file = open(dirPath + '/label/index')
    lines = file.readlines()
    for line in lines:
        label = line.split(' ')[0]
        path = line.split(' ')[1]
        labels[path] = label
    return labels


# 5-fold cross validation
def divideSets():
    labels = readLabels()
    trainSet = []
    testSet = []
    # Attention: use data_cut here but below I use '/data/' to name the relativePath
    fileDirs = os.listdir(dirPath + '/data_cut/')
    for dir in fileDirs:
        files = os.listdir(dirPath + '/data_cut/' + dir)
        for file in files:
            relativePath = '../data/' + dir + '/' + file
            # print(relativePath)
            if random.random() > 0.9:
                testSet.append(relativePath + ' ' + labels[relativePath + '\n'] + '\n')
            else:
                trainSet.append(relativePath + ' ' + labels[relativePath + '\n'] + '\n')

    # write sets
    trainFile = open(dirPath + '/trainSet.data', 'w')
    testFile = open(dirPath + '/testSet.data', 'w')
    trainFile.writelines(trainSet)
    testFile.writelines(testSet)
    print('Divide Done')


def readSets(fileName):
    file = open(dirPath + '/' + fileName)
    lines = file.readlines()
    data = []
    for line in lines:
        line = line.split('\n')[0]
        data.append((line.split(' ')[0], line.split(' ')[1]))
    return data


if __name__ == '__main__':
    # print(readSets('testSet.data'))
    divideSets()
