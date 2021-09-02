/*--------------------------------------------------------------------*/
/* Shen Vyacheslav; ID: 20180878 */
/* Abdimazhit Asmir; ID: 20180823 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dfa.h"
#include "commands.h"
#include "dynarray.h"

#include <assert.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <signal.h>

/*--------------------------------------------------------------------*/
#define MAX_LINE_SIZE 1024 
#define MAXARGS 128 //max size of arguments


/*--------------------------------------------------------------------*/
/* Evaluate command and arguments with pipes */
void eval_pipe(char **argv){
  char *commands[MAXARGS][MAXARGS]; //2d list to store whole commands

  int argc=0; // to iterate through arguments

  int cmd = 0; //number of commands - 1

  int cmd_argc = 0; //number of argument for a command
  
  /* dividing argv into commands seperated by pipes */
  while(1){
    
    if (argv[argc] == NULL){ //last element of argv
      commands[cmd][cmd_argc] = NULL; //set last argument of cmd to null
      commands[cmd+1][0] = NULL;
      break;
    }

    if (strcmp(argv[argc], "|") ==0){ //end of command before pipe
      commands[cmd][cmd_argc] = NULL; //last argument of cmd is null
      cmd++; //number of commands increased
      cmd_argc = 0; //for counting argc of new command
      argc++; //go to next argument
      continue;
    }

    commands[cmd][cmd_argc] = argv[argc];
    cmd_argc++;
    argc++;
  }

  /* executing all commands and creating pipes */
  /* numbet of pipes = cmd; */
  
  int fd[2]; //for pipes
  pid_t pid;
  int fd_in = 0;
  int status;
  
  for (int j = 0; j<=cmd; j++){
    //open pipes
    if (pipe(fd) < 0){
      fprintf(stderr, "Pipe error: %s\n", strerror(errno));
      exit(1);
    }

    //clear all i/o before fork
    if (fflush(NULL) != 0){
    fprintf(stderr, "flush error: %s\n", strerror(errno));
    return;
     }

    //in child process
    if ((pid = fork()) == 0){
      if (dup2(fd_in,0)<0){
	fprintf(stderr, "dup2 error: %s\n", strerror(errno));
	exit(1);
      }

      
      if ( j != cmd){ //if not last command
	if (dup2(fd[1],1)<0){
	  fprintf(stderr, "dup2 error: %s\n", strerror(errno));
	  exit(1);
	}
      }
      

      close(fd[0]); //close read end
      
      if (execvp(commands[j][0], commands[j])<0){
	fprintf(stderr,"%s: %s\n", commands[j][0], strerror(errno));
	exit(1);
      }
      
    }
    //error in fork
    if (pid == -1){
      fprintf(stderr, "fork error: %s\n", strerror(errno));
      exit(1);
    }
    //parent process
      /*Parent waits for child */

  if (waitpid(pid, &status, 0) < 0)
    fprintf(stderr, "waitpid error: %s\n", strerror(errno));

  close(fd[1]); //close write end
  fd_in = fd[0]; //change input end
  }
}

/*--------------------------------------------------------------------*/
/* evaluates command line which must be executed by shell*/

