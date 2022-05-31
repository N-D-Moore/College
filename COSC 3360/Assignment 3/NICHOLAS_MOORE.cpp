#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string.h> 
#include <vector> 
#include <sstream> 
#include <unistd.h>
#include <stdlib.h>
#include <list>
#include <ctype.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/mman.h>
#include <math.h>

using namespace std;

list<string> mylist;

struct Information {
	int tp; //total number of page frames in main memory
	int sl; //log2(sl) gives size of seg and page id
	int ps; //log2(ps) gives size of displacment
	int r; //page frames used in algo
	int x; //used for LRU-x and OPT-X
	int min; //min free pool size
	int max; //max free pool size
	int k; //number of processes
};

struct Processes {
	string full;
	string pid;
	string segid;
	string indid;
	string displacment;
	string end;
	int len;
};

int readFile(int agrc, char *agrv[]) {
	
	string fileName = agrv[1], read;
	ifstream inputFile;
	inputFile.open(fileName);
	while (getline(inputFile, read)){
		mylist.push_back(read);
	}
	inputFile.close();
	return 0;
	
}

Information* GetInformation(){
	struct Information* temp;
	temp = new Information;
	int position = 0;
	for (auto const &v : mylist){
		switch (position) {
			case 0:
				temp->tp = stoi(v);
				position++;
				break;
			case 1:
				temp->sl = stoi(v);
				position++;
				break;
			case 2:
				temp->ps = stoi(v);
				position++;
				break;
			case 3:
				temp->r = stoi(v);
				position++;
				break;
			case 4:
				temp->x = stoi(v);
				position++;
				break;
			case 5:
				temp->min = stoi(v);
				position++;
				break;
			case 6:
				temp->max = stoi(v);
				position++;
				break;
			case 7:
				temp->k = stoi(v);
				position++;
				break;
		}
	}
	return temp;
}

Processes* GetProcesses(int k, int l) {
	int length = 0; 
	int a = 0, b = 0;
	//get the length of the process queue
	for (auto const &v : mylist){
		if (a < k+8)
			a++;
		else
			length++;
	}
	a = 0;
	struct Processes* temp;
	temp = new Processes[length];
	temp[0].len = length;
	for (auto const &v : mylist){
		if (a >= k+8) {
			temp[b].full = v;
			b++;
		}
		else
			a++;
	}
	
	string delimiter = " ";
	size_t pos = 0;
	string token, token0, token2;
	for (int i = 0; i < length; i++){
		token0 = temp[i].full;
		while ((pos = token0.find(delimiter)) != string::npos) {
			//parse out pid
			token = token0.substr(0, pos);
			temp[i].pid = token;
			token0.erase(0, pos + delimiter.length());
		}
		//string without pid
		string token3 = token3+token0[0]+token0[1];
		if (token3 == "-1"){
			temp[i].end = token0;
		}
		else{
			//pase out segid and indexid
			for (int z = 0; z < l; z++) {
				token2 = token2 + token0[z];
			}
			temp[i].segid = token2;
			token2.erase();
			for (int z = l; z < l*2; z++) {
				token2 = token2 + token0[z];
			}
			temp[i].indid = token2;
			token2.erase();
			//parse out delimiter
			int z = l*2;
			while (token0[z]!='B'){
				token2 = token2 + token0[z];
				z++;
			}
			temp[i].displacment = token2;
			token2.erase();
		}
	}
	
	return temp;
}

/*bool GetExist(int a, int b, int c, string Pages[a][b][c], int segid, int d) {
	//for (int i = 0; i <
	
	return false;
}*/

