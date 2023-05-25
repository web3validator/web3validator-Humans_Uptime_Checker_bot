import subprocess
import logging
import toml
import requests
import json
import asyncio


def create_dict():
    data = {
        "message_id": '',
        "validators": {},
        "rpc": {},
    }

    return data


async def terminal(cmd: str | list = None, password: str = "None"):
    try:
        if type(cmd) != type(list()):
            cmd = cmd.split()
        p1 = subprocess.Popen(["echo", password], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=p1.stdout)
        output = p2.communicate()
        p1.stdout.close()
        p2.stdout.close()
        return output
    except Exception as error:
        logging.error("error Terminal\n", error)


async def get_validators(url: str) -> list:
    config = toml.load("config.toml")
    bin = config["path_bin"]

    validators = await terminal(f"{bin} q staking validators --node {url} --limit 1000 -o json")
    output = validators[0].decode('utf-8')
    error = validators[1].decode('utf-8')

    if output != '':
        output = json.loads(output)
        output = output["validators"]

    elif error != '':
        pass

    return output


async def check_url() -> dict:

    config = toml.load("config.toml")

    urls = config["rpc"]

    data = {"active_urls": [], "numer_active": 0, "urls": 0}

    for url in urls:
        try:

            response = requests.get(url)

            if response.status_code == 200:
                data["active_urls"].append(url)
                data["numer_active"] += 1
                logging.info(f"Url is active {url}")
            else:
                logging.info(f"Url {url} is {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(
                f'An error occurred while accessing the website {url}: {e}')

    data["urls"] = len(urls)

    return data


async def get_index_by_moniker(moniker: str, validators: list) -> int:
    for index, val in enumerate(validators):
        # current_moniker = val.get("description").get("moniker")
        # logging.info(f"{index} - {current_moniker}. Seeking: {moniker}")
        if val.get("description").get("moniker") == moniker:
            return int(index)


#
# Get slashing block
#


async def slashing_signing_info(key: str, url: str):

    config = toml.load("config.toml")
    bin = config["path_bin"]

    p_variable = {
        "@type": "/cosmos.crypto.ed25519.PubKey",
        "key": key,
    }
    p_json = json.dumps(p_variable)

    cmd = [bin, 'q', 'slashing', 'signing-info',
           p_json, '--node', url, '-o', 'json']
    result = await terminal(cmd)
    output = result[0].decode('utf-8')
    error = result[1].decode('utf-8')

    if output != '':
        output = json.loads(output)

    elif error != '':
        pass

    return output


async def missed_block_counter(moniker):
    validators = await get_validators()

    validator = validators[await get_index_by_moniker(moniker, validators)]

    missed_block = await slashing_signing_info(validator.get("consensus_pubkey").get("key"))

    print(missed_block)

# asyncio.run(missed_block_counter('ToTheMars'))


async def get_index_by_consAddr(const_addr: str, signing_infos: list) -> int:
    for index, val in enumerate(signing_infos):
        # current_moniker = val.get("description").get("moniker")
        # logging.info(f"{index} - {current_moniker}. Seeking: {moniker}")
        if val.get("address") == const_addr:
            return index


async def slashing_signing_info_all(url: str) -> list:

    config = toml.load("config.toml")
    bin = config["path_bin"]

    cmd = [bin, 'q', 'slashing', 'signing-infos',
           '--limit', '1000', '--node', url, '-o', 'json']
    result = await terminal(cmd)
    output = result[0].decode('utf-8')
    error = result[1].decode('utf-8')

    if output != '':
        output = json.loads(output)
        output = output["info"]

    elif error != '':
        pass

    return output
