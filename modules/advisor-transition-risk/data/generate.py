"""
Synthetic data generator for the advisor transition risk demo.

Generates ~35 advisors (including 3 designed cases + 1 planted contrast)
and ~1,000 households (including 4 designed cases), scores everything,
and writes data.json.

Usage:
    python generate.py
"""

import json
import random
from pathlib import Path
from scoring import (
    score_advisor,
    score_household_baseline,
    score_household_follow,
    compute_concentration,
)
from cases import ADVISOR_CASES, HOUSEHOLD_CASES

random.seed(42)

# ---------------------------------------------------------------------------
# Name pools — large enough for ~1,000 unique household names
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "Sarah", "Michael", "Jennifer", "David", "Emily", "Robert", "Jessica",
    "William", "Amanda", "Christopher", "Ashley", "Daniel", "Stephanie",
    "Matthew", "Nicole", "Andrew", "Elizabeth", "Joshua", "Michelle",
    "Anthony", "Laura", "Kevin", "Rachel", "Brian", "Samantha", "Ryan",
    "Katherine", "Mark", "Megan", "Steven", "Rebecca", "Thomas", "Angela",
    "Timothy", "Heather", "Jason", "Patricia", "Jeffrey", "Christine",
    "Nathan",
]

LAST_NAMES = [
    "Anderson", "Martinez", "Thompson", "Garcia", "Robinson", "Clark",
    "Lewis", "Walker", "Hall", "Young", "Allen", "King", "Wright", "Scott",
    "Green", "Baker", "Adams", "Nelson", "Hill", "Campbell", "Mitchell",
    "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker",
    "Collins", "Edwards", "Stewart", "Morris", "Murphy", "Rivera", "Cook",
    "Rogers", "Morgan", "Peterson", "Cooper", "Reed", "Bailey", "Bell",
    "Howard", "Ward", "Cox", "Russell", "Foster", "Hayes", "Sullivan",
]

