import serial
ser = serial.Serial('COM8', 115200) 
if not ser.is_open:
    ser.open()
ser.write(1)
