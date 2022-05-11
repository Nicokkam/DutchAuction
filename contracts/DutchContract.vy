# @version ^0.3.1

seller: public(address)
duration: public(uint256)
startingPrice: public(uint256)
startDate: public(uint256)
endDate: public(uint256)
discountRate: public(uint256)

@external
def __init__(_seller: address, _startingPrice: uint256, _discountRate: uint256, _duration: uint256):
    self.seller = _seller
    self.duration = _duration
    self.startingPrice = _startingPrice
    self.startDate = block.timestamp
    self.endDate = self.startDate + _duration
    self.discountRate = _discountRate
    assert _startingPrice >= _discountRate * _duration, "Starting price is lower than Min price"

@internal
@view
def _getPrice() -> uint256:
    timeElapsed: uint256 = block.timestamp - self.startDate
    discount: uint256 = self.discountRate * timeElapsed
    return self.startingPrice - discount

@external
@view
def getPrice() -> uint256:
	return self._getPrice()

@external
@payable
def update(): #THIS HAS TO BE HERE TO UPDATE THE CURRENT TIME (B_LOCK.TIMESTAMP)
    send(self.seller, msg.value)

@external
@payable
def buy():
    assert block.timestamp >= self.startDate, "Bidding period has not started"
    assert block.timestamp < self.endDate, "Bidding period is over"

    price: uint256 = self._getPrice()
    assert msg.value >= price, "ETH is not High Enough"

    send(self.seller, price)

    refund: uint256 = msg.value - price
    if refund > 0:
        send(msg.sender, refund)

    selfdestruct(self.seller)