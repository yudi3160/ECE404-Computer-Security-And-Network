#!/usr/bin/env/python

### Average_wu.py
import sys
import random
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
        if len(line) > 4:
            row = line.split()
            arrays.append(row)
s_box = []
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
         left << shifts_key_halvs[i]
         right << shifts_key_halvs[i]
         nkey = left + right
         nkey.permute(key_permutation_2)
         round_key.append(nkey)
    return round_key


########################## encryption and decryption #############################

def des(LE,RE,round_key):
    for i in range(16):
        ##E-step
        temp3 = RE
        temp = RE.permute(expansion_permutation)

        temp = temp ^ round_key[i]
      
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
    return combined



#################################### main #######################################

def main():
    ## prompts the user for the key
    key = get_encryption_key()
    input_file = 'message.txt'

    ##problem II part I
    bv = BitVector( filename = input_file )
    block_ct = 0
    total_diff = 0
    round_key = extract_round_key(key)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 ) 
        ##count how many plaintext blocks
        block_ct += 1
	##make sure bitvec is 64 bits, if not, pad from right
        bit_ct = bitvec.length()
        if(bit_ct != 64):
            bitvec.pad_from_right(64 - bit_ct)
	##modify one random bit 
        change_bit = BitVector(intVal = (1 << random.randint(0,63)),size = 64)
        bitvec2 = bitvec ^ change_bit

        [LE, RE] = bitvec.divide_into_two()
        [LE2, RE2] = bitvec2.divide_into_two()

        cypher1 = des(LE,RE,round_key)
        cypher2 = des(LE2,RE2,round_key)
        diff_bits = (cypher1 ^ cypher2).count_bits()
        total_diff += diff_bits
    ##find average difference on one block
    avg_diff = total_diff / block_ct
    print "Average ciphertext change for plaintext change is %d" % avg_diff

    ##problem II part II
	
    ##store original cipher in result1
    bv = BitVector( filename = input_file )
    result1 = BitVector(size = 0)
    while(bv.more_to_read): 
        bitvec = bv.read_bits_from_file( 64 )   
        bit_ct = bitvec.length()
        if(bit_ct != 64):
            bitvec.pad_from_right(64 - bit_ct)
        [LE, RE] = bitvec.divide_into_two()
        cypher1 = des(LE,RE,round_key)
        result1 += cypher1

    ##randomly change S_box for the first time and store result in result2
    for i in range(8):
         for j in range(4):
             row = []
             row = random.sample(range(16),16)
             s_box[i][j] = row

    bv = BitVector( filename = input_file )
    result2 = BitVector(size = 0)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )   
        bit_ct = bitvec.length()
        if(bit_ct != 64):
            bitvec.pad_from_right(64 - bit_ct)
        [LE, RE] = bitvec.divide_into_two()
        cypher2 = des(LE,RE,round_key)
        result2 += cypher2
   ##randomly change S_box for the second time and store result in result3
    for i in range(8):
        for j in range(4):
            row = []
            row = random.sample(range(16),16)
            s_box[i][j] = row

    bv = BitVector( filename = input_file )
    result3 = BitVector(size = 0)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )   
        bit_ct = bitvec.length()
        if(bit_ct != 64):
            bitvec.pad_from_right(64 - bit_ct)
        [LE, RE] = bitvec.divide_into_two()
        cypher3 = des(LE,RE,round_key)
        result3 += cypher3
    ##find differences and find average for one block
    diff_bits1 = (result1 ^ result2).count_bits()
    diff_bits2 = (result1 ^ result3).count_bits()
    avg_diff = (diff_bits1 + diff_bits2) / 2 / block_ct
    print "Average ciphertext change for S_box change is %d" % avg_diff

    ##problem II part IIII
    total_key = 0
    ##try 5 different modified keys
    for ct in range(5):
        bv = BitVector( filename = input_file )
        change_bit = BitVector(intVal = (1 << random.randint(0,63)),size = 64)
        alter_key = key ^ change_bit
        round_key = extract_round_key(alter_key)
        result4 = BitVector(size = 0)
        while(bv.more_to_read):
            bitvec = bv.read_bits_from_file( 64 )   
            bit_ct = bitvec.length()
            if(bit_ct != 64):
                bitvec.pad_from_right(64 - bit_ct)
            [LE, RE] = bitvec.divide_into_two()
            cypher4 = des(LE,RE,round_key)
            result4 += cypher4
        diff_key = (result1 ^ result4).count_bits()
        total_key += diff_key
    avg_key = total_key / 5 / block_ct
    print "Average ciphertext change for key change is %d" % avg_key
if __name__ == "__main__":
    main()
