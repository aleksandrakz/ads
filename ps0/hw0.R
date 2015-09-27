## CS 458/558
## Fall 2015
## hw0.R
#install.packages("pryr")
#library("pryr")
library("stringr")
#library("hash")


# write a function palindrome which reads an ascii file comprising one word
# per line and returns all the palindromes.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# There is another optional argument of a single letter, in which case the
# program returns only palindromes which start with that letter.

## Use the following function signature. 
palindrome <- function(filename = "/usr/share/dict/words", letter = "all"){
  file<- readLines(filename)
  #print( file)
  for (i in 1:length(file)) {
    word<-file[i]
    lower<-tolower(word)
    lower = str_replace_all(lower, "[^[:alnum:]]", "")
    lower<-strsplit(lower, "")[[1]]
    #print(word)
    #print(lower)
    if (letter != "all" && lower[1]!= letter) {
      next
    }
    len <- length(lower)
    #print(word)
    i <- 1
    j <- len
    while (i<=j) {
      #print(lower[i])
      #print(lower[j])
      if (lower[i] != lower[j] ) {
        #print("do not match")
        break
      }
      i<-i+1
      j<-j-1
    }
    if (j<=i) {
      print(word)
    }
  }
}
  

## Function 2: anagram
##
# write a function anagram which reads an ascii file comprising one word
# per line and returns all the largest set of words which are anagrams.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# (During development, you might want to use a smaller dictionary.)
# 
# There is another optional argument which is a single word.  
# In that case, the function returns all anagrams for that word 

# Example output
# > anagram()
# [1] "alerts" "alters" "artels" "estral" "laster" "lastre" "rastle" "ratels" "relast" "resalt"
# [11] "salter" "slater" "staler" "stelar" "talers"
# 
# > anagram(target = 'male')
# [1] "alem" "alme" "amel" "lame" "leam" "meal" "mela"

## Use the following function signature. 
anagram <- function(filename = "/usr/share/dict/words", target = FALSE){
 dict <- new.env()
 countdict <- new.env()
 maxcount = 0
 maxset = ""
 
 file<- readLines(filename)
 #print( file)
 for (i in 1:length(file)) {
   word <- file[i]
   freq <- rep(c(0), 26)
   lower<-tolower(word)
   lower = str_replace_all(lower, "[^[:alnum:]]", "")
   lower<-strsplit(lower, "")[[1]]
   len <- length(lower)
   for (i in 1:len) {
     letter <- strtoi(charToRaw(lower[i]),16L) -96
     freq[letter]<-freq[letter]+1
   }
   freq= str_replace_all(paste(toString(freq), collapse=NULL), "[ ,]" ,"")
   #print(word)
   #print(freq)
   if (!(exists(freq, envir=dict))) {
     countdict[[freq]] <- 0
     dict[[freq]] <- ""
     }
   count = get(freq, envir=countdict) + 1
   countdict[[freq]] <- count
   
   set = append(get(freq, envir = dict), word)
   dict[[freq]]<-set
   #print(set)
   
   if (count> maxcount) {
     maxcount <- count
     maxset <-freq
   }
 }
 if (target == FALSE) {
   most=get(maxset, envir = dict)
   for (i in 2:length(most)) {
     print (most[i])
   }
 }
 else {
   freq <- rep(c(0), 26)
   lower<-tolower(target)
   lower = str_replace_all(lower, "[^[:alnum:]]", "")
   lower<-strsplit(lower, "")[[1]]
   len <- length(lower)
   for (i in 1:len) {
     letter <- strtoi(charToRaw(lower[i]),16L) -96
     freq[letter]<-freq[letter]+1
   }
   target= str_replace_all(paste(toString(freq), collapse=NULL), "[ ,]" ,"")
   if (exists(target, envir=dict) ) {
     anagrams = get(target, envir = dict)
     for (i in 2:length(anagrams)){
       print(anagrams[i])
     }
   }
 }
}


## Bonus question (no credit)
## An auto-antonym is a word that has two meanings that are opposites.
## For example, "dust" can mean to remove dust (I am dusting under the bed)
## and also "dust" can mean to add dust (I am dusting the cake with powdered sugar)
##
## How would you use a computer to come up with a list of auto-antonyms?
## Hint: there is more than one answer.