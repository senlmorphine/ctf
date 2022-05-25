import re
import sys
import string
from sys import stdout
sys.stderr = stdout

from sys import modules
modules.clear()
del modules

trusted_builtins = """
    True False type int print exec
    """.split()

sanitize = re.compile(
    r'(?:globals|__|import|locals|exec|eval|join|format|replace|translate|try|except|with|content|frame|back)'
    ).sub

alphabet = ' \n\r0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ(),.:;<=>[]_{}'

t1 = ''.join(chr(code) for code in range(256))
t2 = []
for i in t1:
    if i in alphabet:
        t2.append(i)
    else:
        t2.append(' ')
trans_table = str.maketrans(t1, ''.join(t2))

avengers_IQ = 200
PERCEPTION_CHECK = 0

del alphabet, t1, t2, i, sys, string, re


def clear_builtins():
    orig = __builtins__.__dict__.copy()
    __builtins__.__dict__.clear()
    for i in trusted_builtins:
        __builtins__.__dict__[i] = orig[i]

where_is_stone = "**********************"
iam_iron_man = "**********************"
thanos_the_goat = "**********************"

def main():
    print("""
MCSC 2022
    """)

    print ("Welcome to The Avengers End Game!\n\n"
           'Can you steal the stone?\n'
           'Submit your code with Ctrl+D or ///\n')

    stdout.flush()
    
    code = []
    total_chars = 0
    while True:
        try:
            value = input(">>>")
            total_chars += len(value)
            assert total_chars < 1337
            if value == '///':
                break
            code.append(value)
        except EOFError:
            break
    
    code = sanitize("/NO/", '\n'.join(code).translate(trans_table))
    code = code.replace("/NO/closure/NO/", "__closure__")
    code = code.replace("/NO/code/NO/", "__code__")
    code = code.replace("/NO/defaults/NO/", "__defaults__")
    code = code.replace("/NO/doc/NO/", "__doc__")
    clear_builtins()

    def jail():

        def exec_code(inp, ctx):
            exec(inp, ctx)
            print("\nLet's see if you got anyhing...\n"
                  "what you got from the avengers is:"
            )
            try:
                assert FLAG != iam_iron_man 
                print(FLAG)
            except:
                print('Nothing ¯\_(ツ)_/¯')

        def have_you_where_is_stone():
            global FLAG
            FLAG = where_is_stone

        def is_the_avengers_really_gone():
            global FLAG
            FLAG += iam_iron_man

        def did_you_remember_to_take_all_the_loot():
            global FLAG
            FLAG += thanos_the_goat

        def explore():
            
            a = "Commendable!"
            b = "Smart!"
            c = "Try again!"

            def explore():

                def explore():
                    if 21 < PERCEPTION_CHECK:
                        print(a)
                        have_you_where_is_stone()
                    else:
                        print(c)

                if 22 > avengers_IQ:
                    print(b)
                    is_the_avengers_really_gone()
                else:
                    print(c)
                
                return explore

            did_you_remember_to_take_all_the_loot()
            return explore

        exec_code(code, {"explore":explore})

    jail()