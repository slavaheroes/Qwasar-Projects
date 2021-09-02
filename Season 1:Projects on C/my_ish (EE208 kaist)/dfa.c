/*--------------------------------------------------------------------*/
/* Shen Vyacheslav; ID: 20180878 */
/* Abdimazhit Asmir; ID: 20180823 */

/* dfa.c */

/* This file contains functions which are 
used to lexically analyze commandline  */

#include "dfa.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "dynarray.h"
#include <assert.h>
#define MAX_LINE_SIZE 1024
#define MAXARGS 128 //max size of arguments

/*--------------------------------------------------------------------*/
/* A DynArray consists of an array, along with its logical and
   physical lengths. */
struct DynArray
{
	/* The number of elements in the DynArray from the client's
	   point of view. */
	int iLength;
	
	/* The number of elements in the array that underlies the
	   DynArray. */
	int iPhysLength;
	
	/* The array that underlies the DynArray. */
	const void **ppvArray;
};

/*--------------------------------------------------------------------*/
/* A Token is either a string or pipe, expressed as a string. */

struct Token
{
   enum TokenType eType;
   /* The type of the token. */

   char *pcValue;
   /* The string which is the token's value. */
};
/*--------------------------------------------------------------------*/


/*--------------------------------------------------------------------*/
void freeToken(void *pvItem)

/* Free token pvItem. */

{
  struct Token *psToken = (struct Token*)pvItem;
   free(psToken->pcValue);
   free(psToken);
}

/*--------------------------------------------------------------------*/

static struct Token *makeToken(enum TokenType eTokenType,
   char *pcValue)

/* Create and return a Token whose type is eTokenType and whose
   value consists of string pcValue.  Return NULL if insufficient
   memory is available.  The caller owns the Token. */

{
   struct Token *psToken;

   psToken = (struct Token*)malloc(sizeof(struct Token));
   if (psToken == NULL)
      return NULL;

   psToken->eType = eTokenType;

   psToken->pcValue = (char*)malloc(strlen(pcValue) + 1);
   if (psToken->pcValue == NULL)
   {
      free(psToken);
      return NULL;
   }

   strcpy(psToken->pcValue, pcValue);

   return psToken;
}

/*--------------------------------------------------------------------*/
/*LexAnalysis on buffer,
argv is array of pointer which point to  argument string
DynArray is used to store those arguments*/

