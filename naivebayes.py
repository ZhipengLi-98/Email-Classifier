import dataparser
import random
import re
import json


class NaiveBayes:
    # issue 1: set the size of trainSet [0, 1]
    trainSize = 1
    features = {'ham': {}, 'spam': {}}
    probs = {'ham': 0, 'spam': 0}

    def calcPro(self):
        # calculate probility -- y
        trainData = dataparser.readSets('trainSet.data')
        for data in trainData:
            if random.random() > self.trainSize:
                continue

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
        file = open(dataparser.dirPath + 'probs', 'w', encoding='utf-8')
        json.dump(self.probs, file, indent=4)
        print("Probs Done")

        file = open(dataparser.dirPath + 'features', 'w', encoding='utf-8')
        json.dump(self.features, file, ensure_ascii=False, indent=4)
        print("Features Done")


    # def classify(self):
        # classify emails


if __name__ == '__main__':
    classifier = NaiveBayes()
    classifier.calcPro()
