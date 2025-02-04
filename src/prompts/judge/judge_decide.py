prompt = """
    Decide which plot description resembles the one below more and is more accurate to the plot image provided. In order to choose essay you need
    to answer with word: <FIRST> (indicating the first one is better) or <SECOND> (indicating the second is better).

    Here is the golden standard essay you ought to compare to:
    {golden_title}
    {golden_essay}

    <FIRST>
    {standard_essay}

    <SECOND>
    {fine_tuned_essay}
"""