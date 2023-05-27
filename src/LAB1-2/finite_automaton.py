class Finite_automaton:
    def __init__(self,initial_state,final_states,alphabet,transitions,state):
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.state = state

    def checkWord(self,word):
        if word[0] not in self.initial_state:
            print("first is false")
            return False
        if word[-1] not in self.final_states:
            print("second is false")
            return  False

        for letter in word:
            if letter not in self.alphabet:
                print("third is false")
                return False
        return True
    
    def fa_type(self):    ##function to check FA type (NDFA or DFA)
        counts=[]
        print("##################################")
        for transition in self.transitions:
            cs=transition[0]+transition[1]
            if cs in counts:
                print("Automaton of type NDFA")
                return False
            else:
                counts.append(cs)
        print("Automaton of type DFA")
        return True


    def to_reg_grammar(self): ##based on existing transitions we recreate the gammar back from the FA
        grammar={}
        li=[]
        ct=self.transitions[0][0]
        for element in self.transitions:
            if element[0]!=ct:
                grammar[ct]=li
                li=[]
                ct=element[0]
            if len(element)==3:
                cs=element[1]+element[2]
            else:
                cs=element[1]
            li.append(cs)
        grammar[ct]=li
        print("##################################")
        print("FA to regullar grammar conversion results:")
        print(grammar)


    def nfa_to_dfa(self):
        if Finite_automaton.fa_type(self):
            # initialize DFA with initial state
            dfa_states = [frozenset([self.initial_state])]
            unprocessed_states = [frozenset([self.initial_state])]

            # map from sets of NFA states to DFA states
            nfa_to_dfa = {dfa_states[0]: 0}

            # initialize transitions and final states
            dfa_transitions = []
            dfa_final_states = []

            # process unprocessed DFA states
            while unprocessed_states:
                current_state = unprocessed_states.pop()
                transitions = {}

                # find NFA states reachable from current DFA state for each symbol
                for symbol in self.alphabet:
                    next_states = set()
                    for state in current_state:
                        if (state, symbol) in self.transitions:
                            next_states |= set(self.transitions[(state, symbol)])
                    if next_states:
                        next_state = frozenset(next_states)

                        # create new DFA state if necessary
                        if next_state not in nfa_to_dfa:
                            nfa_to_dfa[next_state] = len(dfa_states)
                            dfa_states.append(next_state)
                            unprocessed_states.append(next_state)

                        transitions[symbol] = nfa_to_dfa[next_state]

                dfa_transitions.append(transitions)

                # check if current DFA state contains final NFA states
                if any(state in self.final_states for state in current_state):
                    dfa_final_states.append(nfa_to_dfa[current_state])

            # create new DFA object with transitions and final states
            dfa = Finite_automaton(
                initial_state=0,
                final_states=dfa_final_states,
                alphabet=self.alphabet,
                transitions=dfa_transitions,
                state=dfa_states
            )

            return dfa
        else:
            print("Deterministic type FA does not require conversion.")
            


