# schedSim
# Name: Tyra Krivonak and Jillian Quinn

# Instructions: 
The MakeFile will create an executable that you can then run with the preferred arguments
make clean
make schedSim
./schedSim <input file> -p <algorithm> -q <quantum>
Inputs:
    Algorithm is an optional input and one of FIFO, SJRN, RR (Default is FIFO)
    quantum is an optional integer > 0
    input file is the .in file with the bust time and arrival time
example:
    ./schedSim test1.in -p SJRN
    ./schedSim test1.in -p FIFO
    ./schedSim test1.in -p RR -q 2
    ./schedSim test1.in -p RR

# Questions:
## For what types of workloads does SRTN deliver the same turnaround times as FIFO?
- If all the jobs arrive at the same time and are the same length or all the jobs arrive in the order of shortest to longest job, then they will have the same turnaround time.
## For what types of workloads and quantum lengths does SRTN deliver the same response times as RR?
- When the time quantum is 1 second (since jobs only arrive on integer, non-decimal times) and jobs arrive in order of increasing jobs size, then they will be scheduled in the same order and same Response time as SRTN. Also when the time quantum is larger than the longest job and the jobs arrive in order of increasing job size.
## What happens to response time with SRTN as job lengths increase? Can you use the simulator to demonstrate the trend?
- As job lengths increase, the response time will be much longer because each process will have to wait the length of the burst time of of the jobs before it before it has the chance to run. In the worse case, where jobs are sorted from smallest to largest burst time, then the response time will be the sum of the burst times of all the smaller jobs, since it will have to wait for the shorter jobs to finish first. 
## What happens to response time with RR as quantum lengths increase? Can you write an equation that gives the worst-case response time, given N jobs?
- As your quantum increases, the response time will increase as well because each job has to wait for all the other jobs before it to run their quantum before it gets its quantum time. An equation that models the worst case behavior, last job in the queue, is ResponseTime = (Quantum)*(N-1) 
