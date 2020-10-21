from typing import List, Dict
from re import split

class Searcher(object):
    def _calculate_distances(self, words: List[str])->Dict:
        """
        Calculates distance between each pair of words
        :param words: list of unique words
        :return distances
        """
        calculated_distances={}
        for first_index in range(0, len(words)-1):
            for second_index in range(first_index+1, len(words)):
                distance=self._distance(words[first_index], words[second_index])
                self._max_distance=max(self._max_distance, distance)
                pair=(words[first_index], words[second_index])
                calculated_distances[pair]=distance
        return calculated_distances
    def _distance(self, first: str, second: str)->int:
        """
        Calculates distance between two words
        :param second_word: second word
        :param first_word: first word
        :return distance
        """
        return sum([1 for index in range(min(len(first),len(second))) 
        if first[index]!=second[index]])+abs(len(first)-len(second))
    def _get_pairs(self, distances: Dict)->List:
        """
        Returns pairs with maximum distance
        :param distances: pairs and their distances
        :return pairs with maxumim distance
        """
        return [pair for pair, distance in distances.items()
        if distance==self._max_distance]
    def _get_words(self, words: List)->List:
        """
        Returns list with unique words
        :return list of words
        """
        return list(set([word for pair in words
        for word in pair]))
    def __init__(self, path: str)->None:
        """
        Reads fields from file and stores only unique words
        :param path: path to file
        :return None
        """
        self._words=list(set([self._reduce(word) for line in open(path, "r") 
        for word in split(r"[^a-zA-Z]+", line)]))[1:]
        self._max_distance=0
    def _reduce(self, word: str)->str:
        """
        Reduces length of word
        :param word: word with some length
        :return reduced word
        """
        return word[:30] if len(word)>30 else word
    def result(self)->List:
        """
        Returns result
        :return result
        """
        calculated_distances=self._calculate_distances(self._words)
        largest_pairs=self._get_pairs(calculated_distances)
        return self._get_words(largest_pairs)

if __name__=="__main__":
    solution=Searcher("test.txt").result()
    print(solution)