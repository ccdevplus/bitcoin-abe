Worldcoin-Abe: a free block chain browser for the Worldcoin currency.
https://github.com/alferz/worldcoin-abe

    Copyright(C) 2011,2012,2013 by Abe developers.
    License: GNU Affero General Public License, see the file LICENSE.txt.
    Portions Copyright (c) 2010 Gavin Andresen, see bct-LICENSE.txt.

Welcome to Abe!
===============

This software reads the Worldcoin block file, transforms and loads the
data into a database, and presents a web interface.

The original Abe software draws inspiration from Bitcoin Block Explorer (BBE) and
BlockChain.info and seeks some level of compatibility with them but
uses a completely new implementation. 

Worldcoin-Abe forks the original Abe project to simplify matters a bit by displaying
just one coin: Worldcoin. This version removes the ability to display multiple coins
or even multiple chains for the same coin for simplicity (there is no /chains screen).

Installation - Worldcoin
------------

Install and configure Postgres - see README-POSTGRES.txt.

Install and run the Linux Worldcoin Daemon 
from https://github.com/worldcoinproject/worldcoin-v0.8/

Start Worldcoin Daemon and wait until it has fully downloaded the 
Block Chain

Modify abe.conf to point to your .worldcoin directory and either
modify the logfile line to specify a log file, or comment out 
the logfile line to log to console only.
    
    "dirname":"/path/to/.worldcoin",
    logfile = "/path/to/abe.log"

Issue:

    sudo python setup.py install

This will install ABE to your system.

Modify the abe-load.sh script to point to abe.conf in the directory
where you downloaded worldcoin-abe:

    --config=/path/to/abe.conf

To perform the initial blockchain load into the Postgres database, 
run the abe-load.sh script. It is recommended to run this command 
in a "screen" because the load will take a long time (12-24 Hours).
During the load process you should see log messages either in the 
log file or on screen:

    block_tx 1 1
    block_tx 2 2
    ...

Once loaded, the Postgres database is now synced up with the Worldcoin client.

Now, configure Apache to use fast-cgi as described in README-FASTCGI.txt

You should have a working WDC Explorer running on Port 80. It is also 
recommended to run the server on port 443 with a valid HTTPS cert
to ensure privacy of users. Enforce HTTPS redirect with in your apache site conf:

        RewriteEngine On
        RewriteCond %{REQUEST_URI} !static
        RewriteCond %{REQUEST_URI} !q
        RewriteCond %{SERVER_PORT} !^443$
        RewriteRule ^ https://www.wdcexplorer.com%{REQUEST_URI} [L,R=301]

To ensure the Postgres DB stays up to date, run abe-load.sh every time a new 
block is found by adding this line to your worldcoin.conf file, then 
restart the WDC Daemon:

    blocknotify=/path/to/abe/abe-load.sh

Congratulations, now you have a working WDC Explorer!


Additional Installation Notes from the bitcoin-abe Developers:
------------

Abe depends on Python 2.7 (or 2.6), the pycrypto package, and an SQL
database supporting ROLLBACK.  Abe runs on PostgreSQL, MySQL's InnoDB
engine, and SQLite.  Other SQL databases may work with minor changes.
Abe formerly ran on some ODBC configurations, Oracle, and IBM DB2, but
we have not tested to be sure it still works.  See the comments in
abe.conf about dbtype for configuration examples.

Abe works with files created by the original (Satoshi) Bitcoin client.
You will need a copy of the block files (blk0001.dat, blk0002.dat,
etc. in your Bitcoin directory or its blocks/ subdirectory).  You may
let Abe read the block files while Bitcoin runs, assuming Bitcoin only
appends to the file.  Prior to Bitcoin v0.8, this assumption seemed
safe.  Abe may need some fixes to avoid skipping blocks while current
and future Bitcoin versions run.

NovaCoin and CryptoCash support depends on the ltc_scrypt module
available from https://github.com/CryptoManiac/bitcoin-abe (see
README-SCRYPT.txt).

Hirocoin (and any other X11) support depends on the xcoin_hash module
available from https://github.com/evan82/xcoin-hash.

Bitleu (a Scrypt-Jane coin) depends on the yac_scrypt module.

Copperlark (a Keccak coin) depends on the sha3 module available via
"easy_install pysha3".

License
-------

The GNU Affero General Public License (LICENSE.txt) requires whoever
modifies this code and runs it on a server to make the modified code
available to users of the server.  You may do this by forking the
Github project (if you received this code from Github.com), keeping
your modifications in the new project, and linking to it in the page
template.  Or you may wish to satisfy the requirement by simply
passing "--auto-agpl" to "python -m Abe.abe".  This option makes all
files in the directory containing abe.py and its subdirectories
available to clients.  See the comments in abe.conf for more
information.

Database
--------

For usage, run "python -m Abe.abe --help" and see the comments in
abe.conf.

You will have to specify a database driver and connection arguments
(dbtype and connect-args in abe.conf).  The dbtype is the name of a
Python module that supports your database.  Known to work are psycopg2
(for PostgreSQL) and sqlite3.  The value of connect-args depends on
your database configuration; consult the module's documentation of the
connect() method.

You may specify connect-args in any of the following forms:

* omit connect-args to call connect() with no arguments

* named arguments as a JSON object, e.g.:
  connect-args = { "database": "abe", "password": "b1tc0!n" }

* positional arguments as a JSON array, e.g.:
  connect-args = ["abe", "abe", "b1tc0!n"]

* a single string argument on one line, e.g.:
  connect-args = /var/lib/abe/abe.sqlite

For JSON syntax, see http://www.json.org.

Slow startup
------------

Reading the block files takes much too long, several days or more for
the main BTC block chain as of 2013.  However, if you use a persistent
database, Abe remembers where it stopped reading and starts more
quickly the second time.

Replacing the Block File
------------------------

Abe does not currently handle block file changes gracefully.  If you
replace your copy of the block chain, you must rebuild Abe's database
or (quicker) force a rescan.  To force a rescan of all data
directories, run Abe once with the "--rescan" option.

Web server
----------

By default, Abe expects to be run in a FastCGI environment.  For an
overview of FastCGI setup, see README-FASTCGI.txt.

To run the built-in HTTP server instead of FastCGI, specify a TCP port
and network interface in abe.conf, e.g.:

    port 2750
    host 127.0.0.1  # or a domain name

Input
-----

To display Namecoin, NovaCoin, or any block chain with data somewhere
other than the default Bitcoin directory, specify "datadir" in
abe.conf, e.g.:

    datadir = /home/bitcoin/.namecoin

The datadir directive can include a new chain's basic configuration,
e.g.:

    datadir += [{
            "dirname": "/home/weeds/testnet",
            "chain":   "Weeds",
            "code3":   "WDS",
            "address_version": "o" }]

Note that "+=" adds to the existing datadir configuration, while "="
replaces it.  For help with address_version, please open doc/FAQ.html
in a web browser.

The web interface is currently unaware of name transactions, but see
namecoin_dump.py in the tools directory.

More information
----------------

Please see TODO.txt for a list of what is not yet implemented but
would like to be.

Forum thread: https://bitcointalk.org/index.php?topic=22785.0
Newbies: https://bitcointalk.org/index.php?topic=51139.0

Donations appreciated: 1PWC7PNHL1SgvZaN7xEtygenKjWobWsCuf (BTC)
NJ3MSELK1cWnqUa6xhF2wUYAnz3RSrWXcK (NMC)
