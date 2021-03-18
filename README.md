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

For example, to blacklist `youtube.com` and `facebook.com`, run the following:

```bash
$ focus add youtube.com facebook.com
```

The output is as follows:

```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at /Users/m1k3/.focusenabler
- Checking if host file is accessible → No
- Blacklisting facebook.com → Done
- Blacklisting youtube.com → Already blacklisted
- Writing to config file → OK
```

> Notes:
> 
> * The domain will be ignored if its syntax is invalid.
> 
> * `FocusEnabler` will remember any blacklisted domain names, even after rebooting.
>
> * On the first run, `FocusEnabler` will create a default config file.

### Un-blacklist blacklisted websites

Likewise, to remove (un-blacklist) any domain names, use `focus remove <DOMAINS>`, where `<DOMAINS>` is a list of domain
names to un-blacklist, separated by blank space.

For example, to un-blacklist `youtube.com` and `facebook.com`, run the following:

```bash
$ focus remove youtube.com facebook.com
```

The output should look like this:
```
- Checking operating system → MacOS
- Checking if a config file is already exists → Found at /Users/m1k3/.focusenabler
- Checking if host file is accessible → No
- Un-blacklisting youtube.com → Done
- Un-blacklisting facebook.com → Done
- Writing to config file → OK
```

> Notes:
> * The domain will be ignored if it is not blacklisted already.
> 
> * 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

[GitHub]: https://github.com/GreaterGoodCorp/FocusEnabler
