from tkinter import filedialog
import tkinter as tk
from PIL import Image

fontSize = 4

asciiChars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUXYzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

rootWindow = tk.Tk()
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
rootWindow.title("ASCIINATOR")
rootWindow.attributes('-fullscreen', True)
rootWindow.bind("<Escape>", exit)
rootWindow.geometry(f"{originalWidth}x{originalHeight}")
rootWindow.resizable(False, False)

asciiTextWidget = tk.Text(
    rootWindow,
    wrap="none",
    font=("Courier", fontSize),
    bg="black",
    fg="white",
    bd=0,
    padx=0,
    pady=0,
    highlightthickness=0
)

asciiTextWidget.insert("1.0", asciiImage)

asciiTextWidget.pack(expand=True, fill="both")

rootWindow.mainloop()