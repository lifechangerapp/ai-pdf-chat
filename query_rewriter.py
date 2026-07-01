import re


REPLACEMENTS = {

    "live": "from",

    "living": "from",

    "residence": "from",

    "resident": "from",

    "qualification": "education",

    "qualified": "education",

    "study": "education",

    "studied": "education"
}


def rewrite_query(question):

    question = question.lower()

    for old, new in REPLACEMENTS.items():

        question = re.sub(
            rf"\b{old}\b",
            new,
            question
        )

    return question