import rosbag
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

bag = rosbag.Bag('2020-10-27-16-32-15.bag') #get the data from the rosbag and store it in variable "bag"
topics = bag.get_type_and_topic_info()[1].keys() #get topic and type from bag and store it in variable "topic"
#print(topics) #uncomment to see the topic. Should be /myo_ros/myo_emg

dataCol = [] #initialize empty array
dataCol.append('time') #set the first column header to "time"
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

#Save dataframe to CSV
df.to_csv('47.csv', index=False)

#print(df) #print to see what the data frame looks like now

##Plot the data from the bag file into 8 windows - one single figure
#fig, axs = plt.subplots(4,2)
#for idx, ax in enumerate(axs.flat):
#    ax.plot(df['time'],df['EMG'+str(idx)],label='EMG'+str(idx))
#    ax.set_ylim(0, 2000)
#    ax.set_xlabel('Time [s]')
#    ax.set_ylabel('EMG signal')
#    ax.legend()
#    ax.label_outer()
#
#plt.show()

