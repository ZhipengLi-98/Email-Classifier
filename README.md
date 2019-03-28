# Email-Classifier

---

## Project Introduction

Using Naive Bayes to classfiy Chinese emails.

Experiment of Tsinghua University Machine Learning Course 

---

## File Introduction

dataparser: Parse data and use k-fold cross validation to divide trainset and vertificationset

naivebayes: Naive Bayes classifier without any optimization

---

## Performance

### v1.x

Without any optimization

- Accuracy:  0.45496766374257

- Precision 0.9681756467107215

- Recall 0.184247307193186

- F1-Measure 0.3095315428856455

### v2.x

Use log() to avoid float error

- Accuracy:  0.9296035513220637

- Precision 0.9539721749841675

- Recall 0.9391662149431225

- F1-Measure 0.9465109965319547

### v3.x

Use Laplace Smooth

### v4.x

Use words but characters

- Accuracy:  0.7836013183014405

- Precision 0.8541394322685841

- Recall 0.8124992760644929

- F1-Measure 0.8327877901173502

### v5.x

Add From, url and X-Mailer features

- Accuracy 0.9969100038624952

- Precision 0.9974415629724387

- Recall 0.9979057591623036

- F1-Measure 0.9976736070722345

### v6.x

Add weight for features(weight = 12)

- Accuracy 0.9987640015449981

- Precision 0.998373416986174

- Recall 0.9997673065735893

- F1-Measure 0.9990698755958609
