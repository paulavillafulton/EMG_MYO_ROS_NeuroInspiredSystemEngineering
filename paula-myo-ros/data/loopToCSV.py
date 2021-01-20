import rosbag
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import os



for filename in os.listdir("/home/cybathlon/catkin_ws/src/bagFiles/open"):
    if filename.endswith(".bag"):
      bag = rosbag.Bag(filename) #get the data from the rosbag and store it in variable "bag"
      topics = bag.get_type_and_topic_info()[1].keys() #get topic and type from bag and store it in variable "topic"
      #print(topics) #uncomment to see the topic. Should be /myo_ros/myo_emg

      dataCol = [] #initialize empty array
      dataCol.append('time') #set the second column header to "time"
      dataCol.append('label') #set the first column header to "label"
      for i in range(0,8): #loop through 0 to 8 elements of the bag data and name it EMG0, EMG1, ... EMG7
          dataCol.append('EMG'+str(i))

      df = pd.DataFrame(columns=dataCol) #set the above in a dataframe

      for topic, msg, t in bag.read_messages(topics=['/myo_raw/myo_emg']): #read bag file and loop through topic, msg and t of the topic 
          tmp = [t.to_sec()] #convert time time stamps created in the rosbag to seconds
          tmp.extend(msg.data) #extend the timestamp (now in seconds) to become as long as the data
          tmpSeries = pd.Series(tmp, index=df.columns) #turn time into series to place in dataframe
          df = df.append(tmpSeries, ignore_index=True) #place time into dataframe
      bag.close() #close bag file!

      time_start = df.get('time')[0] #time in the bag file is really long (time of the computer) 
      df['time'] = df.get('time')-time_start #so take the first number and substract it from all other numbers to get the correct recording time
      df['label'] = df._set_value('2') #set the value in this entire column as 0 since I am doing per file: 0,1,2

      #Save dataframe to CSV
      df.to_csv(filename +'.csv', index=False)


