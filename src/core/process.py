process = []


def add_process(new_process, *args, **kwargs):
    process.append([new_process, args, kwargs])
    
    if len(process) == 1:
        run_proccess(process)

def run_proccess(new_process):
    current_process = new_process[0][0]
    args = new_process[0][1]
    kwargs = new_process[0][2]

    current_process(*args, **kwargs)

    process.pop(0)

    if len(process) > 0:
        run_proccess(process)