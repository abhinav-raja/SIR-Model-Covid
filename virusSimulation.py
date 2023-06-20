from math import floor
from random import random
# newCases = i * uninfected^2 * infected / total ^2
# i = newCases * total^2 / (uninfected^2 * infected)
# 23 april : i = 1300 * (1352600000)^2 / (1352598700)^2 *14000
# 26 april:
###newcases = 1490, total = 1352600000, infected = 21003, uninfected = 1352578997
### i = 0.0709 as of 26 April 2020
### newcases=217353, infected = 14500000
### i = 0.01529 as of 17 April 2021
##population object, will be used a lot.
##Set total to total People
##Set infected to infected people at simulation start.
##Set cured to cured people at simulation start.
##set NewCases to new cases on simulation start
NewCases = 217353
population = {
"total" : 1352600000,
"infected" : 14500000,
"cured" : 12876000, ##cured includes deaths
##the following two will initialise themselves
"uninfected" : 0,
"vulnerable" : 0,
}
population['uninfected'] = population['total'] - population['infected']
population['vulnerable'] = population['uninfected'] - population['cured']
##probability of virus transfer; this is the product of virus spread chance and chance that people will meet
infectiousness = NewCases * (population['total']^2) /((population['vulnerable']^2) * population['infected'])


###how many days to simulate
days = 200
##predicts the day on which infection starts to slow. Initialise to 0
turnDay  = 0
##predicts the maximum no.of cases
maxCases = 0

peakNewCases = 0
peakDay = 0

##this will keep track of people who get cured eventually
##CoVID seems to have a curing time of 20 days for mild cases (20 days)
cureArray = []
cureLength = 20

for day in range(0,days):
    population['vulnerable'] = population['total'] - population['cured']
    population['uninfected'] = population['vulnerable'] - population['infected']
    newInfections = floor((infectiousness+(random()*0.002) - 0.001)* population['infected']*((population['uninfected'])**2)/(population['total']**2))
    cureArray.append(newInfections)
    population['infected'] += newInfections
    #factoring for decreasing infectiousness rate due to quarantine measures...activate next line optionally
    #infectiousness -= 0.001
    if day >= cureLength:
        population['infected'] -= cureArray[day - cureLength]
        population['cured'] += cureArray[day - cureLength]
        deltaCasesPrev = deltaCases
        deltaCases = newInfections - cureArray[day - cureLength]
        if deltaCases <= 0 and turnDay == 0:
            turnDay = day
            maxCases = population['infected']
        deltaDeltaCases = deltaCases - deltaCasesPrev
        if deltaDeltaCases <= 0 and peakDay == 0:
            peakDay = day
            peakNewCases = newInfections
    else:
        deltaCases = newInfections
    print(day, population['infected'], population['cured'], newInfections, deltaCases)

print('turning points', turnDay,maxCases)
print('peak', peakDay, peakNewCases)
print('infectiousness', infectiousness)
