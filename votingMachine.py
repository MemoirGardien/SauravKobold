#! /usr/bin/env python3

# Reliable Systems Voting Systems Project
# Team: Barbara Crotty, Brianna Estrada, Ryan Norton, Saurav Gautam, Quan Le
# Date: Nov 27th 2016

from collections import OrderedDict
import string
import crusher
import re


#list of characters the voterID can have
id_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\()*+,-./:;<=>?@[]^_`'

#index is for first calculating voterID
#Candidates is a dictionary where all the different positions and candiates are stored.

index = 0;

candidates = OrderedDict()

#stores the votes for each candidate
candidate_votes = OrderedDict()
# An array of all positions. 

# Stores the positions for each candidate
# It's main function is to keep track of the index of the position
# Because dictionaries keep jumbling the order. 
candidate_positions = []

orig_array = []
results = []

outputstr = ""
txt_database = ""
basename = ""


def vote(position, name):
# generates a txt_database that contains a number that represents the position and alphabet
# that represents the index of the candidate.

    global id_string

    updateCandidates(position, name)
    s = candidate_positions.index(position)
    p = candidates[position].index(name)
    
    candidate_votes[position][p] += 1
    
    return str(s) + id_string[p]
    


def crush(input_string):
    # Takes a string as an input. Then utilizing the noisy channel within crusher.py
    # flips the bits in the string based on the configuration
    channel = crusher.Channel()
    
    return channel.mangle(input_string)
    

def getReliableOutput(string_array):
    # Outputs a string with the most frequently occuring characters within an 
    # array of strings
    # e.g. string_array = ['acb','aac',bab]
    # output: 'aab'
    # 
    # This allows us to eliminate any flipped bits from the data passed into
    # crusher
    
    length = len(string_array[0])
    output = ''
        
    for i in range(length):
        # Combining the characters of the strings passed in at each index
        
        combined_chars = ""
        first = True
        for string in string_array:
            if first:
                combined_chars = string[i]
                first = False
            else:
               combined_chars = string[i]
            
        
        output += str(frequent_char(combined_chars))
   
    return output 

def frequent_char(text):
    
    #Gets the most frequent char in a string
    
    charset = ''.join(sorted(text))

    maxcount = 0
    maxchar = None

    for item in charset.lower():
        charcount = text.count(item)

        if charcount > maxcount :
            maxcount = charcount
            maxchar = item

    return maxchar

def updateCandidates(position, name):
    # Updates the candidates dictionary in the case a new position or candidate is added.
    
    ''' Dynamically adding candidates'''
    if position not in candidates.keys():
        candidates[position] = [name];
        candidate_votes[position] = [0];
        candidate_positions.append(position);
        
    else:
        if name not in candidates[position]:
            candidates[position].append(name)
            candidate_votes[position].append(0)



def testReliability(iterations = 10):
    ## Reads the database that is being passed. When the data is read back
    ## it will be passed through crusher based on the number of iterations.
    ## 
    ## Then it will be passed through a function that will get the most reliable outputs
    ## be compared and the reliability will be calculated
    

    global candidates
    
    votes = txt_database[:txt_database.index('****')]
    split = votes.split('|')
    
    count = 0
    failed = 0
    
    for vote in split:
        string_array = []
        count += 1
        
        for i in range(iterations):
            # Appending the noisy data into string_array
            string_array.append(crush(vote))
        
        check_string = getReliableOutput(string_array)
        
        if check_string.startswith('None'):
            check_string = check_string[4:]
        
        if vote != check_string:
            # If the final and initial strings are not equal
            failed += 1
        
        
             
    print ('Reliability %: ' + str((float(count - failed)/count)*100))

def getResults():
    
    for position in candidate_positions:
        tally = OrderedDict()
        for i,votes in enumerate(candidate_votes[position]):
            tally[candidates[position][i]] = votes
        
        #Sorting the vote tally
        tally = dict(sorted(tally.items(), key=lambda x:x[1], reverse=True));
        
        first = True
        for name in tally.keys():
            if first:
                print ( 'New ' + position + ': ' + name + ' ('+ str(tally[name]) +' votes)' )
                first = False
            
        
        
def getReceipt():
    
    _id = input("Enter voter_id:");
    
    global candidates
    
    votes = txt_database[:txt_database.index('****')]
    split = votes.split('|')
    
    print ( 'There were ' + str(len(split)) + ' voters' )
    
    voteString = ''
    voterIdFound = False
    
    for vote in split:
        
        #Splitting the vote into an array of numbers (positions) and characters(names)
        data_array =  re.findall('\d+|\D+', vote)
        
        first = True
        
        for ch in data_array:
            if first and not voterIdFound:
                #This is the voter_id
                first = False
                if _id == ch:
                    voterIdFound = True
                    voteString += 'Voter Id: ' + _id + '\n'
            elif voterIdFound:
                if ch.isdigit():
                    position = candidate_positions[int(ch)]
                else:
                    name = candidates[position][id_string.index(ch)]
                    voteString += 'Voted ' + name + ' for ' + position + '\n'
        
        if voterIdFound:
            break;
    
    if not voterIdFound:
        print ( 'Id not found\n')
        return
    
    print ( '============= VOTER RECEIPT ===============')
    print ( '\nThank you for voting \nYou cast the following votes: \n')
    print ( voteString     )
    print ( '\n===============xxxxxx=====================')


def readFile(fileName):
    global txt_database #the txt_databaseg that the program is working with.
    global candidates
    global basename
    basename = fileName[:-4]
    count = 0
    candidates = {}
    
    
    with open(fileName) as f: #Basically opens the file and then check for the line
        content = f.readlines()
        receipt_log = ''
        
        first_voter = True
        
        for line in content:
            arr = line.split("\t");

            command = arr[0]
            if command == 'VOTER\n':
                
                if first_voter:
                    first_voter = True
                
                _id = genId()
                txt_database += '|' + _id
                
                if first_voter:
                    first_voter = True
                elif not first_voter:
                    receipt_log += '=========== xxxxx =============\n'
                receipt_log += '===========VOTER RECEIPT=============\n'
                receipt_log += 'Voter Id: ' + _id + '\n'
                
                
            elif command == 'VOTE':
                position = arr[1]
                name = arr[2][:-1]
                
                txt_database += vote(position, name);
                receipt_log += 'Voted ' + name + ' for ' + position + '\n'
            
                
                
        txt_database += ('****' + str(candidates))
        
        fileMaker(basename + '-votelog.txt', receipt_log)

def fileMaker(filename, string):
    
    with open(filename, 'w+') as file:
        file.write(string)
   

      
      

def genId():
#generates a new id for new voters.
    global index

    if index < 78:
        val = id_string[index];
        index += 1
        return val
    elif index >= 78:
        x = index % 78
        y = index/78 - 1
        val = id_string[y] + id_string[x]
        index += 1
        return val
    
    
        
def dashboard():
## The voting system dashboard that the user interacts with.

    count = 0

    while count == 0:
        #user picks an option
        print  ('Choose an option')
        print  ('1. Read Votes File')
        print  ('2. Get Receipt')
        print  ('3. View Results')
        print  ('4. Test Reliability')
        print  ('5. Exit')
        option = int(input("Enter option:"));


        if option == 1:
            filename = input('Enter the filename you would like to read:')
            readFile(filename)
        #option 1 must be run before option 2 or 3, otherwise they will not work 
        elif option == 2:
            print ('You chose to get your voter reciept')
            getReceipt()
        elif option == 3:
            print ('These are the election results: ');
            getResults()
        elif option == 4:
            testReliability();
        elif option == 5:
            print ('Thank you for using our highly sophisticated voting system.')
            break;
        else:
            print ('Enter a valid option')
            
getReliableOutput(['aaa','aab'])
dashboard()
