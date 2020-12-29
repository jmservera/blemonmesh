import asyncio
import aioblescan as aiobs

# check sample code: https://github.com/frawau/aioblescan/blob/master/aioblescan/__main__.py

def my_process(data):
    ev=aiobs.HCI_Event()
    xx=ev.decode(data)

    print("Raw data: {}".format(ev.raw_data))
    print("decode: {}".format(xx))
    ev.show(0)



event_loop = asyncio.get_event_loop()

#First create and configure a raw socket
mysocket = aiobs.create_bt_socket(0)

fac=event_loop._create_connection_transport(mysocket,aiobs.BLEScanRequester,None,None)

conn,btctrl = event_loop.run_until_complete(fac)

btctrl.process=my_process

btctrl.send_scan_request()
try:
    # event_loop.run_until_complete(coro)
    event_loop.run_forever()
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    print('closing event loop')
    btctrl.stop_scan_request()
    command = aiobs.HCI_Cmd_LE_Advertise(enable=False)
    btctrl.send_command(command)
    conn.close()
    event_loop.close()


