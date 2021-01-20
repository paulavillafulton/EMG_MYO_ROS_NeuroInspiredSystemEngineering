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

int pose;   // variable to store the myo position
//int angle;    // variable to store the servo position

ros::NodeHandle nh; //instantiate the node handle

Servo servo; // key servo specific area - create servo object to control servo

void callback( const std_msgs::Int32& pose_msg){
  // do something with pose_msg.data

  if (pose_msg.data == 1)
  {servo.write(0);} // for model 3Fin use 180
    
  else if (pose_msg.data == 0)
  {servo.write(90);}
    
  else if (pose_msg.data == 2)
  {servo.write(0);}  // for model 3Fin use  0

}

ros::Subscriber<std_msgs::Int32> sub("msgArduino", callback); // subscribe to the ros node 'Listener.py'

void setup(){
  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(11); //attach it to pin 9 // key servo specific area
}

void loop(){
  
  nh.spinOnce();
  delayMicroseconds(50); // pauses for 50 miliseconds
}

// in cmd type: rosrun rosserial_python serial_node.py /dev/ttyACM1
