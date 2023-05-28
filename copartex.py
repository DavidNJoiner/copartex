import os
import requests
import psutil  
import platform
from queue import Queue
import pandas as pd
from tqdm import tqdm
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


print(f"platform: {platform.platform()}")
print(f"system: {platform.system()}")
print(f"release: {platform.release()}")
print(f"version: {platform.version()}")
print(f"machine type: {platform.machine()}")
print(f"physical cores: {psutil.cpu_count(logical=False)}")


def main():

    # -----------------------------
    # Functionnal part
    # -----------------------------

    def ValidPath(path):
        if os.path.exists(path):
            if path.endswith('.csv'):
                return True
            else:
                update_status("invalid extension")
                statusLabel.config(fg='orange')
                return False
        else:
            update_status("path does not exist")
            statusLabel.config(fg='red')
            return False

    def BrowseCSV(button):
        filepath = filedialog.askopenfilename(defaultextension=".csv")
        if ValidPath(filepath):
            path = os.path.basename(filepath)
            button.config(text = path)

    def GetCeiling(total_links):
        return int(total_links * (float(end_var.get())/100))

    def UpdateProgress(current_value, progressbar, statusLabel):
        progressbar["value"] = current_value
        statusLabel.config(text="{} / {}".format(current_value, max_value))

    def update_status(status):
        status_var.set("status : " + status)

    def Run():
        
        inputPath = input_filepath_button.cget("text")
        outputPath = output_location_button.cget("text")
        dataframe = pd.read_csv(inputPath, sep=';', low_memory=False)

        qteLinks = len(dataframe)
        end_var.set(qteLinks)
        maxLink = GetCeiling(qteLinks)
        minLink = 0

        #progressbar["maximum"] = qteLinks

        #linksToProcess = dataframe['ImageURL'][minLink:maxLink]
        #ProcessLinks(linksToProcess, outputPath, progressbar, statusLabel)
        l = tfur.makeRandomNumberList(10000)
        tfur.fetchSimu(l, progressbar)

    def RequestParentLink(link):

        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)

        try: return session.get(link)
        except requests.exceptions.ConnectionError as err: print(err)
        except requests.exceptions.MissingSchema as ms: print(ms)

    def ProcessLinks(links, outputPath, progressbar, statusLabel):
        urls = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = list(tqdm(executor.map(lambda x: FetchChildLinks(x, progressbar, statusLabel), links), total=qtelinks, desc="processing links"))
            try:
                urls.extend(results)
            except Exception as exc:
                print('%r generated an exception: %s' % (results, exc))
    
        outputDF = pd.DataFrame(list(filter(None, urls)))
        outputDF.to_csv(outputPath, index=False)
        tk.messagebox.showinfo("info", "processing done!")

    def FetchChildLinks(link, progressbar, statusLabel):

        response = RequestParentLink(link)
        if response != None:
            if response.status_code == 200: 
                data = response.json()
                current_value = progressbar["value"] + 1
                UpdateProgress(current_value, progressbar, statusLabel)
                return [link['url'] for image in data['lotImages'] for link in image['link'] if link['isHdImage'] == False and link['isThumbNail'] == False]
            else: return
        else: return

    # -----------------------------
    # Graphical User Interface part
    # -----------------------------
    
    root = tk.Tk()
    root.title("Copart CSV Processor")
    
    root.geometry('400x350')
    root.resizable(False, False)
    root.configure(bg='#cecece')

    #interface variables
    end_var = tk.IntVar(value=100)
    progress_var = tk.IntVar(value=0)
    status_var = tk.StringVar(value="...")
    option1 = tk.IntVar()

    header_image = tk.PhotoImage(file="header.png")
    header_label = tk.Label(root, image=header_image)
    header_label.grid(row=0, column=0, columnspan=3)

    input_filepath_button = tk.Button(root, text='input file', command=lambda: BrowseCSV(input_filepath_button))
    input_filepath_button.grid(row=1, column=1, pady=5, padx=10, sticky='ew')

    output_location_button = tk.Button(root, text='output file', command=lambda: BrowseCSV(output_location_button))
    output_location_button.grid(row=2, column=1, pady=5, padx=10, sticky='ew')

    optionFrame = tk.Frame(root)
    optionFrame.grid(row=4, column=0, columnspan=3)

    process_button = tk.Button(root, text="RUN", command=Run)
    process_button.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky='ew')

    # progressFrame : frame which hold the progressbar and its label.
    progressFrame = tk.Frame(root, bg='black')
    progressFrame.grid(row=6, column=0, columnspan=3, pady=2)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("grey.Horizontal.TProgressbar", foreground='grey', background='blue')

    statusLabel = tk.Label(progressFrame, textvariable=status_var, bg='black', fg='white')
    statusLabel.grid(row=0, column=0)

    progressbar = ttk.Progressbar(progressFrame, orient="horizontal", length=380, mode="determinate",style='grey.Horizontal.TProgressbar', variable=progress_var, maximum=float(end_var.get()))
    progressbar.grid(row=1, column=0)

    root.mainloop()


main()
