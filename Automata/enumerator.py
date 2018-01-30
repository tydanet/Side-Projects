class Turing:
    def __init__(self, transitions, debug=False):
        self.transitions = transitions

        self.startState = None
        self.acceptState = None
        self.rejectState = None

        self.state = None
        self.tape = None
        self.head = None

        self.debug = debug

    def move(self):
        state = self.state
        symbol = self.tape[self.head]

        triple = self.transitions.get((state, symbol))
        newState, newSymbol, move = triple

        if self.head == 0 and move < 0:
            self.tape = [' '] + self.tape
            self.head += 1

        elif self.head == len(self.tape)-1 and move > 0:
            self.tape = self.tape + [' ']

        self.state = newState
        self.tape[self.head] = newSymbol
        self.head += move

    def run(self, word):
        self.state = self.startState
        self.tape = list(word)
        self.head = 0

        while True:
            self.move()

            if self.state == self.acceptState:
                return True

            elif self.state == self.rejectState:
                return False

            if self.debug:
                print(self.state, self.head, self.tape)

class Enumerator:
    def __init__(self, alphabet, decider):
        self.alphabet = alphabet
        self.decider = decider
        self.rep = [0]

    def enumerate(self, stop=8):
        word = ' '
        accepted = self.decider.run(' ')

        i = 0
        while i < stop:
            if accepted:
                print(word)
                i += 1

            self.rep = self.increment(self.rep)
            word = self.wordify(self.rep)
            accepted = self.decider.run(word)

    def increment(self, rep):
        base = len(self.alphabet)

        i = -1
        rep[i] = (rep[i] + 1) % len(self.alphabet)

        carry = 0
        if rep[i] == 0:
            carry = 1

        while carry == 1:
            i -= 1

            if i < -len(rep):
                rep = [0] + rep
                return rep

            rep[i] = (rep[i] + 1) % len(self.alphabet)

            if rep[i] != 0:
                carry = 0

        return rep

    def wordify(self, rep):
        return ''.join([self.alphabet[x] for x in rep])


if __name__ == '__main__':
    table = { 
            ('0',' '):('A',' ',1),  ('0','a'):('1','x',1),  ('0','b'):('R',' ',1),   ('0','x'):('0','x',1),
            ('1',' '):('R',' ',1),  ('1','a'):('1','a',1),  ('1','b'):('2','x',1),  ('1','x'):('1','x',1),
            ('2',' '):('3',' ',-1), ('2','a'):('R',' ',1),   ('2','b'):('2','b',1),  ('2','x'):('2','x',1),
            ('3',' '):('0',' ',1),  ('3','a'):('3','a',-1), ('3','b'):('3','b',-1), ('3','x'):('3','x',-1),
            }

    turing = Turing(table)
    turing.startState = '0'
    turing.acceptState = 'A'
    turing.rejectState = 'R'

    #print(turing.run('aab'))
    #print(turing.run('aaabbb'))

    enum = Enumerator(['a','b'], turing)

    #for i in range(9):
    #    enum.rep = enum.increment(enum.rep)
    #    print(enum.wordify(enum.rep))

    enum.enumerate()

