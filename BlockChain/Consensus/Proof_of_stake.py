import BlockChain.Utils
from .Lot import Lot
from config import settings


class ProofOfStake:
    def __init__(self):
        # map account keys to corresponding staking of the account
        self.stakers = {}
        self.set_genesisStake()

    def get_stake(self, public_key):
        if public_key in self.stakers.keys():
            return self.stakers[public_key]
        return None

    # set the first stake in the staker list, so we do not have an empty list
    def set_genesisStake(self):
        genesis_account_public = open(settings.genesis_public_key_path, "r").read()
        self.stakers[genesis_account_public] = 1

    # used to set the stake amount and add to staker accounts
    def update(self, public_key, stake_amount):
        if public_key in self.stakers.keys():
            self.stakers[public_key] += stake_amount
        else:
            self.stakers[public_key] = stake_amount

    """
    Generate lots for each staker using HASH CHAINING
    """

    def buildLots(self, seed):
        lot_list = []

        for validator in self.stakers.keys():
            for current_stake in range(self.get_stake(validator)):
                lot_list.append(Lot(validator, current_stake + 1, seed))
        return lot_list

    """
    Establish a winning lot based on which lot hash has the 
    minimum offset to a random generated one
    """

    def findWinner(self, lots, seed):
        winner_lot = None
        min_offset = None

        generated_hash = int(BlockChain.Utils.hash(seed).hexdigest(), 16)

        for lot in lots:
            lot_to_int = int(lot.lotHash(), 16)
            offset = abs(lot_to_int - generated_hash)

            if min_offset is None or offset < min_offset:
                min_offset = offset
                winner_lot = lot
        return winner_lot

    """
    Returns the forger for the winning lot value
    """

    def selectForger(self, last_block_hash):
        lots = self.buildLots(last_block_hash)
        winner_lot = self.findWinner(lots, last_block_hash)

        return winner_lot.public_key
