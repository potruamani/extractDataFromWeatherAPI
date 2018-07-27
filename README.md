# extractDataFromWeatherAPI

Steps to Run the Script:
  1. clone the extractDataFromAPI from repo
  2. install mongodb in your local syatem from https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
  3. start the server and client (follow the link in step 2)
  4. create a test db using (use test) in client command prompt
  4. make sure weather.py and config.py at same folder/directory
  5. install all the requirements from the requirements.txt using (pip install -r requirements.txt)
  6. run weather.py
 Output:
   1. check the collections in the mongodb
       you will see like five_day_forecast and weather_maps
   2. check if the data is inserted
   3. you will see one new folder named weather_maps created where the weather.py file is present and all the downloaded maps in it
   4. you will be prompting a new window showing weather maps for the Clouds in every city  from config file
   
 UserAccess:
    1. change the cities or other options according to your requirement in the config file
   
  TODO:
    1. use graph API to display forecast/previous 10 day data from database as a graph (prebuilt libraries are there to do this)
  
  OtherOptions:
    1. remove comments at 114, 115, 116 lines and call same function in the try block to retrieve data from mongodb
  
  Queries:
     1. every one are welcomed to commit any queries.
