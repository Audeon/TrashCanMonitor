print('Start #################################################################');

db = db.getSiblingDB('tcresults');
db.createUser(
    {
        user: 'tc_usr',
        pwd: 'trashcan',
        roles: [{ role: 'readWrite', db: 'tcresults' }],
    },
);
db.createCollection('trashcan_results');