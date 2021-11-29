#include <stdio.h>

int main(int argc, char* argv[]){
    int char_arr[130] = {0};
    for (int arg = 1; arg<argc; arg++){
        int i = 0;
        while (argv[arg][i] != '\0'){
            if (argv[arg][i] == '"'){
                i++;
                continue;
            }
            int idx = (int) argv[arg][i++];
            char_arr[idx]++;
        }
    }

    for (int i=0; i<128; i++){
        if (char_arr[i] != 0){
            printf("%c:%d\n", (char) i, char_arr[i]);
        }
    }

    return 0;

}