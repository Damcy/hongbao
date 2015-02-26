# -*- encoding=utf-8 -*-
# author: Damcy <stmayue@gmail.com>
# create on: 2015-02-24
# description: 模拟微信抢红包

import os
import sys
import random

# 总人数
total_person_num = 4
# 每人起始金额
candidates = [975, 975, 975, 975]
# 红包占总金额的最大上限
up_percent = 0.75
# 手气最佳需要翻的倍数
who_win = 2
# 第一个红包里面有多少钱
first_hongbao = 100
# 轮次计数
times = 0


def all_info():
    """
    打印当前的玩家状态
    :return: None
    """
    global candidates, times
    print("当前第%d轮" % times)
    for i in list(range(0, len(candidates))):
        print("第%d个人当前钱数为%.2f" % (i + 1, candidates[i]))


def check_valid():
    """
    检测当前钱数是否合法(> 0)
    :return: bool
    """
    global candidates
    for i in list(range(0, len(candidates))):
        if candidates[i] < 0:
            return False
    return True


def distribute_hongbao(total_money, person_num):
    """
    随机分配 total_money 给 person_num 个人
    :param total_money: 供分配的钱数
    :param person_num: 人数
    :return: false or result list
    """
    global up_percent
    if total_money < person_num * 0.01:
        return False
    result = []
    for i in list(range(1, person_num)):
        this_money = round(random.uniform(0.01, total_money*up_percent), 2)
        result.append(this_money)
        total_money = total_money - this_money
    result.append(round(total_money, 2))
    random.shuffle(result)
    return result


def add_money(wat_we_get):
    """
    结算每位参与者的钱数
    :param wat_we_get: 本轮的钱数分配
    :return: None
    """
    global candidates
    for i in list(range(0, len(wat_we_get))):
        candidates[i] += wat_we_get[i]


def find_max(wat_we_get):
    """
    找到本轮分配的红包中拿到最多的一个
    :param wat_we_get: 本轮的钱数分配
    :return:  [钱数最多的人所在 index , money]
    """
    max_val = max(wat_we_get)
    return [wat_we_get.index(max_val), max_val]


def play_next(pre_victor):
    global candidates, total_person_num, who_win
    money = pre_victor[1] * who_win
    candidates[pre_victor[0]] -= money
    wat_we_get = distribute_hongbao(money, total_person_num)
    if wat_we_get:
        victor = find_max(wat_we_get)
        print(wat_we_get)
        print(victor)
        add_money(wat_we_get)
        if check_valid():
            return [True, victor]
        else:
            return [False, victor]
    else:
        return [False, []]


def first_time():
    """
    第一次抢红包
    :return: [bool, victor_info]
    """
    global total_person_num, times, first_hongbao
    all_info()
    wat_we_get = distribute_hongbao(first_hongbao, total_person_num)
    victor = find_max(wat_we_get)
    add_money(wat_we_get)
    flag = check_valid()
    # print(wat_we_get)
    # print(victor)
    times += 1
    all_info()
    return [flag, victor]


def main():
    global times
    flag, victor = first_time()
    while flag:
        times += 1
        flag, victor = play_next(victor)
        all_info()


if __name__ == '__main__':
    sys.exit(main())