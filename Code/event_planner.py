"""
Student Society Event Planner
"""
import time
from itertools import combinations
import sys
def read_input(filename):
    """
    Read input file and parse activity data.
    """
    activities = []
    #open the file and assign test to variable lines
    with open(filename, "r") as f:
        lines = [ln for ln in f]

    #assign n, t and b
    n = int(lines[0])
    line2 = lines[1].split()
    t = int(line2[0])
    b = int(line2[1])

    #iterate through each activity and assign parts to dictionary
    for i in range(n):
        name, time, cost, enjoyment = lines[i+2].split()
        activities.append({
            "name" : name,
            "time" : int(time),
            "cost" : int(cost),
            "enjoyment" : int(enjoyment),
        })
    f.close()
    return t, b, activities



def brute_force_solver(acts, t):
    """
    brute force algorithm which generates every possible subset.
    """
    start = time.perf_counter()
    #initialise variables
    best_enjoyment = -1
    best_acts = []
    best_time = 999
    best_cost = 0
    #iterate through each length of activities (1 to n)
    for i in range(len(acts)+1):
        #iterate through each combination of activities for that length
        for combs in combinations(acts, i):
            #check combination satisfies time constraint
            sum_time = sum(j["time"] for j in combs)
            if sum_time > int(t):
                continue
            sum_enjoyment = sum(k["enjoyment"] for k in combs)
            #find if enjoyment is better and make it current best if so
            if (sum_enjoyment > best_enjoyment or
                (sum_enjoyment == best_enjoyment and sum_time < best_time)):
                best_enjoyment = sum_enjoyment
                best_time = sum_time
                best_acts = list(combs)
                best_cost = sum(j["cost"] for j in combs)
    end = time.perf_counter()
    exec_time = end - start
    return best_acts, best_enjoyment, best_time, best_cost, exec_time



def dp_solver(activities, t):
    """
    Dynamic programming algorithm
    """
    def total_enjoyment(t, weights, enjoyment):
        n= len(weights)
        dp = [[0]*(t + 1) for _ in range(n + 1)]#creates the dynamic programming table

        for i in range (1, n+1):
            for c in range (0, t+1):
                w = weights[i-1]
                val = enjoyment[i-1]

                if w > c: # ignores activities that dont fit into the time constraint
                    dp[i][c] = dp[i-1][c]
                else:
                    dp[i][c] = max(dp[i-1][c],
                                   val + dp[i-1][c-w]
                                   )
        return dp [n][t], dp # returns the answer
    def selected_activities(t, weights, dp):
        """
        used to find the activities selected
        """
        n = len(weights)
        chosen = []
        i, c = n, t

        while i >  0 and c >= 0 :
            if dp[i][c] == dp[i-1][c]:
                i -= 1
            else:
                chosen.append(i-1)
                c -= weights[i-1]
                i -= 1

        chosen.reverse()
        return chosen
    def run_dp(activities, t):
        """
        runs dynamic programming algorithm
        """
        weights = [a ["time"] for a in activities]
        enjoyment = [a["enjoyment"] for a in activities]

        start = time.perf_counter()
        best, dp = total_enjoyment(t, weights, enjoyment)
        chosen_indices = selected_activities(t, weights, dp)
        chosen_acts = [activities[i] for i in chosen_indices]
        total_time = sum(j["time"] for j in chosen_acts)
        total_cost = sum(j["cost"] for j in chosen_acts)
        execution_time = time.perf_counter() - start

        return chosen_acts, best, total_time, total_cost, execution_time


    return run_dp(activities, t)



def print_results(input_file, selected_activities_bf, total_enjoyment_bf,
                 total_time_bf, total_cost_bf, max_time, max_budget, exec_time_bf,
                 selected_activities_dp, total_enjoyment_dp, total_time_dp,
                 total_cost_dp, exec_time_dp):
    """
    Print results in the required format.
    """
    print("========================================")
    print("EVENT PLANNER - RESULTS")
    print("========================================")
    print()
    print("Input File:", input_file)
    print("Available Time:", max_time)
    print("Available Budget:", max_budget)
    print()
    print("--- BRUTE FORCE ALGORITHM ---")
    print("Selected Activities:")
    for act in selected_activities_bf:
        name = act.get("name")
        t = act.get("time")
        c = act.get("cost")
        e = act.get("enjoyment")
        print(f"   - {name} ({t} hours, £{c}, enjoyment {e})")
    print()
    print("Total Enjoyment:", total_enjoyment_bf)
    print("Total Time Used:", total_time_bf, "hours")
    print(f"Total cost: £{total_cost_bf}")
    print()
    print("Execution Time:", round(exec_time_bf, 7), "seconds")
    print()
    print("--- DYNAMIC PROGRAMMING ALGORITHM ---")
    print("Selected Activities:")
    for act in selected_activities_dp:
        name = act.get("name")
        t = act.get("time")
        c = act.get("cost")
        e = act.get("enjoyment")
        print(f"   - {name} ({t} hours, £{c}, enjoyment {e})")
    print()
    print("Total Enjoyment:", total_enjoyment_dp)
    print("Total Time Used:", total_time_dp, "hours")
    print(f"Total cost: £{total_cost_dp}")
    print()
    print("Execution Time:", round(exec_time_dp, 7), "seconds")
    print()
    print("========================================")

def main():
    """
    Main function to run the event planner.
    """
    #take argument from terminal input
    input_file = sys.argv[1]
    #call read_input, brute_force_solver() and dp_solver()
    t, b, activities = read_input(input_file)
    best_acts_bf, best_enjoyment_bf, best_time_bf, best_cost_bf, exec_time_bf = brute_force_solver(activities, t)
    best_acts_dp, best_enjoyment_dp, best_time_dp, best_cost_dp, exec_time_dp = dp_solver(activities, t)
    print_results(input_file, best_acts_bf, best_enjoyment_bf, best_time_bf,
                  best_cost_bf, t, b, exec_time_bf, best_acts_dp, best_enjoyment_dp,
                  best_time_dp, best_cost_dp, exec_time_dp)

if __name__ == "__main__":
    main()
