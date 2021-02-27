__author__ = 'Ldaze'

import random
import numpy as np
import copy


def lesson_initialization(lessons):
    """Input lessons and distribute a number for every lesson."""
    lesson_num = [i for i in range(0, len(lessons))]
    catalog = dict(zip(lesson_num, lessons))
    return catalog


def translate(chromosome, catalog):
    """Visualizing gene coding."""
    time_table = [[] for i in range(0, len(chromosome))]
    tmp = []
    for i, v in enumerate(chromosome):
        for j in v:
            tmp.append(catalog.get(j))
        time_table[i] = copy.deepcopy(tmp)
        tmp.clear()
    return time_table


def init_chromosome(workdays, times, nums):
    """
    Initialize a chromosome.
    :param workdays: Teaching days required in a week.
    :param times: Teaching arrangement in a day.
    :param nums: Number of courses.
    """
    chromosome = [[] for i in range(workdays)]
    gene = [0 for i in range(times)]
    for i in range(workdays):
        for j in range(times):
            gene[j] = random.randrange(nums)
        chromosome[i] = copy.deepcopy(gene)
    return chromosome


def init_individual(class_nums, *args):
    individual = []
    for i in range(class_nums):
        individual.append(init_chromosome(*args))
    return individual


def species_origin(comm_num, *args):
    """
    Initialize a original species.
    :param comm_num: Define the number of species.
    """
    species = [[] for i in range(comm_num)]
    for i in range(comm_num):
        species[i] = init_individual(*args)
    species = np.array(species)
    return species


def fitness(chromosome, lesson_quantity, vector):
    """Evaluation adaptability."""
    score = 0
    for i, v in enumerate(chromosome):
        for j in range(1, lesson_quantity):
            repeat_nums = np.sum(v == j)
            if repeat_nums <= 1:
                score += 200
            elif 1 < repeat_nums <= 3:
                score -= 60
            elif 3 < repeat_nums <= 4:
                score -= 80
            elif 4 < repeat_nums <= 5:
                score -= 100
            else:
                score -= 800
        if i < len(chromosome) - 1:
            for k in v:
                if k not in chromosome[i + 1]:
                    score += 180
                else:
                    score -= 80

        for j, k in enumerate(v):
            if k in vector[i][j]:
                score -= 800
    return score


def cal_score(individual, *args):
    score = 0
    for i in individual:
        score += fitness(i, *args)
    return score


def unifies(scores, species):
    """Delete every negative score."""
    for i, v in enumerate(scores):
        if v < 0:
            del scores[i]
            species = np.delete(species, i, axis=0)
    return species


# def summation(scores):
#     """Sum of the scores."""
#     total = 0
#     for i in scores:
#         total += i
#     return total


def cum_sum(pro):
    """Divide intervals for roulette.
       example：[0.1,0.2,0.15,0.3,0.25]
                [0.1,0.3,0.45,0.75,1]
                [0,0.1,0.3,0.45,0.75,1]
    """
    intervals = []
    for i, v in enumerate(pro):
        if i == 0:
            intervals.append(v)
        else:
            intervals.append(v + intervals[i-1])
    intervals.insert(0, 0)
    return intervals


def select(scores, species):
    """Select individuals with high adaptability. """
    total = sum(scores)
    probabilities = []
    for i in range(len(scores)):
        probabilities.append(scores[i] / total)
    intervals = cum_sum(probabilities)
    new_species = []
    index = 0
    while index < len(species):
        rand = random.random()
        for i, v in enumerate(intervals):
            if intervals[i - 1] <= rand < v:
                if len(new_species) == 0:
                    new_species = np.array([species[i - 1]])
                else:
                    new_species = np.append(new_species, [species[i - 1]], axis=0)
        index += 1
    return new_species


def arb_hybridization(species):
    """Born new individual."""
    tmp1 = random.choice(species)
    tmp2 = random.choice(species)
    rand = random.randrange(0, len(species[0]))
    child1 = np.vstack((tmp1[0:rand], tmp2[rand:len(species[0])]))
    child2 = np.vstack((tmp2[0:rand], tmp1[rand:len(species[0])]))
    child = [child1, child2]
    return [child[random.randint(0, 1)]]


