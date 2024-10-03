# !!!DO NOT RUN THIS FILE!!!
import random


def generate_sbus_packet():
    # SBUS packet structure
    packet = [0x0F]  # Start byte

    # Generate random channel values (11-bit) for 16 channels
    channels = [random.randint(0, 0x07FF) for _ in range(16)]

    # Pack the channel data into the 22 data bytes
    data_bytes = []
    for i in range(0, 16, 2):
        data_bytes.append(channels[i] & 0xFF)  # Lower 8 bits of channel i
        data_bytes.append(
            ((channels[i] >> 8) & 0x07) | ((channels[i + 1] & 0x1F) << 3)
        )  # Upper 3 bits of channel i and lower 5 bits of channel i+1
        data_bytes.append((channels[i + 1] >> 5) & 0xFF)  # Upper 8 bits of channel i+1

    # Fill in the packet
    packet.extend(data_bytes)
    packet.append(0x00)  # Flags byte (no failsafe or frame lost flags set)
    packet.append(0x00)  # End byte

    return bytes(packet)

def SBus_DecodeFrame(packet):
    channel = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    channel[0] = ((packet[2] & 0x07) << 8) | packet[1]
    channel[1] = ((packet[3] & 0x3F) << 5) | ((packet[2] & 0xF8) >> 3)
    channel[2] = ((packet[5] & 0x01) << 10) | (packet[4] << 2) | ((packet[3] & 0xC0) >> 6)
    channel[3] = ((packet[6] & 0x0F) << 7) | ((packet[5] & 0xFE) >> 1)
    channel[4] = ((packet[7] & 0x7F) << 4) | ((packet[6] & 0xF0) >> 4)
    channel[5] = ((packet[9] & 0x03) << 9) | (packet[8] << 1) | ((packet[7] & 0x80) >> 7)
    channel[6] = ((packet[10] & 0x1F) << 6) | ((packet[9] & 0xFC) >> 2)
    channel[7] = (packet[11] << 3) | ((packet[10] & 0xE0) >> 5)
    channel[8] = ((packet[13] & 0x03) << 8) | packet[12]
    channel[9] = ((packet[14] & 0x3F) << 5) | ((packet[13] & 0xF8) >> 3)
    channel[10]  = ((packet[16] & 0x01) << 10) | (packet[15] << 2) | ((packet[14] & 0xC0) >> 6)
    channel[11]  = ((packet[17] & 0x0F) << 7) | ((packet[16] & 0xFE) >> 1)
    channel[12]  = ((packet[18] & 0x7F) << 4) | ((packet[17] & 0xF0) >> 4)
    channel[13]  = ((packet[20] & 0x03) << 9) | (packet[19] << 1) | ((packet[18] & 0x80) >> 7)
    channel[14]  = ((packet[21] & 0x1F) << 6) | ((packet[20] & 0xFC) >> 2)
    channel[15]  = (packet[22] << 3) | ((packet[21] & 0xE0) >> 5)

    return channel

def interpolation(ch):
    # Apply the interpolation formula
    return round(1 + (ch - 0) * (127 - 1) / (2047 - 0))

        
        
def main():    
  for i in range(1,5):
    f1 = "sbus_data[%d]"%(i-1)
    f2 = "expected[%d]"%(i-1)
    file1 = open(f1, "bw")
    file2 = open(f2, "w")
    
    sbus_packet = generate_sbus_packet()
    channels = SBus_DecodeFrame(sbus_packet)
    value = interpolation(channels[0])

    file1.write(sbus_packet)
    file2.write(str(value))
    
    file1.close()
    file2.close()


if __name__ == "__main__":
    main()
