#include <iostream>
#include <fstream>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <list>
#include <sys/wait.h>

using namespace std;

list<string> mylist;
//input_var, vertex, opperatons, writes
int sizes[4];

struct input_var {
	string name;
	float value;
};

struct vertex {
	string name;
	string Opperator;
	float value1;
	float value2;
};

struct opperatons {
	string start;
	string end;
	string end2;
};

//made this one at like 4am no idea why i i did value instead of name here and noticed it only now i am adding comments
struct writes {
	string value;
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

	//get sizes of dynamic arrays for variables
	int count = 0;
	for (auto const &v : mylist){
		if (v[0] == 'i'){
			char a = 'a';
			for (int i = 9; i < v.length(); i++){
				if (v[i] == a) {
					a++;
					count++;
				}
			}
			//counting input_var
			sizes[0] = count;
			count = 0;
		}
		else if (v[0] == 'v' and v[1] == 'e'){
			count = 0;
			for (int i = 6; i < v.length(); i++){
				if (v[i] == 'v') {
					count++;
				}
			}
			//counting vertexs
			sizes[1] = count;
			count = 0;
		}
		else if (v[0] == 'w'){
			//counting operations
			sizes[2] = count;
			count = 0;
			for (int i = 5; i < v.length(); i++){
				if (v[i] != ',' and v[i] != '(' and v[i] != ')' and v[i] != '(' and v[i-1] != 'v' and v[i] != '.') {
					count++;
				}
			}
			//counting writes
			sizes[3] = count;
			count = 0;
		}
		else{
			count++;
		}
	}

	return 0;
}

//next 4 functions are probably pure sphagheti code just parsing out the variables from mylist generated from the input txt file
//wanted to use the built in c++ parser but have only gotten 3-5 hours of sleep a day due to assignments and mid terms so didn't understand it.
input_var* getVar(){
	struct input_var* temp;
	temp = new input_var[sizes[0]];
	int spot = 0;
	for (auto const &v : mylist){
		//input_var name
		if (v[0] == 'i'){
			int j = 0;
			char a = 'a';
			for (int i = 9; i < v.length(); i++){
				if (v[i] == a) {
					temp[j].name = a;
					a++;
					j++;
				}
			}
		}
		//input_var value
		if (isdigit(v[0])){
			for (int i = 0; i < v.length(); i++){
				if (isdigit(v[i]) and not(isdigit(v[i-1])) and v[i-1] != '.'){
					string temp1;
					int j = i;
					while (isdigit(v[j]) or v[j] == '.'){
						temp1 = temp1 + v[j];
						j++;
					}
					temp[spot].value = stof(temp1);
					spot++;
				}
			}
		}
	}
	
	return temp;
}

vertex* getVer(){
	struct vertex* temp;
	temp = new vertex[sizes[1]];
	int spot = 0;
	for (auto const &v : mylist){
		if (v[0] == 'v' and v[1] == 'e'){
			for (int i = 6; i < v.length(); i++){
				string temp1, temp2;
				//get vertexs in format v# and associated opperator ie PLUS etc.
				if (v[i] == 'v') {
					temp1 = temp1 + v[i] + v[i+1];
					int j = i + 5;
					while (v[j] != ','){
						if (v[j] == ',') {
							break;
						}
						else if (v[j] == ';'){
							break;
						}
						temp2 = temp2 + v[j];
						j++;
					}
					temp[spot].name = temp1;
					temp[spot].Opperator = temp2;
					spot++;
				}
				
			}
		}
	}
	return temp;
}

//get the opperations such as a -> v1
opperatons* getOpp(){
	struct opperatons* temp;
	temp = new opperatons[sizes[2]];
	int count = 0;
	int spot = 0;
	for (auto const &v : mylist){
		if (count > 2){
			if (v[0] != 'w'){
				int j = 0;
				while (v[j] != ';'){
					//ignore everything not a input_var or vertex
					if (v[j] != ' ' and v[j] != '-' and v[j] != '>' and v[j-1] != 'v'){
						string temp1; 
						if (v[j] == 'v'){
							temp1 = temp1 + v[j] + v[j+1];
						}
						string tempStart = temp[spot].start;
						string tempEnd = temp[spot].end;
						string tempEnd2 = temp[spot].end2;
						//input before first ->
						if (tempStart.empty()){
							if (v[j] == 'v'){
								temp[spot].start = temp1;
							}
							else{
								temp[spot].start = v[j];
							}
						}
						//input after first ->
						else if (tempEnd.empty() and !tempStart.empty()){
							if (v[j] == 'v'){
								temp[spot].end = temp1;
							}
							else{
								temp[spot].end = v[j];
							}
						}
						//input after second ->
						else if (tempEnd2.empty() and !tempEnd.empty() and !tempStart.empty()){
							if (v[j] == 'v'){
								temp[spot].end2 = temp1;
							}
							else{
								temp[spot].end2 = v[j];
							}
						}
					}
					j++;
				}
				spot++;
			}
		}
		count++;
	}
	return temp;
}	

