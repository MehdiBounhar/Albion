"""
This file contains the EN-US names of artifacts organized by category and subcategory.
Users can fill in the names for each category and subcategory.
"""

ARTIFACT_NAMES = {
    # Rune artifacts
    "Rune": {
        "Warrior": [
            "Ancient Hammer Head",
            "Lost Crossbow Mechanism",
            "Runed Rock",
            "Bloodforged Blade",
            "Morgana Halberd Head",
            "Ursine Guardian Remains",
            "Ancient Chain Rings",
            "Ancient Padding",
            "Ancient Bindings",
            "Ancient Shield Core"
        ],
        "Mage": [
            "Lost Arcane Crystal",
            "Lost Cursed Crystal",
            "Wildfire Orb",
            "Hoarfrost Orb",
            "Possessed Scroll",
            "Druidic Feathers",
            "Druidic Preserved Beak",
            "Druidic Bindings",
            "Alluring Crystal"

        ],
        "Hunter": [
            "Keeper Spearhead",
            "Hardened Debole",
            "Ghastly Arrows",
            "Reinforced Morgana Pole",
            "Imbued Leather Folds",
            "Imbued Visor",
            "Imbued Soles",
            "Runed Horn",
            "Druidic Inscriptions"
        ]
    },
    
    # Soul artifacts
    "Soul": {
        "Warrior": [
            "Demonic Blade",
            "Hellish Bolts",
            "Hellish Hammer Heads",
            "Hellish Sicklehead",
            "Infernal Mace Head",
            "Severed Demonic Horns",
            "Infernal Shield Core",
            "Demonic Plates",
            "Demonic Scraps",
            "Demonic Filling"
        ],
        "Mage": [
            "Occult Orb",
            "Burning Orb",
            "Infernal Scroll",
            "Icicle Orb",
            "Cursed Jawbone",
            "Demonic Jawbone",
            "Infernal Cloth Folds",
            "Infernal Cloth Visor",
            "Infernal Cloth Bindings"
            
        ],
        "Hunter": [
            "Demonic Arrowhead",
            "Infernal Harpoon Tip",
            "Broken Demonic Fang",
            "Symbol of Blight",
            "Hellish Sicklehead Pair",
            "Hellish Handle",
            "Demonic Leather",
            "Demonhide Padding",
            "Demonhide Bindings"
        ]
    },
    
    # Relic artifacts
    "Relic": {
        "Warrior": [
            "Cursed Blades",
            "Keeper Axeheads",
            "Engraved Log",
            "Alluring Bolts",
            "Imbued Mace Head",
            "Warped Raven Plate",
            "Bloodforged Spikes",
            "Carved Skull Padding",
            "Preserved Animal Fur",
            "Inscribed Bindings"
        ],
        "Mage": [
            "Cursed Frozen Crystal",
            "Ghastly Scroll",
            "Bloodforged Catalyst",
            "Processesed Catalyst",
            "Unholy Scroll",
            "Inscribed Stone",
            "Alluring Padding",
            "Alluring Amulet",
            "Alluring Bindings"
        ],
        "Hunter": [
           "Carved Bone",
           "Preserved Rocks",
           "Ghastly Blades",
           "Crused Barbs",
           "Preserved Log",
           "Ghastly Candle",
           "Ghastly Visor",
           "Ghastly Leather",
           "Ghastly Bindings"
        ]
    },
    
    # Avalonian Shard artifacts
    "Avalonian Shard": {
        "Warrior": [
            "Exalted Plating",
            "Exalted Visor",
            "Exalted Greave",
            "Avalonian Battle Memoir",
            "Remnants of the Old King",
            "Massive Metallic Hand",
            "Broken Oaths",
            "Damaged Avalonian Gauntlet",
            "Humming Avalonian Whirligig",
            "Crushed Avalonian Heirloom"
        ],
        "Mage": [
           "Sanctified Belt",
           "Sanctified Mask",
           "Sanctified Bindings",
           "Fractured Opaque Orb",
           "Glowing Harmonic Ring",
           "Chilled Crystalline Shard",
           "Hypnotic Harmonic Ring",
           "Messianic Curio",
           "Severed Celestial Keepsake"
        ],
        "Hunter": [
            "Augured Sash",
            "Augured Padding",
            "Augured Fasteners",
            "Bloodstained Antiquities",
            "Ruined Ancestral Vamplate",
            "Timeworn Walking Staff",
            "Immaculately Crafted Riser",
            "Uprooted Perennial Sapling",
            "Shattered Avalonian Memento"
        ]
    }
}

def get_all_names() -> list[str]:
    """
    Get all EN-US names from all categories and subcategories.
    
    Returns:
        list[str]: List of all EN-US names
    """
    all_names = []
    for category in ARTIFACT_NAMES.values():
        for subcategory in category.values():
            all_names.extend(subcategory)
    return all_names

def get_names_by_category(category: str) -> list[str]:
    """
    Get all EN-US names for a specific category.
    
    Args:
        category (str): The category to get names for (Rune, Soul, Relic, or Avalonian Shard)
    
    Returns:
        list[str]: List of EN-US names for the specified category
    """
    if category not in ARTIFACT_NAMES:
        return []
    
    names = []
    for subcategory in ARTIFACT_NAMES[category].values():
        names.extend(subcategory)
    return names

def get_names_by_category_and_subcategory(category: str, subcategory: str) -> list[str]:
    """
    Get all EN-US names for a specific category and subcategory.
    
    Args:
        category (str): The category to get names for (Rune, Soul, Relic, or Avalonian Shard)
        subcategory (str): The subcategory to get names for (Warrior, Mage, or Hunter)
    
    Returns:
        list[str]: List of EN-US names for the specified category and subcategory
    """
    if category not in ARTIFACT_NAMES or subcategory not in ARTIFACT_NAMES[category]:
        return []
    
    return ARTIFACT_NAMES[category][subcategory] 