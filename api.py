from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import joblib
import os

from assets_data_prep import prepare_data

app = Flask(__name__)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'trained_model.pkl')
model = joblib.load(MODEL_PATH)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required numeric fields
        for field in ['startYear', 'runtimeMinutes']:
            if field not in data or str(data[field]).strip() == '':
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            start_year = float(data['startYear'])
            runtime = float(data['runtimeMinutes'])
        except (ValueError, TypeError):
            return jsonify({'error': 'startYear and runtimeMinutes must be numbers'}), 400

        # Genres: frontend sends a list of selected genres
        genres = data.get('genres', [])
        if isinstance(genres, list):
            genres_str = ','.join(genres) if genres else np.nan
        else:
            genres_str = genres if genres else np.nan

        # num_actors: frontend sends a number (0-5)
        try:
            num_actors = int(data.get('num_actors', 0))
        except (ValueError, TypeError):
            return jsonify({'error': 'num_actors must be a number'}), 400
        fake_actors = str([f'nm{str(i).zfill(7)}' for i in range(num_actors)])

        # plot: frontend sends 1 (has plot) or 0 (no plot)
        has_plot = str(data.get('has_plot', '0'))
        plot_val = 'yes' if has_plot == '1' else np.nan

        # Optional string fields — empty string treated as missing
        budget   = data.get('budget', '')   or np.nan
        country  = data.get('country', '')  or np.nan
        language = data.get('language', '') or np.nan
        title    = data.get('primaryTitle', '') or np.nan

        # Build single-row DataFrame with raw columns
        row = {
            'startYear':       start_year,
            'runtimeMinutes':  runtime,
            'budget':          budget,
            'genres':          genres_str,
            'lead_actors_ids': fake_actors,
            'plot':            plot_val,
            'Country':         country,
            'Language':        language,
            'primaryTitle':    title,
        }
        df = pd.DataFrame([row])

        # Feature engineering (same as training)
        df_prepared = prepare_data(df)

        # Predict
        prediction = model.predict(df_prepared)[0]
        prediction = round(float(prediction), 1)

        return jsonify({'predicted_rating': prediction})

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
