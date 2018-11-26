import random

def remove_duplicates(var_list):
    var_list_unique = []
    for i in range(len(var_list)):
        if var_list[i] not in var_list_unique:
            var_list_unique.append(var_list[i])
    return var_list_unique

'''
could potentially add a make_legend function here??
'''


class Countries:
    
    def __init__(self, country_name, colour_variable, year_list, cba, wdi, country_list):
        self.cba = cba
        self.wdi = wdi
        self.name = country_name
        self.years = year_list
        self.colour_variable = colour_variable
        self.colour = colour_variable
        self.country_list = country_list
        
    def __repr__(self):
        return (f"[{self.name}, CBA: {self.cba}, WDI: {self.wdi}]")
    
    def make_colours(self):
        var_list = []
        for i in range(len(self.country_list)):
            var_list.append(self.country_list[i].colour_variable)
        var_list = remove_duplicates(var_list)
        
        colour_list = []
        while len(colour_list) < len(var_list):
            colour_list.append('#' + "%06x" % random.randint(0, 0xFFFFFF))
            colour_list = remove_duplicates(colour_list)

        colour_index = [var_list, colour_list]
        return colour_index
    
    def assign_colours(self, colour_index):
        for i in range(len(colour_index[0])):
            if self.colour_variable == colour_index[0][i]:
                self.colour = colour_index[1][i]

