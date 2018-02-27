#!/usr/bin/python
### ece404_hw04_wu.py

import sys
from BitVector import *

def mixcol(bitvec):
    AES_modulus = BitVector(bitstring='100011011')
    MUL2 = BitVector(bitstring = '00000010')
    MUL3 = BitVector(bitstring = '00000011')
    bitvec2 = BitVector(intVal = 0,size = 128)
    for i in range(4):

        bitvec2[(i*32):(i*32+8)] = bitvec[(i*32):(i*32+8)].gf_multiply_modular(MUL2,AES_modulus,8) ^ \
                                   bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MUL3,AES_modulus,8) ^ \
                                   bitvec[(i*32+16):(i*32+24)] ^ \
                                   bitvec[(i * 32 + 24):(i * 32 + 32)]
        bitvec2[(i*32+8):(i*32+16)] = bitvec[(i*32):(i*32+8)] ^ \
                                      bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MUL2,AES_modulus,8) ^ \
                                      bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MUL3,AES_modulus,8) ^ \
                                      bitvec[(i*32+24):(i*32+32)]
        bitvec2[(i*32+16):(i*32+24)] = bitvec[(i*32):(i*32+8)] ^ \
                                       bitvec[(i*32+8):(i*32+16)] ^ \
                                       bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MUL2,AES_modulus,8) ^ \
                                       bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MUL3,AES_modulus,8)
        bitvec2[(i*32+24):(i*32+32)] = bitvec[(i*32):(i*32+8)].gf_multiply_modular(MUL3,AES_modulus,8) ^ \
                                   bitvec[(i*32+8):(i*32+16)] ^ \
                                   bitvec[(i*32+16):(i*32+24)]^ \
                                   bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MUL2,AES_modulus,8)
    return bitvec2

def invmixcol(bitvec):
    AES_modulus = BitVector(bitstring='100011011')
    MULE = BitVector(bitstring = '00001110')
    MUL9 = BitVector(bitstring = '00001001')
    MULB = BitVector(bitstring = '00001011')
    MULD = BitVector(bitstring = '00001101')
    bitvec2 = BitVector(intVal = 0, size = 128)
    for i in range(4):
        bitvec2[(i*32):(i*32+8)] = bitvec[(i*32):(i*32+8)].gf_multiply_modular(MULE,AES_modulus,8) ^ \
                                   bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MULB,AES_modulus,8) ^ \
                                   bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MULD,AES_modulus,8) ^ \
                                   bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MUL9,AES_modulus,8)
        bitvec2[(i*32+8):(i*32+16)] = bitvec[(i*32):(i*32+8)] .gf_multiply_modular(MUL9,AES_modulus,8) ^ \
                                      bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MULE,AES_modulus,8) ^ \
                                      bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MULB,AES_modulus,8) ^ \
                                      bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MULD,AES_modulus,8)
        bitvec2[(i*32+16):(i*32+24)] = bitvec[(i*32):(i*32+8)].gf_multiply_modular(MULD,AES_modulus,8) ^ \
                                       bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MUL9,AES_modulus,8) ^ \
                                       bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MULE,AES_modulus,8) ^ \
                                       bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MULB,AES_modulus,8)
        bitvec2[(i*32+24):(i*32+32)] = bitvec[(i*32):(i*32+8)].gf_multiply_modular(MULB,AES_modulus,8) ^ \
                                   bitvec[(i*32+8):(i*32+16)].gf_multiply_modular(MULD,AES_modulus,8) ^ \
                                   bitvec[(i*32+16):(i*32+24)].gf_multiply_modular(MUL9,AES_modulus,8) ^ \
                                   bitvec[(i*32+24):(i*32+32)].gf_multiply_modular(MULE,AES_modulus,8)
    return bitvec2


def getsubbyte(data,sbox):
    [LE,RE] = data.divide_into_two()
    subdata = BitVector(intVal = sbox[int(LE) * 16 + int(RE)], size = 8)
    return subdata
def gfunc(sbox,word,roundconst):
    ##circular shift one byte
    word = word << 8
    ##subbyte
    new_word = getsubbyte(word[0:8],sbox) + getsubbyte(word[8:16],sbox) + getsubbyte(word[16:24],sbox) + getsubbyte(word[24:32],sbox)
    ##xor with roundconst
    new_word = new_word ^ (roundconst + BitVector(intVal = 0, size = 24))

    return new_word
