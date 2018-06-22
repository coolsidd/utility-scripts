# Python Scripts
**Repository containing Python scripts made for simplifying common tasks.** :sunglasses:

## Libraries Used:
 - os
 - sys
 - openpyxl
 - hashlib
 - filecmp
 - struct
 - Crypto           (in auto-backup)
 - shutil           (in auto-backup)
 - vlc              (in alarm-clock)
 - mutagen          (in alarm-clock)
 - python-crontab   (in alarm-clock)

## Scripts:
1. [Duplicate](https://github.com/Pro-Panda/Python-Scripts/tree/master/Duplicate): 
   - It lists all the duplicate files present at a given path.
   - Gives the option to remove/ not remove any of them.
   - Uses 'filecmp' and 'os' libraries to compare files which are of the same size
   
2. [Excel-Attd](https://github.com/Pro-Panda/Python-Scripts/tree/master/Excel-Attd): 
   - Fills the attendance of all BITS Students(mathced by ID) in an excel sheet.
   - Created to fill the attendance of Students registered in CP Course at BITS Pilani
   
3. [Alarm-Clock](https://github.com/siddhantkhandelwal/Python-Scripts/tree/master/alarm-clock):
   - Plays the file 'alarm.mp3' in the cwd once the alarm expires.
   - Can be used to schedule alarms weekly, daily.
   
## How to use:
 - Duplicate

   ```bash
   python filecmp.py /path/to/folder
   ```
 - Excel-Attd

    ```bash
    python update.py /path/to/attendance_list /path/to/excel_sheet <Attd Column No.>
    ```
 - Alarm-Clock

   - CLI Version
     ```bash
     python alarm-clock-cli.py option h m s
     ```
        | Option | Task                               | Example                           |
        |--------|------------------------------------|-----------------------------------|
        | 0      | Ring Immediately                   | python alarm-clock-cli.py 0       |
        | 1      | Create a new scheduled alarm       | python alarm-clock-cli.py 1 10 10 |                   
        | 2      | Delete an existing scheduled alarm | python alarm-clock-cli.py 2       |
    
   - GUI Version
     ```bash
     python alarm-clock-gui.py
     ``` 

## Improvements:
*Anyone is welcome to contribute and improve/modify the scripts.*

- [Alarm-Clock](https://github.com/siddhantkhandelwal/Python-Scripts/tree/master/alarm-clock):
  - CLI Version
    - Add an option to snooze the alarm.
    - Create logs specific to the script. Will help in keeping track of alarms independent of the cron-tab.
  - GUI Version
    - Add options to add alarms, create different frames for different tasks.
    - Improve the look of the app.

*Please open an issue if you find any bugs in any of the scripts.*