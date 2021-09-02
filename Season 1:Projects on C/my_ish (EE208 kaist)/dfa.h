/*--------------------------------------------------------------------*/
/* dfa.h                                                         */
/*--------------------------------------------------------------------*/
/* Shen Vyacheslav; ID: 20180878 */
/* Abdimazhit Asmir; ID: 20180823 */

/*-----------------------------------
This file contains name of function for string processing
---------------------------------*/

#ifndef DFA_INCLUDED
#define DFA_INCLUDED

#include "dynarray.h"
/* Return values for parseline function*/
enum {FALSE, TRUE, NOT_FINISHED_QUOTE, EMPTY_LINE};

/* Token type */
enum TokenType {TOKEN_PIPE, TOKEN_WORD};


/* This function lexically analyzes buf, make tokens
and successfully parsed tokens are stored in argv[]
srting array*/

int parseline(char *buf, char **argv, DynArray_T oTokens);

/* This function analyzes argv, which has parsed commandline
It divides argv into commands according to appereance of pipe 
and store whole command in dynamic array*/

void parsecommands(char **argv, DynArray_T commands);

/*frees token */
void freeToken(void *pvItem);

/* checks existence of Pipe token*/
int isPiped(DynArray_T oTokens);

/* check correctness of command with pipe*/
int CorrectPipe(char **argv);

#endif



