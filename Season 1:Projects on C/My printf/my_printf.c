#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdarg.h>
#include <string.h>

//this function converts num in decimal to string according to its base
void write_number(int num, int base, int* num_chars){
  static char Representation[]= "0123456789abcdef";
  char* buffer = malloc(1024);
  int ind = 0;

  if (num==0){
    write(1,"0",1);
    *num_chars = *num_chars + 1;
    return;
  }

  while (num != 0){
    *(buffer + ind) = Representation[num%base];
    num /= base;
    ind++;
  }
  *num_chars = *num_chars + ind;
  ind--;
  while (ind != -1){
    write(1, buffer+ind, 1);
    ind--;
  }
  
  

  free(buffer);
}

int my_printf(char * restrict format, ...){
    va_list arg; 
    va_start(arg, format);
    int num_chars = 0;

    for (char *c = format; *c != '\0'; c++){
        if (*c != '%'){
            num_chars++;
            write(1,c,1);
            continue;
        }
        c++;

        //these statements handle c (char) and duox flags
        if (*c == 'c'){
          char ch[2] = "/0";
          ch[0] = (char) va_arg(arg, int);
          num_chars++;
          write(1,ch,1);
        }else if (*c == 'd'){
          int num = va_arg(arg, int);
          if (num<0){
            num_chars++;
            write(1,"-",1);
          }
          num = num*(-1);
          write_number(num, 10, &num_chars);    
        }else if (*c == 'u'){
          int num = va_arg(arg, int);
          write_number(num, 10, &num_chars);
        }else if (*c == 'o'){
          int num = va_arg(arg, int);
          write_number(num, 8, &num_chars);
        }else if (*c == 'x'){
          int num = va_arg(arg, int);
          write_number(num, 16, &num_chars);
        }else if (*c == 's'){
            //this statement handle string
            char* buffer = va_arg(arg, char*);
            while (*(buffer) != '\0'){
              num_chars++;
              write(1,buffer,1);
              buffer++;
            }
        }else if (*c == 'p'){
          //this statement handle pointer address
          void* p = va_arg(arg, void *);
          int a = (int) p;
          num_chars++;
          write(1,"0",1);
          num_chars++;
          write(1,"x",1);
          write_number(a, 16, &num_chars);
        }
        
    }

    return num_chars;

}


int main(int argc, char** argv){
    void* a;
    int n = my_printf("char *restrict format, %c %x %s %p...\n", 'f', 0, "HELLO WORLD", a);

    int m = printf("char *restrict format, %c %x %s %p...\n", 'f', 0, "HELLO WORLD",a);

    printf("n is : %d, m is: %d\n", n, m);
    


    return 0;
}