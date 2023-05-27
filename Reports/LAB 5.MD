# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Made by Furdui Alexandru

----

## Theory
A parser, short for "parser generator," is a software tool that analyzes the structure of a sequence of symbols according to a formal grammar. It takes input in the form of a series of tokens and produces an output in the form of a parse tree or an abstract syntax tree (AST).

The primary purpose of a parser is to determine whether a given sequence of symbols conforms to the rules specified by a grammar. The grammar defines the syntax and structure of a programming language or any other formal language. The parser reads the input tokens and checks if they can be combined according to the grammar rules. If the input is syntactically correct, the parser produces a parse tree or an AST.

An abstract syntax tree (AST) is a hierarchical representation of the structure of source code or any other language construct defined by a grammar. It abstracts away the specific details of the source code and focuses on the essential components and their relationships. An AST is typically used as an intermediate representation during the compilation or interpretation process of programming languages.

In an AST, each node represents a language construct, such as a function, statement, expression, or operator. The nodes are connected to each other based on the relationships defined by the language grammar. The AST provides a higher-level representation of the code, making it easier to analyze and manipulate programmatically.

ASTs are widely used in programming language compilers, interpreters, and static analysis tools. They enable various tasks such as code optimization, type checking, semantic analysis, code generation, and more. By representing the code in a structured and abstracted form, ASTs facilitate the implementation of various language-related tools and techniques.


## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.


## Implementation description

&ensp;&ensp;&ensp; ```Position``` class. 

The advance method is used to update the position to the next character. It increments the idx and col variables by 1. If the current_char is a newline character (\n), it also increments the ln variable by 1 and resets the col to 0.

The copy method creates a new instance of the Position class with the same values for all the instance variables (idx, ln, col, fn, and ftxt). It essentially makes a copy of the current position object.

Overall, the Position class is designed to store and manipulate information about a position in a text file, such as the index, line number, column number, filename, and the content of the file (fn and ftxt). The advance method allows for moving the position to the next character, while the copy method provides a way to create a new position object with the same values.

```class Position:
		def __init__(self, idx, ln, col, fn, ftxt):
				self.idx = idx
				self.ln = ln
				self.col = col
				self.fn = fn
				self.ftxt = ftxt

		def advance(self, current_char=None):
				self.idx += 1
				self.col += 1

				if current_char == '\n':
						self.ln += 1
						self.col = 0

				return self

		def copy(self):
				return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
```


&ensp;&ensp;&ensp;```BinOpNode```, ```NumberNode```, ```UnaryOpNode``` classes. 

NumberNode class represents a node in the AST that corresponds to a numerical value. It has an __init__ method that takes a tok parameter representing the token of the number. The tok value is assigned to the tok instance variable. The class also defines a __repr__ method that returns a string representation of the node.

BinOpNode class represents a node in the AST that corresponds to a binary operation, such as addition, subtraction, multiplication, etc. It has an __init__ method that takes three parameters: left_node, op_tok, and right_node. The left_node parameter represents the left-hand side expression of the binary operation, op_tok represents the token of the binary operator, and right_node represents the right-hand side expression. The constructor assigns these parameters to the corresponding instance variables: left_node, op_tok, and right_node. The class also defines a __repr__ method that returns a string representation of the node.

UnaryOpNode class represents a node in the AST that corresponds to a unary operation, such as negation or mathematical functions. It has an __init__ method that takes two parameters: op_tok and node. The op_tok parameter represents the token of the unary operator, and node represents the expression on which the unary operation is applied. The constructor assigns these parameters to the corresponding instance variables: op_tok and node. The class also defines a __repr__ method that returns a string representation of the node.


&ensp;&ensp;&ensp; ```ParseResult``` class.The register method is used to handle the result of a parsing operation. It takes a res parameter representing the result to be registered. If res is an instance of ParseResult, it checks if it has an error. If it does, the error is assigned to the error instance variable of the current ParseResult object. The method then returns the node from the res object. If res is not an instance of ParseResult, it simply returns res.

The success method is used to indicate a successful parsing operation. It takes a node parameter representing the resulting node of the parse. It assigns the node to the node instance variable of the ParseResult object and returns the updated ParseResult object itself.

The failure method is used to indicate a failed parsing operation. It takes an error parameter representing the error message or information about the failure. It assigns the error to the error instance variable of the ParseResult object and returns the updated ParseResult object itself.


