// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

void getstring(char str[]);

int main()
{
	char *filename		=	"ADC_VALUES.csv";

	int sock = 0, valread, i = 0;
	struct sockaddr_in serv_addr;
	char buffer[32] = {0};
	char detect;
	int frequency;
	double time;
	int PORT = 8082;
	printf("Data Interface for ZCU111\n");
	printf("Selected PORT# = %d & IP address(Default) = 192.168.1.3\n", PORT);

	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("\n Socket creation error \n");
		return -1;
	}
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	// Convert IPv4 and IPv6 addresses from text to binary form
	if(inet_pton(AF_INET, "192.168.1.3", &serv_addr.sin_addr)<=0)
	{
		printf("\nInvalid address/ Address not supported \n");
		return -1;
	}
	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{
		printf("\nConnection Failed \n");
		return -1;
	}

	while(1)
	{
		char readorwrite, Sampling_Rate;
		int disconnect = 0;
		printf("Press W for CMD Interface Write(Debug only)\n");
		printf("Press R for Read Operation (D for Restart):[R/D]");
		while(((detect = getchar()) != '\n') && (readorwrite != EOF))
		{
			if(detect != '\n')
				readorwrite = detect;
		}
		if(readorwrite == 'R' || readorwrite == 'r')
		{
			time = 0;
			i = 0;
			send(sock, "ReadDataFromMemory 0 0 32768 1\r\n\0", strlen("ReadDataFromMemory 0 0 32768 1\r\n\0"), 0);
			printf("Command Sent!\n");
			FILE *fp 		=	fopen(filename, "w");
			printf("Please re-Enter the Sampling Rate: (Ms/s)\n");
			printf("A - 1024	B - 2048	C - 3194	D - 3900\n");
			fprintf(fp, "Amplitude (LSB) - Signal,Time (us)\n");
			while(((detect = getchar()) != '\n') && (Sampling_Rate != EOF))
			{
				if(detect != '\n')
					Sampling_Rate = detect;
			}
			if(Sampling_Rate == 'A' || Sampling_Rate == 'a')
			{
				printf("ADC Sampling Rate = 1024Ms/s\n");
				frequency = 1024;
			}
			else if(Sampling_Rate == 'B' || Sampling_Rate == 'b')
			{
				printf("ADC Sampling Rate = 2048Ms/s\n");
				frequency = 2048;
			}
			else if(Sampling_Rate == 'C' || Sampling_Rate == 'c')
			{
				printf("ADC Sampling Rate = 3194Ms/s\n");
				frequency = 3194;
			}
			else if(Sampling_Rate == 'D' || Sampling_Rate == 'd')
			{
				printf("ADC Sampling Rate = 3900Ms/s\n");
				frequency = 3900;
			}


			int j;

			while(!((buffer[0] == 0x0D) && (buffer[1] == 0x0A)))
			{
				valread = read(sock, buffer, 32);
				if(!((buffer[0] == 0x0D) && (buffer[1] == 0x0A)))
				{
					for (j = 0; j < 32; j++)
					{
						//printf("i = %d has value = %02x\n", i, buffer[i]);
						if((j+1) % 2 != 0)
						{
							if(j < 16)
							{
								unsigned char boran = buffer[j];
								unsigned char gungor = buffer[j+1];
								
								unsigned int Boran_Gungor = gungor * 0x100 + boran;
								signed int Lukas_Lund;
								if((Boran_Gungor >> 15) == 1)
									Lukas_Lund = -1 * ((0xFFFF ^ Boran_Gungor) + 1);
								else
									Lukas_Lund = Boran_Gungor;

								printf("[%d] ADC has value decimal of %05d\n", i, Lukas_Lund);
								fprintf(fp, "%05d,%f\n", Lukas_Lund, time);
								time += 1.0/frequency;
								i++;
							}
						}
					}
					printf("\n");
				}
			}
			fclose(fp);
			printf("Data Acquisition Complete! Saved to ./ADC_VALUES.csv\n");
			memset(buffer, 0, sizeof(buffer));
		}
		else if(readorwrite == 'D' || readorwrite == 'd')
		{
			char* command = "disconnect\r\n\0";
			send(sock, command, strlen(command), 0);
			printf("[Socket]Command Sent: %s\n", command);
			main();
			return 1;
		}
		else if(readorwrite == 'W' || readorwrite == 'w')
		{
			char* command;
			char temp;
			int i = 0;
			size_t size = 20000;

			command = (char*) malloc(20000*sizeof(char));

			printf("Enter Command:\n");
			
			//scanf("%s", command);
			getstring(command);
			printf("Do you want to sent Comand: %s 	[Y/N]", command);
			int length;
			length = strlen(command);
			command[length] = 13;
			command[length + 1] = 10;
			command[length + 2] = '\0';

			while(((detect = getchar()) != '\n') && (readorwrite != EOF))
			{
			if(detect != '\n')
				temp = detect;
			}
			if(temp == 'y' || temp == 'Y')
			{
				send(sock, command, strlen(command), 0);
				printf("[Socket]Command Sent: %s\n", command);
			}

			else
				printf("Sent Canceled\n");
			
			memset(command, 0, strlen(command));
			free(command);
			if(disconnect == 1)
				return 1;
		}
		else
			printf("Wrong input\n");
	}
}

void getstring(char str[])
{
	int i = 0;
	int ch;
	while (((ch = getchar()) != '\n') && (ch != EOF))
	{
		str[i++] = ch;
	}
	str[i] = '\0';
}


