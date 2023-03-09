from tkinter import *
from PIL import Image, ImageTk

class MyLabel(Label):
    def __init__(self, master, filename, delayms):
        im = Image.open(filename)
        seq =  []
        self.delay = 10
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay =  delayms#im.info['duration']
        except KeyError:
            self.delay = 10

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = image.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)


root = Tk()
anim = MyLabel(root, 'Fail1.gif', 50)
anim.pack()
root.mainloop()