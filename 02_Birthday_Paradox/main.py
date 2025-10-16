import datetime,random

def getBirthdays(numOf_bdays):
    '''Returns a list of number random date objects for birthdays'''
    birthdays=[]
    for i in range(numOf_bdays):
        # the yera is important for our simulation as long as all yras are same
        startOfyear=datetime.date(2001,1,1)

        # Get a random day in a year
        randomNumOfDays=datetime.timedelta(random.randint(0,364))
        birthday=startOfyear+randomNumOfDays
        birthdays.append(birthday)
    return birthdays


def getMatch(birthdays):
    """Returns the date object of a birthday that occurs more than once
       in the birthdays list."""
    if(len(birthdays)==len(set(birthdays))):
       return None

    for a,bdayA in enumerate(birthdays):
       for b,bdayB in enumerate(birthdays[a+1:]):
            if bdayA==bdayB:
             return bdayA  


# Display the intro:
print('''Birthday Paradox, by Al Sweigart al@inventwithpython.com
 
  The Birthday Paradox shows us that in a group of N people, the odds
  that two of them have matching birthdays is surprisingly large.
  This program does a Monte Carlo simulation (that is, repeated random
  simulations) to explore this concept.
 
  (It's not actually a paradox, it's just a surprising result.)
''')

MONTHS=('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

while True: 
    # keep asking until ser give valid amount
    print('How many bdays shall I generate?(Max 100)')
    response=input('>')
    if response.isdecimal() and 0< int(response)<=100:
        numBDays=int(response)
        break
print()

print('Here are', numBDays, 'birthdays:')
birthdays = getBirthdays(numBDays)
for i, birthday in enumerate(birthdays):
    if i != 0:
        # Display a comma for each birthday after the first birthday.
        print(', ', end='')
    monthName = MONTHS[birthday.month - 1]
    dateText = '{} {}'.format(monthName, birthday.day)
    print(dateText, end='')
print()
print()

match = getMatch(birthdays)
print('In this simulation, ', end='')
if match != None:
    monthName = MONTHS[match.month - 1]
    dateText = '{} {}'.format(monthName, match.day)
    print('multiple people have a birthday on', dateText)
else:
    print('there are no matching birthdays.')
print()



# Run through 100,000 simulations:
print('Generating', numBDays, 'random birthdays 100,000 times...')
input('Press Enter to begin...')

print('Let\'s run another 100,000 simulations.')
simMatch = 0  # How many simulations had matching birthdays in them.
for i in range(100000):
    # Report on the progress every 10,000 simulations:
    if i % 10000 == 0:
        print(i, 'simulations run...')
    birthdays = getBirthdays(numBDays)
    if getMatch(birthdays) != None:
        simMatch = simMatch + 1
print('100,000 simulations run.')

# Display simulation results:
probability = round(simMatch / 100000 * 100, 2)
print('Out of 100,000 simulations of', numBDays, 'people, there was a')
print('matching birthday in that group', simMatch, 'times. This means')
print('that', numBDays, 'people have a', probability, '% chance of')
print('having a matching birthday in their group.')
print('That\'s probably more than you would think!')