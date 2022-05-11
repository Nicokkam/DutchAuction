import os
# import pytest
from dotenv import load_dotenv
from brownie import Wei, accounts, DutchContract

load_dotenv()
def main():
  deploy_account = accounts.add(os.environ['PRIVATE_KEY_1'])
  deployment_details = {
    'from':deploy_account
    # ,'value':Wei('10 ether')
  }
  dutchContract = DutchContract.deploy(deploy_account, 1000*(10**18), 1*(10**18), 500, deployment_details)
  return dutchContract