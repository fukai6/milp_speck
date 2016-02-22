# milp_speck

The speck_diff_find is a python framework for automatic differential cryptanalysis which is developed based on the method presented in the paper "MILP-Based Automatic Search Algorithms for Differential and Linear Trails for Speck"

The step to generate the LP model:

1) Open the speck_diff_find.py or speck_line_find.py with IDLE(we run the code on Windows and the python version is 3.2.5)

2) Enter F5 to run 

3) Input "bar = speck(blocksize); bar.genModel(round)" to get the LP model

4) Use gurobi optimizer to solve the LP model

5) Use get_route_from_sol.sh or get_route_from_sol_1.sh to get the differential path

The example

We input “bar = speck(32); bar.genModel(3)” to get the 3 round speck32’s LP model.

The step to use gurobi to solve the LP model

1) run gurobi

2) Input "m=read("XXX.lp")" to read model

3) Input "m.optimize()" to solve

4) Input "m.write("XXX.sol")" to save the result 



References:

Kai fu, Meiqin Wang, Yinghua Guo, Siwei Sun, Lei Hu : MILP-Based Automatic Search Algorithms for Differential and Linear Trails for Speck
