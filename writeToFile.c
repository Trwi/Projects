// This program will write text input by the user to a file named outFile.txt

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


///////////////////////////////////////////////////////
//                CONSTANTS
///////////////////////////////////////////////////////
#define MAX_TEXT 256

///////////////////////////////////////////////////////
//               typedefs and structures
///////////////////////////////////////////////////////

///////////////////////////////////////////////////////
//               globalVariables
///////////////////////////////////////////////////////

///////////////////////////////////////////////////////
//               FunctionPrototypes
///////////////////////////////////////////////////////


///////////////////////////////////////////////////////
//                FunctionPrototypes
///////////////////////////////////////////////////////


/*****************************************************
 *
 *  Function:  main()
 *
 *  Parameters:
 *
 *      argc - main parameter for argument count
 *      argv - main parameter for argument values
 *
******************************************************/

int main(int argc, char** argv){

    FILE* fp1;                      // File Pointer
    char userText[MAX_TEXT];        // Will contain the text entered by the user
    char lineOfText[MAX_TEXT];      // Will be used to read back the text written to the file
    char* ans = "yes";              // User prompt to continue writing to the file
    char userAns[5];                // Will hold user's answer
    int comparison;                 // Will hold the return value of strcmp()

    // Open and create outFile.txt if it does not exist. w+ allows us to read and write to the file
    fp1 = fopen("outFile.txt", "w+");

    // Error handling in case the file cannot be created
    if (fp1 == NULL){
        printf("Error creating file.\n");
        exit(-1);
        }

    // Do while the user wants to continue to write text to the file
    do{

        printf("Enter the text you would like to write to the file: ");
        fgets(userText, MAX_TEXT - 1, stdin);
        printf("\n");

        fprintf(fp1, "%s", userText);

        printf("Would you like to add another line of text? Enter 'yes' or 'no': ");

        fgets(userAns, 4, stdin);

        int i = 0;

        // Converts the user's answer to lowercase if they use uppercase for any of the letters
        while( userAns[i] ) {
            userAns[i] = tolower(userAns[i]);
            i++;
        }

        printf("\n");

        fflush(stdin);

    } while (strcmp(ans, userAns) == 0); 

    // Reset the cursor to the beginning of the file to read the newly written contents back to the user
    fseek(fp1, 0, SEEK_SET);

    printf("Created the file outFile.txt and wrote the following lines of text: \n\n");

    // Print each line of text in the text file until end of file is reached
    while (fgets(lineOfText, MAX_TEXT, fp1)){

        printf("%s", lineOfText);

    }

    printf("\n\nGoodbye!\n");

    // Close the file we created/opened
    fclose(fp1);

    return 0;
}
