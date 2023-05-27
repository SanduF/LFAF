from finite_automaton import Finite_automaton
import random

class Grammar:
    def __init__(self, grammar):
        self.grammar = grammar
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = None
        self.parse_grammar()
    lowc=[]
    def parse_grammar(self):
        for lhs, rhs in self.grammar.items():
            self.non_terminals.add(lhs)
            for symbol in rhs:
                if symbol not in self.non_terminals:
                    self.terminals.add(symbol)

        self.start_symbol = list(self.grammar.keys())[0]
        self.terminals={'a', 'b'}

    def generate(self, start_symbol):
            rule = self.grammar.get(start_symbol)
            if rule is None:
                return start_symbol
            else:
                random_rule = random.choice(rule)
                return "".join(self.generate(r) for r in random_rule)

    def to_finite_automaton(self):
        initial_states =[]
        lowercase=[]
        for state in self.grammar['S']:
            initial_states.append(state[0])
            lowercase.append(state[0])
        print("Start state is ", initial_states)

        final_states = []
        for key in self.grammar:
            for state in self.grammar[key]:
                if state.islower():
                    final_states.append(state)
        print("Final states is ", final_states)

        self.lowc=lowercase
        transition_functions = []
        for key in self.grammar:
            for state in self.grammar[key]:
                inter = []
                inter.append(key)
                inter = inter + list(state)
                transition_functions.append(inter)

        print(f'Transitions are: {transition_functions}')

        automaton = Finite_automaton(initial_states,
                                   final_states,
                                   lowercase, ##alphabet
                                   transition_functions,
                                   self.non_terminals)

        #####################################
        #####################################
        ##test input word here
        input_word="cabc"
        if automaton.checkWord(input_word):
            print('Checking input word: ',input_word)
            print('Valid word')
        else:
            print('Checking input word: ',input_word)
            print('Invalid word')

        automaton.fa_type()
        automaton.to_reg_grammar()


    def check_grammar_type(self):  ##checks whether grammar is of type 3, returns true if yes 
        for lhs, rhs in self.grammar.items():
            if lhs not in self.non_terminals:
                return False
            for symbol in rhs:
                if len(symbol)>2:
                    return False
                if len(symbol)==2:
                    if symbol[0] not in self.lowc and symbol[1] not in self.non_terminals:
                        return False
                if len(symbol)==1:
                    if symbol[0] not in self.lowc:
                        return False
        return True
    
    def remove_epsilon_prods(self):
        nulls = set()
        for var, prods in self.grammar.items():
            if "e" in prods:
                nulls.add(var)

        new_prods = {}
        for var, prods in self.grammar.items():
            new_prods[var] = []
            for prod in prods:
                if prod == "e":
                    continue
                for nullable in nulls:
                    if nullable in prod:
                        new_prod = prod.replace(nullable, "")
                        if new_prod not in new_prods[var]:
                            new_prods[var].append(new_prod)
                if prod not in new_prods[var]:
                    new_prods[var].append(prod)

        for var, prods in new_prods.items():
            new_prods[var] = [p for p in prods if p != "e"]

        for var, prods in new_prods.items():
            for prod in prods:
                if len(prod) == 1 and prod in nulls:
                    continue
                for i in range(len(prod)):
                    if prod[i] in nulls:
                        new_prod = prod[:i] + prod[i + 1:]
                        if new_prod not in new_prods[var]:
                            new_prods[var].append(new_prod)

        self.grammar = {k: v for k, v in new_prods.items() if v}        
        return self.grammar

    def remove_unit_prods(self):
        for symbol in self.grammar:
            unit_prods = [prod for prod in self.grammar[symbol] if len(prod) == 1 and prod.isupper()]
            while unit_prods:
                unit = unit_prods.pop(0)
                self.grammar[symbol].remove(unit)
                self.grammar[symbol].extend(
                    prod for prod in self.grammar[unit] if prod not in self.grammar[symbol])
                unit_prods = [prod for prod in self.grammar[symbol] if len(prod) == 1 and prod.isupper()]
        #print(self.grammar)        
        return self.grammar
    

    def remove_inaccessible_symbols(self):
        def visit(symbol, visited):
            if symbol not in visited:
                visited.add(symbol)
                for prod in self.grammar[symbol]:
                    for s in prod:
                        if s in self.non_terminals:
                            visit(s, visited)

        accessible_symbols = set()
        visit(self.start_symbol, accessible_symbols)

        self.non_terminals = [nt for nt in self.non_terminals if nt in accessible_symbols]
        self.grammar = {k: v for k, v in self.grammar.items() if k in accessible_symbols}
        #print(self.grammar)        
        return self.grammar

    def remove_nonproductive(self):
        productive = {self.start_symbol}
        old_productive = set()

        while old_productive != productive:
            old_productive = productive.copy()
            for symbol, rhs in self.grammar.items():
                if symbol not in productive:
                    for prod in rhs:
                        if all(s in productive or s in self.terminals for s in prod):
                            productive.add(symbol)

        nonproductive = set(self.non_terminals) - productive

        for symbol in nonproductive:
            del self.grammar[symbol]

        for symbol, rhs in self.grammar.items():
            new_rhs = []
            for prod in rhs:
                if all(s in productive or s in self.terminals for s in prod):
                    new_rhs.append(prod)
            self.grammar[symbol] = new_rhs

        self.non_terminals = sorted(list(productive))
        #print(self.grammar)        
        return self.grammar


    def to_cnf(self):
        new_prods = {}
        next_new_var = 1
        terminal_var_map = {}

        for var, prods in self.grammar.items():
            new_prods[var] = []

            for prod in prods:
                if len(prod) >= 3:
                    prod_vars = [f"X{next_new_var + i}" for i in range(len(prod) - 1)]
                    next_new_var += len(prod) - 1
                    self.non_terminals.extend(prod_vars)

                    new_prods[var].append(prod[0] + prod_vars[0])
                    for i in range(len(prod) - 2):
                        new_var = prod_vars[i]
                        new_prods.setdefault(new_var, [])
                        new_prods[new_var].append(prod[i + 1] + prod_vars[i + 1])
                    new_prods.setdefault(prod_vars[-1], [])
                    new_prods[prod_vars[-1]].append(prod[-1])

                elif len(prod) == 2 and all(sym in self.non_terminals for sym in prod):
                    new_prods[var].append(prod)

                else:
                    new_prod = prod
                    for sym in prod:
                        if sym in self.terminals:
                            if sym not in terminal_var_map:
                                new_var = f"T{next_new_var}"
                                next_new_var += 1
                                self.non_terminals.append(new_var)
                                new_prods.setdefault(new_var, [])
                                new_prods[new_var].append(sym)
                                terminal_var_map[sym] = new_var
                            new_prod = new_prod.replace(sym, terminal_var_map[sym], 1)
                    new_prods[var].append(new_prod)

        self.grammar = new_prods
        self.non_terminals = sorted(list(set(self.non_terminals)))
        ##print(self.grammar)        
        return self.grammar

    def print_grammar(self):
        for var, prods in self.grammar.items():
            
            print(f"{var} :", "  ".join(prods))

    def cfg_to_cnf(self):
        self.remove_epsilon_prods()
        self.remove_unit_prods()
        self.remove_inaccessible_symbols()
        self.remove_nonproductive()
        self.to_cnf()
        self.print_grammar()
        return self
