sh -c "cat /docker-entrypoint-initdb.d/user_events.csv | clickhouse-client --query=\"INSERT INTO default.user_events FORMAT CSVWithNames\";"
