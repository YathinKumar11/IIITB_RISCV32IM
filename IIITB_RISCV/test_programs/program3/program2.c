#include "firmware.h"

void program2(void)  
{  
    int a, b, c;
    a=3;
    b=9;
    c=4;
    int g=0;
    if(a>b && a>c)  //a is greatest
    {  
        g = 1;
        return ;  
    }  
    if(b>a  && b > c)  //b is greatest
    {  
        g = 2;
       return ;   
    } 
    if(c>a && c>b)  //c is greatest
    {  
        g = 3;
        return ;   
    }  
    if(1)//a == b && a == c)   //all 3 are equal
    {  
        g = 4;
       return ;    
    }  
     

}
