## OpenvCloud Portals Functional Tests

Currently only the **End User Portal** is covered.

```
sudo apt install python-nose
```

```
nosetests -v end_user --tc-file=config.ini  2>testresults.log
```