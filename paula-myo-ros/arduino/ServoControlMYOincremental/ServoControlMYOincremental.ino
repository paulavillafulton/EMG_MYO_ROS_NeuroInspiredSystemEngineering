/*
 * rosserial Servo Control Example
 *
 * This sketch demonstrates the control of hobby R/C servos
 * using ROS and the arduiono
 * 
 * For the full tutorial write up, visit
 * www.ros.org/wiki/rosserial_arduino_demos
 *
 * For more information on the Arduino Servo Library
 * Checkout :
 * http://www.arduino.cc/en/Reference/Servo
 */


#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Int32.h>

//int pose;                                    // variable to store the myo position
int angle = 0;                               // variable to store the servo position

ros::NodeHandle nh;                          //instantiate the node handle

Servo servo;                                 // key servo specific area - create servo object to control servo

void callback(const std_msgs::Int32& pose_msg){ // define what to do with pose_msg

  if (pose_msg.data == 0){
    for(angle = 0; angle < 90; angle += 1){  // goes from 0 degrees to 180 degrees // in steps of 1 degree 
      servo.write(90);                       // tell servo to go to position 0 // depending on the orientation of the motor change to 180
      delay(10);                             // waits 15ms for the servo to reach the position 
    }

    for(angle = 90; angle < 180; angle -= 1){ // goes from 90 degrees to 180 degrees // in steps of 1 degree 
      servo.write(90);                        // tell servo to go to position 90
      delay(10);                              // waits 15ms for the servo to reach the position 
    }
  }
  
  if (pose_msg.data == 1){
    for(angle = 0; angle < 180; angle -= 1){  // goes from 0 degrees to 180 degrees // in steps of 1 degree 
      servo.write(0);                         // tell servo to go to position 0
      // depending on the orientation of the motor change to 180
      delay(10);                              // waits 15ms for the servo to reach the position 
    }
  }
 
  else if (pose_msg.data == 2){
    for(angle = 0; angle < 180; angle +=1){
      servo.write(180);                       // depending on the orientation of the motor change to 0
      delay(10);                           
    }
  }
}

ros::Subscriber<std_msgs::Int32> sub("msgArduino", callback); // subscribe to the ros node 'listener.py'

void setup(){
  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(9);                            //attach it to pin 9 // key servo specific area
}

void loop(){
  
  nh.spinOnce();
  delay(15);
}

// in cmd type: rosrun rosserial_python serial_node.py /dev/ttyACM1
