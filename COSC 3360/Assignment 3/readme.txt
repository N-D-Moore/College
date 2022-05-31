Hello grader,

I have 2 remaining grace days so just apply both of them to this grade or apply them to assignment 2 it should equal out to be the same?

In this code i only have it running one algorithm FIFO. When trying to implament the semaphores to run the 3 processes to emulate 
Main Memory, Disk Manager, and Page Fault Handler I have run into a bug i can not figure out. Considering the code is already a day late
and its the end of the semester i am submitting it as is. The specific bug from what i can tell are my semops. The shared memory is generated
properly and so are the semaphores however when i call semop the semop itself fails. I believed this maybe be do to me haveing both sbUP and
sbDOWN in the code so i reduced it to just sb and had it only running down to try and get the program to stall waiting for no up signals and it
still failed. I am not sure if it is my laptop or something in the code that won't allow me to run semop. In another file just doing semaphores 
how i have it works but in my HW3 code the semop fails. I can not find any documentation on how semop would fail beyond the fact that it can.
It might take me several days to try and find the root cause of this issue (even before i try forking semop fails so i doubt its that). I have
spent too much time reading up on trying to fix this as it is and honestly exhausted from this semester (online learning is not easy for me).

Now i know its supposed to run all 6 different algos but since i didn't implament all of them i am going to instead talk about how i was going to
implament them here in the readme. For LRU i was going to use entry 1 was last used and move all data in the table up by 1 and replace the last 
entry (last entry would be most recently used). LRU-X was just going to do the same except whatever was value X would replace 1 in the before 
mentioned. For MFU i was going to create a table to keep track of how many times the pageid had been use and replace the one with most values.
At the same time i would have the same algo for LRU in place so that if the values ended up being the same i would just pick LRU instead for 
the highest value. For OPT i was just gonna have a table that held all the pageids for the specific segid i was looking at X moves a head and replace
the lowest occurance value that is in the current table. WS not sure how to best describe other than constantly shifting entrys up by one and replaceing
the last entry and if the newly added pageid was not currently in the table page fault.

I do apologize for this long readme and hope that you have a wonderful winter break.



to complie and generate the code

g++ -std=c++11 NICHOLAS_MOORE.cpp -o test
./test sample.txt