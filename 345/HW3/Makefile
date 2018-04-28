.PHONY: task_0
task_0:
	@echo "Task 0a output:" > report
	gcc -o 0afork 0afork.c
	time ./0afork >> report
	@echo >> report
	@echo "Task 0b output:" >> report
	gcc -o 0bwait 0bwait.c
	time ./0bwait >> report

.PHONY: task_1
task_1:
	@echo >> report
	@echo "Task 1a output:" >> report
	gcc -o 1asum 1asum.c
	time ./1asum >> report
	@echo >> report
	@echo "Task 1b output:" >> report
	gcc -o 1bsum 1bsum.c
	time ./1bsum >> report

.PHONY: task_2
task_2:
	@echo >> report
	@echo "Task 2a output:" >> report
	gcc -o 2asum 2asum.c -pthread
	time ./2asum >> report
	@echo >> report
	@echo "Task 2b output:" >> report
	gcc -o 2bsum 2bsum.c -pthread
	time ./2bsum >> report
	@echo >> report
	@echo "Task 2c output:" >> report
	gcc -o 2csum 2csum.c -pthread
	time ./2csum >> report

.PHONY: deliverable_1
deliverable_1:
	@echo >> report
	@echo "Deliverable 1a output:" >> report
	gcc -o d1afork d1afork.c
	./d1afork >> report
	@echo >> report
	@echo "Deliverable 1b output:" >> report
	gcc -o d1bfork d1bvfork.c
	./d1bfork >> report
	@echo >> report
	@cat d1c >> report
	@echo >> report

.PHONY: deliverable_2
deliverable_2:
	@echo >> report
	@echo "Deliverable 2 output:" >> report
	gcc -o d2 d2.c -pthread
	./d2 >> report

.PHONY: homework
homework: task_0 task_1 task_2 deliverable_1 deliverable_2