#!/usr/bin/python

### wu_Field.py



def main():
    usr_input = input("Please enter a small integer: ")
    prime = 1
    for i in range(2,int(usr_input)):
        if int(usr_input) % i == 0:
            prime = 0
            break
    f = open('output.txt','w')
    if prime == 1:
        f.write("field")
    else:
        f.write("ring")
    f.close()


if __name__ == "__main__":
    main()
