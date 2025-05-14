import re
from fractions import Fraction

exp_number = re.compile(r'^[+-]?\d*\.?\d+$|^[+-]?\d+\.?\d*$|^[+-]?\d+/\d+$')

def isNumber(number) -> bool:
    return bool(exp_number.match(number))

def parse_number(num_str):
    if '/' in num_str:
        return float(Fraction(num_str))
    elif '.' in num_str:
        return float(num_str)
    else:
        return int(num_str)

class Input():

    def __init__(self, file):
        self.file = file
        self.c = []
        self.a = []
        self.b = []
        self.opt = ""
        self.necessity_fase1 = False
        self.num_constraints = 0
        self.num_vars = 0

    def read(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            self.num_constraints = sum(1 for line in lines[1:] if '>=' in line or '<=' in line or '>' in line or '<' in line)
            f.seek(0)

            all_vars = set()
            for line in lines:
                for word in line.split():
                    if 'x' in word:
                        x_part = word.split('x')[-1]
                        if x_part and x_part.isdigit():
                            all_vars.add(int(x_part))
            self.num_vars = max(all_vars) if all_vars else 0

            slack_pos = 0

            for i, line in enumerate(f):
                separete_words = line.split()
                if not separete_words:
                    continue

                if separete_words[0] in ("max", "min"):
                    self.opt = separete_words[0]
                    self.c = [0] * self.num_vars
                    separete_words = separete_words[2:]  # Pula 'max/min' e 'z ='

                    next_coef = 1
                    for word in separete_words:
                        if word == '-':
                            next_coef = -1
                        elif word == '+':
                            next_coef = 1
                        elif 'x' in word:
                            parts = word.split('x')
                            coef = 1
                            if parts[0]:
                                if parts[0] == '-':
                                    coef = -1
                                elif parts[0] == '+':
                                    coef = 1
                                else:
                                    coef = parse_number(parts[0])
                            coef *= next_coef

                            var_num = int(parts[1]) if len(parts) > 1 and parts[1] else 1
                            if var_num <= self.num_vars:
                                self.c[var_num - 1] = coef
                            next_coef = 1
                    self.c.extend([0] * self.num_constraints)

                else:
                    aux = [0] * self.num_vars
                    inequality = ''
                    independent_term = 0
                    next_coef = 1
                    found_inequality = False

                    for word in separete_words:
                        if word == '-':
                            next_coef = -1
                        elif word == '+':
                            next_coef = 1
                        elif word in (">=", "<=", "=", ">", "<"):
                            inequality = word
                            found_inequality = True
                        elif 'x' in word:
                            parts = word.split('x')
                            coef = 1
                            if parts[0]:
                                if parts[0] == '-':
                                    coef = -1
                                elif parts[0] == '+':
                                    coef = 1
                                else:
                                    coef = parse_number(parts[0])
                            coef *= next_coef

                            var_num = int(parts[1]) if len(parts) > 1 and parts[1] else 1
                            if var_num <= self.num_vars:
                                aux[var_num - 1] = coef
                            next_coef = 1
                        elif found_inequality and isNumber(word.replace('-', '')):
                            independent_term = parse_number(word) * next_coef

                    self.b.append(independent_term)

                    if inequality in (">", ">=", "="):
                        self.necessity_fase1 = True

                    if inequality in ('>=', '<=', '>', '<'):
                        slack_vars = [0] * self.num_constraints
                        if inequality == '<=' or inequality == '<':
                            slack_vars[slack_pos] = 1
                        else:  # '>=' '>'
                            slack_vars[slack_pos] = -1
                        slack_pos += 1
                        full_row = aux + slack_vars
                    else:  # '='
                        full_row = aux + [0] * self.num_constraints

                    self.a.append(full_row)

    def getInputs(self):
        if self.opt == 'max':
            for i in range(self.num_vars):
                self.c[i] += -1
        for i in range(len(self.b)):
            if self.b[i] < 0:
                for j in range(len(self.a[i])):
                    self.a[i][j] *= -1
        return self.c, self.a, self.b

    def getNumVars(self):
        return self.num_vars, self.num_constraints