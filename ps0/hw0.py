import sys
import os
import re
## CS 458/558
## Fall 2015
## hw0.py
## Aleksandra Zakrzewska



## Function 1: palindrome

def palindrome(filename = "/usr/share/dict/words", letter = "all"):
	# open file
	file = open(filename, 'r')

	palindromes = []

	for line in file:
		#skip any words that do not begin with the correct letter--upper or lower case
		i =0
		while (not(line[i].isalpha())):
			#print line[i], "is not alpha"
			i+=1
			
		if ((letter!= "all" and (line[i].lower()!=letter.lower()))):
			#print line[i], letter
			continue
		length = len(line);
		j =length-2
		#check if all letters are reversed at the end
		word = line[:length-1]
		while i<j:
			#print word[i], word[j]
			if ( ((not (word[i].isalpha())) and (not(word[i].isdigit()))) or (word[i] == ' ')):
				i+=1
			elif ( ((not (word[j].isalpha())) and (not(word[j].isdigit()))) or (word[j] == ' ')):
			#elif ( (not (word[j].isalpha()) or word[i].isdigit()) or (word[i] == ' ')):
				j-=1
			elif ((word[i].lower() != word[j].lower()) and (ord(word[i]) != ord(word[j]) -32)):
				#print word[i].lower(), word[j].lower(),  "not same"
				break
			else:
				#print "were same"
				i+=1
				j-=1
		else: 
			print word
			palindromes.append(word)
	#print palindromes



# >>> palindrome(letter = "b")
# B
# b
# Bab
# bab
# B/B
# BB
# bb
# BBB
# Beeb
# Bib
# bib
# Bob
# bob
# boob
# Bub
# bub



## Function 2: anagram

# Example output
# >>> anagram()
# ['alerts', 'alters', 'artels', 'estral', 'laster', 'lastre', 'rastle', 'ratels', 'relast', 'resalt', 'salter', 'slater', 'staler', 'stelar', 'talers']
# 
# >>> anagram(target = 'male')
# ['alem', 'alme', 'amel', 'lame', 'leam', 'male', 'meal', 'mela']

def anagram(filename = "/usr/share/dict/words", target = False):
	
	file = open(filename, 'r')

	anagrams = {}

	maxcount=0
	maxset=""

	for line in file:
		#for every word in the file, count the number of each letter 
		freq= [0] *27 
		word = line[:len(line)-1]
		for i in range (len(word)):
			if ( not (word[i].isalpha())):
				continue
			freq[ord(line[i].lower())-97]+=1
		freqtup= tuple(freq)
		#use that set as a key to store the word in a dict
		if freqtup not in anagrams:
				anagrams[freqtup]=[0, []]
		anagrams[freqtup][0]+=1
		anagrams[freqtup][1].append(word)
		#keep track of which key has the highest count of words
		if anagrams[freqtup][0]>maxcount:
			maxset=freqtup
			maxcount = anagrams[freqtup][0]
	
	#find the target key and print the set of words with that key
	if target!=False:
		targetSet= [0] *27 
		target=target.lower()
		
		for i in range (len(target)):
			if ( not (target[i].isalpha())):
				continue
			targetSet[ord(target[i])-97]+=1
		targetSet= tuple(targetSet)
		for key in anagrams[targetSet][1]:
			print key

	#print the set of words belonging to the most counted key 
	else :
		#print anagrams[maxset][1]
		for key in anagrams[maxset][1]:
			print key


#call the appropriate function with the appropriate argument
def main(arg):
	if len(arg)<1:
		print ("Usage: hw0.py anag|palin [target | letter] [filename = filename]")
		exit()
		#print arg
	if arg[0] == "anagram":
		target = False
		if len(arg)>=2:
			target = arg[1]
		anagram( target = target)

	elif arg[0] == "palindrome":
		letter="all"
		if len(arg)>=2:
			letter = arg[1]
		palindrome( letter = letter)


if __name__ == "__main__":
   main(sys.argv[1:])
