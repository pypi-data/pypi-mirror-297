data <- ISLR::Default

#view summary of dataset
summary(data)

default    student       balance           income     
No :9667   No :7056   Min.   :   0.0   Min.   :  772  
Yes: 333   Yes:2944   1st Qu.: 481.7   1st Qu.:21340  
Median : 823.6   Median :34553  
Mean   : 835.4   Mean   :33517  
3rd Qu.:1166.3   3rd Qu.:43808  
Max.   :2654.3   Max.   :73554  

#find total observations in dataset
nrow(data)

[1] 10000

#make this example reproducible
set.seed(1)

#Use 70% of dataset as training set and remaining 30% as testing set
sample <- sample(c(TRUE, FALSE), nrow(data), replace=TRUE, prob=c(0.7,0.3))
train <- data[sample, ]
test <- data[!sample, ]  

#fit logistic regression model
model <- glm(default~student+balance+income, family="binomial", data=train)

#disable scientific notation for model summary
options(scipen=999)

#view model summary
summary(model)
