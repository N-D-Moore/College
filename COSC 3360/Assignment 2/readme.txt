Hello grader please read through all of this readme. It contains reasons on why i commented out my code and why it "works" and is missing a few things.
The code also still contains all of the cout lines that i was using for debugging purposes. 

If you just execute the given code it will output my generated list of the different execution orders which were meant to be used
with the semaphores to cordinate the individual processes.

As this code currently stands it is missing a dealocator and destructor for my shared memory. This doesn't much matter since 
my code won't fully exect anyway. I have spent the last week spending about 15+ hours a day trying to debug this code and 
get it working and i keep finding more and more issues as i went. This is the very first none operational code i have ever
submitted. I was able to get the semaphores to properly activate and let the different processes run when they are supposed to.
I even got the input files parsed out into a manor i wished it to be so that i could use them. Then i was able to get the program
to parse and go through the opperations and update the flights to reflect the proper order. I then implamented the flight array into
shared memory. I later learned that this was just not possible at least not with how i was doing it since only the first dimension
of the 2 dimensional array was actually in the shared memory. I have also learned that shared memory is static so these dynamic arrays
won't work anyway. So i switched my shared memory to a struct and tested it and thought it was working properly. Then executing the code
ignoring semaphores and one at a time with wait(NULL) the code was to execute properly. Once I allowed both processes to run I encounted 
an issue with Stringstream causing whatever string it was reading when another process activates to lose about 8-12 characters worth of 
the string. I changed this to work without string stream and it worked and the code was able to run again. However i noticed another issue
with my struct of shared memory not sharing strings and this cause some of my logic to break. Removing this to instead be an int appears
to have worked and it runs.

However it now just exits out of the program without throwing an error and i can only assume it is due to exceding memory in some way.
My next idea on fixing the code i realized would remove shared memory completly from the program outside of semaphores. I feel as if this
contradicts the intended shared memory portion of this assignment so did not attempt to implament this idea. I have now given
up on trying to fix this code before i submit it. I have to work on other class work and study for the up coming exam that i haven't even
been able to study for yet due to working on this assignment and i feel as if working on this assignment will not get me more points
than i will lose from the exam and the increased -5 points per day i don't get it in.

Remove the start block comments on lines 671 and 383 if you wish to see the output of the rest of the code.

to complie and generate the code

g++ -std=c++11 NICHOLAS_MOORE.cpp -o test
./test sample.txt