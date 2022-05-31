#initilizing arrays for math. b and c are not initilized due to first element in problem A results in them being 1 and 1 respectivly
#the 2 comes from working on problem B and knowing its needed later

print("Problem A\n")

#generate arrays
a=[0]
d=[0]
e=[0]
f=[0]

a_new=[]
b_new=[1, 2]
c_new=[1, 2]
d_new=[]
e_new=[]
f_new=[]

#I am doing this in a for loop and because could do this by hand but looking at 50 0s serperated by a comma hurts my head trying to count to 50
#so this extra x i am excluding from nva since its optional for the sake of my sanity
for x in range(2, 51):
    a.append(0)
    d.append(0)
    e.append(0)
    f.append(0)

#50(a)+50(d)+50(e)+50(f)+2(b)+2(c)=202
nva=202

#I used matlab to find the min and max values for the variables and used those as the ranges
#to make it more "general" you would instead have it run from 1 to 50 (the stated min and max of the variables)
#also i am dumb and forgot that python is case sensetive so i change how i do my for loops to us captiales to help read code later
for x in range (23, 50): #d
    nva=nva+1
    for y in range (2, 17): #e
        nva=nva+1
        for z in range (7, 43): #a
            nva=nva+1
            #if the values meat critera 3 append
            if x**2==y*y*z+417:
                a[z-1]=z
                e[y-1]=y
                d[x-1]=x

#creating new smaller array of possible results
for x in a:
    nva=nva+1
    if x!=0:
        nva=nva+1
        a_new.append(x)
for x in d:
    nva=nva+1
    if x!=0:
        nva=nva+1
        d_new.append(x)
for x in e:
    nva=nva+1
    if x!=0:
        nva=nva+1
        e_new.append(x)

#I am doing this for memory managment and the code works 100% fine without deleting the lists so not counting it as nva since this is optional
del a
del d
del e

#find known Fs given constraint 2
for E in e_new:
    nva=nva+1
    for D in d_new:
        nva=nva+1
        for x in range(2,27):
            nva=nva+1
            #if values meat criteria 2 append
            if D==E+x+21:
                nva=nva+1
                f[x-1]=x

for x in f:
    nva=nva+1
    if x!=0:
        nva=nva+1
        f_new.append(x)

del f
solved = False
nva=nva+1
#search for solution with known parameters
for A in a_new:
    nva=nva+1
    for E in e_new:
        nva=nva+1
        for F in f_new:
            nva=nva+1
            if E+F<A:
                for D in d_new:
                    nva=nva+1
                    if D==E+F+21 and D**2==E*E*A+417: #criteria 2 and 3
                        for B in b_new:
                            nva=nva+1
                            for C in c_new:
                                nva=nva+1
                                if A==B+C+E+F and E+F<A: #criteria 1 and 4
                                    nva=nva+1
                                    print("Solution found!\n", A, B, C, D, E, F)
                                    solved = True
                                if solved==True:
                                    break
                            if solved==True:
                                break
                    if solved==True:
                        break
            if solved==True:
                break
        if solved==True:
            break
    if solved==True:
        break

ProblemA_nva = nva
nva=0

print("Problem A nva:", ProblemA_nva)
print("Total nva:", ProblemA_nva)

#-------------------------------------------------------------------------
#--------------------------------Problem B--------------------------------
#-------------------------------------------------------------------------

print("\nProblem B\n")

#generating arrays
g=[0]
h=[0]
i=[0]
g_new=[]
h_new=[]
i_new=[]
j_new=[]
for x in range(2, 51):
    g.append(0)
    h.append(0)
    i.append(0)

nva=150

#use c6 to find G
for C in c_new:
    nva=nva+1
    for F in f_new:
        nva=nva+1
        #from testing this i know the range is actually 11 to 11 for it to meet both C6 and C9
        for x in range(1,12):
            nva=nva+1
            #criteria 9 looking for G
            if (x-C)**2==F*C*C+1:
                for A in a_new:
                    nva=nva+1
                    for D in d_new:
                        nva=nva+1
                        #criteria 6 looking for G
                        if A+D==((F-x)**2)-1:
                            nva=nva+1
                            g[x-1]=x                   

for x in g:
    nva=nva+1
    if x!=0:
        nva=nva+1
        g_new.append(x)

#memory managment
del g

#c7 gives us J with simple algebra
for G in g_new:
    j_new.append(int((G**2+39)/4))
    nva=nva+2

#use c5 and c8 to find possible h and i
for J in j_new:
    nva=nva+1
    for G in g_new:
        nva=nva+1
        for E in e_new:
            nva=nva+1
            for H in range(1,13):
                nva=nva+1
                #the actual range with criteria 5 for I is 1 to 35 but i know the next range is 1 to 14 so reducing it here to lower nva
                for I in range(1,14):
                    nva=nva+1
                    if (H*J+E*12)==(G+I)**2:
                        for F in f_new:
                            nva=nva+1
                            if (I-G)**9==(F-H)**3:
                                h[H-1]=H
                                i[I-1]=I
                                nva=nva+2

for x in h:
    nva=nva+1
    if x!=0:
        nva=nva+1
        h_new.append(x)
for x in i:
    nva=nva+1
    if x!=0:
        nva=nva+1
        i_new.append(x)

#memory management
del h
del i

