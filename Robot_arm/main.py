from lib.servo_control import set_servo_angle, create_servo

#--Servo setup--
base = create_servo(1, 50, 1150, 8600)
# joint1 = create_servo(2, 50, 1150, 8600)
# joint2 = create_servo(3, 50, 1150, 8600)
# joint3 = create_servo(1, 50, 1150, 8600)  #wrist roll
# joint4 = create_servo(1, 50, 1150, 8600)  #wrist up/down
# gripper = create_servo(1, 50, 1150, 8600)





#Calibrate

print("Servo to angle 0:")
set_servo_angle(base, 0)