#!/usr/bin/env python
import rospy
import time
import pickle
import random
import numpy as np
from ros_myo.msg import EmgArray
from std_msgs.msg import Int32 # gives me a type of message
from pylsl import StreamInfo, StreamOutlet # used for LabStreamLayer


threshold = 3
scaled_emg_array = np.zeros((threshold, 8))

raw_data_scaled = Int32() # assign gesturePred a type of message that has both header and data
pred = Int32()

###################################### create stream info LabStreamLayer ######################################

# stream markers
info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'string', 'myuidw43536')
# make an outlet
outlet = StreamOutlet(info)
print("now sending markers...")

###################################### importing my scaler and SVM model ######################################

model = pickle.load(open('svmClassifier1030.pkl', 'rb')) # load the model
scaler = pickle.load(open('scaler1030.pkl', 'rb')) # load the scaler

################################################ delay function ###############################################
#   We start by calculating the time which has elapsed since the start of the experiment: current_time        #
#   A desired delay is then implemented within a particular time window of the experiment                     #
#   A single delay will happen upon the participant's command to close the finger                             #                                                                              
###############################################################################################################

def delay(start_time,
          window_start,
          window_length,
          delay_happened,
          delay_rate,
          pred,
          previous_pred,
          short_delay_window_start_times,
          medium_delay_window_start_times,
          long_delay_window_start_times,
          short_delay_rate,
          medium_delay_rate,
          long_delay_rate,
          outlet):

    # calculate the current time
    current_time = time.time() - start_time
    current_second = int(time.time() - start_time)

    # if current time is equal to any of the specified times, then the appropriate delay rates will be induced
    if current_second in long_delay_window_start_times:
        window_start = current_second
        delay_rate = long_delay_rate

    elif current_second in medium_delay_window_start_times:
        window_start = current_second
        delay_rate = medium_delay_rate

    elif current_second in short_delay_window_start_times:
        window_start = current_second
        delay_rate = short_delay_rate

    window_end = window_start + window_length

    rospy.loginfo("current time is:")
    rospy.loginfo(current_time)
    #outlet.push_sample(markernames[4], current_time)

    # we ensure that if the delay has happened once, it does not happen again
    if window_start <= current_time <= window_end and delay_happened == False and previous_pred[0] != 1 and pred[0] == 1:
        delay_happened = True
        rospy.loginfo("delay is :")
        rospy.loginfo(delay_rate)
        rospy.loginfo(previous_pred[0])
        if delay_rate == long_delay_rate:
            outlet.push_sample(['Delay_L'])
        elif delay_rate == medium_delay_rate:
            outlet.push_sample(['Delay_M'])
        elif delay_rate == short_delay_rate:
            outlet.push_sample(['Delay_S'])
        time.sleep(delay_rate)

    elif window_start <= current_time <= window_end and delay_happened == True:
        rospy.loginfo("NO delay, the delay already happened")

    else:
        delay_happened = False
        rospy.loginfo("NO delay")
        
    return delay_happened, delay_rate


################################################### callback ##################################################
#   This callback function scales our incoming data from the Myo Armband                                      #
###############################################################################################################

def callback(data):
    raw_data_scaled.data = scaler.transform(np.array(data.data)[np.newaxis])


################################################### listenMyo ##################################################
#   We subscribe to the Myo Armband's myo_emg messages                                                         #
################################################################################################################

def listenMyo():
    rospy.init_node('listener', anonymous=True) # initialize as node
    sub = rospy.Subscriber('/myo_raw/myo_emg', EmgArray, callback) # get raw data from topic


################################################## talkAdruino #################################################
#   Define the total length of our experiment in seconds: experiment_time                                      #
#   Specify the desired delays to implement between subject command and finger movement                        # 
#   Define the time points in which these delays have to occure - should appear random to subject              #
#   When we reach the time where our delay should happen, our delay() function will listen for the subject's   #
#   command and implement the specified delay                                                                  #
################################################################################################################

def talkArduino():

    # total time of experiment in seconds
    experiment_time = 1200

    # specify desired delays
    delay_rate = 0.5
    long_delay_rate = 10
    medium_delay_rate = 7
    short_delay_rate = 4

    # define start times of the experiment where we want to induce a delay
    short_delay_window_start_times = [60]
    medium_delay_window_start_times = [10]
    long_delay_window_start_times = [180]

    window_start = np.min(np.array(short_delay_window_start_times + medium_delay_window_start_times + long_delay_window_start_times))

    # initialize variables
    delay_happened = False
    counter = 0
    previous_pred = [0]

    # publish messages to msgArduino at 10Hz
    pub = rospy.Publisher('msgArduino', Int32, queue_size=10)
    rate = rospy.Rate(10) # 10hz 

    # start timer
    start_time = time.time()

    while not rospy.is_shutdown():
        
        # calculate the current time
        current_time = time.time() - start_time
        current_second = int(time.time() - start_time)

        # place scaled data into a matrix
        scaled_emg_array[counter,:] = raw_data_scaled.data
        counter += 1 # we use a counter to fill our matrix

        if counter >= threshold: # once the matrix has reached a certain size (size of the threshold) we:
            counter = 0 # 1) reset our counter = 0
            averaged_emg_array = np.mean(scaled_emg_array, axis = 0) # 2) we calculate the average of each column
            pred = model.predict(averaged_emg_array.reshape(1,-1)) # 3) upon this average, we predict what pose was performed by the subject
            

            if random.uniform(0,1) > 0.8:
                pred = [0]


            if pred[0] == 0 and previous_pred[0] != 0: # Command by participant CLOSE
                outlet.push_sample(['C_com']) 
            elif (pred[0] == 1 or pred[0] == 2) and previous_pred[0] == 0: # Command by participant OPEN
                outlet.push_sample(['O_com']) 

            # we now call our delay function
            delay_happened, delay_rate = delay(start_time,
                                   window_start, 
                                   window_length = 40,
                                   delay_happened = delay_happened, 
                                   delay_rate = delay_rate, 
                                   pred = pred,
                                   previous_pred = previous_pred,
                                   short_delay_window_start_times = short_delay_window_start_times,
                                   medium_delay_window_start_times = medium_delay_window_start_times, 
                                   long_delay_window_start_times = long_delay_window_start_times,
                                   short_delay_rate = short_delay_rate,
                                   medium_delay_rate = medium_delay_rate,
                                   long_delay_rate = long_delay_rate,
                                   outlet = outlet)
            rospy.loginfo(pred) # print the model-predicted user command
            pub.publish(pred) # we publish our prediction to msgArduino to move the finger

            if pred[0] == 0 and previous_pred[0] != 0: # SR finger order CLOSE
                outlet.push_sample(['C_act']) 
            elif (pred[0] == 1 or pred[0] == 2) and previous_pred[0] == 0:# SR finger order OPEN
                outlet.push_sample(['O_act']) 

            previous_pred = pred # we update this command to become the previous command
            # send prediction to LSL



        rate.sleep()

        if experiment_time <= current_time: # if the current time exceeds the desired time of the experiment, we terminate the experiment
            rospy.loginfo("End of experiment")
            break

if __name__ == '__main__':
    listenMyo()
    try:
        talkArduino()
    except rospy.ROSInterruptException:
        pass
    rospy.spin() # this needs to be at the end so that it loops through everything - otherwise it will get stuck at this loop

