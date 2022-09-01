#include "firmware.h"

void nested_for(void)
{
    int res = 0;
    for(int i=0;i<10;i++)
    {
        for(int j=0;j<10;j++)
        {
            res+=i+j;
        }
    }
    return;
}