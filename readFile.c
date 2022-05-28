// This program will read a text file and output its contents to the console

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


///////////////////////////////////////////////////////
//                CONSTANTS
///////////////////////////////////////////////////////
#define MAX_NAME 256

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

    // Makes sure there is no junk data when reading fileName or lineOfText later in the program
    char fileName[MAX_NAME] = { 0 };
    char lineOfText[MAX_NAME] = { 0 };

    FILE* fp1;
    int fileSize;

    if (argc == 1) {
        // Prompt the user for the name of the file if not given as a command line argument
        printf("\n");
        printf("Enter the name of the file you would like to print the text of to the console: ");

        // Read the user input in as fileName
        fgets(fileName, MAX_NAME - 1, stdin);

        /*

        strcspn() will count the number of characters until it hits the newline character. This makes it possible to replace
        the newline character with a 0 inside fileName in one line. strlen() could have also been used with multiple lines.
        I found the idea to use strcspn method for this particular use case at
        https://stackoverflow.com/questions/2693776/removing-trailing-newline-character-from-fgets-input

        */

        fileName[strcspn(fileName, "\n")] = 0;

        // open the file as fp1
        fp1 = fopen(fileName, "r");

        }

    else{
        // copy the argument entered by the user into fileName
        strncpy(fileName, argv[1], MAX_NAME - 1);

        // open the file as fp1
        fp1 = fopen(fileName, "r");
    }

    // Check to see if the file exists and can be opened. If not, exit program with -1.
    if (fp1 == NULL){
        printf("\n");
        printf("Error opening file. Make sure the name is correct and the file exists.\n");
        exit(-1);
        }

    printf("\nText contained within the file: \n\n");

    // While not the end of the file, store the line in lineOfText and print the line. Will print each line of the file.
    // Seen at https://riptutorial.com/c/example/29223/read-lines-from-a-file
    while (fgets(lineOfText, MAX_NAME, fp1)){

        printf("%s", lineOfText);

    }

    printf("\n");

    // Close the file we opened
    fclose(fp1);

}
