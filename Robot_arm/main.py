from Robot_arm.servo_control import set_servo_angle, create_servo
from time import sleep
import network
import socket
import select

#--Servo setup--
base = create_servo(1, 50, 1150, 8600)
shoulder = create_servo(2, 50, 1150, 8600)
elbow = create_servo(3, 50, 1150, 8600)
wrist_joint = create_servo(4, 50, 1150, 7840)  #wrist up/down
gripper = create_servo(5, 50, 1150, 7840)
#joint4 = create_servo(1, 50, 1150, 7840)

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
    
    # # Find the query part of the URL
    # query_start = request_str.find('?')
    # if query_start == -1:
    #     return angles # No '?' found
        
    # query_str = request_str[query_start+1:]
    # #Removes 'HTTP/1.1' from query str
    # clean_query_str = query_str.split(' ')[0]

    # Split by '&' to get "j0=90", "j1=45", etc.
    commands = request_str.split('&')
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
    print("Listening:")
    while True:
        try:
            conn, address = s.accept()
            request = conn.recv(1024).decode("utf-8")
            request_line = request.split('\n')[0]
            #Get teh angles to set
            angles_to_set = parse_request(request_line)

            if angles_to_set:
                print("RECIVED VALUES: ", angles_to_set)

            # --Activate Servos--
            if angles_to_set:
                if 0 in angles_to_set:
                    set_servo_angle(base, angles_to_set[0])
                if 1 in angles_to_set:
                    set_servo_angle(shoulder, angles_to_set[1])
                if 2 in angles_to_set:
                    set_servo_angle(elbow, angles_to_set[2])
            #     if 3 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
            #     if 4 in angles_to_set:
            #         set_servo_angle(base, angles_to_set[0])
                if 5 in angles_to_set:
                    set_servo_angle(gripper, angles_to_set[5])

            # Send a simple "OK" response back to the PC
            conn.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\nOK')
            conn.close()
        
        except Exception as e:
            print(f"!!! LOOP CRASHED: {e} !!!")
            if 'conn' in locals(): 
                conn.close()
            print("Connection closed due to error")



def udp_control():
    connect()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(('0.0.0.0', 5000))
    except OSError:
        print("Port busy, resetting...")
        return
    print("Listening for UDP commands on Port 5000...")

    poller = select.poll()
    poller.register(s, select.POLLIN)

    while True:
        try:
            res = poller.poll(100)
            
            if res:
                data, addr = s.recvfrom(1024)
                message = data.decode('utf-8')
                angles_to_set = parse_request(message)

                # --Activate Servos--
                if angles_to_set:
                    print("RECIVED VALUES: ", angles_to_set)
                    if 0 in angles_to_set:
                        set_servo_angle(base, angles_to_set[0])
                    if 1 in angles_to_set:
                        set_servo_angle(shoulder, angles_to_set[1])
                    if 2 in angles_to_set:
                        set_servo_angle(elbow, angles_to_set[2])
                    if 3 in angles_to_set:
                        set_servo_angle(wrist_joint, angles_to_set[3])
                #     if 4 in angles_to_set:
                #         set_servo_angle(base, angles_to_set[0])
                    if 5 in angles_to_set:
                        set_servo_angle(gripper, angles_to_set[5])

                #constant
                #set_servo_angle(wrist_joint, 90)

        except Exception as e:
            print("Error:", e)


udp_control()

#test wrist
# for i in range(20):
#     print(i)
#     a = 90 + 60
#     set_servo_angle(shoulder, a)
#     sleep(0.3)