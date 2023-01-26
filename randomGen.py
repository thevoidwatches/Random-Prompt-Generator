import sys
import os.path
import random as r

# CONSTANTS
SAMPLING = 28
SAMPLINGEST = 24
FILENAME = os.path.basename(__file__)

# FILE ARGUMENTS
if "-h" in sys.argv or "-help" in sys.argv:
    print("\nThis is a program designed to generate multiple prompts for us in an image-generating AI program,")
    print("such as Stable Diffusion. It does so by taking a .txt file containing different possible items for")
    print("each category within a prompt, then creating a prompt from each possible combination of one item")
    print("from each category. It can also be used to regenerate a random subset of those possible combinations.")
    
    print("\nThe provided .txt file should be formatted as follows:\n")
    
    print("   category1item1")
    print("   category1item2\n")

    print("   category2item1")
    print("   category2item2")
    print("   category2item3\n")

    print("   category3item1")
    print("   category3item2")
    print("   category3item3")
    print("   category3item4")
    
    print("\nThis program requires at least one argument, and accepts several optional others.")
    if not "-arg" in sys.argv:
        print("View them with the -arg argument.")
        exit()

if "-arg" in sys.argv:
    if not "-h" in sys.argv and not "-help" in sys.argv:
        print("\nThis program requires at least one argument, and accepts several optional others.")
    print("Usage is as follows, in any order:")
    
    print("> INFILE (REQUIRED)")
    print(">> " + FILENAME + " -if FILENAME.TXT")
    print(">>> Selects the file from which the possible items will be chosen.")
    print(">>> The selected file must exist, must not be blank, and must be formatted correctly.")
    
    print("> OUTFILE (OPTIONAL)")
    print(">> " + FILENAME + " -of FILENAME.TXT")
    print(">> Names the file into which the created prompts will be saved.")
    print(">> The file will be overwritten if it already exists.")
    
    print("> LABEL (OPTIONAL)")
    print(">> " + FILENAME + " -l")
    print(">> If there is a properly-formatted version of the infile with 'labeled' prepended to it,")
    print("   generates an additional outfile with 'labeled' prepended to it, which sumarizes the")
    print("   generated prompt for each line.")
    print(">> The labeled file must be identical to the infile but with a label for each line,")
    print("   separated from the rest of the line by a : and a space.")
    
    print("> RANDOM (OPTIONAL)")
    print(">> " + FILENAME + " -r [NUMBER]")
    print(">> Lets you choose a number of prompts to randomly choose from all possible prompts.")
    print(">> If a number is not provided, the program will automatically choose 1 possible prompt.")
    print(">> If the provided number is greater than the number of possible prompts, the program")
    print("   will duplicate random lines from the prompt to reach the requested number of prompts.")
    
    print("> TEST (OPTIONAL)")
    print(">> " + FILENAME + " -t")
    print(">> Causes the program to check the infile for correct formatting,")
    print("   rather than creating the actual combinations or writing to the outfile.")
    
    print("> VERBOSE (OPTIONAL)")
    print(">> " + FILENAME + " -v")
    print(">> Causes the program to give status updates as it runs, as well as an estimate of the")
    print("   generation time for the final file (based on constants representing the number of")
    print("   sampling steps and estimated time for each step.")
    
    print("> HELP (OPTIONAL)")
    print(">> " + FILENAME + "-h")
    print(">> " + FILENAME + "-help")
    print(">> Prints a help message instead of running the program.")
    print(">> Compatible with the -arg argument.")
    
    print("> ARGUMENTS (OPTIONAL)")
    print(">> " + FILENAME + "-arg")
    print(">> Prints this argument list instead of running the program.")
    print(">> Compatible with the -h and -help arguments.")
    exit()
    
test = False
if "-t" in sys.argv:
    test = True
""" If Test is true, the program will read the provided file and check for correct formatting,
rather than performing the actual combinations or writing to the final file. By default,
this is off.
"""

verbose = False
if "-v" in sys.argv:
    verbose = True
""" If Verbose is true, the program will print status updates as it runs,
and also give an estimate on how long the actual generation time will take to run,
based on the total number of combinations and the SAMPLING and SAMPLINGEST constants
provided at the top of the file. By default, this is off.
"""

random = 0
if "-r" in sys.argv:
    try:
        random = int(sys.argv[sys.argv.index("-r")+1])
    except:
        random = 1
