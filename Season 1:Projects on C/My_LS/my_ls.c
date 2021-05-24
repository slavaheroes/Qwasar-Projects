#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdbool.h>
#include <pwd.h>
#include <grp.h>
#include <string.h>
#include <time.h>
#include "my_ls.h"
#define MAX_STR_LENGTH 1024
#define MAX_TIME_LENGTH 20

// this struct is used to make an array of files we are going to list
// it makes easy them to sort

int main(int argc, char* argv[]){

	struct stat sb;
	int opt, optcount=0;
	bool listAll = false, listLong = false;  bool listSort = false;

	char filename[MAX_STR_LENGTH];


	while((opt = getopt(argc, argv, "alt")) != -1){
		switch(opt){
			case('a'):
				listAll = true;
				break;
			case('l'):
				listLong = true;
				break;
            case('t'):
                listSort = true;
			default:
				break;
		}
	}

	//check the number of option arguments (starting with '-')
	for(int i = 1; i < argc; i++){
		if(argv[i][0] == '-'){
			optcount++;
		}
	}

	//if there were no arguments other than options, then list what's in the current directory
	if(argc - optcount == 1){
        listDir(".", listAll, listLong, listSort);
	}
	else{
		//go through each command line argument
		for(int i = 1; i < argc; i++){
			strncpy(filename, argv[i], MAX_STR_LENGTH);
			
			//exclude option arguments
			if(filename[0] == '-'){
				continue;
			}
			
			//make sure filename is valid
			if(stat(filename, &sb) == -1){
				perror(filename);
			}
			else{
				//if the file is a directory then read it's contents and list the files inside
				//otherwise just list the file
				if((sb.st_mode & S_IFMT) == S_IFDIR){
					if(argc - optcount > 2){
						printf("%s:\n",filename);
					}
                    listDir(filename, listAll, listLong, listSort);
					printf("\n");
				}
				else{
					listFile(".",filename, listLong);
				}
			}
		}
	}
}