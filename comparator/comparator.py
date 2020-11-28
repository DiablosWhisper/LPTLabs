from typing import TypeVar, Tuple
import argparse

FiniteAutomat=TypeVar("FiniteAutomat")

class FiniteAutomat(object):
    def compare(self, other: FiniteAutomat)->bool:
        """
        Compares two automata for equivalence
        :param automata: automata to compare
        :return equivalence of automatas
        """
        queue, visited=[(self._start, other._start)], []
        while queue:
            state1, state2=queue.pop()
            if self._is_end(state1)!=other._is_end(state2):
                return False
            visited.append((state1, state2))
            for symbol in self._symbols:
                pair=(other[(state2, symbol)], 
                self[(state1, symbol)])
                if pair not in visited:
                    queue.append(pair)
        return True
    def _is_end(self, state: str)->bool:
        """
        Defines whether the state is final
        :param state: state of automat
        :return whether the state is final
        """
        return state in self._terminal

    def __getitem__(self, rule: Tuple)->object:
        """
        Returns next state using the current rule
        :param rule: rule for transition
        :return state
        """
        return self._rules.get(rule)
    def __init__(self, path: str)->None:
        """
        Reads configuration file for finite automat
        :param path: path to file with configuration
        :return None
        """
        "[Read all lines from the current file]"
        self._configuration=[line.rstrip().split(" ")
        for line in open(path, "r").readlines()]

        "[Divide configuration into peaces]"
        self._symbols, self._states=set(), set()
        self._start=self._configuration[2][0]
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
    parser.add_argument("automat1", metavar="path", type=str)
    parser.add_argument("automat2", metavar="path", type=str)

    second=FiniteAutomat(parser.parse_args().automat2)
    first=FiniteAutomat(parser.parse_args().automat1)
    print(first.compare(second))