int main(int agrc, char *agrv[]) {
	readFile(agrc, agrv);
	
	struct Information *information;
	information = GetInformation();
	struct Processes *processes;
	processes = GetProcesses(information->k, log2(information->sl));	
	
	//Mian Memory - check table and if pagefault call pagefault
	//Fault Handler - convert logical to phyiscal address call disk manager for data
	//Disk Manager - give data for physical address
	
	//need shared memory to give process position, for if it faulted (store fault amount in MM), shared memory to give physical address.
	//need 3 semaphores for the operation of 3 processes
	
	//need a vector that contains the pid, process#, seg length
	//create vecotr of info[#of process][pid,process,seg length]
	vector<vector<string>> info(information->k);
	for (int i = 0; i < information->k; i++){
		//generate pid (pid = 100+process) (process = i+1)
		info[i].push_back(to_string(100+1+i));
		info[i].push_back(to_string(1+i));
		//get how many segments there are
		int Seglen = 0; 
		int SegBool = 0;
		vector<string> tempSeg;
		//iterate through all process
		for (int j = 0; j < processes[0].len; j++){
			//make sure its not exit and it matches the pid
			if (processes[j].segid != "" && processes[j].pid == to_string(100+1+i)){
				//iterate through the vector to see if it exists already
				for (int k = 0; k < tempSeg.size(); k++){
					if (processes[j].segid == tempSeg[k]){
						SegBool = 1;
					}
				}
				if (SegBool == 0){
					//iterate length and add to vecotr
					Seglen++;
					tempSeg.push_back(processes[j].segid);
				}
				else //reset SegBool and don't itterate length
					SegBool = 0;
			}
		}
		info[i].push_back(to_string(Seglen));
		tempSeg.clear();
	}
	
	long key = 1390458;
	int nbytes = 4096; //I am not messing with this unless this code doesn't work properly
	
	//create vector of semaphores
	vector<int> vecSid;
	int sid;
	for (int i = 0; i < 3; i++){
		key = key + i;
		sid = semget(key, 1, 0666 | IPC_CREAT);
		vecSid.push_back(sid);
	}
	//reset key
	key = 1390458;
	
	int shmid0, shmid1, shmid2, shmid3;
	char *pmem0, *pmem1, *pmem2, *pmem3;
	shmid0 = shmget(key-1, nbytes, 0666 | IPC_CREAT);
	shmid1 = shmget(key-2, nbytes, 0666 | IPC_CREAT);
	shmid2 = shmget(key-3, nbytes, 0666 | IPC_CREAT);
	shmid3 = shmget(key-4, nbytes, 0666 | IPC_CREAT);
	pmem0 = (char *)shmat(shmid0, 0, 0);
	if (pmem0 == (char *)(-1))
		perror("Shared memory pmem0 failed");
	pmem1 = (char *)shmat(shmid0, 0, 0);
	if (pmem1 == (char *)(-1))
		perror("Shared memory pmem1 failed");
	pmem2 = (char *)shmat(shmid0, 0, 0);
	if (pmem2 == (char *)(-1))
		perror("Shared memory pmem2 failed");
	pmem3 = (char *)shmat(shmid0, 0, 0);
	if (pmem3 == (char *)(-1))
		perror("Shared memory pmem3 failed");
	
	struct sembuf sbUP;
	sbUP.sem_num = 0;
	sbUP.sem_op = 1;
	sbUP.sem_flg = 0;
	//semop(sid, &sbUP, 1);
	
	struct sembuf sbDOWN;
	sbDOWN.sem_num = 0;
	sbDOWN.sem_op = -1;
	sbDOWN.sem_flg = 0;
	//semop(sid, &sbDOWN, 1);
	
	for (int i = 0; i < 3; i++){
		if(fork() == 0){
			//cout << "hello " << i << endl;
			if (i == 0){
				//main memory
				//create table to track number of page faults
				int pageFaults[information->k];
				for (int j = 0; j < information->k; j++){
					pageFaults[j] = 0;
				}
				int numSeg = 0;
				for (int j = 0; j < stoi(info[j][2]); j++){
					if (numSeg < stoi(info[j][2]))
						numSeg = stoi(info[j][2]);
				}
				//Create 3d table for algos [pid][seg][page] (seg is largest possible seg size) page 0 is segid
				string Pages[information->k][numSeg][(information->r)+1];
				//FIFO
				int fifoPos = 1;
				for (int j = 0; j < processes[0].len; j++){
					//cout << "Loop# " << j << " should last till " << processes[0].len << endl;
					
					//get process#
					int a;
					for (int k = 0; k < information->k; k++){
						if (info[k][0] == processes[j].pid){
							a = stoi(info[k][1]);
							break;
						}
					}
					//checck for matches in Pages table to populate segids
					bool match = false;
					for (int k = 0; k < numSeg; k++){
						if (Pages[a-1][k][0] == processes[j].segid && processes[j].end == ""){
							match = true;
							break;
						}
						if (processes[j].end != ""){
							match = true;
							break;
						}
					}
					//if segid not matched add to table
					if(match != true){
						for (int k = 0; k < numSeg; k++){ 
							if (Pages[a-1][k][0] != processes[j].segid && Pages[a-1][k][0] == ""){
								//add segid and indid
								Pages[a-1][k][0] = processes[j].segid;
								Pages[a-1][k][1] = processes[j].indid;
								break;
							}
						}
						//update pagefault counter
						pageFaults[a-1] = pageFaults[a-1]+1;
						//semop(vecSid[1], &sbUP, 1);
						//semop(vecSid[0], &sbDOWN, 1);
						//cout << "process " << a << " has now " << pageFaults[a-1] << " page faults" << endl;
					}
					else{
						for (int k = 0; k < numSeg; k++){ 
							if (Pages[a-1][k][0] == processes[j].segid){
								for (int l = 1; l < (information->r)+1; l++){
									if (Pages[a-1][k][l] == processes[j].indid){
										break; //break to catch if it is already in list
									}
									if (Pages[a-1][k][l] != processes[j].indid && Pages[a-1][k][l] == ""){
										//if the index id isn't in list add it and pagefault
										Pages[a-1][k][l] = processes[j].indid;
										pageFaults[a-1] = pageFaults[a-1]+1;
										//cout << "process " << a << " has now " << pageFaults[a-1] << " page faults" << endl;
										break;
									}
									//if table is full and no matches replace and page fault
									if (l == information->r && Pages[a-1][k][l] != ""){
										Pages[a-1][k][fifoPos] = processes[j].indid;
										pageFaults[a-1] = pageFaults[a-1]+1;
										fifoPos++;
										if (fifoPos == information->r)
											fifoPos = 1;
										break;
									}
								}
							}
						}
						// << "do nothing" << endl;
					}
				}
				cout << "Number of page faults for each process: FIFO" << endl;
				for (int k = 0; k < information->k; k++){
					cout << "Process " << info[k][0] << ": " << pageFaults[k] << ";" << endl;
				}
				strncpy(pmem0, "Shared memory works", nbytes);
			}
			if (i == 1){
				//if (semop(vecSid[1], &sbDOWN, 1) == -1);
					//cout << "failed" << endl;
				//semop(vecSid[2], &sbUP, 1);
				//fault handler
				//cout << pmem0 << endl;
				strncpy(pmem0, "Shared memory works2", nbytes);
			}
			if (i == 2){
				//semop(vecSid[2], &sbDOWN, 1);
				//semop(vecSid[0], &sbUP, 1);
				//disk manager
				//create conversion table for logical to physical. Doesn't asctually convert or give anything in this program since its not really needed
				vector<vector<string>> Conversion(information->k);
				//cout << pmem0 << endl;
			}
			exit(0);
		}
	}
	
	//destroy shared memory
	for (int i = 0; i < 3; i++){
		semctl(vecSid[i], 0, IPC_RMID, 0);
	}
	
	
	shmdt(pmem0);
	shmdt(pmem1);
	shmdt(pmem2);
	shmdt(pmem3);
	semctl(shmid0, 0, IPC_RMID, 0);
	semctl(shmid1, 0, IPC_RMID, 0);
	semctl(shmid2, 0, IPC_RMID, 0);
	semctl(shmid3, 0, IPC_RMID, 0);
	
	return 0;
}