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

using namespace std;

list<string> mylist;

struct CurentOp{
	string FullOp;
	int CurentAgent;
	string Opperation;
	string Plane;
	string Seat;
	string Person;
	int Deadline;
	int NextAgent;
	string nextFullOp;
	//1 cancel SA113 2A Tom deadline 15
};

struct Airplanes {
	string name;
	int rows;
	int seats;
	string **seat;
};

struct Agents{
	int ticket;
	int reserve;
	int wait;
	int waitany;
	int cancel;
	int check_passenger;
	list<string> opperations;
};

//read inputed file and move it to mylist for further break up into other variables
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

//parse out the variables for the airplanes
Airplanes* getAirplanes(){
	//Number of airplanes is the first variabe from txt file
	int flights = stoi(mylist.front());
	int agents = 0;
	struct Airplanes* temp;
	temp = new Airplanes[flights];
	int count = 0;
	//iterating through list
	for (auto const &v : mylist){
		if (agents <= flights) {
			if (agents == 0){
				agents++;
			}
			else {
				//parsing string into vector tokens
				vector <string> tokens; 
				stringstream check1(v); 
				string intermediate;
				while(getline(check1, intermediate, ' ')) 
				{ 
					tokens.push_back(intermediate); 
				} 
				//assign the temp struct with parsed data (if i have time look back to make it so that you don't use vector since i was getting errors before when i didn't)
				temp[count].name = tokens[0];
				temp[count].rows = stoi(tokens[1]);
				temp[count].seats = stoi(tokens[2]);
				count++;
				agents++;
			}
		}
		else 
			break;
	};
	for (int i = 0; i < stoi(mylist.front()); i++){
		temp[i].seat = new string*[temp[i].rows];
		for (int j = 0; j < temp[i].rows; j++){
			temp[i].seat[j] = new string[temp[i].seats];
		}
	}
	return temp;
}

//find the number of agents
int getNumberAgents(){
	int flights = stoi(mylist.front());
	int count = 0;
	int agents;
	for (auto const &v : mylist){
		if (count <= flights) {
			count++;
		}
		else {
			agents = stoi(v);		
			break;
		}
	};
	return agents;
}

//parse out the variabes for the agents
Agents* getAgents(){
	int flights = stoi(mylist.front());
	int count = 0;
	int agents = getNumberAgents();
	struct Agents* temp;
	temp = new Agents[agents];
	int loopCount = 0;
	int agentCount = 0;
	//iterating through list
	for (auto const &v : mylist){
		//First agent starts flight+2 lines into code
		if (count <= flights+2) {			
			count++;
		}
		else {
			//check for "end." to tell when agent finished
			string test1;
			test1 = test1+v[0]+v[1]+v[2]+v[3];
			if (test1 == "end."){
				//decrement count by 1 to avoid agent line after end
				count--;
				//move count to next agent if one agent already added
				if (loopCount > 0){
					agentCount++;
					loopCount = 0;
				}
			}
			else{
				//parsing string into vector tokens
				vector <string> tokens; 
				stringstream check1(v); 
				string intermediate;
				while(getline(check1, intermediate, ' ')) 
				{ 
					tokens.push_back(intermediate); 
				} 
				switch(loopCount) {
					//0=ticket 1=reserve 2=wait 3=waitany 4=cancel 5=check_passenger default=opperations
					case 0:
						temp[agentCount].ticket = stoi(tokens[1]);
						break;
					case 1:
						temp[agentCount].reserve = stoi(tokens[1]);
						break;
					case 2:
						temp[agentCount].wait = stoi(tokens[1]);
						break;
					case 3: 
						temp[agentCount].waitany = stoi(tokens[1]);
						break;
					case 4:
						temp[agentCount].cancel = stoi(tokens[1]);
						break;
					case 5:
						temp[agentCount].check_passenger = stoi(tokens[1]);
						break;
					default:
						temp[agentCount].opperations.push_back(v);
						break;
				}
				loopCount++;
			}
		}
	};
	return temp;
}

