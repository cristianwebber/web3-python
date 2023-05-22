from brownie import FruitaCoin

from scripts.config import get_account
from scripts.config import network_args


NAME = 'FruitaCoin'
SYMBOL = 'FRUITA'
PREMINT = 1_000_000


def deploy_token():
    account = get_account()

    token = FruitaCoin.deploy(
        NAME,
        SYMBOL,
        PREMINT,
        {'from': account},
        publish_source=network_args().get('verify', False),
    )
    print(f'Deployed {NAME} Token.')

    return token


def main():
    deploy_token()


if __name__ == '__main__':
    main()
