#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void countPlaced(int num1, int num2){
  int countWell = 0;
  int arr1[4] = {0};
  int arr2[4] = {0};
  for (int i=3; i>=0; i--){
    arr1[i] = num1%10;
    num1 = num1 /10;

    arr2[i] = num2%10;
    num2 = num2 /10;

    if (arr1[i]==arr2[i]){
      countWell++;
    }
  }
  int countMiss = 0;
  for (int i=0; i<4; i++){
    for (int j=0; j<4; j++){
      if (i!=j && arr1[i]==arr2[j]){
        countMiss++;
        break;
      }
    }
  }
  printf("Well placed pieces: %d\n", countWell);
  printf("Misplaced pieces: %d\n", countMiss);
}

int check(int num1, int num2){
    if (num1==num2){
      return 1;
    }
    countPlaced(num1, num2);

    return 0;
}

int Readline(char* buff){
    int size = 0;
    char ch;
    while (size < 10){
      read(0, &ch, 1);
      buff[size++] = ch;
      if (ch == '\n'){
        break;
      }
    }
    if (size!=5){
        return 0;
    }
    return 1;

}

int check_input(int num){
    if (num<99 || num > 9999){return 0;}
    int arr1[4] = {0};
    for (int i=3; i>=0; i--){
        arr1[i] = num%10;
        num = num /10;
    }
    for (int i = 0; i<4; i++){
        if (arr1[i] > 7){
            return 0;
        }
        for (int j = i+1; j<4; j++){
            if (arr1[i] == arr1[j]){
                return 0;
            }
        }
    }

    return 1;      
}

int mastermind(int code, int numAttempt){
    int attempt = 0;
    int userInput = 0;
    char buffer[10];

    while (attempt < numAttempt){
        printf("Round %d\n", attempt);
        if (Readline(buffer) == 0){
            printf("Input must be exactly size of 4!\n");
            continue;
        }
        userInput = atoi(buffer);
        if (check_input(userInput)==0){
          printf("Wrong Input!\n");
          continue;
        }
        
        if (check(code, userInput)){
            printf("Congratz! You did it!\n");
            return 1;
        }else{
            printf("---\n");
            attempt++;
        }   
    }

    printf("You Lost!\n");
    printf("Correct code is %d\n", code);
    return 1;
}