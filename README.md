# fs-testing-dashboard-client

## Development

1. create .env file in root directory of this repository
  put these variables inside:
      - API_URL=URL to API endpoint (backend URL)
      - NGINX_PORT=Port where NGINX is running
      - CURRENT_IP=IP of machine that is currently running the app. If developing, this should be localhost
2. create venv using "python -m venv venv"
3. activate the venv using "./venv/Scripts/activate"
4. run "pip install -r requirements.txt"
5. run the app using "python app.py"
