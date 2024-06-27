# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container (optional, if your bot does not serve a web page, you can skip this)
EXPOSE 8000

# Define environment variable
ENV DISCORD_TOKEN=MTI1NDAyMzA0NzcyNDE0MjY0NQ.GsRxun.u8tUb7aY4D_9VrWeGislf3dgbG6P80y-bd7KzE

# Run bot.py when the container launches
CMD ["python", "main.py"]