#!/bin/zsh

PORT=8000

# Kill any process using the port
PIDS=$(lsof -i :$PORT | awk 'NR != 1 {print $2}' | sort -u)

if [[ -z "$PIDS" ]]; then
  echo "No process found using port $PORT."
else
  echo "Killing processes on port $PORT: $PIDS"
  echo "$PIDS" | xargs kill -9
  echo "Done."
fi

# Make migrations (detect changes and create migration files if needed)
python3 manage.py makemigrations

# Apply migrations to the database
python3 manage.py migrate

# Start the Django development server
python3 manage.py runserver
