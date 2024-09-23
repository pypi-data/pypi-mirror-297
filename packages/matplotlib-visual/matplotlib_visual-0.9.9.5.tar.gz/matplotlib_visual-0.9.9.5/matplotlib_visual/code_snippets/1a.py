#factorial
fact <- function(num){
  if(num<0){
    return("Negative int can't be processed")
  }else if(num == 0){
    return(1)
  }else {
    f <- 1
    for (i in 1:num){
      f<-f * i
    }
    return(f)
  }
}

num <- 8
result <- fact(num)
print(paste(result))
