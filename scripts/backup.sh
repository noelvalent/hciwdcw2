#!/usr/bin/env bash

fileName=`date`.tar;
echo $fileName;

cp ./db.sqlite3 ./media/img/db.sqlite3;
tar -cf "./media/backup_cached/$fileName" ./media/img;
rm ./media/img/db.sqlite3;