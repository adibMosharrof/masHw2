from itertools import combinations
import re


class Coalition:
    initial_value = 0
    optimal_value = None
    structure = []
    optimal_structure = []

    def get_value(self):
        return self.optimal_value or self.initial_value
    
    def get_optimal_structure(self):
        if len(self.optimal_structure) > 0:
            return self.optimal_structure
        return self.structure 

from itertools import combinations

class Coalition:
    initial_value = 0
    optimal_value = None
    structure = []
    optimal_structure = []

    def __init__(self, text):
        structure_text = re.findall(r'{(.*?)}', text).pop()
        self.structure = [int(numeric_string) for numeric_string in structure_text.split(',')]
        self.initial_value = int(text.split(",").pop())

    def get_value(self):
        return self.optimal_value or self.initial_value

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return "C(%s) " % (self.structure)


class Program:
    players = None  # 4
    players_as_array = []
    output = []
    data = {}
    comb = []

    def init(self):
        self.read_input_file()
        max_coalition_structure = self.get_optimal_coalition()
        self.write_output(max_coalition_structure)
        a = 1

    def write_output(self, max_coalition_structure):
        coalition = self.data[str(max_coalition_structure)]
        self.get_optimal_structure_for_output(coalition)
        with open('optimalCS.txt', mode = 'w+') as outputFile:
            text = str(coalition.optimal_value) + '\n'
            for row in self.output:
                text += "{%s}\n" % ','.join(str(x) for x in row )
            outputFile.write( text )
    
    def get_optimal_structure_for_output(self, coaltion):
        if len(coaltion.optimal_structure) > 1:
            for structure in coaltion.optimal_structure:
                self.get_optimal_structure_for_output(self.data[str(structure)])
        else:
            self.output.append(coaltion.optimal_structure[0])
            
    def get_optimal_coalition(self):
        max_coalition_value = 0
        max_coalition_structure = ""
        for i in range(1, self.players + 1):
            coalitions = self.get_coalitions(i)
            for coalition in coalitions:
                combs = self.get_combinations(i, coalition.structure)
                self.update_coalition(coalition, combs)
                if coalition.optimal_value > max_coalition_value:
                    max_coalition_value = coalition.optimal_value
                    max_coalition_structure = coalition.structure
                    
        return max_coalition_structure
    
    def update_coalition(self, coalition, combs):
        max_combination_value = -1
        max_comb = None
        for comb in combs:
            comb_value = 0
            for c in comb:
                comb_value += self.get_combination_value(c)
            if(comb_value > max_combination_value):
                max_combination_value = comb_value
                max_comb = self.get_plain_list_from_tuple_list(comb)
                               
        coalition.optimal_value = max_combination_value
        coalition.optimal_structure = max_comb
    
    def get_combination_value(self, combination):
        output = 0
        if type(combination) is list:
            for comb in combination:
                output += self.get_combination_value(comb)
        else:
            list_c = list(combination)
            key = str(list_c)
            output = self.data[str(key)].get_value()
        return output    
    
    def get_plain_list_from_tuple_list(self, comb): 
        plain_list = []
        for tl in comb:
            plain_list.append(list(tl))
        return plain_list    
    
    def get_coalitions(self, maximum_coalition_size):
        comb = list(combinations(self.players_as_array, maximum_coalition_size))
        coalitions = []
        for c in comb:
            coalitions.append(self.data[str(list(c))])
        return coalitions

    def get_combinations(self, maximum_coalition_size, coalition):
        output_combinations = []
        combs = []
        for i in range(maximum_coalition_size):
            combs.append(list(combinations(coalition, i + 1)))

        output_combinations.append(combs.pop())
        return self.__join_combinations(combs, output_combinations)

    def __merge_two_combinations_arrays(self, a, b, output):
        for i in range(len(a)):
            output.append([a[i], b[-i - 1]])

    def __merge_one_combination_array(self, a, output):
        for i in range(int(len(a) / 2)):
            output.append([a[i], a[-1 - i]])

    def __join_combinations(self, comb, output):
        if len(comb) is 1:
            self.__merge_one_combination_array(comb[0], output)
            return output
        if len(comb) is 0:
            return output
        
        self.__merge_two_combinations_arrays(comb.pop(0), comb.pop(), output)
        self.__join_combinations(comb, output)
        return output

    def read_input_file(self):
        filepath = 'gameCS.txt'
        with open(filepath) as fp:
            line = fp.readline()
            self.players = int(line)
            for i in range(1, self.players + 1):
                self.players_as_array.append(i)
            while line:
                line = fp.readline()
                if (line is ''):
                    continue
                c = Coalition(line)
                self.data[str(c.structure)] = c


program = Program()
program.init()
