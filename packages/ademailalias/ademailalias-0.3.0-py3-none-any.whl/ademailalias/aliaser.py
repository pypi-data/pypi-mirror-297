import json
import logging
import sys
from functools import lru_cache
from pathlib import Path

import requests
from appdirs import AppDirs

from ademailalias import CREDENTIALS, EMPTY_TOKENS_CONFIG, forge_url

APPDIRS = AppDirs("mail_aliases", "numeric-gmbh")
TOKENS_CONFPATH = Path(APPDIRS.user_config_dir) / "tokens.json"
ALIASES_CONFPATH = Path(APPDIRS.user_config_dir) / "aliases.json"


def generate_passwd(length=20):
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password


def check_config():
    NEW = False
    # =========================================================================
    # check if tokens config file exists
    # if i doesn't exist, create a dummy one to be filled
    # =========================================================================
    if not TOKENS_CONFPATH.exists():
        TOKENS_CONFPATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKENS_CONFPATH, "w") as fh:
            fh.write(json.dumps(EMPTY_TOKENS_CONFIG, indent=4))
        raise FileNotFoundError(f"{TOKENS_CONFPATH} has been created. Fill it please!")
    # -------------------------------------------------------------------------
    # if it exists, check that it is not filled with dummy stuff
    with open(TOKENS_CONFPATH) as fh:
        tokens = json.loads(fh.read())
        if "_changeme_" in tokens:
            raise ValueError(f"Please change default tokens file {TOKENS_CONFPATH}")
    # =========================================================================
    # check that aliases config file has relevant entries
    # =========================================================================
    if not ALIASES_CONFPATH.exists():
        ALIASES_CONFPATH.parent.mkdir(parents=True, exist_ok=True)
        ALIASES_CONFPATH.touch()
        default_data = {name: {} for name in tokens}
        with open(ALIASES_CONFPATH, "w") as fh:
            fh.write(json.dumps(default_data, indent=4))
    # -------------------------------------------------------------------------
    # create an empty section if the section does not exists
    with open(ALIASES_CONFPATH) as fh:
        aliases = json.loads(fh.read())
    has_changed = False
    for name in tokens:
        if name not in aliases:
            has_changed = True
            aliases[name] = {}
    if has_changed:
        with open(ALIASES_CONFPATH, "w") as fh:
            fh.write(json.dumps(aliases, indent=4))
    return tokens, aliases


class Aliaser:
    def __init__(self, name):
        tokens, aliases = check_config()
        self.redirect = tokens[name]["redirect"]
        self.store_passwd = tokens[name].get("store_passwd", False)
        self.name = name
        self.domain = tokens[name]["domain"]
        self._credentials = (f"{tokens[name]['token']} account={name}", "")
        self.aliases = aliases[name]
        self._domain_id = self.domains()[self.domain]

    def requests_get(self, what):
        url = forge_url(what=what)
        # Send HTTP request
        response = requests.get(url, auth=self._credentials)
        if response.ok is False:
            msg = f"{url}:: code{response.status_code}"
            logging.error(msg)
            raise ValueError(msg)
        return json.loads(response.content.decode())

    def requests_delete(self, what):
        url = forge_url(what=what)
        # Send HTTP request
        response = requests.delete(url, auth=self._credentials)
        if response.ok is False:
            return response
            msg = f"{url}:: code{response.status_code}"
            logging.error(msg)
            raise ValueError(msg)
        return

    @lru_cache
    def domains(self):
        domains = {}
        for domain in self.requests_get("domain"):
            name = domain.pop("name")
            domains[name] = domain["id"]
        return domains

    def list(self):
        return self.aliases.keys()

    def create(self, alias, redirect=None, annotation=False):
        if not redirect:
            redirect = self.redirect
        if not annotation:
            annotation = f"alias for '{redirect}'"
        # always prefix annotation to be able to find them from server
        annotation = "EmailAlias - " + annotation
        payload = {
            "name": alias,
            "domain": self._domain_id,
            "redirect_enabled": True,
            "redirect_to": redirect,
            "redirect_local_copy": False,
            "annotation": annotation,
            "password": generate_passwd(),
        }
        url = forge_url("mailbox")
        ret = requests.post(url, auth=self._credentials, data=json.dumps(payload))
        if ret.status_code == 201:
            # everything is OK,
            # save data
            configured_aliases = self.requests_get("mailbox")
            res = [m for m in configured_aliases if m["name"] == alias][0]
            if self.store_passwd:
                res["password"] = payload["password"]
            else:
                res.pop("password")
            self.aliases[alias] = res
            self.save()
        else:
            raise RuntimeError(ret.json())

    def delete(self, alias):
        cfg = self.aliases.get(alias)
        if not cfg:
            raise KeyError(
                f"{alias} does not exis. Existing = {sorted(self.aliases.keys())}"
            )
        url = forge_url(cfg["href"])
        ret = requests.delete(url, auth=self._credentials)
        if ret.status_code == 204:
            self.aliases[alias] = {}
            self.save()
        else:
            raise RuntimeError(ret.json())

    def save(self):
        with open(ALIASES_CONFPATH) as fh:
            all = json.loads(fh.read())
        previous = all[self.name]
        previous.update(self.aliases)
        # purge empty content
        self.aliases = {k: v for k, v in previous.items() if v}
        all[self.name] = self.aliases
        with open(ALIASES_CONFPATH, "w") as fh:
            fh.write(json.dumps(all, indent=4))