void evaluate(char *cmdline){
  char *argv[MAXARGS]; //stores arguments
  char buf[MAX_LINE_SIZE]; //holds cmdline

  int dfa_out; // output value of dfa
  
  pid_t pid;
  int status;

  DynArray_T oTokens; //dynamic array
  oTokens = DynArray_new(0);
  //check for error
  if (oTokens == NULL)
  {
    fprintf(stderr, "Cannot allocate memory\n");
    exit(EXIT_FAILURE);
  }
  
  assert(cmdline);
  strcpy(buf, cmdline); //copy cmdline to buf
  
  dfa_out = parseline(buf, argv, oTokens);

  /*Handle error outcomes*/
  if (argv[0] == NULL) return;

  if (dfa_out == FALSE){
    /*failed memory allocation, exit*/
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    exit(1);
  }
  
  
  if (dfa_out == EMPTY_LINE){ //cmdline is empty
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    return; //empty line, simply ignore it
  }

  if (dfa_out == NOT_FINISHED_QUOTE){
    //not finished quote; print error message
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    fprintf(stderr, "./ish: Could not find quote pair\n");
    return; //take new input
  }

  
  /* parseline returned TRUE */
  /* Checking for piper and their correctness*/

  if (isPiped(oTokens) == 1){
    if (CorrectPipe(argv) == 1){
      //everything ok with argv, evaluate pipes
      eval_pipe(argv);
    }

    //wrong cmdline with pipes, ignore it
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    return;   
  }
  
  
  /*four commands we have to build */
  /*cd command */
  if (strcmp(argv[0], "cd")==0){
    ch_dir(argv);

    // free memory
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    return;
  }
  /* setenv command*/
  if (strcmp(argv[0], "setenv")==0){

    
    env_set(argv);
    // free memory
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    return;
  }
  /* unsetenv command */
  if (strcmp(argv[0], "unsetenv")==0){    
    env_unset(argv);

    // free memory
    DynArray_map(oTokens, freeToken);
    DynArray_free(oTokens);
    
    return;
  }
  
  /* exit command */
  if (strcmp(argv[0], "exit")==0){
    call_exit(argv, oTokens);
    return;
  }

  /*case when we deal with other build-in commands*/

  //clear all i/o before fork
  if (fflush(NULL) != 0){
    fprintf(stderr, "flush error: %s\n", strerror(errno));
    return;
  }
  if ((pid = fork()) == 0) { /*in child process*/

    //ignore signal handlers
    signal(SIGINT, SIG_DFL);
    signal(SIGQUIT, SIG_DFL);
    if (execvp(argv[0], argv) < 0){
      fprintf(stderr,"%s: %s.\n", argv[0], strerror(errno));

      // free memory before exit
      DynArray_map(oTokens, freeToken);
      DynArray_free(oTokens);
      exit(1);
    }
    
    //error in fork free memory and exit
    if (pid == -1){
      fprintf(stderr, "fork error: %s\n", strerror(errno));
      DynArray_map(oTokens, freeToken);
      DynArray_free(oTokens);
      exit(1);
    }
    
    // free memory in child process
     DynArray_map(oTokens, freeToken);
     DynArray_free(oTokens);
     exit(0);
  }

  /*Parent waits for child */

  if (waitpid(pid, &status, 0) < 0)
    fprintf(stderr, "waitpid error: %s\n", strerror(errno));

      // free memory
  DynArray_map(oTokens, freeToken);
  DynArray_free(oTokens);
  
  return;
    

}



/*--------------------------------------------------------------------*/
/* Read ishrc file and evaluate it */

void eval_ish(){

  /*get current diretory */
  char curr_dir[MAX_LINE_SIZE];

  //error in getting current directory
  if (getcwd(curr_dir, sizeof(curr_dir)) == NULL) {
    fprintf(stderr, "getcdw() error: %s\n", strerror(errno));
    return;
  }
  /*change dir to home directory*/
   if (chdir(getenv("HOME")) < 0){
      fprintf(stderr, "ish: %s\n", strerror(errno));
      return;
    }
  
  char *filename = ".ishrc";
  
  FILE *fp; //stores file pointer
  char cmdline[MAX_LINE_SIZE]; //stores command

  // test existence of a file

  if (access(filename, F_OK) == -1) {//not exist
    //change directory to initial directory
    if (chdir(curr_dir) < 0){
      fprintf(stderr, "Chdir() error: %s\n", strerror(errno));
      exit(0);
    }
    
    return;
   }

  
  //file exists and open it
  fp = fopen(filename, "r");
  
  //check fopen return value
  
  if (fp == NULL){
    fprintf(stderr, "Error in opening file: %s\n", strerror(errno));
    return;
  }

    //change directory to initial directory
  if (chdir(curr_dir) < 0){
      fprintf(stderr, "Chdir() error: %s\n", strerror(errno));
      exit(0);
   }
  //start reading it
  while (fgets(cmdline, sizeof(cmdline), fp)){
    
        /* print and evaluate */
    printf("%c %s",'%', cmdline);
    evaluate(cmdline); 
  }

  //successfully finished
  return;

}

/*--------------------------------------------------------------------*/
int main()
{
        /* Signal handling*/
  if (signal(SIGINT, siginthandler)== SIG_ERR){
    fprintf(stderr,"signal error: %s", strerror(errno));
  };
  if (signal(SIGQUIT, sigquithandler)==SIG_ERR){
    fprintf(stderr,"signal error: %s", strerror(errno));
  };
  
  if (signal(SIGALRM, sigalrmhandler)==SIG_ERR){
    fprintf(stderr,"signal error: %s", strerror(errno));
  };

  
  char cmdline[MAX_LINE_SIZE]; //for storing command line

  /* Initialize shell by evaluating ishrc file*/
  eval_ish();
  
  while (1){

    /* Read */
    printf("%c ",'%');
    fgets(cmdline, MAX_LINE_SIZE, stdin);
    
   if (feof(stdin)) // if EOF, then exit
      exit(0);

    /*Evaluate the command line  */
    evaluate(cmdline);    
  }
  
  return 0;
}
