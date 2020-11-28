from config import (RESERVED_WORDS, HEX_DECIMALS, WORD, EMPTY,
HEX_LETTERS, OPERATORS, DELIMITERS, DECIMALS, STRING)
from typing import List
from enum import Enum
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

    class Class(Enum):
        "[Represents set of lexeme classes]"
        OPERATOR, DECIMAL, HEX_DECIMAL, IDENTIFIER=1, 2, 3, 9
        DELIMITER, COMMENT, WORD, RESERVED=5, 6, 7, 8
        FLOAT, ERROR, STRING, UNKNOWN=4, 10, 11, 12
        PREPROCESS_DIRECTIVE=13

        def __str__(self)->str:
            """
            Returns enum represented as string
            :return enum represented as string
            """
            return self.name

    class State(Enum):
        "[Represents states of automat]"
        INITIAL, OPERATOR, ERROR, DECIMAL=0, 1, 2, 3
        NUMBER_OR_WORD, WORD, DELIMITER=7, 8, 9
        HEX_DECIMAL, FLOAT, COMMENT=4, 5, 6
        WORD_BEGIN, WORD_END=10, 11
        PREPROCESS_DIRECTIVE=12

        def __str__(self)->str:
            """
            Returns enum represented as string
            :return enum represented as string
            """
            return self.name

    def _second_block(self, symbol: str)->None:
        """
        Second big block of if statements
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in DECIMALS:
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
        else:
            self._current.relate_to=self.Class.UNKNOWN
    def _first_block(self, symbol: str)->None:
        """
        First big block of if statements
        :param symbol: symbol to analyze
        :return None
        """
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
    def _third_block(self, symbol: str)->None:
        """
        Third big block of if statements
        :param symbol: symbol to analyze
        :return None
        """
        if symbol in OPERATORS:
            self._save_lexeme()
            self._current.relate_to=self.Class.OPERATOR
            self._state=self.State.OPERATOR
        elif symbol in DELIMITERS:
            self._save_lexeme()
            self._current.relate_to=self.Class.DELIMITER
            self._state=self.State.INITIAL
        else:
            self._current.relate_to=self.Class.UNKNOWN
            self._state=self.State.ERROR

    def _number_of_word_lexeme(self, symbol: str)->None:
        """
        Describes number of word lexeme
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in HEX_DECIMALS:
            if symbol in WORD:
                self._current.relate_to=self.Class.WORD
                self._state=self.State.WORD
            else:
                self._third_block(symbol)
    def _hex_decimal_lexeme(self, symbol: str)->None:
        """
        Describes hex decimal lexeme
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in HEX_DECIMALS:
            self._third_block(symbol)
    def _preprocess_lemexe(self, symbol: str)->None:
        """
        Describes preprocess lexeme
        :return None
        """
        if symbol=="\n":
            self._state=self.State.INITIAL
    def _word_end_lexeme(self, symbol: str)->None:
        """
        Describes word end lexeme
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
    def _operator_lexeme(self, symbol: str)->None:
        """
        Describes operator lexeme
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif (self._current.lexeme+symbol)=="//":
            self._current.relate_to=self.Class.COMMENT
            self._state=self.State.COMMENT
        elif symbol not in OPERATORS:
            self._save_lexeme()
            self._second_block(symbol)
    def _decimal_lexeme(self, symbol: str)->None:
        """
        Describes decimal lexeme
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
            self._third_block(symbol)
    def _comment_lexeme(self, symbol: str)->None:
        """
        Describes comment lexeme
        :return None
        """
        if symbol=="\n":
            self._state=self.State.INITIAL
    def _float_lexeme(self, symbol: str)->None:
        """
        Describes float lexeme
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
        elif symbol not in DECIMALS:
            self._third_block(symbol)
    def _error_lexeme(sefl, symbol: str)->None:
        """
        Describes error lexeme
        :return None
        """
        if symbol in EMPTY:
            self._state=self.State.INITIAL
    def _word_lexeme(self, symbol: str)->None:
        """
        Describes word lexeme
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
        cold_start=True
        for symbol in self._code:
            if self._state==self.State.INITIAL:
                if cold_start: cold_start=False
                else: self._save_lexeme()
                self._first_block(symbol)

            elif self._state==self.State.PREPROCESS_DIRECTIVE:
                self._preprocess_lemexe(symbol)
            elif self._state==self.State.DELIMITER: pass
            elif self._state==self.State.NUMBER_OR_WORD:
                self._number_of_word_lexeme(symbol)
            elif self._state==self.State.HEX_DECIMAL:
                self._hex_decimal_lexeme(symbol)
            elif self._state==self.State.WORD_BEGIN:
                if symbol in STRING:
                    self._state=self.State.WORD_END
            elif self._state==self.State.WORD_END:
                self._word_end_lexeme(symbol)
            elif self._state==self.State.OPERATOR:
                self._operator_lexeme(symbol)
            elif self._state==self.State.DECIMAL:
                self._decimal_lexeme(symbol)
            elif self._state==self.State.COMMENT:
                self._comment_lexeme(symbol)
            elif self._state==self.State.FLOAT:
                self._float_lexeme(symbol)
            elif self._state==self.State.ERROR:
                self._error_lexeme(symbol)
            elif self._state==self.State.WORD:
                self._word_lexeme(symbol)
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
        self._lexemes=[]

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Variant C++")
    parser.add_argument("path", metavar="path", type=str)
    
    Lexer(parser.parse_args().path).analyze().result()