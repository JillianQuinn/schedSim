
all: schedSim
examples: test1FIFOresult.out test1RR1result.out test1RR3result.out test1SRJNresult.out test2FIFOresult.out test2RR1result.out test2RR3result.out test2SRJNresult.out

test1: schedSim
	python3 schedSim test1.in -p SRJN
	python3 schedSim test1.in -p RR -q 1
	python3 schedSim test1.in -p SRJN
	python3 schedSim test1.in -p SRJN

test2: schedSim 
	python3 schedSim test2.in -p SRJN
	python3 schedSim test2.in -p RR -q 1
	python3 schedSim test2.in -p SRJN
	python3 schedSim test2.in -p SRJN

clean:
	-rm schedSim test1FIFOresult.out test1RR1result.out test1RR3result.out test1SRJNresult.out test2FIFOresult.out test2RR1result.out test2RR3result.out test2SRJNresult.out
	

