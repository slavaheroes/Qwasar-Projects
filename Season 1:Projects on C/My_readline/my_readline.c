#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#define READLINE_READ_SIZE 50000

char *my_readline(int fd){
    char* ret = malloc(READLINE_READ_SIZE);
    if (ret == NULL){
        fprintf(stderr,"malloc error: %s", strerror(errno));
        return NULL;
    }
    unsigned long long len = 0;


    char temp;

    while(1){
        ssize_t size = read(fd, &temp, 1);

        if (size == -1){
            // error of read function
            fprintf(stderr,"read error: %s", strerror(errno));
            free(ret);
            return NULL;
        } 
        //we succesfully got some character     
        if (size == 0){
            //we reached end of file
            *(ret+len) = '\0';
            return ret;
        }
        
        if (temp == '\n'){
            //we reached the newline character
            *(ret+len) = '\0';
            return ret;
        }

        *(ret+len) = temp;
        len++;
    }

    return ret;

}

int main(){
    
    char* res = my_readline(0);
    printf("%s", res);

    FILE *fp;
    fp=fopen("test.txt", "r");

    char* res1 = my_readline(fileno(fp));
    printf("%s", res1);

    free(res);
    free(res1);
}