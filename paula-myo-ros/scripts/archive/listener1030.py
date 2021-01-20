#!/usr/bin/env python
import rospy
import pickle
import numpy as np
from ros_myo.msg import EmgArray
from std_msgs.msg import Int32 # gives me a type of message

gesturePred = Int32() # assign gesturePred a type of message that has both header and data

# load the model
model = pickle.load(open('svmClassifier1030.pkl', 'rb'))
# load the scaler
scaler = pickle.load(open('scaler1030.pkl', 'rb'))

def callback(data):
    rawDataScaled = scaler.transform(np.array(data.data)[np.newaxis])
    gesturePred.data = model.predict(rawDataScaled) # take from the message called gesturePred only the data (not the header) and predicts pose and reformats it
    #print("Predicted gesture:", gesturePred.data[0]) # prints the predicted pose (select first & only value of array)
    #rospy.loginfo(data.data, type(data.data)) # will print the raw data
    
def listenMyo():
    rospy.init_node('listener', anonymous=True) # initialize as node
    sub = rospy.Subscriber('/myo_raw/myo_emg', EmgArray, callback) # get raw data from topic

def talkArduino():
    pub = rospy.Publisher('msgArduino', Int32, queue_size=10)
    rate = rospy.Rate(5) # 10hz too slow 
    while not rospy.is_shutdown():
    	rospy.loginfo(gesturePred.data) # call data type's value (aka the predicted pose value)
    	pub.publish(gesturePred) # here it is ok to give it only the message (with header and data) because publisher turns the data into a message anyhow!
    	rate.sleep()

if __name__ == '__main__':
    listenMyo()
    try:
        talkArduino()
    except rospy.ROSInterruptException:
        pass
    rospy.spin() # this needs to be at the end so that it loops through everything - otherwise it will get 			   stuck at this loop

