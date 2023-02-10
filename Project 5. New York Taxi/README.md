# __Project 5: New York City Taxi Trip Duration__

### __Contents__
[1. Description]()<br>

[2. Target metric]()

[3. Tasks]()<br>

[4. About data]()<br>

[5. Stages]()<br>

[6. Results]()<br>

[7. Conclusion]()<br>

![](https://img.freepik.com/premium-vector/taxi-set-in-the-doodle-hand-drawn-style_341076-229.jpg?w=2000)

### __1. Description__
Based on [the Kaggle competition](https://www.kaggle.com/competitions/nyc-taxi-trip-duration).  
In this competition, Kaggle is challenging you to build a model that predicts the total ride duration of taxi trips in New York City. Your primary dataset is one released by the NYC Taxi and Limousine Commission, which includes pickup time, geo-coordinates, number of passengers, and several other variables.  

### __2. Target metric__
The evaluation metric for this competition is [Root Mean Squared Logarithmic Error](https://hrngok.github.io/posts/metrics/#:~:text=Root%20Mean%20Squared%20Logaritmic%20Error%20(RMSLE)&text=It%20is%20the%20Root%20Mean,possible%200%20(zero)%20values.).

### __3. Tasks__
**Business problem:** determine the characteristics and use them to predict the duration of a taxi ride.  
**The technical task:** to build a machine learning model that, based on the proposed characteristics of the client, will predict a numerical feature - the taxi ride time.

### **4. About data**
- *id* - a unique identifier for each trip
- *vendor_id* - a code indicating the provider associated with the trip record
- *pickup_datetime* - date and time when the meter was engaged
- *dropoff_datetime* - date and time when the meter was disengaged
- *passenger_count* - the number of passengers in the vehicle (driver entered value)
- *pickup_longitude* - the longitude where the meter was engaged
- *pickup_latitude* - the latitude where the meter was engaged
- *dropoff_longitude* - the longitude where the meter was disengaged
- *dropoff_latitude* - the latitude where the meter was disengaged
- *store_and_fwd_flag* - This flag indicates whether the trip record was held in vehicle memory before sending to the vendor because the vehicle did not have a connection to the server: 
    - Y=store and forward;
    - N=not a store and forward trip
- **trip_duration** - duration of the trip in seconds

### **5. Stages**
- Part I. Loading and exploring
- Part II. Feature engineering
- Part III. Exploratory Data Analysis
- Part IV. Selection and transformation of features
- Part V. Machine Learning
- Conclusion

### **6. Results**
In the course of the current work, complex processing of the provided data was carried out and several machine learning models were built. Target metric reached: RMSLE 0.3907

### **7. Conclusion**
The best result was shown by the gradient boosting model. The median absolute error of the model is less than 2 minutes.  
Score: 0.39456

:arrow_up:[back to contents]()