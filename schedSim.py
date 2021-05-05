import sys
import queue

class schedSim:       

    # [job#, burst, arrival]
    def FIFO(self, jobTimes):
        time = 0
        responses = []
        waits = []
        turnarounds = []
        fp = open("testResult.out", "w+")
        # if first job doesnt arrive at time 0
        if jobTimes[0][2] != 0:
            time = jobTimes[0][2]
        for job in jobTimes:
            # start time of next job
            if time < job[2]:
                time = job[2]
            response = time - job[2] # get CPU - arrival
            responses.append(response)
            time += job[1] # add burst time to total time counter
            turnaround = float(time - job[2]) # exit time - arrival time
            turnarounds.append(turnaround)
            wait = float(turnaround - job[1]) # turnaround - burst
            waits.append(wait)
            fp.write("Job {0} -- Response: {1:.2f} Turnaround {2:.2f}  Wait {3:.2f}\n".format(job[0], response, turnaround, wait))
        fp.write("Average -- Response: {0:.2f} Turnaround {1:.2f}  Wait {2:.2f}\n".format((sum(responses))/(len(responses)), (sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))

    
    def RR(self, jobTimes, quantum):
        fp = open("testRRResult.out", "w+")
        waits = []
        turnarounds = []
        time = 0
        q = queue.Queue(999999999999)
        for job in jobTimes:
            job.append(job[1])
            q.put(job)
        while q.empty() == False:
            job = q.get()
            if (int(quantum) < job[1]):
                job[1] -= int(quantum)
                q.put(job)
                time += int(quantum)
            else:
                time += job[1]
                turnarounds.append(time - job[2])
                waits.append(time - job[2] - job[3])
                fp.write("Job  {0} -- Turnaround: {1:.2f}  Wait {2:.2f} \n".format(job[0], time - job[2], time - job[2]- job[3]))
        fp.write("Average -- Turnaround: {0:.2f}  Wait: {1:.2f}\n".format((sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))

    def SRJN(self, jobTimes):
        result = []
        responses = []
        waits = []
        turnarounds = []
        time = 0
        fp = open("testSRJNResult.out", "w+")
        # if first job doesnt arrive at time 0
        if jobTimes[0][2] != 0:
            time = jobTimes[0][2]
        job = jobTimes[0]
        res = []
        res.append(jobTimes[0][0])
        jobTimes.pop(0)
        responses.append(time - job[2])
        res.append(time - job[2])
        time += job[1]
        res.append(float(time - job[2]))
        turnarounds.append(float(time - job[2]))
        res.append(float(float(time - job[2]) - job[1]))
        waits.append(float(float(time - job[2]) - job[1]))
        result.append(res)
        while(len(jobTimes) > 0):
            res = []
            possibleJobs = [i for i in jobTimes if i[2] <= time]
            possibleJobs.sort(key = lambda x: x[1])
            job = possibleJobs[0]
            # start time of next job
            if time < job[2]:
                time = job[2]
            res.append(job[0])
            jobTimes.remove(job)
            if time < job[1]:
                time = job[1]
            res.append(time - job[2])
            responses.append(time - job[2])
            time += job[1]
            res.append(float(time - job[2]))
            turnarounds.append(float(time - job[2]))
            res.append(float(float(time - job[2]) - job[1]))
            waits.append(float(float(time - job[2]) - job[1]))
            result.append(res)
        result.sort(key = lambda x: x[0])
        for i in range(len(result)):
            fp.write("Job   {0} -- Response: {1:.2f}   Turnaround {2:.2f}  Wait {3:.2f}\n".format(result[i][0], result[i][1], result[i][2], result[i][3]))
        fp.write("Average -- Response: {0:.2f}  Turnaround {1:.2f}   Wait {2:.2f}\n".format((sum(responses))/(len(responses)), (sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))
        
    
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
