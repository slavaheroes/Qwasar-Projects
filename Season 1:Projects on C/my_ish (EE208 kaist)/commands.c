/*--------------------------------------------------------------------*/
/* Shen Vyacheslav; ID: 20180878 */
/* Abdimazhit Asmir; ID: 20180823 */

/* dfa.c */

/* This file contains functions which are 
used to execute 4 shell built in commands  */

#include "commands.h"
#include "dfa.h"
#include "dynarray.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#include <unistd.h>
#include <errno.h>

/*--------------------------------------------------------------------*/
/* cd [dir] */

void ch_dir(char **argv)
{

  if (argv[1] == NULL){ // no argument
    if (chdir(getenv("HOME")) < 0){
      fprintf(stderr, "ish: %s\n", strerror(errno));
    }
    return;
  }

     
  if (argv[2] == NULL){// inpur with argument

    if (chdir(argv[1])<0){ //error in cd
      fprintf(stderr, "ish: %s\n", strerror(errno));
    }

  return;
  }

  //other cases which are error
  fprintf(stderr, "ish: cd takes one parameter\n");
  return;

}

/*--------------------------------------------------------------------*/
/*setenv var [value] */
void env_set(char **argv){
  // no parameter
  if ((argv[1] == NULL)){
    fprintf(stderr, "./ish: setenv takes one or two parameters\n");
    return;
  }

  //when [value] exist or two parametes

  if (argv[3] == NULL){
    if (setenv(argv[1], argv[2], 1) < 0){ //add new var or overwrite
	fprintf(stderr, "./ish: %s\n", strerror(errno));
	return;
      }
    return; //successfully finished
    }
  
  // when [value] does not exist or one parameter
  if (argv[2] == NULL){
    if (setenv(argv[1], "", 1) < 0){
      
      //[value] is replaced by empty string
      
	fprintf(stderr, "./ish: %s\n", strerror(errno));
	return;
      }
    return; //succesfully finished
    }
  

  //more than two parameters and printing error
  fprintf(stderr, "./ish: setenv takes one or two parameters\n");
  return;
 }





/*--------------------------------------------------------------------*/
/* unsetenv var */
void env_unset(char **argv){
  // check for inputs
  //has no input or more than one
  if (argv[1] == NULL){
    fprintf(stderr,"./ish: unsetenv takes one parameter\n");
    return;
  }

  // unsetting and printing error
  if (unsetenv(argv[1]) < 0){
    fprintf(stderr, "./ish: %s\n", strerror(errno));
    return;
  }

  
  //succesfully unsetting
  return;
}
/*--------------------------------------------------------------------*/
/* exit command */
void call_exit(char **argv, DynArray_T oTokens){

  //check input

  if (argv[1] != NULL){
    //exit has parameter

    fprintf(stderr, "./ish: exit does not take any parameters\n");
    return;
  }

  // correct input
  //free all memory
  DynArray_map(oTokens, freeToken);
  DynArray_free(oTokens);

  //exit
  exit(0);  
}

/*--------------------------------------------------------------------*/
/*--------------------------------------------------------------------*/
/* Signal handling functions*/
int flag = 0;
/*handles Ctrl-C  */
void siginthandler(int iSignal){
  //ignore
  return;
}

/*--------------------------------------------------------------------*/
/* handles Ctrl-\ */

void sigquithandler(int iSignal){
  char msg[1024] = "\nType Ctrl-\\ again within 5 seconds to exit\n";
  char cmd[2] = "% ";
  if (flag == 1){
    exit(0);
  }
  //error case
  if (write(1,msg, sizeof(msg)) != sizeof(msg)){
    exit(0);
  }
  if (write(2,cmd,2) != 2){
    exit(0);
  }
  
  flag = 1;
  alarm(5);
  
  return;
}
/*--------------------------------------------------------------------*/
void sigalrmhandler(int iSignal){
  flag = 0;
  return;
}

/*--------------------------------------------------------------------*/
