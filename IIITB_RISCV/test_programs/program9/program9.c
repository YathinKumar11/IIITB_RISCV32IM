#include "firmware.h"

int main()
{
    int i=0,j=0;
    int a[5],temp,min_ind;
    a[0]=5;a[1]=4;a[2]=3;a[3]=2;a[4]=1;

    for(i=0;i<4;i++)
    {
        min_ind = i;
        for(j=i+1;j<5;j++)
        {
            if(a[j]<a[min_ind])
            {
                min_ind = j;
            }
        }
        temp = a[i];
        a[i] = a[min_ind];
        a[min_ind] = temp;
    }

}