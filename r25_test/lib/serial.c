#include <serial.h>
#include <errno.h>

// Function to open the serial port
FILE* open_file(const char* portname, char* mode) {
	FILE* file_ptr = fopen(portname, mode);
	if (file_ptr == NULL) {
		printf("Error opening %s : %d\n", portname,
			errno);
		return NULL;
	}
	return file_ptr;
}

// Function to read data from SBUS
void read_SBUS(uint8_t* buffer, size_t size, size_t n, FILE* file_ptr) {
	int rc = fread(buffer, size, n, file_ptr);
	if(rc != n) printf("Error reading file : %d", errno);
}

// Function to write data to Sabertooth
void write_to_SB(FILE* file_ptr, char* fmt, ...)
{
	va_list args;
	va_start(args, fmt);
	int rc = vfprintf(file_ptr, fmt, args);
	va_end(args);
	if(rc < 0) printf("Error writting to file : %d", errno);
}

// Function to close the serial port
void close_file(FILE* file_ptr) { 
	fclose(file_ptr); 
}

