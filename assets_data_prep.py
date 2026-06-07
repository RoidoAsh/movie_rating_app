import ast
import re
import numpy as np
import pandas as pd

# Top 10 most common genres
TOP_GENRES = ['Drama', 'Comedy', 'Documentary', 'Romance', 'Action',
              'Crime', 'Thriller', 'Horror', 'Adventure', 'Mystery']


def parse_genres(value):
    if pd.isna(value):
        return []
    s = str(value).strip()
    if s.startswith('['):
        try:
            result = ast.literal_eval(s)
            if isinstance(result, list):
                return [str(g).strip() for g in result]
        except (ValueError, SyntaxError):
            s = s.strip('[]').replace("'", "").replace('"', '')
    return [g.strip() for g in s.split(',') if g.strip()]


def parse_budget(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        result = float(value)
    else:
        s = str(value).strip()
        if not s:
            return np.nan
        try:
            result = float(s)
        except ValueError:
            s_clean = s.replace(',', '').replace(' ', ' ')
            s_clean = re.sub(r'\(.*?\)', '', s_clean)
            s_clean = s_clean.replace('est.', '').strip()
            s_lower = s_clean.lower()

            range_match = re.search(r'(\d+\.?\d*)\s*[–\-]\s*(\d+\.?\d*)', s_clean)
            if range_match:
                num = (float(range_match.group(1)) + float(range_match.group(2))) / 2
            else:
                num_match = re.search(r'(\d+\.?\d*)', s_clean)
                if num_match is None:
                    return np.nan
                num = float(num_match.group(1))

            USD_PER_INR_CRORE = 0.12
            USD_PER_GBP = 1.27
            USD_PER_AUD = 0.67
            USD_PER_EUR = 1.07

            if '₹' in s_clean or 'inr' in s_lower or 'rupee' in s_lower:
                if 'crore' in s_lower:
                    result = num * USD_PER_INR_CRORE
                elif 'lakh' in s_lower:
                    result = num * USD_PER_INR_CRORE / 100
                else:
                    result = num * 0.012 / 1e6
            elif '£' in s_clean or 'gbp' in s_lower:
                result = num * USD_PER_GBP if 'million' in s_lower else num * USD_PER_GBP / 1e6
            elif 'a$' in s_lower or 'aud' in s_lower:
                result = num * USD_PER_AUD if 'million' in s_lower else num * USD_PER_AUD / 1e6
            elif '€' in s_clean or 'eur' in s_lower:
                result = num * USD_PER_EUR if 'million' in s_lower else num * USD_PER_EUR / 1e6
            elif '$' in s_clean or 'usd' in s_lower:
                if 'million' in s_lower:
                    result = num
                elif 'billion' in s_lower:
                    result = num * 1000
                else:
                    result = num / 1e6
            elif 'million' in s_lower:
                result = num
            elif 'billion' in s_lower:
                result = num * 1000
            else:
                result = num

    if result > 1000:
        result = result / 1e6
    if result > 500:
        return np.nan
    if result <= 0:
        return np.nan
    return result


def parse_num_actors(value):
    if pd.isna(value):
        return 0
    s = str(value).strip()
    if not s:
        return 0
    if s.startswith('['):
        try:
            result = ast.literal_eval(s)
            if isinstance(result, list):
                return len(result)
        except (ValueError, SyntaxError):
            pass
    nm_codes = re.findall(r'nm\d+', s)
    return len(nm_codes)


def prepare_data(df):
    df = df.copy()

    if 'tconst' in df.columns:
        df = df.set_index('tconst')

    leakage_cols = ['averageRating', 'numVotes', 'BoxOffice']
    for col in leakage_cols:
        if col in df.columns:
            df = df.drop(columns=col)

    if 'startYear' in df.columns:
        df['startYear'] = df['startYear'].replace(0, np.nan)

    if 'budget' in df.columns:
        budget_clean = df['budget'].apply(parse_budget)
        df['has_budget'] = budget_clean.notna().astype(int)
        df['log_budget'] = np.log1p(budget_clean)
        df = df.drop(columns='budget')

    if 'genres' in df.columns:
        genres_list = df['genres'].apply(parse_genres)
        df['genre_count'] = genres_list.apply(len)
        for g in TOP_GENRES:
            col_name = f'genre_{g.lower()}'
            df[col_name] = genres_list.apply(lambda x: int(g in x))
        df = df.drop(columns='genres')

    if 'lead_actors_ids' in df.columns:
        df['num_actors'] = df['lead_actors_ids'].apply(parse_num_actors)
        df = df.drop(columns='lead_actors_ids')

    if 'plot' in df.columns:
        df['has_plot'] = df['plot'].notna().astype(int)
        df = df.drop(columns='plot')

    if 'Country' in df.columns:
        df['is_usa'] = df['Country'].apply(
            lambda x: 1 if pd.notna(x) and 'United States' in str(x) else 0
        )
        df['has_country'] = df['Country'].notna().astype(int)
        df = df.drop(columns='Country')

    if 'Language' in df.columns:
        df['is_english'] = df['Language'].apply(
            lambda x: 1 if pd.notna(x) and 'English' in str(x) else 0
        )
        df['has_language'] = df['Language'].notna().astype(int)
        df = df.drop(columns='Language')

    if 'primaryTitle' in df.columns:
        df['title_length'] = df['primaryTitle'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) else 0
        )
        df = df.drop(columns='primaryTitle')

    if 'startYear' in df.columns:
        df['decade'] = (df['startYear'] // 10 * 10)

    return df
