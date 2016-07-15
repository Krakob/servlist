#!/usr/bin/env python3

import psutil
from tabulate import tabulate
from termcolor import colored

# Processes to look for.
TARGETS = {
    'tmux':         'Tmux',
    'vivaldi.exe':  'Vivaldi'
}

# Running/not running text for targetted processes.
MESSAGES = {
    'on': colored('Running', 'green'),
    'off': colored('Not running', 'red')
}

QUERIES = (
    psutil.Process.username,
)

allproc = list(psutil.process_iter())

# Get all processes in TARGETS; append their nickname for readability
processes = []
for p in allproc:
    try:
        if p.name() in TARGETS:
            processes.append(p)
            p.nickname = TARGETS[p.name()]
    except psutil.NoSuchProcess:
        pass

# print(processes)
# Build a table for tabulate to print.
out_table = []
for p in processes:
    process_list = []
    process_list.append(p.nickname)

    for query in QUERIES:
        process_list.append(query(p))

    process_list.append(MESSAGES['on'])

    out_table.append(process_list)

# Add processes that aren't running.
for q in TARGETS:
    # Check if the target's nickname is not in the first column of out_table
    if TARGETS[q] not in [p[0] for p in out_table]:
        out_table.append([TARGETS[q], '', MESSAGES['off']])


print(
    tabulate(
        sorted(
            out_table, key=lambda p: p[0]
        ),
        headers=('Program', 'User', 'Status')
    )
)
