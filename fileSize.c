// This program will inform the user how large in bytes a given file is

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

    // Makes sure there is no junk data when reading fileName later in the program
    char fileName[MAX_NAME] = { 0 };

    FILE* fp1;
    int fileSize;

    if (argc == 1) {
        // Prompt the user for the name of the file if not given as a command line argument
        printf("\n");
        printf("Enter the name of the file you would like to check the size of: ");

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
        printf("\nError opening file. Make sure the name is correct and the file exists.\n");
        exit(-1);
        }

    // Moves the cursor to the end of the file
    fseek(fp1, 0, SEEK_END);

    /*

    fileSize will hold the position in bytes where the cursor is.
    Since the cursor is now at the end of the file, it should give us the total number of bytes.
    https://www.systutorials.com/how-to-get-the-size-of-a-file-in-c/

    */

    fileSize = ftell(fp1);

    printf("\n");

    // Inform the user how large their file is
    printf("The file '%s' is %d bytes in size.\n\n", fileName, fileSize);

    // Close the file we opened
    fclose(fp1);

}
