import re


class Regex:
    def __init__(self, regex_string):
        self.regex_string = regex_string

    def split_parenthesis(self, regex_string):
        i = 0
        regex_array = ""
        for c in regex_string:
            i += 1
            if c == "(":
                return self.split_parenthesis(regex_string[i:])
            elif c == ")":
                print(regex_array)
            else:
                regex_array += c

        return regex_array

    def text_match(self, text, regex):
        patterns = regex
        if re.search(patterns, text):
            return True
        else:
            return False
