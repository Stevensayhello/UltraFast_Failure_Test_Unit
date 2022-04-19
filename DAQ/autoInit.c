// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

void getstring(char str[]);
void send_cmd(int sock, char* command);
void receive_cmd(int sock, int byte);

int main(int init)
{
	int sock = 0, valread;
	struct sockaddr_in serv_addr;
	char detect;
	char restart;
	char buffer[32] = {0};
	int PORT = 8081;
	printf("TCP Command Interface for ZCU111\n");
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

	printf("Start Initialization:");
	if(init)
	{
		sleep(1);
		send_cmd(sock, "\r\n\0");
		sleep(1);
		send_cmd(sock, "TermMode 0\r\n\0");
		sleep(1);
		send_cmd(sock, "disconnect\r\n\0");
		printf("\nRestart the Data Server and then press any key to continue.\n");
		while(!getchar());
		sleep(1);
		main(0);
	}
	else
	{
		sleep(1);
		send_cmd(sock, "\r\n\0");
		sleep(1);
		send_cmd(sock, "TermMode 0\r\n\0");
		sleep(1);
		send_cmd(sock, "Version\r\n\0");
		sleep(1);
		receive_cmd(sock, 32);
		sleep(1);
		send_cmd(sock, "RfdcVersion\r\n\0");
		sleep(1);
		receive_cmd(sock, 32);
	}

	char Sampling_Rate;
	while(1)
	{
		printf("Please Choose ADC Sampling Rate: (Ms/s)\n");
		printf("A - 1024	B - 2048	C - 3194	D - 3900\n");
		while(((detect = getchar()) != '\n') && (Sampling_Rate != EOF))
		{
			if(detect != '\n')
				Sampling_Rate = detect;
		}
		if(Sampling_Rate == 'A' || Sampling_Rate == 'a')
		{
			printf("ADC Sampling Rate = 1024Ms/s\n");
			send_cmd(sock, "DynamicPLLConfig 0 0 1 245.760000 1024.000000\r\n\0");
			sleep(1);
			send_cmd(sock, "SetFabClkOutDiv 0 0 2\r\n\0");
			sleep(1);
		}
		else if(Sampling_Rate == 'B' || Sampling_Rate == 'b')
		{
			printf("ADC Sampling Rate = 2048Ms/s\n");
			send_cmd(sock, "DynamicPLLConfig 0 0 1 245.760000 2048.000000\r\n\0");
			sleep(1);
			send_cmd(sock, "SetFabClkOutDiv 0 0 2\r\n\0");
			sleep(1);
		}
		else if(Sampling_Rate == 'C' || Sampling_Rate == 'c')
		{
			printf("ADC Sampling Rate = 3194Ms/s\n");
			send_cmd(sock, "DynamicPLLConfig 0 0 1 245.760000 3194.000000\r\n\0");
			sleep(1);
			send_cmd(sock, "SetFabClkOutDiv 0 0 2\r\n\0");
			sleep(1);
		}
		else if(Sampling_Rate == 'D' || Sampling_Rate == 'd')
		{
			printf("ADC Sampling Rate = 3900Ms/s\n");
			send_cmd(sock, "DynamicPLLConfig 0 0 1 245.760000 3900.000000\r\n\0");
			sleep(1);
			send_cmd(sock, "SetFabClkOutDiv 0 0 2\r\n\0");
			sleep(1);
		}

		printf("\n\nSystem Ready.\n");
		printf("Press any key to start acquiring data.\n");
		while(!getchar());
	
		printf("Start Acquiring Data.\n");
		send_cmd(sock, "SetLocalMemSample 0 0 0 8192\r\n\0");
		printf("...");
		sleep(1);
		send_cmd(sock, "LocalMemInfo 0\r\n\0");
		printf("...");
		sleep(1);
		send_cmd(sock, "LocalMemTrigger 0 0 8192 0x0001\r\n\0");
		printf("...");
		sleep(1);
		printf("\n\nData Ready.\n");
		printf("Use Data Server to Load the Data to .csv\n");
		printf("Press C to enter CMD Interface. Or press else key to Start Again\n");
		while(((detect = getchar()) != '\n') && (restart != EOF))
		{
			if(detect != '\n')
				restart = detect;
		}
		if(restart == 'C' || restart == 'c')
			break;
	}


	while(1)
	{
		char readorwrite;
		int disconnect = 0;
		printf("[CMD]Read or Write Operation (D for Disconnect):[R/W/D]");
		while(((detect = getchar()) != '\n') && (readorwrite != EOF))
		{
			if(detect != '\n')
				readorwrite = detect;
		}
		if(readorwrite == 'R' || readorwrite == 'r')
		{
			valread = read(sock, buffer, 32);
			printf("%s\n",buffer );
		}
		else if(readorwrite == 'D' || readorwrite == 'd')
		{
			char* command = "disconnect\r\n\0";
			send_cmd(sock, command);
			main(0);
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
				send_cmd(sock, command);
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

void send_cmd(int sock, char* command)
{
	send(sock, command, strlen(command), 0);
	printf("[Socket]Command Sent: %s", command);
}

void receive_cmd(int sock, int byte)
{
	char* buffer;
	buffer = (char*) malloc(byte*sizeof(char));
	read(sock, buffer, byte);
	printf("%s\n",buffer);
}