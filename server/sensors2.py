#This Python script will obtain data from 5 different sensors connected to the Pi, store them in a data format, and store the data locally on the Pi database which may be used for transmission
#It will be ran automatically on Pi start up 
#5 sensors used in this project: Pi Camera, BNO085 IMU, Ultimate GPS Breakout, SGP40 Air Quality Sensor, and Temperature Sensor 

import sqlite3
import time
import board
import busio
import adafruit_gps
import os
import json
import serial
#from picamera2 import Picamera2
from adafruit_sgp40 import SGP40
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_ROTATION_VECTOR

# Initialize the database
def initialize_database():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist, including columns for GPS data
    cursor.execute('''

        CREATE TABLE IF NOT EXISTS SensorData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            accelerometer TEXT NOT NULL,
            gyroscope TEXT NOT NULL,
            quaternion TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Store data into the database (including GPS data)
def store_data_to_database(accel, gyro, quat):
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()

    # Serialize data into JSON strings
    accel_json = json.dumps({"x": accel[0], "y": accel[1], "z": accel[2]})
    gyro_json = json.dumps({"x": gyro[0], "y": gyro[1], "z": gyro[2]})
    quat_json = json.dumps({"i": quat[0], "j": quat[1], "k": quat[2], "real": quat[3]})

    # Insert data into the table
    cursor.execute('''
        INSERT INTO SensorData (timestamp, accelerometer, gyroscope, quaternion)
        VALUES (?, ?, ?, ?)
    ''', (time.strftime('%Y-%m-%d %H:%M:%S'), accel_json, gyro_json, quat_json))
    conn.commit()
    conn.close()

# Capture image from the camera and save it to a file
#def capture_image():
    # Define the directory to store images
    #image_dir = "/home/pi/sensor_images"
    #if not os.path.exists(image_dir):
        #os.makedirs(image_dir)

    # Generate a unique filename using the current timestamp
    #timestamp = time.strftime('%Y%m%d_%H%M%S')
    #image_filename = f"{timestamp}.jpg"
    #image_path = os.path.join(image_dir, image_filename)

    # Initialize the camera
    #picam2 = Picamera2()
    #picam2.start_preview()
    #time.sleep(2)  # Allow time for the camera to adjust
    #picam2.capture_file(image_path)

    #return image_path

# Main loop to read sensor data and store it
def main():
    initialize_database()

    # Initialize I2C and IMU sensor
    i2c = busio.I2C(board.SCL, board.SDA)

    while not i2c.try_lock():
        pass

    try:
        devices = i2c.scan()
        if not devices:
            print("No I2C devices found!")
        else:
            print("Found I2C devices at:", [hex(device) for device in devices])
    finally:
        i2c.unlock()

    bno = BNO08X_I2C(i2c, address=0x4A)
    bno.enable_feature(BNO_REPORT_ACCELEROMETER)
    bno.enable_feature(BNO_REPORT_GYROSCOPE)
    bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
    
    # Initialize Air Qual 
    sgp40 = SGP40(i2c, address=0x4B)

    # Initialize UART and GPS 
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    
    print("Starting data collection. Press Ctrl+C to stop.")
    try:
        while True:
            # Retrieve IMU data
            accel = bno.acceleration
            gyro = bno.gyro
            quat = bno.quaternion
            

            # Retrieve Air Qual data 
            voc_index = sgp40.measure_index()

            # Retrieve GPS data
            #gps.update()

            #if not gps.has_fix:
                #print("Waiting for fix...")
                #continue

            # GPS data
            #latitude = gps.latitude
            #longitude = gps.longitude

            #print(f"Latitude: {latitude:.6f} degrees")
            #print(f"Longitude: {longitude:.6f} degrees")
            print(f"Accelerometer: {accel}")
            print(f"Gyroscope: {gyro}")
            print(f"Quaternion: {quat}")
            print(f"VOC Index: {voc_index}")

            #image_path = capture_image()
            #print(f"Image saved to: {image_path}")

            # Store data in the database
            store_data_to_database(accel, gyro, quat, voc_index)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Data collection stopped.")

if __name__ == "__main__":
    main()
