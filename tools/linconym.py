"""
Module containing the core of Linconym.
"""

###############
### Imports ###
###############

from tools.path import (
    PATH_GAMEPLAY,
    PATH_RESOURCES_FOLDER
)
from tools.constants import (
    ENGLISH_WORDS_DICTS,
    GAMEPLAY_DICT
)
from tools.basic_tools import (
    dichotomy,
    save_json_file,
    load_json_file
)

#################
### Functions ###
#################


def is_in_english_words(word: str):
    """
    Indicates whether a word belongs to the english words dictionnary or not.

    Parameters
    ----------
    word : str
        Word to check.

    Returns
    -------
    bool
        True if the word is in the dictionnary, False otherwise.
    """

    return dichotomy(word, ENGLISH_WORDS_DICTS["375k"]) is not None


def count_different_letters(word1: str, word2: str):
    """
    Count the number of different letters between two words.

    Parameters
    ----------
    word1 : str
        First word.
    word2 : str
        Second word.

    Returns
    -------
    int
        Number of different letters.
    """

    # Initialise the number of different letters
    nb_different_letters = 0
    used_letters = [False] * len(word2)

    # Iterate over the letters of the first word
    for letter in word1:
        valid_letter_bool = False
        for i, check_letter in enumerate(word2):
            if check_letter == letter and used_letters[i] is False:
                used_letters[i] = True
                valid_letter_bool = True
                break
        if valid_letter_bool is False:
            nb_different_letters += 1

    return nb_different_letters


def count_common_letters(word1: str, word2: str):
    res = len(word1) - count_different_letters(word1, word2)
    # TEMP
    res += (len(word2) - len(word1)) // 2
    if res < 0:
        res = 0
    return res


def is_valid(new_word: str, current_word: str, skip_in_english_words: bool = False):
    """
    Determine whether a word is valid or not to be submitted.

    Parameters
    ----------
    new_word : str
        New word to check.
    current_word : str
        Current word.

    Returns
    -------
    bool
        True if the word is valid, False otherwise.
    """

    # Check if the new word derives from the current word
    if len(new_word) - len(current_word) == 0:
        # Shuffle and change one letter case
        if count_different_letters(new_word, current_word) <= 1:
            derive_bool = True
        else:
            derive_bool = False
    elif len(new_word) - len(current_word) == 1:
        # New letter addition case
        if count_different_letters(new_word, current_word) <= 1:
            derive_bool = True
        else:
            derive_bool = False
    elif len(new_word) - len(current_word) == -1:
        # Letter deletion case
        if count_different_letters(new_word, current_word) == 0:
            derive_bool = True
        else:
            derive_bool = False
    else:
        derive_bool = False

    # Check if the new word is in the english dictionnary
    if skip_in_english_words:
        english_words_bool = True
    else:
        english_words_bool = is_in_english_words(new_word)

    # Check if the new word verifies both conditions
    valid_bool = derive_bool and english_words_bool

    return valid_bool


def find_all_next_words(current_word: str, english_words):
    next_words = []
    for word in english_words:
        if is_valid(word, current_word, skip_in_english_words=True):
            next_words.append(word)

    return next_words


def convert_position_to_wordlist(position: tuple, position_to_word_id, words_found):
    wordlist = []
    for i in range(1, len(position) + 1):
        word = words_found[position_to_word_id[position[:i]]]
        wordlist.append(word)
    return wordlist


def insert_in_sorted_list(item, sorted_list):
    a = 0
    b = len(sorted_list) - 1
    c = (a + b) // 2
    if item > sorted_list[b]:
        return None
    while sorted_list[c] != item and b - a > 1:
        if sorted_list[c] > item:
            b = c
        else:
            a = c
        c = (a + b) // 2
    idx_to_insert = c
    if item > sorted_list[idx_to_insert]:
        new_list = sorted_list[:idx_to_insert + 1] + \
            [item] + sorted_list[idx_to_insert + 1:]
    else:
        new_list = sorted_list[:idx_to_insert] + \
            [item] + sorted_list[idx_to_insert:]

    return new_list


