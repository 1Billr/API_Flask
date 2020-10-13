# API_Flask

Contains the api code for 1Billr data

**To edit the api:**

1. Edit the file billr.py with the appropriate code
2. Run command: '_sudo systemctl restart billr_' to rerun the code
3. Check the status: '_sudo systemctl status billr_' to check the status. The status should be _running_

**To edit the nginx configrations:**

1. Edit the configurations in file: _/etc/nginx/sites-available/billr_
2. Restart the server as: '_sudo systemctl restart nginx_'
3. Check the status as: '_sudo systemctl status nginx_'

### Run migration

- Postgres needs to be running locally on port 5432
- Do these steps to create tables

```
flask db init
flask db migrate
flask db upgrade
```
