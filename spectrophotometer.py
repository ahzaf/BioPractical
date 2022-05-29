print("Loading libraries")

import time
import board
import busio
import digitalio
import pwmio
from time import sleep
from adafruit_as7341 import AS7341
print("Connecting sensor")

i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
sensor = AS7341(i2c)

print("Setting up LEDs")

led1 = pwmio.PWMOut(board.GP19, frequency=1000)

#-----------------------------------------------------------

def setled1(brightness):
    led1.duty_cycle = brightness
    print(f"led 1 brightness set: {str(brightness)}")

def setled2(brightness):
    led2.duty_cycle = brightness
    print(f"led 2 brightness set: {str(brightness)}")

def set_gain(gain1):
    my_sensor.gain = gain1
    print(f"gain set: {str(gain1)}")

def setintegration(intTime):
    stepSize = 9999
    sensor.astep = stepSize
    sensor.atime = int(intTime*1000/(2.78*(stepSize+1)))
    print("Integration: "+str(((1+sensor.atime)*(1+sensor.astep)*0.00278))+" ms")

def read():
    print('starting read')
    wl_list = [415, 445, 480, 515, 555, 590, 630, 680]
    sensor_read = sensor.all_channels
    r_num = 0
    s_reads = []
    for i in sensor_read:
        print(f"wavelength: {wl_list[r_num]} nm = {sensor_read[r_num]}")
        s_reads.append(i)
        r_num = r_num + 1

def background():
    print('Place cuvette in device, fill with buffer and cover with cloth')
    print('waiting 10 seconds')
    time.sleep(10)
    print(sensor.all_channels[3])

def max_intensity():
    print('Place cuvette in device, fill with buffer and cover with cloth')
    print('waiting 10 seconds')
    setled1(16000)
    time.sleep(10)
    print(sensor.all_channels[3])

def time_course():
    setled1(16000)
    secs = 0
    time_df = []
    int_df_530 = []
    for i in range(31):
        time_df.append(secs)
        int_df_515.append(sensor.all_channels[3])
        print(time_df)
        secs += 10
        time.sleep(10)
    else:
        print('final values')
        print('Time array')
        print(time_df)
        print('515 nm readings')
        print(int_df_515)


#-----------------------------------------------------------

def run_commands(cmd):
    if cmd[:4] == "led1":
        setled1(int(cmd[4:]))
    elif cmd[:4] == "led2":
        setled2(int(cmd[4:]))
    elif cmd[:4] == "gain":
        set_gain(int(cmd[4:]))
    elif cmd[:4] == "read":
        read()
    elif cmd[:4] == "time":
        time_course()
    else:
        print('invalid input')

while True:
    command = input(">")
    run_commands(command)
