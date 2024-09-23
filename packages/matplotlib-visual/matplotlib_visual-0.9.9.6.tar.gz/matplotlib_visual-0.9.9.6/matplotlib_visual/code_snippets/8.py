install.packages("rpart")
install.packages("rpart.plot")
library(rpart)
library(rpart.plot)

data(iris)
set.seed(123)
train_indices <- sample(1:nrow(iris), 0.7 * nrow(iris))
train_data <- iris[train_indices, ]
test_data <- iris[-train_indices, ]

model <- rpart(Species ~ ., data = train_data, method = "class")

predictions <- predict(model, test_data, type = "class")

confusion_matrix <- table(test_data$Species, predictions)
print(confusion_matrix)

rpart.plot(model)
