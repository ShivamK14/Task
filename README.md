Interview task


Step 1:- Start Backend Django server:
	-Clone the repository using git clone https://github.com/ShivamK14/Task
	-The backend folder contains Django Rest api
	-Install the required python packages using  =                pip install -r requirements.txt
	-After installing requirements run           =                python manage.py makemigrations
	-The database used is simple db.sqlite which 
	 is the default database django provides,make sure to migrate
	 the migrations this will create the tables rquired    =      python manage.py migrate
	- you are all set to run the backend server  run using =      python manage.py runserver
	- make sure the default port is :8000 or the frontend 
	  will not be getting the response
	  
	  
Step 2:- Start the Frontend React server:
	-The Frontend/front folder includes the react js project  
	-fitst run the command to install all the dependencied required =  npm install
	-Then run this comand to start the Front server                 =  npm start
	-You are all set to use the webapp , locate the url in browser  =  http://localhost:3000
 
Step 3:- Using the app:
	-First select the jpg file you want to detect the object      
	-Also select thr xml which contains the image information  
	-select the "Detect object" button ,this will disply the processed image
	-For generating the csv report select the date range from date picker,
	and click the "Generate" button, after clicking download the csv report will be downloaded
	
	
Step 4:- Using Docker-compose:
	-Get to the root directory where "docker-compose.yml" is present
	-use command to create the docker images, this will create 
	 the docker images of both front end as well as backend        =  docker-compose build
	-finally use this command to deploy backend as well as         =  docker-compose up
	 front server
	

