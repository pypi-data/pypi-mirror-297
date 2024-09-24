import numpy as np
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution

from qusbt.testing import calculate_fail_number_GA

import math


class TestingProblem(IntegerProblem):
    def __init__(self, config_dic, solution_sheet, log_sheet):
        super(IntegerProblem).__init__()

        self.config_dic = config_dic
        self.solution_sheet = solution_sheet
        self.log_sheet = log_sheet

        n = len(config_dic['inputID'])
        # if 'M' in config_dic.keys():
        #     self.number_of_variables = config_dic['M']
        # else:
        #     self.number_of_variables = math.ceil(pow(2, n) * config_dic['beta'])

        self.obj_directions = [self.MINIMIZE]

        self.lower_bound = self.number_of_variables() * [0]

        self.upper_bound = self.number_of_variables() * [pow(2,n)-1]



    def number_of_variables(self) -> int:
        if 'M' in self.config_dic.keys():
            return self.config_dic['M']
        else:
            n = len(self.config_dic['inputID'])
            return math.ceil(pow(2, n) * self.config_dic['beta'])


    def number_of_objectives(self) -> int:
        return 1

    def number_of_constraints(self) -> int:
        return 0


    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        variables = np.array(solution.variables)
        p = calculate_fail_number_GA(variables, self.config_dic, self.solution_sheet, self.log_sheet)
        # the value is negated because we want to maximize "p" using a minimization problem
        solution.objectives[0] = -p
        return solution

    def name(self) -> str:
        return 'TestingProblem'
