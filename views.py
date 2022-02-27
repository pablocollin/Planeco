from flask import Flask
from flask import render_template, request, redirect, url_for, g
import csv
from io import TextIOWrapper
from Employee import Employee
from Workspace import Workspace
from Company import Company

app = Flask(__name__)

DAYINDEX = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4}
COMPANY = Company([])

def formatWillingList(willingExplicit):
    willingFormat=[0,0,0,0,0]
    for day in willingExplicit:
        willingFormat[DAYINDEX[day]]=1
        
    return willingFormat

def formatWorkspaces():
    workspacesFormat=[]
    for workspace in COMPANY.workspaces:
        workspacesFormat.append((workspace.id, workspace.name, workspace.dailyLimit, workspace.getEmployees()))
    return workspacesFormat

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route('/workspace', methods=['POST', 'GET'])
def workspace():
    results = request.form

    if results:
        name = results["name"]


        capacity = int(results["capacity"])

        gauge = float(results["amountInput"])

        tmpWorkspace = Workspace(name, capacity, [], gauge)

        COMPANY.workspaces.append(tmpWorkspace)
        
        workspaces = formatWorkspaces()

        return render_template("workspace.html", workspaces = workspaces)
    
    workspaces = formatWorkspaces()
    
    return render_template("workspace.html", workspaces = workspaces)


@app.route('/employee/<id>', methods=['POST', 'GET'])
def employee(id):
    results = request.form
    if results and request.method=="POST":

        workspaceID = int(id)

        name = results["name"]

        surname = results["surname"]

        time = int(results["time"])-1

        sustainability = int(results["sustainability"])-1

        needDays = int(results["needDays"])

        willingDaysExplicit = results.getlist("willingDay")
        willingFormat = formatWillingList(willingDaysExplicit)

        for workspace in COMPANY.workspaces:
            if workspace.id == workspaceID:
                workspace.employees.append(Employee(name, surname, time, sustainability, needDays, willingFormat))
                break

        return render_template("employee.html", workspaceID=id)

    return render_template("employee.html", workspaceID=id)


@app.route('/upload/<id>', methods=['POST'])
def upload_route_summary(id):
    if request.method == 'POST':
        
        workspaceID = int(id)

        f = request.files['fileupload']  

        fstring = f.read().decode('UTF-8')

        listRows=fstring.split()

        if len(listRows) >0:
            listKeys = listRows[0].split(";")

            listRows = listRows[1:]

            csv_dicts=[]

            for row in listRows:
                tmpListRow = row.split(";")
                tmpRowDict = {}
                for i in range(len(listKeys)):
                    tmpRowDict[listKeys[i]]=tmpListRow[i]
                csv_dicts.append(tmpRowDict)

            for employee in csv_dicts:
                name = employee["name"]
                surname = employee["lastName"]
                time = int(employee["time"])-1
                sustainability = int(employee["sustainability"])-1
                needDays = int(employee["needDays"])
                willingFormat = [int(employee["willMo"]), int(employee["willTu"]), int(employee["willWe"]), int(employee["willTh"]), int(employee["willFr"])]
                for workspace in COMPANY.workspaces:
                    if workspace.id == workspaceID:
                        workspace.employees.append(Employee(name, surname, time, sustainability, needDays, willingFormat))
        
        workspaces = formatWorkspaces()
        
        return render_template("workspace.html", workspaces = workspaces)


@app.route('/schedule/<id>', methods=['POST'])
def schedule(id):

    scheduleFormat = []
 
    workspaceID = int(id)

    for workspace in COMPANY.workspaces:
        if workspace.id == workspaceID:
            scheduleFormat = workspace.getScheduleFormat()
            break
    
                
    return render_template("schedule.html", schedule=scheduleFormat, workspaceID=workspaceID)


@app.route('/schedulePerso/<id>', methods=['POST'])
def schedulePerso(id):

    workspaceID = int(id)

    persoSchedule = []

    results=request.form

    if results:
        isInWorkspace=False
        name = results["name"]
        surname = results["lastName"]
        workspaceName=""
        for workspace in COMPANY.workspaces:
            if workspace.id == workspaceID:
                scheduleFormat = workspace.getScheduleFormat()
                workspaceName=workspace.name
                for employee in workspace.employees:
                    if name+" "+surname == employee.name+" "+employee.surname:
                        isInWorkspace=True
                        break
                break
        
        if not isInWorkspace:
            return render_template("schedulePerso.html", persoSchedule=[], fullIntro=name+" "+surname+" not found in "+workspaceName)

        
        persoSchedule = ["Remote","Remote","Remote","Remote","Remote"]

        for i in range(len(scheduleFormat)):
            for employee in scheduleFormat[i]:
                if (employee == name+" "+surname):
                    persoSchedule[i]=workspaceName
                
    return render_template("schedulePerso.html", persoSchedule=persoSchedule, fullIntro=name+" "+surname+"'s schedule")

app.run(debug=True)