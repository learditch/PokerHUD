import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageEnhance

root = tk.Tk()
root.resizable(0, 0)

def show_image(image):
    win = tk.Toplevel()
    win.image = ImageTk.PhotoImage(image)
    tk.Label(win, image=win.image).pack()
    win.grab_set()
    win.wait_window(win)

def area_sel():
    x1 = y1 = x2 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image') # remove old overlay image
        roi_image = image.crop((x1, y1, x2, y2)) # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        canvas.coords('roi', x1, y1, x2, y2)
        # make sure the select rectangle is on top of the overlay image
        canvas.lift('roi') 

    root.withdraw()  # hide the root window
    image = ImageGrab.grab()  # grab the fullscreen as select region background
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
    # create a fullscreen window to perform the select region action
    win = tk.Toplevel()
    win.attributes('-fullscreen', 1)
    win.attributes('-topmost', 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
    # bind the mouse events for selecting region
    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', lambda e: win.destroy())
    # use Esc key to abort the capture
    win.bind('<Escape>', lambda e: win.destroy())
    # make the capture window modal
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()  # restore root window
    # show the capture image
    if roi_image:
        show_image(roi_image)

tk.Button(root, text='select area', width=30, command=area_sel).pack()

root.mainloop()