# NOYO API

## FILE DESCRIPTION:
```
•	noyo_run.py - Python code for Flask Application
•	requirements.txt - Packages to be installed in the Python Application Image
•	run.sh - To run the application and build the DB
```

## RUNNING THE APPLICATION:
```
• This application requires Python3
• cd /Noyo/
• ./run.sh

Now, once the application service is up and running, it can be tested using web interface by going to a local
browser and typing the URL “http:/localhost:5000/”.
It can also be tested through command line using curl -> curl http://localhost:5000/ (make sure your application is running)
```

## Testing
```
Basic unit testing pointers:
- Make sure your application is running in the terminal
-	Go to your local web browser and type URL http://localhost:5000/ or http://localhost:5000/noyo/.
Both the links will take you to the Task1 from the requirements document
- Enter the required details. (All the fields on the Task1 page are mandatory fields except the middle name field).
The userID field here is used as the DB primary key. If the entry with a specific userID already exists, it
will alert the user to  enter a unique userID and re-enter the required details
- The Task2 of the requirements doc can be run using the URL formatted as - http://localhost:5000/noyo/person/<str:userId>
This fetches the details of the person in the DB with specified userId. If userId does not exist, user will be alerted with an error message
- Task3 requires userID as well as the specific version of the person whose details need to be fetched,
using the URL formatted as - http://localhost:5000/noyo/person/<str:userId>/<int:version>. If userId does not exist or version's incorrect, user will be alerted with an error message
- Similarly Task4 fetches all the person details in the DB using URL formatted as - http://localhost:5000/noyo/all_persons
- Task5 retrieves the form to update the person details using the URL - http://localhost:5000/noyo/person/update
Enter the userId for the person who's details you wish to update followed by the details to be updated
- Task6 of the specification is to delete a person entry in the DB with the specified userID.
The method used here is "DELETE", and can be tested using Postman with DELETE request to url http://localhost:5000/noyo/person/<str:userId>. If userId does not exist, user will be alerted with an error message
```
```

Error Handlers in the code
	404(Page Not Found)
	405 (Method Not Allowed)
	500 (Internal Server Error)
```