# ~1,100 unique family surnames — no suffixes needed
FAMILY_NAMES = sorted(set([
    # Original set
    "Sullivan", "Vasquez", "Chen-Williams", "Abramov", "Okonkwo",
    "Johansson", "Patel-Shah", "McCarthy", "Dubois", "Tanaka",
    "Krishnamurthy", "O'Brien", "Lindqvist", "Morales", "Fitzgerald",
    "Kaminski", "Al-Rashid", "Bergmann", "Santoro", "Whitfield",
    "Holloway", "Drummond", "Matsuda", "Collingwood", "Beaumont",
    "Sinclair", "Castellano", "Pemberton", "Stanhope", "Ashworth",
    "Tremaine", "Lockwood", "Kingsley", "Harrington", "Fairbanks",
    "Montague", "Aldridge", "Thornton", "Calloway", "Wentworth",
    "Blackwell", "Prescott", "Hawthorne", "Radcliffe", "Sterling",
    "Cartwright", "Langford", "Merriweather", "Worthington", "Ashford",
    "Kensington", "Ainsworth", "Bainbridge", "Dalton", "Eastwood",
    "Farrington", "Grantham", "Hemsworth", "Ingham", "Jameson",
    # Extended set — distinct real surnames, no fabricated suffixes
    "Abernathy", "Ackerman", "Adler", "Aguilar", "Albright",
    "Alderman", "Alfonso", "Allard", "Allison", "Almeida",
    "Altman", "Amato", "Ambrose", "Andersen", "Andrade",
    "Angelos", "Anselmo", "Appleby", "Archer", "Armitage",
    "Armstrong", "Arnett", "Ashby", "Ashton", "Atherton",
    "Atkinson", "Aubrey", "Avery", "Ayers", "Babcock",
    "Bachmann", "Bader", "Bagley", "Ballard", "Bancroft",
    "Banner", "Barclay", "Barlow", "Barnard", "Barnett",
    "Barrera", "Barrett", "Barrow", "Bartlett", "Barton",
    "Bassett", "Bates", "Baxter", "Beckett", "Bedford",
    "Belmont", "Benedict", "Bennett", "Benson", "Bentley",
    "Beresford", "Bergen", "Berkley", "Bernard", "Bethune",
    "Beveridge", "Bigelow", "Billings", "Bishop", "Blackburn",
    "Blackwood", "Blair", "Blake", "Blanchard", "Blanton",
    "Bledsoe", "Bloom", "Blythe", "Bogart", "Bolton",
    "Bonner", "Booker", "Booth", "Borden", "Boswell",
    "Bourne", "Bowden", "Bowen", "Bowman", "Boyd",
    "Bradford", "Bradley", "Brady", "Bragg", "Brandon",
    "Brandt", "Brennan", "Brewster", "Bridges", "Briggs",
    "Brinker", "Bristow", "Brock", "Broderick", "Bronson",
    "Brookfield", "Brooks", "Broughton", "Browning", "Buchanan",
    "Buckley", "Buford", "Burgess", "Burke", "Burnett",
    "Burns", "Burrell", "Burton", "Butler", "Butterfield",
    "Cadwell", "Calderon", "Caldwell", "Callahan", "Cameron",
    "Carmichael", "Carrington", "Carroll", "Carson", "Caruso",
    "Chadwick", "Chamberlain", "Chambers", "Chandler", "Chapin",
    "Chapman", "Chastain", "Cheney", "Chilton", "Cho",
    "Christiansen", "Churchill", "Clancy", "Claridge", "Clayton",
    "Clement", "Cleveland", "Clifford", "Clifton", "Coburn",
    "Cochran", "Coffey", "Colburn", "Coleman", "Collier",
    "Compton", "Connelly", "Connors", "Conrad", "Conway",
    "Corbett", "Cordero", "Corwin", "Costello", "Courtney",
    "Covington", "Cowan", "Crawford", "Crenshaw", "Crockett",
    "Cromwell", "Crosby", "Crossley", "Crowley", "Cullen",
    "Cummings", "Cunningham", "Curran", "Cushing", "Cutler",
    "Davenport", "Davidson", "Dawkins", "Dawson", "Deacon",
    "Decker", "Delacroix", "Delaney", "Dempsey", "Denison",
    "Denton", "Desmond", "Devereaux", "Devlin", "Dickinson",
    "Dillard", "Dixon", "Donahue", "Donovan", "Dorsey",
    "Douglas", "Dowling", "Downey", "Drake", "Draper",
    "Drayton", "Drew", "Driscoll", "Duffy", "Dugan",
    "Dunbar", "Duncan", "Dunham", "Dunlap", "Dunn",
    "Dupont", "Durham", "Durkin", "Dutton", "Dwyer",
    "Eagan", "Eaton", "Eckert", "Edgerton", "Edmonds",
    "Eldridge", "Elliot", "Ellis", "Ellsworth", "Elmore",
    "Emerson", "Emery", "Endicott", "Enright", "Erickson",
    "Espinoza", "Estes", "Everett", "Fairchild", "Falconer",
    "Fanning", "Farley", "Farnsworth", "Farrell", "Faulkner",
    "Feldman", "Felton", "Fenwick", "Ferguson", "Ferris",
    "Fielding", "Finch", "Finley", "Fischer", "Fleming",
    "Fletcher", "Flores", "Flynn", "Fontaine", "Forbes",
    "Ford", "Forrest", "Forsythe", "Frazier", "Freemont",
    "French", "Frost", "Fulton", "Galbraith", "Gallagher",
    "Galloway", "Gamble", "Gannon", "Gardiner", "Garfield",
    "Garner", "Garrett", "Garrison", "Gaskin", "Gates",
    "Gentry", "Gibbs", "Gibson", "Gifford", "Gilbert",
    "Gilchrist", "Gillespie", "Gilmore", "Gladstone", "Glenn",
    "Glover", "Godfrey", "Goodman", "Goodrich", "Goodwin",
    "Gordon", "Grady", "Grafton", "Graham", "Grant",
    "Graves", "Grayson", "Greenfield", "Greenwood", "Gregory",
    "Griffin", "Griffith", "Grimes", "Grisham", "Grover",
    "Guerrero", "Guilford", "Gutierrez", "Hadley", "Hagen",
    "Haines", "Hale", "Halliday", "Halsey", "Hamilton",
    "Hammond", "Hampton", "Hancock", "Hanley", "Harding",
    "Hardy", "Hargrove", "Harmon", "Harper", "Hartley",
    "Hartwell", "Harvey", "Haskins", "Hastings", "Hathaway",
    "Hayden", "Hayward", "Hazleton", "Healy", "Heath",
    "Hedges", "Henderson", "Henley", "Hennessy", "Henson",
    "Herbert", "Hernandez", "Hewitt", "Hickman", "Higgins",
    "Hilliard", "Hilton", "Hobbs", "Hodges", "Hoffman",
    "Holbrook", "Holcomb", "Holland", "Hollis", "Holman",
    "Holmes", "Holt", "Hood", "Hooper", "Hopkins",
    "Horton", "Houghton", "Houston", "Howell", "Hubbard",
    "Hudson", "Huffman", "Humphrey", "Hunt", "Hunter",
    "Huntington", "Hurley", "Hutchins", "Hutton", "Hyde",
    "Ingalls", "Ingram", "Irwin", "Iverson", "Ivory",
    "Jablonski", "Jackman", "Jacobson", "Jarvis", "Jefferson",
    "Jennings", "Jensen", "Jericho", "Johannsen", "Joiner",
    "Jordan", "Jorgensen", "Judson", "Keating", "Keller",
    "Kelley", "Kendall", "Kendrick", "Kennedy", "Kenyon",
    "Kerr", "Kessler", "Kilpatrick", "Kimball", "Kincaid",
    "Kirkland", "Kirkpatrick", "Klein", "Knapp", "Knightley",
    "Knox", "Krueger", "Lacey", "Lafferty", "Lambert",
    "Lancaster", "Landry", "Langdon", "Langley", "Larkin",
    "Larsen", "Lassiter", "Latham", "Laughlin", "Laurence",
    "Lavigne", "Lawrence", "Lawson", "Layton", "Leach",
    "Leighton", "Lennox", "Leonard", "Leverett", "Livingston",
    "Lombard", "Lonergan", "Loomis", "Lowell", "Lowry",
    "Lucas", "Ludlow", "Lundgren", "Lyons", "MacAllister",
    "MacArthur", "MacDonald", "Mackenzie", "MacLean", "Maddox",
    "Madigan", "Magnuson", "Maguire", "Mahoney", "Mallory",
    "Malone", "Mandeville", "Manning", "Marchetti", "Markham",
    "Marlowe", "Marquardt", "Marshall", "Martinson", "Mason",
    "Masterson", "Matheson", "Mauldin", "Maxwell", "McBride",
    "McCaffrey", "McClellan", "McConnell", "McCord", "McCormick",
    "McCoy", "McDermott", "McDowell", "McElroy", "McFadden",
    "McGrath", "McGregor", "McIntyre", "McKenna", "McKinney",
    "McLaughlin", "McMahon", "McNally", "McPherson", "McQueen",
    "Meacham", "Meadows", "Melton", "Mendez", "Mercer",
    "Meredith", "Merrick", "Metcalf", "Middleton", "Milford",
    "Millard", "Monroe", "Montoya", "Moody", "Moorehead",
    "Moran", "Moreland", "Moreno", "Moriarty", "Morley",
    "Morrow", "Morse", "Morton", "Moseley", "Mullen",
    "Mulligan", "Munroe", "Murdock", "Murillo", "Nance",
    "Navarro", "Neely", "Neff", "Neville", "Newberry",
    "Newcomb", "Newell", "Newkirk", "Newman", "Newton",
    "Nichols", "Nicholson", "Noble", "Nolan", "Norberg",
    "Nordstrom", "Norman", "Norris", "Northcott", "Norton",
    "Novak", "Nowell", "Nugent", "Oakes", "Oberlin",
    "Ogden", "Ogilvy", "Oliphant", "Olsen", "O'Malley",
    "O'Neill", "Ormsby", "Osborne", "Oswald", "Overstreet",
    "Owens", "Padgett", "Palmer", "Parham", "Parish",
    "Parkinson", "Parnell", "Parrish", "Parsons", "Pascale",
    "Paxton", "Peabody", "Pearce", "Pearson", "Peck",
    "Pelham", "Pendleton", "Penn", "Pennington", "Peralta",
    "Perkins", "Perrault", "Perry", "Phelps", "Pickering",
    "Pierce", "Platt", "Plummer", "Pollard", "Pollock",
    "Poole", "Pope", "Porter", "Portman", "Potter",
    "Powell", "Pratt", "Prentice", "Preston", "Price",
    "Prichard", "Proctor", "Pryor", "Putnam", "Quigley",
    "Quincy", "Quinn", "Rafferty", "Ramsey", "Randall",
    "Randolph", "Rankin", "Ratcliff", "Rawlings", "Rayburn",
    "Redmond", "Reeves", "Regan", "Remington", "Renwick",
    "Reynolds", "Rhodes", "Richmond", "Ridgeway", "Riley",
    "Rinehart", "Ritchie", "Robbins", "Rochester", "Rockwell",
    "Rodgers", "Roland", "Rollins", "Romano", "Rosenthal",
    "Rossi", "Rothwell", "Rourke", "Rowan", "Rowland",
    "Ruiz", "Runyon", "Ruskin", "Rutherford", "Rutledge",
    "Ryder", "Sackville", "Sadler", "Salazar", "Salisbury",
    "Sandberg", "Sanders", "Sanford", "Santiago", "Saunders",
    "Savage", "Sawyer", "Scanlon", "Schaefer", "Schneider",
    "Schofield", "Schuyler", "Sedgwick", "Selby", "Seton",
    "Seward", "Sexton", "Seymour", "Shackleton", "Shaffer",
    "Shannon", "Shapiro", "Sharpe", "Shaw", "Shea",
    "Sheffield", "Sheldon", "Shelton", "Shepard", "Sheridan",
    "Sherman", "Sherwood", "Shipley", "Shirley", "Simmons",
    "Sinclair", "Skinner", "Sloane", "Smedley", "Somerset",
    "Sondheim", "Sorensen", "Southgate", "Spalding", "Spencer",
    "Stafford", "Stallworth", "Stanford", "Stanton", "Stark",
    "Stedman", "Steele", "Steinberg", "Stephens", "Stern",
    "Stetson", "Stevenson", "Stillman", "Stokes", "Stone",
    "Stratton", "Strickland", "Strong", "Stroud", "Stuart",
    "Summerfield", "Sumner", "Sutherland", "Sutton", "Swanson",
    "Sweeney", "Sykes", "Talbot", "Tanner", "Tate",
    "Templeton", "Tennyson", "Thatcher", "Thayer", "Thorpe",
    "Thurston", "Tierney", "Tillman", "Tindall", "Tobin",
    "Todd", "Tomlinson", "Townsend", "Tracy", "Trask",
    "Trent", "Trevelyan", "Truman", "Tucker", "Tulley",
    "Turnbull", "Tuttle", "Underwood", "Upshaw", "Upton",
    "Valdez", "Valentine", "Van Buren", "Vance", "Vanderbilt",
    "Vargas", "Vaughan", "Vernon", "Vickers", "Vincent",
    "Wadsworth", "Wakefield", "Walcott", "Waldron", "Wallace",
    "Waller", "Walters", "Walton", "Warburton", "Warfield",
    "Warner", "Warren", "Warwick", "Washington", "Waterford",
    "Watkins", "Watson", "Watts", "Weatherby", "Weaver",
    "Webb", "Webster", "Weldon", "Wellington", "Wells",
    "Wescott", "Westbrook", "Weston", "Westover", "Wexford",
    "Wheatley", "Wheeler", "Whitaker", "Whitcomb", "Whitney",
    "Whitmore", "Whittaker", "Wickham", "Wilder", "Wilkins",
    "Willoughby", "Wilmot", "Winchester", "Windsor", "Winslow",
    "Winters", "Wolcott", "Wolfe", "Woodbury", "Woodward",
    "Woolsey", "Wycliffe", "Wyndham", "Yates", "York",
    "Youngblood", "Zimmerman",
    # Additional pool to exceed 1,000 unique names
    "Aaronson", "Abbot", "Ackroyd", "Adair", "Ahearn",
    "Alcott", "Aldous", "Alford", "Allingham", "Alston",
    "Amherst", "Anstey", "Arbuthnot", "Arden", "Ashcroft",
    "Astor", "Athey", "Attwood", "Axton", "Babington",
    "Badger", "Bagshaw", "Bakewell", "Baldridge", "Balfour",
    "Bannerman", "Barcroft", "Bardwell", "Barfield", "Barham",
    "Barnwell", "Bartram", "Basford", "Beachcroft", "Beardsley",
    "Beckford", "Beecham", "Bellingham", "Benbow", "Bentham",
    "Berkshire", "Berwick", "Bethell", "Bickford", "Biddulph",
    "Birchwood", "Blackstone", "Blakeley", "Bligh", "Blundell",
    "Bolingbroke", "Bonham", "Bonington", "Boothby", "Boscombe",
    "Bottomley", "Brabourne", "Brackenridge", "Bradshaw", "Brampton",
    "Bransfield", "Brearley", "Brentwood", "Brigham", "Broadhurst",
    "Bromfield", "Brookhaven", "Brougham", "Brownlee", "Brunton",
    "Buckminster", "Burford", "Burgham", "Burleigh", "Burnham",
    "Butterworth", "Cadbury", "Calthorpe", "Camberwell", "Campion",
    "Canfield", "Cardwell", "Carlisle", "Carstairs", "Caulfield",
    "Cavendish", "Chadbourne", "Chalford", "Charlesworth", "Chatsworth",
    "Chelmsford", "Cheswick", "Chisholm", "Churchwell", "Clarendon",
    "Clayborne", "Clemson", "Clivedon", "Coleridge", "Colquhoun",
    "Congreve", "Coningsby", "Copeland", "Copperthwaite", "Cosgrove",
    "Cottingham", "Craddock", "Cranborne", "Cranston", "Craven",
    "Creswell", "Critchley", "Crofton", "Crossfield", "Crowther",
    "Dallimore", "Darnley", "Dashwood", "Daventry", "Debenham",
    "Denholm", "Devonshire", "Digby", "Dorchester", "Drayford",
    "Duxbury", "Eccleston", "Ellerby", "Elmsford", "Enfield",
    "Errington", "Etchingham", "Eversley", "Fairfax", "Falkland",
    "Fanshawe", "Featherstone", "Fenworth", "Fincastle", "Fitzroy",
    "Foxworth", "Fulbright", "Gainsborough", "Galsworthy", "Gateshead",
    "Gilbertson", "Glanville", "Glastonbury", "Goldsworth", "Granville",
]))