//get all the values specified to be written after caluclations
writes* getWrite(){
	struct writes* temp;
	temp = new writes[sizes[3]];
	int spot = 0;
	for (auto const &v : mylist){
		if (v[0] == 'w'){
			for (int i = 5; i < v.length(); i++){
				string temp1;
				//ignore none variables and only extra variables
				if (v[i] != ',' and v[i] != '(' and v[i] != ')' and v[i] != '(' and v[i-1] != 'v' and v[i] != '.') {
					if (v[i] == 'v'){
						temp1 = temp1 + v[i] + v[i+1];
						temp[spot].value = temp1;
						spot++;
					}
					else{
						temp[spot].value = v[i];
						spot++;
					}
				}
			}
		}
	}
	return temp;
}	

//figure out the value of given input by looking it up in either input_Var or Vertex
float getValue(string Name, input_var* input_Var, vertex* Vertex){
	float temp;
	for (int j = 0; j < sizes[0]; j++){
		if (Name == input_Var[j].name){
			temp = input_Var[j].value;
			return temp;
		}
	}
	for (int j = 0; j < sizes[1]; j++){
		if (Name == Vertex[j].name){
			temp = Vertex[j].value1;
			return temp;
		}
	}
	return temp;
}

//moved math into function to clean up code below
float doMath(float a, float b, string ver, vertex* Vertex){
	float temp;
	string temp2;
	//find math opperation for given vertex
	for (int i = 0; i < sizes[1]; i++){
		if (ver == Vertex[i].name){
			//first assignment however will mess up if the value after math is supposed to be 0
			if ( a == 0){
				return b;
			}
			temp2 = Vertex[i].Opperator;
			break;
		}
	}
	if (temp2 == "PLUS"){
		temp = a + b;
	}
	if (temp2 == "MINUS"){
		temp = a - b;
	}
	if (temp2 == "DIVIDE"){
		temp = a / b;
	}
	if (temp2 == "TIMES"){
		temp = a * b;
	}
	return temp;
}



int main(int agrc, char *agrv[]) {
	
	readFile(agrc, agrv);
	
	struct input_var* input_Var;
	input_Var = getVar();
	struct vertex* Vertex;
	Vertex = getVer();
	struct opperatons* Opperatons;
	Opperatons = getOpp();
	struct writes* Write;
	Write = getWrite();
	
	//construct pipes for the vertexs
	int fd[sizes[1]][2];
	for (int i = 0; i < sizes[2]; i++){
		pipe(fd[i]);
	}
	pid_t pipeTest = fork();
	//for loop to itterate through the list of opperations
	for (int i = 0; i < sizes[2]; i++){
		//child
		if (pipeTest == 0){
			string temp1 = Opperatons[i].end2;
			// are there more than 1 opperatons?
			if (!temp1.empty()){
				//find given values for inputs in the opperation line
				float a, b, c, d;
				a = getValue(Opperatons[i].start, input_Var, Vertex);
				b = getValue(Opperatons[i].end, input_Var, Vertex);
				c = getValue(Opperatons[i].end2, input_Var, Vertex);
				//math requested by given inputs ie a PLUS v1 = a+v1
				d = doMath(b, a, Opperatons[i].end, Vertex);
				//update with vertex with new value
				for (int j = 0; j < sizes[1]; j++){
					if (Opperatons[i].end == Vertex[j].name){
						Vertex[j].value1 = d;
						break;
					}
				}
				//relook up value for b now that it has been updated
				b = getValue(Opperatons[i].end, input_Var, Vertex);
				//math requested by given inputs ie a PLUS v1 = a+v1
				d = doMath(c, b, Opperatons[i].end2, Vertex);
				//update vertex with new value
				for (int j = 0; j < sizes[1]; j++){
					if (Opperatons[i].end2 == Vertex[j].name){
						Vertex[j].value1 = d;
						break;
					}
				}
			}
			//if there are only one opperation
			else{
				//find given values for inputs in the opperation line
				float a, b, c;
				a = getValue(Opperatons[i].start, input_Var, Vertex);
				b = getValue(Opperatons[i].end, input_Var, Vertex);
				//math requested by given inputs ie a PLUS v1 = a+v1
				c = doMath(b, a, Opperatons[i].end, Vertex);
				//update with vertex with new value
				for (int j = 0; j < sizes[1]; j++){
					if (Opperatons[i].end == Vertex[j].name){
						Vertex[j].value1 = c;
						break;
					}
				}				
			}
			//writing values to pipe
			for (int j = 0; j < sizes[1]; j++){
				write(fd[j][1], &Vertex[j].value1, sizeof(int));
			}
		}
		//parent
		else{
			//tried to get the caluclations to be done across the fork but every time i try it fails due to child not waiting on parent to finish
			// read pipes from child and update values with what is inside
			for (int j = 0; j < sizes[1]; j++){
				read(fd[j][0], &Vertex[j].value1, sizeof(int));
			}			
			//parent is last to run therefore prints out the final values requested by write when it hits the final iteration of the for loop
			if (i == 7){
				for (int i = 0; i < sizes[3]; i++){
					cout << Write[i].value << "=" << getValue(Write[i].value, input_Var, Vertex) << endl;
				}
			}
		}
		
	}
	//deallocate memory
	delete [] input_Var;
	delete [] Vertex;
	delete [] Opperatons;
	delete [] Write;
	input_Var = NULL;
	Vertex = NULL;
	Opperatons = NULL;
	Write = NULL;
	
	return 0;
}
