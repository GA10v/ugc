#!/bin/bash

port=${PORT:-27017}

echo "Waiting for startup.."
until mongosh --host mongos1:${port} --eval 'quit(db.runCommand({serverStatus:1}).ok ? 0 : 2)' &>/dev/null; do
    printf '.'
    sleep 1
done

echo "Started.."

echo setup.sh time now: `date +"%T" `
mongosh --host mongocfg1:${port} <<EOF
var cfg = {
        "_id": "mongors1conf",
        "configsvr": true,
        "members": [
            {
                "_id": 0,
                "host": "mongocfg1:${port}"
            },
            {
                "_id": 1,
                "host": "mongocfg2:${port}"
            },
            {
                "_id": 2,
                "host": "mongocfg3:${port}"
            }
        ]
    };
    rs.initiate(cfg, { force: true });
EOF

mongosh --host mongors1n1:${port} <<EOF
var cfg = {
        "_id": "mongors1",
        "configsvr": true,
        "members": [
            {
                "_id": 0,
                "host": "mongors1n1:${port}"
            },
            {
                "_id": 1,
                "host": "mongors1n2:${port}"
            },
            {
                "_id": 2,
                "host": "mongors1n3:${port}"
            }
        ]
    };
    rs.initiate(cfg, { force: true });
EOF

mongosh --host mongos1:${port} <<EOF
var cfg = "mongors1/mongors1n1"
    sh.addShard(cfg, { force: true });
EOF


mongosh --host mongors2n1:${port} <<EOF
var cfg = {
        "_id": "mongors2",
        "configsvr": true,
        "members": [
            {
                "_id": 0,
                "host": "mongors2n1:${port}"
            },
            {
                "_id": 1,
                "host": "mongors2n2:${port}"
            },
            {
                "_id": 2,
                "host": "mongors2n3:${port}"
            }
        ]
    };
    rs.initiate(cfg, { force: true });
EOF

mongosh --host mongos1:${port} <<EOF
var cfg = "mongors2/mongors2n1"
    sh.addShard(cfg, { force: true });
EOF

mongosh --host mongors1n1:${port} <<EOF
"use ugc_db";
EOF


mongosh --host mongos1:${port} <<EOF
var cfg = "ugc_db"
    sh.enableSharding(cfg);
EOF

