from tkinter import messagebox

from Automata import Automata
from EvaluateAutomata import EvaluateAutomata
from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

drawing_area = None
au = Automata("dfa")


def draw_circle(canv, x, y, state_name):
    split_text = state_name.split(",")

    if split_text[1] == "I":
        if not au.create_state(split_text[0], False, False):
            draw_circle_aux(canv, x, y, '#66b3ff', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")
    if split_text[1] == "N":
        if not au.create_state(split_text[0], True, False):
            draw_circle_aux(canv, x,y, '#669999', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")
    if split_text[1] == "F":
        if not au.create_state(split_text[0], False, True):
            draw_circle_aux(canv, x, y, '#99ff99', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")

    text_state = split_text[0] + "," + str(x) + "," + str(y) + "|"
    GUI.state_positions += text_state


def draw_circle_aux(canv, x, y, fill_color, label_text):
    canv.create_oval(x - 25, y - 25, x + 25, y + 25, width=0, fill=fill_color)
    canv.create_text(x, y, text=label_text, font=("Purisa", 12))


class node_data():
    def __init__(self, x_pos, y_pos, node_name, fill_color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.node_name = node_name
        self.fill_color = fill_color


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
    # DFA
    # NFA
    # NFA->DFA
    # NFA-E
    # NFA-E>DFA

    state_positions = ""
    state_node = []
    transition_edge = []

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # au.generate_automata("a,I|b,F*a,0,a|a,1,a|a,1,b")
        self.master.title("Pythomatas")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=710, y=560)
        GUI.drawing_area = Canvas(bg="#cccccc", height=520, width=760)
        GUI.drawing_area.place(x=20, y=20)

        new_transition_button = Button(self, text="New Transiton", command=self.create_transition_aux)
        new_transition_button.place(x=20, y=549)

        test_string_button = Button(self, text="Test String", command=self.test_string_fun)
        test_string_button.place(x=20, y=579)

        # GUI.drawing_area.create_oval(50, 50, 20, 20, width=0, fill='#99ff99')

    def create_transition_aux(self):
        transition_data = askstring('Insert Transition', "a,0,b")
        ntd = transition_data.split(",")
        au.create_transition(ntd[0], ntd[2], ntd[1])
        self.draw_line(ntd[0], ntd[2], ntd[1])

    def draw_line(self, state1, state2, transition_char):
        x1, y1 = self.get_state_data(state1)
        x2, y2 = self.get_state_data(state2)

        tlx = (int(x1) + int(x2)) / 2
        tly = (int(y1) + int(y2)) / 2

        GUI.drawing_area.create_text(tlx, tly, text=transition_char, font=("Purisa", 12))

        if int(x1) < int(x2):
            if (int(y1) < int(y2)):
                GUI.drawing_area.create_line(int(x1) + 15, int(y1) + 15, int(x2) - 15, int(y2) - 15, tags=("line",),
                                             arrow="last")
            else:
                GUI.drawing_area.create_line(int(x1) + 15, int(y1) - 15, int(x2) - 15, int(y2) + 15, tags=("line",),
                                             arrow="last")
        else:
            if (int(y1) < int(y2)):
                GUI.drawing_area.create_line(int(x1) - 15, int(y1) + 15, int(x2) + 15, int(y2) - 15, tags=("line",),
                                             arrow="last")
            else:
                GUI.drawing_area.create_line(int(x1) - 15, int(y1) - 15, int(x2) + 15, int(y2) + 15, tags=("line",),
                                             arrow="last")

    def move_node(event):
        print("x: " + str(event.x) + " y: " + str(event.y))
        GUI.drawing_area.move(ALL, 1, 1)

    def get_state_data(self, state_name):
        my_state_positions = self.state_positions.split("|")

        for ssp in my_state_positions:
            new_ssp = ssp.split(",")
            if new_ssp[0] == state_name:
                return new_ssp[1], new_ssp[2]

    def test_string_fun(self):
        test_string = askstring('Insert test string', "")
        result = EvaluateAutomata().evaluate_nfa(test_string, au)

        if result:
            messagebox.showinfo("Result", "La cadena fue aceptada")
        else:
            messagebox.showinfo("Result", "La cadena no fue aceptada")

    def callback(event):
        state_name = askstring('State name', 'a,I')

        if state_name:
            draw_circle(GUI.drawing_area, event.x, event.y, state_name)

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
    # root.bind("<B1-Motion>", GUI.move_node)
    app = GUI()
    root.mainloop()


if __name__ == '__main__':
    main()
