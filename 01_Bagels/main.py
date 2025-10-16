import random
NUM_DIGITS=3
MAX_GUESSES=10

def main():
     print('''Bagels, a deductive logic game.
By Al Sweigart al@inventwithpython.com

I am thinking of a 3(dpends on you difficulty level)-digit number with no repeated digits.
Try to guess what it is. Here are some clues:
When I say:    That means:
Pico         One digit is correct but in the wrong position.
Fermi        One digit is correct and in the right position.
Bagels       No digit is correct.

For example, if the secret number was 248 and your guess was 843, the
clues would be Fermi Pico.''')
     level=input('Choose difficulty level- Easy/Medium/Hard')
     if(level.lower()=='easy'):
        NUM_DIGITS=3
        MAX_GUESSES=10
        points=1
     if(level.lower()=='medium'):
        NUM_DIGITS=4
        MAX_GUESSES=15
        points=2
     if(level.lower()=='hard'):
        NUM_DIGITS=5
        MAX_GUESSES=20
        points=3
     fun(NUM_DIGITS,MAX_GUESSES,points)


def fun(NUM_DIGITS,MAX_GUESSES,points):
     score=0
     while True:
        # int number=random.randint(100,1000)
        secNum=getsecNum()
        print(f''' You have {MAX_GUESSES} guesses to get it. SCORE:{score}''')
        n=1
        while(n<=MAX_GUESSES):
            guessNum=''
            while(len(guessNum)!=NUM_DIGITS or not guessNum.isdecimal()):
                print('Guess#{}: '.format(n))
                guessNum=input('> ')
            clues=getClues(guessNum,secNum)
            print(clues)
            n=n+1
            if(guessNum==secNum):
             score+=points   
             break
            if(n>MAX_GUESSES):
             print('You are out  of guesses')
             print('The number was {}'.format(secNum))

        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
          break
     print('Thanks for playing!') 


def getClues(guessNum,secNum):
    if(guessNum==secNum):   
     print('You got it!')
    clues=[]
    for i in range(len(guessNum)):
        if(guessNum[i]==secNum[i]):
         clues.append('Fermi')

        elif(guessNum[i] in secNum):
         clues.append('Pico')
    if(len(clues)==0):
     return 'bagels'

    else:
        # Sort the clues into alphabetical order so their original order
        # doesn't give information away.
        clues.sort()
        # Make a single string from the list of string clues.
        return ' '.join(clues) 

def getsecNum():
    """Returns a string made up of NUM_DIGITS unique random digits."""
    numbers=list('012345689')
    random.shuffle(numbers)

    # Get the first NUM_DIGITS digits in the list for the secret number:
    secNum=''
    for i in range(NUM_DIGITS):
        secNum+= str(numbers[i])

    return secNum

if __name__ == '__main__':
    main()



