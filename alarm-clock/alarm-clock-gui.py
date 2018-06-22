'''
Alarm Clock GUI Client

Requirements:
vlc:            pip install vlc
mutagen:        pip install mutagen
python-crontab: pip install python-crontab
'''

import sys
import string
import vlc
import os
import getpass
from time import sleep
from mutagen.mp3 import MP3
from crontab import CronTab
from tkinter import *


username = getpass.getuser()
script_path = os.path.abspath(sys.argv[0])


class Window(Frame):
	
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master=master
        self.init_window()

    def init_window(self):
        self.master.title('Alarm')
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        head_label = Label(self, text="Alarm Clock")
        head_label.grid(padx=5, pady=5)

        scheduled_tasks_list_box = Listbox(self)
        scheduled_tasks_list_box.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
        self.show_scheduled_alarms(scheduled_tasks_list_box)
        scheduled_tasks_list_box.bind("<<onScheduledAlarmSelect>>", self.onScheduledAlarmSelect)

        #scrollbar_scheduled_tasks_list_box = Scrollbar(self.master, orient="horizontal")
        #scrollbar_scheduled_tasks_list_box.config(command=scheduled_tasks_list_box.xview)
        #scrollbar_scheduled_tasks_list_box.pack(side="bottom", fill="x")
        #scheduled_tasks_list_box.config(xscrollcommand=Scrollbar.set)

        self.var=StringVar()


        ringnow_button = Button(self, text="Ring Now", command=self.ringnow)
        ringnow_button.grid(row=1, column=3)
        
        delete_scheduled_alarm_button = Button(self, text="Delete Scheduled Alarm", command= lambda: self.delete_scheduled_alarm(scheduled_tasks_list_box))
        delete_scheduled_alarm_button.grid(row=2, column=3)

    def show_scheduled_alarms(self, scheduled_tasks_list_box):
        scheduled_tasks_list_box.delete(0, END)
        cron_task = CronTab(user=username)
        for job in cron_task:
            if job.comment.startswith('alarm-clock-'):
                scheduled_tasks_list_box.insert(END, job)

    def onScheduledAlarmSelect(self, val):
        sender=val.widget
        idx=sender.curselection()
        value=sender.get(idx)    
        self.var.set(value)

    def ringnow(self):
        alarm_file = vlc.MediaPlayer(os.path.join(os.path.dirname(script_path), "alarm.mp3"))
        alarm_file_length = MP3(os.path.join(os.path.dirname(script_path), "alarm.mp3")).info.length
        alarm_file.play()

    def delete_scheduled_alarm(self, scheduled_tasks_list_box):
        #import pdb
        #pdb.set_trace()
        cron_task = CronTab(user=username)
        idno = self.var.get()
        print(idno)
        for job in cron_task:
            if job.comment=='alarm-clock-'+idno:
                cron_task.remove(job)
                cron_task.write()
        self.show_scheduled_alarms(scheduled_tasks_list_box)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()