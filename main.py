from tkinter import messagebox
from Automata import Automata
from EvaluateAutomata import EvaluateAutomata
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from RegexActions import Regex


def draw_circle(canvas, x, y, state_name):
    split_text = state_name.split(",")

    if len(split_text) == 2:
        if split_text[1] == "I" or split_text[1] == "II":
            if not GUI.au.create_state(split_text[0], True, False):
                GUI.draw_circle_aux(canvas, x, y, '#66b3ff', split_text[0])
            else:
                messagebox.showinfo("Alert", "El estado ya existe")
        if split_text[1] == "N":
            if not GUI.au.create_state(split_text[0], False, False):
                GUI.draw_circle_aux(canvas, x, y, '#669999', split_text[0])
            else:
                messagebox.showinfo("Alert", "El estado ya existe")
        if split_text[1] == "F" or split_text[1] =="FF":
            if not GUI.au.create_state(split_text[0], False, True):
                GUI.draw_circle_aux(canvas, x, y, '#99ff99', split_text[0])
            else:
                messagebox.showinfo("Alert", "El estado ya existe")
        if split_text[1] == "IF" or split_text[1] == "FI":
            if not GUI.au.create_state(split_text[0], True, True):
                GUI.draw_circle_aux(canvas, x, y, '#ff66ff', split_text[0])
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


