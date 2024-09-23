prime <- function(num) {
  if (num<= 1){
    return(FALSE)
  }else if(num == 2 || num == 1){
    return(TRUE)
  }else{
    snum <- floor(sqrt(num))
    for (i in 3:snum){
      if(num%%i == 0){
        return(FALSE)
      }else{
        return(TRUE)
      }
    }
  }
}
num <- 11
result <- prime(num)
print(result)