FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

RUN mkdir /code
RUN mkdir /config

# Install dependencies
RUN apt-get update && apt-get install -y inkscape && apt-get clean
COPY /config/requirements.txt /config/
RUN pip install --no-cache-dir -r /config/requirements.txt

# Copy code
WORKDIR /code
COPY . /code/

# Set working dir
WORKDIR /code/mysite