TEAMS = ["Northeast", "Southeast", "Midwest", "West", "Central"]

SERVICE_LINES = ["investments", "planning", "banking", "insurance", "trust"]

ORG_EVENT_OPTIONS = ["passed_over", "manager_change", "compliance_action"]

COVERING_ADVISORS = [
    "Sarah Anderson", "Michael Clark", "Jennifer Wright",
    "David Scott", "Emily Baker",
]


# ---------------------------------------------------------------------------
# Planted contrast advisor — Elevated band, low concentration
# ---------------------------------------------------------------------------

CONTRAST_ADVISOR = {
    "advisor_id": "ADV-RUSSO",
    "name": "Patricia Russo",
    "team": "Midwest",
    "tenure_years": 4,
    "comp_ratio": 0.84,
    "production_trend_pct": -5,
    "org_events": ["passed_over"],
    "engagement_decline_pct": 25,
    "free_text_notes": ["not sure about future here"],
    "status": "active",
    "departure_date": None,
    "score_as_of_date": None,
    # Expected: comp=20, prod=14, tenure=10, org=5, eng=10, text=4 → 63 Elevated
    # But her book is firm-originated, multi-service, deeply embedded → low concentration
}


# ---------------------------------------------------------------------------
# Random advisor generation
# ---------------------------------------------------------------------------

