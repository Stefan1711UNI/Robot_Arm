from machine import Pin, PWM
from time import sleep

def create_servo(pin_num, freq=50, min_duty=1802, max_duty=7864):
    if isinstance(pin_num, Pin):
        pin = pin_num
    else:
        pin = Pin(pin_num)
    pwm = PWM(pin)
    pwm.freq(freq)
    return {'pwm': pwm, 'min_duty': int(min_duty), 'max_duty': int(max_duty), 'freq': int(freq)}

#Converts an angle to a duty cycle
def angle_to_duty(angle, min_duty, max_duty, angle_min=0, angle_max=180):
    #Check if valid angle
    if angle <= angle_min:
        return int(min_duty)
    if angle >= angle_max:
        return int(max_duty)
    
    span_angle = angle_max - angle_min
    span_duty = max_duty - min_duty
    duty = min_duty + ( (angle - angle_min) * span_duty ) / span_angle
    return int(round(duty))


def set_servo_angle(servo, angle):
    duty = angle_to_duty(angle, servo['min_duty'], servo['max_duty'])
    servo['pwm'].duty_u16(duty)


def stop_servo(servo):
    """Turn off PWM (cleanup)."""
    try:
        servo['pwm'].deinit()
    except Exception:
        # ignore if already deinitialized
        pass

#Test function to sweep servo
def sweep_servo(servo, start=0, end=180, step=1, delay=0.02):
    """
    Smoothly sweep servo from start to end (inclusive).
    step: positive int. If start > end, the function will still sweep by negating step.
    delay: pause between steps (seconds).
    """
    if step == 0:
        raise ValueError("step must be non-zero")
    if start < end:
        rng = range(start, end + 1, abs(step))
    else:
        rng = range(start, end - 1, -abs(step))
    for a in rng:
        set_servo_angle(servo, a)
        sleep(delay)


def main():
    base = create_servo(1)
    #Sets angle to 0 
    set_servo_angle(base, 0)
    #Break
    sleep(1)

    try:
        while True:
            #Sweep base from 0 to 180
            sweep_servo(base, 0, 180, step=2, delay=0.01)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        #Stops servo
        stop_servo(base)

main()