import usb.core
import usb.util
import datetime
import requests

import readEvents

def send_event(time, data, userid):
    event = {   "userID": userid, 
                "appID": "dilongGamepad",
                "timestamp": str(time),
                "competition": "throwaway",
                "event": ''.join(str(buttonPressed) for buttonPressed in data) }
    resp = requests.post('http://localhost:5000/event', json=event)
    if resp.status_code != 201:
        print('sending of event failed')
    print('Sent ' + str(data))

def main():
    # find device ids with lsusb in terminal
    device = usb.core.find(idVendor=0x0079, idProduct=0x0011) # Dilong Gamepad
    if device is None:
        print('did not find an input device')
        return

    # make sure device is not busy and use default configuration
    device.reset()
    if device.is_kernel_driver_active(0) == True:
        device.detach_kernel_driver(0)
    device.set_configuration()

    # first endpoint
    endpoint = device[0][(0,0)][0]

    # read data
    data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    oldData = []
    startTime = datetime.datetime.now()
    while data[6] != 32:
        try:
            data = device.read(endpoint.bEndpointAddress,
                            endpoint.wMaxPacketSize)
            # send events when buttons are pressed and when they are releasesed 
            if oldData != data:
                time = datetime.datetime.now() - startTime
                buttonData = readEvents.dilongGamepadArrayToButtons(data)
                send_event(time, buttonData, 0)
            oldData = data

        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                continue
    

if __name__ == '__main__':
  main()
