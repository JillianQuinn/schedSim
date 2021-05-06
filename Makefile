schedSim: schedSim.py
	@touch schedSim
	@echo '#!/bin/sh\npython schedSim.py' "\$$@" > ./schedSim
	@chmod u+x schedSim

clean:
	rm schedSim testResult.out