""" If Random is true, the program will generate a limited number of prompts from all possible combinations,
allowing you to use it to randomly create prompts rather than creating all possible prompts. You can
provide a number of random prompts to create - if you don't, it will create only a single prompt.
"""

labeled = False
if "-l" in sys.argv:
    labeled = True
""" If Labeled is true, the program will look for a file corresponding to the infile with Labeled prepended
to it, and follow that along with the file to regenerate labels for each prompt it creates.
"""
    
if "-if" in sys.argv:
    try:
        infile = sys.argv[sys.argv.index("-if")+1]
        
        """ Prepends 'labeled' to the provided infile, if Labeled is true.
            Works for files in a subfolder, e.g. if you have character-specific
        prompts in a lower folder from the main program."""
        if labeled and "/" in infile:
            splitInFile = infile.split("/")
            if os.path.exists(splitInFile[0]+"/labeled" + splitInFile[1][0].upper() + splitInFile[1][1:]):
                labelFile = splitInFile[0]+"/labeled" + splitInFile[1][0].upper() + splitInFile[1][1:]
        elif labeled and os.path.exists("labeled" + infile[0].upper() + infile[1:]):
            labelFile = "labeled" + infile[0].upper() + infile[1:]
        else:
            #Turns off Labeled if it can't find the file, but continues to run.
            labeled = False
            print("Could not find a labeled text file. Running without labels.")
    except:
        print("\nPlease provide the name of the .txt file to read from, using the -if argument.")
        print("Format as " + FILENAME + " -if FILENAME.TXT")
        exit()
else:
    print("\nPlease provide the name of the .txt file to read from, using the -if argument.")
    print("Format as " + FILENAME + " -if FILENAME.TXT")
    exit()
""" Specify the name of the file that the program will read the prompt items from.
If not provided, the program will not run.
"""
    
outfile = "prompts.txt"
if "-of" in sys.argv:
    try:
        outfile = sys.argv[sys.argv.index("-of")+1]
    except:
        print("\nNo filename provided. Using default name prompts.txt.")
""" Specify the name of the file that the program will write the generated prompts to.
By default, this is prompts.txt.
"""

append = False
if "-a" in sys.argv:
    append = True

try:    
    """ Generates an array called prompts which contains each line of the infile.
    If Labeled is true, does the same thing for the labelFile.
    """
    
    with open(infile) as f:
        prompts = [line.rstrip() for line in f]
    if labeled:
        with open(labelFile) as lf:
            labels = [label.rstrip() for label in lf]
    if prompts == []:
        # If prompts is empty - meaning that the file was empty - it exits the TRY block into the EXCEPT.
        exit()
    if labeled:
        if labels == [] or len(prompts) != len(labels):
            exit()
    if verbose:
        # Reports the succesful file read, if verbose.
        labelReport = ""
        if labeled:
            labelReport = " and " +labelFile
        print("\nSuccessfully read from " + infile + labelReport + ".")
except:
    # If there was an error, reports the location of the error and exits the program.
    print("\nUnable to read from the provided .txt file. Please check that the name of the file is correct, and that the file is not blank.")
    exit()

try:
    # Creates an empty array and a variable to track the point at which the last split occured.
    splitPrompts = []
    if labeled:
        splitLabels = []
    lastSplit = 0
    for lineNum in range(len(prompts)):
        if prompts[lineNum] == "":
            """ Counts through each line in the prompts array. Iif the line is an empty string,
            extracts the prompts array from the previous split up to the current line
            (not counting the empty line) and adds it to the splitPrompts array,
            then sets the new location of the last split.
            """
            splitPrompts.append(prompts[lastSplit:lineNum])            
            if labeled:
                splitLabels.append(labels[lastSplit:lineNum])
            lastSplit = lineNum+1
            
            if splitPrompts[-1] == []:
                # If the last split was empty, removes it from the splitPrompts array.
                splitPrompts.pop(-1)
                if labeled:
                    splitLabels.pop(-1)
    # Adds the last chunk of the prompts array.
    splitPrompts.append(prompts[lastSplit:])
    if labeled:
        splitLabels.append(labels[lastSplit:])
    if splitPrompts[-1] == []:
        # If the last split was empty, removes it from the splitPrompts array.
        splitPrompts.pop(-1)
        if labeled:
            splitLabels.pop(-1)
    
    """ At this point, splitPrompts is an array of subarrays,
    each subarray containing a chunk of lines from the infile
    which were separated by a blank line.
    
        If labeled is true, there is also splitLabels,
    which is similarly an array of subarrays contiaining
    chunks of lines from the labelfile separated by a
    blank line.
    """
    
    numCats = len(splitPrompts)
    if numCats <= 1:
        """ Reports if there is only one subarray in splitPrompts, meaning that there were no
        blank links separating lines within the original file.
        """
        print("Found only 1 category. Please check that your file is formatted correctly.")
        print("Separate each category with a single blank line.")
        print("Items within the category should be on a single line for each distinct item.")
        print("If you have only one category, you can use your file directly.")
    elif verbose:
        # Reports the successful split, if verbose.            
        print("Successfully split " + infile + labelReport + " into " + str(len(splitPrompts)) + " categories.")
