from token import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def lex(self):
        tokens = []
        while self.pos < len(self.text):
            if self.text[self.pos].isdigit():  #if current position is a digit, check if other digits follow it
                i=self.pos
                st=""
                while(self.text[i].isdigit()):
                    st+=self.text[i]
                    i+=1
                self.pos=i
                tokens.append(Token('INTEGER', int(st)))
            if self.text[self.pos].isalpha():  #if current position is a char, check if other chars follow it
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
            elif self.text[self.pos] == '+':
                tokens.append(Token('PLUS', '+'))
                self.advance()
            elif self.text[self.pos] == '-':
                tokens.append(Token('MINUS', '-'))
                self.advance()
            elif self.text[self.pos] == '=':
                tokens.append(Token('EQUAL', '='))
                self.advance()
            elif self.text[self.pos] == '*':
                tokens.append(Token('MULTIPLY', '*'))
                self.advance()
            elif self.text[self.pos] == '/':
                tokens.append(Token('DIVIDE', '/'))
                self.advance()
            elif self.text[self.pos] == ':':
                tokens.append(Token('COLON', ':'))
                self.advance()
            elif self.text[self.pos] == ',':
                tokens.append(Token('COMMA', ','))
                self.advance()
            elif self.text[self.pos] == '>':
                tokens.append(Token('GREATER', '>'))
                self.advance()
            elif self.text[self.pos] == '<':
                tokens.append(Token('LESS', '<'))
                self.advance()
            elif self.text[self.pos] == '(':
                tokens.append(Token('LPAREN', '('))
                self.advance()
            elif self.text[self.pos] == ')':
                tokens.append(Token('RPAREN', ')'))
                self.advance()
            elif self.text[self.pos] == '[':
                tokens.append(Token('LBRACKET', '['))
                self.advance()
            elif self.text[self.pos] == ']':
                tokens.append(Token('RBRACKET', ']'))
                self.advance()
            elif self.text[self.pos] == '#':
                i=self.pos
                st=""
                while(self.text[i]!='\n'):
                    st+=self.text[i]
                    i+=1
                self.pos=i
                tokens.append(Token('COMMENT', st))
                self.advance()
            else:
                #raise ValueError(f'Invalid character at position {self.pos}: {self.text[self.pos]}')
                pass
            self.skip_whitespace()
        return tokens