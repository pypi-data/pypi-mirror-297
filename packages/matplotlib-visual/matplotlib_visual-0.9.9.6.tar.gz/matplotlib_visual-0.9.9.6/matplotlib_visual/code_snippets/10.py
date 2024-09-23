PROGRAM 10:

# Create a matrix
A <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2, ncol = 3)

# Perform Singular Value Decomposition
svd_result <- svd(A)

# Extract and print the results
U <- svd_result$u
D <- svd_result$d
V <- svd_result$v

# Print the matrices
cat("Matrix A:\n")
print(A)

cat("\nMatrix U:\n")
print(U)

cat("\nSingular Values (D):\n")
print(D)

cat("\nMatrix V:\n")
print(V)
