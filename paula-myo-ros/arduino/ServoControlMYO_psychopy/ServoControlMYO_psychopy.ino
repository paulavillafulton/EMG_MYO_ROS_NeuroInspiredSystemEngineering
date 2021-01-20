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
 
// ----------LIBRARIES-------------------------------------

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Int32.h>

// --------CONSTANTS (won't change)---------------

const int closeFinger = 0;
const int openFinger = 90;
int wait = 3000; // three second delay

//const int servoMinDegrees = 20; // the limits to servo movement
//const int servoMaxDegrees = 150;

//------------ VARIABLES (will change)---------------------

int fingerAngle = 0;
int counter = 0; 
// int servoDegrees = 2; // amount servo moces at each step
                      // changes to negative value when servo moves to other direction
unsigned long currentMillis = 0;    // stores the value of millis() in each iteration of loop()


///////////////////
// baud is at 57600 //
///////////////////

ros::NodeHandle nh; //instantiate the node handle

Servo servo; // key servo specific area - create servo object to control servo


//------------ Callback Function ------------------------

void callback( const std_msgs::Int32& pose_msg){
  // do something with pose_msg.data


// function to find prime numbers -----------------------

boolean isPrime(int x) {
  boolean prime = true;
 
  for(int i = 2; i <= x/2; i++) { //Loop every number up to half
    if(x % i == 0) { //If it's divisible...
      prime = false; //It isn't prime!
      break;
    }
  }
  return prime;
}


// decide what to do with pose_msg.data ------------------

  if (pose_msg.data == 1)
  {
     counter++;
     Serial.print("counter value:");
     Serial.println(counter);

     if (isPrime(counter)) // if this condition happens x times, wait to close finger
     {
      delay(wait);
      servo.write(closeFinger);
      nh.loginfo("Finger closed with delay");
     }
     
     //if (counter >= 50) // if counter reaches 100, reset to 0
     //{
     // counter = 0;
     //}
     
     else
     {
      servo.write(closeFinger);
      nh.loginfo("Finger closed");
     } // for model 3Fin use 180

     
  }
  
  else if (pose_msg.data == 0)
  {
    servo.write(openFinger);
    nh.loginfo("Finger open");
  }
    
  else if (pose_msg.data == 2)
  {
    servo.write(openFinger);
    nh.loginfo("Finger open");
  }
}

ros::Subscriber<std_msgs::Int32> sub("msgArduino", callback); // subscribe to the ros node 'Listener.py'

void setup(){

  Serial.begin(57600);
  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(11); //attach it to pin 9 // key servo specific area

}

void loop(){  
  
  nh.spinOnce();
  delay(1);
}

// in cmd type: rosrun rosserial_python serial_node.py /dev/ttyACM1
