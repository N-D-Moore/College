#include <iostream>
#include <string.h>
#include <cmath>
#include <iomanip>

using namespace std;

bool constraintsA(int b, int c, int e, int f) {
    int d = e + f + 21;
    int a = b + c + e + f;
    if ((a <= 50) && (e + f <= 29)){
        if ((e*e*a + 417) == d*d) {
            cout << "Solution found: " << a << " " << b << " " << c << " " << d << " " << e << " " << f << ", ";
            return true;
        }
        //HE IS MISSING AN ELSE STATMENT HERE TO RETURN FALSE IF IT REACHES INSIDE THIS IF STATEMENT FUNCTION RETURNS NOTHING AND THIS IS A BUG
        //ADDING THE ELSE STATEMENT FIXES THE CODE
    }
    else 
    {
        return false;
    }
}

void *problemA() {
    int nva = 0;
    for (int b = 1; b <= 47; b++)
        for (int c = 1; c <= 47; c++)
            for (int e = 1; e <= 47; e++)
                for (int f = 1; f <= 47; f++) {
                    nva++;
                    if (constraintsA(b, c, e, f) == true){
                        cout << "nva: " << nva << endl;
                        return NULL;
                }
                }
    return NULL;
}

int main()
{
    char problem;
    cout << "Select problem [A], [B], or [C]: ";
    cin >> problem;
    if (problem == 'A'){
        problemA();
    }
	return 0;
}