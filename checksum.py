import hashlib

# File to check
fname = input("Enter file name: ")
# this gets the md5 checksum of the original file
md5a = hashlib.md5(open(fname ,'rb').read()).hexdigest()
print (md5a)
#---------------------------------------------------------------------
#gets file to check against
checkfile = input('Enter file name to check contents against: ')
#open file
opencf = open(checkfile, 'rb')
#read the contents of the file
data = opencf.read()
#create md5 checksum of file
md5b = hashlib.md5(data).hexdigest()
print(md5b)
#---------------------------------------------------------------------
# comparing the original md5 with new md5
if md5a == md5b:
    print("Checksum IS correct.")
else:
    print ("Checksum IS NOT correct.")
