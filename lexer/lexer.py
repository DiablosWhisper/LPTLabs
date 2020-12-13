from config import (RESERVED_WORDS, HEX_DECIMALS, WORD, COMMENTS,
HEX_LETTERS, OPERATORS, DELIMITERS, DECIMALS, STRING, EMPTY)
from enum import Enum, auto
from typing import List
import argparse

class Lexer(object):
    class Lexeme(object):
        "[Represents read lexeme by automat]"
        def __init__(self, relate_to: object, lexeme: str="")->None:
            """
            Creates lexeme object
            :param relate_to: relation to some class
            :param lexeme: lexeme
            :return None
            """
            self.relate_to, self.lexeme=relate_to, lexeme.strip()
        def __str__(self)->str:
            """
            Returns lexeme and relation to class
            :return lexeme and relation to class
            """
            return f"{self.lexeme} - {str(self.relate_to)}"

        def clear(self)->None:
            """
            Clears class fields
            :return None
            """
            self.relate_to, self.lexeme="", ""

    class State(Enum):
        "[Represents states of automat]"
        (INITIAL, OPERATOR, ERROR, DECIMAL, HEX_DECIMAL, FLOAT,
        COMMENT_BEGIN, COMMENT_END, NUMBER_OR_WORD, WORD,
        DELIMITER, WORD_BEGIN, PREPROCESS_DIRECTIVE, 
        WORD_END, COMMENT)=[auto() for _ in range(15)]
        def __str__(self)->str:
            """
            Returns enum represented as string
            :return enum represented as string
            """
            return self.name

    class Class(Enum):
        "[Represents set of lexeme classes]"
        (OPERATOR, WORD, HEX_DECIMAL, FLOAT, DELIMITER, 
        COMMENT, DECIMAL, PREPROCESS_DIRECTIVE,
        IDENTIFIER, ERROR, UNKNOWN, RESERVED,
        STRING)=[auto() for _ in range(13)]
        def __str__(self)->str:
            """
            Returns enum represented as string
            :return enum represented as string
            """
            return self.name

    def _preprocess_directive(self, symbol: str)->None:
        """
        Automat behavior at preprocess directive state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol=="\n":
            self._state=self.State.INITIAL
    def _number_or_word(self, symbol: str)->None:
        """
        Automat behavior at number or word state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in HEX_DECIMALS:
            if symbol in WORD:
                self._current.relate_to=self.Class.WORD
                self._state=self.State.WORD
            else:
                if symbol in OPERATORS:
                    self._save_lexeme()
                    self._current.relate_to=self.Class.OPERATOR
                    self._state=self.State.OPERATOR
                elif symbol in DELIMITERS:
                    self._save_lexeme()
                    self._current.relate_to=self.Class.DELIMITER
                    self._state=self.State.INITIAL
                else:
                    self._current.relate_to=self.Class.ERROR
                    self._state=self.State.ERROR
    def _comment_begin(self, symbol: str)->None:
        """
        Automat behavior at comment begin state
        :param symbol: symbol to analyze
        :return None
        """
        if "*/" in self._current.lexeme:
            self._save_lexeme()
            self._state=self.State.INITIAL
    def _comment_end(self, symbol : str)->None:
        """
        Automat behavior at comment end state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol=="\n":
            self._state=self.State.INITIAL
        
    def _hexdecimal(self, symbol: str)->None:
        """
        Automat behavior at hexdecimal state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in HEX_DECIMALS:
            if symbol in OPERATORS:
                self._save_lexeme()
                self._current.relate_to=self.Class.OPERATOR
                self._state=self.State.OPERATOR
            elif symbol in DELIMITERS:
                self._save_lexeme()
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.INITIAL
            else:
                self._current.relate_to=self.Class.ERROR
                self._state=self.State.ERROR
    def _word_begin(self, symbol: str)->None:
        """
        Automat behavior at word begin state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in STRING:
            self._state=self.State.WORD_END
    def _word_end(self, symbol: str)->None:
        """
        Automat behavior at word end state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        else:
            if symbol in OPERATORS:
                self._save_lexeme()
                self._current.relate_to=self.Class.OPERATOR
                self._state=self.State.OPERATOR
            elif symbol in DELIMITERS:
                self._save_lexeme()
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.INITIAL
            elif symbol not in STRING:
                self._current.relate_to=self.Class.UNKNOWN
                self._state=self.State.ERROR
    def _operator(self, symbol: str)->None:
        """
        Automat behavior at operator state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif self._current.lexeme+symbol=="//":
            self._current.relate_to=self.Class.COMMENT
            self._state=self.State.COMMENT
        elif self._current.lexeme+symbol=="/*":
            self._current.relate_to=self.Class.COMMENT
            self._state=self.State.COMMENT_BEGIN
        elif symbol not in OPERATORS:
            self._save_lexeme()
            if symbol in DECIMALS:
                self._current.relate_to=self.Class.DECIMAL
                self._state=self.State.DECIMAL
            elif symbol in HEX_LETTERS:
                self._current.relate_to=self.Class.HEX_DECIMAL
                self._state=self.State.NUMBER_OR_WORD
            elif symbol in DELIMITERS:
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.DELIMITER
            elif symbol in WORD:
                self._current.relate_to=self.Class.WORD
                self._state=self.State.WORD
            elif symbol in STRING:
                self._current.relate_to=self.Class.STRING
                self._state=self.State.WORD_BEGIN
            else:
                self._current.relate_to=self.Class.UNKNOWN
    def _initial(self, symbol: str)->None:
        """
        Automat behavior at initial state
        :param symbol: symbol to analyze
        :return None
        """
        if self._cold_start: self._cold_start=False
        elif self._current.lexeme=="." and symbol in DECIMALS+"e":
            self._current.relate_to=self.Class.FLOAT
            self._state=self.State.FLOAT
        else: self._save_lexeme()
        if self._state!=self.State.FLOAT:
            if symbol=="#":
                self._current.relate_to=self.Class.PREPROCESS_DIRECTIVE
                self._state=self.State.PREPROCESS_DIRECTIVE
            elif symbol in OPERATORS:
                self._current.relate_to=self.Class.OPERATOR
                self._state=self.State.OPERATOR
            elif symbol in DECIMALS:
                self._current.relate_to=self.Class.DECIMAL
                self._state=self.State.DECIMAL
            elif symbol in HEX_LETTERS:
                self._current.relate_to=self.Class.HEX_DECIMAL
                self._state=self.State.NUMBER_OR_WORD
            elif symbol in DELIMITERS:
                self._current.relate_to=self.Class.DELIMITER
            elif symbol in WORD:
                self._current.relate_to=self.Class.WORD
                self._state=self.State.WORD
            elif symbol in STRING:
                self._current.relate_to=self.Class.STRING
                self._state=self.State.WORD_BEGIN
            elif symbol in EMPTY:
                self._state=self.State.INITIAL
            else:
                self._current.relate_to=self.Class.UNKNOWN
    def _decimal(self, symbol: str)->None:
        """
        Automat behavior at decimal state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol==".":
            self._current.relate_to=self.Class.FLOAT
            self._state=self.State.FLOAT
        elif symbol in HEX_LETTERS:
            self._current.relate_to=self.Class.HEX_DECIMAL
            self._state=self.State.HEX_DECIMAL
        elif symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in DECIMALS:
            if symbol in OPERATORS:
                self._save_lexeme()
                self._current.relate_to=self.Class.OPERATOR
                self._state=self.State.OPERATOR
            elif symbol in DELIMITERS:
                self._save_lexeme()
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.INITIAL
            else:
                self._current.relate_to=self.Class.ERROR
                self._state=self.State.ERROR
    def _float(self, symbol: str)->None:
        """
        Automat behavior at float state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            if self._current.lexeme[-1] not in DECIMALS and self._current.lexeme[0] not in DECIMALS:
                self._current.relate_to=self.Class.ERROR
            elif (self._current.lexeme[0]=="." and self._current.lexeme[1]=="e"):
                self._current.relate_to=self.Class.ERROR
            self._state=self.State.INITIAL
        elif symbol=="e" or self._current.lexeme[-1]+symbol=="e-":
            pass
        elif symbol not in DECIMALS:
            if symbol in OPERATORS:
                if (self._current.lexeme[-1] not in DECIMALS and
                self._current.lexeme[-1]!="."):
                    self._current.relate_to=self.Class.ERROR
                self._save_lexeme()
                self._current.relate_to=self.Class.OPERATOR
                self._state=self.State.OPERATOR
            elif symbol in DELIMITERS:
                if self._current.lexeme[-1] not in DECIMALS:
                    self._current.relate_to=self.Class.ERROR
                elif (self._current.lexeme[0]=="." and self._current.lexeme[1]=="e"):
                    self._current.relate_to=self.Class.ERROR
                self._save_lexeme()
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.INITIAL
            else:
                self._current.relate_to=self.Class.ERROR
                self._state=self.State.ERROR
    def _error(self, symbol: str)->None:
        """
        Automat behavior at error state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
    def _word(self, symbol: str)->None:
        """
        Automat behavior at word state
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in WORD:
            if symbol in DELIMITERS:
                self._save_lexeme()
                self._current.relate_to=self.Class.DELIMITER
                self._state=self.State.INITIAL
                self._current.lexeme=""
            else:
                if symbol in OPERATORS:
                    self._save_lexeme()
                    self._current.relate_to=self.Class.OPERATOR
                    self._state=self.State.OPERATOR
                    self._current.lexeme=""
                else:
                    self._current.relate_to=self.Class.UNKNOWN
                    self._state=self.State.ERROR
    def _delimiter(self, symbol: str)->None:
        """
        """
        if symbol=="\n":
            self._state=self.State.INITIAL
        elif symbol in DECIMALS:
            self._current.relate_to=self.Class.FLOAT
            self._state=self.State.FLOAT
    def _save_lexeme(self)->None:
        """
        Saves the current lexeme
        :return None
        """
        lexeme=self._current.lexeme.strip()
        relation=self._current.relate_to
        if relation==self.Class.WORD:
            relation=(self.Class.RESERVED 
            if lexeme in RESERVED_WORDS
            else self.Class.IDENTIFIER)
        self._lexemes.append(self.Lexeme(relation, lexeme))
        self._current.clear()
    def analyze(self)->None:
        """
        Returns lexeme class objects
        :return lexeme class objects
        """
        for symbol in self._code:
            if self._state==self.State.INITIAL:
                self._initial(symbol)
            elif self._state==self.State.PREPROCESS_DIRECTIVE:
                self._preprocess_directive(symbol)
            elif self._state==self.State.DELIMITER:
                self._delimiter(symbol)
            elif self._state==self.State.NUMBER_OR_WORD:
                self._number_or_word(symbol)
            elif self._state==self.State.HEX_DECIMAL:
                self._hexdecimal(symbol)
            elif self._state==self.State.WORD_BEGIN:
                self._word_begin(symbol)
            elif self._state==self.State.WORD_END:
                self._word_end(symbol)
            elif self._state==self.State.OPERATOR:
                self._operator(symbol)
            elif self._state==self.State.DECIMAL:
                self._decimal(symbol)
            elif self._state==self.State.COMMENT_BEGIN:
                self._comment_begin(symbol)
            elif self._state==self.State.COMMENT_END:
                self._comment_end(symbol)
            elif self._state==self.State.FLOAT:
                self._float(symbol)
            elif self._state==self.State.ERROR:
                self._error(symbol)
            elif self._state==self.State.WORD:
                self._word(symbol)
            elif self._state==self.State.COMMENT:
                if symbol=="\n":
                    self._state=self.State.INITIAL
            self._current.lexeme+=symbol
        self._save_lexeme()
        return self
    def result(self)->None:
        """
        Writes result into file
        :return None
        """
        with open("output.txt", "w") as file:
            for lexeme in self._lexemes:
                if (lexeme.lexeme!="" and
                lexeme.relate_to!=self.Class.COMMENT):
                    file.write(str(lexeme)+"\n")

    def __init__(self, path: str)->None:
        """
        Initializes lexer variables
        :param code: code to analyze
        :return None
        """
        self._code=open(path, "r").read()
        self._state=self.State.INITIAL
        self._current=self.Lexeme("")
        self._cold_start=True
        self._lexemes=[]

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Variant C++")
    parser.add_argument("path", metavar="path", type=str)
    
    Lexer(parser.parse_args().path).analyze().result()