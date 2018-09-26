# Timesheet automation

I forbid to use software from this repository for evil purposes!
I do not take, claim and/or give any responsibility for its use.
This repository does not exists anywhere else but in your imagination.
Stop reading. Wake up.

## Installation

Exec
```
# ./install.sh <user>
```
as root that installs all libraries and requirements. ```<user>``` is non-root account under which browser can be opened without admin privileges

Setup your OTP as described [here](./otp.md).

In ```conf/properties.properties``` set every property value containing ```<TODO>``` other TODOs ignore.

## Configure

Currently used configuration properties:
```
USE_WEEK_DAY_PREFIX=True
WEEK_DAY_<1-5>_START
WEEK_DAY_<1-5>_COMMENT
APPEND_TILL_TODAY
APPEND_ONLY_ONE
```


## Notest

For testing use ```export PROPERTIES_FILE_NAME=properties-test.properties``` and ```conf/properties-test.properties``` will be used.


### Encoding

Waiting for text to (diss)appear at page is using conversion iso-8859-2 -> UTF-8 in ui_utils.py file ```text=text.encode("iso-8859-2").decode("UTF-8")```

### Files

If you cannot find screenshots try change property ```FIREFOX_DOWNLOAD_DIR``` to absolute path.

### TODO

- Comment randomization?
- Using regex to match rows by values (date?)
