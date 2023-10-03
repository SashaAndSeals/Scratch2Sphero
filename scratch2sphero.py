import time
import threading
from scratchcloud import CloudClient, CloudChange
from spherov2 import scanner 
from spherov2.sphero_edu import SpheroEduAPI,EventType
from spherov2.types import Color
chars = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/()[]{}.,:;?!@#$%^&<>\|/`~=_ "'+"'"
def decode(intcode):
    code=str(intcode)
    decoded=""
    i=0
    for i2 in range(int(len(code)/2)):
        decoded+=chars[int(intcode[i])*10+int(intcode[i+1])-1]
        i+=2
    return decoded
def motor(droid,right,left,time):
    droid.raw_motor(right,left,time) 
def pixel(droid,x,y,r,g,b):
    droid.set_matrix_pixel(x,y,Color(r,g,b))  
def main():
    print("Looking for sphero...")
    toy = scanner.find_toy()
    print("Connecting to sphero...")
    with SpheroEduAPI(toy) as droid:
        print("Connected to sphero!")
        client = CloudClient(input("Username:"),input("Project ID:"))
        @client.event
        async def on_connect():
            print('Connected to scratch!')

        @client.event
        async def on_disconnect():
            print('Disconnected from scratch!')

        @client.event
        async def on_message(cloud: CloudChange):
            if cloud.name=="SEND":
                msg=decode(cloud.value)
                if msg.startswith("motor("):
                    msg=msg.replace("motor(","").replace(")","").split(",")
                    motor(droid,int(msg[0]),int(msg[1]),int(msg[2]))
                elif msg.startswith("pixel("):
                    msg=msg.replace("pixel(","").replace(")","").split(",")
                    pixel(droid,int(msg[0]),int(msg[1]),int(msg[2]),int(msg[3]),int(msg[4]))
        client.run(input("Password:"))
if __name__ == "__main__":
    main()
