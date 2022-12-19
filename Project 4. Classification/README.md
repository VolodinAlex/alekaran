# __Model hyperparameter optimization__

### __Contents__
[1. Description](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#1-description)<br>

[2. Target metric](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#2-target-metric)

[3. Tasks](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#3-tasks)<br>

[4. About data](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#4-about-data)<br>

[5. Stages](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#5-stages)<br>

[6. Results](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#6-results)<br>

[7. Conclusion](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#conclusion)<br>

![](https://miro.medium.com/max/1400/1*2gsysrNnSD-n8HDCHmpZFw.jpeg)

### __1. Description__
The target metric maximization is not the purpose of this assignment! The main goal is using various options to optimize hyperparameters.  
The challenge is based on the [Kaggle: Predicting a Biological Response](https://www.kaggle.com/c/bioresponse).  
It is necessary to predict the biological response of molecules (column 'Activity') from their chemical composition (columns D1-D1776).

### __2. Target metric__
F1-score is our core metric for comparing result.

### __3. Tasks__
Two models need to be trained: logistic regression and random forest. Next, you need to make a selection of hyperparameters using basic and advanced optimization methods.
It is important to use four methods (GridSeachCV, RandomizedSearchCV, Hyperopt, Optuna) at least once, the maximum number of iterations should not exceed 50.

### **4. About data**
The data is presented in CSV format. Each line represents a molecule.
- The first Activity column contains experimental data describing the actual biological response [0, 1].
- The remaining columns D1-D1776 are molecular descriptors - these are calculated properties that can capture some characteristics of a molecule, such as size, shape, or composition of elements.

### **5. Stages**
- Part I. Simple model without optimization
- Part II. GridSearchCV
- Part III. RandomizedSearchCV
- Part IV. Hyperopt
- Part V. Optuna
- Conclusion

### **6. Results**
With the help of optimization algorithms, it was possible to increase the result on the target metric relative to the baseline.

### **7. Conclusion**
Basic and advanced optimization algorithms show consistently high results on the target metric. However, the use of basic algorithms even in a small space to search for the best optimization parameters takes a huge time period, which cannot be said about advanced ones.

:arrow_up:[back to contents](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#contents)
