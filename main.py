from tkinter import *
from PIL import Image, ImageTk

# Gif stuff
class MyLabel(Label):
    def __init__(self, master, filename, delayms, bg, loop, x, y):
        super().__init__(master)  # Call Label constructor with master widget
        im = Image.open(filename)
        seq = []
        self.delay = 10
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq))  # skip to next frame
        except EOFError:
            pass  # we're done

        try:
            self.delay = delayms  # im.info['duration']
        except KeyError:
            self.delay = 10

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]
        self.canvas = Canvas(master, bg=bg, height=500, width=500, highlightthickness=0)
        self.canvas.place(relx=x, rely=y, anchor='center')
        self.image_item = self.canvas.create_image(0, 0, image=self.frames[0], anchor='nw')

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = image.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0
        self.cancel = self.after(self.delay, self.play)
        self.loop = loop

    def stop(self):
        self.after_cancel(self.cancel)
        self.canvas.destroy()

    def play(self):
        if self.loop:
            self.canvas.itemconfig(self.image_item, image=self.frames[self.idx])
            self.idx += 1
            if self.idx == len(self.frames):
                self.idx = 0
            self.cancel = self.after(self.delay, self.play)
        else:
            for i, a in enumerate(self.frames):
                time.sleep(0.04)
                self.canvas.itemconfig(self.image_item, image=self.frames[i])
                self.canvas.update_idletasks()
            print('Finished')


root = Tk()
root.geometry("500x500")
anim = MyLabel(root, 'Fail1.gif', 50, 'white', True, 0.5, 0.5)
anim.pack()
root.mainloop()
