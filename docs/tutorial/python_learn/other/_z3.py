from z3 import *

# 注意，z3 解得的模型只是一个可行解，不一定是最优解
"""var and notatation"""
### Int ###
# x = Int("x")
# y, z = Ints("y z")
# y = 2
# print(x + y + 1)

### Bool ###
# b1 = Bool("b2")  # 注意命名
# solve(b1 == True)

### Real ###
# x = Real("x")
# # print(x + 1 / 3)  # wrong
# print(x + RealVar(1) / 3)
# print(x + Q(1, 3))
# print(x + "1/3")
# print(x + 0.25)
# # set_option(rational_to_decimal=True)
# solve(3 * x == 1)

### And & Or ###

### BitVec ###
# def is_power_of_two(n):
#     return And(n > 0, n & (n - 1) == 0)


# x = BitVec("x", 32)
# solve(is_power_of_two(x))
"""变量定义"""


"""solve"""
# z = Real("z")
# solve(3 * z == 1)
# x = Real("x")
# y = Real("y")
# solve(x**2 + y**2 > 3, x**3 + y < 5)
# set_option(precision=30)  # solving, and displaying result with 30 decimal places
# solve(x**2 + y**2 == 3, x**3 == 2)
"""直接求解"""

"""SMT-LIB2 scripts"""
# Tie, Shirt = Bools("Tie Shirt") # 创建两个布尔变量
# s = Solver() # 创建一个求解器
# s.add(Or(Tie, Shirt), Or(Not(Tie), Shirt), Or(Not(Tie), Not(Shirt)))
# print(s.check()) # sat 表示有解
# print(s.model()) # 解模型

"""args"""
# x, y = Ints('x y')
# n = x + y >= 3
# print("children: ", n.children())  # [x + y, 3]
# print("num args: ", n.num_args())  # 2
# print("1st child:", n.arg(0))  # x + y
# print("2nd child:", n.arg(1))  # 3
# print("operator: ", n.decl())  # >=
# print("op name:  ", n.decl().name())  # >=

"""simplify"""
# x, y = Ints("x y")
# print(simplify(x + y + 2 * x + 3))
# print(simplify(x < y + x + 2))
# print(simplify(And(x + 1 >= 3, x**2 + x**2 + y**2 + 2 >= 5)))
"""化简"""

"""set_option"""
# x = Int("x")
# y = Int("y")
# print(x**2 + y**2 >= 1)
# set_option(html_mode=False)
# print(x**2 + y**2 >= 1)

"""Sorts and functions"""
# Z = IntSort()
# B = BoolSort()
# f = Function("f", Z, B)
# x = Int("x")  # Create an integer variable
# s = Solver()
# s.add(
#     ForAll([x], f(x) == (x + 1 == 0))
# )  # Use x instead of Z, and make sure the equality returns a boolean
# print(s.check())
# print(s.model() if s.check() == sat else "No solution")
"""集合和映射"""
