#include <stdint.h>
#include <stdio.h>
#include <serial.h>
#include <parsing.h>

int main(int argc, char** argv) {
	char *port_name_1 = argv[1]; // SBUS 
	char *port_name_2 = argv[2]; // Sabertooth1

	FILE *sbus; 
	FILE *sabertooth;

	// to store sbus packets
	uint8_t sbus_packet[15];

	// to store value of indiviual RC channel
	uint16_t *channel;

	// pwm value after interpolation 
	int pwm;

	// opening serial port for serial communication with Sabertooth and SBUS
	sbus = open_file(port_name_1, "rb");
	sabertooth = open_file(port_name_2, "w+");
	
	// read data from RC transmitter using sbus
	read_SBUS(sbus_packet, 1, sizeof(sbus_packet), sbus);

	// parsing sbus packet
	channel = parse_buffer(sbus_packet);

	// get pwm range for Sabertooth 1			 
	pwm = interpolation(channel[0]);		//  write								
							//  to
	// write data to Sabertooth 1			//  sabertooth	
	write_to_SB(sabertooth, "%d", pwm);		

	// closing all serial port 
	close_file(sbus);
	close_file(sabertooth);
}
