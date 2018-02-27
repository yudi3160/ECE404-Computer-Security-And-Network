#!/usr/bin/env/python

### DES_wu.py

##This program only works well with Python2, running with Python3 would result in unknown bugs
import sys
from BitVector import *

################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8,
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19,
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
arrays = []
with open('s-box-tables.txt') as f:
    for line in f:
        ##store lines wih length larger than 4 into arrays
        if len(line) > 4:
            row = line.split()
            arrays.append(row)
s_box = []
##Seperate arrays into 8 boxes
for i in range(0,32, 4):
    s_box.append([arrays[k] for k in range(i, i+4)]) # S_BOX
f.close()



#######################  Get encryptin key from user  ###########################

def get_encryption_key(): # key
    ## ask user for input
    while True:
        key = raw_input("Please enter a 8 characters key: ")
        ## make sure it satisfies any constraints on the key
        if len(key) == 8:
            break
        else:
            print("Your key is not 8 characters long")
    user_key_bv = BitVector(textstring = key)
    key_bv = user_key_bv.permute(key_permutation_1)        ## permute() is a BitVector function
    return key_bv


################################# Generatubg round keys  ########################
def extract_round_key( nkey ): # round key
    round_key = []
    for i in range(16):
         [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
         ##Shift two halves
         left << shifts_key_halvs[i]
         right << shifts_key_halvs[i]
         ##Combine two halves and permute
         nkey = left + right
         nkey.permute(key_permutation_2)
         round_key.append(nkey)
    return round_key


########################## encryption and decryption #############################

def des(encrypt_or_decrypt, input_file, key ):
    bv = BitVector( filename = input_file )
    ##change output_file name depends on Encrypt or Decrypt mode
    if encrypt_or_decrypt == 1:
        output_file = 'encrypted.txt'
    else:
        output_file = 'decrypted.txt'
    ##Set write byte mode
    FILEOUT = open( output_file, 'wb' )

    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral
        ##find if bitvec is complete 64 bit, if no, padding from the right
        bit_ct = bitvec.length()
        if(bit_ct != 64):
            bitvec.pad_from_right(64 - bit_ct)
        [LE, RE] = bitvec.divide_into_two()
        ##extract all round keys
        round_key = extract_round_key(key)
        for i in range(16):
            ##E-step
            temp3 = RE
            temp = RE.permute(expansion_permutation)
            if(encrypt_or_decrypt == 1):
                temp = temp ^ round_key[i]
            else:
                temp = temp ^ round_key[15 - i]
            ##S-BOX
            temp2 = BitVector(size = 0)
            for i in range(8):
                row = 2 * temp[i * 6] + temp[i * 6 + 5]
                col = 8 * temp[i * 6 + 1] + 4 * temp[i * 6 + 2] + 2 * temp[i * 6 + 3] + temp[i * 6 + 4]
                temp2 += BitVector(intVal = int(s_box[i][row][col]), size = 4)
            ##P-BOX
            temp2 = temp2.permute(p_box_permutation)

            RE = LE ^ temp2
            LE = temp3
        ##output
        combined = RE + LE
        combined.write_to_file(FILEOUT)
    FILEOUT.close()



#################################### main #######################################

def main():
    ## write code that prompts the user for the key
    ## and then invokes the functionality of your implementation
    key = get_encryption_key()
    while True:
        function = raw_input("Encryption or Decryption?: ")
        if (function == 'encryption') or (function == 'Encryption') or (function == 'En') or (function == 'en'):
            function = 1
            break
        elif (function == 'decryption') or (function == 'Decryption') or (function == 'De') or (function == 'de'):
            function = 0
            break
        else:
            print("Please enter a valid option.\n")

    des(function,'message.txt',key)
if __name__ == "__main__":
    main()
