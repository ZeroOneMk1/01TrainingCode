LOGINURL = "https://www.infosecclubresources.com/login?redirect="

USERNAME = "ZeroOne"
# This is not the password for anything important for me, so don't try using it anywhere else.
PASS = "7?~Mdd!'K&Ss28a;"

USERNAMEBUTTON = "/html/body/div/div/div/div/div/div/div[2]/div/form/div[1]/input"
PASSWORDBUTTON = "/html/body/div/div/div/div/div/div/div[2]/div/form/div[2]/input"
REMEMBERBUTTON = "/html/body/div/div/div/div/div/div/div[2]/div/form/div[3]/div/label"
LOGINBUTTON = "/html/body/div/div/div/div/div/div/div[2]/div/form/a"


HILLURL = "https://www.infosecclubresources.com/games/cipherKoTH/g/public/a1d48f47d3ed322a2a0c4948a3c776673a3308f6e09a2e9abb849d02/hill"
CYPHERLOCATION = "/html/body/div[1]/div/div/div/p[5]"
CYPHERFORMAT = r"(icrCTF{\S*})"
CYPHERSOLUTION = "icrCTF{"

F01LOCATION = "/html/body/div[1]/div/div/div/div/p[1]"

FLAGINPUTLOCATION = "/html/body/div[1]/div/div/div/form/input"
FLAGBUTTON = "/html/body/div[1]/div/div/div/form/a"

MORSECYPHERFORMAT = r"AA BABA ABA BABA B AABA {(\w+)\s(\w+)\s(\w+)\s(\w+)\s(\w+)\s(\w+)\s}"
BACONCYPHERFORMAT = r"ABAAA AAABA BAAAB AAABA BAABB AABAB {(\w+)\s(\w+)\s(\w+)\s(\w+)\s(\w+)\s(\w+)\s}"

MORSELETTERS = {"AB": "A", "BAAA": "B", "BABA": "C", "BAA": "D", "A": "E", "AABA": "F", "BBA": "G", "AAAA": "H", "AA": "I", "ABBB": "J", "BAB": "K", "ABAA": "L",
                "BB": "M", "BA": "N", "BBB": "O", "ABBA": "P", "BBAB": "Q", "ABA": "R", "AAA": "S", "B": "T", "AAB": "U", "AAAB": "V", "ABB": "W", "BAAB": "X",
                "BABB": "Y", "BBAA": "Z"}

BACONLETTERS = {"AAAAA": "A", "AAAAB": "B", "AAABA": "C", "AAABB": "D", "AABAA": "E", "AABAB": "F", "AABBA": "G", "AABBB": "H", "ABAAA": "I", "ABAAB": "J", "ABABA": "K", "ABABB": "L",
                "ABBAA": "M", "ABBAB": "N", "ABBBA": "O", "ABBBB": "P", "BAAAA": "Q", "BAAAB": "R", "BAABA": "S", "BAABB": "T", "BABAA": "U", "BABAB": "V", "BABBA": "W", "BABBB": "X",
                "BBAAA": "Y", "BBAAB": "Z"}
