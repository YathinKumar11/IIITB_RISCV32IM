#include "firmware.h"

void array(void)
{
    int a[6];
    a[0] = 0;
    a[1] = 1;
    a[2] = 2;
    a[3] = 3;
    a[4] = 4;
    a[5] = 5;
    int res=0;
    for(int i=0;i<6;i++)
    {
        res+=a[i];
    }
}
