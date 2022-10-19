#include <iostream>
using namespace std;
double r1,r2,r3,r;
double sum_r(double r1,double r2,double r3);
int main()
{
    cout<< "VVedite soprotivlenie R1 ";
    cin>>r1;
    cout<< "VVedite soprotivlenie R2 ";
    cin>>r2;
    cout<< "VVedite soprotivlenie R3 ";
    cin>>r3;
    
    r=sum_r(r1,r2,r3);
    
    cout<< "Summa soprotivlenii "<< r <<endl;
 
    return 0;
 
}
double sum_r(double r1,double r2,double r3)
{
    r = 1/(1/r1+1/r2+1/r3);
    return r;
}