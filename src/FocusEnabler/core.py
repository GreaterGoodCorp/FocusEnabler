import ctypes
import io
import itertools
import json
import os
import pathlib
import re
import subprocess
import sys
import typing
import functools

import click

# Config data
config_filename: str = ".focusenabler"
config_dict: typing.Dict = dict()
config_exist: bool = False

# Path data
path_config: pathlib.Path
path_host: pathlib.Path

# Host data
is_host_accessible: bool

# OS data
os_name: str

# Make partial
style = functools.partial(click.style, bold=True, reset=True)

# base_stdout: Holds a copy of the original stdout
base_stdout = sys.stdout

# redirect: All output, if not to STDOUT, will go here.
redirect: io.StringIO = io.StringIO()


def disable_stdout():
    sys.stdout = redirect


def enable_stdout():
    sys.stdout = base_stdout


def is_domain_valid(domain):
    """Check if the domain contains valid syntax."""
    return True if re.match(
        r"^(([a-zA-Z])|([a-zA-Z][a-zA-Z])|([a-zA-Z][0-9])|([0-9][a-zA-Z])"
        r"|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$",
        domain
    ) else False


def initialise_config_dict():
    """Initialise a new config dictionary and write to file."""
    global config_dict
    config_dict = {
        "section_start": "# Added by FocusEnabler, do not modify!",
        "section_end": "# End of section FocusEnabler",
        "blacklisted_domains": [],
    }
    write_config_to_file()


def print_message(title, content, title_colour="white", content_colour="green", fp=None):
    """Print a formatted message."""
    if not fp:
        fp = sys.stdout
    click.echo(get_input_prompt(title, title_colour) + click.style(content, content_colour), file=fp)


def print_error(error):
    click.secho(error, sys.stderr, color="red")


def get_input_prompt(title, colour="white"):
    """Get prompt for input() function"""
    return click.style(f"- {title} \u2192 ", colour)


def decorate_domain_name(dm):
    """Decorate the domain name to stand out."""
    return f"{click.style(dm, 'yellow', underline=True)}"


def initialise_win32():
    """Initialise app on Windows."""
    global path_config, path_host
    path_config = pathlib.Path(os.getenv("APPDATA"), config_filename)
    path_host = pathlib.Path(os.getenv("WINDIR"), "System32", "drivers", "etc", "hosts")


def initialise_linux():
    """Initialise app on Linux."""
    global path_config, path_host
    path_config = pathlib.Path(pathlib.Path.home(), config_filename)
    path_host = pathlib.Path("/etc", "hosts")


def initialise_darwin():
    """Initialise app on MacOS."""
    initialise_linux()


def load_config():
    """Load config from file."""
    global config_dict, config_exist
    if pathlib.Path.is_file(path_config):
        with open(path_config) as fp:
            config_dict = json.load(fp)
            config_exist = True
            print_message("Checking if a config file is already exists", f"Found at {path_config}")
    else:
        config_dict = dict()
        config_exist = False
        print_message("Checking if a config file is already exists", "Not found", content_colour="red")
    initialise_config_non_exist()


def initialise_app():
    """Initialise app on startup."""
    global os_name
    # Check for OS-dependent initialisation
    if sys.platform == "win32":
        os_name = "Windows"
        initialise_win32()
    elif sys.platform == "darwin":
        os_name = "MacOS"
        initialise_darwin()
    else:
        os_name = "Linux"
        initialise_linux()
    print_message("Checking operating system", os_name)
    # Attempt to load config
    load_config()
    # Check host file accessibility
    check_host_accessibility()


def check_host_accessibility():
    """Check if host file is accessible."""
    global is_host_accessible
    if os.access(path_host, os.W_OK | os.R_OK):
        print_message("Checking if host file is accessible", "Yes")
        is_host_accessible = True
    else:
        print_message("Checking if host file is accessible", "No", content_colour="red")
        is_host_accessible = False


def enforce_accessible_host():
    """Make sure the host file is accessible."""
    if not is_host_accessible:
        print_error("Host file is inaccessible!")
        exit(1)