def find_solutions(start_word: str, end_word: str, english_words: list = ENGLISH_WORDS_DICTS["375k"]):

    start_position = (0,)
    position_to_word_id = {start_position: 0}
    words_found = [start_word]
    pile = {}

    for i in range(len(end_word) + 1):
        pile[i] = []

    pile[0].append(start_position)

    not_found = True

    while not_found:
        current_position = None
        for i in sorted(pile.keys()):
            if len(pile[i]) > 0:
                # print(i)
                current_position = pile[i].pop(0)
                break

        if current_position is None:
            return None

        current_word = words_found[position_to_word_id[current_position]]
        # print(current_word, i)
        # print(current_position)
        next_words = find_all_next_words(current_word, english_words)
        # print(len(next_words))
        new_word_id = 0

        for word in next_words:
            if word not in words_found or word == end_word:
                temp_nb_common_letters = count_common_letters(word, end_word)
                new_position = current_position + (new_word_id,)
                position_to_word_id[new_position] = len(words_found)
                words_found.append(word)
                new_word_id += 1
                if word == end_word:
                    not_found = False
                    final_position = new_position
                    print(convert_position_to_wordlist(
                        final_position, position_to_word_id, words_found))
                else:
                    pile_id = -temp_nb_common_letters + len(new_position)
                    # print(pile_id)
                    if pile_id in pile:
                        pile[pile_id].append(new_position)
                    else:
                        pile[pile_id] = [new_position]

    solution = []
    for i in range(1, len(final_position) + 1):
        word = words_found[position_to_word_id[final_position[:i]]]
        solution.append(word)

    return solution


def fill_daily_games_with_solutions():
    DAILY_DICT = load_json_file(PATH_RESOURCES_FOLDER + "daily_games.json")
    for date in DAILY_DICT:
        start_word = DAILY_DICT[date]["start_word"]
        end_word = DAILY_DICT[date]["end_word"]
        if "simplest_solution" not in date:
            for resolution in ENGLISH_WORDS_DICTS:
                solution = find_solutions(
                    start_word=start_word,
                    end_word=end_word,
                    english_words=ENGLISH_WORDS_DICTS[resolution])
                if solution is not None:
                    DAILY_DICT[date]["simplest_solution"] = solution
                    break
        if "best_solution" not in date:
            if resolution != "375k":
                solution = find_solutions(
                    start_word=start_word,
                    end_word=end_word,
                    english_words=ENGLISH_WORDS_DICTS["375k"])
            DAILY_DICT[date]["best_solution"] = solution
    save_json_file(PATH_RESOURCES_FOLDER + "daily_games.json", DAILY_DICT)


def fill_gameplay_dict_with_solutions():
    for act in GAMEPLAY_DICT:
        for level in GAMEPLAY_DICT[act]:
            if level == "name":
                continue
            start_word = GAMEPLAY_DICT[act][level]["start_word"]
            end_word = GAMEPLAY_DICT[act][level]["end_word"]
            for resolution in ENGLISH_WORDS_DICTS:
                if f"{resolution}_sol" not in GAMEPLAY_DICT[act][level]:
                    print(resolution)
                    solution = find_solutions(
                        start_word=start_word,
                        end_word=end_word,
                        english_words=ENGLISH_WORDS_DICTS[resolution])
                    if solution is not None:
                        GAMEPLAY_DICT[act][level][f"{resolution}_sol"] = len(
                            solution)
                    else:
                        GAMEPLAY_DICT[act][level][f"{resolution}_sol"] = None

    save_json_file(PATH_GAMEPLAY, GAMEPLAY_DICT)

#############
### Class ###
#############


class Game():
    """
    Class to manage all actions and variables during a game of Linconym.
    """

    def __init__(self, start_word: str, end_word: str) -> None:
        self.start_word = start_word
        self.end_word = end_word
        self.current_position = (0,)
        self.position_to_word_id = {self.current_position: 0}
        self.words_found = [start_word]
        self.current_word = start_word

    def get_nb_next_words(self, position: tuple):
        """
        Get the number of words deriving directly from the given position

        Parameters
        ----------
        position : tuple
            Position to use.

        Returns
        -------
        int
            Number of next words.
        """

        # Initialise the number of next words
        nb_next_words = 0

        # Iterate over all stored positions
        for key in self.position_to_word_id:
            if len(key) == len(position) + 1:
                if key[:len(position)] == position:
                    nb_next_words += 1

        return nb_next_words

    def change_position(self, new_position: tuple):
        """
        Change the position of the cursor from one word to another

        Parameters
        ----------
        new_position : tuple
            New position to set.
        """

        self.current_position = new_position
        self.current_word = self.words_found[self.position_to_word_id[self.current_position]]

    def submit_word(self, new_word: str):
        if is_valid(new_word):

            # Compute the new position
            new_word_id = self.get_nb_next_words(self.current_position)
            new_position = self.current_position + (new_word_id,)

            # Add the word to the list of words found
            self.position_to_word_id[new_position] = len(self.words_found)
            self.words_found.append(new_word)

            # Switch to the new position
            self.change_position(new_position)

            # Check if the final word is reached
            if self.current_word == self.end_word:
                print("End word reached")

        else:
            print("Word not valid")


if __name__ == "__main__":
    fill_gameplay_dict_with_solutions()
    fill_daily_games_with_solutions()
