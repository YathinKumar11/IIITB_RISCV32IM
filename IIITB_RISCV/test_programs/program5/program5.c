#include "firmware.h"
void nested_ifelse(void) {
    int number1=5, number2=8;
    int result=0;
    if (number1 >= number2) {
      if (number1 == number2) {
        result=1;
        return;
      }
      else {
        result=2;
        return;
      }
    }
    else {
        result = 3;
        return;
    }
}