# Weekly Assignment 4 – Server Cloning, Backups and Database Replication

## Project overview

This project uses two Ubuntu servers.

- Server A (`vmbox`): MariaDB primary server and Week 2 Flask application.
- Server B (`vmbox-b`): MariaDB replica server and Week 4 Flask application.

Server B was created as a separate virtual machine based on Server A's environment.

## Application URLs

- Server A – Week 2: http://193.166.24.7/viikko2/
- Server B – Week 4: http://86.50.252.36/viikko4/

## Server B software and application

Server B runs:

- Ubuntu
- Nginx
- MariaDB
- Python and Flask
- Gunicorn

The Week 4 application is located in `/home/ubuntu/week4/` and is managed by the `week4` systemd service.

The application reads the visitor counter from Server B's local MariaDB database.

## Storage layout

### Server A

- Website files: `/var/www/html/`
- Backup script: `/home/ubuntu/bin/backup-html-to-b.sh`
- Backup log: `/home/ubuntu/backup-logs/backup.log`
- SSH key: `/home/ubuntu/.ssh/id_ed25519_vmbox_b`

### Server B

- Backup destination: `/var/backups/viikko2/`
- Backup directories use timestamped names, for example `backup-YYYYMMDD-HHMMSS`.
- Week 4 application: `/home/ubuntu/week4/`

## Website backups

Server A backs up `/var/www/html/` to Server B using rsync over SSH.

The hourly cron schedule on Server A is:

`0 * * * * /home/ubuntu/bin/backup-html-to-b.sh`

Backup logs are stored on Server A:

`/home/ubuntu/backup-logs/backup.log`

Each backup is stored in a separate timestamped directory on Server B.

## Backup permissions and security

- The backup directory on Server B is owned by `ubuntu`.
- The backup directory permissions are `700`.
- SSH authentication uses a dedicated key.
- Passwords and private SSH keys are not stored in this repository.
- Database dumps and backup data are not stored in this repository.

## Backup tests

The following tests succeeded:

- Manual rsync backup transfer.
- Seven automatic hourly backup runs.
- Timestamped backup directories were created on Server B.
- A test file was restored to a separate directory.
- The original and restored file had matching SHA-256 checksums.

The matching checksum confirmed that the restored test file was identical to the original.

## MariaDB replication

Server A acts as the MariaDB primary server and Server B as the replica.

The Week 4 application reads the replicated `viikko2` database from Server B's local MariaDB server.

The replication status was checked on Server B:

- `Slave_IO_Running: Yes`
- `Slave_SQL_Running: Yes`
- `Seconds_Behind_Master: 0`
- `Last_Errno: 0`
- `Last_Error`: empty

The replication threads were running and the reported replication delay was zero.

## Read-only database access

MariaDB on Server B has `read_only` enabled.

The Week 4 application uses the dedicated database user `week4_reader`.

The verified database grant is:

`GRANT SELECT ON viikko2.* TO week4_reader@localhost`

The application only executes a SELECT query to read the visitor counter. It does not increment or modify the counter.

## Reboot testing

The server reboot tests were completed.

After reboot, Nginx, MariaDB and the Python application were checked.

The replication status was also verified, and the replica was running without reported errors.

## GitHub

Repository:

https://github.com/SallaHei/Viikko4_linux

The repository contains the Week 4 application and project documentation.

Passwords, private SSH keys and database dumps are excluded from the repository.

## What I learned

This assignment provided practical experience with:

- Creating a second server based on an existing server environment.
- Automating backups with cron, rsync and SSH.
- Keeping timestamped backup versions.
- Restoring files and verifying them with SHA-256 checksums.
- Configuring MariaDB primary-replica replication.
- Using a dedicated read-only database user.
- Checking services and replication after a server reboot.

Database replication keeps the replica updated, while timestamped backups provide separate recovery points.

The assignment required a considerable amount of time, troubleshooting and repeated corrections before everything worked as expected. I learned that configuring servers, backups and database replication involves several details that must work together. Testing and fixing problems step by step was an important part of completing the assignment.
