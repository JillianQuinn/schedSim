import sys

class schedSim:       

    def FIFO(self, jobTimes):
        time = 0
        responses = []
        waits = []
        turnarounds = []
        fp = open("testResult.out", "w+")
        for job in jobTimes:
            response = time 
            responses.append(response)
            wait = float(time - job[1])
            waits.append(wait)
            time += job[1] # add burst time to total time counter
            turnaround = float(time - job[2])
            turnarounds.append(turnaround)
            # fp.write("Job {0} -- Turnaround {1}  Wait {2}".format(job[0], turnaround, wait))
            fp.write("Job {0} -- Response: {1:.2f} Turnaround {2:.2f}  Wait {3:.2f}\n".format(job[0], response, turnaround, wait))
        fp.write("Average -- Response: {0:.2f} Turnaround {1:.2f}  Wait {2:.2f}\n".format((sum(responses))/(len(responses)), (sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))

    
    # def RR(self, jobTimes, quantum):

    def SRJN(self, jobTimes):
        result = []
        jobTimes.sort(key = lambda x: x[1])
        result.append(jobTimes[0])
        jobTimes.pop(0)
        jobTimes.sort(key = lambda x: x[2])
        print(jobTimes)
        print(result)
    
def main():
    ss = schedSim()
    try:
        quantum, algorithm = 1, "FIFO"
        # read file
        fp = open(sys.argv[1], "r")
        jobTimes = fp.readlines()
        fp.close()
        for i in range(len(jobTimes)):
            jobTimes[i] = list(map(int, (jobTimes[i].strip()).split(" ")))
        jobTimes.sort(key = lambda x: x[1])
        for i in range(len(jobTimes)):
            jobTimes[i] = [i] + jobTimes[i]
            
        # get algorithm
        if sys.argv[2] == "-p":
            algorithm = sys.argv[3]
        elif len(sys.argv) == 6 and sys.argv[4] == "-p":
            algorithm = sys.argv[5]
        # get quantum and call function
        if sys.argv[2] == "-q":
            quantum = sys.argv[3]
        elif len(sys.argv) == 6 and sys.argv[4] == "-q":
            quantum = sys.argv[5]
        if algorithm == "RR":
            ss.RR(jobTimes, quantum)
        elif algorithm == "SRJN":
            ss.SRJN(jobTimes)
        else:
            ss.FIFO(jobTimes)   
    except FileNotFoundError:
        print("File or command not found")
        return
    

if __name__ == "__main__":
    main()