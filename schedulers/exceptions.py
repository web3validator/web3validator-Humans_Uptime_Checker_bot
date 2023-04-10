class Errors:
    NoData = "No data"
    InvalidToken = "Invalid token"
    InvalidMoniker = "Invalid moniker"
    NoMonikerSpecified = "No moniker specified"
    InvalidPlatform = "Invalid platform"
    NoBlocks = "No blocks"
    NoValidators = "No validators"
    NoValidatorWithMoniker = "No validator with this moniker"
    NoConsensusPubkey = "No consensus pubkey"
    NoSlashingInfo = "No slashing info"
    NoMissedBlocksCounter = "No missed blocks"


class NoData(Exception):
    pass


class InvalidToken(Exception):
    pass


class InvalidMoniker(Exception):
    pass


class NoMonikerSpecified(Exception):
    pass


class InvalidPlatform(Exception):
    pass


class NoBlocks(Exception):
    pass


class NoValidators(Exception):
    pass


class NoValidatorWithMoniker(Exception):
    pass


class NoConsensusPubkey(Exception):
    pass


class NoSlashingInfo(Exception):
    pass


class NoMissedBlocksCounter(Exception):
    pass


def raise_error(e: str):
    if e == Errors.NoData:
        raise NoData
    elif e == Errors.InvalidToken:
        raise InvalidToken
    elif e == Errors.InvalidMoniker:
        raise InvalidMoniker
    elif e == Errors.NoMonikerSpecified:
        raise NoMonikerSpecified
    elif e == Errors.InvalidPlatform:
        raise InvalidPlatform
    elif e == Errors.NoBlocks:
        raise NoBlocks
    elif e == Errors.NoValidators:
        raise NoValidators
    elif e == Errors.NoValidatorWithMoniker:
        raise NoValidatorWithMoniker
    elif e == Errors.NoConsensusPubkey:
        raise NoConsensusPubkey
    elif e == Errors.NoSlashingInfo:
        raise NoSlashingInfo
    elif e == Errors.NoMissedBlocksCounter:
        raise NoMissedBlocksCounter
