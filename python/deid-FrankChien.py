import re
import sys
import locationtagger
from nltk.tag import pos_tag

"""
Frank Chien
Assignment 8 - de-identification
10/15/21

This script adapts the phone tagger patient information de-identification algorithm.
The chosen category for this assignment is 'locations'.
In the deid_phone function, instead of calling check_for_phone this script will call check_for_location
The check_for_location function represents my work.

Instead of the approach used in the PELR script, this assignment uses a natural language processing approach.
The strategy for location PHI identification is as follows
!) use location tagger to identify locations
2) use nltk part of speech tagging to identify proper nouns
3) The intersect of locations and proper nouns are flagged as location PHI

The reason why proper nouns were used as a requirement is because the words such as "home" or "hospital" would
represent (and correctly be tagged) as locations. However, do not offer identifiable patient information.
Locations such as "Calvert" or "Boston" for instance would be identifiable information and are proper nouns.

One difficulty this strategy encountered was the sensitivity and specificity of the strategy relies on the performance
of both the location tagger and the part of speech tagger. Since the input was medical documentation, which includes
specific language, syntax, sympbols, and abbreviations which are not seen in other domains of common English,the
natural language processing components had difficulty. For example, "Aline" was frequently tagged as a location, whereas
physicians/nurses would understand 'aline' as an arterial line, a piece of medical equipment. Another example is that
some notes were written in all-caps. The NLTK POS tagger relies on caplitalization to identify proper nouns, thus
for these notes, many tokens were incorrectly tagged as as 'NNP', or proper noun.

In summary, using a natural language processing approach to medical note deindification is a challenge due to the difficulty in parsing medical language with NLP tools,
which can be very different syntactically and in lexicon from common English.

Unfortunately, the performance of this NLP strategy as implemented is poor. Though the algorithm detected some locations correctly
(56 true positives), the number of false positives and false negatives were great (816, and 311, respectively). A large number of
tokens were incorrectly identified as a location (such as "aline") and further, incorrectly tagged as proper nouns.
This exercise has been a demonstration of both how medical record de-identification works, but also of the difficulty in
analyzing medical texts as natrual language.
 
The location tagger was obtained at
https://pypi.org/project/locationtagger/
"pip install location tagger" was run on terminal to install the location tagger
Following the instructions from the website, the command "python -m spacy download en" was required.
The location tagger is maintained by kaushiksoni10 and has an open source license
Per webiste, "OSI approved::MIT license"

Part of speech tagging was achieved throught he NLTK tagger pos_tag. 

"""

def check_for_phone(patient,note,chunk, output_handle):
    #ths is the original code written by Clifford Lab
    """
    Inputs:
        - patient: Patient Number, will be printed in each occurance of personal information found
        - note: Note Number, will be printed in each occurance of personal information found
        - chunk: one whole record of a patient
        - output_handle: an opened file handle. The results will be written to this file.
            to avoid the time intensive operation of opening and closing the file multiple times
            during the de-identification process, the file is opened beforehand and the handle is passed
            to this function. 
    Logic:
        Search the entire chunk for phone number occurances. Find the location of these occurances 
        relative to the start of the chunk, and output these to the output_handle file. 
        If there are no occurances, only output Patient X Note Y (X and Y are passed in as inputs) in one line.
        Use the precompiled regular expression to find phones.
    """
    # The perl code handles texts a bit differently, 
    # we found that adding this offset to start and end positions would produce the same results
    offset = 27

    # For each new note, the first line should be Patient X Note Y and then all the personal information positions
    output_handle.write('Patient {}\tNote {}\n'.format(patient,note))

    # search the whole chunk, and find every position that matches the regular expression
    # for each one write the results: "Start Start END"
    # Also for debugging purposes display on the screen (and don't write to file) 
    # the start, end and the actual personal information that we found


    for match in ph_reg.finditer(chunk):
                
            # debug print, 'end=" "' stops print() from adding a new line
            print(patient, note,end=' ')
            print((match.start()-offset),match.end()-offset, match.group())
                
            # create the string that we want to write to file ('start start end')    
            result = str(match.start()-offset) + ' ' + str(match.start()-offset) +' '+ str(match.end()-offset) 
            
            # write the result to one line of output
            output_handle.write(result+'\n')


