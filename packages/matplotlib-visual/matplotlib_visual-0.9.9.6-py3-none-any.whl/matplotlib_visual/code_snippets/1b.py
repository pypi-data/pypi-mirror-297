# Function to check if a number is an Armstrong number
isArmstrong <- function(num) {
  original <- num
  num_digits <- nchar(num)
  sum <- 0
  
  while (num > 0) {
    digit <- num %% 10
    sum <- sum + digit^num_digits
    num <- num %/% 10
  }
  
  return(sum == original)
}

# Function to find Armstrong numbers within a given range
findArmstrong <- function(start, end) {
  armstrong_numbers <- c()
  
  for (num in start:end) {
    if (isArmstrong(num)) {
      armstrong_numbers <- c(armstrong_numbers, num)
    } 
  }
  
  return(armstrong_numbers)
}

start <- 1
end <- 1000
armstrong_nums <- findArmstrong(start, end)
cat("Armstrong numbers between", start, "and", end, "are:", armstrong_nums, "\n")
