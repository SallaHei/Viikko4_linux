# MariaDB Primary-Replica Replication

## Server A – Primary

- Hostname: vmbox
- Server ID: 1
- Binary logging is enabled.
- Binary log format: ROW.
- MariaDB listens on the private network address.

Configuration example: `server-a.cnf.example`

## Server B – Replica

- Hostname: vmbox-b
- Server ID: 2
- `read_only = ON`

Configuration example: `server-b.cnf.example`

## Replication direction

Replication runs from Server A to Server B.

Server A records database changes in its binary log. Server B receives and applies those changes to its local MariaDB database.

## Verification

The replica status was checked on Server B:

- `Slave_IO_Running: Yes`
- `Slave_SQL_Running: Yes`
- `Seconds_Behind_Master: 0`
- `Last_Errno: 0`
- `Last_Error`: empty

The application database user `week4_reader` has only SELECT privileges on the `viikko2` database.

The Week 4 application reads the local replica and does not modify the visitor counter.

These files are sanitized configuration examples for documentation. They do not contain passwords or replication credentials.
