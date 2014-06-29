#! /usr/bin/env python3

from tkinter import *
from time import ctime, time

def frame(root, side):
    w = Frame(root)
    w.pack(side = side, expand = "yes", fill = "both")
    return w

def button(root, side, text, command = None):
    w = Button(root, text = text, command = command, padx = 10, pady = 20)
    w.pack(side = side)
    return w

class AnnouncementFrame(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.config(padx = 15, pady = 15)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title('Phrase rating system')
        self.iconname('phrase_rater')

        encompassing_frame = frame(self, 'top')
        encompassing_frame.pack(expand = 'yes', fill = 'both')
        smaller_frame = Frame(encompassing_frame, borderwidth = 0, relief = 'groove')
        smaller_frame.place(relx = 0.5, rely = 0.5, y = -5, anchor = 'center')
        phrase_frame = frame(smaller_frame, 'top')
        phrase_frame.config(padx = 25, pady = 25)
        Label(phrase_frame, text = """You will be shown a phrase.
Please read it to yourself.
(It is important that you don’t read it aloud.)
Try to read at your natural pace. 
As soon as you’ve read and understood the phrase,
press “Enter” or click anywhere on the screen.""", justify = 'left', font=('Georgia', 18)).pack(side = 'top')
        button_frame = frame(smaller_frame, 'top')
        next = button(button_frame, 'top', 'Ready', self.destroy)

class RaterPhrame(Tk):
    def __init__(self, filename):
        with open(filename, 'r') as inp:
            lines = inp.readlines()
        phrases = [el.strip('\n') for el in lines]
        self.phrases = list(reversed(phrases))
        self.responses = []

        Tk.__init__(self)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.rateFrame = Frame(self, borderwidth = 0)
        self.rateFrame.config(width = self.winfo_screenwidth(), height = self.winfo_screenheight())
        self.rateFrame.place(x = 0, y = 0)
        smaller_frame = Frame(self.rateFrame, borderwidth = 0, relief = 'groove', width = 350, height = 320)
        smaller_frame.pack_propagate(0)
        smaller_frame.place(relx = 0.5, rely = 0.5, anchor = 'center')
        Label(smaller_frame, text = """How natural was this phrase? 
5 – Absolutely natural, I’d say it myself.
4 – You can hear people saying this.
3 – Not very natural.
2 – Not natural at all, but still
understandable.
1 – The phrase is incorrect.""", font = ('Georgia', 18), pady = 25, justify = 'left').pack(side = 'top')
        radio_frame = frame(smaller_frame, 'top')
        radio_sub_frame = Frame(radio_frame)
        radio_sub_frame.place(relx = 0.5, rely = 0.5, anchor = 'center')
        ratings = ['1', '2', '3', '4', '5']
        self.rating = StringVar()
        self.rating.set(None)
        for r in ratings:
            b = Radiobutton(radio_sub_frame, text = r, variable = self.rating, value = r)
            b.pack(anchor = 'w', side = 'left')
        next_frame = frame(smaller_frame, 'top')
        next_frame.config(pady = 20)
        next = self.button(next_frame, 'top', 'Next sentence', self.process_next_phrase)

        self.responseFrame = Frame(self)
        self.responseFrame.config(width = self.winfo_screenwidth(), height = self.winfo_screenheight())
        self.responseFrame.place(x = 0, y = 0)
        smaller_frame = Frame(self.responseFrame, borderwidth = 0, relief = 'groove')
        smaller_frame.place(relx = 0.5, rely = 0.5, y = -5, anchor = 'center')
        phrase_frame = frame(smaller_frame, 'top')
        phrase_frame.config(padx = 25, pady = 25)
        self.current_phrase = self.phrases.pop()
        self.label = Label(phrase_frame, text = self.current_phrase, justify = 'center', font=('Georgia', 24))
        self.label.pack(side = 'top')
        self.current_time = time()
        # button_frame = frame(smaller_frame, 'top')
        # button_frame.config(padx = 10, pady = 10)
        # # next = self.button(button_frame, 'top', 'Ready', self.measure_response_time_and_rate)
        self.responseFrame.focus_set()
        self.responseFrame.bind('<Return>', self.measure_response_time_and_rate)
        self.responseFrame.bind('<Button-1>', self.measure_response_time_and_rate)
        phrase_frame.bind('<Button-1>', self.measure_response_time_and_rate)
        self.label.bind('<Button-1>', self.measure_response_time_and_rate)

    def measure_response_time_and_rate(self, event):
        self.processing_time = time() - self.current_time
        self.rateFrame.lift()

    def process_next_phrase(self):
        self.responses.append("Phrase: %s, processing_time: %.2f, rating: %s.\n" % (self.current_phrase, self.processing_time, self.rating.get()))
        if len(self.phrases) == 0:
            new_filename = 'phrase_ratings_' + str(ctime()).replace(' ', '_').replace(':', '-') + '.txt'
            with open(new_filename, 'w', encoding = 'utf-8') as out:
                out.writelines(sorted(self.responses))
            announcement = Frame(self)
            announcement.config(width = self.winfo_screenwidth(), height = self.winfo_screenheight())
            announcement.place(x = 0, y = 0)
            smaller_frame = Frame(announcement, borderwidth = 0, relief = 'groove')
            smaller_frame.place(relx = 0.5, rely = 0.5, y = -5, anchor = 'center')
            phrase_frame = frame(smaller_frame, 'top')
            phrase_frame.config(padx = 25, pady = 25)
            Label(phrase_frame, text = 'That was all, thank you for your time!', justify = 'center', font=('Georgia', 24)).pack(side = 'top')
            button_frame = frame(smaller_frame, 'top')
            button_frame.config(padx = 10, pady = 10)
            next = self.button(button_frame, 'top', 'Quit', self.destroy)
        else:
            self.current_time = time()
            self.current_phrase = self.phrases.pop()
            self.label.config(text = self.current_phrase)
            self.rating.set(None)
            self.responseFrame.lift()
            self.responseFrame.focus_set()

    def button(self, root, side, text, command):
        w = Button(root, text = text, command = command, padx = 20, pady = 10)
        w.pack(side = side)
        return w

if len(sys.argv) == 1:
    print('Usage: python3 phraseRater.py <file_with_phrases>')
    sys.exit(1)

af = AnnouncementFrame()
af.mainloop()

rf = RaterPhrame(sys.argv[1])
rf.mainloop()
