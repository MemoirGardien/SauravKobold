import hashlib

# File to check
fname = input("Enter file name: ")


# this gets the md5 checksum of the original file
original_md5 = hashlib.md5(open(fname ,'rb').read()).hexdigest()
print (original_md5)

checkfile = input('Enter file name to check contents against: ')

# Open,close, read file and calculate MD5 on its contents
with open(checkfile, 'rb') as file_to_check:
    # read contents of the file
    data = file_to_check.read()
    # get the md5 checksum of the new file
    md5_returned = hashlib.md5(data).hexdigest()

# comparing the original MD5 with freshly calculated md5
if original_md5 == md5_returned:
    print("Checksum IS correct.")
else:
    print ("Checksum IS NOT correct.")
