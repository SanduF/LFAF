# Topic: Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Made by Furdui Alexandru

----

## Theory

A grammar is in Chomsky Normal Form if all its production rules are of the form:
`A → BC or A → a` ,
meaning that there are either two non-terminal symbols or one terminal symbol.

To obtain grammar in CNF we have to follow these 5 steps:
1. Eliminate ε productions.
2. Eliminate unit productions.
3. Eliminate inaccessible symbols.
4. Eliminate the non productive symbols.
5. Obtain the Chomsky Normal Form.


## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.


## Implementation description
### Input grammar, v15
```

grammar = {
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['e', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C':['abC'],
    'D':['AB']
}

```

### Remove epsilon productions
* Elimination of epsilon productions. The epsilon elimination step involves removing any occurrence of epsilon from the logical formula by introducing new variables and clauses to represent the epsilon cases. This is done to ensure that the resulting CNF formula does not contain any empty clauses, which would make it unsatisfiable.
* The function  creates a new set ```nulls``` to store the variables that have an epsilon production. then proceeds to create a new dictionary ```new_prods``` that will contain the new productions with the epsilon productions removed. It iterates over each production and checks if it is an epsilon production. If it is, it skips it. If it is not, it checks if the production contains any variables that have epsilon productions. If it does, it creates a new production with those variables removed and adds it to the list of new productions for the current variable.

```
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


```

### Remove unit productions
* Remove unit productions. the function first creates a list of all the unit productions for the current variable. It then enters a while loop, where it removes the first unit production from the list and replaces it with all the productions of the variable it was producing. These new productions are added to the list of productions for the current variable.

* The function then checks again if there are any remaining unit productions for the current variable, and if there are, the process is repeated until all unit productions for the current variable have been removed. Finally, the function moves on to the next variable in the grammar and repeats the process of removing unit productions. The modified grammar is returned as the output of the function.

```
def remove_unit_prods(self):
        for symbol in self.grammar:
            unit_prods = [prod for prod in self.grammar[symbol] if len(prod) == 1 and prod.isupper()]
            while unit_prods:
                unit = unit_prods.pop(0)
                self.grammar[symbol].remove(unit)
                self.grammar[symbol].extend(
                    prod for prod in self.grammar[unit] if prod not in self.grammar[symbol])
                unit_prods = [prod for prod in self.grammar[symbol] if len(prod) == 1 and prod.isupper()]
```

### Remove inaccessible symbols
* The function then defines a nested helper function called ```pres``` that takes in a symbol and a set of visited symbols as arguments. The visit function recursively visits all symbols that can be reached from the given symbol using the productions in the grammar, adding each visited symbol to the set of visited symbols.

* The ```remove_inaccessible_symbols``` function initializes an empty set called ```accessible_symbols```, and then calls visit on the start symbol of the grammar with ```accessible_symbols``` as the set of visited symbols. This populates ```accessible_symbols``` with all symbols that can be derived from the start symbol.

* The function then updates the list of non-terminal symbols by removing any symbols that are not in the set of accessible symbols. It also updates the grammar dictionary by removing any productions that involve inaccessible symbols.



```
    def remove_inaccessible_symbols(self):
        def pres(symbol, visited):
            if symbol not in visited:
                visited.add(symbol)
                for prod in self.grammar[symbol]:
                    for s in prod:
                        if s in self.non_terminals:
                            visit(s, visited)

        accessible_symbols = set()
        pres(self.start_symbol, accessible_symbols)

        self.non_terminals = [nt for nt in self.non_terminals if nt in accessible_symbols]
        self.grammar = {k: v for k, v in self.grammar.items() if k in accessible_symbols}
```

### Remove nonproductive symbols
* The function initializes two sets: ```productive```, which initially contains only the start symbol, and ```old_productive```, which is initially empty. It then enters a loop that repeatedly updates productive by iterating over all symbols in the grammar and adding any symbols that can be used to derive a string consisting only of terminal symbols and symbols that are already known to be productive.

* The loop continues until ```old_productive``` and ```productive``` are the same set, indicating that no new productive symbols have been found. The function then calculates ```nonproductive``` by subtracting ```productive``` from the set of all non-terminal symbols in the grammar.

```

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
```

###  Final functionality to convert to CNF.
* The code iterates through the productions of the input grammar and creates new productions to convert the existing productions into CNF. If a production has a length greater than two, the function creates new nonterminal symbols for each pair of adjacent symbols in the production and replaces the original production with a series of new productions. If a production has a length of two and both symbols are nonterminals, the function does nothing. If a production has a length of one or has a terminal symbol, the function replaces the terminal symbol with a new nonterminal symbol.

```
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
```


## Conclusions / Screenshots / Results
### Final Output
```
S : T1  T1A  T2  T2A  T1S
T1 : b
T2 : a
A : T2S  BX3  AX5
X3 : aX4
X4 : b
X5 : BX6
X6 : aX7
X7 : b
B : T2  T1S
```

### Unit Testing
* Here are 2 of the 4 unit tests performed

```
    def test_eps(self):
        prods={
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['e', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C':['abC'],
    'D':['AB']
    }
        grammar=Grammar(prods)
        expected_output={'S': ['C', 'AC', 'b', 'bA', 'B', 'a', 'aA'], 'A': ['aS', 'Bab', 'ABab'], 'B': ['a', 'bS'], 'C': ['abC'], 'D': ['B', 'AB']}
        method_output=grammar.remove_epsilon_prods()
        print(method_output)
        self.assertEqual(method_output, expected_output)




    def test_unit(self):
        prods={
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['e', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C':['abC'],
    'D':['AB']
    }
        grammar=Grammar(prods)
        expected_output={'S': ['T1', 'T1A', 'T2', 'T2A', 'T1S'], 'T1': ['b'], 'T2': ['a'], 'A': ['T2S', 'BX3', 'AX5'], 'X3': ['aX4'], 'X4': ['b'], 'X5': ['BX6'], 'X6': ['aX7'], 'X7': ['b'], 'B': ['T2', 'T1S']}
        method_output=grammar.remove_unit_prods()
        self.assertEqual(method_output, expected_output)

 





if __name__=="__main__":
    unittest.main()
```

```
..
----------------------------------------------------------------------
Ran 4 tests in 0.08s

OK
```
