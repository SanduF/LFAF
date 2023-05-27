from lexer import Lexer
from Parser import Parser

'''Input for lab 3
text = def bubblesort(arr):
    n = len(arr)
    # Traverse through all array elements\n
    for i in range(n):
        # Last i elements are already sorted\n
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element\n
            #nota 10 pls ^_^\n
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

lexer = Lexer(text)
tokens = lexer.lex()
'''


'''for token in tokens:
    print(token)'''

# Lab 5 run program, insert user input.

def run(fn, text):
		# Generate tokens
		lexer = Lexer(fn, text)
		tokens, error = lexer.make_tokens()
		if error: return None, error
		
		# Generate AST
		parser = Parser(tokens)
		ast = parser.parse()

		return ast.node, ast.error



while True:
		text = input('shell > ')
		result, error = run('<stdin>', text)

		if error: print(error.as_string())
		else: print(result)