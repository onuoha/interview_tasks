
You need to create a script that will run a simple power flow calculation using pandapower https://github.com/e2nIEE/pandapower and present its results via a REST API. The task is expected to take at most 2 hours. You can find the Python module with the simulation code that you need to use here https://github.com/gridsingularity/interview_tasks/blob/master/research_engineer/test_sim.py. You do not need to create your own simulation script, you can use the one provided (test_sim.py), expose its results via a REST API, and expand it according to the requirements stated below. The main function of the script is the run_simulation, which returns the pandapower network object, which allows you to retrieve results from the power flow analysis of the grid. 

The API needs to expose only one endpoint: a GET request that runs the simulation and returns a dict with the active and reactive power for each node in the grid, grouped by loads, generators and external grid connections. The structure of the dict should be the following: 
```
{
   "loads": {
        "<load_1_name>": (<active_power>, <reactive_power>),
        .....
   },
   "generators": {
        "<gen_1_name>": (<active_power>, <reactive_power>),
        .....
   },
   "external_grid": {
        "<ext_grid_connection_1>": (<active_power>, <reactive_power>), 
        .....
   }
}
```

The endpoint should be reachable via /grid-power-analysis/. You are free to use any units for the active and reactive power, even though MW and Mvar are the default pandapower ones.

You can use any Python framework you like for the REST API (Flask, DRF, Bottle). 

After creating the API, you need to expand the provided simulation script by adding more nodes to it. One more medium / low voltage transformer needs to be added to the medium voltage bus, and on the low voltage side one load, one PV plant (that consists of individual 5 PVs, all connected on a separate bus and not coupled with the load) and one external connection. The active and reactive power values from these nodes need to be reported via the endpoint /grid-power-analysis/ that was implemented on the previous step.

In order to submit your solution to this task a fork of this repo has to be created, and the solution can be committed to the fork.

