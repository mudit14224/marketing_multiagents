# Use the official Python 3.10 image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Gradio will run on
EXPOSE 7860

# Define the command to run the Gradio app
CMD ["python", "app.py"]
