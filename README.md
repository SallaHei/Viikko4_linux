# Weekly Assignment 4 – Server Cloning, Backups and Database Replication

## Project overview

This project uses two Ubuntu servers.

- Server A: vmbox – MariaDB primary server and Week 2 Flask application.
- Server B: vmbox-b – MariaDB replica server and Week 4 Flask application.

## Application URLs

- Server A – Week 2:
  http://193.166.24.7/viikko2/

- Server B – Week 4:
  http://86.50.252.36/viikko4/

## Server B creation

Server B is a separate Ubuntu virtual machine.
It runs Nginx, MariaDB, Python, Flask and Gunicorn.

## Database replication

Server A acts as the MariaDB primary server.
Server B acts as the replica server.

Week 4 reads the visitor counter from the local MariaDB database on Server B.

The application uses the dedicated database user `week4_reader`.
The user has SELECT privileges.

Server B has MariaDB read_only enabled.

Week 4 only reads the visitor counter and does not increment it.

## Website backups

Server A backs up `/var/www/html/` to Server B.

Backup destination:

`/var/backups/viikko2/`

The transfer uses rsync over SSH.

The backup script runs every hour using cron:

`0 * * * * /home/ubuntu/bin/backup-html-to-b.sh`

Backup logs are stored on Server A:

`/home/ubuntu/backup-logs/backup.log`

Backups use timestamped directories.

## Backup permissions

The backup directory on Server B is owned by ubuntu.

Directory permissions are 700.

SSH authentication uses a dedicated key.

## Backup tests

The following tests have succeeded:

- Manual backup transfer.
- Seven automatic hourly backup runs.
- Timestamped backup directories created on Server B.
- Test file restored to a separate directory.
- SHA-256 checksums of the original and restored file matched.

## Replication and read-only testing

The Week 4 application displays the replicated visitor counter from Server B's local database.

The application uses SELECT and does not modify the counter.

## GitHub

Repository:

https://github.com/SallaHei/Viikko4_linux

Passwords, private SSH keys and database dumps are excluded from the repository.

## Remaining verification

- Verify replication status again.
- Verify both public application URLs.
- Perform a reboot test on Server B.
- Verify website, replication and cron operation after reboot.
