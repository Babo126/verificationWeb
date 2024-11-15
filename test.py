from flask import Flask, request, redirect, render_template, session, url_for
import requests
import json
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 16 表示生成一個 32 位的十六進位密鑰

# Set your LINE channel details
LINE_CHANNEL_ID = '2006556911'
LINE_CHANNEL_SECRET = '42eb9b2d38b6ab498ee67d9d6ab35b9a'
REDIRECT_URI = 'https://3ee1-140-117-177-209.ngrok-free.app/callback'


# Route to start the login process
@app.route('/temp')
def temp():
    return render_template('temp.html')

# Route to handle LINE Login callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': LINE_CHANNEL_ID,
        'client_secret': LINE_CHANNEL_SECRET
    }
    
    # Request access token
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    access_token = token_info.get('access_token')

    # Get user profile
    if access_token:
        profile_url = 'https://api.line.me/v2/profile'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile = profile_response.json()

        # Pass profile to the verification page
        return render_template('verification.html', profile=profile)

    return "Error in LINE Login"

# Placeholder routes for location and photo verification
@app.route('/verify_location', methods=['POST'])
def verify_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # Add your location verification logic here
    return json.dumps({'success': True})

@app.route('/verify_photo', methods=['POST'])
def verify_photo():
    file = request.files['photo']
    # Add your photo verification logic here
    return json.dumps({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
