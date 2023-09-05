from difflib import get_close_matches, SequenceMatcher
import wordninja
import pandas as pd


standard_terms_df = pd.read_csv('../resources/temp/standard_terms.tsv', sep='\t', header=0)
print(standard_terms_df.head())

df = standard_terms_df
# df['DESCRIPTION'] = df.apply(lambda row:", ".join([(val if val[0]=='a' else "["+val+"]") for val in row if not pd.isna(val)]), axis=1)
df['DESCRIPTION'] = df.apply(lambda row: (row['DESCRIPTION'][1:-1] if not pd.isna(row['DESCRIPTION']) else ""), axis=1)

df.to_csv('../resources/stand_terms_1.csv', index=False)

terms = []
for i, row in df.iterrows():
    terms.append({
        "term": row["TERM"],
        "ontology": row["ID"],
        "description": row["DESCRIPTION"]
    })

print(terms)




def get_nearest_mapping(term):
    term2 = ["alcohol usage history", "Tobacco"]
    matches = get_close_matches(term, term2)
    print(matches)
    term2 = "alcohol use history"
    matches = SequenceMatcher(a=term, b=term2).ratio()
    print(matches)


def remove_special(term):
    return term.replace('_', ' ').replace('.', ' ')


def guess_word_boundary(term):
    return ' '.join(wordninja.split(term))


def clean_term(term):
    return guess_word_boundary(remove_special(term))


def clean_terms(terms):
    return [clean_term(term) for term in terms]


get_nearest_mapping("alcohol use hist")
print(wordninja.split("AlcoholUseHistory"))