int parseline(char *buf, char **argv, DynArray_T oTokens){

  /* dfa states */
  enum LexState {IN_QUOTE, IN_WORD, IN_SPACE};
  enum LexState eState;

  /* variables declaration */
  
  int buf_index = 0; //index of buffer
  int token_index = 0; //index inside of token
  char curr; //current char
  char token[MAX_LINE_SIZE]; //temporarily stores token

  struct Token *psToken;
  
  int argc = 0; //number of arguments

  /* checking inputs*/
  assert(buf);
  assert(argv);
  assert(oTokens);

  
  /*Ignore empty lines*/
  if (strlen(buf) == 0) {return EMPTY_LINE;}

  /*start from state IN_SPACE */
  eState = IN_SPACE;

  
  while (1){
    curr = buf[buf_index++];

    //condition to break the loop
    if ((curr == '\0') || (curr == '\n')){
      if (eState == IN_WORD){
          token[token_index] = '\0'; //add trailing eof
	  /* Create word token*/
	  psToken = makeToken(TOKEN_WORD,token);

	  /* Checking for errors */
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }

	  //argument points to this string
          argv[argc++] = psToken->pcValue;
      }
      
      if (eState == IN_QUOTE){
          token[token_index] = '\0'; //add trailing eof
	  /* Create word token*/
	  psToken = makeToken(TOKEN_WORD,token);
	  /*-------Checking for errors--------*/
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	  /*---------------------------------------*/
	   //argument points to this string
          argv[argc++] = psToken->pcValue;
      }
      break;
    } 

    
    switch(eState){
      case IN_SPACE:
        if (curr == '"'){ //start of quote
          eState = IN_QUOTE;
          token_index = 0;
          break;
        }
        if (curr == '|'){ //pipe
          token[0] = curr;
          token[1] = '\0';
	  /* Create pipe token*/
	  psToken = makeToken(TOKEN_PIPE,token);
	  //error check
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	   //argument points to this string
          argv[argc++] = psToken->pcValue;
          break;
        }
        if (!isspace(curr)){ //start of word
          eState = IN_WORD;
          token_index = 0;
          token[token_index++] = curr;
        }
        break;

      case IN_WORD:
        if (curr == '"'){ //achieved quote
          eState = IN_QUOTE;
          break;
        }
        if (curr == '|'){ //pipe
          token[token_index] = '\0'; //add trailing eof
	  /* Create word token*/
	  psToken = makeToken(TOKEN_WORD,token);

	  //error check
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	   //argument points to this string
          argv[argc++] = psToken->pcValue;
	  	  
          token_index = 0;

	  //making new token
          token[0] = curr;
          token[1] = '\0';
	  /* Create pipe token*/
	  psToken = makeToken(TOKEN_PIPE,token);
	  //error check
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	  
	   //argument points to this string
          argv[argc++] = psToken->pcValue;

          eState = IN_SPACE;
          break;
        }
        if (!isspace(curr)){

	  //remain inside a word state
          eState = IN_WORD;
          token[token_index++] = curr;
	  break;
        }
        if (isspace(curr)){ //end of token and word state
          eState = IN_SPACE;
          token[token_index] = '\0'; //add trailing eof

	  
	  /* Create word token*/
	  psToken = makeToken(TOKEN_WORD,token);
	  //check for errors
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	   //argument points to this string
          argv[argc++] = psToken->pcValue;

	  
          token_index = 0;
        }
        break;
      
      case IN_QUOTE:
        if (curr == '"'){ //end of quote
	  //check conditions to make token
          if (isspace(buf[buf_index]) || (buf[buf_index] == '|')
	      || (buf[buf_index]=='\0')){
            eState = IN_SPACE;
            token[token_index] = '\0';
	  /* Create word token*/
	  psToken = makeToken(TOKEN_WORD,token);
	  //error check
          if (psToken == NULL)
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
          if (! DynArray_add(oTokens, psToken))
             {
               fprintf(stderr, "Cannot allocate memory\n");
               return FALSE;
             }
	  
	   //argument points to this string
          argv[argc++] = psToken->pcValue;
	  
          token_index = 0;
	  
          }
	  else{ //after quote is not space, hence in_word state
	    eState = IN_WORD;
	  }
        }
        else{
	  //continue quote token
          token[token_index++] = curr;
        }
        break;
    }
  }

  // quote is not finished
  if (eState == IN_QUOTE) return NOT_FINISHED_QUOTE;

  //set last argumen NULL
  argv[argc] = NULL;
  return TRUE;
  

}


/*--------------------------------------------------------------------*/
/* checks does tokens have pipe type*/

int isPiped(DynArray_T oTokens){
  //stores temporary token
  struct Token *psToken;

  /*checking input*/
  assert(oTokens);


  //iteration through elements of oTokens array
  
  for (int i = 0; i < oTokens->iLength; i++){
    psToken = (struct Token*) oTokens->ppvArray[i];
    //return one if it's token pipe
    if (psToken->eType == TOKEN_PIPE) return 1;
  }

  //pipe is not found, return false
  return 0;
  
}

/* This function analyzes argv, which has parsed commandline
It divides argv into commands according to appereance of pipe 
and store whole command in dynamic array*/

void parsecommands(char **argv, DynArray_T commands){

  return;


}


/*--------------------------------------------------------------------*/
/* Checks correctness of pipes*/

int CorrectPipe(char **argv){

  char *prev; //stores previous element in argv array
  
  /*checking input*/
  assert(argv);

  //checking first element is pipe

  if (strcmp(argv[0],"|") == 0){
    fprintf(stderr,"./ish: Missing command name \n");
    return 0;
  }
  
  //iteration through arguments and
  //checking cases of two consecutive pipes
  
  for (int i = 0; argv[i] != NULL; i++){
    if ((strcmp(argv[i],"|")) == 0){
      if ((strcmp(prev,"|")) == 0) {
	fprintf(stderr,
	    "./ish: Pipe or redirection destination not specified\n");
	return 0;
      }
    }

    prev = argv[i];
  }

  //checking cases when last element is pipe

  if ((strcmp(prev,"|"))==0) {
    fprintf(stderr,
	    "./ish: Pipe or redirection destination not specified\n");
    return 0;
  }


  //all error cases passed return 1

  return 1;

}
