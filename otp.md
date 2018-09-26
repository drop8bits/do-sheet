# How to automate generating OTP token

Install oathtool
```
dnf -y install oathtool
```

1. Using TOTP generate token (use random seed a check using Google authenticator) and save result secret somewhere safe,
2. set its pin to your choice,
3. enable token if not already enabled by default(?),
4. generate code
```
oathtool --base32 <secret>
```
5. synchronize token in your TOTP provider UI

### Notes
If your machine has messed up time try use oathtool with ```
--now=`date "+%Y-%m-%d %H:%M:%S" -d '4 hour ago'`
``` or similar