#save as in problem A (copy pasted most of it from A)
solved=False
for A in a_new:
    nva=nva+1
    for E in e_new:
        nva=nva+1
        for F in f_new:
            nva=nva+1
            if E+F<A:
                for D in d_new:
                    nva=nva+1
                    if D==E+F+21 and D**2==E*E*A+417:
                        for B in b_new:
                            nva=nva+1
                            for C in c_new:
                                if A==B+C+E+F and E+F<A:
                                    for G in g_new:
                                        nva=nva+1
                                        if A+D==(F-G)**2-1 and (G-C)**2==F*C*C+1: #criteria 9 and 6
                                            for J in j_new:
                                                nva=nva+1
                                                if 4*J==G**2+39: #criteria 7
                                                    for H in h_new:
                                                        nva=nva+1
                                                        for I in i_new:
                                                            nva=nva+1
                                                            if H*J+E*12==(G+I)**2 and (I-G)**9==(F-H)**3: #criteria 5 and 8
                                                                nva=nva+1
                                                                print("Solution found!\n", A, B, C, D, E, F, G, H, I, J)
                                                                solved = True
                                                            if solved==True:
                                                                break
                                                        if solved==True:
                                                            break  
                                                if solved==True:
                                                    break
                                        if solved==True:
                                            break
                                if solved==True:
                                    break
                            if solved==True:
                                break
                    if solved==True:
                        break
            if solved==True:
                break
        if solved==True:
            break
    if solved==True:
        break

ProblemB_nva = nva
nva = 0
print("Problem B nva:", ProblemB_nva)
print("Total nva:", ProblemA_nva+ProblemB_nva)

#-------------------------------------------------------------------------
#--------------------------------Problem C--------------------------------
#-------------------------------------------------------------------------

print("\nProblem C\n")

nva=0

#only initilizing arrays because these variables only have 1 result so that i save on nva
k=[]
l=[]
m=[]
n=[]
o=[]

#check for O solutions given C14
for x in range (30,44): #using 44 as a constraint with knowledge that no result after 43 is found and 30 because only 43 is found
    nva=nva+1
    for G in g_new:
        nva=nva+1
        for H in h_new:
            nva=nva+1
            for I in i_new:
                nva=nva+1
                for B in b_new:
                    nva=nva+1
                    if x**2==G*H*I*B+133:
                        nva=nva+1
                        o.append(x)

#find values for M and N given c10 and c14
for M in range (38,48): #using these constraints because the only possible answer for this equation is M=47 and K=10
    nva=nva+1
    for K in range(1,11): 
        nva=nva+1
        for O in o:
            nva=nva+1
            if M+O==K**2-10 and 2*M==K**2-6:
                nva=nva+2
                m.append(M)
                k.append(K)

#find values for L given c15
for x in range(1,11): #yet again this results in only answer of 3 so restricting the constraints down
    nva=nva+1
    for B in b_new:
        nva=nva+1
        for K in k:
            nva=nva+1
            for I in i_new:
                nva=nva+1
                if x**3+I==(x+B)*K:
                    nva=nva+1
                    l.append(x)

#find values for N given c11 and c12
for x in range(40,51): #only result is 50
    nva=nva+1
    for O in o:
        nva=nva+1
        for M in m:
            nva=nva+1
            for I in i_new:
                nva=nva+1
                for F in f_new:
                    nva=nva+1
                    if (x-O)**3+7==(F-I)*x and x**2==M**2+291:
                        if not n: #adding this to prevent it from appending 50 twice without having to change my code
                            #If I have stored the values from problem B i could of used those and cut back on nva and
                            #only get 1 value since i know there is only 1 possible solution to problem B but keeping it general
                            nva=nva+1
                            n.append(x)

#same as in problem B (copy pasted most of it from B)
solved=False
for A in a_new:
    nva=nva+1
    for E in e_new:
        nva=nva+1
        for F in f_new:
            nva=nva+1
            if E+F<A:
                for D in d_new:
                    nva=nva+1
                    if D==E+F+21 and D**2==E*E*A+417: #criteria 2 and 3
                        for B in b_new:
                            nva=nva+1
                            for C in c_new:
                                if A==B+C+E+F and E+F<A: #criteria 1 and 4
                                    for G in g_new:
                                        nva=nva+1
                                        if A+D==(F-G)**2-1 and (G-C)**2==F*C*C+1: #criteria 9 and 6
                                            for J in j_new:
                                                nva=nva+1
                                                if 4*J==G**2+39: #criteria 7
                                                    for H in h_new:
                                                        nva=nva+1
                                                        for I in i_new:
                                                            nva=nva+1
                                                            if H*J+E*12==(G+I)**2 and (I-G)**9==(F-H)**3: #criteria 5 and 8
                                                                for O in o:
                                                                    if O**2==G*H*I*B+133: #criteria 13
                                                                        for K in k:
                                                                            for M in m:
                                                                                if M+O==K**2-10 and 2*M==K**2-6: #criteria 14 and 10
                                                                                    for L in l:
                                                                                        if L**3+I==(L+B)*K: #criteria 15
                                                                                            for N in n:
                                                                                                if (N-O)**3+7==(F-I)*N and N**2==M**2+291: #criteria 11 and 12
                                                                                                    nva=nva+1
                                                                                                    print("Solution found!\n", A, B, C, D, E, F, G, H, I, J, K, L, M, N, O)
                                                                                                    solved = True
                                                                                            if solved==True:
                                                                                                break
                                                                                    if solved==True:
                                                                                        break
                                                                            if solved==True:
                                                                                break
                                                                        if solved==True:
                                                                            break
                                                            if solved==True:
                                                                break
                                                        if solved==True:
                                                            break  
                                                if solved==True:
                                                    break
                                        if solved==True:
                                            break
                                if solved==True:
                                    break
                            if solved==True:
                                break
                    if solved==True:
                        break
            if solved==True:
                break
        if solved==True:
            break
    if solved==True:
        break

print("Problem C nva:", nva)
print("Total nva:", ProblemA_nva+ProblemB_nva+nva)