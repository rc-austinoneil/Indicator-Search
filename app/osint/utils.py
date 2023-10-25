import re
import ipaddress


def remove_duplicate_keys(dictionary):
    unique_dict = {}
    for key, value in dictionary.items():
        if key not in unique_dict:
            unique_dict[key] = value
    return unique_dict


def refang(indicator):
    if "[.]" in indicator:
        indicator = indicator.replace("[.]", ".")
    return indicator


def get_type(indicator):
    """
    This function checks the indicator to see if it is an IP address, hash, URL,
    email address, SSL fingerprint, MAC address, or FQDN.
    """
    try:
        getVer = ipaddress.ip_address(indicator)
        if getVer.version == 4:
            return "ipv4"
        elif getVer.version == 6:
            return "ipv6"
    except ValueError:
        pass

    # MD5
    if re.match("^[a-f0-9]{32}$", indicator, re.I):
        return "hash.md5"
    # SHA-1
    elif re.match("^[a-f0-9]{40}$", indicator, re.I):
        return "hash.sha1"
    # SHA-256
    elif re.match("^[a-f0-9]{64}$", indicator, re.I):
        return "hash.sha256"
    # SHA-512
    elif re.match("^[a-f0-9]{128}$", indicator, re.I):
        return "hash.sha512"
    # URL
    elif re.match("^https?://", indicator, re.I):
        return "url"
    # Email Addresses
    elif re.match("^.*?@.*?$", indicator, re.I):
        return "email"
    # Mac Addresses
    elif re.match(
        "^([0-9a-fA-F][0-9a-fA-F][-:\.]){5}([0-9a-fA-F][0-9a-fA-F])$", indicator, re.I
    ):
        return "mac"
    # FQDN
    elif re.match(
        "(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)",
        indicator,
        re.I,
    ):
        return "fqdn"
    # Phone number
    elif re.match("^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$",
        indicator,
        re.I,
    ):
        return "phone"
    return None


def no_results_found(tool_name):
    return (
        {
            "site": tool_name,
            "results": {"error": "No results found"},
        },
    )


def failed_to_run(tool_name, error):
    return (
        {
            "site": tool_name,
            "results": {"error": f"{tool_name} failed to run: {str(error)}"},
        },
    )


def status_code_error(tool_name, status_code, reason):
    return (
        {
            "site": tool_name,
            "results": {"error": f"{tool_name} failed to run: {status_code} {reason}"},
        },
    )


def get_feedlist_type(indicator):
    if indicator.indicator_type in ["ipv4", "ipv6"]:
        return "ip"
    elif indicator.indicator_type in [
        "hash.md5",
        "hash.sha1",
        "hash.sha256",
        "hash.sha512",
    ]:
        return "hash"
    elif indicator.indicator_type in ["fqdn", "url"]:
        return "fqdn"
    else:
        return None


def remove_ip_address(string):
    ip_address_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3} \b"
    if re.search(ip_address_pattern, string):
        string = string.split(" ")[1]
        string = string.strip()
    return string


def convert_email_to_fqdn(email):
    return email.split("@")[1]


def convert_fqdn_to_url(fqdn):
    if fqdn.startswith("http://") or fqdn.startswith("https://"):
        return fqdn
    else:
        return "https://" + fqdn


def convert_url_to_fqdn(url):
    domain_match = re.search(
        r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)",
        url,
    )
    if domain_match:
        return domain_match.group(1)
    else:
        raise Exception("Invalid URL")
