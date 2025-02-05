class processHandeler:
    def __init__(self):
        self.process = []
    
    
    def add_process(self, process, *args, **kwargs):
        self.process.append([process, args, kwargs])
        
        if len(self.process) == 1:
            self.run_proccess()
    
    
    def run_proccess(self):
        process = self.process[0][0]
        args = self.process[0][1]
        kwargs = self.process[0][2]
        
        process(*args, **kwargs)
        
        self.process.pop(0)
        
        if len(self.process) > 0:
            self.run_proccess()