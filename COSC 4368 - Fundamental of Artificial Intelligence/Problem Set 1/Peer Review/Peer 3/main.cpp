#include <iostream>
#include <cmath>
#include <array>
#include <vector>


using namespace std;



int main() {
    int count=0;
    char input;
    
    cout<< "Please enter which problem you would like to run (A/B/C)"<<endl;
    cin>> input;
    
    switch (input){
        case 'A':
        case 'a':
            int d,f,c;
            for(int a=1; a<51; a++){
                count+=1;
                for (int e=1; e<50; e++){
                    count+=1;
                    d=sqrt(pow(e, 2)*a+417);
                    count+=1;
                    f=d-e-21;
                    count+=1;
                    if(f>0){
                    for (int b=1; b<a-e-f; b++){
                        count+=1;
                        c=a-b-e-f;
                        count+=1;
                        if(a==b+c+e+f){
                        if(d==e+f+21){
                        if(pow(d,2)==e*e*a+417){
                        if(a>f+e){
                            cout<< "A= "<<a<<endl;
                            cout<< "B= "<<b<<endl;
                            cout<< "C= "<<c<<endl;
                            cout<< "D= "<<d<<endl;
                            cout<< "E= "<<e<<endl;
                            cout<< "F= "<<f<<endl;
        
                            cout<<"nva count: "<< count<<endl;
                            return 0;
                        }}}}
                    }}}}
            break;
        case 'b':{
        case 'B':
            int d,f,c,g,h,j;

            for(int a=1; a<51; a++){
                count+=1;
                for (int e=1; e<50; e++){
                    count+=1;
                    d=sqrt(pow(e, 2)*a+417);
                    count+=1;
                    f=d-e-21;
                    count+=1;
                    if(f>0){
                    g=f-sqrt(a+d+1);
                    count+=1;
                    j=(pow(g, 2)+39)/4;
                    count+=1;
                    if(g>0){
                    for (int b=1; b<a-e-f; b++){
                        count+=1;
                        c=a-b-e-f;
                        count+=1;
                    for (int i=1;i<51;i++){
                        count+=1;
                        h=(pow(g+i, 2)-e*12)/j;
                        count+=1;
                        if(a==b+c+e+f){
                        if(d==e+f+21){
                        if(pow(d,2)==e*e*a+417){
                        if(a>f+e){
                        if(pow(g+i,2)==h*j+e*12){
                        if(a+d==pow(f-g, 2)-1){
                        if(4*j==pow(g, 2)+39){
                        if(pow(i-g, 9)==pow(f-h, 3)){
                        if(pow(g-c, 2)==f*c*c+1){
                        cout<< "A= "<<a<<endl;
                            cout<< "B= "<<b<<endl;
                            cout<< "C= "<<c<<endl;
                            cout<< "D= "<<d<<endl;
                            cout<< "E= "<<e<<endl;
                            cout<< "F= "<<f<<endl;
                            cout<< "G= "<<g<<endl;
                            cout<< "H= "<<h<<endl;
                            cout<< "I= "<<i<<endl;
                            cout<< "J= "<<j<<endl;
                            
                            cout<<"nva count: "<< count<<endl;
                            return 0;
                        }}}}}}}}}}
                        }}}}}
            break;
        }


        case 'c':
        case 'C':{
            int d,f,c,g,h,j,o,k,n;

                for(int a=1; a<51; a++){
                    count+=1;
                    for (int e=1; e<50; e++){
                        count+=1;
                        d=sqrt(pow(e, 2)*a+417);
                        count+=1;
                        f=d-e-21;
                        count+=1;
                        if(f>0){
                        g=f-sqrt(a+d+1);
                            count+=1;
                        j=(pow(g, 2)+39)/4;
                            count+=1;
                        if(g>0){
                        for (int b=1; b<a-e-f; b++){
                            count+=1;
                            c=a-b-e-f;
                            count+=1;
                        for (int i=1;i<51;i++){
                            count+=1;
                            h=(pow(g+i, 2)-e*12)/j;
                            count+=1;
                            o=sqrt(g*h*i*b+133);
                            count+=1;
                        for (int m=1;m<51;m++){
                            count+=1;
                            k=sqrt(2*m+6);
                            count+=1;
                            n=sqrt(pow(m, 2)+291);
                            count+=1;
                        for(int l=1;l<51;l++){
                            count+=1;
                            if(a==b+c+e+f){
                            if(d==e+f+21){
                            if(pow(d,2)==e*e*a+417){
                            if(a>f+e){
                            if(pow(g+i,2)==h*j+e*12){
                            if(a+d==pow(f-g, 2)-1){
                            if(4*j==pow(g, 2)+39){
                            if(pow(i-g, 9)==pow(f-h, 3)){
                            if(pow(g-c, 2)==f*c*c+1){
                            if(2*m==pow(k, 2)-6){
                            if(pow(n-o, 3)+7==(f-i)*n){
                            if(pow(n, 2)==pow(m, 2)+291){
                            if(pow(o, 2)==g*h*i*b+133){
                            if(m+o==pow(k, 2)-10){
                            if(pow(l, 3)+i==(l+b)*k){
                            cout<< "A= "<<a<<endl;
                                cout<< "B= "<<b<<endl;
                                cout<< "C= "<<c<<endl;
                                cout<< "D= "<<d<<endl;
                                cout<< "E= "<<e<<endl;
                                cout<< "F= "<<f<<endl;
                                cout<< "G= "<<g<<endl;
                                cout<< "H= "<<h<<endl;
                                cout<< "I= "<<i<<endl;
                                cout<< "J= "<<j<<endl;
                                cout<< "K= "<<k<<endl;
                                cout<< "L= "<<l<<endl;
                                cout<< "M= "<<m<<endl;
                                cout<< "N= "<<n<<endl;
                                cout<< "O= "<<o<<endl;
                            cout<<"nva count: "<< count<<endl;
                                return 0;
                            }}}}}}}}}}}}}}}}}}}
                            }}}}}
                break;
        default:{
            cout<< "Choice invalid"<<endl;
        }
    }




    return 0;
}



