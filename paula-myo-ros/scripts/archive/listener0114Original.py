#!/usr/bin/env python
import rospy
import pickle
import numpy as np
from ros_myo.msg import EmgArray
from std_msgs.msg import Int32 # gives me a type of message
# We will use the time module
import time
from threading import Timer
 
gesturePred = Int32() # assign gesturePred a type of message that has both header and data

# slect delays
delayShort = 10
delayBase = 5
delayLong = 1

########################################################################################

# load the model
model = pickle.load(open('svmClassifier1030.pkl', 'rb'))
# load the scaler
scaler = pickle.load(open('scaler1030.pkl', 'rb'))

########################################################################################

def callback(data):
    rawDataScaled = scaler.transform(np.array(data.data)[np.newaxis])
    gesturePred.data = model.predict(rawDataScaled) # take from the message called gesturePred only the data (not the header) and predicts pose and reformats it
    #print("Predicted gesture:", gesturePred.data[0]) # prints the predicted pose (select first & only value of array)
    #rospy.loginfo(data.data, type(data.data)) # will print the raw data
    
def listenMyo():
    rospy.init_node('listener', anonymous=True) # initialize as node
    sub = rospy.Subscriber('/myo_raw/myo_emg', EmgArray, callback) # get raw data from topic

######################### countdown from start of experiment ###########################

# Create a function that will print the time
def create_countdown_timer(time):
    #print(time,"......")
 
# Here we have to modify the time for which the experiment will run (30 mins = 1800 seconds)
time_in_sec=int(input(1800)) 
 
# For the first time we will call the function manually
create_countdown_timer(time_in_sec) 
 
for times in range(1,time_in_sec): 
    # calling the Timer class every second
    t = Timer(1,create_countdown_timer,[str(time_in_sec-times)])
    t.start()
    time.sleep(1)

return t

################################# send EMG data to Arduino #############################
## need to take in t from countdown
def talkArduino():
    pub = rospy.Publisher('msgArduino', Int32, queue_size=10)

## should I modify rate, queue size, or sleep????????

    ##for t in range(420, 480):
    ##     if gesturePredPrev == 0 or gesturePredPrev == 2 && gesturePred.data = 1
    ##          delay = delayLong
    ## ONLY ONCE IN THAT TIME RANGE, THEN QUIT or reinitialze delay
        
    ##for t in range(550, 600):
    ##     if gesturePredPrev == 0 or gesturePredPrev == 2 && gesturePred.data = 1
    ##          then delay = delayShort
    ## ONLY ONCE IN THAT TIME RANGE, THEN QUIT or reinitialze delay


## OR ##

    ## counter++ for every time combination 2-1 or 0-1 happens (aka from open to close // close while the previous was not closed)

    ##if counter is == 5, 19, other random numbers 
    ##     if gesturePredPrev == 0 or gesturePredPrev == 2 && gesturePred.data[0] == 1
    ##          delay = delayLong // OR // output pub = [2,2,2,2,2,2,2,2,2,2,2] -> same as inducing delay
    ##          print("delayed and now closed")
    ## ONLY ONCE IN THAT TIME RANGE, THEN QUIT or reinitialze delay



    rate = rospy.Rate(delay) # 5Hz = 0.2s // 10hz = 0.1S
    while not rospy.is_shutdown():
    	rospy.loginfo(gesturePred.data) # call data type's value (aka the predicted pose value)

        ## save data in variable
        ## gesturePredPrev = gesturePred.data

    	pub.publish(gesturePred) # here it is ok to give it only the message (with header and data) because publisher turns the data into a message anyhow!

            # dalayAnti = gesturePred = 1

    	rate.sleep() # this rate should modify based on 



if __name__ == '__main__':
    listenMyo()
    try:
        talkArduino()
    except rospy.ROSInterruptException:
        pass
    rospy.spin() # this needs to be at the end so that it loops through everything - otherwise it will get 			   stuck at this loop






