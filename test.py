from tqdm import tqdm
import platform
import psutil 
import random
import time

#GUI
import tkinter as tk
from tkinter import ttk


def make_random_num_list(listLength):
    rList=[]
    for i in range(listLength):
        rList.append(random.randint(0,100))
    return rList

class ProgressTracker():
    def __init__(self):
        self.stopped = False
        self.value = 0
    
    def update():
        for val, i in enumerate (tqdm(l)):
            if stop_clicked:
                break
            l[i]+=1
            update_value.set(val)
            status_var.set(f"Processing: {val+1}/{l_size}")
            root.update_idletasks()
            time.sleep(0.1)

    def stop_progressbar():
        global stop_clicked
        stop_clicked = True

if __name__ == "__main__":
    print(f"platform: {platform.platform()}")
    print(f"system: {platform.system()}")
    print(f"release: {platform.release()}")
    print(f"version: {platform.version()}")
    print(f"machine type: {platform.machine()}")
    print(f"physical cores: {psutil.cpu_count(logical=False)}")
    
    stop_clicked = False
    l = make_random_num_list(1000)
    l_size = len(l)
    
    root = tk.Tk()
    root.title("Testing Progressbar")

    update_value = tk.IntVar(value=0)
    status_var = tk.StringVar(value="Ready")
    
    root.geometry('400x350')
    root.resizable(False, False)
    root.configure(bg='#cecece')

    progressFrame = tk.Frame(root, bg='#cecece')
    progressFrame.grid(row=2, column=0, columnspan=1, pady=0)

    style1 = ttk.Style()
    style1.theme_use('default')
    style1.configure("grey.Horizontal.TProgressbar", foreground='grey', background='blue')

    statusLabel = tk.Label(progressFrame, textvariable=status_var, bg='#cecece', fg='black')
    statusLabel.grid(row=0, column=0)

    progressbar = ttk.Progressbar(progressFrame, orient="horizontal", length=380, mode="determinate",style='grey.Horizontal.TProgressbar', variable=update_value, maximum=(l_size-1))
    progressbar.grid(row=1, column=0)

    start = ttk.Button(progressFrame,text='start',command=update_progressbar())
    start.grid(row=2, column=0)

    stop = ttk.Button(progressFrame,text='stop',command=stop_progressbar())
    stop.grid(row=3, column=0)

    root.mainloop()


