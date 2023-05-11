from scripts.config import get_account, get_contract, network_args
from brownie import Lottery

def deploy_lottery():
    account = get_account()
    # network_args = network_args()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        network_args()["fee"],
        network_args()["keyhash"],
        {"from": account},
        publish_source=network_args().get("verify", False),
    )
    print("Deployed Lottery")

def main():
    deploy_lottery()

if __name__ == '__main__':
    main()
