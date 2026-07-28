import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pins for stepper motor
motor_channel = (29, 31, 33, 35)

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_channel, GPIO.OUT)

# Step sequence for full-step mode (Clockwise)
step_sequence = [
    (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH),
    (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW),
    (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
    (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
]

# Function to move motor in given direction
def rotate_motor(direction):
    sequence = step_sequence if direction == 'c' else list(reversed(step_sequence))

    for _ in range(512):  # 512 steps for ~360° rotation
        for step in sequence:
            GPIO.output(motor_channel, step)
            sleep(0.002)  # Speed control (lower value = faster rotation)


try:
    while True:
        motor_direction = input("Select direction (c=clockwise, a=anticlockwise, q=quit): ").strip().lower()
        if motor_direction == 'q':
            print("Motor stopped.")
            break
        elif motor_direction in ['c', 'a']:
            rotate_motor(motor_direction)
        else:
            print("Invalid input! Please enter 'c', 'a', or 'q'.")
except KeyboardInterrupt:
    print("\nMotor stopped by user.")
finally:
    GPIO.cleanup()