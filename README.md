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