&ensp;&ensp;&ensp;```Parser``` class.

Advance: This method advances the token index and updates the current_tok variable to the next token in the list. It returns the updated current_tok. 

Parse: This method is the entry point for parsing. It calls the expr method to parse an expression and assigns the result to res. It then checks if there was no error during parsing and if the current token type is not the end of file (EOF). If there is an error or the current token is not EOF, it returns a failure result with an InvalidSyntaxError. Otherwise, it returns the res result. 

Factor: This method handles parsing of factors in the expression. It creates a new ParseResult object res and assigns the current token to tok. It then checks different cases based on the token type. If the token type is TT_PLUS or TT_MINUS, it registers the advance of the token, recursively calls factor, and returns a success result with a UnaryOpNode containing the token and the factor result. If the token type is TT_INT or TT_FLOAT, it registers the advance of the token and returns a success result with a NumberNode containing the token. If the token type is TT_LPAREN, it registers the advance of the token, calls expr to parse an expression recursively, and checks if the current token is TT_RPAREN. If it is, it registers the advance and returns a success result with the parsed expression. Otherwise, it returns a failure result with an InvalidSyntaxError. If none of the cases match, it returns a failure result with an InvalidSyntaxError for an unexpected token type.

Expr: This method handles parsing of expressions. It uses the bin_op method with self.term as the func argument and a tuple of token types (TT_PLUS, TT_MINUS) as the ops argument. It returns the result of the bin_op method.

```
class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self, ):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

	def parse(self):
		res = self.expr()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*' or '/'"
			))
		return res

	
	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register(self.advance())
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))
		
		elif tok.type in (TT_INT, TT_FLOAT):
			res.register(self.advance())
			return res.success(NumberNode(tok))

		elif tok.type == TT_LPAREN:
			res.register(self.advance())
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register(self.advance())
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			"Expected int or float"
		))

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

```

&ensp;&ensp;&ensp; ```Error```, ```IllegalCharError```, ```InvalidSyntaxError``` classes.

For the error class: as_string: This method returns a string representation of the error. It constructs the error message by concatenating the error_name and details with a newline character. It then includes the file name (fn), line number (ln), and the text representation of the error position range using the pos_start and pos_end objects. It calls the string_with_arrows function with the text (ftxt), pos_start, and pos_end to generate a string with arrows pointing to the error position range. Finally, it returns the constructed error message.

The IllegalCharError class is a subclass of Error and represents an error caused by encountering an illegal character during parsing.

The InvalidSyntaxError class is also a subclass of Error and represents an error caused by encountering invalid syntax during parsing.




&ensp;&ensp;&ensp; Main program
```
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
```



## Conclusions / Screenshots / Results
Basic working output of mathemathical expression:
```
shell > 3+(1*34-3)/(2.4+2+9879)-4
((INT:3, PLUS, (((INT:1, MUL, INT:34), MINUS, INT:3), DIV, ((FLOAT:2.4, PLUS, INT:2), PLUS, INT:9879))), MINUS, INT:4)
```

Syntax error example:
```
shell > 345-(8573/452)-(762+523324.9
Invalid Syntax: Expected ')'
File <stdin>, line 1

345-(8573/452)-(762+523324.9
                            ^
```

Illegal charachter example:

```
shell > 234$
Illegal Character: '$'
File <stdin>, line 1

234$
   ^
```

&ensp;&ensp;&ensp;As we can see, an AST represents the hierarchical structure of the code and captures its syntax and semantics. It provides an organized and abstract representation of the code that can be further processed, analyzed, or executed.


&ensp;&ensp;&ensp;Building a parser and an AST can be challenging depending on the complexity of the language and the level of sophistication required. It involves understanding language specifications, designing grammars, implementing parsing algorithms (such as recursive descent or parser generators), and constructing the AST data structure. The difficulty can vary depending on factors like language complexity, grammar ambiguity, error recovery strategies, and the desired level of error reporting.


&ensp;&ensp;&ensp;The process of building a parser and an AST typically requires knowledge of formal language theory, grammars, parsing techniques, and data structures. It can be complex and time-consuming, especially for more expressive or domain-specific languages. However, there are tools, libraries, and frameworks available that can simplify the process and provide abstractions to handle many of the underlying complexities.



&ensp;&ensp;&ensp;Overall, building a parser and an AST is crucial for language processing tasks and can range in difficulty depending on the specific requirements and the available resources and tools.
