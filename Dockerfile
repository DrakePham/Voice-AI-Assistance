# Start by pulling the Python image
FROM python:3.9.6

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pulseaudio \
    portaudio19-dev \
    mpg123 \
    alsa-utils \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install mpg123 -y
RUN apt-get install wget -y

# Set the PulseAudio server environment variable
# You can set this directly if you know the value for your system
ENV PULSE_SERVER=host.docker.internal

# Set the ALSA default configuration to use a null device (silences audio output)
RUN echo "pcm.!default { type plug slave.pcm 'null' }" > /root/.asoundrc

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Switch working directory
WORKDIR /app

# Install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy every content from the local file to the image
COPY . /app

# Expose the necessary port if your app needs it (optional)
# EXPOSE 5000

# Configure the container to run in an executed manner
ENTRYPOINT ["python"]

# Command to run your application
CMD ["app.py"]
