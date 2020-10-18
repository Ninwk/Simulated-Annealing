import math
import random
from typing import List, Any
import visualize_tsp


class sa(object):

    def __init__(self):
        self.places = []
        self.initial_place()
        self.NUM = len(self.places)
        # 总城市数
        self.T = 8
        # 初始温度
        self.D = 0.995
        # 降温速率
        self.stop_T = 1e-50
        # 终止温度
        self.stop_I = 100000
        self.iteration = 1
        # 终止次数

        self.nodes = [i for i in range(self.NUM)]
        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []
        self.current_sol = []
        self.current_fit = 0

    def initial_solution(self):
        """
        初始化贪心算法的路径，以便后续模拟退火算法来进行优化
        :return: 贪心算法最短路径已经路径长度
        """
        i_nodes = random.choice(self.nodes)
        # 随机寻找初始城市/节点
        node_solution = [i_nodes]
        # 节点加入列表
        f_nodes = set(self.nodes)
        # 定义空闲城市列表/节点
        f_nodes.remove(i_nodes)
        # 释放随机寻找到的初始城市/节点

        while f_nodes:
            next_node = min(f_nodes, key=lambda x: self.dist(i_nodes, x))
            # 求最近节点
            f_nodes.remove(next_node)
            node_solution.append(next_node)
            # 添加最近节点至解决路径里
            i_nodes = next_node
            # 遍历节点

        current_fit = self.fitness(node_solution)
        if current_fit < self.best_fitness:
            self.best_fitness = current_fit
            self.best_solution = node_solution
        self.fitness_list.append(current_fit)
        visualize_tsp.plotTSP([node_solution], self.places)
        return node_solution, current_fit

    def ann(self):

        self.current_sol, self.current_fit = self.initial_solution()
        while self.T >= self.stop_T and self.iteration < self.stop_I:
            candidate = list(self.current_sol)
            ol = random.randint(2, self.NUM - 1)
            oi = random.randint(0, self.NUM - ol)
            candidate[oi: (oi + ol)] = reversed(candidate[oi: (oi + ol)])
            self.accept(candidate)

            self.T *= self.D
            self.iteration += 1

            self.fitness_list.append(self.current_fit)

        self.priStu()
        print("最佳的最短路径长度: ", self.best_fitness)
        print("共迭代次数:%d" % self.iteration)
        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        print(f"对贪心算法的改进率: {improvement : .2f}%")

    def priStu(self):
        print("-------学号:18401010124，班级:网络181，姓名:吴冰寒-------")
    def accept(self, candidate):
        """
        一定概率接受
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.current_fit:
            self.current_fit, self.current_sol = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.current_fit, self.current_sol = candidate_fitness, candidate

    def initial_place(self):
        place = open("coord.txt", "r")
        for line in place.readlines():
            line = [float(x.replace("\n", "")) for x in line.split(" ")]
            self.places.append(line)

    def dist(self, node_0, node_1):
        """
        求出距离节点0最近的节点1
        """
        coord_0, coord_1 = self.places[node_0], self.places[node_1]
        return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

    def fitness(self, solution):
        """
        求出solution的总路径长度
        """
        cur_fit = 0
        for i in range(self.NUM):
            cur_fit += self.dist(solution[i % self.NUM], solution[(i + 1) % self.NUM])
        return cur_fit

    def p_accept(self, candidate_fitness):
        return math.exp(-abs(candidate_fitness - self.current_fit) / self.T)

    def r_sol(self):
        return self.best_solution, self.places

# print(dka)
# visualize_tsp.plotTSP([ok], sa().places)
