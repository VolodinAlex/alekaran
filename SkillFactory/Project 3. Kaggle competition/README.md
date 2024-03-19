# __Project 3: Kaggle. Regression__

### __Remark__
This learning project is based on a [Kaggle competition](https://www.kaggle.com/competitions/sf-booking/overview).
I reached 7th place in this competition.

### __Contents__
[1. Description](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#1-description)<br>

[2. Task](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#2-task)

[3. Target metric](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#3-target-metric)<br>

[4. About data](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#4-about-data)<br>

[5. Stages](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#5-stages)<br>

[6. Results](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#6-results)<br>

[7. Conclusion](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#7-conclusion)<br>

![](https://i1.wp.com/blog.keycafe.com/wp-content/uploads/2019/05/screen-shot-2017-10-24-at-9-54-22-am.png?fit=1091%2C500&ssl=1)

### __1. Description__
Imagine that you are a data scientist at Booking. One of the problems of the company is dishonest hotels that wind up their rating. One way to find such hotels is to build a model that predicts the rating of the hotel. If the predictions of the model are very different from the actual result, then the hotel may be playing unfairly and should be checked.

### __2. Task__
You are tasked with creating such a model.

### __3. Target metric__
The results are evaluated by the MAPE.

### **4. About data**
- hotel_address - hotel address
- review_date - the date the reviewer posted the corresponding review
- average_score - the hotel's average score, calculated based on the last comment for the last year
- hotel_name - hotel name
- reviewer_nationality - reviewer's nationality
- negative_review - negative review that the reviewer gave to the hotel.
- review_total_negative_word_counts - total number of words in negative review
- positive_review - positive review that the reviewer has given to the hotel
- review_total_positive_word_counts - total number of words in a positive review
- total_number_of_reviews_reviewer_has_given - Number of reviews that reviewers have given in the past
- total_number_of_reviews - total number of valid hotel reviews
- tags - tags that the reviewer gave to the hotel.
- days_since_review - duration between review date and cleanup date
- additional_number_of_scoring - There are also some guests who simply rated the service instead of leaving a review. This number indicates how many valid grades there are without validation.
- lat - latitude of the hotel
- lng - hotel longitude
- **reviewer_score** - is a target varuable - the rating given by the reviewer to the hotel based on their experience

### **5. Stages**
- Part I. Loading and exploring
- Part II. Feature engineering
- Part III. Feature Selection
- Part IV. Machine Learning
- Conclusion

### **6. Results**
A full-fledged processing of features was carried out and a machine learning model was built.

### **7. Conclusion**
With the help of full-fledged work with each feature, a machine learning model was created. Due to the limitations of the current task (you cannot reduce the number of rows), working with outliers was impossible or extremely difficult. However, we managed to achieve the value of the target metric less than 12%.

[![KAGGLE.png](https://i.postimg.cc/L6Y67wzy/KAGGLE.png)](https://postimg.cc/6yKX4HbR)

:arrow_up:[back to contents](https://github.com/VolodinAlex/alekaran/tree/AlekaranDS/Project%203.%20Kaggle%20competition#contents)