def _random_advisor(advisor_id: str, target_band: str = "Stable") -> dict:
    """Generate a random advisor.

    target_band biases the signal generation to land in a particular band
    but doesn't guarantee it — provides realistic variance.
    """
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    if target_band == "Watch":
        # Bias toward mid-range signals
        tenure = round(random.triangular(2, 12, 4), 1)
        comp = round(random.gauss(0.93, 0.06), 2)
        comp = max(0.78, min(1.15, comp))
        prod = round(random.gauss(-2, 4), 1)
        prod = max(-12, min(8, prod))
        # Higher chance of one org event
        events = []
        for evt in ORG_EVENT_OPTIONS:
            if random.random() < 0.25:
                events.append(evt)
        eng = round(max(0, random.gauss(15, 10)), 1)
        # Occasional text signal
        notes = []
        if random.random() < 0.3:
            notes.append(random.choice([
                "seems distracted lately",
                "less engaged in recent team meetings",
                "frustrated with new reporting requirements",
                "skipping team meetings more often",
            ]))
    elif target_band == "Elevated":
        tenure = round(random.triangular(2, 8, 4), 1)
        comp = round(random.gauss(0.87, 0.05), 2)
        comp = max(0.78, min(0.98, comp))
        prod = round(random.gauss(-6, 3), 1)
        prod = max(-14, min(0, prod))
        events = []
        for evt in ORG_EVENT_OPTIONS:
            if random.random() < 0.35:
                events.append(evt)
        if not events:
            events.append(random.choice(ORG_EVENT_OPTIONS))
        eng = round(max(0, random.gauss(28, 12)), 1)
        notes = []
        if random.random() < 0.4:
            notes.append(random.choice([
                "seems distracted lately",
                "less engaged in recent team meetings",
                "frustrated with management changes",
            ]))
    else:  # Stable
        tenure = round(random.triangular(1, 20, 9), 1)
        comp = round(random.gauss(1.02, 0.06), 2)
        comp = max(0.88, min(1.25, comp))
        prod = round(random.gauss(2, 4), 1)
        prod = max(-6, min(15, prod))
        events = []
        for evt in ORG_EVENT_OPTIONS:
            if random.random() < 0.05:
                events.append(evt)
        eng = round(max(0, random.gauss(3, 6)), 1)
        notes = []

    return {
        "advisor_id": advisor_id,
        "name": f"{first} {last}",
        "team": random.choice(TEAMS),
        "tenure_years": tenure,
        "comp_ratio": comp,
        "production_trend_pct": prod,
        "org_events": events,
        "engagement_decline_pct": eng,
        "free_text_notes": notes,
        "status": "active",
        "departure_date": None,
        "score_as_of_date": None,
    }


