from tkinter import messagebox
from Automata import Automata
from EvaluateAutomata import EvaluateAutomata
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring


def draw_circle(canv, x, y, state_name):
    split_text = state_name.split(",")

    if split_text[1] == "I":
        if not GUI.au.create_state(split_text[0], True, False):
            GUI.draw_circle_aux(canv, x, y, '#66b3ff', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")
    if split_text[1] == "N":
        if not GUI.au.create_state(split_text[0], False, False):
            GUI.draw_circle_aux(canv, x, y, '#669999', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")
    if split_text[1] == "F":
        if not GUI.au.create_state(split_text[0], False, True):
            GUI.draw_circle_aux(canv, x, y, '#99ff99', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")
    if split_text[1] == "IF":
        if not GUI.au.create_state(split_text[0], True, True):
            GUI.draw_circle_aux(canv, x, y, '#99ff99', split_text[0])
        else:
            messagebox.showinfo("Alert", "El estado ya existe")


def get_all_state_components(item_id):

    i = 0

    for sc in GUI.state_nodes:
        if sc.type == "node":
            if item_id == sc.label_id or item_id == sc.node_id:
                return sc.type, sc.node_name, sc.label_id, sc.node_id, 0, 0, i
            i += 1
        else:
            if item_id == sc.char_id or item_id == sc.edge_id:
                return sc.type, sc.node_origin_name, sc.transition_char, sc.node_destiny_name, sc.char_id, sc.edge_id, i
            i += 1

class node_data():
    def __init__(self, x_pos, y_pos, node_name, fill_color, label_id, node_id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.node_name = node_name
        self.fill_color = fill_color
        self.label_id = label_id
        self.node_id = node_id
        self.type = "node"

class edge_data():
    def __init__(self, node_origin_id, node_destiny_id, x_pos_a, y_pos_a, x_pos_b, y_pos_b, transition_char,
                 char_id, edge_id, node_origin_name, node_destiny_name):
        self.node_origin = node_origin_id
        self.node_destiny = node_destiny_id
        self.transition_char = transition_char
        self.char_id = char_id
        self.edge_id = edge_id
        self.node_origin_name = node_origin_name
        self.node_destiny_name = node_destiny_name
        self.x_pos_a = x_pos_a
        self.y_pos_a = y_pos_a
        self.x_pos_b = x_pos_b
        self.y_pos_b = y_pos_b
        self.type = "edge"


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

    drawing_area = None
    au = Automata("nfa")
    state_nodes = []
    transition_edge = []
    edit_states = False
    automataType = None
    nfa_to_dfa_button = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def draw_circle_aux(canv, x, y, fill_color, label_text):

        oval_id = canv.create_oval(x - 25, y - 25, x + 25, y + 25, width=0, fill=fill_color, tags="label_text")
        text_id = canv.create_text(x, y, text=label_text, font=("Purisa", 12))
        GUI.state_nodes.append(node_data(x, y, label_text, fill_color, text_id, oval_id))

    def init_ui(self):

        # au.generate_automata("a,I|b,F*a,0,a|a,1,a|a,1,b")
        self.master.title("Pythomatas")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=710, y=560)
        GUI.drawing_area = Canvas(bg="#cccccc", height=520, width=760)
        self.drawing_area.place(x=20, y=20)

        new_transition_button = Button(self, text="New Transiton", command=self.create_transition_aux)
        new_transition_button.place(x=20, y=549)

        test_string_button = Button(self, text="Test String", command=self.test_string_fun)
        test_string_button.place(x=20, y=579)

        new_transition_button = Button(self, text="Edit states", command=self.change_edit_state)
        new_transition_button.place(x=115, y=549)

        nfa_to_dfa_button = Button(self, text="NFA -> DFA", command=self.convert_nfa_to_dfa)
        nfa_to_dfa_button.place(x=200, y=549)
  #      nfa_to_dfa_button.place_forget()

        GUI.automataType = IntVar()

        radio_1 = Radiobutton(self.master, text="DFA", variable=self.automataType, value=1, command=self.choose_automata)
        radio_1.place(x=800, y=20)
        radio_2 = Radiobutton(self.master, text="NFA", variable=self.automataType, value=2, command=self.choose_automata)
        radio_2.place(x=800, y=40)

        save_automata_button = Button(self, text="Save automata", command=self.save_automata)
        save_automata_button.place(x=800, y=490)

        load_automata_button = Button(self, text="Load automata", command=self.load_automtata)
        load_automata_button.place(x=800, y=520)

    def save_automata(self):
        file_name = askstring('File name', "")
        if file_name:
            if self.au.save_automata(file_name):
                messagebox.showinfo("Result", "El automata se salvo")

    def load_automtata(self):

        f_name = askopenfilename()
        print(f_name)
        if f_name:
            if self.au.load_automata(f_name):
                messagebox.showinfo("Result", "El automata se cargo")


    def choose_automata(self):
        selection = str(self.automataType.get())
        if selection == 1:
            GUI.au = Automata("dfa")
            GUI.nfa_to_dfa_button.place_forget()
        elif selection == 2:
            GUI.au = Automata("nfa")

    def convert_nfa_to_dfa(self):
        self.au.save_automata()
        return EvaluateAutomata().nfa_to_dfa(GUI.au)

    def change_edit_state(self):
        if GUI.edit_states:
            GUI.edit_states = False
            self.master.title("Pythomatas")
        else:
            GUI.edit_states = True
            self.master.title("Pythomatas Edit*")

    def create_transition_aux(self):
        transition_data = askstring('Insert Transition', "a,0,b")

        if transition_data:
            ntd = transition_data.split(",")
            if self.au.create_transition(ntd[0], ntd[2], ntd[1]):
               self.draw_line(ntd[0], ntd[2], ntd[1])
            else:
                messagebox.showinfo("Info", "La transision no se creo")

    def draw_line(self, state1, state2, transition_char):
        x1, y1, node_id1 = self.get_state_data(state1)
        x2, y2, node_id2 = self.get_state_data(state2)

        tlx = (int(x1) + int(x2)) / 2
        tly = (int(y1) + int(y2)) / 2

        text_id = GUI.drawing_area.create_text(tlx, tly, text=transition_char, font=("Purisa", 12))

        if int(x1) < int(x2):
            if int(y1) < int(y2):
                xa = int(x1) + 15
                ya = int(y1) + 15
                xb = int(x2) - 15
                yb = int(y2) - 15
            else:
                xa = int(x1) + 15
                ya = int(y1) - 15
                xb = int(x2) - 15
                yb = int(y2) + 15
        else:
            if int(y1) < int(y2):
                xa = int(x1) - 15
                ya = int(y1) + 15
                xb = int(x2) + 15
                yb = int(y2) - 15
            else:
                xa = int(x1) - 15
                ya = int(y1) - 15
                xb = int(x2) + 15
                yb = int(y2) + 15

        edge_id = GUI.drawing_area.create_line(xa, ya, xb, yb, tags=("line",), arrow="last")
        self.state_nodes.append(edge_data(node_id1, node_id2, xa, ya, xb, yb, transition_char, text_id, edge_id,
                                          state1, state2))

    def move_node(event):
        GUI.drawing_area.move(ALL, 1, 1)

    def get_state_data(self, state_name):
        for sn in self.state_nodes:
            if sn.type == "node":
                if sn.node_name == state_name:
                    return sn.x_pos, sn.y_pos, sn.node_id

    def test_string_fun(self):
        test_string = askstring('Insert test string', "")

        if test_string:
            result = EvaluateAutomata().evaluate_nfa_e(test_string, self.au)

            if result:
                messagebox.showinfo("Result", "La cadena fue aceptada")
            else:
                messagebox.showinfo("Result", "La cadena no fue aceptada")

    def canvas_operations(event):
        if GUI.edit_states:
            GUI.delete_drawn_object(event)
        else:
            GUI.create_node(event)

    def create_node(event):
        state_name = askstring('State name', 'a,I')

        if state_name:
            draw_circle(GUI.drawing_area, event.x, event.y, state_name)

    def delete_drawn_object(event):
        item = GUI.drawing_area.find_closest(event.x, event.y)
        if len(item) is not 0:
            object_type, state_name, element1, element2, c_id, e_id, i = get_all_state_components(item[0])

            if object_type == "node":
                GUI.au.delete_state(state_name)
                GUI.drawing_area.delete(element1)
                GUI.drawing_area.delete(element2)
                del GUI.state_nodes[i]

                for sn in GUI.state_nodes:
                    if sn.type == "edge":
                        GUI.drawing_area.delete(sn.char_id)
                        GUI.drawing_area.delete(sn.edge_id)

            else:
                print(str(state_name) + " ," + str(element1) + ", " + str(element2))
                GUI.au.delete_transition(state_name, element1, element2)
                GUI.drawing_area.delete(c_id)
                GUI.drawing_area.delete(e_id)
                del GUI.state_nodes[i]

    def center_window(self):
        w = 1000
        h = 650
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))



def main():
    root = Tk()
    app = GUI()
    GUI.drawing_area.bind("<Double-Button-1>", GUI.canvas_operations)
    # root.bind("<B1-Motion>", GUI.move_node)
    root.mainloop()


if __name__ == '__main__':
    main()
