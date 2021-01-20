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

// -------- CONSTANTS (won't change)----------------------

const int closeFinger = 0;
const int openFinger = 90;
int wait = 2000; //two second delay

//------------ VARIABLES (will change)---------------------

int previousFingerState = 1;
int counter = 0; 
// int servoDegrees = 2; // amount servo moces at each step
                      // changes to negative value when servo moves to other direction
unsigned long currentMillis = 0;    // stores the value of millis() in each iteration of loop()


//////////////////////
// baud is at 57600 //
//////////////////////

ros::NodeHandle nh; //instantiate the node handle

Servo servo; // key servo specific area - create servo object to control servo


//------------ Callback Function ------------------------

void callback(const std_msgs::Int32& pose_msg){

// decide what to do with pose_msg.data ----------

  if (pose_msg.data == 1)
  {
     counter++;

     if (isPrime(counter) && previousFingerState == openFinger) // if this condition happens x times, wait to close finger 
     {
      nh.loginfo("Finger closing with delay");
      Serial.println("Finger closing with delay");
      delay(wait);
      servo.write(closeFinger);
     }

     else if (counter >= 100) // if counter reaches 10, reset to 0
     {
      counter = 0;
     }
     
     else
     {
      servo.write(closeFinger);
      nh.loginfo("Finger closed");
      Serial.println("Finger closed");
     } // for model 3Fin use 180

     previousFingerState = closeFinger; // update previousFingerState to closed
  }
  
  else if ((pose_msg.data == 0) or (pose_msg.data == 2))
  {
    servo.write(openFinger);
    nh.loginfo("Finger open");
    Serial.println("Finger open");

    previousFingerState = openFinger; // update previousFingerState to opened
  }

}

ros::Subscriber<std_msgs::Int32> sub("msgArduino", callback); // subscribe to the ros node 'Listener.py'

void setup(){

  Serial.begin(57600);
  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(11); //attach it to pin 11 // key servo specific area

}

void loop(){  
  
  nh.spinOnce();
  delay(1);
}

boolean isPrime(int x) 
  {
    boolean prime = true;
   
    for(int i = 2; i <= x/2; i++) { //Loop every number up to half
      if(x % i == 0) { //If it's divisible...
        prime = false; //It isn't prime!
        break;
      }
    }
    return prime;
  }


// in cmd type: rosrun rosserial_python serial_node.py /dev/ttyACM1
