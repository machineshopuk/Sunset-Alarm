from machine import I2C, Pin, PWM
from Suntime import Sun
from time import gmtime, sleep, time
from ds1307 import DS1307

buzzer = PWM(Pin(11))
buzzer.freq(800)

button = Pin(26, Pin.IN)
led = Pin(13, Pin.OUT)

# DS3231 I2C address
I2C_ADDR = 0x68

# Initialize I2C (adjust pin numbers if necessary)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
ds1307 = DS1307(addr=I2C_ADDR, i2c=i2c)

################################ Clock Setup Process ############################
# Set the location of the clock by entering the Latitude and Longitude here:
LATITUDE = 51.5072
LONGITUDE = 0.1276

# Set the date and time on the digital clock
# change these values to suit the next minute
Year = 2024
Month = 10
Day = 10
Hour = 12
Minute = 34
Second = 00
# do not change this line
newTime = (Year, Month, Day, Hour, Minute, Second, 4, 271, 0)
# uncomment the line below, this will set the new date and time 
# ds1307.datetime = newTime
# run this file on the clock, then comment out the line above to prevent the time changing again


# Function to convert BCD to decimal
def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

# Function to convert decimal to BCD
def dec_to_bcd(dec):
    return (dec // 10) * 16 + (dec % 10)


TIMEZONE_DIFFERENCE = 0
sun = Sun(LATITUDE, LONGITUDE, TIMEZONE_DIFFERENCE + 1)



ds1307.halt = False

AlarmedToday = 0
todaysDate = ds1307.datetime[2]
# Continuously read and print the time
while True:
    #year, month, day, hours, minutes, seconds = read_time()
    #print(f"Time: {year}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    timeNow = ds1307.datetime
    timeNowWithoutSeconds = (timeNow[0],timeNow[1],timeNow[2],timeNow[3],timeNow[4])
    sunset = sun.get_sunset_time(timeNow)
    print("Time:", timeNowWithoutSeconds, " Sunset:", sunset)
    if not AlarmedToday:
        if timeNowWithoutSeconds == sunset:
            AlarmedToday = 1
            while(button.value()):
                print("sunset!!!!")
                buzzer.duty_u16(1<<15)
                sleep(0.3)
                if not button.value():
                    buzzer.duty_u16(0)
                    break
                buzzer.duty_u16(0)
                sleep(0.3)
    if todaysDate != timeNow[2]:
        print("New day")
        todaysDate = timeNow[2]
        AlarmedToday = 0
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(0.8)
