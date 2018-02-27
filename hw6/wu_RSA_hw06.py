#!/usr/bin/env python

import sys
import pickle
from PrimeGenerator import *
from BitVector import *
import numpy as np
from solve_pRoot import *

def keygeneration():
    e_val = 65537
    e_bitvec = BitVector(intVal  = e_val)
    while True:
        generator = PrimeGenerator(bits = 128, debug = 0)
        p = generator.findPrime()
        q = generator.findPrime()
        p_bitvec = BitVector(intVal = p,size = 128)
        q_bitvec = BitVector(intVal = q,size = 128)
        ##check if p and q satisfy three conditions, if not generate new p and q
        if p_bitvec[0] & p_bitvec[1] & q_bitvec[0] & q_bitvec[1]:
            if p != q:
                if (int(BitVector(intVal = (p-1)).gcd(e_bitvec)) == 1) & (int(BitVector(intVal = (q-1)).gcd(e_bitvec)) == 1):
                    break
    ##calculte totient_n and d
    n = p * q
    totient_n = (p - 1) * (q - 1)
    tn_bitvec = BitVector(intVal = totient_n)
    d_bitvec = e_bitvec.multiplicative_inverse(tn_bitvec)
    key = [e_val, int(d_bitvec), n, p, q]
    return key

def encryption(inputfile, outfile, e,n,p,q):
    bv = BitVector(filename = inputfile)
    fptr = open(outfile,'w')
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        while bitvec.length() < 128:
            bitvec += BitVector(textstring = "\n")
        bitvec.pad_from_left(128)
        ##Use CRT to calculate power % n
        vp = pow(int(bitvec),e,p)
        vq = pow(int(bitvec),e,q)
    	p_bitvec = BitVector(intVal = p,size = 128)
    	q_bitvec = BitVector(intVal = q,size = 128)
    	xp = q * int(q_bitvec.multiplicative_inverse(p_bitvec))
    	xq = p * int(p_bitvec.multiplicative_inverse(q_bitvec))
    	data = (vp * xp + vq *xq) % n
        BitVector(intVal = data,size = 256).write_to_file(fptr)
        ##print(BitVector(intVal = data,size = 256).get_bitvector_in_hex())
    fptr.close()

def decryption(inputfile, outfile,d,n,p,q):
    bv = BitVector(filename = inputfile)
    fptr = open(outfile,'w')
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(256)
        ##Use CRT to calculate power % n
        vp = pow(int(bitvec),d,p)
        vq = pow(int(bitvec),d,q)
    	p_bitvec = BitVector(intVal = p,size = 128)
    	q_bitvec = BitVector(intVal = q,size = 128)
    	xp = q * int(q_bitvec.multiplicative_inverse(p_bitvec))
    	xq = p * int(p_bitvec.multiplicative_inverse(q_bitvec))
    	data = (vp * xp + vq *xq) % n
        BitVector(intVal = data,size = 128).write_to_file(fptr)
        ##print(BitVector(intVal = data,size = 128).get_bitvector_in_hex())

    fptr.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Error: wrong number of arguments")
        exit()
    if sys.argv[1] == '-e':
        key = keygeneration()
        encryption(sys.argv[2],sys.argv[3],key[0],key[2],key[3],key[4])
        fptr = open('key.txt','w')
        pickle.dump(key,fptr)
        fptr.close()
    elif sys.argv[1] == '-d':
        with open ('key.txt') as fptr:
            key = pickle.load(fptr)
        ##print(key[1])
        ##print(key[3])
        ##print(key[4])
        decryption(sys.argv[2],sys.argv[3],key[1],key[2],key[3],key[4])
