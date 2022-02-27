class Employee:
    num_employees=0

    def __init__(self, name, surname, time, sustainability, needDays, willing):

        self.name = name #string
        self.surname = surname

        self.id = Employee.num_employees # int
        Employee.num_employees += 1

        self.time = time # int 0-5
        self.sustainability = sustainability # int 0-2
        self.needDays = needDays # int 0-5
        self.willing = willing # list - length 5 (ex. [0,1,1,0,1])
        self.numDays = 0 # int
    

    def addDay(self):
        self.numDays += 1
        
    
    def presenceIndex(self):
        pIndex = -1

        if self.sustainability == 0:
            pIndex = 1
        elif self.sustainability == 1:
            pIndex = 0.7
        else:
            pIndex = 0.3

        pIndex -= self.time * 0.1

        pIndex -= self.numDays * 0.15

        return pIndex


    
    
        
            

        
        
        
    
    