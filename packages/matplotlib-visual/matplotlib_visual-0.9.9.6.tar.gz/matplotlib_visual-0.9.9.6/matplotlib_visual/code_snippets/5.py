library(stats)

# Sample data (replace with your data)
x <- c(1, 2, 3, 4, 5)
y <- c(2, 4, 5, 4, 5)

# Create the model
model <- lm(y ~ x)

# Print the model summary
summary(model)

# Make predictions for new data
new_x <- 6
predicted_y <- predict(model, newdata = data.frame(x = new_x))

# Print the predicted value
cat("Predicted y for x =", new_x, ":", predicted_y)