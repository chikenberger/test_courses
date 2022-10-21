#include <iostream>
using namespace std;
void sum_r(double r1,double r2,double r3, dounlr &r);
int main()
{
    double r1,r2,r3,r;
    cout<< "VVedite soprotivlenie R1 ";
    cin>>r1;
    cout<< "VVedite soprotivlenie R2 ";
    cin>>r2;
    cout<< "VVedite soprotivlenie R3 ";
    cin>>r3;
    
    dounle &r_link;
    r_link = r;
    sum_r(r1,r2,r3,r);
    
    cout<< "Summa soprotivlenii "<< r <<endl;
 
    return 0;
 
}
void sum_r(double r1,double r2,double r3, dounlr &r)
{
    r = 1/(1/r1+1/r2+1/r3);
}