# ---------------------------------------------------------------------------
# Household generators
# ---------------------------------------------------------------------------

def _random_household(household_id: str, advisor_id: str,
                      advisor_tenure: float) -> dict:
    """Generate a random household with default distributions."""
    # AUM: $1M-$15M typical, occasional up to $40M
    if random.random() < 0.05:
        aum = round(random.uniform(15_000_000, 40_000_000), -4)
    else:
        aum = round(random.uniform(1_000_000, 15_000_000), -4)

    firm_tenure = round(random.uniform(
        max(1, advisor_tenure * 0.3),
        max(advisor_tenure * 1.8, 15)
    ), 1)
    adv_tenure = round(random.uniform(
        0.5, min(firm_tenure, advisor_tenure)
    ), 1)

    origin = random.choice(["advisor_book", "firm_originated", "firm_originated"])
    n_services = random.choices([1, 2, 3, 4, 5], weights=[25, 30, 22, 15, 8])[0]
    services = random.sample(SERVICE_LINES, min(n_services, len(SERVICE_LINES)))
    contacts = random.choices([0, 1, 2, 3, 4, 5],
                               weights=[12, 22, 25, 22, 12, 7])[0]
    portal = round(max(0, random.gauss(5, 4)), 1)
    comm_excl = round(random.uniform(15, 95), 0)
    fee = random.randint(10, 95)
    perf = round(random.gauss(0.5, 3), 1)
    perf = max(-8, min(8, perf))
    complaints = random.choices([0, 1, 2, 3, 4],
                                 weights=[60, 20, 10, 7, 3])[0]
    net_flow = round(random.gauss(0, 5), 1)
    net_flow = max(-20, min(15, net_flow))
    sat = random.choices(
        [None, 3, 4, 5, 6, 7, 8, 9, 10],
        weights=[10, 2, 3, 5, 8, 15, 25, 22, 10]
    )[0]

    return {
        "household_id": household_id,
        "name": "",  # assigned later
        "advisor_id": advisor_id,
        "aum": aum,
        "firm_tenure_years": firm_tenure,
        "advisor_tenure_years": adv_tenure,
        "acquisition_origin": origin,
        "service_lines": services,
        "firm_contacts_count": contacts,
        "portal_logins_monthly": portal,
        "communication_exclusivity_pct": comm_excl,
        "fee_percentile": fee,
        "perf_vs_benchmark_pct": perf,
        "service_complaints_12mo": complaints,
        "net_flow_pct": net_flow,
        "satisfaction_score": sat,
    }


def _high_follow_household(household_id: str, advisor_id: str,
                           advisor_tenure: float) -> dict:
    """Generate a household biased toward High follow likelihood.

    Models clients who came with the advisor's acquired book:
    tenure ratio near 1.0, advisor_book origin, narrow services,
    few firm contacts, low portal use, high comm exclusivity.
    """
    if random.random() < 0.05:
        aum = round(random.uniform(15_000_000, 40_000_000), -4)
    else:
        aum = round(random.uniform(1_000_000, 15_000_000), -4)

    # Tenure ratio near 1.0 — client arrived with the advisor
    firm_tenure = round(random.uniform(
        max(1.5, advisor_tenure * 0.7),
        max(advisor_tenure * 1.1, advisor_tenure + 1)
    ), 1)
    # Advisor tenure ≈ firm tenure (came in together)
    adv_tenure = round(random.uniform(
        firm_tenure * 0.85,
        min(firm_tenure, advisor_tenure)
    ), 1)
    adv_tenure = max(0.5, min(adv_tenure, firm_tenure))

    origin = "advisor_book"
    n_services = random.choices([1, 2], weights=[65, 35])[0]
    services = random.sample(SERVICE_LINES, n_services)
    contacts = random.choices([0, 1], weights=[60, 40])[0]
    portal = round(max(0, random.gauss(1.5, 1.5)), 1)
    comm_excl = round(random.uniform(70, 95), 0)
    fee = random.randint(15, 85)
    perf = round(random.gauss(0.5, 3), 1)
    perf = max(-8, min(8, perf))
    complaints = random.choices([0, 1, 2], weights=[70, 20, 10])[0]
    net_flow = round(random.gauss(0, 4), 1)
    net_flow = max(-15, min(10, net_flow))
    sat = random.choices(
        [None, 5, 6, 7, 8, 9, 10],
        weights=[8, 3, 5, 12, 28, 30, 14]
    )[0]

    return {
        "household_id": household_id,
        "name": "",
        "advisor_id": advisor_id,
        "aum": aum,
        "firm_tenure_years": firm_tenure,
        "advisor_tenure_years": adv_tenure,
        "acquisition_origin": origin,
        "service_lines": services,
        "firm_contacts_count": contacts,
        "portal_logins_monthly": portal,
        "communication_exclusivity_pct": comm_excl,
        "fee_percentile": fee,
        "perf_vs_benchmark_pct": perf,
        "service_complaints_12mo": complaints,
        "net_flow_pct": net_flow,
        "satisfaction_score": sat,
    }


