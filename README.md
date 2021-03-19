# Focus Enabler

Focus Enabler is a Python program that deals with focusing issues while using computer, by blocking unneeded websites.

## Installation

### Prerequisites

Python (`python3.6` and above) with `pip` installed.

### Via `pip`

For most end-users, this package can be installed by running:

```bash
pip3 install FocusEnabler
```

> Notes:
> 
> * Make sure `pip3` is up-to-date by running `python3 -m pip --install pip`.
> 
> * For Windows, use `python` instead of `python3`, and `pip` instead of `pip3`.

### Via source

The latest source code for this program can be found on [GitHub]. The program can then be built from source by running:

```bash
git clone https://github.com/GreaterGoodCorp/FocusEnabler
cd FocusEnabler
make build      # or 'make dev-install' to install developmental version
```

## Usage

Once installed, the program can be invoked by running `focus`. Sample usage is as follows:

### Blacklist certain websites

In order to blacklist certain domain names, use `focus add <DOMAINS>`, where `<DOMAINS>` is a list of domain names to
blacklist, separated by blank space.

Available options:

* `-c` (`--clear`): Remove all blacklisted domains before adding new one (same as `focus remove .`)

* `-d` (`--disable-verbose`): Disable echoing info-messages to console. This option does not block warning or error
   messages

For example, to blacklist `youtube.com` and `facebook.com`, run the following:

```bash
$ focus add youtube.com facebook.com
```

The output is as follows:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at ~/.focusenabler
- Checking if host file is accessible → No
- Blacklisting facebook.com → Done
- Blacklisting youtube.com → Already blacklisted
- Writing to config file → OK
```

> Notes:
> 
> * The domain will be ignored if its syntax is invalid.
> 
> * Do not run this command as `root` (or Administrator, for Windows). An error will occur when attempting to do so.
> 
> * `FocusEnabler` will remember any blacklisted domain names, even after rebooting.
>
> * On the first run, `FocusEnabler` will create a default config file.

### Un-blacklist blacklisted websites

Likewise, to remove (un-blacklist) any domain names, use `focus remove <DOMAINS>`, where `<DOMAINS>` is a list of domain
names to un-blacklist, separated by blank space.

Available options:

* `-c` (`--confirm`): Ask before removing each domain.

* `-d` (`--disable-verbose`): Disable echoing info-messages to console. This option does not block warning or error
   messages.

For example, to un-blacklist `youtube.com` and `facebook.com`, run the following:

```bash
$ focus remove youtube.com facebook.com
```

The output should look like this:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at ~/.focusenabler
- Checking if host file is accessible → No
- Un-blacklisting youtube.com → Done
- Un-blacklisting facebook.com → Done
- Writing to config file → OK
```

> Notes:
> 
> * The domain will be ignored if it is not blacklisted already.
> 
> * Do not run this command as `root` (or Administrator, for Windows). An error will occur when attempting to do so.

### List blacklisted websites

To check for all blacklisted domains, run `focus list`.

Available options:

* `-d` (`--disable-verbose`): Disable echoing info-messages to console. This option does not block warning or error
   messages.

The output should look like this:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at ~/.focusenabler
- Checking if host file is accessible → No
All blacklisted domains:
(1) instagram.com
```

> Notes:
> 
> * Do not run this command as `root` (or Administrator, for Windows). An error will occur when attempting to do so.
> 
> * If `--disable-verbose` is set, this function will still list all blacklisted domains, minus the extra system
>   information.

### Activate FocusEnabler

To activate FocusEnabler, i.e. to start blocking blacklisted domains, run `sudo focus activate` (on Windows, open
`Command Prompt` as administrator and run `focus activate` instead).

Available options:

* `-d` (`--disable-verbose`): Disable echoing info-messages to console. This option does not block warning or error
   messages.

The output should look like this:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at /Users/m1k3/.focusenabler
- Checking if host file is accessible → Yes
- Adding entry instagram.com → Done
- Writing to host file → Done
FocusEnabler is enabled!
```

> Notes:
> 
> * `sudo` (or Administrator on Windows) is required as this program needs to write to the system' hosts file.

### Activate FocusEnabler

Likewise, to deactivate FocusEnabler, run `sudo focus deactivate` (on Windows, open `Command Prompt` as administrator
and run `focus deactivate` instead).

Available options:

* `-d` (`--disable-verbose`): Disable echoing info-messages to console. This option does not block warning or error
   messages.

The output should look like this:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at /Users/m1k3/.focusenabler
- Checking if host file is accessible → Yes
- Reading host file → Done
- Deactivating FocusEnabler → Done
- Writing to host file → Done
FocusEnabler is disabled!
```

> Notes:
> 
> * Like `focus activate`, `sudo` (or Administrator on Windows) is required as this program needs to write to the 
> system' hosts file.

## Changelog

### Version 1.0.0 - 1.2.0

Initial release. No changelog available

### Version 1.3.0

1. New features:

   * Added an option to all commands to disable echoing info-messages to console.
   
2. Internal changes

   * Optimised code flow
   
   * Remove unnecessary code guard

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This program is licensed under the
[MIT License](https://github.com/GreaterGoodCorp/FocusEnabler/blob/main/LICENSE).

[GitHub]: https://github.com/GreaterGoodCorp/FocusEnabler
