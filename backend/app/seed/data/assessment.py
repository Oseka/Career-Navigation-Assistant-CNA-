"""Career discovery assessment instrument.

Structure per docs/assessment-methodology.md: 9 categories, 3 interest
statements per category, presented interleaved so consecutive questions never
share a category. Every question uses the same 4-point agreement scale.

Seeds are insert-only by natural key (category key; category_id +
question_order). Existing rows are never modified, so admin edits survive
re-runs.
"""

CATEGORIES: list[dict[str, object]] = [
    {
        "key": "software_dev",
        "name": "Software & Application Development",
        "description": "Building software applications, from writing code to shipping features.",
        "display_order": 1,
    },
    {
        "key": "ai_ml",
        "name": "Artificial Intelligence & Machine Learning",
        "description": "Machine learning, model building, and applied artificial intelligence.",
        "display_order": 2,
    },
    {
        "key": "data_analysis",
        "name": "Data Analysis & Data Science",
        "description": "Working with data, statistics, and visualisation to answer questions.",
        "display_order": 3,
    },
    {
        "key": "cloud",
        "name": "Cloud Computing & Infrastructure",
        "description": "Cloud platforms, infrastructure provisioning, and scalable deployment.",
        "display_order": 4,
    },
    {
        "key": "security",
        "name": "Cybersecurity",
        "description": "Protecting systems, understanding threats, and defending against attacks.",
        "display_order": 5,
    },
    {
        "key": "networking",
        "name": "Networking & Systems",
        "description": "Networks, servers, operating systems, and connectivity.",
        "display_order": 6,
    },
    {
        "key": "database",
        "name": "Database Management",
        "description": "Designing, querying, and managing structured data stores.",
        "display_order": 7,
    },
    {
        "key": "uiux",
        "name": "UI & UX Design",
        "description": "Interface design, usability, and user research.",
        "display_order": 8,
    },
    {
        "key": "qa",
        "name": "Software Testing & Quality Assurance",
        "description": "Software testing, quality assurance, and defect prevention.",
        "display_order": 9,
    },
]

AGREEMENT_OPTIONS: list[tuple[str, int]] = [
    ("Strongly agree", 3),
    ("Agree", 2),
    ("Disagree", 1),
    ("Strongly disagree", 0),
]

_QUESTIONS_BY_CATEGORY: dict[str, list[str]] = {
    "software_dev": [
        "I enjoy designing and writing programs that solve everyday problems.",
        "I like taking an idea and turning it into a working piece of software.",
        "I get satisfaction from refactoring code so it is cleaner and easier to maintain.",
    ],
    "ai_ml": [
        "I find it exciting to train and evaluate models that learn from data.",
        "I am curious about how artificial intelligence systems make decisions.",
        "I enjoy exploring datasets to discover patterns that could feed into intelligent systems.",
    ],
    "data_analysis": [
        "I enjoy working with datasets to find patterns and answer questions.",
        "I like creating charts and visualisations that make data easy to understand.",
        "I am interested in using statistics to support decisions with evidence.",
    ],
    "cloud": [
        "I am interested in how cloud platforms host and scale applications.",
        "I enjoy provisioning and configuring infrastructure, whether locally or in the cloud.",
        "I like learning how containers and orchestration tools keep services running reliably.",
    ],
    "security": [
        "I enjoy learning how attackers break into systems so I can defend against them.",
        "I am curious about vulnerabilities in software and how they are exploited.",
        "I find satisfaction in hardening systems and responding to security incidents.",
    ],
    "networking": [
        "I like understanding how computers communicate across networks.",
        "I enjoy configuring and troubleshooting servers and network equipment.",
        "I am interested in how large-scale systems stay connected and reliable.",
    ],
    "database": [
        "I enjoy designing database schemas that organise information cleanly.",
        "I like writing queries to extract exactly the information I need.",
        "I am interested in how databases are tuned to perform well at scale.",
    ],
    "uiux": [
        "I enjoy designing interfaces that are clear and pleasant to use.",
        "I like observing how people use software and finding ways to improve their experience.",
        "I care about accessibility and making software usable for everyone.",
    ],
    "qa": [
        "I like systematically trying to break software to find defects before users do.",
        "I enjoy designing test cases that cover both typical and edge-case scenarios.",
        "I find satisfaction in improving software quality through careful review and testing.",
    ],
}


def _interleaved_questions() -> list[tuple[str, str]]:
    return [
        (str(category["key"]), _QUESTIONS_BY_CATEGORY[str(category["key"])][round_index])
        for round_index in range(3)
        for category in CATEGORIES
    ]


QUESTIONS: list[tuple[str, str]] = _interleaved_questions()