def _low_follow_household(household_id: str, advisor_id: str,
                          advisor_tenure: float) -> dict:
    """Generate a household biased toward Low follow likelihood.

    Models firm-originated clients with deep service adoption,
    multiple firm contacts, high portal use, low comm exclusivity.
    """
    if random.random() < 0.05:
        aum = round(random.uniform(15_000_000, 40_000_000), -4)
    else:
        aum = round(random.uniform(1_000_000, 15_000_000), -4)

    # Long firm tenure, short advisor tenure → low ratio
    firm_tenure = round(random.uniform(6, 20), 1)
    adv_tenure = round(random.uniform(
        0.5, min(firm_tenure * 0.4, advisor_tenure)
    ), 1)
    adv_tenure = max(0.5, adv_tenure)

    origin = "firm_originated"
    n_services = random.choices([3, 4, 5], weights=[30, 40, 30])[0]
    services = random.sample(SERVICE_LINES, n_services)
    contacts = random.choices([2, 3, 4, 5], weights=[20, 35, 30, 15])[0]
    portal = round(max(2, random.gauss(10, 4)), 1)
    comm_excl = round(random.uniform(10, 40), 0)
    fee = random.randint(10, 95)
    perf = round(random.gauss(0.5, 3), 1)
    perf = max(-8, min(8, perf))
    complaints = random.choices([0, 1, 2, 3, 4],
                                 weights=[55, 20, 12, 8, 5])[0]
    net_flow = round(random.gauss(0, 5), 1)
    net_flow = max(-20, min(15, net_flow))
    sat = random.choices(
        [None, 3, 4, 5, 6, 7, 8, 9, 10],
        weights=[10, 2, 3, 5, 8, 15, 25, 22, 10]
    )[0]

    return {
        "household_id": household_id,
        "name": "",
        "advisor_id": advisor_id,
        "aum": aum,
        "firm_tenure_years": firm_tenure,
        "advisor_tenure_years": adv_tenure,
        "acquisition_origin": origin,
        "service_lines": services,
        "firm_contacts_count": contacts,
        "portal_logins_monthly": portal,
        "communication_exclusivity_pct": comm_excl,
        "fee_percentile": fee,
        "perf_vs_benchmark_pct": perf,
        "service_complaints_12mo": complaints,
        "net_flow_pct": net_flow,
        "satisfaction_score": sat,
    }


# ---------------------------------------------------------------------------
# Transition plan generation for departed advisor
# ---------------------------------------------------------------------------

def _generate_transition_entries(households: list[dict],
                                  advisor_id: str) -> list[dict]:
    """Generate transition plan entries for a departed advisor's households."""
    statuses = ["retained", "contacted", "scheduled", "not_started", "lost"]
    weights = [30, 20, 15, 15, 20]

    entries = []
    for hh in households:
        status = random.choices(statuses, weights=weights)[0]

        last_contact = None
        if status in ("retained", "contacted", "scheduled"):
            days_ago = random.randint(1, 60)
            month = 7 if days_ago <= 31 else 6
            day = max(1, min(28, (31 - days_ago) if days_ago <= 31 else (61 - days_ago)))
            last_contact = f"2026-{month:02d}-{day:02d}"

        if status == "not_started":
            next_action = "Schedule intro call with new advisor"
        elif status == "scheduled":
            next_action = random.choice([
                "Attend scheduled intro meeting",
                "Prepare portfolio review for meeting",
            ])
        elif status == "contacted":
            next_action = random.choice([
                "Follow up after initial outreach",
                "Schedule in-person review",
                "Send portfolio transition summary",
            ])
        elif status == "retained":
            next_action = "Schedule next quarterly review"
        else:
            next_action = "Document departure reason"

        entries.append({
            "household_id": hh["household_id"],
            "advisor_id": advisor_id,
            "status": status,
            "assigned_to": random.choice(COVERING_ADVISORS),
            "last_contact_date": last_contact,
            "next_action": next_action,
            "follow_likelihood_band": hh.get("follow_likelihood_band", ""),
            "baseline_risk_band": hh.get("baseline_risk_band", ""),
        })

    return entries


# ---------------------------------------------------------------------------
# Guarantee: every advisor has at least one High-follow household
# ---------------------------------------------------------------------------

MIN_CONCENTRATION_PCT = 8.0  # No advisor below this


