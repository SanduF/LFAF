# Laboratory work nr.2
### Course: Formal Languages & Finite Automata
### Made by Furdui Alexandru  FAF-213
## Objectives:
1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

    b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.
    
    d. Represent the finite automaton graphically (Optional, and can be considered as a __*bonus point*__):
      
    - You can use external libraries, tools or APIs to generate the figures/diagrams.
        
    - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.
## Implementations:
2. For the first task we have to add some functionality to differ between grammar types, so i decided to implement a method for the **Grammar** class that outputs a boolean True if the grammar is in fact of type 3.
    There's some rules we must follow to carefully detect what we look for:

            a. The start symbol can only appear on the left side of a production rule.

            b. Each production rule can have only one non-terminal symbol on the left-hand side.

            c. The right-hand side of each production rule must consist of a single terminal symbol or a single non-terminal symbol followed by a terminal symbol.

            d. Production rules can be of two types:
                Non-terminal symbol → ε (where ε represents the empty string).
                Non-terminal symbol → terminal symbol or Non-terminal symbol.

    Here is my implementation:
    ```
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
    ```
## Results
 ```
    The grammar is of type 3.
 ```

3. Objectives

    a. We must convert FA to RG.
        Here we mostly play with existing FA transitions from the **Finite_automaton** class. For each transition we add a new rule to the grammar, this can be done easily by checking the length of the transition list (3 elements or 2) and adding a functionality for both cases in the conversion. Also mostly appending and concatenating was done here.
        Also the output is a dictionary, because my ***Grammar*** class accepts a dictionary as input. Therefore this is the desired output *for my code*.

    Here is my implementation:
    ```
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
    ```
  
    ## Results
    ```
    FA to regullar grammar conversion results:
{'S': ['aS', 'bS', 'cA'], 'A': ['aB'], 'B': ['aB', 'bB', 'c']}
    ```
  
    b. Determine whether your FA is deterministic or non-deterministic.
    To determine whether an FA is an NFA or DFA, you need to check the following:


        Determine if the FA has multiple transitions on the same input symbol from a state. If it does, then it is an NFA.

        Check if there is any state with an epsilon transition to another state. If there is, then it is an NFA.

        Verify if every state in the FA has exactly one transition on each input symbol in the alphabet. If this is the case, then it is a DFA.

        Check whether the FA accepts strings by final state or by empty stack. If it accepts by final state only, then it is a DFA.


    For my implementation I've decided it's easier and faster to check if automaton is of type NFA, by identifying whether I encounter any multiple transitions with same input symbol of a state (check if current symbol exists in my symbol list (called ```counts```)), once this happens the return of the method automatically becomes False.

    Here is my implementation:
   

    ## Results
   
  

    c. Implement some functionality that would convert an NDFA to a DFA.
    First of all my FA is definitely deterministic, so in my case I would implement this for a *potential* NFA. figured I culd also put my *fa_type* method for good use and have it dictate whether this method should be called or not. Now, for the method itself, we must follow some rules first:

        Start with the initial state of the NDFA as the initial state of the DFA.

        Create a new state in the DFA for each combination of states that the NDFA can be in after reading a particular input symbol.

        For each new state in the DFA, determine which states of the NDFA it represents. This can be done by tracing all possible paths through the NDFA from the initial state, following the transitions for the input symbol.

        For each new state in the DFA, determine its transitions by considering all possible transitions from the states it represents in the NDFA. If there are multiple transitions for a single input symbol, combine them into a single transition in the DFA.

        Mark any state in the DFA that includes an accepting state of the NDFA as an accepting state of the DFA.

        Repeat steps 2-5 for each input symbol until all states in the DFA have been created and transitions determined.

        The resulting DFA represents the same language as the original NDFA.

    Here is my *part* of implementation:
  

 
    d. Represent the finite automaton graphically 
    I've decided to use this tool I found on *http://magjac.com/graphviz-visual-editor/*.
    Here is the code provided.
    
    

    Here is the output:

  


---
## Conclusions
In summary, the exploration of finite automata, grammar types, NFA, and DFA yields valuable insights into both the theory and practical aspects of computational science. Through hands-on laboratory work, we have obtained a more profound comprehension of diverse grammar types and their connections with automata. Additionally, we have grasped the disparities between NFA and DFA and their applications in modeling different language types.

Moreover, this laboratory experience has highlighted the significance of computational models across various domains, including computer science, linguistics, and artificial intelligence. By employing finite automata and associated concepts, we can rigorously and systematically describe and analyze language structures. This underscores the vital role these tools play in understanding and advancing our knowledge in these fields.

