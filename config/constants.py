RESOURCE_TYPES = [
    "PLANKS",
    "ORE",
    "FIBER",
    "HIDE",
    "CLOTH",
    "LEATHER",
    "STONEBLOCK",
    "METALBAR",
]
TIERS = list(range(4, 9))
ENCHANTMENTS = list(range(0, 5))
CITIES = [
    "Thetford",
    "Martlock",
    "Bridgewatch",
    "Lymhurst",
    "Fort Sterling",
    "Caerleon",
    "Black Market",
    "Brecilien",
]
BASE_URL = "https://www.albion-online-data.com/api/v2/stats/prices/"

# API Rate Limits
RATE_LIMIT_PER_MINUTE = 180
RATE_LIMIT_PER_5_MINUTES = 300
MAX_URL_LENGTH = 4096
BATCH_SIZE = 80  # Number of items to combine in a single request

# Rune Item IDs
RUNE_ITEMS = [
    "T4_RUNE",
    "T5_RUNE",
    "T6_RUNE",
    "T7_RUNE",
    "T8_RUNE",
]

# Artifact Item IDs
SOUL_ITEMS = [
    "T4_SOUL",
    "T5_SOUL",
    "T6_SOUL",
    "T7_SOUL",
    "T8_SOUL",
]

RELIC_ITEMS = [
    "T4_RELIC",
    "T5_RELIC",
    "T6_RELIC",
    "T7_RELIC",
    "T8_RELIC",
]

AVALONIAN_ITEMS = [
    "T4_SHARD_AVALONIAN",
    "T5_SHARD_AVALONIAN",
    "T6_SHARD_AVALONIAN",
    "T7_SHARD_AVALONIAN",
    "T8_SHARD_AVALONIAN",
]
