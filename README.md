# Bitbucket Utility

## Basic Usage

List repos:

```
bitbucket.py list my-workspace --username user123 --password secretpassword
```

Clone all repos:

```
bitbucket.py clone my-workspace --username user123 --password secretpassword
```

Clone all repos within within a project:

```
bitbucket.py clone my-workspace --username user123 --password secretpassword --project-key myproject
```

## Limitations

Supports list and clone operations up to 100 repos