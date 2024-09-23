# Step 1: Install and load the necessary libraries
install.packages("naivebayes")
library(naivebayes)

# Step 2: Prepare your dataset
# Example dataset
data(iris)
set.seed(123)  # For reproducibility
train_indices <- sample(1:nrow(iris), 0.7 * nrow(iris))
train_data <- iris[train_indices, ]
test_data <- iris[-train_indices, ]

# Step 3: Create the Naive Bayes model
model <- naive_bayes(Species ~ ., data = train_data)

# Step 4: Make predictions
predictions <- predict(model, test_data)

# Step 5: Evaluate the model's performance
confusion_matrix <- table(test_data$Species, predictions)
print(confusion_matrix)
