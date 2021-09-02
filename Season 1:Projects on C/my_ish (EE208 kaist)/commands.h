/*--------------------------------------------------------------------*/
/* commands.h                                                         */
/*--------------------------------------------------------------------*/
/* Shen Vyacheslav; ID: 20180878 */
/* Abdimazhit Asmir; ID: 20180823 */
                           
/*-----------------------------------
This file contains name of functions which executes four commands:

cd, setenv, unsetenv, exit
---------------------------------*/

#ifndef COMMANDS_INCLUDED
#define COMMANDS_INCLUDED

#include "dynarray.h"

void ch_dir(char **argv); //to change directories

void env_set(char **argv); //setenv

void env_unset(char **argv); //unsetenv

void call_exit(char **argv, DynArray_T oTokens); //exit command

void siginthandler(int iSignal); //to handle SIGINT signal

void sigquithandler(int iSignal); //to handle SIGQUIT signal

void sigalrmhandler(int iSignal); //to handle SIGALRM signal

#endif


