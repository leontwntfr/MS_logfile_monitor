# MS logfile monitor - small project

> Aim: Code a small script for a tool that monitors the log files of the mass spectrometers in real-time.

### September 3, 2024

> First aim: Start writing the script.

I implemented all basic functions and code needed for the log file monitor. The script is called `MS_log_monitor.py`. It includes a class for handling the events of changes to log files in a given directory, a function to apply this handling, a function to read the historic data (of previous log files), and a function to update according to changing log files in real-time. It should further include the following aspects:
- argparse integration to provide start date (date of first log file to be considered) and, optionally, the directory of log files (in same folder as script by default)
- some general quality improvements

Up until now, the basic functions are generally working. However, I am working on handling the header lines repeating themselves in log files.

### September 4, 2024

> First aim: Fix script so that repeating header lines can be handled.

I successfully fixed the issue of reading logfiles with repeated header lines by checking if in lines of the logfiles in the "Date" column the value is also "Date" and removing these lines.

Now, a plot was successfully generated. However, the y-values were unordered (in a random order from down to up at the y-axis).

> Second aim: Fix issue of y-values randomly ordered.

After a while of bug hunting and research, I found that the y-values were considered as string and not floats. Converting the values to floats fixed the issue.

I tested the real-time aspect by manually removing and readding line to a logfile. However, the updated plot (updating itself worked after given time) did not include the new data and stayed the same.

> Third aim: Fix code so that real-time aspect is working.

I found that the name of the first function in the class has to be changed for it to be recognized by watchdog. Renaming fixed the issue.

This marks the first completely working version of the MS logfile monitor. Next, I want to implement argparse integration.