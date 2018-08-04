from flask import Flask, jsonify, render_template, request, session
import os
import pandas as pd
import helpers


app = Flask(__name__)
app.secret_key = os.urandom(24)
results = helpers.load_data("csv/ahs_air_output_saved.csv")

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
# "cd ~/1_Programming/Energize_Andover/Assignments/4_Assignment/ ;

@app.route("/", methods={"GET"})
def index():
    message = "Please wait for data"

    return render_template("index.html")


@app.route("/update_all", methods={"GET"})
def update(): # sends JSON containing the updated data
    global results
    print("Updating")
    #os.system('python3 ahs_air.py -h 10.12.4.98 -p 8000 ; wait')

    results = helpers.load_data("csv/ahs_air_output.csv")

    # save the temporary values into permanent storage
    os.system('cp ahs_air_output.csv ahs_air_output_saved.csv ; wait')

    return jsonify(results)


@app.route("/load_saved_data", methods={"GET"})
def load_saved_data(): # sends JSON containing saved data
    global results
    results = helpers.load_data("csv/ahs_air_output_saved.csv")
    print("data to be sent: ")
    print(results)
    json = jsonify(results)
    return json


@app.route("/update_area", methods={"GET"})
def update_area():
    os.system("pgrep python3 > process_id.txt")
    file = open("process_id.txt", 'r')
    process_id = file.read()
    print(process_id)
    file.close()
    if process_id != "":
        # kill any other queries, there can be only one
        os.system("kill -9 " + str(process_id))

    wing = request.args.get("wing")
    floor = request.args.get("floor")
    #os.system('python3 query_specific.py -h 10.12.4.98 -p 8000 -w ' + wing + ' -f ' + floor + ' ; wait')

    global results
    area_results = helpers.load_data("csv/ahs_air_specific_output.csv")
    results = helpers.update_data(results, area_results, ord(wing) - ord('A'), int(floor))
    return jsonify(results)

@app.route("/update_floor", methods={"GET"})
def update_floor():
    global results
    os.system("pgrep python3 > process_id.txt")
    file = open("process_id.txt", 'r')
    process_id = file.read()
    print(process_id)
    file.close()
    if process_id != "":
        # kill any other queries, there can be only one
        os.system("kill -9 " + str(process_id))

    floor = request.args.get("floor")
    os.system('python3 query_specific.py -h 10.12.4.98 -p 8000 -w A -f ' + floor + ' ; wait')
    area_results = helpers.load_data("csv/ahs_air_specific_output.csv")
    results = helpers.update_data(results, area_results, ord('A') - ord('A'), int(floor))

    print("A", results)

    os.system('python3 query_specific.py -h 10.12.4.98 -p 8000 -w B -f ' + floor + ' ; wait')
    area_results = helpers.load_data("csv/ahs_air_specific_output.csv")
    results = helpers.update_data(results, area_results, ord('B') - ord('A'), int(floor))

    print("B", results)

    os.system('python3 query_specific.py -h 10.12.4.98 -p 8000 -w C -f ' + floor + ' ; wait')
    area_results = helpers.load_data("csv/ahs_air_specific_output.csv")
    results = helpers.update_data(results, area_results, ord('C') - ord('A'), int(floor))

    print("C", results)

    os.system('python3 query_specific.py -h 10.12.4.98 -p 8000 -w D -f ' + floor + ' ; wait')
    area_results = helpers.load_data("csv/ahs_air_specific_output.csv")
    results = helpers.update_data(results, area_results, ord('D') - ord('A'), int(floor))

    print("D", results)

    return jsonify(results)
