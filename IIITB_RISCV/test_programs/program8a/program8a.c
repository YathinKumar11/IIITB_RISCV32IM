#include "firmware.h"

void array(void)
{
    int a[6], b[6];
    a[0] = 0;
    a[1] = 1;
    a[2] = 2;
    a[3] = 3;
    a[4] = 4;
    a[5] = 5;
    
    b[0] = 0;
    b[1] = 2;
    b[2] = 4;
    b[3] = 6;
    b[4] = 8;
    b[5] = 10;
    int res=0;
    
    
    for(int i=0;i<6;i++)
    {
        res+=a[i]+b[i];
    }
}
