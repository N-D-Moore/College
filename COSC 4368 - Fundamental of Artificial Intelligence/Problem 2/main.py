#f(x,y) = [1 + (x + y +1)2(19 - 14x + 3x2 -14y + 6xy +3y2)][30 + (2x - 3y)2(18 -32x + 12x2 + 4y - 36xy + 27y2)], where -2 ≤ x,y ≤ 2\
import random

def function(x,y):
    return (1+((x+y+1)**2)*(19-14*x+(3*x**2)-14*y+6*x*y+(3*y**2)))*(30+((2*x-3*y)**2)*(18-32*x+(12*x**2)+4*y-36*x*y+(27*y**2)))

def RHC(sp, p, z, seed):
    random.seed(seed)

    solution_count = 1
    solution_prev = function(sp[0],sp[1])
    solution = solution_prev
    solution_cords = sp
    neighborhood = []

    for x in range (0, p):
        neighborhood.append((sp[0]+random.uniform(-z,z),sp[1]+random.uniform(-z,z)))

    for x in neighborhood:
        solution_count = solution_count+1
        if solution > function(x[0],x[1]):
            solution = function(x[0],x[1])
            solution_cords = x


    del neighborhood[:]

    while solution < solution_prev:
        solution_prev = solution
        for x in range (0, p):
            neighborhood.append((solution_cords[0]+random.uniform(-z,z),solution_cords[1]+random.uniform(-z,z)))

        for x in neighborhood:
            solution_count = solution_count+1
            if solution > function(x[0],x[1]):
                solution = function(x[0],x[1])
                solution_cords = x

        del neighborhood[:]

    print(sp, p, z, seed)
    print("Solution:", solution)
    print("Solution Cords:", solution_cords)
    print("Solution Count:",solution_count)
    print("")

RHC((0.4,-0.5), 30, 0.003, "help")
RHC((0.4,-0.5), 30, 0.003, "saveme")
RHC((0.4,-0.5), 30, 0.003, "help")
RHC((0.4,-0.5), 30, 0.003, "saveme")
RHC((0.4,-0.5), 30, 0.003, "help")
RHC((0.4,-0.5), 30, 0.003, "saveme")
RHC((0.4,-0.5), 30, 0.003, "help")
RHC((0.4,-0.5), 30, 0.003, "saveme")
