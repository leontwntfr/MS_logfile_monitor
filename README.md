# MS Log Monitor

A python script to monitor the currents of mass spectrometer turbopumps from log files and visualize the data in real-time.

## Dependencies

This script requires Python 3.7+ and the following packages (see installation section on how to install).

- `pandas`
- `matplotlib`
- `watchdog`

## Installation

1. Clone this repository:

```
git clone https://github.com/yourusername/MS_logfile_monitor.git
cd MS_logfile_monitor
```

2. Install the required dependencies using ``pip``:

```
pip install -r dependencies.txt
```

3. Try the script:

```
python MS_log_monitor.py -h
```

## Usage

The script requires the start date (the date from which on the currents should be plotted) and, optionally, the directory to the log file (instead, the script can be place inside the log file directory and run from there).

```
python MS_log_monitor.py [-h] --start-date START_DATE [--log-dir LOG_DIR]
```