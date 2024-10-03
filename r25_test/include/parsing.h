#include <stdint.h>

// function to parse sbus channel
uint16_t *parse_buffer(uint8_t buff[]);

// interpolate channel and return pwm value 
int interpolation(uint16_t ch);