def delete(species, index):
    """Delete the chromosome in species."""
    if index == 0:
        return np.array(species[1:len(species)])
    else:
        tmp1 = np.array(species[0:index])
        tmp2 = np.array(species[index + 1:len(species)])
    return np.append(tmp1, tmp2, axis=0)


def select_best_index(scores):
    """Select index of the best individual in the species."""
    return scores.index(max(scores))


def select_best_species(species, scores, n):
    """Select excellent individuals."""
    tmp_scores = scores.copy()
    tmp_species = np.array(species)
    index = select_best_index(tmp_scores)
    excellent_species = np.array([tmp_species[index]])
    tmp_species = delete(tmp_species, index)
    del tmp_scores[index]
    for i in range(0, n-1):
        index = select_best_index(tmp_scores)
        tmp = np.array([tmp_species[index]])
        excellent_species = np.append(excellent_species, tmp, axis=0)
        tmp_species = delete(tmp_species, index)
        del tmp_scores[index]
    return excellent_species


def crossover(species, scores, n):
    """
    Cross combination.
    :param species: Ignore.
    :param scores: Ignore.
    :param n: Retain several excellent chromosomes.
    """
    num = len(species)
    new_species = np.array(select_best_species(species, scores, n))  # Retain several excellent chromosomes
    # new_species = np.array(select_best(species,scores))
    for i in range(0, num-n):
        new_species = np.append(new_species, arb_hybridization(species), axis=0)
    return new_species


def vary(species, lesson_quantity, iters=40, p=0.4):
    """
    Produce variation.
    :param species: Ignore.
    :param lesson_quantity: Ignore.
    :param iters: Number of iterations.
    :param p: Probability threshold of variation.
    """
    c = 0
    while c < iters:
        rand = random.random()
        if rand <= p:
            individual = random.randrange(0, len(species))
            chromosome = random.randrange(0, len(species[0]))
            gene = random.randrange(0, len(species[0][0]))
            base = random.randrange(0, len(species[0][0][0]))
            species[individual][chromosome][gene][base] = random.randrange(0, lesson_quantity)
        c += 1


def iteration(lesson_quantity, vector, species, threshold, n=1):
    """
    Genetic iteration.
    :param lesson_quantity: The quantity of lessons.
    :param vector: Forbidden space.
    :param species: Ignore.
    :param threshold: Fitness threshold.
    :param n: Retain several excellent chromosomes.
    :return: The best species.
    """
    score = []
    scores = []
    while 1:
        for i in species:
            scores.append(cal_score(i, lesson_quantity, vector))
        species = unifies(scores, species)
        species = select(scores, species)
        species = crossover(species, scores, n)
        vary(species, lesson_quantity)
        for i in species:
            score.append(cal_score(i, lesson_quantity, vector))
        print(score)
        for i, v in enumerate(score):
            if v >= threshold:
                return species[i]
        scores.clear()
        score.clear()


def run(lessons_list, class_nums, workdays, times, comm_num, vector, threshold=2000, n=10):
    """
    Run the program.
    :param lessons_list: Lessons set.
    :param class_nums: Number of class.
    :param workdays: Teaching days required in a week.
    :param times: Teaching arrangement in a day.
    :param comm_num: Initial number of original species.
    :param vector: Forbidden space.
    :param threshold: Fitness threshold.
    :param n: Retain several excellent chromosomes.
    """
    while 1:
        try:
            lessons = lesson_initialization(lessons_list)
            species = species_origin(comm_num, class_nums, workdays, times, len(lessons))
            best_individual = iteration(len(lessons_list), vector, species, threshold, n)
            time_table = []
            for i in best_individual:
                time_table.append(translate(i, lessons))
            # print(lessons)
            # print(best_individual)
            # for i in time_table:
            #     print(i)
        except (IndexError, ValueError):
            continue
        else:
            return time_table


if __name__ == '__main__':
    lesson = ['自习', '数据库', '操作系统', '数据结构', 'C', 'Python', 'database']
    vec = [
        [
            [1, 3], [2, 4], [3], [], [], [], [], []
        ],
        [
            [3], [], [5], [], [], [], [], []
        ],
        [
            [], [], [6], [], [], [2, 4], [], []
        ],
        [
            [], [], [7], [], [], [], [], [3, 7]
        ],
        [
            [], [], [1], [], [], [], [1, 2, 4], []
        ],
    ]
    run(lesson, 6, 5, 8, 50, vec, 3000)

