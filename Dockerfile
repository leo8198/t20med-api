FROM ubuntu:20.04


USER root

WORKDIR /home/root/monolith

# Install necessary packages
COPY requirements.txt requirements.txt

RUN apt-get update

RUN apt-get install curl -y

# Install pip
RUN apt-get install -y python3-pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy all necessary folders and files for the service
COPY . .

# Export the environment variables
RUN export $(grep -v '^#' .env | xargs)

# Change ubuntu timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install tzdata -y
RUN dpkg-reconfigure -f noninteractive tzdata


EXPOSE 80

# Add root permissions to the current user
RUN chown -R $USER:$USER .
RUN chown -R $USER:$USER ..


CMD ["bash", "start.sh"]