class node_data:
    def __init__(self, x_pos, y_pos, node_name, fill_color, label_id, node_id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.node_name = node_name
        self.fill_color = fill_color
        self.label_id = label_id
        self.node_id = node_id
        self.type = "node"


class edge_data:
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


def convert_nfa_to_dfa():
    GUI.record_state_position = True


def get_text_from_file(save_name):
    text_automtata = ""
    f = open(save_name, "r")

    if f.mode == 'r':
        text_automtata = f.read()

    return text_automtata


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
    # ER->NFAE
    # DFA->ER
    # Resta
    # Complemento
    # Reflexion (regex)

    # DFA
    # NFA
    # NFA->DFA
    # NFA-E
    # NFA-E>DFA
    # Union
    # Interseccion

    # PDA
    # Turing

    drawing_area = None
    au = Automata("nfa")
    pda = Automata("pda")
    state_nodes = []
    transition_edge = []
    edit_states = False
    automataType = None
    nfa_to_dfa_button = None

    automata_type = "Pda"
    shown_transitions = ""
    glc_string_data = ""
    state_position = []
    record_state_position = False



    def __init__(self):
        super().__init__()
        self.init_ui()

    def draw_circle_aux(canv, x, y, fill_color, label_text):

        oval_id = canv.create_oval(x - 25, y - 25, x + 25, y + 25, width=0, fill=fill_color, tags="label_text")
        text_id = canv.create_text(x, y, text=label_text, font=("Purisa", 12))
        GUI.state_nodes.append(node_data(x, y, label_text, fill_color, text_id, oval_id))

    def init_ui(self):
        self.master.title("Pythomatas: Pfa")
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=710, y=560)
        GUI.drawing_area = Canvas(bg="#cccccc", height=520, width=760)
        self.drawing_area.place(x=20, y=20)

        new_transition_button = Button(self, text="New Transiton", command=self.create_transition_aux)
        new_transition_button.place(x=20, y=549)

        test_input = Entry(self, width=25)
        test_input.place(x=20, y=590)

        test_string_button = Button(self, text="Test String", command=lambda: self.test_string_fun(test_input.get()))
        test_string_button.place(x=200, y=590)

        delete_button = Button(self, text="Delete", command=self.change_edit_state)
        delete_button.place(x=115, y=549)

        state_pos = Button(self, text="State position", command=convert_nfa_to_dfa)
        state_pos.place(x=200, y=549)

        dfa_to_regex_button = Button(self, text="Switch", command=self.switch_automata)
        dfa_to_regex_button.place(x=800, y=20)

        nfa_to_dfa_button = Button(self, text="To DFA", command=self.nfa_to_dfa)
        nfa_to_dfa_button.place(x=800, y=50)

        nfae_to_dfa_button = Button(self, text="NFA-ε to DFA", command=self.convert_nfae_to_dfa)
        nfae_to_dfa_button.place(x=800, y=80)

        save_automata_button = Button(self, text="Save automata", command=self.save_automata)
        save_automata_button.place(x=800, y=490)

        load_automata_button = Button(self, text="Load automata", command=self.load_automata)
        load_automata_button.place(x=800, y=520)

        clear_all_button = Button(self, text="Clear", command=lambda: self.clear_canvas(True))
        clear_all_button.place(x=800, y=460)

        union_button = Button(self, text="Union", command=lambda: self.automata_operations("u"))
        union_button.place(x=800, y=130)

        compliment_button = Button(self, text="Compliment", command=lambda: self.automata_operations("c"))
        compliment_button.place(x=880, y=160)

        reflexion_button = Button(self, text="Reflexion", command=lambda: self.automata_operations("r"))
        reflexion_button.place(x=800, y=160)

        intersection_button = Button(self, text="Intersection", command=lambda: self.automata_operations("i"))
        intersection_button.place(x=880, y=130)

        show_new_drawing_area_button = Button(self, text="Show PDA Data", command=lambda: self.show_new_area(True))
        show_new_drawing_area_button.place(x=800, y=410)

        pda_to_glc = Button(self, text="PDA to GLC", command=self.pda_to_glc)
        pda_to_glc.place(x=800, y=350)

        glc_to_pda = Button(self, text="GLC to PDA", command=lambda: self.show_new_area(False))
        glc_to_pda.place(x=800, y=380)

    def pda_to_glc(self):
        result = EvaluateAutomata().pda_to_glc(self.au)
        if result:
            GUI.glc_string_data = result
            self.show_new_area(False)

    def automata_operations(self, operation):
        result = EvaluateAutomata().automata_operations(self.au, operation)
        self.clear_canvas(False)

        self.generate_text_automata(result)

    def minimize_automata(self):
        result = self.au.minimize()
        self.clear_canvas(False)
        self.generate_text_automata(result)

    def show_new_area(self, data):
        t = Toplevel(self)
        t.geometry('%dx%d+%d+%d' % (760, 520, 480, 250))
        t.wm_title("Data")

        text_area = Text(t, bg="#cccccc", height=29, width=90)
        text_area.place(x=10, y=10)

        text_area.insert(END, GUI.glc_string_data)

        if not data:
            save_text_button = Button(t, text="Create PDA", command=lambda: self.glc_to_pda(text_area.get("1.0", END)))
            save_text_button.place(x=645, y=480)
            load_glc_button = Button(t, text="Load GLC", command=self.load_glc)
            load_glc_button.place(x=545, y=480)
        else:
            text_area = Text(t, bg="#cccccc", height=29, width=90)
            text_area.place(x=10, y=10)
            text_area.insert(END, GUI.au.get_pda_transitions())

        save_glc_button = Button(t, text="Save GLC", command=lambda: self.save_glc(text_area.get("1.0", END)))
        save_glc_button.place(x=450, y=480)

    def glc_to_pda(self, glc_data):

        clean_glc_data = ""

        for gd in glc_data:
            if gd == " " or gd == "[" or gd == "]":
                pass
            else:
                clean_glc_data += gd

        print(clean_glc_data)

        result = EvaluateAutomata().glc_to_pda(clean_glc_data)
        print(result)
        self.clear_canvas(True)
        GUI.state_position.append([150, 300])
        GUI.state_position.append([400, 300])
        GUI.state_position.append([650, 300])
        self.generate_text_automata(result)

    def load_glc(self):
        glc_text = askopenfilename()
        if glc_text:
            automata_text = get_text_from_file(glc_text)
            self.glc_to_pda(automata_text)

    def test_regex(self, regex_string):

        test_string = askstring('Insert string', " ")


        if test_string:

            result = Regex(regex_string).text_match(test_string, regex_string)

            if result:
                messagebox.showinfo("Result", "La cadena fue aceptada")
            else:
                messagebox.showinfo("Result", "La cadena no fue aceptada")

                # regex.split_parenthesis(regex_string)

    def switch_automata(self):
        if GUI.automata_type == "Nfa":
            GUI.automata_type = "Pda"
            self.master.title("Pythomatas: " + GUI.automata_type)
            self.clear_canvas(True)
        elif GUI.automata_type == "Pda":
            GUI.automata_type = "Turing"
            self.master.title("Pythomatas: " + GUI.automata_type)
            self.clear_canvas(True)
        elif GUI.automata_type == "Turing":
            GUI.automata_type = "Nfa"
            self.master.title("Pythomatas: " + GUI.automata_type)
            self.clear_canvas(True)

    def nfa_to_dfa(self):
        result = EvaluateAutomata().nfa_to_dfa(self.au)
        self.clear_canvas(False)
        self.generate_text_automata(result)

    def convert_nfae_to_dfa(self):
        result = EvaluateAutomata().nfae_to_dfa(self.au)
        self.clear_canvas(False)
        self.generate_text_automata(result)

    def save_automata(self):
        file_name = askstring('File name', "")

        if file_name:
            if GUI.automata_type == "Pda":
                if self.au.save_pda_automata(file_name, "y"):
                    messagebox.showinfo("Result", "El automata se salvo")
            else:
                if self.au.save_automata(file_name, "y"):
                    messagebox.showinfo("Result", "El automata se salvo")

    def create_self_transition(self, transition_char, x, y, state, node_id):

        text_id = GUI.drawing_area.create_text(x, y-50, text=transition_char, font=("Purisa", 12))
        edge_left_id = GUI.drawing_area.create_line(x-18, y-18, x-15, y-40, tags=("line",))
        edge_top_id = GUI.drawing_area.create_line(x-15, y-40, x+15, y-40, tags=("line",))
        edge_right_id = GUI.drawing_area.create_line(x+15, y-40, x+18, y-20, tags=("line",), arrow="last")

        self.state_nodes.append(edge_data(node_id, node_id, x-18, y-18, x-15, y-40, transition_char, text_id,
                                          edge_left_id, state, state))
        self.state_nodes.append(edge_data(node_id, node_id, x-15, y-40, x+15, y-40, transition_char, text_id,
                                          edge_top_id, state, state))
        self.state_nodes.append(edge_data(node_id, node_id, x+15, y-40, x+18, y-20, transition_char, text_id,
                                          edge_right_id, state, state))

    def load_automata(self):
        f_name = askopenfilename()
        if f_name:
            automata_text = get_text_from_file(f_name)
            self.generate_text_automata(automata_text)

    def save_glc(self, glc_text):
        file_name = askstring('File name', "")

        if file_name:
            EvaluateAutomata().save_glc(file_name, glc_text)

    def change_edit_state(self):
        if GUI.edit_states:
            GUI.edit_states = False
            self.master.title("Pythomatas")
        else:
            GUI.edit_states = True
            self.master.title("Pythomatas Edit*")

    def create_transition_aux(self):

        if GUI.automata_type == "Pda":
            transition_data = askstring('Insert Transition', "a,b,char,pop,push")
        else:
            transition_data = askstring('Insert Transition', "a,0,b")

        if transition_data:
            ntd = transition_data.split(",")

            if len(ntd) == 3:
                if self.au.create_transition(ntd[0], ntd[2], ntd[1]):
                    self.draw_line(ntd[0], ntd[2], ntd[1])
                else:
                    messagebox.showinfo("Info", "La transision no se creo")
            else:
                if self.au.create_pda_transition(ntd[0], ntd[1], ntd[2], ntd[3], ntd[4]):
                    self.draw_line(ntd[0], ntd[1], ntd[2] + "," + ntd[3] + "/" + ntd[4])
                else:
                    messagebox.showinfo("Info", "La transision no se creo")

    def draw_line(self, state1, state2, transition_char):
        x1, y1, node_id1 = self.get_state_data(state1)
        x2, y2, node_id2 = self.get_state_data(state2)

        if node_id1 == node_id2:
            self.create_self_transition(transition_char, x1, y1, state1, node_id1)
            return

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

    def get_state_data(self, state_name):
        for sn in self.state_nodes:
            if sn.type == "node":
                if sn.node_name == state_name:
                    return sn.x_pos, sn.y_pos, sn.node_id

    def test_string_fun(self, test_string):
        # test_string = askstring('Insert test string', "")

        if test_string:
            if GUI.automata_type == "Pda":
                result = False #EvaluateAutomata().evaluate_pda(test_string, self.au)
            else:
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
                        if sn.node_origin == item[0] or sn.node_destiny == item[0]:
                            # GUI.drawing_area.delete(sn.char_id)
                            GUI.drawing_area.delete(sn.edge_id)

            if object_type == "edge":

                if GUI.automata_type == "pda":
                    GUI.au.delete_pda_transition(state_name, element1, element2)
                    GUI.drawing_area.delete(c_id)
                    GUI.drawing_area.delete(e_id)
                    del GUI.state_nodes[i]
                else:
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

    def generate_text_automata(self, automata_text):

        state_transition_division = automata_text.split("*")
        states_division = state_transition_division[0].split("|")
        transition_division = state_transition_division[1].split("|")

        GUI.shown_transitions = transition_division

        i = 0
        for sd in states_division:
            draw_circle(self.drawing_area, self.state_position[i][0], self.state_position[i][1], sd)
            i += 1

        for td in transition_division:
            ntd = td.split(",")
            if GUI.automata_type == "Pda":
                self.au.create_pda_transition(ntd[0], ntd[4], ntd[1], ntd[2], ntd[3])
                self.draw_line(ntd[0], ntd[4], ntd[1] + "," + ntd[2] + "/" + ntd[3])
            else:
                self.au.create_transition(ntd[0], ntd[2], ntd[1])
                self.draw_line(ntd[0], ntd[2], ntd[1])

    def get_mouse_data(event):
        if GUI.record_state_position:
            GUI.global_x = event.x
            GUI.global_y = event.y
            GUI.state_position.append([GUI.global_x, GUI.global_y])

    def test_event_state(event):
        messagebox.showinfo("Result", "La cadena fue aceptada")

    def clear_canvas(self, full_clear):

        self.drawing_area.delete(ALL)
        GUI.state_nodes = []
        GUI.au = Automata("Pfa")
        GUI.transition_edge = []

        if full_clear:
            GUI.state_position = []

    def print_states_transitions(self):
        self.au.list_transitions()
        self.au.list_states()

def main():
    root = Tk()
    app = GUI()
    GUI.drawing_area.bind("<Double-Button-1>", GUI.canvas_operations)
    GUI.drawing_area.bind("<Button-1>", GUI.get_mouse_data, GUI.drawing_area)
    root.bind("<Button-3>", GUI.test_event_state)

    root.mainloop()


if __name__ == '__main__':
    main()
