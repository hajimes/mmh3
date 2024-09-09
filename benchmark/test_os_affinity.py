# from https://www.geeksforgeeks.org/python-os-sched_setaffinity-method/
# Python program to explain os.sched_setaffinity() method

# importing os module
import os

# Get the number of CPUs
# in the system
# using os.cpu_count() method
print("Number of CPUs:", os.cpu_count())

# Get the set of CPUs
# on which the calling process
# is eligible to run. using
# os.sched_getaffinity() method
# 0 as PID represents the
# calling process
pid = 0
affinity = os.sched_getaffinity(pid)

# Print the result
print("Process is eligible to run on:", affinity)


# Change the CPU affinity mask
# of the calling process
# using os.sched_setaffinity() method

# Below CPU affinity mask will
# restrict a process to only
# these 2 CPUs (0, 1) i.e process can
# run on these CPUs only
affinity_mask = {0, 1}
pid = 0
os.sched_setaffinity(0, affinity_mask)
print("CPU affinity mask is modified for process id % s" % pid)


# Now again, Get the set of CPUs
# on which the calling process
# is eligible to run.
pid = 0
affinity = os.sched_getaffinity(pid)

# Print the result
print("Now, process is eligible to run on:", affinity)
