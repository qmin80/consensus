from urllib.request import Request, urlopen
import math
from sys import exit
from json import loads
import csv

ERR_MSG = f"\033[91m[ERR] API endpoint unreachable: api\n" \
          f"[ERR] Be sure you have enabled your API " \
          f"(you can enable this in your app.toml config file)\n" \
          f"Bugreports Discord: Yep++#9963\033[0m"

# default ports
RPC = {
    "Akash" : "https://akash-rpc.polkachu.com",
    "AssetMantle" : "https://assetmantle-rpc.polkachu.com",
    "Axelar" : "https://axelar.rpc.stake2.me",
    "Band" : "http://rpc.laozi1.bandchain.org",
    "Bitcanna" : "https://bitcanna-rpc.polkachu.com",
    "Bitsong" : "https://rpc-bitsong.itastakers.com",
    "Cerberus" : "https://cerberus-rpc.polkachu.com",
    "Certik" : "https://certik-rpc.polkachu.com",
    "Chihuahua" : "https://chihuahua-rpc.polkachu.com",
    "Comdex" : "https://comdex-rpc.polkachu.com",
    "Cosmos" : "https://cosmos-rpc.polkachu.com",
    "Crypto.org" : "https://rpc.cosmos.directory/cryptoorgchain",
    "Desmos" : "https://rpc.morpheus.desmos.network",
    "Emoney" : "https://rpc-emoney.keplr.app",
    "Evmos" : "https://evmos-rpc.theamsolutions.info",
    "Fetch.AI" : "https://fetch-rpc.polkachu.com",
    "Gravity Bridge" : "https://gravitychain.io:26657",
    "Injective" : "https://injective-rpc.polkachu.com",
    "IRISnet" : "http://35.234.10.84:26657",
    "Juno" : "https://juno-rpc.polkachu.com",
    "Kava" : "https://rpc.kava.io",
    "KI Chain" : "https://kichain-rpc.polkachu.com",
    "Konstellation" : "https://konstellation-rpc.polkachu.com",
    "LUM" : "https://rpc.cosmos.directory/lumnetwork",
    "NYX (NYM)" : "https://nym-rpc.polkachu.com",
    "Omniflix" : "https://rpc.flixnet.omniflix.network",
    "Osmosis" : "https://osmosis-mainnet-rpc.allthatnode.com:26657",
    "Persistence" : "https://rpc.core.persistence.one",
    "Provenance" : "https://rpc.provenance.io",
    "Regen" : "https://rpc.cosmos.directory/regen",
    "Rizon" : "http://seed-1.mainnet.rizon.world:26657",
    "Secret" : "https://secret-4.api.trivium.network:26657",
    "Sentinel" : "https://rpc.sentinel.co",
    "Sifchain" : "https://sifchain-rpc.polkachu.com",
    "Stargaze" : "https://stargaze.rpc.stake2.me",
    "Starname" : "https://rpc.cosmos.directory/starname",
    "Terra" : "https://terra-rpc.easy2stake.com",
    "Umee" : "https://rpc.aphrodite.main.network.umee.cc",
}

REST = {
	"Akash" : "https://akash-api.polkachu.com",
	"AssetMantle" : "https://assetmantle-api.polkachu.com",
	"Axelar" : "https://axelar-api.polkachu.com",
	"Band" : "https://rest.cosmos.directory/bandchain",
	"Bitcanna" : "https://bitcanna-api.polkachu.com",
	"Bitsong" : "https://rest.cosmos.directory/bitsong",
	"Cerberus" : "https://cerberus-api.polkachu.com",
	"Certik" : "https://certik-api.polkachu.com",
	"Chihuahua" : "https://chihuahua-api.polkachu.com",
	"Comdex" : "https://comdex-api.polkachu.com",
	"Cosmos" : "https://cosmos-api.polkachu.com",
	"Crypto.org" : "https://rest.cosmos.directory/cryptoorgchain",
	"Desmos" : "https://rest.cosmos.directory/desmos",
	"Emoney" : "https://rest.cosmos.directory/emoney",
	"Evmos" : "https://evmos-api.theamsolutions.info",
	"Fetch.AI" : "https://fetch-api.polkachu.com",
	"Gravity Bridge" : "https://gravitychain.io:1317",
	"Injective" : "https://lcd.injective.network",
	"IRISnet" : "http://35.234.10.84:1317",
	"Juno" : "https://juno-api.polkachu.com",
	"Kava" : "https://api.kava.io",
	"KI Chain" : "https://kichain-api.polkachu.com",
	"Konstellation" : "https://konstellation-api.polkachu.com",
	"LUM" : "https://rest.cosmos.directory/lumnetwork",
	"NYX (NYM)" : "https://nym-api.polkachu.com",
	"Omniflix" : "https://rest.flixnet.omniflix.network",
	"Osmosis" : "https://osmosis.stakesystems.io",
	"Persistence" : "https://rest.cosmos.directory/persistence",
	"Provenance" : "https://api.provenance.io",
	"Regen" : "https://rest.cosmos.directory/regen",
	"Rizon" : "http://seed-1.mainnet.rizon.world:1317",
	"Secret" : "https://secret-4.api.trivium.network:1317",
	"Sentinel" : "https://lcd.sentinel.co",
	"Sifchain" : "https://sifchain-api.polkachu.com",
	"Stargaze" : "https://stargaze-api.polkachu.com",
	"Starname" : "https://rest.cosmos.directory/starname",
	"Terra" : "https://lcd.terra.dev",
	"Umee" : "https://api.aphrodite.main.network.umee.cc",
}

