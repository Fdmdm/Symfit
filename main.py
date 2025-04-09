import os
import math
import pandas as pd

VIDEO_SETTINGS = {
    'reference_video_dir': 'reference_videos',
    'output_dir': 'output_data',
    'supported_formats': ['.mov', '.mp4', '.avi'],
    'min_frames': 30,
    'max_frames': 1000
}
POSE_SETTINGS = {
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.7,
    'model_complexity': 2,
    'smooth_landmarks': True
}
ANALYSIS_SETTINGS = {
    'technique_weight': 0.6,
    'athletic_weight': 0.4,
    'noise_level': 0.01,
    'min_visibility': 0.5
}
ATHLETIC_METRICS = {
    'features': ['AGE', 'HEIGHT', 'WEIGHT', 'max_speed', 'avg_speed',
                 'Vertical_Jump', 'VO2_Max', 'peak_acceleration', 'Force', 'position'],
    'weights': {
        'AGE': 0.1,
        'HEIGHT': 0.15,
        'WEIGHT': 0.15,
        'max_speed': 0.1,
        'avg_speed': 0.1,
        'Vertical_Jump': 0.1,
        'VO2_Max': 0.1,
        'peak_acceleration': 0.1,
        'Force': 0.1
    }
}
os.makedirs(VIDEO_SETTINGS['reference_video_dir'], exist_ok=True)
os.makedirs(VIDEO_SETTINGS['output_dir'], exist_ok=True)
player = {
    'AGE':23,
    'HEIGHT':180.0,
    'WEIGHT':75.0,
    'max_speed':22.0,
    'avg_speed':27.5,
    'Vertical_Jump':70.0,
    'VO2_Max':50.0,
    'peak_acceleration':5.21,
    'position':'Forward'
}
player['Force'] = player['WEIGHT'] * player['peak_acceleration']
player_position = player['position']
print("Player Athletic Data:")
for key, value in player.items():
    print(f"  {key}: {value}")
PRO_METRICS_FILE = 'Book1.xlsx'
professional_avg = None
keys = ['HEIGHT', 'WEIGHT', 'max_speed', 'avg_speed', 'Vertical_Jump', 'VO2_Max', 'peak_acceleration', 'Force']
if os.path.exists(PRO_METRICS_FILE):
    df = pd.read_excel(PRO_METRICS_FILE)
    filtered = df[df['position'].str.lower() == player_position.lower()]
    if not filtered.empty:
        professional_avg = {k: filtered[k].mean() for k in keys}
    else:
        print(f"No professional data found for position: {player_position}")
else:
    print(f"WARNING: Excel file '{PRO_METRICS_FILE}' not found. Skipping professional athletic data.")
base_value = (
    player['HEIGHT'] * ATHLETIC_METRICS['weights']['HEIGHT'] +
    player['WEIGHT'] * ATHLETIC_METRICS['weights']['WEIGHT'] +
    player['max_speed'] * ATHLETIC_METRICS['weights']['max_speed'] +
    player['avg_speed'] * ATHLETIC_METRICS['weights']['avg_speed'] +
    player['Vertical_Jump'] * ATHLETIC_METRICS['weights']['Vertical_Jump'] +
    player['VO2_Max'] * ATHLETIC_METRICS['weights']['VO2_Max'] +
    player['peak_acceleration'] * ATHLETIC_METRICS['weights']['peak_acceleration'] +
    player['Force'] * ATHLETIC_METRICS['weights']['Force']
)
if player['AGE'] < 25:
    multiplier = 1.5
elif player['AGE'] < 30:
    multiplier = 1.2
else:
    multiplier = 1.0
market_value = base_value * multiplier
print(f"\nEstimated future market value: {market_value:.2f}")
athletic_similarity = None
if professional_avg:
    diff_sum = 0
    for k in keys:
        diff = player[k] - professional_avg[k]
        diff_sum+=diff ** 2
    distance= math.sqrt(diff_sum)
    athletic_similarity = 1 / (1 + distance)
    print(f"Athletic similarity score (to professionals in '{player_position}'): {athletic_similarity:.2f}")
else:
    print("Skipping athletic similarity calculation due to missing data.")

video_similarity = 0.85  # Placeholder score
print(f"Video technique similarity score: {video_similarity:.2f}")
if athletic_similarity is not None:
    overall_similarity = (
        ANALYSIS_SETTINGS['athletic_weight'] * athletic_similarity +
        ANALYSIS_SETTINGS['technique_weight'] * video_similarity
    )
    print(f"\nOverall similarity score (combined): {overall_similarity:.2f}")
else:
    print(f"\nOverall similarity score (technique only): {video_similarity:.2f}")
