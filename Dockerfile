# 1. Use an official lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file FIRST
# (This leverages Docker's cache if dependencies don't change)
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
# (Our .dockerignore file will prevent copying 'venv', etc.)
COPY . .

# 6. Define the command to run when the container starts
CMD ["python", "main.py"]