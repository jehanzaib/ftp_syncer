# ftp_syncer #

ftp_syncer keeps your local directory synced with remote directory via FTP. Based on watchdog, a Python library to monitor filesystem events, ftp_syncer maps the resulting events such as on_created {directory} with FTP.mkd() {directory}.

## Why ftp_syncer? ##

At times many shared hosting services (like HostGator, BlueHost) doesn't allow ssh into shared hosting instances. In that case, only options left are either FileZilla or other FTP specific code deployment tools.

ftp_syncer leverages the existing FTP capabilities and doesn't require you to manually deploy your codebase whenever there's a change in it. Just keep writing or deleting the code and see the resulting changes on server.

## Can I use it in production environment? ##

You should never use it in production environment. ftp_syncer should only be used within dev environment and that too with great caution.

## How it works ##

1. Install watchdog and ftplib modules.
2. Save your FTP credentials in config.yaml

```
python syncer.py -c config.yaml -s YOUR_SERVER_DIR -l YOUR_LOCAL_DIR
```

## Script Help ##

Execute with --help parameter to get help on all available options.

```
python syncer.py --help
```

## Notes ##

Contact me at [@_jehanzaib_][mjb] or <mjb@iknowl.net> for any feedback/suggestions.

[mjb]:   https://twitter.com/_jehanzaib_
