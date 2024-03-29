from config import settings

import BlockChain.Utils
from .Lot import Lot

BASE_OF_HASH_DIGEST = 16


class ProofOfStake:
    def __init__(self):
        # map account keys to corresponding staking of the account
        self.stakers = {}
        self.set_genesisStake()

    def get_stakers(self):
        return self.stakers

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

    def buildLots(self, seed):
        """
        Generate lots for each staker using HASH CHAINING
        """
        lot_list = []

        for validator in self.stakers.keys():
            for current_stake in range(self.get_stake(validator)):
                lot_list.append(Lot(validator, current_stake + 1, seed))
        return lot_list

    def findWinner(self, lots, seed):
        """
        Establish a winning lot based on which lot hash has the
        minimum offset to a random generated one
        """
        winner_lot = None
        min_offset = None

        generated_hash = int(
            BlockChain.Utils.hash(seed).hexdigest(), BASE_OF_HASH_DIGEST
        )

        for lot in lots:
            lot_to_int = int(lot.lotHash(), BASE_OF_HASH_DIGEST)
            offset = abs(lot_to_int - generated_hash)

            if min_offset is None or offset < min_offset:
                min_offset = offset
                winner_lot = lot
        return winner_lot

    def selectForger(self, last_block_hash):
        """
        Returns the forger for the winning lot value
        """
        lots = self.buildLots(last_block_hash)
        winner_lot = self.findWinner(lots, last_block_hash)

        return winner_lot.public_key
