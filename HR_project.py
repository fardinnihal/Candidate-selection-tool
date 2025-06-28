import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load data
df = pd.read_excel('restaurant_applicants.xlsx')

# Filter out disqualified roles
disqualified_roles = ["kitchen hand", "waiter"]
df = df[~df['Role'].str.lower().isin(disqualified_roles)]

# Define priority mappings
priority_1 = ["nandos", "mcdonalds", "kfc", "guzman-y-gomez", "hungry jacks", "sushi hub"]
priority_2 = ["subway", "zambrero", "dominos", "nene chicken", "noodle bar"]

def compute_score(row):
    # Workplace priority
    workplace = row['Previous Workplace'].strip().lower()
    if workplace in [r.lower() for r in priority_1]:
        wp = 3
    elif workplace in [r.lower() for r in priority_2]:
        wp = 2
    else:
        wp = 1

    # Role priority
    role = row['Role'].strip().lower()
    if role in ["front of house", "foh", "customer service", "back of house"]:
        rp = 3
    else:
        rp = 1

    # Age (less is better)
    age_score = 50 - row['Age']  # example normalization
    exp = row['Experience']

    return wp * 5 + rp * 4 + age_score * 3 + exp * 2

# Create a target score
df['score'] = df.apply(compute_score, axis=1)

# Define features and target
X = df[['Previous Workplace', 'Age', 'Experience', 'Role']]
y = df['score']

# Preprocessing for categorical data
categorical_features = ['Previous Workplace', 'Role']
numeric_features = ['Age', 'Experience']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'  # keep Age, Experience
)

# Pipeline with regression
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train model
model.fit(X, y)

# Predict scores
df['predicted_score'] = model.predict(X)

# Pick best applicant
best_applicant = df.loc[df['predicted_score'].idxmax()]
print(f"The person selected for interview is {best_applicant['Name']}")
