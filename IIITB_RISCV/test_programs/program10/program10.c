#include "firmware.h"

void matmul(void)
{
    int a[2][2],b[2][2],c[2][2];

    a[0][0] = 1; a[0][1] = 2; a[1][0] = 3; a[1][1] = 4;
    b[0][0] = 1; b[0][1] = 2; b[1][0] = 3; b[1][1] = 4;
    c[0][0] = 0; c[0][1] = 0; c[1][0] = 0; c[1][1] = 0;

    for(int i=0;i<2;i++)
    {
        for(int j=0;j<2;j++)
        {
            for(int k=0;k<2;k++)
            {
                c[i][j] += a[i][k]*b[k][j];
            }
        }
    }

    return;
}