except:
    # If there was an error, reports the location of the error and exits the program.
    labelError = ""
    if labeled:
        labelError = "or " + labelFile
    print("\nEncountered an error while splitting " + infile + labelError + " into categories.")
    exit()

try:
    """ Runs through the number of items in each category. If Test is true, it prints them
    each out for the user to double-check - if Verbose is true, it instead prints the number
    of items in each category.
        As it does so, the program uses the acc variable to count the total number of
    combinations that will be generated.
    """
    acc = 1
    for i in range(numCats):
        numItems = len(splitPrompts[i])
        acc *= numItems
        if test:
            # Prints each category with each item in it, if test is true.
            print("> Category " + str(i+1))
            for j in range(numItems):
                if labeled:
                    print(">> " + str(i+1) + "." + str(j+1) + " " + splitLabels[i][j])
                else:
                    print(">> " + str(i+1) + "." + str(j+1) + " " + splitPrompts[i][j])
        elif verbose:
            # If test is not true, but verbose is, reports the number of items found in each category.
            print("   Found " + str(numItems) + " items in category " + str(i+1) + ".")
except:
    # If there was an error, reports the location of the error and exits the program.
    print("\nEncountered an error while counting items per category.")
    exit()
    
if verbose:
    try:
        """ Estimates the total number of seconds it will take to generate the full prompt list by
        multiplying acc (or random) by the number of sampling steps and the estimated time that
        each step will take.
        """
        if random:
            genSec = random * SAMPLING * SAMPLINGEST
        else:
            genSec = acc * SAMPLING * SAMPLINGEST
        # Divides down to get the number of minutes, hours, and days that the prompt list will take.
        genMin = genSec / 60
        genHours = genMin / 60
        genDays = int(genHours / 24)
        # Runs a modulo on hour and minutes to get remainders and round down to the nearest whole number.
        genHours = int(genHours % 24)
        genMin = int(genMin % 60)
        # Converts to a string depending on the total length.
        if genDays >= 365:
            genTime = str(int(genDays/365)) + " years and " + str(int((genDays % 365)/30)) + " months"
        elif genDays >= 32:
            genTime = str(int(genDays/30)) + " months and " + str(int((genDays % 30)/7)) + " weeks"
        elif genDays >= 10:
            genTime = str(int(genDays/7)) + " months and " + str(genDays % 7) + " days"
        elif genDays >= 3:
            genTime = str(genDays) + " days"
        elif genDays >= 1:
            genTime = str(genDays) + " days and " + str(genHours) + " hours"
        elif genHours >= 2:
            genTime = str(genHours) + " hours and " + str(genMin) + " minutes"
        elif genMin >= 2:
            genTime = str(genMin) + " minutes"
        else:
            genTime = str(genSec) + " seconds"
        
        # Prints the results.
        if random:
            print("Calulated " + str(acc) + " total combinations, of which " + str(random) + " will be generated.\n")
        else:
            print("Calculated " + str(acc) + " total combinations.\n")
        print("Estimating generation time with " + str(SAMPLING) + " sampling steps at an average of " + str(SAMPLINGEST) + " seconds per step...")
        print("Estimated generation time: " + genTime + ".")
        if not random:
            print("\nYou can reduce the generation time by removing one or more prompt categories,")
            print("or by reducing the items in each category. Removing items from smaller categories")
            print("will have a greater effect on the generation time.")
    except:
        # If there was an error, reports the location of the error and exits the program.
        print("\nEncountered an error while estimating generation time.")
        exit()
    
