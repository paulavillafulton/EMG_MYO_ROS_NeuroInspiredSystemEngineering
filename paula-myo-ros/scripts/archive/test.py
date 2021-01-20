import time
import numpy as np

EXPERIMENT_TIME = 120
delay_happened = False
delay_rate = 1

short_delay_window_start_times = [9, 18, 28]
medium_delay_window_start_times = [24]
long_delay_window_start_times = [57]

window_start = np.min(np.array(short_delay_window_start_times + medium_delay_window_start_times + long_delay_window_start_times))
print(window_start)

def delay(window_start, window_length, delay_happened, delay_rate):

    window_end = window_start + window_length

    if window_start <= current_time <= window_end and delay_happened == False:
        delay_happened = True
        print(f'current time is: {current_time}, delay is :{delay_rate}')
        time.sleep(delay_rate)

    elif window_start <= current_time <= window_end:
        print(f'current time is: {current_time}, NO delay, the delay already happened')

    else:
        delay_happened = False
        print(f'current time is: {current_time}, NO delay')

    return delay_happened

start_time = time.time()

for times in range(1, 20000): 
    current_time = time.time() - start_time
    current_second = int(time.time() - start_time)

    #for element in short_delay_window_start_times
    #    window_start = short_delay_window_start_times[element]

    if current_second in long_delay_window_start_times:
        window_start = current_second
        delay_rate = 2

    if current_second in medium_delay_window_start_times:
        window_start = current_second
        delay_rate = 1

    if current_second in short_delay_window_start_times:
        window_start = current_second
        delay_rate = 0.5
    
    delay_happened = delay(window_start, window_length=5,delay_happened=delay_happened, delay_rate = delay_rate)

    time.sleep(0.1)

    if EXPERIMENT_TIME <= current_time:
        break
        print("The experiment is over")
