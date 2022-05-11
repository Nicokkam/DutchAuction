import pytest
import time
from brownie import Wei, accounts, DutchContract

owner = 2
buyer = 0

@pytest.fixture
def dutch_contract():
  return DutchContract.deploy(accounts[owner], 10*(10**18), (1/100)*(10**18), 500, {'from': accounts[owner]})

@pytest.fixture
def dutch_contract2():
  return DutchContract.deploy(accounts[owner], 100*(10**18), 20*(10**18), 5, {'from': accounts[owner]})

## TESTS ##

def test_lowerAmount(dutch_contract): #Check if prints error msg (I Want it to fail)
  pre_contract_balance = dutch_contract.getPrice()
  pre_buyer_balance = accounts[buyer].balance()
  dutch_contract.buy({'from':accounts[buyer], 'value': '1 ether'})

def test_exactAmount(dutch_contract):
  pre_contract_balance = dutch_contract.getPrice()
  pre_buyer_balance = accounts[buyer].balance()
  pre_owner_balance = accounts[owner].balance()
  dutch_contract.buy({'from':accounts[buyer], 'value': '10 ether'})

  assert accounts[buyer].balance() == pre_buyer_balance - pre_contract_balance
  assert accounts[owner].balance() == pre_owner_balance + pre_contract_balance

def test_greaterAmount(dutch_contract): #Check for refund
  pre_contract_balance = dutch_contract.getPrice()
  pre_buyer_balance = accounts[buyer].balance()
  pre_owner_balance = accounts[owner].balance()
  dutch_contract.buy({'from':accounts[buyer], 'value': '20 ether'})

  assert accounts[buyer].balance() == pre_buyer_balance - pre_contract_balance
  assert accounts[owner].balance() == pre_owner_balance + pre_contract_balance

def test_timeExpired(dutch_contract2): #Check if prints error msg (I Want it to fail)
  pre_contract_balance = dutch_contract2.getPrice()
  pre_buyer_balance = accounts[buyer].balance()
  pre_owner_balance = accounts[owner].balance()
  time.sleep(6)
  dutch_contract2.buy({'from':accounts[buyer], 'value': '100 ether'})

def test_isDiscountWorking(dutch_contract2):
  pre_buyer_balance = accounts[buyer].balance()
  pre_owner_balance = accounts[owner].balance()
  # dutch_contract2.buy({'from':accounts[buyer], 'value': '40 ether'}) -> Denied
  time.sleep(3)
  dutch_contract2.update({'from':accounts[owner], 'value': '0 ether'})
  pre_contract_balance = dutch_contract2.getPrice()
  dutch_contract2.buy({'from':accounts[buyer], 'value': '40 ether'}) #-> Approved

  assert accounts[buyer].balance() == pre_buyer_balance - pre_contract_balance
  assert accounts[owner].balance() == pre_owner_balance + pre_contract_balance

def test_hasAutoDestructed(dutch_contract): #Check if prints error msg (I Want it to fail)
  assert dutch_contract.seller() == accounts[owner]
  dutch_contract.buy({'from':accounts[buyer], 'value': '10 ether'})
  assert dutch_contract.exists() == accounts[owner]