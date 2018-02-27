#!/usr/bin/env python

import sys
import pickle
from PrimeGenerator import *
from BitVector import *
import numpy as np
from solve_pRoot import *
def keygeneration():
    e_val = 3
    e_bitvec = BitVector(intVal  = e_val)
    while True:
        generator = PrimeGenerator(bits = 128, debug = 0)
        p = generator.findPrime()
        q = generator.findPrime()
        p_bitvec = BitVector(intVal = p,size = 128)
        q_bitvec = BitVector(intVal = q,size = 128)
        if p_bitvec[0] & p_bitvec[1] & q_bitvec[0] & q_bitvec[1]:
            if p != q:
                if (int(BitVector(intVal = (p-1)).gcd(e_bitvec)) == 1) & (int(BitVector(intVal = (q-1)).gcd(e_bitvec)) == 1):
                    break
    n = p * q
    totient_n = (p - 1) * (q - 1)
    tn_bitvec = BitVector(intVal = totient_n)
    d_bitvec = e_bitvec.multiplicative_inverse(tn_bitvec)
    key = [e_val, int(d_bitvec), n, p, q]
    return key
def encryption(inputfile,e,n,p,q):
    bv = BitVector(filename = inputfile)
    output = BitVector(size = 0)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        while bitvec.length() < 128:
            bitvec += BitVector(textstring = "\n")
        bitvec.pad_from_left(128)
        vp = pow(int(bitvec),e,p)
        vq = pow(int(bitvec),e,q)
    	p_bitvec = BitVector(intVal = p,size = 128)
    	q_bitvec = BitVector(intVal = q,size = 128)
    	xp = q * int(q_bitvec.multiplicative_inverse(p_bitvec))
    	xq = p * int(p_bitvec.multiplicative_inverse(q_bitvec))
    	data = (vp * xp + vq *xq) % n
        output += BitVector(intVal = data,size = 256)

    return output

if __name__ == '__main__':
    key1 = keygeneration()
    key2 = keygeneration()
    key3 = keygeneration()
    file1 = encryption(sys.argv[1],key1[0],key1[2],key1[3],key1[4])
    ##print(file1.get_bitvector_in_hex())
    ##print()
    ##print(key1[2])
    ##print()
    file2 = encryption(sys.argv[1],key2[0],key2[2],key2[3],key2[4])
    ##print(file2.get_bitvector_in_hex())
    ##print()
    ##print(key2[2])
    ##print()
    file3 = encryption(sys.argv[1],key3[0],key3[2],key3[3],key3[4])
    ##print(file3.get_bitvector_in_hex())
    ##print()
    ##print(key3[2])
    ##print()
    N_val = key1[2] * key2[2] * key3[2]
    N1 = N_val/key1[2]
    N2 = N_val/key2[2]
    N3 = N_val/key3[2]
    N1_MI = BitVector(intVal = N1).multiplicative_inverse(BitVector(intVal = key1[2]))
    N2_MI = BitVector(intVal = N2).multiplicative_inverse(BitVector(intVal = key2[2]))
    N3_MI = BitVector(intVal = N3).multiplicative_inverse(BitVector(intVal = key3[2]))
    fptr = open(sys.argv[2],'w')
    for i in range(0,len(file1),256):
        bitvec1 = file1[i+0:i+256]
        bitvec2 = file2[i+0:i+256]
        bitvec3 = file3[i+0:i+256]
        M_3 = (int(bitvec1) * N1 * int(N1_MI) + int(bitvec2) * N2 * int(N2_MI) + int(bitvec3) * N3 * int(N3_MI)) % N_val
        M = solve_pRoot(3,M_3)
        BitVector(intVal = M, size = 128).write_to_file(fptr)
        ##print(BitVector(intVal = M, size = 128).get_bitvector_in_hex())
    fptr.close()
