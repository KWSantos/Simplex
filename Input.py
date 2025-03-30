import re

exp_number = re.compile("^[0-9]+$")


def isNumber(number) -> bool:
    return bool(exp_number.match(number))


class Input():

    def __init__(self, file):
        self.file = file
        self.c = []
        self.a = []
        self.b = []
        self.opt = ""
        self.num_constraints = 0
        self.num_vars = 0

    def read(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            self.num_constraints = len(lines) - 1
            f.seek(0)

            count_x = 0
            for i, line in enumerate(f):
                separete_words = line.split()
                if not separete_words:
                    continue

                if separete_words[0] == "max" or separete_words[0] == "min":
                    self.opt = separete_words[0]
                    separete_words.pop(0)
                    separete_words.pop(0)
                    next_coef = 1
                    for word in separete_words:
                        if word == '-':
                            next_coef = -1
                        elif word == '+':
                            next_coef = 1
                        elif isNumber(word[0]):
                            count_x += 1
                            self.c.append(int(word[0]) * next_coef)
                            next_coef = 1
                        elif word[0] == 'x':
                            self.c.append(1 * next_coef)
                            count_x += 1
                            next_coef = 1

                    self.num_vars = count_x
                    self.c.extend([0] * self.num_constraints)

                else:
                    next_coef = 1
                    aux = []
                    inequality = ''
                    independent_term = None

                    for word in separete_words:
                        if word == '-':
                            next_coef = -1
                        elif word == '+':
                            next_coef = 1
                        elif word in (">=", "<=", "=="):
                            inequality = word
                        elif word[0] == 'x':
                            aux.append(1 * next_coef)
                            next_coef = 1
                        elif word.startswith('-x'):
                            aux.append(-1 * next_coef)
                            next_coef = 1
                        elif isNumber(word[0]):
                            if 'x' in word:
                                coef = int(word.split('x')[0]) * next_coef
                                aux.append(coef)
                                next_coef = 1
                            else:
                                if word == separete_words[-1]:
                                    independent_term = int(word) * next_coef
                                else:
                                    aux.append(int(word) * next_coef)
                                    next_coef = 1
                        elif word.startswith('-') and len(word) > 1 and isNumber(word[1]):
                            if word == separete_words[-1]:
                                independent_term = int(word)
                            else:
                                aux.append(int(word) * next_coef)
                                next_coef = 1

                    if independent_term is None:
                        independent_term = 0

                    self.b.append(independent_term)

                    slack_vars = [0] * self.num_constraints

                    if inequality == ">=":
                        slack_vars[i - 1] = -1
                    elif inequality == "<=":
                        slack_vars[i - 1] = 1
                    elif inequality == "==":
                        slack_vars[i - 1] = 0
                    full_row = aux + slack_vars
                    self.a.append(full_row)

    def getInputs(self):
        return self.c, self.a, self.b