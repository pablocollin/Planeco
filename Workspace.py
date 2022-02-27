from Employee import Employee
from itertools import cycle

DAYLIST = [0,1,2,3,4]
DAYNAMELIST = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

class Workspace:
    num_workspaces=0

    def __init__(self, name, capacity, employees, gauge=100):
        self.name = name
        self.dailyLimit = int(capacity*gauge/100) #Limit of people who can work at workspace per day (COVID regulation)
        self.employees = employees #List of Employee objects
        self.officeSchedule = [[],[],[],[],[]] #2D list (days --> employees)
        self.homeSchedule = [[],[],[],[],[]]

        self.id = Workspace.num_workspaces
        Workspace.num_workspaces+=1
    
    def distribNeededWorkers(self):
        """
        Distributes the workers that must be at work at least once per week in the schedule.
        """

        dayCycle = cycle(DAYLIST)

        needcounter = {}
        for employee in self.employees:
            if employee.needDays > 0:
                needcounter[employee]=employee.needDays
        while sum(needcounter.values())>self.dailyLimit*5:
            emps_sorted = sorted(needcounter, key=needcounter.get, reverse=True) # list employee decreasing order
            emp = emps_sorted[0] # emp = employee with most needDays
            emp.needDays-=1 # 
            needcounter[emp]-=1 
        
        for employee in self.employees:
            count = -1
            while employee.needDays > 0:
                dayIndex = next(dayCycle)
                count += 1
                if count > 9:
                    employee.needDays -= 1
                if count > 4:
                    if (employee not in self.officeSchedule[dayIndex]) and (len(self.officeSchedule[dayIndex]) < self.dailyLimit):
                        self.officeSchedule[dayIndex].append(employee)
                        employee.numDays+=1
                        employee.needDays-=1
                if employee.willing[dayIndex] == 1 and count <= 4:
                    if (employee not in self.officeSchedule[dayIndex]) and (len(self.officeSchedule[dayIndex]) < self.dailyLimit):
                        self.officeSchedule[dayIndex].append(employee)
                        employee.numDays+=1
                        employee.needDays-=1




    def createSchedule(self):
        self.distribNeededWorkers()

        for day in range (5):
            potentialEmployees = {}
            for employee in self.employees:

                if employee in self.officeSchedule[day]:
                    continue

                elif employee.willing[day] == 0:
                    self.homeSchedule[day].append(employee)
                    continue

                else:
                    potentialEmployees[employee] = employee.presenceIndex()

            for employee in sorted(potentialEmployees, key=potentialEmployees.get, reverse=True):
                if (employee not in self.officeSchedule[day]) and (len(self.officeSchedule[day]) < self.dailyLimit):
                    self.officeSchedule[day].append(employee)
                    employee.numDays+=1
                elif employee not in self.homeSchedule[day]:
                    self.homeSchedule[day].append(employee)
        
    
    def printSchedule(self):

        print("OFFICE SCHEDULE:")

        for day in range(5):
            print("__________________________________________")
            print(DAYNAMELIST[day], ":")

            for employee in self.officeSchedule[day]:
                print("-", employee.name, employee.surname)
            
            print("__________________________________________")

        print("")

        print("HOME SCHEDULE:")

        for day in range(5):
            print("__________________________________________")
            print(DAYNAMELIST[day], ":")

            for employee in self.homeSchedule[day]:
                print("-", employee.name, employee.surname)
            
            print("__________________________________________")
    

    def getScheduleFormat(self):
        self.createSchedule()

        schedule=[[],[],[],[],[]]
        for day in range(5):
            for employee in self.officeSchedule[day]: 
                schedule[day].append(employee.name+" "+employee.surname)

        scheduleRev=[]

        return schedule

            
    def getEmployees(self):
        employeeList=[]
        for employee in self.employees:
            employeeList.append(employee.name+" "+employee.surname)
        return ', '.join(employeeList)
