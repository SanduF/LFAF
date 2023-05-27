import unittest
from grammar import Grammar


class TestChomsky(unittest.TestCase):

        

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

 

    def test_inact(self):
        prods={
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['e', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C':['abC'],
    'D':['AB']
    }
        grammar=Grammar(prods)
        expected_output={'S': ['T1', 'T1A', 'T2', 'T2A', 'T1S'], 'A': ['T2S', 'BX3', 'AX5'], 'B': ['T2', 'T1S']}
        method_output=grammar.remove_inaccessible_symbols()
        print(method_output)
        self.assertEqual(method_output, expected_output)

    
    def test_nonprod(self):
        prods={
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['e', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C':['abC'],
    'D':['AB']
    }
        grammar=Grammar(prods)
        expected_output={'S': [], 'T1': ['b'], 'T2': ['a'], 'X4': ['b'], 'X7': ['b']}
        print(method_output)
        method_output=grammar.remove_nonproductive()

        self.assertEqual(method_output, expected_output)

    


if __name__=="__main__":
    unittest.main()