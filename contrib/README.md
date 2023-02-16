# Cluster prep

Once we get a cluster, we need to create accounts for all the attendees.

Standa is so awesome and wrote a script for that: `htpasswd_gen.sh`

Prepare a file structured as:
```
username password
username2 password2
... ...
test ...
... ...
```

Make sure `oc` speaks to the right cluster (!) and you're a cluster-admin.

Then just run:
```
$ htpasswd_gen.sh ht-source.txt
```

Once done, try the `test` login.
