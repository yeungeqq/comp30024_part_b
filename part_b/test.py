# Script used for testing the agent against against an opponent
# n number of times using multiprocessing to speed up the process.
# Gives some data on the performance of the agent.

import subprocess
import multiprocessing

num_games = 10
opponent = "testing_agents/agent3"
directory = "game_logs/random_1/"

def run_script(args):
    subprocess.run(["python", "-m", "referee", "-l"] + args + ["-s", "250", "-t", "180", "agent", opponent])

arg_list = []

for i in range(num_games):
    arg = directory + str(i) + "_game.log"
    arg_list.append([arg])

pool = multiprocessing.Pool(processes=len(arg_list))
pool.map(run_script, arg_list)
pool.close()
pool.join()

wins = 0
losses = 0
total_time = 0
total_turns = 0

for log in range(num_games):
    with open(directory + str(log) + "_game.log", "r") as file:
        lines = file.readlines()
    if lines:
        final_line = lines[-1].split()
        turn_line = lines[-3].split()
        if final_line[-1] == "winner:RED":
            wins += 1
        else:
            losses += 1
        total_time += float(final_line[0][1:-1])
        total_turns += int(turn_line[3])

print("\n")

print("wins: " + str(wins))
print("losses: " + str(losses))
print("average time: " + str(total_time/num_games))
print("average turns: " + str(total_turns/num_games))