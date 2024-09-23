if (!require(arules)) install.packages("arules")
library(arules)

# Sample data (replace with your data)
transactions <- data.frame(
  transaction = c("T1", "T1", "T2", "T2", "T3", "T3"),
  item = c("bread", "milk", "cereal", "beer", "bread", "cheese")
)

# Convert data to transactions object
tx <- as(split(transactions$item, transactions$transaction), "transactions")

# Minimum support and confidence thresholds
min_support <- 0.2
min_confidence <- 0.6

# Find frequent itemsets
rules <- apriori(tx, minlen=2, minval=min_support, confidence=min_confidence)

# Inspect the rules
inspect(rules)