if not test:
    try:
        """ Sets prompts to be an empty array which will contain the generated prompts,
        as well as an array of 0s equal to the number of categories in length, which
        will be used to track which items are being used in the current prompt.
            If Labeled is true, runs the same operation on the labels.
        """
        
        prompts = []
        if labeled:
            labelsOut = []
        pRead = [0] * numCats
        combining = True
        while combining:
            # Creates an empty string, which will have one item from each category added to it.
            temp = ""
            if labeled:
                tempLabels = ""
            for i in range(numCats):
                # Counts through each category in splitPrompts and appends the pRead[i]th item from it to temp, as well as a comma.
                temp += splitPrompts[i][pRead[i]] + ", "
                if labeled:
                    tempLabels += splitLabels[i][pRead[i]] + ", "
            #adds all but the comma from temp as an entry into prompt.
            prompts.append(temp[:-2])
            if labeled:
                labelsOut.append(tempLabels[:-2])
            
            """ Counts from the back of pRead to the front. Adds 1 to the value of the current slot,
            and if that makes its value higher than the item count for that category, resets to 0 and
            moves to the previous slot in pRead.
                This continues until it iterrates a slot in pRead without resetting and movie to the
            previous slot, or until it resets the first slot, at which point it breaks the entire loop.
                The effect is to count through all possible combinations of pRead without going past
            the number of items in the relevant category for each slot of pRead.
            """
            
            for i in range(numCats):
                pRead[-1-i] += 1
                if pRead[-1-i] >= len(splitPrompts[-1-i]):
                    # Checks to see if the current slot's value needs to be reset.
                    if i+1 == numCats:
                        # Breaks the while loop when the first value would have been reset.
                        combining = False
                    # If the current slot isn't the first, sets its value to 0 and continues to the previous slot.
                    pRead[-1-i] = 0
                else:
                    # If the current slot didn't need to be reset, break the loop to generate the next prompt.
                    break
        if verbose:
            # Reports the successful generation of prompts, if verbose.
            print("\nSuccessfully generated " + str(len(prompts)) + " prompts.")
    except:
        # If there was an error, reports the location of the error and exits the program.
        print("\nEncountered an error while combining category items to create prompts.")
        exit()
        
if random:
    try:
        """ Gets random prompts from the full list of possibilities by randomly
        selecting them and adding them to an empty array until the array is
        the desired size.
        """
    
        selPrompts = []
        if labeled:
            selLabels = []
            
        while len(selPrompts) < random:
            choice = r.randrange(len(prompts))
            selPrompts.append(prompts[choice])
            if labeled:
                selLabels.append(labelsOut[choice])
        
        prompts = selPrompts
        if labeled:
            labelsOut = selLabels
            
        if verbose:
            # Reports the successful selection of prompts, if verbose.
            print("Successfully selected " + str(len(prompts)) + " prompts from " + str(acc) + " prompts.")
    except:
        print("\nEncountered an error while performing random selection.")
        exit()
                
if not test:
    try:
    # Empties the outfile, then writes each entry in the prompt array 
        if not append:
            open(outfile, 'w')
        with open(outfile, 'a') as f:
            if append:
                f.write("\n")
            totalPrompts = len(prompts)
            for line in range(totalPrompts):
                f.write(prompts[line])
                if line < totalPrompts - 1:
                    #writes a newline character after each entry, unless it's the last line of the file.
                    f.write("\n")
        if verbose:
            print("\nSuccessfully wrote " + str(len(prompts)) + " prompts to " + outfile + ".")
        if labeled:
            outLabels = "labeled" + outfile[0].upper() + outfile[1:]
            if not append:
                open(outLabels, 'w')
            with open(outLabels, 'a') as f:
                if append:
                    f.write("\n")
                totalLabels = len(labelsOut)
                for line in range(totalLabels):
                    f.write(labelsOut[line])
                    if line < totalLabels - 1:
                        f.write("\n")
            if verbose:
                print("Successfully wrote " + str(len(labelsOut)) + " prompt labels to " + outLabels + ".")
    except:
        #if there was an error, reports the location of the error and exits the program.
        print("Encountered an error while writing to " + outfile + ".")
        exit()