from Robot_arm.servo_control import set_servo_angle, create_servo
from time import sleep

#--Servo setup--
base = create_servo(1, 50, 1150, 8600)
# joint1 = create_servo(2, 50, 1150, 8600)
# joint2 = create_servo(3, 50, 1150, 8600)
# joint3 = create_servo(1, 50, 1150, 8600)  #wrist roll
# joint4 = create_servo(1, 50, 1150, 8600


print("Servo to angle 0:")
set_servo_angle(base, 0)
sleep(4)
print("Servo to angle 180:")
set_servo_angle(base, 180)
sleep(4)
print("Done")