# Laboratory work nr.3
## Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Made by Furdui Alexandru

----
## Theory

  &ensp;&ensp;&ensp; A lexer, also known as a scanner converts each syntactical element in the input into a token using regular expressions. Tokens are the smallest pieces of a programming language that can be processed further by the compiler or interpreter.
  
  &ensp;&ensp;&ensp; A lexer receives an input character and separates it into tokens according to rules given , providing a token display as output, it can be used by a parser to understand the structure of the program.
  
  &ensp;&ensp;&ensp; This process of processing the input stream character by character and organizing them into meaningful chunks or lexemes such as identifiers, keywords, operators, literals, and punctuation. Each lexeme is given a token type and a value that can be used to build a parse tree.
  
  &ensp;&ensp;&ensp; Overall, a lexer is a critical component of a compiler or interpreter that performs lexical analysis on source code and outputs a sequence of tokens. This procedure is required for parsing and interpreting a programming language and is an essential step in the compilation process.


## Objectives:
1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.


## Implementation description

&ensp;&ensp;&ensp;I use two classes, ```Token``` and ```Lexer```. Token uses a keyword dictionary to be used by the lexer in order to identify them in the code input. The lexer class has a 'lex' function to iterate through each input charachter, identify it's type and return it to the used.
```
        while self.pos < len(self.text):
            if self.text[self.pos].isdigit():  
                st=""
                while(self.text[i].isdigit()):
                    st+=self.text[i]
                    i+=1
                self.pos=i
                tokens.append(Token('INTEGER', int(st)))
```



&ensp;&ensp;&ensp;This is the outer loop that runs as long as the current position within the text (indicated by ```self.pos```) is less than the length of the text.

&ensp;&ensp;&ensp;This checks whether the character at the current position within the text is a digit. If the current character is a digit, this inner loop extracts a sequence of digits from the text by repeatedly appending each digit to a string ```st``` and incrementing the position i. The loop stops when a non-digit character is encountered, and ```st``` contains the complete sequence of digits. 

&ensp;&ensp;&ensp;After the inner loop terminates, the current position is updated to skip over the sequence of digits that was just processed. Then, a new Token object is created with a type of 'INTEGER' and a value equal to the integer conversion of the string. This Token object is then appended to a list of tokens.


```
            if self.text[self.pos].isalpha():  
                i=self.pos
                st=""
                while(self.text[i].isalpha()):
                    st+=self.text[i]
                    i+=1
                self.pos=i
                if(st in Token.keywords):
                    tokens.append(Token(f'{Token.keywords[st]}', st))
                else:
                    tokens.append(Token('IDENT', st))
```

&ensp;&ensp;&ensp;This checks whether the character at the current position within the text is an alphabetic character (i.e., a letter).If the current character is a letter, this inner loop extracts a sequence of letters from the text by repeatedly appending each letter to a string ```st``` and incrementing the position ```i```. 

&ensp;&ensp;&ensp;The loop stops when a non-letter character is encountered,us obtaining the complete sequence of letters. After the inner loop terminates, the current position is updated to skip over the sequence of letters that was just processed.It also determines whether the string represents a reserved keyword (e.g., if, else, while) or a user-defined identifier (e.g., variable names). 

&ensp;&ensp;&ensp;The if statement checks if the string is present as a key in a Token.keywords dictionary. If it is, the corresponding value is used to create a new Token object . 
```
            elif self.text[self.pos] == '+':
                tokens.append(Token('PLUS', '+'))
                self.advance()
            elif self.text[self.pos] == '-':
                tokens.append(Token('MINUS', '-'))
                self.advance()
            elif self.text[self.pos] == '=':
                tokens.append(Token('EQUAL', '='))
                self.advance()
```
&ensp;&ensp;&ensp;If the current character is a '+' symbol, a new Token object is created with a type of 'PLUS' and a value of '+' and added to a list of tokens.The current position within the text is then incremented by one, by calling the advance() method. This method moves the self.pos pointer to the next position in the input text.

&ensp;&ensp;&ensp;The same process is repeated for '-' and '=' symbols, with the corresponding token types 'MINUS' and 'EQUAL', respectively.

