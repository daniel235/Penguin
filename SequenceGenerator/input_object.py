#object to fill in with specified files and data.  Eventually will be passed into 
#the machine learning models. 

class InputObject():
    def __init__(self, path):
        self.fastPath = path
        self.sam_file = None
        self.basecall_file = None
        self.event_file = None

    #getters
    def get_path(self):
        return self.fastPath


    def get_sam(self):
        return self.sam_file


    def get_basecall(self):
        return self.basecall_file


    def get_event(self):
        return self.event_file


    #setters
    def set_path(self, directoryName):
        this.fastPath = directoryName


    def set_sam(self, fileName):
        this.sam_file = fileName


    def set_basecall(self, fileName):
        this.basecall_file = fileName

    
    def set_event(self, fileName):
        this.event_file = fileName
