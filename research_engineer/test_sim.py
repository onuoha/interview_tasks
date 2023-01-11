'''
import required libraries and modules
FLASK provides the application instance, REQUEST allows for methods to be added to routes, and JSONIFY encodes python dictionary to JSON
This task was solved by CHIDIEBERE ONUOHA on 10.01.2023
'''
from flask import Flask, request, jsonify
import pandapower as pp
import pandas as pd
#create empty net
net = pp.create_empty_network() 

#create buses
b1 = pp.create_bus(net, vn_kv=20., name="Bus 1")
b2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
b3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")

#create bus elements
pp.create_ext_grid(net, bus=b1, vm_pu=1.02, name="Grid1")           # Changed name from 'Grid Connection' to 'Grid1'
pp.create_ext_grid(net, bus=b3, vm_pu=1.00, name="Grid2")           # Added a second Grid to bus 3
pp.create_load(net, bus=b3, p_mw=0.1, q_mvar=0.05, name="load1")    # Changed name from 'Load' to 'load1'
pp.create_load(net, bus=b2, p_mw=0.15, q_mvar=0.04, name="load2")   # Added a second load to bus 2
pp.create_gen(net, bus=b3, p_mw=0.2, q_mvar=0.07, name="gen1")      # Added a generator to bus 3
pp.create_gen(net, bus=b2, p_mw=0.15, q_mvar=0.03, name="gen2")     # Added a second generator to bus 2

#create branch elements
tid = pp.create_transformer(net, hv_bus=b1, lv_bus=b2, std_type="0.4 MVA 20/0.4 kV", name="Trafo")
pp.create_line(net, from_bus=b2, to_bus=b3, length_km=0.1, name="Line",std_type="NAYY 4x50 SE")   


def run_simulation():
    pp.runpp(net)
    return net

# Created a function to extract the Active and Reactive power for Loads, External Grids and Generators and convert them into a single dictionary.
def simresult():
    # Assigns the return value of the run_simulation() to result
    result = run_simulation()
    # Extracts the output load result
    myloads = result.res_load
    # Extracts on the Active and Reactive power of the output gen result
    mygen = result.res_gen[['p_mw', 'q_mvar']]
    # Extracts the output result of ext_grid
    myext_grid = result.res_ext_grid
    # Adds a column with name as 'item' containing specific load name e.g. 'load1'
    myloads['item'] = net.load.name
    # Sets 'item' column as index column
    myloads = myloads.set_index('item')
    # Adds a column with name as 'item' containing specific gen name e.g. 'gen1'
    mygen['item'] = net.gen.name
     # Sets 'item' column as index column
    mygen = mygen.set_index('item')
     # Adds a column with name as 'item' containing specific ext_grid name e.g. 'Grid1'
    myext_grid['item']  = net.ext_grid.name
     # Sets 'item' column as index column
    myext_grid = myext_grid.set_index('item')
    # Concatenates all dataframes into a single dataframe, 'psys'
    psys = pd.concat([myloads, mygen, myext_grid], axis=0)
    # Converts dataframe into a dictionary required for jsonify module of Flask
    simres = psys.to_dict(orient = 'index')
    # Block of code to group the elements
    loads = {}
    generator = {}
    external_grid = {}
    sys = {}
    for i in simres.keys():
        if i.startswith('load'):
            loads[i] = simres[i].copy()
        elif i.startswith('gen'):
            generator[i] = simres[i].copy()
        elif i.startswith('Grid'):
            external_grid[i] = simres[i].copy()
    sys = {'loads':loads, 'generators':generator, 'external_grid':external_grid}
    return sys

# initializes Flask object
app = Flask(__name__)
# initializes simresult as module of test_sim in 'test_sim.py'
rsim = simresult()
# Creates a route for endpoint via 'grid-power-analysis'
@app.route('/grid-power-analysis', methods=['GET'])
# Defines a function for the route to use HTTP methods
def grid():
    if request.method == 'GET':
        if len(rsim)>0:
            return jsonify(rsim)
        else:
            "Nothing Found", 404

# Runs application
if __name__ == '__main__':
    app.run()

