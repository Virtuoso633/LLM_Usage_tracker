# import matplotlib
# # Set the backend to 'Agg' before importing pyplot
# matplotlib.use('Agg')

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# from matplotlib import patches
# import pytz
# from datetime import datetime, timezone, timedelta
# import matplotlib.pyplot as plt
# import numpy as np
# import io
# import base64
# # from utils import create_year_heatmap
# from collections import Counter

# app = Flask(__name__)
# # Enable CORS for all domains
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# def create_year_heatmap(convo_times, year):
    
#     # Clear any existing plots
#     plt.clf()
    
#     # Convert convo_times to dates and filter for the given year
#     just_dates = [convo.date() for convo in convo_times if convo.year == year]

#     date_counts = Counter(just_dates)

#     # Create a full year date range for the calendar
#     start_date = datetime(year, 1, 1).date()
#     end_date = datetime(year, 12, 31).date()

#     total_days = (end_date - start_date).days + 1
#     date_range = [start_date + timedelta(days=i) for i in range(total_days)]

#     # Prepare data for plotting
#     data = []
#     for date in date_range:
#         week = ((date - start_date).days + start_date.weekday()) // 7
#         day_of_week = date.weekday()
#         count = date_counts.get(date, 0)
#         data.append((week, day_of_week, count))

#     weeks_in_year = (end_date - start_date).days // 7 + 1

#     # Plot the heatmap
#     fig, ax = plt.subplots(figsize=(15, 8))
#     ax.set_aspect('equal')

#     # Handle the case when there are no conversations
#     if date_counts:
#         max_count_date = max(date_counts, key=date_counts.get)
#         max_count = date_counts[max_count_date]
#         p90_count = np.percentile(list(date_counts.values()), 90)
#     else:
#         max_count_date = start_date
#         max_count = 0
#         p90_count = 1
        
#     for week, day_of_week, count in data:
#         color = plt.cm.Greens((count + 1) / p90_count) if count > 0 else 'lightgray'
#         rect = plt.Rectangle((week, day_of_week), 1, 1, linewidth=0.5, edgecolor='black', facecolor=color)
#         ax.add_patch(rect)

#     # Replace week numbers with month names below the heatmap
#     month_starts = [start_date + timedelta(days=i) for i in range(total_days)
#                     if (start_date + timedelta(days=i)).day == 1]
#     for month_start in month_starts:
#         week = (month_start - start_date).days // 7
#         plt.text(week + 0.5, 7.75, month_start.strftime('%b'), ha='center', va='center', fontsize=10, rotation=0)

#     # Adjustments for readability
#     ax.set_xlim(-0.5, weeks_in_year + 0.5)
#     ax.set_ylim(-0.5, 8.5)
#     plt.title(
#         f'{year} ChatGPT Conversation Heatmap (total={sum(date_counts.values())}).\nMost active day: {max_count_date} with {max_count} convos.',
#         fontsize=16
#     )
#     plt.xticks([])
#     plt.yticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
#     plt.gca().invert_yaxis()
#     # plt.show()
#     img_buffer = io.BytesIO()
#     plt.savefig(img_buffer, format='png', bbox_inches='tight')
#     img_buffer.seek(0)
#     img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
#     # Clean up
#     plt.close(fig)

#     return img_base64

# @app.route('/api/test', methods=['GET'])
# def test():
#     try:
#         return jsonify({
#             "status": "success",
#             "message": "Backend is working!"
#         }), 200
#     except Exception as e:
#         print(f"Error in test endpoint: {str(e)}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500    

# @app.route('/api/generate-heatmap', methods=['POST'])
# def generate_heatmap():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'status': 'error', 'message': 'No file provided'}), 400
            
#         file = request.files['file']
#         timezone_str = request.form.get('timezone', 'UTC')        
        
#         # Print debug information
#         print(f"Received file: {file.filename}")
#         print(f"Timezone: {timezone_str}")
        
#         # Read and process the conversations file
#         conversations = json.load(file)
        
#         # Process timestamps
#         convo_times = []
#         for conv in conversations:
#             unix_timestamp = conv['create_time']
#             # Create UTC datetime from timestamp
#             utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
#             # Convert to specified timezone
#             local_datetime = utc_datetime.astimezone(pytz.timezone(timezone_str))
#             convo_times.append(local_datetime)
        
#         # Generate heatmap
#         current_year = 2024
#         img_base64 = create_year_heatmap(convo_times, current_year)
        
#         return jsonify({
#             'status': 'success',
#             'image': img_base64
#         })
    
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         }), 400

# ## **for vercel add**
# # For Vercel serverless function
# def handler(request):
#     if request.path == '/api/test':
#         return app.view_functions['test']()
#     elif request.path == '/api/generate-heatmap':
#         return app.view_functions['generate_heatmap']()
    



# # **used for local server**
# # if __name__ == '__main__':
# #     print("Starting Flask server...")
# #     app.run(debug=True, port=5000, host='0.0.0.0')
    
    
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "status": "success",
        "message": "Backend is working!",
        "version": "1.0"
    })

# This is required for Vercel
app = app.wsgi_app