def initialise_config_non_exist():
    """Create a default config if no config is found."""
    if not config_exist:
        initialise_config_dict()
        print_message("Config file does not exist! Creating default config", "Done")


def enforce_privileged_access():
    """Make sure the app is run with privileged access."""
    try:
        if os.getuid() != 0:
            print_error("WARNING: Please run this command as 'root'")
            exit(1)
    except AttributeError:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print_error("WARNING: Please run this command as an administrator")
            exit(1)


def enforce_non_privileged_access():
    """Make sure the app is not run with privileged access."""
    try:
        if os.getuid() == 0:
            print_error("WARNING: Please do not run this command as 'root'")
            exit(1)
    except AttributeError:
        if ctypes.windll.shell32.IsUserAnAdmin():
            print_error("WARNING: Please do not run this command as an administrator")
            exit(1)


def flush_dns_darwin():
    """Flush DNS on MacOS."""
    subprocess.Popen(["sudo", "killall", "-HUP", "mDNSResponder"])
    subprocess.Popen(["sudo", "dscacheutil", "-flushcache"])


def flush_dns_linux():
    """Flush DNS on Linux."""
    subprocess.Popen(["sudo", "/etc/init.d/nscd", "restart"])
    subprocess.Popen(["sudo", "/etc/init.d/dnsmasq", "restart"])
    subprocess.Popen(["sudo", "/etc/init.d/named", "restart"])


def flush_dns_win32():
    """Flush DNS on Windows."""
    subprocess.Popen(["ipconfig", "/flushdns"])


def flush_dns():
    """Flush DNS cache on machine."""
    if sys.platform == "win32":
        flush_dns_win32()
    elif sys.platform == "darwin":
        flush_dns_darwin()
    else:
        flush_dns_linux()


def write_config_to_file():
    """Write config dict to file as JSON."""
    try:
        with open(path_config, "w+") as fp:
            json.dump(config_dict, fp)
        print_message("Writing to config file", "OK")
    except OSError:
        print_message("Writing to config file", "Failed", content_colour="red", fp=sys.stderr)
        exit(1)


def add_domain_internal(domains):
    """(Internal) Add domain to config."""
    c: int = 0
    for dm, c in zip(domains, itertools.count()):
        if is_domain_valid(dm):
            if dm not in config_dict["blacklisted_domains"]:
                config_dict["blacklisted_domains"].append(dm)
                print_message(f"Blacklisting {decorate_domain_name(dm)}", "Done")
            else:
                print_message(f"Blacklisting {decorate_domain_name(dm)}", "Already blacklisted")
        else:
            print_message(f"Blacklisting {decorate_domain_name(dm)}", "Invalid", content_colour="red")
    return c


def remove_domain_internal(confirm, domains, fp):
    """(Internal) Remove domain from config."""
    if domains == (".",):
        if len(config_dict["blacklisted_domains"]) == 0:
            click.echo("No blacklisted domains found", color="bright_white")
            exit(0)
        domains = config_dict["blacklisted_domains"]
    for dm in domains:
        if dm in config_dict["blacklisted_domains"]:
            option = None
            while confirm and option not in ("y", "n"):
                option = input(get_input_prompt(f"Un-blacklist '{decorate_domain_name(dm)}'? [Y/N]"))
            if option == "n":
                continue
            config_dict["blacklisted_domains"].remove(dm)
            print_message(f"Un-blacklisting {decorate_domain_name(dm)}", "Done", fp=fp)
        else:
            print_message(f"Un-blacklisting {decorate_domain_name(dm)}",
                          "Not found", content_colour="red", fp=fp)


@click.group("FocusEnabler")
def app_root():
    """FocusEnabler is a program that enables your focus by blocking websites."""
    pass


@app_root.command("add")
@click.option("-c", "--clear", is_flag=True, help="(Optionally) Remove all blacklisted domains (same as 'remove')")
@click.option("-d", "--disable-verbose", help="Disable echoing messages.", is_flag=True)
@click.argument("domains", nargs=-1, required=True)
def add_domain(clear, domains, disable_verbose):
    """Add DOMAINS to blacklist."""
    if disable_verbose:
        disable_stdout()
    initialise_app()
    enforce_non_privileged_access()
    if clear:
        remove_domain_internal(False, ".", redirect)
    add_domain_internal(domains)
    write_config_to_file()
    exit(0)


