#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include "mastermind.h"


int main(int argc, char* argv[]){
    time_t t;
    /* Intializes random number generator */
    srand((unsigned) time(&t));
    int code = 0;
    while (!check_input(code)){
        code = rand()%10000;
    }
    int numAttempt = 10;
    for (int i = 0; i<argc; i++){
        if (argv[i][0] == '-'){

            if (argv[i][1] == 'c' && argv[i][2]=='\0'){
                int len = 0;
                while (argv[i+1][len] != '\0'){
                    len++;
                }
                if (len != 4){
                    printf("Enter 4 digits integer!\n");
                    return 0;
                }
                code = atoi(argv[i+1]);
            }
            else if (argv[i][1] == 't' && argv[i][2]=='\0'){
                numAttempt = atoi(argv[i+1]);
            }else if (argv[i][1] == 'c' && argv[i][2] == 't'){
                int len = 0;
                while (argv[i+1][len] != '\0'){
                    len++;
                }
                if (len != 4){
                    printf("Enter 4 digits integer!\n");
                    return 0;
                }
                code = atoi(argv[i+1]);
                numAttempt = atoi(argv[i+2]);
            }else if (argv[i][1] == 't' && argv[i][2] == 'c'){
                int len = 0;
                while (argv[i+2][len] != '\0'){
                    len++;
                }
                if (len != 4){
                    printf("Enter 4 digits integer!\n");
                    return 0;
                }
                code = atoi(argv[i+2]);
                numAttempt = atoi(argv[i+1]);
            }
            
        }
    }

    if (check_input(code) == 0){
        printf("Wrong Code format\n");
        return 1;
    }

    /* Variables are initialized, let's play! */
    printf("Will you find the secret code?\n");
    printf("---\n");
    
    return mastermind(code, numAttempt);
}