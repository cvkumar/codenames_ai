# word_vectors = word2vec_vectors
import itertools
from typing import List, Tuple

import inflect


class CodenameBoard:
    def __init__(self, red: list, blue: list, neutral: list, black: str, word_vectors):
        self.reds = red
        self.blues = blue
        self.neutrals = neutral
        self.black = black
        self.word_vectors = word_vectors
        self.inflect_engine = inflect.engine()

    def guess_word(self, word: str):
        if word in self.reds:
            print(f"word was red: {word}")
            self.reds.remove(word)

        elif word in self.blues:
            print(f"word was blue: {word}")
            self.blues.remove(word)

        elif word in self.neutrals:
            print(f"word was neutral: {word}")
            self.neutrals.remove(word)

        elif word in self.black:
            print(f"GAME OVER word was black: {word}")

        else:
            print(f"Word: {word} not on board :/")

        if self.check_for_winner():
            print(f"Game over! {self.check_for_winner()} team won!")

    def check_for_winner(self):
        if not self.blues:
            return "blue"

        if not self.reds:
            return "red"

        else:
            return None

    def _process_similarity_results(self, positive_words: List[str], results: List[Tuple[str, float]]) -> Tuple[str, float]:
        # remove plural/singular matches
        not_fair_clues = set()
        for word in positive_words:
            not_fair_clues.add(self.inflect_engine.singular_noun(word))
            not_fair_clues.add(self.inflect_engine.plural(word))

        for result in results:
            clue = result[0]
            score = result[1]

            if clue in not_fair_clues:
                continue

            if any([clue in pos_word or pos_word in clue for pos_word in positive_words]):
                continue

            else:
                return clue, score

    def give_clue(self, team: str) -> Tuple[str, int]:
        clue_size = 2
        if team == "blue":
            cards = self.blues
        else:
            cards = self.reds

        if not cards:
            print(f"No cards remaining for team: {team}")

        if len(cards) == 1:
            results: List[Tuple[str, float]] = self.word_vectors.most_similar(cards[0])
            max_clue, max_score = self._process_similarity_results([cards[0]], results)
            print(f"{max_clue} for {1} with similarity score: {max_score}")
            return max_clue, clue_size

        pairs = itertools.permutations(cards, clue_size)
        max_score = float("-inf")
        max_clue = None
        for pair in pairs:
            results = self.word_vectors.most_similar(positive=pair)
            clue, score = self._process_similarity_results(pair, results)

            if score > max_score:
                max_score = score
                max_clue = clue

        print(f"{max_clue} for {clue_size} with similarity score: {max_score}")

        return max_clue, clue_size

    def print_board(self):
        return self.reds + self.blues + [self.black] + self.neutrals
