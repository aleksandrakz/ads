## CS 458/558
## Fall 2015
## author: Ronghui Gu
## email: ronghui.gu@yale.edu

# This is a sample test script

import os
import re

# pre-process the word, remove all the non-alphanumeric characters
def pre_process_word (word):
    return re.sub ("\W", "", word.lower ())

# test whether all the required files are existing
def test_file_exists (total_cases):
    flag = False
    if not os.path.exists ("hw0.py"):
        print ">> hw0.py is not found, please add your hw0.py in this directory"
    elif not os.path.exists("hw0.R"):
        print ">> hw0.R is not found, please add your hw0.R in this directory"
    elif not os.path.exists ("testwords"):
        print ">> testwords (the dictionary file) is not found"
    else:
        flag = True
        for i in xrange (0, total_cases):
            if not os.path.exists ("cases/case" + str (i)):
                print ">> the test case " + str (i) +" is not found"
                flag = False
    return flag

# get the result from the Python code
def get_Python_result (command):
    # run the Python code in the shell
    # I use "####" as the special mark to split the output of hw0.py and the function call I invoke
    p_output = os.popen ("python -c 'import hw0; print \"####\"; hw0." + command + "'").readlines ()
    # get the index of "####"
    index = p_output.index ("####\n")
    p_output_set = set ([""])
    for word in p_output[index + 1:] :
        # add the processed word into the result [SET]
        # I use a set, instead of the list.
        # Therefore, the order or the duplication of the output DOESN'T matter
        p_output_set.add (pre_process_word (word))
    return p_output_set

# get the result from the R code
def get_R_result (command):
    # run the R code in the shell
    # I use "####" as the special mark to split the output of hw0.py and the function call I invoke
    p_command = "Rscript -e 'source(\"hw0.R\"); print (\"####\"); " + command + "'"
    p_output = os.popen (p_command).readlines ()
    p_list = [];
    for word in p_output:
        # remove the line number like "[1]"
        # split the word with "\"", such that it can deal with the case that you failed to print a word per line
        p_list += re.sub ("\[\d+\]", "", word.lower ()).split ("\"")
    # get the index of "####"
    index = p_list.index ("####")
    p_output_set = set ([""])
    for word in p_list[index + 1:] :
        # add the processed word into the result [SET]
        # I use a set, instead of the list.
        # Therefore, the order or the duplication of the output DOESN'T matter
        p_output_set.add (pre_process_word (word))
    return p_output_set

def grade_hw0 (total_cases = 5):
    # test whether all the required files are existing
    if not test_file_exists (total_cases):
        print ">> the test is uncomplete, since some files are missing"
        return
    # the number of passed cases
    passed_cases = 0
    for i in xrange (0, total_cases):
        case_filename = "cases/case" + str (i)
        print ">> case " + str (i) + " start"
        with open (case_filename) as case_file:
            # read the case file
            case = case_file.readlines()
            case_output_set = set ([""])
            # get the standard output [SET]
            for word in case[1:]:
                case_output_set.add (pre_process_word (word))  
            # get the command to execute
            command = case[0].strip()
            # test the result
            if get_Python_result (command) == case_output_set:
                passed_cases += 1
                print "\tPython code passed"
            else:
                print "\tPython code failed!!!!!!"        
            if get_R_result (command) == case_output_set:
                passed_cases += 1
                print "\tR code passed"
            else:
                print "\tR code failed!!!!!!"        
    print ">> result: " + str (passed_cases) + "/" + str (total_cases * 2) + " cases passed!"                
    return

grade_hw0 (5)
