# Use the official Python 3.12 Bookworm image
FROM python:3.12-bookworm

# Set the working directory inside the container
WORKDIR /workspace

# Copy the requirements file first, to leverage Docker cache
COPY requirements.txt .

# Install dependencies, but only if requirements.txt exists
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the rest of the project files into the container
COPY . .

# Expose port 5000 for web apps (Flask, Django, etc.)
EXPOSE 5000

# Set the default command to run Python
CMD ["python3"]
