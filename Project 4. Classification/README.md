# __Project 4: Classification__

### __Remark__
This project has two solutions:
- [BASELINE]() - performance of the task strictly within the specified framework and conditions.
- [UPDATE]() - an attempt to improve the predictive ability of the model.


### __Contents__
[1. Description](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#1-description)<br>

[2. Target metric](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#2-target-metric)

[3. Tasks](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#3-tasks)<br>

[4. About data](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#4-about-data)<br>

[5. Stages](https://github.com/AlekaranDS/alekaran/blob/AlekaranDS-ms/README.md#5-stages)<br>

[6. Results](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#5-stages)<br>

[7. Conclusion](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#7-conclusion)<br>


![](https://inteligencia-analitica.com/wp-content/uploads/2017/09/Random-Forest_750.png)

### __1. Description__
Banks would like to be able to choose among their customers exactly those who are most likely to take advantage of a particular offer, and contact them.

You were provided with data on the latest marketing campaign conducted by the bank: the task was to attract customers to open a deposit. You must analyze this data, identify patterns and find the decisive factors that influenced the fact that the client invested money in this particular bank. If you can do this, you will raise the bank's income and help understand the target audience that needs to be attracted through advertising and various offers.

### __2. Target metric__
F1-score is our core metric for comparing result.

### __3. Tasks__
*Business task:* to determine the characteristics by which it is possible to identify customers who are more inclined to open a deposit in a bank, and thereby increase the effectiveness of a marketing campaign.

*Technical task:* to build a machine learning model that, based on the proposed characteristics of the client, will predict whether he will take advantage of the offer to open a deposit or not.

### **4. About data**
*Bank customer data:*
- age (age);
- job (field of employment);
- marital (marital status);
- education (level of education);
- default (whether there is an overdue loan);
- housing (whether there is a loan for housing);
- loan (whether there is a loan for personal needs);
- balance (balance).

*Data related to the last contact in the context of the current marketing campaign:*
- contact (type of contact with the client);
- month (the month in which the last contact was made);
- day (the day the last contact was made);
- duration (contact duration in seconds).

*Other signs:*
- campaign (number of contacts with this client during the current campaign);
- pdays (the number of days missed from the last marketing campaign to the contact in the current campaign);
- previous (number of contacts before the current campaign)
- poutcome (the result of a past marketing campaign).

*Target variable is deposit*, which determines whether the client agrees to open a deposit with the bank. This is what we will try to predict in this case.

### **5. Stages**
- Part I. Data Explore and Cleaning
- Part II. Exploratory Data Analysis
- Part III. Selection and transformation of features
- Part IV. Machine Learning
- Conclusion

### **6. Results**
In the course of the current work, complex processing of the provided data was carried out and several machine learning models were built. Target metric reached:
- Baseline F1-score = 0.8170
- Update F1 score = 0.8550

### **7. Conclusion**
Using the constructed machine learning model, it is possible to predict with high accuracy for a particular client how likely a deposit will be taken.

:arrow_up:[back to contents](https://github.com/AlekaranDS/alekaran/tree/AlekaranDS-ms/Project%204.%20Classification#contents)
