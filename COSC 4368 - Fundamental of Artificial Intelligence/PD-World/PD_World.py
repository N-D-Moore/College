#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Athena Group Project
"""
import numpy as np
import random
import pandas as pd 

def startTest(a,g):
    global steps, opCount, bank, bankArray, alpha, gamma, state, thisOp, p, pContains, drop, dContains, qTable, terms
    '''Initial conditions'''
    steps = 0 #Total number of operators 
    opCount = 0 #number of operatiors applied to reach terminal state
    bank = 0 #the bank account of the agent
  
    bankArray = [] #start a bank array for plotting 
    
    alpha = a
    gamma = g
    state = coordnatesToSpace(5,1) #Starting point
    thisOp = random.choice([0,2])
    #coordinates for pick up locations
    p = [coordnatesToSpace(3,5), 
         coordnatesToSpace(4,2)]
    pContains = [8,8] #boxes in locations respectively
    
    #coordinates for the drop off locatons
    drop = [coordnatesToSpace(1,1,True),
            coordnatesToSpace(1,5,True), 
            coordnatesToSpace(3,3,True),
            coordnatesToSpace(5,5,True)]
    dContains = [0,0,0,0] #drop off location initial boxes respectively
    qTable = np.zeros((50,6), dtype=float) # initiate empty q-table
    terms = list()
    
def reset():
    global pContains, dContains, terms, state, opCount, bank, steps, thisOp
    '''Resets the PD World to initial state after final state is reached'''
    state = coordnatesToSpace(5,1)
    thisOp = random.choice([0,2])
    opCount = 0 
    bank = 0 
    pContains = [8,8] #boxes in locations respectively
    dContains = [0,0,0,0] #drop off location initial boxes respectively
    statement = "TERMINATED at state "+ str(state) + " in " + str(steps) + " steps"
    print(statement,'\n')
    terms.append(statement)

def plot(Experiment):
    global bankArray, seed, terms, qTable
    '''Save plots to csv files'''
    terms
    df = pd.DataFrame(data=qTable[:,:])
    df.rename({ 0: 'North' , 1 : 'South', 2 : 'East', 3 : 'West', 
              4: 'Pickup' , 5 : 'Drop' }, axis='columns', inplace=True)
    df.head()
    df.to_csv("Experiment_"+Experiment+"_Run_"+str(seed)+".csv")
    
    pd.DataFrame(bankArray).to_csv("AgentBank_"+Experiment+"_Run_"+str(seed)+".csv")
    

def intersection(lst1, lst2):
    '''Get the like elements from two lists (to remove non aplicable operands)'''
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def stateSpace(state):
    global pContains, dContains
    '''outputs the state current state space, use this to check for final condition'''
    if state > 24:
        x = True
    else:
        x = False
    state = state % 25
    i = state // 5
    j = state % 5
    return(i, j, x, pContains[0],pContains[1],
           dContains[0], dContains[1], dContains[2], dContains[3], )
        
        
def coordnatesToSpace(x,y,p=False):
    '''Converts current coordinate to state index in the Q-table'''
    state = x*5 + y - 6
    if p == True: 
        state+=25
    return state

def pickUp(state):
    global p, pContains
    ''' returns True if this is a pickup location is available and is not empty'''
    if state<25:
        try:
            i = p.index(state)
            if (pContains[i] > 0):
                pContains[i] -= 1 #take box from location
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return False

def dropOff(state):
    global drop, dContains
    ''' returns True if this is a dropoff location is available and is not full'''
    if state>24:
        try:
            i = drop.index(state)
            if (dContains[i] < 4):
                dContains[i] += 1 #drop off box at location
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return False
    
def direction(state):
    ''' Returns a list of possible directions that the ai can move, the elements can be directly added to Q-table index to find next index
    0=North 1=South 2=East 3=West'''
    state = state% 25 # remove 25 if state is >25
    operators = [0,1,2,3]
    if state >= 0 and state <=4: #cannot move north
        operators.remove(0)
    if state >=20 and state <=24: #cannot move south
        operators.remove(1)
    if state % 5 == 4: #cannot move east
        operators.remove(2)
    if state % 5 == 0: #cannot move west
        operators.remove(3)
    
    return operators
    
def nextMove(state, thisOp, q, pol):
    global qTable, alpha, gamma, bank, opCount, bankArray
    '''pick the next move for the algorithm and does the Q-table calculations
    Q-Table actions: 0=North 1=South 2=East 3=West 4=PickUp 5=Drop'''
    #calculate the new state when operator applied
    r=-1
    newState = int()
    if thisOp == 0: #north
        newState = state-5
    if thisOp == 1: #south
        newState = state+5
    if thisOp == 2: #east
        newState = state+1
    if thisOp == 3: #west
        newState = state-1
    if thisOp == 4: #pickup
        newState = state+25
        r=13
    if thisOp == 5: #dropoff
        newState = state-25
        r=13
        
    #next operator based on new state 
    if pickUp(newState): #pick up if pick-up available op=4
        op = 4
    elif dropOff(newState): #drop if drop off available op=5
        op = 5
    #if pick up or drop off not available next State
    else:
        operators = direction(newState)

        
        if pol=="PRANDOM": #pick operator at random
            op = random.choice(operators)
            
        if pol=="PEXPLOIT": #80% optimal, 20% explore
            m = max(qTable[newState,operators])
            MaxOps = [i for i, j in enumerate(qTable[newState,0:4]) if j == m] #all maximum operator indexes
            MaxOps = intersection(operators, MaxOps)
            maximum = random.choice(MaxOps) #pick a maximum operator (index) at random
            if random.choices(['optimal','explore'], weights=(80,20)) == ['optimal']:
                op = maximum #index of operator (N,S,E,W) 80% chance of picking this
            else:
                operators.remove(maximum) #remove max from being an option, 20% chance of picking one of these
                op = random.choice(operators) 
                
        if pol=="PGREEDY": #pick the best q-value 
            m = max(qTable[newState,operators])
            MaxOps = [i for i, j in enumerate(qTable[newState,0:4]) if j == m] #all maximum operator indexes
            MaxOps = intersection(operators, MaxOps)
            maximum = random.choice(MaxOps) #pick a maximum operator (index) at random
            op = maximum #index of operator (N,S,E,W)


    #calculate Q-value 
    opCount += 1
    bank += r
    bankArray.append(bank)
    
    if (q == "Q-Learning"):
        qTable[state,thisOp] = (1-alpha)*qTable[state,thisOp] + alpha*(r + gamma*qTable[newState,op])
    elif (q == "SARSA"):
        qTable[state,thisOp] = qTable[state,thisOp] + alpha*(r + gamma*qTable[newState,op] - qTable[state, thisOp])
    return newState, op


def getDir(op):
    if op == 0:
        return "North"
    elif op == 1:
        return "South"
    elif op == 2:
        return "East"
    elif op == 3:
        return "West"
    elif op == 4:
        return "Pickup"
    elif op == 5:
        return "Dropoff"
    else: 
        return "None"
    
def printThis():
    global thisOp, state, steps, opCount
    '''Print statements for chekcing'''
    if thisOp == 5:
        print("Dropoff at state: ", state, "Operations in this run:", opCount)
    if thisOp == 4:
        print("Pickup at state: ", state, "Operations in this run:", opCount)
    '''
    print("Steps: ", steps)
    print("State : ", state,"Previous Action: ", getDir(thisOp))
    print("\n")
    '''

# In[2]:
'''     Start Tests        '''
for seed in range (1,3):
    random.seed(seed)
    
    # <h2>1.</h2>

    # In Experiment 1 you use α=0.3 and   γ=0.5, and run the traditional Q-learning algorithm for 6000 steps; 
    # 
    # initially you run the policy PRANDOM for 500 steps, then
    # 
    #     a.Continue running PRANDOM for 5500 more steps

    
    #Experiment 1a
    startTest(0.3,0.5)
    
    while steps <= 6000:
        printThis()
        state, thisOp = nextMove(state, thisOp, "Q-Learning","PRANDOM")
        
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
            
    
    # In[3]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("1a")

    # In[4]:
    
    # In Experiment 1 you use α=0.3 and   γ=0.5, and run the traditional Q-learning algorithm for 6000 steps; 
    # 
    # initially you run the policy PRANDOM for 500 steps, then
    # 
    #     b. Run PGREEDY for the remaining 5500 steps
    
    # In[7]:
    
    # Experiment 1b  
    startTest(0.3,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, then Run PGREEDY for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PGREEDY"
        state, thisOp = nextMove(state, thisOp, "Q-Learning", algo)

        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
    
    
    # In[8]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("1b")
    
    # In[10]:
    
    
    # In Experiment 1 you use α=0.3 and   γ=0.5, and run the traditional Q-learning algorithm for 6000 steps; 
    # 
    # initially you run the policy PRANDOM for 500 steps, then
    #    
    #     c. Run PEXPLOIT for the remaining 5500 steps
    
    # In[11]:
    
    # Experiment 1c
    startTest(0.3,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, Run PEXPLOIT for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PEXPLOIT"
        state, thisOp = nextMove(state, thisOp, "Q-Learning", algo)
            
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
    
    
    # In[12]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("1c")
    
    
    # In[13]:
    
    
    # <h2>2.</h2>
    
    # Experiment 2 is the same as experiment 1.c except you run the SARSA q-learning variation for 6000 steps. 
    
    # In[14]:
    
    # Experiment 2  
    startTest(0.3,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, then Run PGREEDY for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PEXPLOIT"
        state, thisOp = nextMove(state, thisOp, "SARSA", algo)
        
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
            
    
    # In[15]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("2")
    
    
    # In[16]:
    
    # <h2>3.</h2>
    
    # In Experiment 3 you rerun Experiment 1.c but with learning rates α=0.15 
    
    # In[19]:
    
    #Experiment 3a
    startTest(0.15,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, then Run PGREEDY for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PEXPLOIT"
        state, thisOp = nextMove(state, thisOp, "Q-Learning", algo)
        
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
    
    
    # In[20]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("3a")
    
    # In[21]:
    
    
    # In Experiment 3 you rerun Experiment 1.c but with learning rates α=0.45 
    
    # In[23]:
    
    
    # Experiment 3  part 2;  Experiment 1.c with learning rates α=0.45 
    startTest(0.45,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, then Run PGREEDY for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PEXPLOIT"
        state, thisOp = nextMove(state, thisOp, "Q-Learning", algo)
            
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
        steps+=1
    
    
    # In[24]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("3b")
    
    # In[25]:
    
    
    
    # <h2>4.</h2>
    
    # Experiment 4 is the somewhat similar to Experiment 1c you use α=0.3 and γ=0.5 in conjunction with Q-learning
    # 
    # you run PRANDOM for the first 500 steps; next, you run PEXPLOIT;
    # 
    # however, after the agent reaches a terminal state the third time, change the pickup locations to (3,1) and (1,3); 
    # 
    # the drop off locations and the Q-table remain unchanged; finally, you continue running PEXPLOIT 
    # 
    # with the “new” pickup locations until the agent reaches a terminal state the sixth time. 
    
    # In[27]:
    
    
    # Experiment 4  you use α=0.3 and γ=0.5 in conjunction with either Q-learning
    startTest(0.3,0.5)
    
    while steps < 6000:
        printThis()
        #  initially you run the policy PRANDOM for 500 steps, then Run PGREEDY for the remaining 5500 steps
        algo = "PRANDOM" if steps < 500 else "PEXPLOIT"
        state, thisOp = nextMove(state, thisOp, "Q-Learning", algo)
        
        i,j,x,a,b,c,d,e,f = stateSpace(state)
        '''reset values if final conditions have been met'''
        if [x,a,b,c,d,e,f] == [0,0,0,4,4,4,4]:
            reset()
            # after the agent reaches a terminal state the third time, change the pickup locations to (3,1) and (1,3);
            if len(terms) == 3:
                p = [coordnatesToSpace(3,1), coordnatesToSpace(1,3)]
                
            # until the agent reaches a terminal state the sixth time, then I guess revert to "old" pickup locations
            if len(terms) == 6:
                p = [coordnatesToSpace(3,5), coordnatesToSpace(4,2)]
        steps+=1
    
    
    # In[28]:
    
    '''Ouput q-Table and bankArray to csv'''
    plot("4")
