#!/usr/bin/python3

class TuringMachine:

    def __init__(self, delta, q0, qa, qr, blank=' '):
        self.transition_function = delta
        self.start_state = q0
        self.accept_state = qa
        self.reject_state = qr
        self.blank = blank

    def step(self, state, symbol):
        return self.transition_function[(state, symbol)]

    def simulate(self, word):
        tape = list(word) + [self.blank]
        curr_state = self.start_state
        curr_pos = 0

        while curr_state != self.accept_state:
            self.display(tape, curr_pos)

            config = self.step(curr_state, tape[curr_pos])
            curr_state = config[0]
            tape[curr_pos] = config[1]
            curr_pos += config[2]

            if curr_pos < 0:
                curr_pos = 0

            while curr_pos >= len(tape):
                tape = tape + [self.blank]

            if curr_state == self.reject_state:
                return '{} => REJECT'.format(word)

        return '{} => ACCEPT'.format(word)

    def display(self, tape, curr_pos):
           print(''.join(tape))
           pos = [ ' ' for x in tape ]
           pos[curr_pos] = '^'
           print(''.join(pos))

class TMCreator:

    def __init__(self):
        self.start_state = None
        self.accept_state = None
        self.reject_state = None
        self.states = set()
        self.tape_alphabet = set('_')
        self.transition = {}
        self.turing_machine = None

    def set_alphabet(self, symbols):
        self.tape_alphabet = set(symbols + ['_'])

    def add_state(self, name):
        self.states.add(name)

        for symbol in self.tape_alphabet:
            self.transition[(name, symbol)] = None

    def add_transition(self, A, B, symbol, write, move):
        if move == 'R':
            self.transition[(A, symbol)] = (B, write, 1)

        else:
            self.transition[(A, symbol)] = (B, write, -1)

    def set_start(self, name):
        self.start_state = name

    def set_accept(self, name):
        self.accept_state = name

    def set_reject(self, name):
        self.reject_state = name

    def set_turing_machine(self):
        self.turing_machine = TuringMachine(self.transition,
                                            self.start_state,
                                            self.accept_state,
                                            self.reject_state,
                                            blank='_')

    def test(self, word):
        print(self.turing_machine.simulate(word))

    def display(self):
        print('Tape Alphabet: {}'.format(self.tape_alphabet))
        print('Start State: {}'.format(self.start_state))
        print('Accept State: {}'.format(self.accept_state))
        print('Reject State: {}'.format(self.reject_state))
        print('States: {}'.format(self.states))
        print('Transition Function:\n {}'.format(self.transition))

    def clear(self):
        self.tape_alphabet = set('_')
        self.states = set()
        self.start_state = None
        self.accept_state = None
        self.reject_state = None
        self.transition = {}
        self.turing_machine = None

    def parse(self, command):
        tokens = command.split(' ')

        if tokens[0] == 'gamma' and len(tokens) == 2:
            print('Setting tape alphabet.')
            self.set_alphabet(list(tokens[1]))

        elif tokens[0] == 'add' and len(tokens) == 2:
            print('Adding state:', tokens[1])
            self.add_state(tokens[1])

        elif (
                len(tokens) == 6 and
                set([tokens[0],tokens[3]]) <= self.states and
                set([tokens[1],tokens[4]]) <= self.tape_alphabet and
                (tokens[5] == 'R' or tokens[5] == 'L') and
                tokens[2] == '->'
             ): 
            print('Adding transition.')
            self.add_transition(tokens[0], tokens[3], tokens[1], tokens[4], tokens[5])

        elif tokens[0] == 'start' and len(tokens) == 2:
            print('Setting start state.')
            self.set_start(tokens[1])

        elif tokens[0] == 'accept' and len(tokens) == 2:
            print('Setting accept state.')
            self.set_accept(tokens[1])

        elif tokens[0] == 'reject' and len(tokens) == 2:
            print('Setting reject state.')
            self.set_reject(tokens[1])

        elif tokens[0] == 'create':
            print('Creating Turing machine.')
            self.set_turing_machine()

        elif tokens[0] == 'test' and len(tokens) == 2:
            print('Testing Turing machine on input.')
            self.test(tokens[1])

        elif tokens[0] == 'display':
            self.display()

        elif tokens[0] == 'clear':
            self.clear()

        else:
            print('Unrecognized command')

    def repl(self):
        while True:
            command = input('>>> ')

            if command != 'q':
                self.parse(command)

            else:
                break

tmc = TMCreator()
tmc.repl()
