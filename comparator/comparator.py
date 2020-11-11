from typing import TypeVar
import argparse

FiniteAutomata=TypeVar("FiniteAutomata")

class FiniteAutomata(object):
    def compare(self, other: FiniteAutomata)->bool:
        """
        Compares two automatas for equivalence
        :param automata: automata to compare
        :return equivalence of automatas
        """
        queue, visited=[(self._incipient, other._incipient)], []
        while queue:
            u, v=queue.pop()
            if self._is_end(u)!=other._is_end(v):
                return False
            visited.append((u, v))
            for c in self._symbols:
                other_rule=other._rules.get((v, c))
                self_rule=self._rules.get((u, c))
                if (self_rule, other_rule) not in visited:
                    queue.append((self_rule, other_rule))
        return True
    def _is_end(self, state: str)->bool:
        """
        Defines whether the state is final
        :param state: staet of automata
        :return whether the state is final
        """
        return state in self._terminal

    def __init__(self, path: str)->None:
        """
        Reads configuration file for finite automata
        :param path: path to file with configuration
        :return None
        """
        "[Read all lines from the current file]"
        self._configuration=[line.rstrip().split(" ")
        for line in open(path, "r").readlines()]

        "[Divide configuration into peaces]"
        self._incipient=self._configuration[2][0]
        self._symbols, self._states=set(), set()
        self._terminal=self._configuration[3]
        self._rules={tuple(rule[:2]): rule[2]
        for rule in self._configuration[4:]}

        "[Create states and alphabet]"
        for rule in self._configuration[4:]:
            self._symbols.add(rule[1])
            self._states.add(rule[0])
            self._states.add(rule[2])

        "[Delete unusable variables]"
        del self._configuration

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Variant 13")
    parser.add_argument("automata1", metavar="path", type=str)
    parser.add_argument("automata2", metavar="path", type=str)

    second=FiniteAutomata(parser.parse_args().automata2)
    first=FiniteAutomata(parser.parse_args().automata1)
    print(first.compare(second))