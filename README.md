# movie_sheet_checker
A small project that will go through a list of movies on a shared google doc spreadsheet and check to see if and where the movies are being streamed. 

If you want to use this with your own spread sheet, replace the SHEET_ID and SHEET_NAME in update_sheet.py. You will need to setup credentials, to do this go to https://developers.google.com/sheets/api/guides/authorizing and acquire an api key.
Place the api key in your home directory (some work will be necessary to get this going on windows) and run the update_sheet.py.
You should be made to validate the credentials via a browser. After that the program should run normally and no longer need a log in.
To set this up periodically you should be able to just have update_schedule.py run as a cron job but you may find it easier to get
the provided scheduler.py script. Have the script execute automatically at login and everything should run in the background. 
