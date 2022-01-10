#!/usr/bin/env python3

import serial
import sys

if len(sys.argv) != 3:
    print(sys.argv[0] + " <serial port> <command>")
    print("\nvalid commands:")
    print("status")
    print("play (always side a)")
    print("playa")
    print("playb")
    print("pause")
    print("stop")
    print("rwd")
    print("fwd")
    print("eject")
    sys.exit(1)

ser = serial.Serial(sys.argv[1], 9600, timeout=3)
cmd = sys.argv[2]
if cmd == "play" or cmd == "playa":
    ser.write(b'\x01')
elif cmd == "playb":
    ser.write(b'\x02')
elif cmd == "pause":
    ser.write(b'\x05')
elif cmd == "stop":
    ser.write(b'\x06')
elif cmd == "rwd":
    ser.write(b'\x04')
elif cmd == "fwd":
    ser.write(b'\x03')
elif cmd == "eject":
    ser.write(b'\x08')
elif cmd == "status":
    ser.write(b'\x0b') #begin sending status
    r = ser.read() #ack
    if not r or r[0] != 0x15:
        print("no acknowledge from deck")
        sys.exit(1)
    s = ser.read()
    if not s:
        print("no status from deck")
        sys.exit(1)
    if s[0] == 10:
        print("playing side a")
    elif s[0] == 12:
        print("paused side a")
    elif s[0] == 20:
        print("playing side b")
    elif s[0] == 22:
        print("paused side b")
    elif s[0] == 30:
        print("fast forwarding")
    elif s[0] == 40:
        print("rewinding")
    elif s[0] == 50:
        print("stopped side a")
    elif s[0] == 52:
        print("stopped side b")
    elif s[0] == 60:
        print("no tape")
    else:
        print("unknown deck status: " + str(s[0]))
    ser.write(b'\x0c') #stop sending status
    r = ser.read() #ack
    if not r or r[0] != 0x16:
        print("no acknowledge from deck after status request")
        sys.exit(1)
    sys.exit(0)
else:
    print("unknown command. execute without arguments to see usage")
    sys.exit(1)

print("command sent")
sys.exit(0)