def handle_request(api: str, pattern: str):
    try:
        requestUrl = Request(f"{api}/{pattern}", headers={'User-Agent': 'Mozilla/5.0'})
        response = loads(urlopen(requestUrl).read())
        return response if response is not None else exit(ERR_MSG.replace('api', api))

    except Exception as e:
        print(e)
        exit(ERR_MSG.replace('api', api))


def strip_emoji_non_ascii(moniker):
    # moniker = emoji.replace_emoji(moniker, replace='')
    moniker = "".join([letter for letter in moniker if letter.isascii()])[:15].strip().lstrip()
    return moniker if moniker != "" else "Non_Ascii_Name"


def get_validators(chain):
    validators = []
    state_validators = STATE['result']['round_state']['validators']['validators']
    for val in state_validators:
        res = val['address'], val['voting_power'], val['pub_key']['value']
        validators.append(res)
        
    return validators


def get_validators_rest(chain):
    bonded_tokens = int(get_bonded(chain)["bonded_tokens"])
    validator_dict = {}
    validators = handle_request(REST[chain], '/staking/validators')["result"]

    for validator in validators:
        validator_vp = int(int(validator["tokens"]))
        vp_percentage = round((100 / bonded_tokens) * validator_vp, 3)
        moniker = validator["description"]["moniker"][:15].strip()
        moniker = strip_emoji_non_ascii(moniker)
        validator_dict[validator["consensus_pubkey"]["value"]] = {
                                 "moniker": moniker,
                                 "operator_address": validator["operator_address"],
                                 "status": validator["status"],
                                 "voting_power": validator_vp,
                                 "voting_power_perc": f"{vp_percentage}%"}

    return validator_dict, len(validators)

def merge_info(chain):

    validators = get_validators(chain)
    validator_rest, total_validators = get_validators_rest(chain)
    final_list = []

    for v in validators:
        if v[2] in validator_rest:
            validator_rest[v[2]]['address'] = v[0]
            final_list.append(validator_rest[v[2]])

    return final_list, total_validators


def get_chain_id(chain):
    response = handle_request(REST[chain], 'node_info')
    chain_id = response['node_info']['network']
    return chain_id


def get_bonded(chain):
    result = handle_request(REST[chain], '/cosmos/staking/v1beta1/pool')['pool']
    return result


def colorize_output(validators):
    result = []
    csv_result = []

    result.append("validator_address\tmoniker\tvoting_power\tvoting_power_perc\toperator_address")
    #csv_result.append(["validator_address","moniker","voting_power","voting_power_perc","operator_address"])

    for num, val in enumerate(validators):
        validator_address = val['address']
        moniker = val['moniker']
        voting_power = val['voting_power']
        voting_power_perc = val['voting_power_perc']
        operator_address = val['operator_address']
        rank = num + 1

        result.append(f"{validator_address}\t{moniker:<18}\t{voting_power}\t{voting_power_perc}\t{operator_address}")
        csv_result.append([f"{chain}",f"{rank}",f"{validator_address}",f"{moniker}",f"{voting_power}",f"{voting_power_perc}",f"{operator_address}"])

    return result, csv_result


def calculate_colums(result):
        return list_columns(result, cols=1)


def list_columns(obj, cols=3, columnwise=True, gap=8):
    # thnx to https://stackoverflow.com/a/36085705

    sobj = [str(item) for item in obj]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    return printer


def main(chain, STATE):
    validators, total_validators = merge_info(chain)

    result, csv_result = colorize_output(validators)
    #print(calculate_colums(result))

    #filename = get_chain_id(chain) + "_monikers.csv"    
    filename = "monikers.csv"    
    with open(filename, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(csv_result)
        
if __name__ == '__main__':

    for chain, rpc in RPC.items() :
        STATE = handle_request(rpc, 'dump_consensus_state')
        main(chain, STATE)
