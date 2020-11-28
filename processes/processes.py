from multiprocessing import Pool
from random import randrange
from os import getpid

def guess_the_number(suggestion: int)->bool:
    """
    Returns equivalence of suggestion and answer
    :return equivalence of suggestion and answer
    """
    print(f"Current using process ID: {getpid()}")
    return suggestion==randrange(0, 3)

if __name__=="__main__":
    pool=Pool(processes=2)
    while(True):
        try:
            suggestion=int(input("Insert a number between 0 and 3: "))
            results=pool.map(guess_the_number, [suggestion]*2)
            print(f"Result: {results[0] or results[1]}")
        except: print("Insert type error occured")
        next=input("Do you want to continue? ")
        if(next!="Y"): break
    pool.close()