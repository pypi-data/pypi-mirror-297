.. :changelog:

History
-------

0.0.1 (12-04-2019)
---------------------

* First code creation


0.0.11 (28-05-2019)
-------------------

* removal of .json on set_maintenance_policy


0.0.12 (28-05-2019)
-------------------

* added functions


0.0.13 (28-05-2019)
-------------------

* maintenance policies - list functions - are now teambased


0.0.14 (28-05-2019)
-------------------

* added function: count_alerts_by_query


0.0.15 (10-06-2019)
-------------------

* 'added functionality: adding more than 1 policy to a set_maintenance_policy'


0.0.16 (10-06-2019)
-------------------

* refactoring


0.0.17 (11-06-2019)
-------------------

* 2nd try on adding multiple arguments for set_maintenance_policy


0.0.18 (09-08-2019)
-------------------

* function names with more explicit names + reusing url endpoints to make the code more dry


0.0.19 (09-08-2019)
-------------------

* Adding the functionality to enable and disable alert/notification policies


0.0.20 (16-08-2019)
-------------------

* cancel_maintenance_policy now supports multiple ID's


0.0.21 (17-08-2019)
-------------------

* Allowing the input of multiple ID's for delete_maintenance_policy


0.0.22 (18-08-2019)
-------------------

* Adding multiple arguments for: disable/enable/delete notification- & alert policy


0.0.23 (20-08-2019)
-------------------

* Small fixes regarding the loops in multiple functions


0.0.24 (07-09-2019)
-------------------

* Added the function: list_schedule_timeline_by_team_name


0.0.25 (02-10-2019)
-------------------

* Adding users endpoint and the function list users


0.0.26 (03-10-2019)
-------------------

* Added function close_alerts


0.0.27 (09-10-2019)
-------------------

* Removed the team-id from list_maintenance_policy and renamed the function name


0.0.28 (11-10-2019)
-------------------

* Added pagination for query_alerts


0.0.29 (29-11-2019)
-------------------

* Class name changed from OpsGenie to Opsgenie and the functions with maintenance_policy were renamed to maintenance so removing the policy part.


0.0.30 (04-01-2020)
-------------------

* Added function create_alert_policy


0.0.31 (19-06-2020)
-------------------

* Adding more parameters to the function: list_schedule_timeline_by_team_name


0.0.32 (23-06-2020)
-------------------

* Return empty array when response.json()['data'] is empty


0.0.33 (26-06-2020)
-------------------

* Better way of limiting results of query_alerts to 2000 results maximum


0.0.34 (29-06-2020)
-------------------

* added limit param to the query_alerts method


0.0.35 (12-10-2020)
-------------------

* Cleaning up


0.0.36 (21-03-2023)
-------------------

* Using the existing dataclasses more in the output for teams



0.0.37 (22-03-2023)
-------------------

* Created Alert policy class and modified the other functions to use that class


0.0.38 (22-03-2023)
-------------------

* Added functions: get_alert_policy_by_name & set_maintenance_hours_by_name


0.0.39 (02-04-2023)
-------------------

* Modeling MaintenancePolicy


0.0.40 (09-04-2023)
-------------------

* Returning maintenancepolicy object instead of json and finding a alert policy is now case insensitive


0.0.41 (09-04-2023)
-------------------

* fixing a bug in cancel_maintenance


0.0.42 (15-08-2023)
-------------------

* Adding: heartbeat, team, user profile/notification functions


0.0.43 (15-11-2023)
-------------------

* AlertPolicy filter was not parsed correctly

0.0.44 (21-03-2024)
-------------------

* Feature: Add ability to filter maintenance policies based on start and end date

0.0.47 (23-09-2024)
-------------------

* Chore: Teams class didn't get the same data provided