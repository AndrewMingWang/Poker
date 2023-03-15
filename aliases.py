def aliasToPerson(alias):
    for person in aliases:
        if alias in aliases[person]:
            return person
    print("ERROR! Alias not tracked: ", alias)

people = {"Joel", "Andi", "Andrew", "Danial", "Dorothy", "Fred", "Jade", "Juli", "Matthew", "Qi", "Sunny", "William"}
aliases = {
    "Andi": [
        "Ayatollah Cum",
        "Ayatollah cum"
    ],
    "Andrew": [
        "Andrew"
    ],
    "Danial": [
        "Danial"
    ],
    "Dorothy": [
        "dorothy"
    ],
    "Fred": [
        "Fred"
    ],
    "Jade": [
        "Jade"
    ],
    "Joel": [
        "Joel"
    ],
    "Juli": [
        "Juli",
        "Jul"
    ],
    "Matthew": [
        "matt2"
    ],
    "Qi": [
        "qipanda"
    ],
    "Sunny": [
        "the giver x4",
        "the giver x2",
        "the giver",
        "sunny"
    ],
    "William": [
        "william",
        "William",
    ]
}