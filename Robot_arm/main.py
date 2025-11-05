from Robot_arm.servo_control import set_servo_angle, create_servo
from time import sleep
import network
import socket

#--Servo setup--
base = create_servo(1, 50, 1150, 8600)
# joint1 = create_servo(2, 50, 1150, 8600)
# joint2 = create_servo(3, 50, 1150, 8600)
# joint3 = create_servo(1, 50, 1150, 8600)  #wrist roll
# joint4 = create_servo(1, 50, 1150, 8600

#--Wifi--
def connect():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Ziggo3027886", "jjjtzx3kxnbRjueb")
    while wlan.isconnected() == False:
        print("Waiting to be connected")
        sleep(1)
    print("Connected")
    ip_info = wlan.ifconfig()  
    print("IP Address:", ip_info[0])  


#--Parse json recived
def parse_request(request_str):
    angles = {}
    
    # Find the query part of the URL
    query_start = request_str.find('?')
    if query_start == -1:
        return angles # No '?' found
        
    query_str = request_str[query_start+1:]
    
    # Split by '&' to get "j0=90", "j1=45", etc.
    commands = query_str.split('&')
    
    for cmd in commands:
        try:
            # Split "j0=90" into "j0" and "90"
            key, value = cmd.split('=')
            
            # Get the joint index (the '0' from 'j0')
            joint_index = int(key.lstrip('j'))
            # Get the angle
            angle_value = int(value)
            
            # Save to dictionary
            angles[joint_index] = angle_value
        except (ValueError, IndexError):
            # Ignore bad commands like "j=abc" or "foo"
            pass
            
    return angles

#--Start listening--
def web_control():
    connect()
    addr=socket.getaddrinfo("0.0.0.0",80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    while True:
        try:
            conn, address = s.accept()
            request = conn.recv(1024).decode("utf-8")
            request_line = request.split('\n')[0]
            #Get teh angles to set
            angles_to_set = parse_request(request_line)

            if angles_to_set:
                print("RECIVED VALUES: ", angles_to_set[0])

            # --Activate Servos--
            # if angles_to_set:
            #     print("Received angles:", angles_to_set)

            #     if 0 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 1 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 2 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 3 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 4 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 6 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])

            # Send a simple "OK" response back to the PC
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
            conn.close()
        
        except OSError as e:
            conn.close()
            print("Connection closed")

        
web_control()