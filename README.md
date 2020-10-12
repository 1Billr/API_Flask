# API_Flask
Contains the api code for 1Billr data

**To edit the api:**
1. Edit the file billr.py with the appropriate code
2. Run command:  '*sudo systemctl restart billr*' to rerun the code
3. Check the status: '*sudo systemctl status billr*' to check the status. The status should be *running*

**To edit the nginx configrations:**
1. Edit the configurations in file: */etc/nginx/sites-available/billr*
2. Restart the server as: '*sudo systemctl restart nginx*'
3. Check the status as: '*sudo systemctl status nginx*'
