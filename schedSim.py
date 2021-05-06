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
        fp = open("testResult.out", "w+")
        waits = []
        turnarounds = []
        time = 0
        result = []
        responses = []
        seen = 0
        q = queue.Queue(999999999999)
        
        for job in jobTimes:
            job.append(job[1])

        q.put(jobTimes[0])
        time = jobTimes[0][2]

        while q.empty() == False:
            job = q.get()
            if (job[0] == seen):
                seen += 1
                responses.append(time - job[2] + 1)
            if (int(quantum) < job[1]):
                job[1] -= int(quantum)
                for findjob in jobTimes:
                    if (job[0] == findjob[0]):
                        findjob[1] = job[1]
                time += int(quantum)
                for jobt in jobTimes:
                    if (jobt[0] > job[0]) & (jobt[1] > 0) & (jobt[2] <= time):
                        found = False
                        for el in list(q.queue):
                            if jobt[0] == el[0]:
                                found = True
                        if found == False:
                            q.put(jobt)
                q.put(job)
            else:
                time += job[1]
                turnarounds.append(time - job[2])
                waits.append(time - job[2] - job[3])
                job[1] = 0
                templist = []
                templist.append(job[0])
                templist.append(time - job[2])
                templist.append(time - job[2]- job[3])
                result.append(templist)
                for jobt in jobTimes:
                    if (jobt[0] > job[0]) & (jobt[1] > 0) & (jobt[2] <= time):
                        found = False
                        for el in list(q.queue):
                            if jobt[0] == el[0]:
                                found = True
                        if found == False:
                            q.put(jobt)
                
        result = sorted(result, key=lambda x : x[0])
        count = 0
        for item in result:
            item.append(responses[count])
            count += 1
            fp.write("Job  {0} -- Response: {1:.2f}  Turnaround: {2:.2f}  Wait: {3:.2f} \n".format(item[0], item[3], item[1], item[2]))

        fp.write("Average -- Response: {0:.2f}  Turnaround: {1:.2f}  Wait: {2:.2f}\n".format((sum(responses))/(len(responses)),(sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))

    def SRJN(self, jobTimes):
        result = []
        responses = []
        waits = []
        turnarounds = []
        time = 0
        fp = open("testResult.out", "w+")
        time = 0
        # job indexes are [job#, remaining burst, arrival, start, end, total burst]
        while(len(jobTimes) > 0):
            possibleJobs = [i for i in jobTimes if i[2] <= time and i[1] > 0]
            if len(possibleJobs) == 0:
                time += 1
                continue
            possibleJobs.sort(key = lambda x: x[1])
            job = possibleJobs[0]
            if (len(job) == 3):
                # keep track of start time 
                job.append(time)
                # create field for end time
                job.append(-1)
                # keep track of total burst time
                job.append(job[1]) 
            job[1] -= 1
            if job[1] == 0: 
                res = []
                # if job finishing, set end time, remove it from the array, calculate 
                job[4] = time
                jobTimes = [i for i in jobTimes if i[1] > 0]
                # job name
                res.append(job[0])
                res.append(job[3] - job[2]) # time to get CPU - arrival time
                responses.append(job[3] - job[2])
                res.append(float((time + 1) - job[2])) # exit time - arrival time
                turnarounds.append(float((time + 1) - job[2]))
                res.append(float(float((time + 1) - job[2]) - job[5]))
                waits.append(float(float((time + 1) - job[2]) - job[5])) # turnaround - burst
                result.append(res)
            time += 1
        result.sort(key = lambda x: x[0])
        for i in range(len(result)):
            fp.write("Job   {0} -- Response: {1:.2f}  Turnaround {2:.2f}  Wait {3:.2f}\n".format(result[i][0], result[i][1], result[i][2], result[i][3]))
        fp.write("Average -- Response: {0:.2f}  Turnaround {1:.2f}  Wait {2:.2f}\n".format((sum(responses))/(len(responses)), (sum(turnarounds))/(len(turnarounds)), (sum(waits))/(len(waits))))
        
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
        if len(sys.argv) > 2 and sys.argv[2] == "-p":
            algorithm = sys.argv[3]
        elif len(sys.argv) == 6 and sys.argv[4] == "-p":
            algorithm = sys.argv[5]
        # get quantum and call function
        if len(sys.argv) > 2 and sys.argv[2] == "-q":
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
