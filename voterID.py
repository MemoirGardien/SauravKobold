#!/usr/bin/env python3
import random

def main():
    vID = random_id(5)
    print(vID)


def random_id(length):
    alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789'
    id = ''
    for i in range(0,length):
        id += random.choice(alphanum)

    return id

if __name__ == '__main__':
    print ("This project sucks")
    main()