def check_for_location(patient,note,chunk, output_handle):
    #this is the function wrote by Frank Chien for the assignment
    #please see comment above for description of the strategy

    offset = 27 #identified offset required by clifford lab
    output_handle.write('Patient {}\tNote {}\n'.format(patient,note))
    #print(patient, note) #allows us to see how many notes the algorithm has worked through
    
    #using the location tagger 
    locations = locationtagger.find_locations(text = chunk) #locationtagger returns a location object
    all_locations = locations.countries + locations.regions + locations.cities #location objects stores locations in 3 places, as countries, locations, and cities
   
    #using the NLTK part of speech tagger
    tagged_chunk = pos_tag(chunk.split()) #first split into tokens, then tag

    for location in all_locations: #iterates through identified locations
        for token_pos in tagged_chunk: #looks for location in list of tagged tokens. token_pos is a tuple: (token, part of speech tag)
            if location.lower() == token_pos[0].lower(): #to match location to token, only lower cases are used
                if token_pos[1]=='NNP': #if the token is a proper noun, we have identified a possible location PHI
                    substring=token_pos[0] 
                    indices=[_.start() for _ in re.finditer(substring,chunk)] #uses a regex to identify all instances of the location within the chunk
                    for start_pos in indices: #composes the result line to be written to the output file
                        start_pos = start_pos - offset 
                        end_pos = start_pos + len(substring)
                        result = str(start_pos) + ' ' + str(start_pos) + ' '+ str(end_pos)

                        output_handle.write(result+'\n') #writes result to output file

                    break #break the loop and check for the next location token. The regex iterator will already obtain all instances of the location in the chunk.
                
                
    
def deid_phone(text_path= 'id.text', output_path = 'phone.phi'):
    
    """
    Inputs: 
        - text_path: path to the file containing patient records
        - output_path: path to the output file.
    
    Outputs:
        for each patient note, the output file will start by a line declaring the note in the format of:
            Patient X Note Y
        then for each phone number found, it will have another line in the format of:
            start start end
        where the start is the start position of the detected phone number string, and end is the detected
        end position of the string both relative to the start of the patient note.
        If there is no phone number detected in the patient note, only the first line (Patient X Note Y) is printed
        to the output
    Screen Display:
        For each phone number detected, the following information will be displayed on the screen for debugging purposes 
        (these will not be written to the output file):
            start end phone_number
        where `start` is the start position of the detected phone number string, and `end` is the detected end position of the string
        both relative to the start of patient note.
    
    """
    # start of each note has the patter: START_OF_RECORD=PATIENT||||NOTE||||
    # where PATIENT is the patient number and NOTE is the note number.
    start_of_record_pattern = '^start_of_record=(\d+)\|\|\|\|(\d+)\|\|\|\|$'

    # end of each note has the patter: ||||END_OF_RECORD
    end_of_record_pattern = '\|\|\|\|END_OF_RECORD$'

    # open the output file just once to save time on the time intensive IO
    with open(output_path,'w+') as output_file:
        with open(text_path) as text:
            # initilize an empty chunk. Go through the input file line by line
            # whenever we see the start_of_record pattern, note patient and note numbers and start 
            # adding everything to the 'chunk' until we see the end_of_record.
            chunk = ''
            #remove later
        #    counter=0
            for line in text:
                record_start = re.findall(start_of_record_pattern,line,flags=re.IGNORECASE)
                if len(record_start):
                    patient, note = record_start[0]
                chunk += line

                # check to see if we have seen the end of one note
                record_end = re.findall(end_of_record_pattern, line,flags=re.IGNORECASE)

                if len(record_end):
                    # Now we have a full patient note stored in `chunk`, along with patient numerb and note number
                    # pass all to check_for_phone to find any phone numbers in note.

                    #check_for_phone(patient,note,chunk.strip(), output_file)
                    check_for_location(patient, note, chunk.strip(), output_file)
         #           counter+=1
          #          if(counter>0):
           #             break

                    #this the one we need to modify above - 
                    
                    # initialize the chunk for the next note to be read
                    chunk = ''

                
if __name__== "__main__":
    print(sys.prefix)
    deid_phone(sys.argv[1], sys.argv[2])
    
