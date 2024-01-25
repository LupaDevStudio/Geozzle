# Compilation instructions

## Debug

### Compilation of a debug version

`python -m buildozer -v android debug`

### Launch the debug version on a device connected to the computer

`python -m buildozer -v android deploy run logcat | grep python`

## Release

### Creation of the app signing key

```bash
keytool -genkey -v -keystore ~/keystores/Geozzle.keystore -alias Geozzle -keyalg RSA -keysize 2048 -validity 10000
keytool -importkeystore -srckeystore ~/keystores/Geozzle.keystore -destkeystore ~/keystores/Geozzle.keystore -deststoretype pkcs12
```

### Compilation of a release version

```bash
export P4A_RELEASE_KEYALIAS="Geozzle"
export P4A_RELEASE_KEYSTORE=~/keystores/Geozzle.keystore
export P4A_RELEASE_KEYSTORE_PASSWD=
export P4A_RELEASE_KEYALIAS_PASSWD=
python -m buildozer android release
```

## Bug fix

### Java Heap Space error

`export GRADLE_OPTS="-Xms1724m -Xmx5048m -Dorg.gradle.jvmargs='-Xms1724m -Xmx5048m'"`