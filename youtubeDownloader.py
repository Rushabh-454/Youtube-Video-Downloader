from pytube import YouTube
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import requests
from io import BytesIO

root = Tk()
root.title("Youtube Video Downloader")
icon = ImageTk.PhotoImage(Image.open("icon.jpg"))
root.iconphoto(FALSE, icon)

img = Image.open("image.jpg")
width, height = img.size
img = img.resize((width+200, height+100))
img = ImageTk.PhotoImage(img)
imgLabel = Label(root, image=img)
imgLabel.grid(row=0, column=0, columnspan=3)

streams = dict()

def download():
    path = filedialog.askdirectory()
    try:
        reqdStream.download(path)
        messagebox.showinfo("Youtube Video Downloader", "File Downloaded Successfully!")        
    except:
        messagebox.showerror("Something went wrong!")

    return
    
def fileSize(*args):
    l = streams[formatType.get()]
    itag = -1
    for i in l:
        if i[0] == resAbr.get():
            itag = i[1]
            break

    global reqdStream
    reqdStream = yt.streams.get_by_itag(itag)
    fs = reqdStream.filesize/8
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'EB']
    unit = 0
    while fs//1000 > 0:
        fs /= 1000
        unit += 1
    fs = round(fs, 2)

    text = "File size: "+str(fs)+" "+units[unit]
    font = tkFont.Font(family="Helvetica", size=13)
    Label(root, text=text, font=font).grid(row=6, column=1)

    button_dwnld = Button(root, text="Download", width=10, height=1, command=download)
    button_dwnld.grid(row=10, column=2, padx=10, pady=10)

def res_abr(*args):
    fType = formatType.get()
    option = [i[0] for i in streams[fType]]
    option = sorted(list(set(option)))

    global resAbr
    resAbr = StringVar(root)
    resAbr.set(option[0])

    text = ""
    if "audio" in fType:
        text = "Average Bitrate"
    else:
        text = "Resolution"

    Label(root, text="Select "+text).grid(row=4, column=2)
    OptionMenu(root, resAbr, *option).grid(row=5, column=2)
    resAbr.trace("w", fileSize)
    return

def Format(*args):
    sType = streamType.get()
    formats = []
    for keys in streams:
        if sType in keys:    
            formats.append(keys)
    
    Label(root, text="Format Type").grid(row=4, column=1)
    global formatType
    formatType = StringVar(root)
    formatType.set(formats[0])
    OptionMenu(root, formatType, *formats).grid(row=5, column=1)
    formatType.trace("w", res_abr)
    return

def stream():
    fs = tkFont.Font(family="Times", size=13, underline=1)
    titleLabel = Label(root, text="Title: "+yt.title, font=fs)
    titleLabel.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    global streamType
    streamType = StringVar(root)
    streamType.set("Video")
    Label(root, text="Stream Type").grid(row=4, column=0)
    video = Radiobutton(root, text="Video", variable=streamType, value="video")
    audio = Radiobutton(root, text="Audio", variable=streamType, value="audio")

    video.grid(row=5, column=0)
    audio.grid(row=6, column=0)
    streamType.trace("w", Format)
    return

def processStream():
    st = yt.streams
    for i in range(len(st)):
        itag = st[i].itag
        string = str(st[i]).replace('"', '')
        string = string[9:-1].split()
        mtype = string[1].split("=")[1]
        if mtype not in streams.keys():
            streams[str(mtype)] = []
        
        if "video" in mtype:
            res = string[2].split("=")[1]
            if res != 'None':
                streams[mtype].append((res, itag))
        else:
            abr = string[2].split("=")[1]
            streams[mtype].append((abr, itag))

def button_search():
    link = search.get()
    try:
        global yt
        yt = YouTube(link)
        
        # TO DISPLAY THUMBNAIL OF THE VIDEO
        # tbURL = yt.thumbnail_url
        # tb_data = requests.get(tbURL).content
        # tb_img = Image.open(BytesIO(tb_data))
        # tb_img = tb_img.resize((width,height))
        # tb_img = ImageTk.PhotoImage(tb_img)
        # tbLabel = Label(root, image=tb_img)
        # tbLabel.grid(row=2, column=0, columnspan=3)

    except:
        messagebox.showerror("Error", "Invalid URL!")
        return

    processStream()
    stream()

search = Entry(root, text="Enter URL", width=50, borderwidth=3)
search.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

myFont = tkFont.Font(family='Helvetica', size=10)

button_search = Button(root, text="search", width=10, height=1, font=myFont, command=button_search)
button_search.grid(row=1, column=2, padx=10, pady=10)

button_cancel = Button(root, text="Cancel", width=10, font=myFont, command=root.destroy)
button_cancel.grid(row=10, column=1, padx=10, pady=10)

root.mainloop()

