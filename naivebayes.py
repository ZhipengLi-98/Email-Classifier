import dataparser
import random
import re
import json


class NaiveBayes:
    # issue 1: set the size of trainSet [0, 1]
    trainSize = 1
    features = {'ham': {}, 'spam': {}}
    probs = {'ham': 0, 'spam': 0}

    def calcPro(self, fold):
        print('Calc Fold ' + str(fold) + ' Start')
        # calculate probility -- y
        trainData = []
        for i in range(dataparser.folds):
            if not i == fold:
                temp = dataparser.readSets('trainSet' + str(i) + '.data')
                for j in temp:
                    trainData.append(j)
        # trainData = dataparser.readSets('trainSet.data')
        cnt = 0
        for data in trainData:
            cnt += 1
            if random.random() > self.trainSize:
                continue

            if cnt % 500 == 0:
                print(float(cnt) / float(len(trainData)) * 100)
            emailPath = data[0]
            label = data[1]
            # emailPath: '../data/xxx/xxx'
            # using data_cut here
            email = open(dataparser.dirPath + '/data_cut/' + emailPath[8:], encoding='utf-8')

            # using email content to classify
            # nothing else by now
            # issue 3 relative?
            content = email.read()

            # [\u4e00-\u9fa5]
            # 单个字符 是不是使用分词结果更好一些？
            pattern = '[\u4e00-\u9fa5]'
            characters = re.findall(re.compile(pattern), content)
            for character in characters:
                if character in self.features[label].keys():
                    self.features[label][character] += 1
                else:
                    self.features[label][character] = 1

        for i in self.features['spam'].values():
            self.probs['spam'] += i
        for i in self.features['ham'].values():
            self.probs['ham'] += i
        file = open(dataparser.dirPath + '/probs' + str(fold) + '.data', 'w', encoding='utf-8')
        json.dump(self.probs, file, indent=4)
        print("Probs Done")

        file = open(dataparser.dirPath + '/features' + str(fold) + '.data', 'w', encoding='utf-8')
        json.dump(self.features, file, ensure_ascii=False, indent=4)
        print("Features Done")

        print('Calc Fold ' + str(i) + ' Done')

    def classify(self, fold):
        print('Classify Fold ' + str(fold) + ' Start')
        # classify emails
        correctCnt = 0
        totalCnt = 0
        spamCnt = 0
        spamCorCnt = 0
        recallCnt = 0
        recallCorCnt = 0
        totalNum = 0
        testSet = dataparser.readSets('trainSet' + str(fold) + '.data')
        probsFile = open(dataparser.dirPath + '/probs' + str(fold) + '.data')
        probs = json.load(probsFile)
        featuresFile = open(dataparser.dirPath + '/features' + str(fold) + '.data', encoding='utf-8')
        features = json.load(featuresFile)
        for num in probs.values():
            totalNum += num
        for data in testSet:
            result = ''
            hamProb = float(probs['ham']) / float(totalNum)
            spamProb = float(probs['spam']) / float(totalNum)
            emailPath = data[0]
            label = data[1]
            email = open(dataparser.dirPath + '/data_cut/' + emailPath[8:], encoding='utf-8')
            content = email.read()
            pattern = '[\u4e00-\u9fa5]'
            characters = re.findall(re.compile(pattern), content)
            temp = 'ham'
            for character in characters:
                # print(features[temp].keys())
                if character in features[temp].keys():
                    hamProb *= float(features[temp][character]) / float(probs[temp])
            temp = 'spam'
            for character in characters:
                # print(features[temp].keys())
                if character in features[temp].keys():
                    spamProb *= float(features[temp][character]) / float(probs[temp])

            if spamProb > hamProb:
                result = 'spam'
                spamCnt += 1
            else:
                result = 'ham'
            totalCnt += 1
            if label == 'spam':
                recallCnt += 1
            if result == label:
                correctCnt += 1
                if label == 'spam':
                    spamCorCnt += 1
                    recallCorCnt += 1
            print(float(totalCnt) / float(len(testSet)) * 100)

        accuracy = float(correctCnt) / float(totalCnt)
        precision = float(spamCorCnt) / float(spamCnt)
        recall = float(recallCorCnt) / float(recallCnt)
        f1_measure = float(2) * float(precision) * float(recall) / (float(precision) + float(recall))
        # print('Test ID', fold)

        print('Classify Fold ' + str(fold) + ' Done')
        return [accuracy, precision, recall, f1_measure]

    def crossClassify(self):
        results = []
        for i in range(dataparser.folds):
            # trainSeti.data as vertification set
            self.calcPro(i)
            results.append(self.classify(i))

        accuracy = 0.0
        precision = 0.0
        recall = 0.0
        f1_measure = 0.0
        for i in range(len(results)):
            accuracy += results[i][0]
            precision += results[i][1]
            recall += results[i][2]
            f1_measure += results[i][3]
        print('Accuracy: ', float(accuracy) / dataparser.folds)
        print('Precision', float(precision) / dataparser.folds)
        print('Recall', float(recall) / dataparser.folds)
        print('F1-Measure', float(f1_measure) / dataparser.folds)


if __name__ == '__main__':
    classifier = NaiveBayes()
    classifier.crossClassify()
