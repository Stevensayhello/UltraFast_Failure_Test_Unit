#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

int main()
{
    char *filename		=	"steven.txt";
	FILE *fp 		=	fopen(filename, "w");

    unsigned char a = 0xF1;
    unsigned char b = 0xFF;
    unsigned d  = b * 0x100 + a;

    printf ("%02x\n", a);
    printf ("%02x\n", b);
    printf ("%04x\n", d);

    
    signed int c = -1 * ((0xFFFF ^ d) + 1);
    fprintf(fp, "%d\n", 13);
    fprintf(fp, "%d\n", c);
    fprintf(fp, "%d\n", c);
    fprintf(fp, "%d\n", c);
    fprintf(fp, "%d\n", c);
    fprintf(fp, "%d\n", c);
    

    printf ("%04x\n", c);
    printf ("%d\n", c);

    fclose(fp);

   return 0;
}