def _ensure_min_concentration(advisor: dict, book: list[dict]) -> list[dict]:
    """Ensure the advisor's book has enough High-follow households to meet
    the minimum concentration threshold. Replaces the lowest-AUM non-High
    households with high-follow ones until the threshold is met."""
    if not book:
        return book

    total_aum = sum(h["aum"] for h in book)
    high_aum = sum(h["aum"] for h in book
                   if h.get("follow_likelihood_band") == "High")

    if total_aum == 0:
        return book

    current_conc = high_aum / total_aum * 100

    # Keep replacing until we hit the floor
    max_replacements = 5  # safety cap
    replacements = 0
    while current_conc < MIN_CONCENTRATION_PCT and replacements < max_replacements:
        # Find lowest-AUM non-High, non-designed household to replace
        candidates = sorted(
            [h for h in book
             if h.get("follow_likelihood_band") != "High"
             and not h["household_id"].startswith("HH-")
             or (h.get("follow_likelihood_band") != "High"
                 and h["household_id"].startswith("HH-"))],
            key=lambda h: h["aum"]
        )
        # Exclude designed cases
        candidates = [h for h in candidates
                      if h["household_id"] not in (
                          "HH-PATERSON", "HH-NAKAMURA",
                          "HH-BRENNAN", "HH-DOMINGO")]
        if not candidates:
            break

        target = candidates[0]
        replacement = _high_follow_household(
            target["household_id"], advisor["advisor_id"],
            advisor["tenure_years"]
        )
        replacement["name"] = target["name"]

        follow_result = score_household_follow(replacement)
        baseline_result = score_household_baseline(replacement)
        replacement.update(follow_result)
        replacement.update(baseline_result)

        idx = book.index(target)
        book[idx] = replacement

        # Recalculate
        total_aum = sum(h["aum"] for h in book)
        high_aum = sum(h["aum"] for h in book
                       if h.get("follow_likelihood_band") == "High")
        current_conc = high_aum / total_aum * 100 if total_aum > 0 else 0
        replacements += 1

    return book


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate() -> dict:
    advisors = []
    all_households = []
    transition_entries = []

    # Shuffled name pool for unique assignment
    available_names = list(FAMILY_NAMES)
    random.shuffle(available_names)
    name_idx = [0]  # mutable counter

    def next_family_name() -> str:
        if name_idx[0] < len(available_names):
            n = available_names[name_idx[0]]
            name_idx[0] += 1
            return n
        # Fallback: shouldn't happen with 1000+ names for ~1000 HH
        name_idx[0] += 1
        return f"Family-{name_idx[0]}"

    # Reserve names used by designed household cases
    designed_names = set()
    for case in HOUSEHOLD_CASES:
        raw = case["input"]["name"]
        clean = raw.replace("The ", "").replace(" Family", "").replace(" Account", "")
        designed_names.add(clean)
    available_names = [n for n in available_names if n not in designed_names]
    random.shuffle(available_names)
    name_idx[0] = 0

    # Track used household names
    used_names = set(designed_names)

    # --- Plant designed advisor cases ---
    designed_advisor_ids = set()
    for case in ADVISOR_CASES:
        adv = dict(case["input"])
        designed_advisor_ids.add(adv["advisor_id"])
        advisors.append(adv)

    # --- Plant contrast advisor (Elevated, low concentration) ---
    advisors.append(dict(CONTRAST_ADVISOR))
    designed_advisor_ids.add("ADV-RUSSO")

    # --- Generate random advisors ---
    # Target distribution for 35 total: ~4 Elevated, ~9 Watch, ~22 Stable
    # We have 4 designed/planted advisors (Webb=Elevated, Chen=Watch,
    # Okafor=Elevated, Russo=Elevated). So from 31 random we want:
    # ~1 more Elevated, ~8 Watch, ~22 Stable
    n_random = 31
    band_targets = (
        ["Elevated"] * 1 +
        ["Watch"] * 8 +
        ["Stable"] * 22
    )
    random.shuffle(band_targets)

    for i in range(n_random):
        target_band = band_targets[i] if i < len(band_targets) else "Stable"
        adv = _random_advisor(f"ADV-{i+1:03d}", target_band=target_band)
        advisors.append(adv)

    # --- Score all advisors ---
    for adv in advisors:
        result = score_advisor(adv)
        adv.update(result)

    # --- Define household counts per advisor ---
    advisor_hh_counts = {}
    for adv in advisors:
        aid = adv["advisor_id"]
        if aid == "ADV-WEBB":
            advisor_hh_counts[aid] = 38  # + 4 designed = 42
        elif aid == "ADV-OKAFOR":
            advisor_hh_counts[aid] = 28
        elif aid == "ADV-CHEN":
            advisor_hh_counts[aid] = 30
        elif aid == "ADV-RUSSO":
            advisor_hh_counts[aid] = 35
        else:
            advisor_hh_counts[aid] = random.randint(18, 38)

    # Scale random advisor counts to hit ~1000 total (minus designed HH)
    designed_hh_count = len(HOUSEHOLD_CASES)  # 4
    fixed_counts = {"ADV-WEBB": 38, "ADV-OKAFOR": 28, "ADV-CHEN": 30, "ADV-RUSSO": 35}
    fixed_total = sum(fixed_counts.values()) + designed_hh_count
    random_aids = [a for a in advisor_hh_counts if a not in fixed_counts]
    random_total = sum(advisor_hh_counts[a] for a in random_aids)
    target_random = 1000 - fixed_total
    if random_total > 0:
        scale = target_random / random_total
        for aid in random_aids:
            advisor_hh_counts[aid] = max(8, round(advisor_hh_counts[aid] * scale))

    # --- Plant designed household cases ---
    for case in HOUSEHOLD_CASES:
        hh = dict(case["input"])
        all_households.append(hh)

    # --- Generate random households ---
    hh_counter = 1
    advisor_books = {adv["advisor_id"]: [] for adv in advisors}

    # Add designed HHs to Webb's book tracker
    for hh in all_households:
        advisor_books[hh["advisor_id"]].append(hh)

    for adv in advisors:
        aid = adv["advisor_id"]
        n = advisor_hh_counts.get(aid, 20)

        # Russo: explicit slot assignment, shuffled so types aren't clumped
        russo_slots = (["hf"] * 7 + ["lf"] * 18 + ["rand"] * 10)
        random.shuffle(russo_slots)

        for j in range(n):
            hh_id = f"HH-{hh_counter:04d}"
            hh_counter += 1

            # Choose generator based on advisor and desired concentration
            if aid == "ADV-WEBB":
                # ~78% high-follow to hit 65-70% concentration
                if random.random() < 0.78:
                    hh = _high_follow_household(hh_id, aid, adv["tenure_years"])
                else:
                    hh = _random_household(hh_id, aid, adv["tenure_years"])
            elif aid == "ADV-RUSSO":
                # Explicit mix: 8 high-follow, 17 low-follow, 10 random
                # out of 35 → targets ~15-20% concentration
                slot = russo_slots[j] if j < len(russo_slots) else "rand"
                if slot == "hf":
                    hh = _high_follow_household(hh_id, aid, adv["tenure_years"])
                elif slot == "lf":
                    hh = _low_follow_household(hh_id, aid, adv["tenure_years"])
                else:
                    hh = _random_household(hh_id, aid, adv["tenure_years"])
            else:
                hh = _random_household(hh_id, aid, adv["tenure_years"])

            # Assign unique name
            family = next_family_name()
            hh["name"] = f"The {family} Family"

            all_households.append(hh)
            advisor_books[aid].append(hh)

    # --- Score all households ---
    for hh in all_households:
        follow_result = score_household_follow(hh)
        baseline_result = score_household_baseline(hh)
        hh.update(follow_result)
        hh.update(baseline_result)

    # --- Ensure every advisor meets minimum concentration floor ---
    for adv in advisors:
        aid = adv["advisor_id"]
        book = advisor_books[aid]
        book = _ensure_min_concentration(adv, book)
        advisor_books[aid] = book

    # --- Compute advisor-level aggregates ---
    for adv in advisors:
        aid = adv["advisor_id"]
        book = advisor_books[aid]
        adv["household_count"] = len(book)
        adv["book_aum"] = sum(h["aum"] for h in book)

        concentration = compute_concentration(book)
        adv["exposed_aum"] = concentration["exposed_aum"]
        adv["concentration_pct"] = concentration["concentration_pct"]
        adv["has_unscored_households"] = concentration["has_unscored_households"]
        adv["unscored_count"] = concentration["unscored_count"]
        adv["unscored_aum"] = concentration["unscored_aum"]

    # --- Generate transition plan for Okafor ---
    okafor_book = advisor_books["ADV-OKAFOR"]
    transition_entries = _generate_transition_entries(okafor_book, "ADV-OKAFOR")

    # --- Build evaluation cases ---
    from evaluation import run_evaluation
    evaluation_cases = run_evaluation()

    # Flatten household list from books (designed HHs are already in advisor_books)
    final_households = []
    seen_hh_ids = set()
    for adv in advisors:
        for hh in advisor_books[adv["advisor_id"]]:
            if hh["household_id"] not in seen_hh_ids:
                final_households.append(hh)
                seen_hh_ids.add(hh["household_id"])

    data = {
        "metadata": {
            "generated": "2026-08-04",
            "description": "Synthetic data for advisor transition risk demo. "
                           "No real clients or advisors are represented.",
            "advisor_count": len(advisors),
            "household_count": len(final_households),
        },
        "advisors": advisors,
        "households": final_households,
        "transition_entries": transition_entries,
        "evaluation_cases": evaluation_cases,
    }

    return data


