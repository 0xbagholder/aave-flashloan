from brownie import FlashloanV2, accounts, config, network, interface
from scripts.get_weth import get_weth
from scripts.deployment_v2 import main as run_deploy

MINIMUM_FLASHLOAN_WETH_BALANCE = 0.01 * 10**18
ETHERSCAN_TX_URL = "https://kovan.etherscan.io/tx/{}"


def main():
    run_deploy()
    get_weth()
    """
    Executes the funcitonality of the flash loan.
    """
    acct = accounts[0]
    # acct = accounts.add(config["wallets"]["from_key"])
    print("Getting Flashloan contract...")
    flashloan = FlashloanV2[len(FlashloanV2) - 1]
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth"])
    # We need to fund it if it doesn't have any token to fund!
    if weth.balanceOf(flashloan) < MINIMUM_FLASHLOAN_WETH_BALANCE:
        print("Funding Flashloan contract with WETH...")
        weth.transfer(flashloan, MINIMUM_FLASHLOAN_WETH_BALANCE, {"from": acct})
    print("Executing Flashloan...")
    tx = flashloan.flashloan(weth, {"from": acct})
    tx.wait(1)
    print("You did it! View your tx here: " + ETHERSCAN_TX_URL.format(tx.txid))
    return flashloan