@app_root.command("list")
@click.option("-d", "--disable-verbose", help="Disable echoing messages.", is_flag=True)
def list_domain(disable_verbose):
    """List blacklisted domains"""
    if disable_verbose:
        disable_stdout()
    initialise_app()
    enforce_non_privileged_access()
    if len(config_dict["blacklisted_domains"]) == 0:
        click.echo("No blacklisted domains found", color="bright_white")
        exit(0)
    click.echo("All blacklisted domains:", color="blue", file=base_stdout)
    for domain, count in zip(config_dict["blacklisted_domains"], itertools.count()):
        click.echo(f"({count + 1}) {domain}", color="cyan", file=base_stdout)


@app_root.command("remove")
@click.option("-c", "--confirm", is_flag=True, help="Ask before removing each domain")
@click.option("-d", "--disable-verbose", help="Disable echoing messages.", is_flag=True)
@click.argument("domains", nargs=-1, required=True)
def remove_domain(confirm, domains, disable_verbose):
    """Remove DOMAINS from blacklist"""
    if disable_verbose:
        disable_stdout()
    initialise_app()
    enforce_non_privileged_access()
    remove_domain_internal(confirm, domains, sys.stdout)
    write_config_to_file()


@app_root.command("activate")
@click.option("-d", "--disable-verbose", help="Disable echoing messages.", is_flag=True)
def activate_app(disable_verbose):
    """Activate FocusEnabler."""
    if disable_verbose:
        disable_stdout()
    initialise_app()
    enforce_privileged_access()
    enforce_accessible_host()
    with open(path_host) as fp:
        if config_dict["section_start"] in fp.read():
            print_error("FocusEnabler is already activated! Deactivate first.")
            exit(1)
    entries: typing.List[str] = [config_dict["section_start"]]
    for domain in config_dict["blacklisted_domains"]:
        print_message(f"Adding entry {decorate_domain_name(domain)}", "Done")
        entries.append(f"127.0.0.1   {domain}")
        entries.append(f"127.0.0.1   www.{domain}")
    entries.append(config_dict["section_end"])
    try:
        with open(path_host, "a") as fp:
            fp.write("\n".join(entries))
        print_message("Writing to host file", "Done")
        flush_dns()
        click.echo("FocusEnabler is enabled!", color="cyan")
        exit(0)
    except OSError:
        print_message("Writing to host file", "Failed", content_colour="red", fp=sys.stderr)
        exit(1)


@app_root.command("deactivate")
@click.option("-d", "--disable-verbose", help="Disable echoing messages.", is_flag=True)
def deactivate_app(disable_verbose):
    """Deactivate FocusEnabler"""
    if disable_verbose:
        disable_stdout()
    initialise_app()
    enforce_privileged_access()
    enforce_accessible_host()
    content = None
    try:
        with open(path_host) as fp:
            content = fp.read()
            original_content_len = len(content)
        print_message("Reading host file", "Done")
        content = re.sub(rf"{config_dict['section_start']}(.|[\n\r\t])*{config_dict['section_end']}", "", content)
        if len(content) == original_content_len:
            print_error("FocusEnabler is not activated! Activate first")
            exit(1)
        else:
            print_message("Deactivating FocusEnabler", "Done")
    except OSError:
        print_message("Reading host file", "Failed", content_colour="red", fp=sys.stderr)
        exit(1)
    try:
        with open(path_host, "w") as fp:
            fp.write(content)
        print_message("Writing to host file", "Done")
        click.echo("FocusEnabler is disabled!", color="cyan")
    except OSError:
        print_message("Writing to host file", "Failed", content_colour="red", fp=sys.stderr)


def run_core():
    """Acts as the entry point to run this app."""
    app_root()


if __name__ == '__main__':
    run_core()
