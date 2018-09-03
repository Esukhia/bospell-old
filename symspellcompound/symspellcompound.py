# -*- coding: utf-8 -*-

"""Main module."""
import os
from copy import copy
import math
import time

from symspellcompound.errors import DistanceException
from .tools import text_to_word_sequence, to_int, sort_suggestion
from .typo_distance import typo_distance
from .items import SuggestItem, DictionaryItem

import platform
if platform.system() != "Windows":
    from pyxdameraulevenshtein import damerau_levenshtein_distance
else:
    from jellyfish import levenshtein_distance
    

def time_printer(func):
    def func_wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, *kwargs)
        print("--- {} executed in  {:.4f} s ---".format(func.__name__, time.time() - start_time))
        return res

    return func_wrapper


if platform.system() != "Windows":
    DISTANCE_MAPPER = {
        "dameraulevenshtein": damerau_levenshtein_distance,
        "typo": typo_distance
    }
else:
    DISTANCE_MAPPER = {
        "dameraulevenshtein": levenshtein_distance,
        "typo": typo_distance
    }


class SySpellCompound(object):
    def __init__(self, distance="dameraulevenshtein", initialCapacity=16, maxDictionaryEditDistance=2, prefixLength=7, countThreshold=1, compactLevel=5):
        if not(distance in DISTANCE_MAPPER or callable(distance)):
            raise DistanceException("Distance must be dameraulevenshtein, typo or a function taking two arguments "
                                    "the two words which needs to be compared")
        self.initialCapacity = initialCapacity
        self.maxDictionaryEditDistance = maxDictionaryEditDistance
        self.prefixLength = prefixLength
        self.countThreshold = countThreshold
        self.compactLevel = min(compactLevel, 16)
        self.enable_compound_check = True
        # false: assumes input string as single term, no compound splitting / decompounding
        # true:  supports compound splitting / decompounding with three cases:
        # 1. mistakenly inserted space into a correct word led to two incorrect terms
        # 2. mistakenly omitted space between two correct words led to one incorrect combined term
        # 3. multiple independent input terms with/without spelling errors
        self.edit_distance_max = 2
        self.verbose = 0  # //ALLWAYS use verbose = 0 if enableCompoundCheck = true!
        # 0: top suggestion
        # 1: all suggestions of smallest edit distance
        # 2: all suggestions <= editDistanceMax (slower, no early termination)

        #  //Dictionary that contains both the original words and the deletes derived from them. A term might be both word and delete from another word at the same time.
        # //For space reduction a item might be either of type dictionaryItem or Int.
        # //A dictionaryItem is used for word, word/delete, and delete with multiple suggestions. Int is used for deletes with a single suggestion (the majority of entries).
        # //A Dictionary with fixed value type (int) requires less memory than a Dictionary with variable value type (object)
        # //To support two types with a Dictionary with fixed type (int), positive number point to one list of type 1 (string), and negative numbers point to a secondary list of type 2 (dictionaryEntry)
        self.dictionary = {}  # Initialize
        self.deletes = {}
        self.words = {}
        self.belowThresholdWords = {}
        self.max_length = 0
        # self.bigram = {} TODO: Remove it

    @staticmethod
    def parse_words(text):
        return text_to_word_sequence(text=text,
                                     filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                     lower=True,
                                     split=' ')

        # @time_printer

    def create_dictionary_entry(self, key, count):
        if (count <= 0):
            if self.countThreshold > 0:
                return False
            count = 0
        count_previous = -1
        if self.countThreshold > 1 and key in self.belowThresholdWords:
            count = (sys.maxsize - count_previous > count) and count_previous+count or sys.maxsize
            if count >= countThreshold:
                self.belowThresholdWords.pop(key)
            else:
                self.belowThresholdWords[key] = count
                return False
        elif key in self.words:
            count = (sys.maxsize - count_previous > count) and count_previous+count or sys.maxsize
            self.words[key] = count
            return False
        elif count < self.countThreshold:
            belowThresholdWords[key] = count
            return False
        self.words[key] = count
        if len(key) > self.max_length:
            self.max_length = len(key)
        edits = self.edits_prefix(key)
        for delete in edits:
            deleteHash = self.get_string_hash(delete)
            if deleteHash in self.deletes:
                self.deletes[deleteHash].append(key)
            else:
                self.deletes[deleteHash] = [key]
        # print("deletes:")
        # print(self.deletes)
        # print("words:")
        # print(self.words)
        return True

    def get_string_hash(self, s):
        return hash(s)

    def load_dictionary(self, corpus, term_index, count_index):
        # path = os.path.join(__file__, corpus)
        path = corpus
        if not os.path.isfile(path=path): return False
        for line in SySpellCompound.load_file(path=path):
            tokens = text_to_word_sequence(line)
            if len(tokens) >= 2:
                key = tokens[term_index]
                count = to_int(tokens[count_index])
                if count:
                    self.create_dictionary_entry(key=key, count=count)
        self.belowThresholdWords = {}
        return True

    def delete_in_suggestion_prefix(self, delete, delete_len, suggestion, suggestion_len):
        if delete_len == 0:
            return True
        if self.prefixLength < suggestion_len:
            suggestion_len = self.prefixLength
        j = 0
        for c in delete:
            while j < suggestion_len and c != suggestion[j]:
                j += 1
            if j == suggestion_len:
                return False
        return True

    def create_dictionary(self, corpus):
        # path = os.path.join(__file__, corpus)
        path = corpus
        if not os.path.isfile(path=path): return False
        for line in SySpellCompound.load_file(path=path):
            for token in line.split():
                self.create_dictionary_entry(key=token, count=1)
        self.belowThresholdWords = {}
        return True

    @staticmethod
    def load_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line

    def add_lowest_distance(self, item, suggestion, suggestion_int, delete):
        if self.verbose < 2 and len(item.suggestions) > 0 and (
                len(self.word_list[item.suggestions[0]]) - len(delete)) > (len(suggestion) - len(delete)):
            item.suggestions.clear()

        if self.verbose == 2 or len(item.suggestions) == 0 or (
                    len(self.word_list[item.suggestions[0]]) - len(delete) >= len(suggestion) - len(delete)):
            item.suggestions.append(suggestion_int)
        return item

    def edits_prefix(self, key):
        hashSet = []
        keylen = len(key)
        if keylen <= self.maxDictionaryEditDistance:
            hashSet.append("")
        if keylen > self.prefixLength:
            key = key[:self.prefixLength]
        hashSet.append(key)
        return self.edits(key, 0, hashSet)

    def edits(self, word, edit_distance, deletes):
        edit_distance += 1
        wordlen = len(word)
        if wordlen > 1:
            for index in range(0, wordlen):
                delete = word[:index] + word[index + 1:]
                if delete not in deletes:
                    deletes.append(delete)
                    if edit_distance < self.maxDictionaryEditDistance:
                        self.edits(delete, edit_distance, deletes)
        return deletes

    def lookup(self, input_string, verbosity, edit_distance_max):
        if edit_distance_max > self.maxDictionaryEditDistance:
            return []
        input_len = len(input_string)
        if (input_len - edit_distance_max) > self.max_length:
            return []

        suggestions = [] # list of SuggestItems
        hashset1 = set()
        hashset2 = set()

        if input_string in self.words:
            suggestions.append(SuggestItem(input_string, 0, self.words[input_string]))

        hashset2.add(input_string)

        edit_distance_max2 = edit_distance_max
        candidates_index = 0
        singleSuggestion = [""]
        candidates = [] # list of strings

        input_prefix_len = input_len
        if input_prefix_len > self.prefixLength:
            input_prefix_len = self.prefixLength
            candidates.append(input_string[:input_prefix_len])
        else:
            candidates.append(input_string)
        while candidates_index < len(candidates):
            candidate = candidates[candidates_index]
            candidates_index+=1
            candidate_len = len(candidate)
            lengthDiff = input_prefix_len - candidate_len

            if lengthDiff > edit_distance_max2:
                if verbosity == 2:
                    continue
                break
            candidateHash = self.get_string_hash(candidate)
            if candidateHash in self.deletes:
                dict_suggestions = self.deletes[candidateHash]
                for suggestion in dict_suggestions:
                    if suggestion == input_string:
                        continue
                    suggestion_len = len(suggestion)
                    if (abs(suggestion_len - input_len) > edit_distance_max2 or
                        suggestion_len < candidate_len or
                        (suggestion_len == candidate_len and suggestion != candidate)):
                        continue
                    sugg_prefix_len = min(suggestion_len, self.prefixLength)
                    if sugg_prefix_len > input_prefix_len and (sugg_prefix_len - candidate_len) > edit_distance_max2:
                        continue
                    distance = 0
                    if candidate_len == 0:
                        distance = min(input_len, suggestion_len)
                        if distance > edit_distance_max2:
                            continue
                        if suggestion in hashset2:
                            continue
                        hashset2.add(suggestion)
                    elif suggestion_len == 1:
                        if input_string.find(suggestion[0] < 0):
                            distance = input_len
                        else:
                            distance = input_len -1
                        if distance > edit_distance_max2:
                            continue
                        if suggestion in hashset2:
                            continue
                        hashset2.add(suggestion)
                    else:
                        len_min = min(input_len, suggestion_len) - self.prefixLength
                        if ((self.prefixLength - edit_distance_max == candidate_len and
                            len_min > 1 and input_string[input_len+1-len_min:] != suggestion[suggestion_len+1-len_min:]) or
                            (len_min > 0 and input_string[input_len-len_min] != suggestion[suggestion_len-len_min] and
                            (input_string[input_len-len_min-1] != suggestion[suggestion_len-len_min] or input_string[input_len-len_min] != suggestion[suggestion_len-len_min-1]))):
                            continue
                        else:
                            if verbosity < 2 and not self.delete_in_suggestion_prefix(candidate, candidate_len, suggestion, suggestion_len) or suggestion in hashset2:
                                continue
                            if suggestion not in hashset2:
                                hashset2.add(suggestion)
                            distance = distance_between_words(input_string, suggestion)
                            if distance < 0:
                                continue
                    if distance <= edit_distance_max2:
                        suggestion_count = self.words[suggestion]
                        si = SuggestItem(suggestion, distance, suggestion_count)
                        if len(suggestions) > 0:
                            if verbosity == 1:
                                if distance < edit_distance_max2:
                                    suggestions = []
                                break
                            elif verbosity == 0:
                                if distance < edit_distance_max2 or suggestion_count > suggestions[0].getCount():
                                    edit_distance_max2 = distance
                                    suggestions[0] = si
                                continue
                        if verbosity < 2:
                            edit_distance_max2 = distance
                        suggestions.append(si)

            if lengthDiff < edit_distance_max and candidate_len <= self.prefixLength:
                if verbosity < 2 and lengthDiff > edit_distance_max2:
                    continue
                for index in range(0, candidate_len):
                    delete = candidate[:index] + candidate[index + 1:]
                    if delete not in hashset1:
                        candidates.append(delete)
                    else:
                        hashset1.add(delete)
        if len(suggestions) > 1:
            suggestions = sort_suggestion(suggestions)
        return suggestions

    # @time_printer
    def lookup_compound(self, input_string, edit_distance_max):
        term_list_1 = input_string.split()
        suggestions = []
        suggestion_parts = []

        last_combi = False

        for i in range(0, len(term_list_1)):
            suggestions_previous_term = []
            for k in range(0, len(suggestions)):
                suggestions_previous_term.append(copy(suggestions[k]))
            suggestions = self.lookup(term_list_1[i], 0, edit_distance_max)
            if i > 0 and not last_combi:
                suggestions_combi = self.lookup(term_list_1[i-1] + term_list_1[i], 0, edit_distance_max)
                if len(suggestions_combi) > 0:
                    best1 = suggestion_parts[-1]
                    best2 = None
                    if len(suggestions) > 0:
                        best2 = suggestions[0]
                    else:
                        best2 = SuggestItem(term_list_1[i], edit_distance_max+1, 0)
                    distance1 = distance_between_words(term_list_1[i-1]+" "+term_list_1[i], best1.term+" "+best2.term)
                    if distance1 > 0 and suggestions_combi[0].distance + 1 < distance1:
                        suggestions_combi[0].distance += 1
                        suggestion_parts[-1] = suggestions_combi[0]
                        last_combi = True
                        break
            last_combi = False

            if len(suggestions) > 0 and (suggestions[0].distance == 0 or len(term_list_1[i]) == 1):
                suggestion_parts.append(suggestions[0])
            else:
                suggestions_split = []
                if len(suggestions) > 0:  # 473
                    suggestions_split.append(suggestions[0])
                if len(term_list_1[i]) > 1:
                    for j in range(1, len(term_list_1[i])):
                        part1 = term_list_1[i][0:j]
                        part2 = term_list_1[i][j:]
                        suggestion_split = SuggestItem()
                        suggestions1 = self.lookup(part1, 0, edit_distance_max)
                        if len(suggestions1) > 0:
                            if len(suggestions) > 0 and suggestions[0].term == suggestions1[0].term:
                                break
                            suggestions2 = self.lookup(part2, 0, edit_distance_max)
                            if len(suggestions2) > 0:
                                # if split correction1 == einzelwort correction
                                if len(suggestions) > 0 and suggestions[0].term == suggestions2[0].term:
                                    break
                                suggestion_split.term = suggestions1[0].term + " " + suggestions2[0].term
                                distance2 = distance_between_words(term_list_1[i], suggestions1[0].term+" "+suggestions2[0].term)
                                if distance2 < 0:
                                    distance2 = edit_distance_max+1
                                suggestion_split.distance = distance2
                                suggestion_split.count = min(suggestions1[0].count, suggestions2[0].count)
                                suggestions_split.append(suggestion_split)
                                if suggestion_split.distance == 1:
                                    break
                    if len(suggestions_split) > 0:
                        # sorted(suggestions_split, key=lambda x: 2 * x.distance - x.count, reverse=True)
                        suggestions_split = sort_suggestion(suggestions_split,
                                                            fonction=lambda x: 2 * x.distance - x.count)
                        suggestion_parts.append(suggestions_split[0])
                    else:
                        si = SuggestItem(term_list_1[i], edit_distance_max+1, 0)
                        suggestion_parts.append(si)
                else:
                    si = SuggestItem(term_list_1[i], edit_distance_max+1, 0)
                    suggestion_parts.append(si)
        suggestion = SuggestItem()
        suggestion.count = math.inf
        s = ""
        for si in suggestion_parts:
            s += si.term + " "
            suggestion.count = min(si.count, suggestion.count)
        suggestion.term = s.strip()
        suggestion.distance = distance_between_words(suggestion.term, input_string)
        return suggestion


def distance_between_words(word1, word2):
    if platform.system() != "Windows":
        return damerau_levenshtein_distance(word1, word2)
    else:
        return levenshtein_distance(word1, word2)
    
    # return typo_distance(s=word1, t=word2, layout='AZERTY')


if __name__ == "__main__":
    ssc = SySpellCompound()
    print(ssc.load_dictionary("fr_full.txt", term_index=0, count_index=1))
    print(ssc.dictionary.get("frprobleme"))
    # print(ssc.create_dictionary("model_fr.txt", "fr"))

    print(ssc.lookup_compound(input_string="le problm avc cete solutin", edit_distance_max=3))
