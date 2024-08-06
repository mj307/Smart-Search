# Smart Search 📚

**Smart Search** is a RAG-based application that lets you quickly find answers to specific questions within the content you're reading, so you don't have to sift through the entire material to find what you're looking for.

## Features
👍 User-Friendly Dashboard: Clear and intuitive interface with easy-to-follow instructions

🗣️ Interactive Chatbox: Ask your questions directly and get instantaneous answers

📈 Comprehensive Results Page: View detailed search results and relevant information in one place

## Getting Started ##

### Prerequisites

- **Docker**: Make sure Docker is installed. You can get it from [here](https://docs.docker.com/get-docker/).
- **Ollama Server**: Make sure the Ollama server is installed as well. You can get it from [here](https://ollama.com/download).


### Setup Instructions

1. **Clone the Repository**
   ```shell
   git clone https://github.com/mj307/Smart-Search.git
   cd Smart-Search
   ```
2. **Build the Docker Image**
   ```shell
   docker build -t smartsearch:v1 .
   ```
3. **Run the Docker Container**
   ```shell
   docker run -d -p 8000:8000 -e PDF='/app/brain.pdf' -e HOST='http://host.docker.internal:11434' smartsearch:v1
   ```
    -d runs the container in detached mode (in the background)
   
   -p 8000:8000 maps port 8000 on your machine to port 8000 in the container. You can adjust this if your application uses a different port.
   
   -e specifies that we are using an env variable (so we aren't hard coding any values). In this case, I'm using the brain.pdf PDF which already exists in my directory (I'm setting PDF='/app/brain.pdf') and I'm specifying the host of the image which is 'http://host.docker.internal:11434'. 


4. **Access the Application**
   
Open a web browser and navigate to http://localhost:8000 or the appropriate URL based on your application configuration.

## Files
**Dockerfile**: Docker configuration file

**index.html, result.html**: HTML files used by the application

**brain.pdf**: PDF file so the application has the context to answer questions

**main.py**: Main Python script

**requirements.txt**: List of Python dependencies


## Troubleshooting
**Docker Build Issues**: If you encounter errors while building the Docker image, ensure that your Dockerfile is correctly configured and that all files listed in it are present

**Port Conflicts**: If port 8000 on your machine is already in use, you can change the port mapping by modifying -p 8000:8000 to a different port, such as -p 8080:8000

**Container Logs**: To check the logs of a running container:
```shell
docker logs <container_id>
```
**Docker Logs**: In the event where your containers aren't able to start up, you can look at your docker logs to see what the issue may be. Navigate here to get to the location of the logs:
```shell
/Library/Containers/com.docker.docker/Data/log/
```

Run this command to see the content of the logs:
```shell
tail -f /Library/Containers/com.docker.docker/Data/log/<log_filename>
```

## Future Iterations
- Currently, my code can only take in files that have been already uploaded in the /app directory as input during the *docker run* portion. In the future, I want to build an upload function in my dashboard so that users can upload any file and have the **Smart Search** analyze that. 