int main(int agrc, char *agrv[]) {
	cout << "Program starting" << endl;	
	//read through file and add it to mylist global variable
	readFile(agrc, agrv);
	
	//populate structs with found information
	struct Airplanes *airplanes;
	airplanes = getAirplanes();
	//airplanes = (Airplanes *) shmat(shmid, 0, 0);
	struct Agents* agents;
	agents = getAgents();

	//first in first out
	cout << "Generating FIFO order" << endl;
	list<string> FIFO;
	int count = getNumberAgents();
	int numAgen = count;
	//temp list so as to not delete old lists
	list<string> tempList[count];
	for (int i = 0; i < count; i++){
		tempList[i] = agents[i].opperations;
	}
	//while loop till all agents are empty and for FIFO order add front of agent list (tempList) to FIFO list
	while (count != 0) {
		for( int i = 0; i < numAgen; i++) {
			//agent has been emptied decrement count and add element into list to be ignored
			if (tempList[i].empty() == 1){
				count--;
				tempList[i].push_back("DONE");
			}
			//do nothing since agent has been emptied
			else if (tempList[i].front() == "DONE") {
			}
			//add opperations into tempList and remove them from the agent so they are not added more than once
			else {
				//add a value in front to keep track of which agent is executing therefore which semaphore to allow to go next
				FIFO.push_back(to_string(i) + " " + tempList[i].front());
				tempList[i].pop_front();
			}
		}
	}
	//empty tempList to be repopulated and used for next order
	for (int i = 0; i < numAgen; i++){
		tempList[i].clear();
	}
	for (auto const &v : FIFO){
		cout << v << endl;
	}
	
	//Earliest deadline first
	cout << "Generating EDF order" << endl;
	list<string> EDF;
	count = numAgen;
	//temp list so as to not delete old lists
	list<string> tempList2(FIFO);
	int numOpps = tempList2.size();
	//create an array of strings with the length of EDF from the cloned EDF list (totally number of opperations and EDF already has agent flag in front)
	string tempArray[numOpps];
	for (int i = 0; i < numOpps; i++){
		tempArray[i] = tempList2.front();
		tempList2.pop_front();
	}
	//I just spent 5 hours debugging the fact that there is a null character at the end of these string -_-
	for (int i = 0; i < numOpps; i++){
		if (tempArray[i][tempArray[i].length()] == '\0'){
			tempArray[i] = tempArray[i].erase(tempArray[i].length()-1);
		}
	}
	//While i am at it lets fix the FIFO so that it does not have any null characters
	//I should really move this up to FIFO section but i have spent several days debugging this and it is already 2 days late
	for (int i = 0; i < numOpps; i++){
		FIFO.pop_front();
	}
	for (int i = 0; i < numOpps; i++){
		FIFO.push_back(tempArray[i]);
	}
	//Bubble sort to get ordered by deadline. Going simple instead of fancy even if it is slower to make sure no errors pop up
	string tempString;
	for (int i = 0; i < numOpps; i++){
		for (int j = i+1; j < numOpps; j++){
			size_t last_index = tempArray[i].find_last_not_of("0123456789");
			int tempInt1 = stoi(tempArray[i].substr(last_index + 1));
			last_index = tempArray[j].find_last_not_of("0123456789");
			int tempInt2 = stoi(tempArray[j].substr(last_index + 1));
			if (tempInt2 < tempInt1){
				tempString = tempArray[i];
				tempArray[i] = tempArray[j];
				tempArray[j] = tempString;
			}
		}
	}
	
	for (int i = 0; i < numOpps; i++){
		EDF.push_back(tempArray[i]);
	}
	
	for (auto const &v : EDF){
		cout << v << endl;
	}
	
	//Least laxicity first (deadline - execution)
	cout << "Generating LLF order" << endl;
	list<string> LLF;
	//tempArray is already in EDF now to convert to LLF
	
	int agentI, agentJ, agentILaxity, agentJLaxity;
	string agentII, agentJJ;
	for (int i = 0; i < numOpps; i++){
		stringstream ss;
		for (int j = i+1; j < numOpps; j++){
			//extract first word and change it into int for i agent
			ss << tempArray[i];
			ss >> agentI;
			ss >> agentII;
			if (agentII == "ticket")
				agentILaxity = agents[agentI].ticket;
			else if (agentII == "reserve")
				agentILaxity = agents[agentI].reserve;
			else if (agentII == "wait")
				agentILaxity = agents[agentI].wait;
			else if (agentII == "waitany")
				agentILaxity = agents[agentI].waitany;
			else if (agentII == "cancel")
				agentILaxity = agents[agentI].cancel;
			else if (agentII == "check_passenger")
				agentILaxity = agents[agentI].check_passenger;
			//extract deadline of i
			size_t last_index = tempArray[i].find_last_not_of("0123456789");
			int tempInt1 = stoi(tempArray[i].substr(last_index + 1));
			agentILaxity = tempInt1 - agentILaxity;
			//deadline - execution (execution extracted from agents struct using the found parent agent)
			stringstream ss;
			ss << tempArray[j];
			ss >> agentJ;
			ss >> agentJJ;
			if (agentJJ == "ticket")
				agentJLaxity = agents[agentJ].ticket;
			else if (agentJJ == "reserve")
				agentJLaxity = agents[agentJ].reserve;
			else if (agentJJ == "wait")
				agentJLaxity = agents[agentJ].wait;
			else if (agentJJ == "waitany")
				agentJLaxity = agents[agentJ].waitany;
			else if (agentJJ == "cancel")
				agentJLaxity = agents[agentJ].cancel;
			else if (agentJJ == "check_passenger")
				agentJLaxity = agents[agentJ].check_passenger;
			last_index = tempArray[j].find_last_not_of("0123456789");
			int tempInt2 = stoi(tempArray[j].substr(last_index + 1));
			agentJLaxity = tempInt2 - agentJLaxity;
			//agentJLaxity = getLaxity(agentJJ, agentJ, tempInt1, &agents);
			if (agentJLaxity < agentILaxity){
				tempString = tempArray[i];
				tempArray[i] = tempArray[j];
				tempArray[j] = tempString;
			}
		}
	}
	
	for (int i = 0; i < numOpps; i++){
		LLF.push_back(tempArray[i]);
	}
	
	for (auto const &v : LLF){
		cout << v << endl;
	}
	
	cout << "Executing Opperations in given orders" << endl;
	
	cout << endl << "Please read the readme.txt I have commented out the rest of my code and explained it in there" << endl;
	/*
	//create list to hold those on wait/waitany
	vector<string> waitList;
	//create semaphores
	int sid;
	long key = 139045800890;
	vector<int> vecSid;
	for (int i = 0; i < numAgen; i++){
		key = key + i;
		sid = semget(key, 1, 0666 | IPC_CREAT);
		vecSid.push_back(sid);
	}
	key = 139045800890;
	//create shared memory for tracking current op and execution time
	int shmid, shmid2, shmid3;
	key = key - 1;
	int nbytes;
	shmid = shmget(key, nbytes, 0666 | IPC_CREAT);
	key = key - 1;
	shmid2 = shmget(key, sizeof(CurentOp) * 10, 0666 | IPC_CREAT);
	
	key = 139045800890;
	
	int *pmem;
	string shmString;
	pmem = (int *) shmat(shmid, 0, 0); 
	struct CurentOp *curOpp;
	curOpp = (CurentOp *) shmat(shmid2, 0, 0); 
	
	struct sembuf sb;
	sb.sem_num = 0;
	//increases semaphore by 1 (go speed racer goooo!)
	sb.sem_op = 1;
	sb.sem_flg = 0;

	
	int &timePassed = *pmem;
	timePassed = 0;
	cout << "Running in FIFO order: " << endl;
	curOpp->nextFullOp = FIFO.front();

	//decreases semaphore by 1 (wait)
	stringstream ss;
	string tempStart, tempStart2;
	int startAgent;
	tempStart = FIFO.front();
	ss << tempStart;
	ss >> tempStart2;
	startAgent = stoi(tempStart2);
	semop(vecSid[startAgent], &sb, 1);
	sb.sem_op = -1;
	for (int i = 0; i < numAgen; i++){
		if(fork() == 0){
			cout << "Starting process: " << i << endl;
			if (agents[i].opperations.empty()){
				cout << "test exiting if the list is empty" << endl;
				exit(0);
			}
			//Keep going through loop till all processes for the agent are done
			while (!agents[i].opperations.front().empty()){
				cout << "Process id: " << i << " " << sb.sem_op << endl;
				//sb.sem_op = -1;
				semop(vecSid[i], &sb, 1); 
				//while(FIFO.front() != curOpp->nextFullOp){
				while(startAgent != curOpp->NextAgent){
					cout << endl << "starting inner loop" << endl;
					cout << "Current Op: " << FIFO.front() << endl << "curOpp->nextFullOp: " << endl << curOpp->nextFullOp << endl << "curOpp->NextAgent: " << curOpp->NextAgent << endl;
					struct CurentOp tempStruct;
					int tempRow, tempSeat;
					string temprow, tempseat;
					stringstream ss;
					string tempStr = FIFO.front();
					string tempDeadline;
					ss << tempStr;
					ss >> tempStruct.CurentAgent;
					cout << "tempStruct.CurentAgent: " << tempStruct.CurentAgent << endl;
					ss >> tempStruct.Opperation;
					cout << "tempStruct.Opperation: " << tempStruct.Opperation << endl;
					ss >> tempStruct.Plane;
					cout << "tempStruct.Plane: " << tempStruct.Plane << endl;
					ss >> tempStruct.Seat;
					cout << "tempStruct.Seat: " << tempStruct.Seat << endl;
					ss >> tempStruct.Person;
					ss >> tempDeadline;
					ss >> tempStruct.Deadline;
					//front parsed and poped from local list
					FIFO.pop_front();
					tempStr = FIFO.front();
					//ss << tempStr;
					//ss >> tempStruct.NextAgent;
					int tempStringCount2 = 0;
					while(FIFO.front()[tempStringCount2] != ' '){
						tempStr = tempStr + FIFO.front()[tempStringCount2];
						tempStringCount2++;
					}
					tempStruct.NextAgent = stoi(tempStr);
					cout << "NextAgent " << FIFO.front() << endl;
					startAgent = tempStruct.NextAgent;
					cout << "these should match " << startAgent << " " << tempStruct.CurentAgent << " " << curOpp->NextAgent << endl;
					//seperate out the row from the seat letter. letter to int is A-65=0 B-65=1 a-97=0 b-97=1
					for (int j = 0; j < tempStruct.Seat.length(); j++){
						if(isdigit(tempStruct.Seat[j])){
							temprow += tempStruct.Seat[j];
						}
						else{
							tempseat += tempStruct.Seat[j];
						}
					}
					//change row to int
					cout << "Is it giving a stoi error here? 1" << endl;
					tempRow = stoi(temprow);
					//change seat to int (accounting for upper and lower case)
					if(isupper(tempseat[0])){
						tempSeat = tempseat[0]-97;
					}
					else{
						tempSeat = tempseat[0]-65;
					}
					
					//Now that everything is parsed i shouldn't have to worry about if the Opperation is a wait since it should be from anohter agent
					//Now to update the flight with the given information by finding the correct flight and updating the seats
					cout << "Is it giving a stoi error here? 2" << endl;
					for (int j = 0; j < stoi(mylist.front()); j++){
						if (airplanes[j].name == tempStruct.Plane){
							if (airplanes[j].seat[tempRow][tempSeat].empty()){
								airplanes[j].seat[tempRow][tempSeat] = tempStruct.Person;
							}
							else if (tempStruct.Opperation == "cancel"){
								//if cancle and someone is on waitlist replace with person on wait list if waitlist is empty then just remove from seat
								if (!waitList.front().empty()){
									string tempWaitStr, tempWaitStr2;
									stringstream waitSS;
									//cycle through waitList to check for any person waiting on the seat
									for (int k = 0; k < waitList.size(); k++){
										waitSS << waitList[k];
										//curent agent
										waitSS >> tempWaitStr;
										//opperation
										waitSS >> tempWaitStr;
										//planes
										waitSS >> tempWaitStr;
										//seat
										waitSS >> tempWaitStr;
										//Person
										waitSS >> tempWaitStr2;	
										//check if anyone is waiting on the seat if so give them the seat and remove from list
										if (tempWaitStr == curOpp->Seat){
											waitList.erase(waitList.begin()+k);
											//found the seat and person and removed from wait list now leave loop
											break;
										}
									}
									airplanes[j].seat[tempRow][tempSeat] = tempWaitStr2;
								}
								else{
									airplanes[j].seat[tempRow][tempSeat].clear();
								}
							}
							else if (tempStruct.Opperation == "wait" or tempStruct.Opperation == "waitany"){
								waitList.push_back(tempStr);
							}
						}
					}
					//tempStruct.NextAgent;
						
					}
				//timePassed for int on execution and check deadline
				
				//SOOOOOO stringstream breaks when you fork? I need to make this a manual parse
				int tempRow, tempSeat, tempStringCount = 0;
				string temprow, tempseat;
				//stringstream ss;
				string tempStr = FIFO.front();
				string tempStr2;
				curOpp->FullOp = tempStr;
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 1" << endl;
				//itterate by 1 to go past ' '
				tempStringCount++;
				cout << "first stoi: " << tempStr2 << endl;
				curOpp->CurentAgent = stoi(tempStr2);
				//clear the string for next word
				tempStr2.clear();
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 2" << endl;
				tempStringCount++;
				cout << "Opperation " << tempStr2 << endl;
				curOpp->Opperation = tempStr2;
				tempStr2.clear();
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 3" << endl;
				tempStringCount++;
				curOpp->Plane = tempStr2;
				tempStr2.clear();
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 4" << endl;
				tempStringCount++;
				curOpp->Seat = tempStr2;
				tempStr2.clear();
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 5" << endl;
				tempStringCount++;
				cout << "Made it past while loop 5.2" << endl;
				cout << tempStr2 << endl;
				curOpp->Person = tempStr2;
				cout << "Made it past while loop 5.3" << endl;
				tempStr2.clear();
				cout << "Made it past while loop 5.4" << endl;
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 6" << endl;
				tempStringCount++;
				tempStr2.clear();
				//go twice to get past "deadline" and to the value
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				cout << "Made it past while loop 7" << endl;
				tempStringCount++;
				curOpp->Deadline = stoi(tempStr2);
				tempStr2.clear();
				FIFO.pop_front();
				tempStr = FIFO.front();
				cout << "set " << FIFO.front() << " to curOpp->nextFullOp " << endl;
				curOpp->nextFullOp = FIFO.front();
				cout << "did it set right?" << endl << curOpp->nextFullOp << endl;
				tempStringCount = 0;
				while(FIFO.front()[tempStringCount] != ' '){
					tempStr2 = tempStr2 + FIFO.front()[tempStringCount];
					tempStringCount++;
				}
				tempStringCount++;
				curOpp->NextAgent = stoi(tempStr2);
				tempStringCount = 0;
				tempStr2.clear();
				cout << "Made it out of parsing" << endl;
				/*ss << tempStr;
				ss >> tempStr2;
				//tempStr2 += tempStr[0];
				//tempStr.erase(tempStr.begin());
				//tempStr.erase(tempStr.begin());
				cout << FIFO.front() << endl << tempStr2 << endl << "Is it giving a stoi error here? 3 - " << tempStr2 << endl;
				curOpp->CurentAgent = stoi(tempStr2);
				ss >> tempStr2;
				curOpp->Opperation = tempStr2;
				ss >> tempStr2;
				curOpp->Plane = tempStr2;
				ss >> tempStr2;
				curOpp->Seat = tempStr2;
				ss >> tempStr2;
				curOpp->Person = tempStr2;
				//just to get past the "deadline" portion of input string
				ss >> tempStr2;
				ss >> tempStr2;
				cout << "Is it giving a stoi error here? 4" << endl;
				curOpp->Deadline = stoi(tempStr2);
				//front parsed and poped from local list
				FIFO.pop_front();
				tempStr = FIFO.front();
				curOpp->nextFullOp = tempStr;
				stringstream ss2;
				ss2 << tempStr;
				ss2 >> tempStr2;
				//get next agent that needs to execute 
				cout << "Is it giving a stoi error here? 5" << endl;
				curOpp->NextAgent = stoi(tempStr2);*/
				
				//////////////////////////////////////////////////////////////////////////////////////////
				
				//seperate out the row from the seat letter. letter to int is A-65=0 B-65=1 a-97=0 b-97=1
				/*
				for (int j = 0; j < curOpp->Seat.length(); j++){
					if(isdigit(curOpp->Seat[j])){
						temprow += curOpp->Seat[j];
					}
					else{
						tempseat += curOpp->Seat[j];
					}
				}
				//change row to int
				cout << "Is it giving a stoi error here? 6" << endl;
				tempRow = stoi(temprow);
				//change seat to int (accounting for upper and lower case)
				if(isupper(tempseat[0])){
					tempSeat = tempseat[0]-65;
				}
				else{
					tempSeat = tempseat[0]-97;
				}
				
				cout << "Is it giving a stoi error here? 7" << endl;
				for (int j = 0; j < stoi(mylist.front()); j++){
					if (airplanes[j].name == curOpp->Plane){
						if (curOpp->Opperation == "wait"){
							if (airplanes[j].seat[tempRow][tempSeat].empty()){
								airplanes[j].seat[tempRow][tempSeat] = curOpp->Person;
								timePassed += agents[curOpp->CurentAgent].wait;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
							else{
								waitList.push_back(curOpp->FullOp);
								timePassed += agents[curOpp->CurentAgent].wait;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
						}
						//exact same as wait instead difference when the agent finishes
						else if (curOpp->Opperation == "waitany"){
							if (airplanes[j].seat[tempRow][tempSeat].empty()){
								airplanes[j].seat[tempRow][tempSeat] = curOpp->Person;
								timePassed += agents[curOpp->CurentAgent].waitany;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
							else{
								waitList.push_back(curOpp->FullOp);
								timePassed += agents[curOpp->CurentAgent].waitany;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
						}
						else if (curOpp->Opperation == "reserve"){
							cout << "testing reserve at " << tempRow << " " << tempSeat << endl;
							cout << airplanes[j].seat[tempRow][tempSeat].empty() << endl;
							if (airplanes[j].seat[tempRow][tempSeat].empty()){
								airplanes[j].seat[tempRow][tempSeat] = curOpp->Person;
								timePassed += agents[curOpp->CurentAgent].reserve;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
							else{
								timePassed += agents[curOpp->CurentAgent].reserve;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " fails to " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " fails to " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " at time " << timePassed << ", deadline missed" << endl;
								}
							}
						}
						else if (curOpp->Opperation == "ticket"){
							if (airplanes[j].seat[tempRow][tempSeat].empty()){
								airplanes[j].seat[tempRow][tempSeat] = curOpp->Person;
								timePassed += agents[curOpp->CurentAgent].ticket;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " Successfully at time " << timePassed << ", deadline missed" << endl;
								}
							}
							else{
								timePassed += agents[curOpp->CurentAgent].ticket;
								if (timePassed <= curOpp->Deadline){
									cout << curOpp->Person << " fails to " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " at time " << timePassed << ", deadline met" << endl;
								}
								else{
									cout << curOpp->Person << " fails to " << curOpp->Opperation << " " << curOpp->Plane << " " << curOpp->Seat << " at time " << timePassed << ", deadline missed" << endl;
								}
							}
						}
						else if (curOpp->Opperation == "cancel"){
							//if cancle and someone is on waitlist replace with person on wait list if waitlist is empty then just remove from seat
							cout << "Cancel start!" << endl;
							if (!waitList.front().empty()){
								string tempWaitStr, tempWaitStr2;
								stringstream waitSS;
								//cycle through waitList to check for any person waiting on the seat
								for (int k = 0; k < waitList.size(); k++){
									waitSS << waitList[k];
									//curent agent
									waitSS >> tempWaitStr;
									//opperation
									waitSS >> tempWaitStr;
									//planes
									waitSS >> tempWaitStr;
									//seat
									waitSS >> tempWaitStr;
									//Person
									waitSS >> tempWaitStr2;	
									//check if anyone is waiting on the seat if so give them the seat and remove from list
									if (tempWaitStr == curOpp->Seat){
										waitList.erase(waitList.begin()+k);
										//found the seat and person and removed from wait list now leave loop
										break;
									}
								}
								airplanes[j].seat[tempRow][tempSeat] = tempWaitStr2;
							}
							else{
								airplanes[j].seat[tempRow][tempSeat].clear();
							}
							cout << "Cancel end!" << endl;
						}
						else if (curOpp->Opperation == "check_passenger"){
							cout << "check_passenger" << endl;
							
						}
					}
				}
			//tell next agent to go;
			agents[i].opperations.pop_front();
			sb.sem_op = 1;
			cout << "Tell " << curOpp->NextAgent << " to go" << endl;
			semop(vecSid[curOpp->NextAgent], &sb, 1);
			sb.sem_op = -1;
			//set sem_op back to wait
			}
			
			cout << "exiting" << endl;
			exit(0);
		}
		//else
			//wait(NULL);
	}
	//wait(NULL);	
	/*cout << endl << "Running in EDF order: " << endl;
	curOpp->FullOp = EDF.front();
	for (int i = 0; i < 3; i++){
		if(fork() == 0){
		cout << "hello " << i << endl;
		exit(0);
		}
		else
			wait(NULL);
	}
	
	cout << endl << "Running in LLF order: " << endl;
	curOpp->FullOp = LLF.front();
	for (int i = 0; i < 3; i++){
		if(fork() == 0){
			cout << "hello " << i << endl;
			exit(0);
		}
		else
			wait(NULL);
	}
	//wait(NULL);
	cout << "this is a different run3" << endl;*/
	//semctl(sid, 0, IPC_RMID, 0);

	/*forkTest();
	wait(NULL);
	cout << "This should only print once" << endl;*/
	
	return 0;
};