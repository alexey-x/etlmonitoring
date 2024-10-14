# How to use t_etlmonitoring.py

## Purpose

The script is used to check results before deployment.

## Usage
-1. Stop current proceess if working

```
$ ./bin/run.sh stop
```

0. Import new control object in t_etlmonitoring.py if needed

1. Start it with the command:

```
$ python tests/e2e/t_etlmonitoring.py
```

2. Insert proper test rows to the proper tables.

3. Check email for proper events notification.

4. to test file monitoring
    - open another terminal
    - cd /mo/gbc_mo/
    - ./mo_public_sas_trigger.sh
    - check email
    - remove created file(s) for a case /mo/acrm/mo_triggers/MO_SUCCESS_(check today's date)
## Clean Up

Remove inserted test rows from the proper tables.

## TODO

Swith from test MS SQL database to SQLite.
