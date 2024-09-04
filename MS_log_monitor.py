import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from threading import Thread, Lock
import numpy as np

# ------------------------------------------------------

# directory to log files to monitor (user-defined)
log_dir = '.'
# start date from when data is shown
start_date = datetime.strptime('2024-08-01', '%Y-%m-%d')

# ------------------------------------------------------

# set curr_log parameter
curr_log = None

# global data storage
data = {'TURBO1': [], 'TURBO2': [], 'TURBO3': []}
timestamps = []
lock = Lock()


### class for handling changes in log file directory (if change in log file, new data is added)
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global curr_log, data, timestamps
        if event.src_path.endswith('log'):
            if curr_log is None or event.src_path != curr_log:
                curr_log = event.src_path

            
            # new line from log file
            with lock:
                with open(curr_log, 'r') as f:
                    log_df = pd.read_csv(curr_log, skipinitialspace= True, encoding= "ISO-8859-1", delimiter= '\t', header = 0)
                    log_df = log_df[~log_df.apply(lambda row:row.loc['Date'] == 'Date', axis= 1)]

                    # update global data with changes
                    data['TURBO1'].extend(log_df['TURBO1_CURR_R [A]'].tolist())
                    data['TURBO2'].extend(log_df['TURBO2_CURR_R [A]'].tolist())
                    data['TURBO3'].extend(log_df['TURBO3_CURR_R [A]'].tolist())
                    timestamps.extend(pd.to_datetime(log_df['Date']).to_list())
        
                    # sort
                    sort_ind = sorted(range(len(timestamps)), key=lambda k: timestamps[k])
                    timestamps = [timestamps[i] for i in sort_ind]
                    data['TURBO1'] = [data['TURBO1'][i] for i in sort_ind]
                    data['TURBO2'] = [data['TURBO2'][i] for i in sort_ind]
                    data['TURBO3'] = [data['TURBO3'][i] for i in sort_ind]


def load_prev_data():
    global data, timestamps
    # get sorted log file list
    log_file_list = sorted([file for file in os.listdir(log_dir) if file.endswith('.log')])

    for log_file in log_file_list:
        # extract date from log file names
        log_data_str = log_file.split('--')[1].replace('.log', '')
        log_date = datetime.strptime(log_data_str, '%Y-%m-%d') # convert to datetime format

        if log_date >= start_date: # load from user-defined start date
            log_df = pd.read_csv(os.path.join(log_dir, log_file), skipinitialspace= True, encoding= "ISO-8859-1", delimiter= '\t', header = 0)
            log_df = log_df[~log_df.apply(lambda row:row.loc['Date'] == 'Date', axis= 1)]
            data['TURBO1'].extend(log_df['TURBO1_CURR_R [A]'].tolist())
            data['TURBO2'].extend(log_df['TURBO2_CURR_R [A]'].tolist())
            data['TURBO3'].extend(log_df['TURBO3_CURR_R [A]'].tolist())
            timestamps.extend(pd.to_datetime(log_df['Date']).to_list())

            # sort
            sort_ind = sorted(range(len(timestamps)), key=lambda k: timestamps[k])
            timestamps = [timestamps[i] for i in sort_ind]
            data['TURBO1'] = [data['TURBO1'][i] for i in sort_ind]
            data['TURBO2'] = [data['TURBO2'][i] for i in sort_ind]
            data['TURBO3'] = [data['TURBO3'][i] for i in sort_ind]

def monitor_log_files():

    observer = Observer()
    observer.schedule(LogFileHandler(), log_dir, recursive= False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def animate_plot(i):
    with lock:
        dat_turb1 = [float(x) for x in data['TURBO1']]
        dat_turb2 = [float(x) for x in data['TURBO2']]
        dat_turb3 = [float(x) for x in data['TURBO3']]
        plt.cla()
        plt.plot(timestamps, dat_turb1, label= 'TURBO1_CURR_R [A]')
        plt.plot(timestamps, dat_turb2, label= 'TURBO2_CURR_R [A]')
        plt.plot(timestamps, dat_turb3, label= 'TURBO3_CURR_R [A]')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Current [A]')
        plt.grid(True)
        plt.tight_layout()


def main():
    
    plt.style.use('seaborn')

    # load previous data
    load_prev_data()

    # start monitoring in specific thread
    monitor_thread = Thread(target= monitor_log_files)
    monitor_thread.daemon = True
    monitor_thread.start()

    # plot in real-time
    anim = FuncAnimation(plt.gcf(), animate_plot, interval= 5000)
    plt.show()


if __name__ == "__main__":
    main()

### we want "TURBO1/2/3_CURR_R [A]"
# include possibility to change parameter that is shown in monitor?