def main():
    data = generate()

    output_path = Path(__file__).parent / "output" / "data.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nGenerated:")
    print(f"  Advisors: {data['metadata']['advisor_count']}")
    print(f"  Households: {data['metadata']['household_count']}")
    print(f"  Transition entries: {len(data['transition_entries'])}")
    print(f"  Evaluation cases: {len(data['evaluation_cases'])}")

    # Band distribution
    bands = {}
    for adv in data["advisors"]:
        b = adv["flight_risk_band"]
        bands[b] = bands.get(b, 0) + 1
    print(f"\n  Advisor risk bands: {bands}")

    # Concentration by band
    print(f"\n  Concentration by advisor (sorted by band, then concentration):")
    sorted_advisors = sorted(
        data["advisors"],
        key=lambda a: (
            {"Elevated": 0, "Watch": 1, "Stable": 2}[a["flight_risk_band"]],
            -a["concentration_pct"]
        )
    )
    for adv in sorted_advisors:
        flag = ""
        if adv["advisor_id"] in ("ADV-WEBB", "ADV-RUSSO", "ADV-CHEN", "ADV-OKAFOR"):
            flag = " *designed*"
        unscored = ""
        if adv["has_unscored_households"]:
            unscored = f" ({adv['unscored_count']} unscored)"
        print(f"    {adv['flight_risk_band']:>8s}  "
              f"conc={adv['concentration_pct']:5.1f}%  "
              f"score={adv['flight_risk_score']:2d}  "
              f"{adv['name']:<25s}"
              f"  ${adv['book_aum']/1e6:.0f}M  "
              f"{adv['household_count']} HH"
              f"{unscored}{flag}")

    # Evaluation
    passed = sum(1 for c in data["evaluation_cases"] if c["pass"])
    total = len(data["evaluation_cases"])
    print(f"\n  Evaluation: {passed}/{total} passing")
    print(f"\n  Output: {output_path}")


if __name__ == "__main__":
    main()
