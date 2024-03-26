# Stack Class
from collections import deque
import tkinter as tk
from tkinter import messagebox

class Stack:
    def __init__(self):
        self.items = deque()

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return "$"

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return "$"

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# Transition PDA Class


class Transition:
    def __init__(self, current, read, pop, pop2, next, push, push2):
        self.current = current
        self.read = read
        self.pop = pop
        self.pop2 = pop2  
        self.next = next
        self.push = push
        self.push2 = push2 



class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.nextStates = []


# Two Stack PDA Class
class Two_Stack_PDA:
    # other methods defined here
    """
        Parameter:
        machineDir: filename EXCLUDING TXT | Contains Machine Configurations

        Inputs & Attributes
        Q: Finite Set of States
        E: finite input alphabet
        L: finite stack alphabet
        S: transition functions
        Q1: initial state | must be an element of Q
        Z1: initial stack symbol for Stack 1 | must be an element of L
        QF: final / accepting state | must be an element of Q

        Attributes
        stack1: data structure representation of stack1
    """

    """
        Reserved Symbols:
            $ : lambda / empty symbol
            \ : start and end of list of transition functions

        Read File: extension .txt

        Sample: [Ignore including and anything beyond the symbol |, this is for better context explanation]
        Q0 Q1 Q2 | [Q] Each Space separated string is a state
        0 1 | [E] Each Space separated string is an input element of the alphabet 
        X | [L] Each space separated String is an input element of the alphabet
        \ | [S] Signifies the start of all transition functions, each new line represents a new transition
        A a $ $ A a $ Format: Initial State, Read, Pop(Stack 1), Pop (Stack 2), Next State, Push (Stack 1), Push(Stack 2).
        A b a a B $ $
        B b a a B $ $
        B $ Z Z C $ $
        C $ Z Z C $ $
        \ | [S] end of list of transition functions
        A | [Q1] Initial State
        Z | [Z1] Initial Stack Symbol for stack 1
        Z | [Z2] Initial Stack Symbol for stack 2
        C | [QF] Final / Accepting State 
    """

    def process_transition(self, current_state, symbol, processed_input, input_string, result_text):
        transition_found = False
        lambda_transition_occurred = False

        for transition in self.S:
                if transition.current == current_state and (transition.read == symbol):
                    if self.stack1.is_empty() and transition.pop != "$" and transition.pop != 'Z':
                      print("Input string rejected. Transition attempts to pop from empty stack 1.")
                      result_text.see(tk.END)
                      return current_state, False, lambda_transition_occurred
                    elif not self.stack1.is_empty() and transition.pop != "$":
                      if transition.pop != self.stack1.peek():
                         print(f"Input string rejected. Top of stack 1 ({self.stack1.peek()}) does not match the pop symbol ({transition.pop}).")
                         result_text.see(tk.END)
                         return current_state, False, lambda_transition_occurred

                    if self.stack2.is_empty() and transition.pop2 != "$" and transition.pop2 != 'Z':
                       print("Input string rejected. Transition attempts to pop from empty stack 2.")
                       result_text.see(tk.END)
                       return current_state, False, lambda_transition_occurred
                    elif not self.stack2.is_empty() and transition.pop2 != "$" and transition.pop2 != self.stack2.peek():
                       print(f"Input string rejected. Top of stack 2 ({self.stack2.peek()}) does not match the pop symbol ({transition.pop2}).")
                       result_text.see(tk.END)
                       return current_state, False, lambda_transition_occurred
                    
                    stack1_before_transition = list(self.stack1.items)
                    stack2_before_transition = list(self.stack2.items)

                    if (self.stack1.is_empty() and transition.pop == "$") or (not self.stack1.is_empty() and (transition.pop == self.stack1.peek() or transition.pop == "$")):
                      if (self.stack2.is_empty() and transition.pop2 == "$") or (not self.stack2.is_empty() and (transition.pop2 == self.stack2.peek() or transition.pop2 == "$")):
                            transition_found = True

                            if transition_found:
                                processed_input += symbol

                            unprocessed_input = input_string[len(processed_input):]

                            result_text.insert(tk.END, f"Current input symbol: {processed_input[:-1]}['{symbol if transition.read != '$' else ''}']{unprocessed_input}\n")
                            result_text.insert(tk.END, f"Current state: {current_state}\n")
                            result_text.insert(tk.END, f"Transition: {transition.current} - {transition.read} - {transition.pop} - {transition.pop2} - {transition.next} - {transition.push} - {transition.push2}\n")
                            result_text.insert(tk.END, f"Stack 1 before transition: {list(self.stack1.items)}\n")
                            result_text.insert(tk.END, f"Stack 2 before transition: {list(self.stack2.items)}\n")

                            if transition.pop != "$":
                                self.stack1.pop()
                            if transition.pop2 != "$":
                                self.stack2.pop()

                            if transition.push != "$":
                                self.stack1.push(transition.push)
                            if transition.push2 != "$":
                                self.stack2.push(transition.push2)

                            result_text.insert(tk.END, f"Stack 1 after transition: {list(self.stack1.items)}\n")
                            result_text.insert(tk.END, f"Stack 2 after transition: {list(self.stack2.items)}\n")

                            current_state = transition.next

                            print(f"stack1:{self.stack1.peek()}")
                            print(f"stack2:{self.stack2.peek()}")
                            print(transition.read)
                            print(self.stack1.size())
                            print(self.stack2.size())
                            print(transition.next)

                            if transition.read == "$" and (self.stack1.size() >= 0 or self.stack2.size() >= 0 or current_state != self.QF[0]):
                             lambda_transition_occurred = True
                            else:
                             lambda_transition_occurred = False
                             break

        return current_state, transition_found, lambda_transition_occurred
    

    def handle_lambda_transitions(self, current_state, result_text):
     processed_states = set()
     states_to_process = deque([current_state])

     while states_to_process:
        current_state = states_to_process.popleft()
        processed_states.add(current_state)

        if current_state in self.QF and self.stack1.is_empty() and self.stack2.is_empty():
            print("Execute")
            return current_state, True

        for transition in self.S:
            if transition.current == current_state and transition.read == "$":
                
                result_text.insert(tk.END, f"Current state before lambda transition: {current_state}\n")
                result_text.insert(tk.END, f"Stack 1 before lambda transition: {list(self.stack1.items)}\n")
                result_text.insert(tk.END, f"Stack 2 before lambda transition: {list(self.stack2.items)}\n")
                result_text.insert(tk.END, f"Lambda Transition: {transition.current} - {transition.read} - {transition.pop} - {transition.pop2} - {transition.next} - {transition.push} - {transition.push2}\n")

                if self.check_and_pop_stack(self.stack1, transition.pop) and \
                    self.check_and_pop_stack(self.stack2, transition.pop2):

                    self.check_and_push_stack(self.stack1, transition.push)
                    self.check_and_push_stack(self.stack2, transition.push2)

                    result_text.insert(tk.END, f"Stack 1 after lambda transition: {list(self.stack1.items)}\n")
                    result_text.insert(tk.END, f"Stack 2 after lambda transition: {list(self.stack2.items)}\n")

                    next_state = transition.next

                    if next_state not in processed_states and next_state not in states_to_process:
                        states_to_process.append(next_state)
                
                print(f"Current State: {current_state}")

     return current_state, True



    def check_and_pop_stack(self, stack, pop_symbol):
     if stack.is_empty() and pop_symbol != "$":
        return False
     elif not stack.is_empty() and pop_symbol != "$" and pop_symbol != stack.peek():
        return False
     elif pop_symbol != "$":
        stack.pop()
     return True

    def check_and_push_stack(self, stack, push_symbol):
     if push_symbol != "$":
        stack.push(push_symbol)

                
    def process_string(self, input_string):
     current_state = self.Q1[0]
     processed_input = ""
     unprocessed_input = input_string
     transition_not_counter = 0

     print(f"Starting processing of input string: {input_string}")
     result_text.insert(tk.END, f"Starting processing of input string: {input_string}\n")

     index = 0
     while index < len(input_string):
        symbol = input_string[index]
        print(f"Processing symbol: {symbol}")
        result_text.insert(tk.END, f"Processing symbol: {symbol}\n")

        stack1_before_value = self.stack1.size()
        stack2_before_value = self.stack2.size()
        current_state_before = current_state
        symbol_before = symbol

        current_state, transition_found, lambda_transition_occurred = self.process_transition(
            current_state, symbol, processed_input, input_string, result_text
        )

        if not transition_found:
            transition_not_counter += 1
            current_state, success = self.handle_lambda_transitions(current_state, result_text)
            if success:
                lambda_transition_occurred = True

            if not success:
                print("No valid transition found for input symbol: " + symbol)
                result_text.see(tk.END)
                return False      

            if not lambda_transition_occurred:
                index += 1
                transition_not_counter = 0
        else:
            processed_input += symbol
            unprocessed_input = input_string[len(processed_input):]
            index += 1
            transition_not_counter = 0

        if stack1_before_value == self.stack1.size() and stack2_before_value == self.stack2.size() and current_state_before == current_state and symbol_before == symbol and not transition_found and lambda_transition_occurred:
           break
        

     current_state, success = self.handle_lambda_transitions(current_state, result_text)
     if not success:
        print("Input string rejected due to lambda transitions.")
        result_text.see(tk.END)
        return False

     if len(unprocessed_input) == 0 and current_state in self.QF:
        print("Input string accepted.")
        result_text.see(tk.END)
        return True
     else:
        print("Input string rejected.")
        result_text.see(tk.END)
        return False


    def __init__(self, machineName):
        machineDir = "./machinerules/" + machineName + ".txt"
        self.Q = []
        self.E = []
        self.L = []
        self.S = []
        self.Q1 = []
        self.Z1 = []
        self.Z2 = []
        self.QF = []

        try:
            with open(machineDir, 'r') as file:
                # Step 2: Read the content
                # Read the entire content at once
                # content = file.read()

                # Read one line at a time
                # line = file.readline()

                # Read all lines into a list
                lines = file.readlines()

                # Step 3: Close the file (not required with "with" statement)
                # file.close()

            # Now you can work with the content
            # For example, if you used readlines():
            shift = 1
            for i in range(0, 8):
                if i == 0:
                    self.Q = lines[i].strip().split()
                elif i == 1:
                    self.E = lines[i].strip().split()
                elif i == 2:
                    self.L = lines[i].strip().split()
                elif i == 3:
                    self.S = []
                    counter = 4
                    while lines[counter].strip() != "\\":
                     print(f"Counter: {counter}")
                     print(f"Current line: {lines[counter]}")
                     rules = lines[counter].strip().split()
                     self.S.append(Transition(
                       rules[0], rules[1], rules[2], rules[3], rules[4], rules[5], rules[6]))
                     shift += 1
                     counter += 1
                elif i == 4:
                    self.Q1 = lines[i+shift].strip().split()
                elif i == 5:
                    line = lines[i+shift].strip()
                    if line:
                       self.Z1 = line.split()
                elif i == 6:
                    line = lines[i+shift].strip()
                    if line:
                       self.Z2 = line.split()
                elif i == 7:
                    self.QF = lines[i+shift].strip().split()

        except FileNotFoundError:
            print(f"File not found at path: {machineDir}")
        except IOError:
            print("An error occurred while reading the file.")

        self.stack1 = Stack()
        self.stack2 = Stack()

        if len(self.Z1) > 0:
          self.stack1.push(self.Z1[0])
        if len(self.Z2) > 0:
          self.stack2.push(self.Z2[0])


        self.initalState = None

        # Create Copy Arrays
        copyStates = self.Q.copy()
        copyTransitions = self.S.copy()

        # Find First Transition for head of linked list
        def findTransitionIndex(self, state):
            for i, transition in enumerate(copyTransitions):
                if transition.current == state:
                    return i
            return -1

        # Find
        self.head = State(self.Q1[0])
        currentState = self.head

        def recursiveMethod(self, currentState, remainingTransitions):
            if currentState.name == self.QF:
                return 0

            #  Find All Transitions
            for transition in remainingTransitions.copy():
                if transition.current == currentState.name:
                    # Check if Next State leads to the same state
                    if transition.next != currentState.name:
                        currentState.nextStates.append(
                            State(transition.next))
                        currentState.transitions.append(
                            transition)
                        remainingTransitions.pop(
                            remainingTransitions.index(transition))
                    else:
                        currentState.nextStates.append(
                            currentState)
                        currentState.transitions.append(
                            transition)

            for nextState in currentState.nextStates:
                if nextState != currentState:
                    recursiveMethod(self, nextState,
                                    remainingTransitions)

            # Find Next Transitions
            # currentTransition = 0
            # while currentTransition != -1:
            #     currentTransition = findTransitionIndex(
            #         self, currentState.name)
            #     if currentTransition == -1:
            #         break

                # duplicateState = False
                # # Append New States based on given Transitions from starting state
                # for state in remainingTransitions:
                #     if remainingTransitions.current == currentState.name
                #     if remainingTransitions[currentTransition].current == state.name:
                #         duplicateState = True

                #     if not duplicateState:
                #         currentState.nextStates.append(
                #             State(remainingTransitions[currentTransition].current))
                #         currentState.transitions.append(
                #             remainingTransitions[currentTransition])
                #         remainingTransitions.pop(currentTransition)

            self.recursiveMethod(nextState, remainingTransitions)