def getkeyschedule(subBytesTable,key):
    keyschedule = []
    roundconst = getRC()
    for i in range(0,16,4):
        keyschedule.append(BitVector(textstring =(key[i],key[i+1],key[i+2],key[i+3])))
    for i in range(4,44,4):
        keyschedule.append(gfunc(subBytesTable,keyschedule[i-1],roundconst[int((i-4)/4)]) ^ keyschedule[i - 4])
        keyschedule.append(keyschedule[i-3] ^ keyschedule[i])
        keyschedule.append(keyschedule[i-2] ^ keyschedule[i+1])
        keyschedule.append(keyschedule[i-1] ^ keyschedule[i+2])
    return keyschedule

def getRC():
    AES_modulus = BitVector(bitstring='100011011')
    RC = BitVector(bitstring = '00000001')
    roundconst = []
    for i in range(10):
        roundconst.append(RC)
        RC = RC.gf_multiply_modular(BitVector(bitstring='00000010'),AES_modulus,8)
    return roundconst

def getSbox(choice):
    AES_modulus = BitVector(bitstring='100011011')
    subBytesTable = []                                                  # for encryption
    invSubBytesTable = []                                               # for decryption
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For byte scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For byte scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))
    if choice == 1 :
        return subBytesTable
    elif choice == 0:
        return invSubBytesTable

def encrypt(inputfile,outputfile,key):
    bv = BitVector( filename = inputfile )
    FILEOUT = open(outputfile,'wb')
    subBytesTable = getSbox(1)                                               # for encryption
    keyschedule = getkeyschedule(subBytesTable,key)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        bit_ct = bitvec.length()
        if(bit_ct != 128):
            bitvec.pad_from_right(128 - bit_ct)
        ##first_round
        bitvec = bitvec ^ (keyschedule[0]+keyschedule[1]+keyschedule[2]+keyschedule[3])
        for i in range(10):
            ##1 substition process
            for j in range(16):
                bitvec[j*8:(j*8 + 8)] = getsubbyte(bitvec[j*8:(j*8+8)],subBytesTable)
            ##2 shift row
            bitvec = bitvec[0:8]  + bitvec[40:48] + bitvec[80:88] +   bitvec[120:128] + \
                     bitvec[32:40]+ bitvec[72:80] + bitvec[112:120] + bitvec[24:32]   + \
                     bitvec[64:72]+ bitvec[104:112] + bitvec[16:24] + bitvec[56:64]   + \
                     bitvec[96:104]+ bitvec[8:16] + bitvec[48:56] + bitvec[88:96]
            ##3 mix columns
            if i != 9:
                bitvec = mixcol(bitvec)
            ##4 add round key
            bitvec = bitvec ^ (keyschedule[4+i*4]+keyschedule[5 + i *4]+keyschedule[6 + i * 4]+keyschedule[7 + i * 4])
        bitvec.write_to_file(FILEOUT)
    FILEOUT.close()


def decrypt(inputfile,outputfile,key):
    bv = BitVector( filename = inputfile )
    FILEOUT = open(outputfile,'wb')
    invSubBytesTable = getSbox(0)                                              # for decryption
    keyschedule = getkeyschedule(getSbox(1),key)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        bit_ct = bitvec.length()
        if(bit_ct != 128):
            bitvec.pad_from_right(128 - bit_ct)
        ##first_round
        bitvec = bitvec ^ (keyschedule[40]+keyschedule[41]+keyschedule[42]+keyschedule[43])
        for i in range(10):
            ##1 inverse shift row
            bitvec = bitvec[0:8]  + bitvec[104:112] + bitvec[80:88] +   bitvec[56:64] + \
                     bitvec[32:40]+ bitvec[8:16] + bitvec[112:120] + bitvec[88:96]    + \
                     bitvec[64:72]+ bitvec[40:48] + bitvec[16:24] + bitvec[120:128]   + \
                     bitvec[96:104]+ bitvec[72:80] + bitvec[48:56] + bitvec[24:32]
            ##2 substition process
            for j in range(16):
                bitvec[j*8:(j*8 + 8)] = getsubbyte(bitvec[j*8:(j*8+8)],invSubBytesTable)
            ##3 add round key
            bitvec = bitvec ^ (keyschedule[36 - i*4]+keyschedule[37 - i *4]+keyschedule[38 - i * 4]+keyschedule[39 - i * 4])
            ##4 mix columns
            if i != 9:
                bitvec = invmixcol(bitvec)
        bitvec.write_to_file(FILEOUT)
    FILEOUT.close()

def main():
    key = 'howtogettosesame'
    while 1:
        choice = input("Plese choose encryption or decryption: ")
        if (choice == 'encryption') | (choice == 'en') | (choice == 1):
            encrypt('plaintext.txt','encryptedtext.txt',key)
            break
        elif (choice == 'decryption') | (choice == 'de') | (choice == 0):
            decrypt('encryptedtext.txt','decryptedtext.txt',key)
            break
        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
