# Random-Prompt-Generator
A simple python script to randomly generate prompts for use with AI Art programs, based on an inputted .txt file. Outputs as a .txt file.

### Usage
To use, fill out the promptSource.txt file with chunks of prompts that you'd like to randomly mix - separate the chunks into categories by leaving a blank line between the categories.

One line from each category will be selected when generating prompts, which you can do by double-clicking fullGen.bat (to generate all possible combinations of a single line from each category) or randomGen.bat (to specify a random number of combinations to generate).

Run testGen.bat to check that your input files are formatted correctly without generating prompts.

### Labels
If you wish, fill out the labeledPromptSource.txt file with a label corresponding to each line in promptSource.txt, and a file will be outputted when you run the program which generates a simplified version of each prompt, using the labels rather than the full prompt chunks, in addition to the normal output.

### Advanced Use
Change the arguments listed in the .bat files in order to customize the program's output by changing the input file, renaming the output file, simplifying the output, etc.

Running  `python randomGen.py -h -arg` in a comman prompt will list the possible arguments.

Change the SAMPLING and SAMPLINGEST arguments in randomGen.py to match the sampling steps and estimated time (in seconds) for each step to estimate generation time on your computer. Current values are based on my own preferences and generation times.