def process_input():
    machine_name = machine_name_entry.get()
    input_string = input_string_entry.get()
    
    if not machine_name or not input_string:
        messagebox.showerror("Error", "Both machine name and input string are required.")
        return
    
    rules = Two_Stack_PDA(machine_name)
    result = rules.process_string(input_string)

    if result:
        result_text.insert(tk.END, "Input string accepted.\n")
    else:
        result_text.insert(tk.END, "Input string rejected.\n")

def clear_log():
    result_text.delete(1.0, tk.END)

def show_info():
    messagebox.showinfo("File Information", 
                        """Please input the name of the file located in the 'machinerules' directory without the extension.

Default Machine Names:
onestacksim
twostacksim
bioninfomtest

If you want to create your own:

            $ : lambda / empty symbol
            \ : start and end of list of transition functions

        Read File: extension .txt

        Sample: [Ignore including and anything beyond the symbol |, this is for better context explanation]
        Q0 Q1 Q2 | [Q] Each Space separated string is a state
        0 1 | [E] Each Space separated string is an input element of the alphabet 
        X | [L] Each space separated String is an input element of the alphabet
        \ | [S] Signifies the start of all transition functions, each new line represents a new transition
        A a $ $ A a $ Format: Initial State, Read, Pop(Stack 1), Pop (Stack 2), Next State, Push (Stack 1), Push(Stack 2).
        A b a a B $ $
        B b a a B $ $
        B $ Z Z C $ $
        C $ Z Z C $ $
        \ | [S] end of list of transition functions
        A | [Q1] Initial State
        Z | [Z1] Initial Stack Symbol for stack 1
        Z | [Z2] Initial Stack Symbol for stack 2
        C | [QF] Final / Accepting State""")



root = tk.Tk()
root.title("Deterministic PDA Simulator(Two Stack)")

machine_name_frame = tk.Frame(root)
machine_name_label = tk.Label(machine_name_frame, text="Machine Name")  # Parent is the frame
info_button = tk.Button(machine_name_frame, text="?", command=show_info)  # Parent is the frame

machine_name_entry = tk.Entry(root)  # Parent is root

input_string_label = tk.Label(root, text="Input String")
input_string_entry = tk.Entry(root)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(root, yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

# Pack the label and button inside the frame
machine_name_label.pack(side=tk.LEFT)
info_button.pack(side=tk.LEFT)

machine_name_frame.pack()  # Pack the frame 

machine_name_entry.pack()

input_string_label.pack()
input_string_entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

process_button = tk.Button(button_frame, text="Process String", command=process_input)
clear_button = tk.Button(button_frame, text="Clear Log", command=clear_log)

clear_button.pack(side=tk.LEFT)
process_button.pack(side=tk.LEFT)

result_text.pack(side=tk.BOTTOM, fill=tk.BOTH)

root.mainloop()