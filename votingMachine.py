#! /usr/bin/env python3
#Reliable Systems Project
#Team: Ryan Norton, Saurav Gautam, Quan Le, Barbara Crotty, Brianna.
#Date: 11/17/2016


# Candidates = {
#     President: []
# }
import string
import crusher


#list of characters the voterID can have
id_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\()*+,-./:;<=>?@[]^_`'

#index is for first calculating voterID
#Candidates is a dictionary where all the different positions and candiates are stored.

index = 0;

candidates = {}
orig_array = []

outputstr = ""



def vote(position, name):
# generates a string that contains a number that represents the position and alphabet
# that represents the index of the candidate.


    global id_string
    updateCandidates(position, name)
    print position
    print name
    p = candidates.keys().index(position)
    s = candidates[position].index(name)
    '''print str(s) + id_string[p]'''
    return str(s) + id_string[p]

def updateCandidates(position, name):
# Updates the candidates dictionary in the case a new position or candidate is added.
    ''' Dynamically adding candidates'''
    if position not in candidates.keys():
        candidates[position] = [name]
    else:
        if name not in candidates[position]:
            candidates[position].append(name)


def readFile():
#Reads the input command file and then stores and processes the data in a string.
    strin = '' #the string that the program is working with.
    global candidates
    candidates = {}
    with open('bigeasy.txt') as f: #Basically open the file and then check for the line
        content = f.readlines()

        for line in content:
            arr = line.split("\t");

            command = arr[0]
            if command == 'VOTER\n':
                strin += '|' + genId();
            elif command == 'VOTE':
                position = arr[1]
                name = arr[2][:-1]
                strin += vote(position, name);

        strin += str(candidates)

        print strin;

def genId():
#generates a new id for new voters.
    global index

    if index < 78:
        val = id_string[index];
        print val
        index += 1
        return val
    elif index >= 78:
        x = index % 78
        y = index/78 - 1;
        val = id_string[y] + id_string[x]
        print id_string[y] + id_string[x]
        index += 1
        return val

def dashboard():
# The interface of what the voter system will look like. It is still under construction.
# Will be updated in the final submission.
    count = 0

    while count == 0:
        #user picks an option
        print ('Choose an option')
        print ('1. Vote')
        print ('2. Get Receipt')
        print ('3. Exit')
        # print ('4. GenId')
        option = int(input("Enter option:"));

        if option == 1:
            print('You chose to vote.')
            readFile()
        elif option == 2:
            print('You chose to get your voter reciept')
        elif option == 3:
            print ('Thank you for using our highly sophisticated voting system.')
            break;
        else:
            print ('Enter a valid option')

dashboard()
