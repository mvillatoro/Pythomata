from Automata import Automata
from EvaluateAutomata import EvaluateAutomata
from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

drawing_area = None
au = Automata("dfa")

def draw_circle(canv, x, y, rad, stateName):
    split_text = stateName.split(",")
    if split_text[1] == "N":
        au.create_state(split_text[0], False, False)
        canv.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='#669999')
    elif split_text[1] == "I":
        au.create_state(split_text[0], True, False)
        canv.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='#66b3ff')
    elif split_text[1] == "F":
        au.create_state(split_text[0], False, True)
        canv.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='#99ff99')

    au.list_states()

    canv.create_text(x, y, text=split_text[0], font=("Purisa", 12))

class GUI(Frame):
    """
    def __init__(self):
        # au = Automata("dfa")
        au = Automata("nfa")

        # au.generate_automata("a,I|b,N|c,F|d,N|e,N|f,N|g,N|h,N*a,0,b|a,1,f|b,1,c|b,0,g|c,1,c|c,0,a|d,0,c|d,1,g|e,1,
        # f|e,0,h|f,1,g|f,0,c|g,0,g|g,1,e|h,0,g|h,1,c")  #000000000010111111



        au.generate_automata("a,I|b,F*a,0,a|a,1,a|a,1,b")

        if EvaluateAutomata().evaluate_dfa("1", au):
            print("Acepta")
        else:
            print("NO acepta")
"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.master.title("Pythomatas")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=710, y=560)
        GUI.drawing_area = Canvas(bg="#cccccc", height=520, width=760)
        GUI.drawing_area.place(x=20, y=20)

        new_transition_button = Button(self, text="New Transiton", command=self.create_transition_aux)
        new_transition_button.place(x=150, y=549)

        test_string_button = Button(self, text="Test String", command=self.test_string_fun)
        test_string_button.place(x=150, y=579)

    def create_transition_aux(self):
        transition_data = askstring('Insert Transition', "a,0,b")
        ntd = transition_data.split(",")
        au.create_transition(ntd[0], ntd[2], ntd[1])


    def test_string_fun(self):
        test_string = askstring('Insert test string',"")
        result = EvaluateAutomata().evaluate_dfa(test_string, au)

        if result:
            print("acepta")
        else:
            print("no acepta")

    def callback(event):
        state_name = askstring('State name', 'a,I')
        draw_circle(GUI.drawing_area, event.x,event.y, 25, state_name)

    def center_window(self):
        w = 800
        h = 650
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    # root.bind('<Motion>', GUI.motion)
    root.bind("<Double-Button-1>", GUI.callback)
    app = GUI()
    root.mainloop()


if __name__ == '__main__':
    main()


