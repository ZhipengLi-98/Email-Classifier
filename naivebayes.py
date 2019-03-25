import dataparser
import random
import re
import json


class NaiveBayes:
    # issue 1: set the size of trainSet [0, 1]
    trainSize = 1
    features = {'ham': {}, 'spam': {}}
    probs = {'ham': 0, 'spam': 0}
    totalNum = 0

    def calcPro(self):
        # calculate probility -- y
        trainData = dataparser.readSets('trainSet.data')
        cnt = 0
        for data in trainData:
            cnt += 1
            if random.random() > self.trainSize:
                continue

            if cnt % 1000 == 0:
                print(cnt)
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
        file = open(dataparser.dirPath + '/probs.data', 'w', encoding='utf-8')
        json.dump(self.probs, file, indent=4)
        print("Probs Done")

        file = open(dataparser.dirPath + '/features.data', 'w', encoding='utf-8')
        json.dump(self.features, file, ensure_ascii=False, indent=4)
        print("Features Done")

    def classify(self):
        # classify emails
        correctCnt = 0
        totalCnt = 0
        testSet = dataparser.readSets('testSet.data')
        probsFile = open(dataparser.dirPath + '/probs.data')
        probs = json.load(probsFile)
        featuresFile = open(dataparser.dirPath + '/features.data', encoding='utf-8')
        features = json.load(featuresFile)
        for num in probs.values():
            self.totalNum += num
        for data in testSet:
            result = ''
            hamProb = float(probs['ham']) / float(self.totalNum)
            spamProb = float(probs['spam']) / float(self.totalNum)
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
            else:
                result = 'ham'
            totalCnt += 1
            if result == label:
                correctCnt += 1
            # print(float(correctCnt) / float(totalCnt))

        accuracy = float(correctCnt) / float(totalCnt)
        print('Correct: ', correctCnt)
        print('Total: ', totalCnt)
        print('Accuracy: ', accuracy)


if __name__ == '__main__':
    classifier = NaiveBayes()
    # classifier.calcPro()
    classifier.classify()
