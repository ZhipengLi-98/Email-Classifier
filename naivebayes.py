import dataparser
import random
import re
import json
import math


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
            content = email.read()

            # [\u4e00-\u9fa5]
            pattern = '[\u4e00-\u9fa5]+'
            characters = re.findall(re.compile(pattern), content)

            pattern = 'From.*@.*'
            fromFeat = re.findall(re.compile(pattern), content)
            if not len(fromFeat) == 0:
                sender = fromFeat[0].split("@")[-1].split(">")[0].split(" ")[0]
                characters.append(sender)

            pattern = 'http'
            url = re.findall(re.compile(pattern), content)
            characters += url

            pattern = 'X-Mailer: .*'
            mailer = re.findall(re.compile(pattern), content)
            if not len(mailer) == 0:
                xmailer = mailer[0].split(":")[1].split(" ")[1]
                characters += xmailer

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

        print('Calc Fold ' + str(fold) + ' Done')

    def classify(self, fold, laplaceSmooth=False, laplaceProb=1.0):
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
        # testSet = dataparser.readSets('testSet.data')
        probs = {}
        features = {}
        for i in range(0, dataparser.folds):
            if not i == fold:
                probsFile = open(dataparser.dirPath + '/probs' + str(i) + '.data')
                probs.update(json.load(probsFile))
        for i in range(0, dataparser.folds):
            if not i == fold:
                featuresFile = open(dataparser.dirPath + '/features' + str(i) + '.data', encoding='utf-8')
                features.update(json.load(featuresFile))
        for num in probs.values():
            totalNum += num
        for data in testSet:
            result = ''
            hamProb = math.log(float(probs['ham']) / float(totalNum))
            spamProb = math.log(float(probs['spam']) / float(totalNum))
            emailPath = data[0]
            label = data[1]
            email = open(dataparser.dirPath + '/data_cut/' + emailPath[8:], encoding='utf-8')
            content = email.read()

            pattern = '[\u4e00-\u9fa5]+'
            characters = re.findall(re.compile(pattern), content)
            pattern = 'From.*@.*'
            fromFeat = re.findall(re.compile(pattern), content)
            if not len(fromFeat) == 0:
                sender = fromFeat[0].split("@")[-1].split(">")[0].split(" ")[0]
                characters.append(sender)
            pattern = 'http'
            url = re.findall(re.compile(pattern), content)
            characters += url

            pattern = 'X-Mailer: .*'
            mailer = re.findall(re.compile(pattern), content)
            if not len(mailer) == 0:
                xmailer = mailer[0].split(":")[1].split(" ")[1]
                characters += xmailer

            temp = 'ham'
            for character in characters:
                # print(features[temp].keys())
                if character in features[temp].keys():
                    hamProb += math.log(float(features[temp][character]) / float(probs[temp]))
                else:
                    if laplaceSmooth:
                        hamProb += math.log(laplaceProb / (float(probs[temp]) + laplaceProb * len(characters)))
            temp = 'spam'
            for character in characters:
                # print(features[temp].keys())
                if character in features[temp].keys():
                    spamProb += math.log(float(features[temp][character]) / float(probs[temp]))
                else:
                    if laplaceSmooth:
                        spamProb += math.log(laplaceProb / (float(probs[temp]) + laplaceProb * len(characters)))

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
            if totalCnt % 100 == 0:
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
            results.append(self.classify(i, laplaceSmooth=False))
            print(results[i])

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

    def preCalc(self):
        for i in range(dataparser.folds):
            self.calcPro(i)

    def laplace(self):
        laplace = {}
        for i in range(-30, -29):
            print(float('1e%d' % i))
            # uncomment this one before submit
            # for j in range(dataparser.folds):
            # temp = i % 5
            results = self.classify(0, laplaceSmooth=True, laplaceProb=float('1e%d' % i))
            accuracy = results[0]
            precision = results[1]
            recall = results[2]
            f1_measure = results[3]
            laplace[i] = [accuracy, precision, recall, f1_measure]

        file = open(dataparser.dirPath + '/' + 'laplace.result', 'w')
        json.dump(laplace, file, indent=4)


if __name__ == '__main__':
    classifier = NaiveBayes()
    classifier.preCalc()
    # classifier.crossClassify()
    classifier.laplace()
