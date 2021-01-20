#!/usr/bin/env python
import rospy
import pickle
import numpy as np
from ros_myo.msg import EmgArray
from std_msgs.msg import Int32 # gives me a type of message
# We will use the time module
import time
 
#################################### constants ########################################

gesturePred = Int32() # assign gesturePred a type of message that has both header and data

# slect delays
delayShort = 10
delayBase = 5
delayLong = 1
delay_happened = False
rate = 1

############################### classifier & scaler ####################################

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

##################################### start timer #######################################

start_time = time.time()

##################################### delay functions #######################################

def longDelay(beginningTimeframe, endTimeframe, delay_happened):

    print(delay_happened)
    if beginningTimeframe <= current_time <= endTimeframe and delay_happened == False:
        delay = delayLong
        delay_happened = True
        print(f'current time is: {current_time}, delay is :{delay}, the delay happened: {delay_happened}')

    elif beginningTimeframe <= current_time <= endTimeframe:
        delay = delayBase
        print(f'current time is: {current_time}, delay is :{delay}, the delay happened: {delay_happened}')

    else:
        delay = delayBase
        delay_happened = False
        print(f'current time is: {current_time}, delay is :{delay}, the delay happened: {delay_happened}')

    return delay_happened, delay

################################# send EMG data to Arduino #############################
## need to take in t from countdown
def talkArduino():
    pub = rospy.Publisher('msgArduino', Int32, queue_size=10)

    current_time = time.time() - start_time
    ## if current_time > 420 and current_time < 480:
    ##     if gesturePredPrev != 1 && gesturePred.data = 1 && delay_happened = False

## call function longDelay() if gesturePredPrev != 1 && gesturePred.data = 1 && delay_happened = False

    rate = rospy.Rate(delay) # 5Hz = 0.2s // 10hz = 0.1S
    while not rospy.is_shutdown():
    	rospy.loginfo(gesturePred.data) # call data type's value (aka the predicted pose value)
        gesturePredPrev = gesturePred.data # save data in variable
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






