from tkinter import filedialog
import tkinter as tk
from PIL import Image
import ctypes

fontSize = 4

asciiChars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUXYzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

darkMode = False

def fullscreenator(event=None):
    stateAtual = rootWindow.attributes('-fullscreen')
    newState = not stateAtual
    rootWindow.attributes('-fullscreen', newState)

def changeTheme(event=None):
    global darkMode, asciiChars, asciiImage
    
    darkMode = not darkMode
    
    
    asciiChars = asciiChars[::-1]
    
    
    asciiImage = ""
    for i in range(len(pixelsList)):
        index = pixelsList[i] * (len(asciiChars) - 1) // 255
        asciiImage += asciiChars[index]
        if (i + 1) % asciiColumns == 0:
            asciiImage += "\n"
            
    
    if darkMode:
        asciiTextWidget.config(bg="black", fg="white")
        rootWindow.config(bg="black")
    else:
        asciiTextWidget.config(bg="white", fg="black")
        rootWindow.config(bg="white")
        
    
    asciiTextWidget.delete("1.0", tk.END)
    asciiTextWidget.insert("1.0", asciiImage)
    
    if newState:
        scrollY.pack_forget()
        scrollX.pack_forget()
        asciiTextWidget.pack_forget()
        asciiTextWidget.pack(expand=True, fill="both")
    else:
        asciiTextWidget.pack_forget()
        scrollY.pack_forget()
        scrollX.pack_forget()

        scrollY.pack(side="right", fill="y")
        scrollX.pack(side="bottom", fill="x")
        asciiTextWidget.pack(expand=True, fill="both")

rootWindow = tk.Tk()

try:
    myappid = 'project.leshitex.vesion.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

icon = tk.PhotoImage(file="assets/image/Leshitext_icon.png")
rootWindow.iconphoto(True, icon)

rootWindow.withdraw()

filePath = filedialog.askopenfilename(
    title="Select an image",
    filetypes=[("Image", "*.jpg *.jpeg *.png *.bmp *.webp")]
)

if not filePath:
    print("Not an image. Exiting...")
    rootWindow.destroy()
    exit()

originalImage = Image.open(filePath)
originalWidth, originalHeight = originalImage.size

characterWidth = fontSize * 0.6
characterHeight = fontSize * 1.32

asciiColumns = int(originalWidth / characterWidth)
asciiRows = int(originalHeight / characterHeight)

processedImage = originalImage.resize(
    (asciiColumns, asciiRows)
).convert("L")

pixelsList = list(processedImage.getdata())

asciiImage = ""

for i in range(len(pixelsList)):
    index = pixelsList[i] * (len(asciiChars) - 1) // 255
    asciiImage += asciiChars[index]
    if (i + 1) % asciiColumns == 0:
        asciiImage += "\n"

rootWindow.deiconify()
rootWindow.title("Leshitex")
rootWindow.bind("<space>", fullscreenator)
rootWindow.bind("<d>", changeTheme)
rootWindow.bind("<Escape>", exit)
rootWindow.geometry(f"{originalWidth}x{originalHeight}")
rootWindow.resizable(True, True)

scrollY = tk.Scrollbar(rootWindow, orient="vertical")
scrollX = tk.Scrollbar(rootWindow, orient="horizontal")

asciiTextWidget = tk.Text(
    rootWindow,
    wrap="none",
    font=("Courier", fontSize),
    bg="white",
    fg="black",
    bd=0,
    padx=0,
    pady=0,
    highlightthickness=0,
    yscrollcommand=scrollY.set,
    xscrollcommand=scrollX.set
)


scrollY.config(command=asciiTextWidget.yview)
scrollX.config(command=asciiTextWidget.xview)

scrollY.pack(side="right", fill="y")
scrollX.pack(side="bottom", fill="x")
asciiTextWidget.pack(expand=True, fill="both")

asciiTextWidget.insert("1.0", asciiImage)

rootWindow.mainloop()