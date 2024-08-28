## Setting up the testdata

In order to develop the validators, some test-data has been setup.  
These are some layers containing basic geometry in ESPG:28992. These should only be used for development and testing purposes, since the actual data will be in EPSG:3035.

Before importing the test-data, make sure the PostGIS-extension and PgCrypto-extension are enabled.
To do so, run the following commands on the corresponding database:
```sql
CREATE EXTENSION "postgis";
CREATE EXTENSION "pgcrypto";
```

After enabling these extensions, the database-dump _testdata.backup_ can be imported.

This can be done in PgAdmin4 by following these steps:
- Open the Object Explorer
- Right-click on the database where the test-data should be imported and choose 'Restore...'
- For the option 'Filename' browse to and select the file _testdata.backup_
- To start the restore, click the 'Restore' button