&ensp;&ensp;&ensp;So, overall, this code scans the input text for specific symbols ('+', '-', and '=') and produces a stream of tokens that represent those symbols. The tokenizer identifies these symbols by checking the character at the current position within the text, and then creates a new token with the appropriate token type and value. The advance() method is then called to move to the next position in the input text.

```
            elif self.text[self.pos] == '#':
                i=self.pos
                st=""
                while(self.text[i]!='\n'):
                    st+=self.text[i]
                    i+=1
                self.pos=i
                tokens.append(Token('COMMENT', st))
                self.advance()
```
It is also noted that we merge comment words.If the current character is a '#' symbol, this inner loop extracts a sequence of characters from the text until a newline character ('\n') is encountered. 

&ensp;&ensp;&ensp;The loop repeatedly appends each character to a string ```st``` and increments the position ```i```. The loop stops when a newline character is encountered (\n), and ```st``` contains the complete sequence of characters that make up the comment.


## Results

Input code used:
```
text = '''def bubblesort(arr):
    n = len(arr)
    # Traverse through all array elements\n
    for i in range(n):
        # Last i elements are already sorted\n
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element\n
            #nota 10 pls ^_^\n
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
'''
```

Result:
```
Token(FUNCTION, def)
Token(IDENT, bubblesort)
Token(LPAREN, ()
Token(IDENT, arr)
Token(RPAREN, ))
Token(COLON, :)
Token(IDENT, n)
Token(EQUAL, =)
Token(LEN, len)
Token(LPAREN, ()
Token(IDENT, arr)
Token(RPAREN, ))
Token(COMMENT, # Traverse through all array elements)
Token(FOR, for)
Token(IDENT, i)
Token(IN, in)
Token(RANGE, range)
Token(LPAREN, ()
Token(IDENT, n)
Token(RPAREN, ))
Token(COLON, :)
Token(COMMENT, # Last i elements are already sorted)
Token(FOR, for)
Token(IDENT, j)
Token(IN, in)
Token(RANGE, range)
Token(LPAREN, ()
Token(INTEGER, 0)
Token(COMMA, ,)
Token(IDENT, n)
Token(MINUS, -)
Token(IDENT, i)
Token(MINUS, -)
Token(INTEGER, 1)
Token(RPAREN, ))
Token(COLON, :)
Token(COMMENT, # Swap if the element found is greater than the next element)
Token(COMMENT, #nota 10 pls ^_^)
Token(IF, if)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(RBRACKET, ])
Token(GREATER, >)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(PLUS, +)
Token(INTEGER, 1)
Token(RBRACKET, ])
Token(COLON, :)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(RBRACKET, ])
Token(COMMA, ,)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(PLUS, +)
Token(INTEGER, 1)
Token(RBRACKET, ])
Token(EQUAL, =)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(PLUS, +)
Token(INTEGER, 1)
Token(RBRACKET, ])
Token(COMMA, ,)
Token(IDENT, arr)
Token(LBRACKET, [)
Token(IDENT, j)
Token(RBRACKET, ])
```
&ensp;&ensp;&ensp;The output of our lexer, also known as a tokenizer, is the stream of tokens that represent the individual lexemes, or basic units of syntax, in a given input text. Each token typically consists of a token type and a token value. The purpose of a lexer is to break down a piece of code or input text into smaller, more manageable units that can be processed by the next stage of the compiler or interpreter. By identifying the individual lexemes and assigning them to their respective token types, the lexer provides a structured and standardized way to analyze the input text, which can be used to perform various operations such as syntax analysis, semantic analysis, or code generation.

## Conclusions 

To summarize, mastering the art of programming a lexer is an indispensable skill for individuals aspiring to delve into the realms of programming languages, compilers, or interpreters. This laboratory project provided me with the opportunity to acquire essential knowledge and techniques in recognizing and tokenizing diverse token types, including keywords, identifiers, numbers, and operators. Additionally, I honed my practical expertise by implementing a lexer and subjecting it to rigorous testing using various inputs to guarantee both its precision and efficiency.

&ensp;&ensp;&ensp;Moreover, I realized that the lexer is a critical component in the overall process of interpreting or compiling code. It serves as the building block for other parts of the interpreter or compiler and must be efficient and dependable.

&ensp;&ensp;&ensp;Overall, this laboratory work has provided me with valuable knowledge and skills that will be useful in building more complex interpreters and compilers in the future.
