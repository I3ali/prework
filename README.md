**Prework Assignment - Flask App with Redis, MongoDB, and Nginx**

**Overview**
This project is a simple Flask application integrated with Redis and MongoDB, deployed using Docker Swarm. It features an Nginx reverse proxy and security measures to handle rate limiting and secure sensitive data.

**Setup**

creating the virtual env:
```
python3 -m venv venv
```
*activating the virtual env*
```
source venv/bin/activate
```
installing dependencies
```
pip install -r requirements.txt
```

running the tests:
pytest

##This project utilizes Docker Swarm for scalable deployment. 
Below are the essential commands to build, deploy, and monitor the application within the Swarm.
Services were defined in the docker-compose.yml file, which included:
- Flask App (web service): Running the Flask application.
- Redis: Used for caching and quick data access.
- Nginx: Acting as a reverse proxy with load balancing.

Initialized Docker Swarm on the local machine with the command
```
docker swarm init
```
### Build the Docker Image
```
docker build -t prework-flask-app .
```
This command builds the Docker image for the Flask application and tags it as prework-flask-app.

### Deploy the Stack:
```
docker stack deploy -c docker-compose.yml prework_stack
```
Deploys the services defined in docker-compose.yml to Docker Swarm as a stack named prework_stack.

### View Service Logs:
```
docker service logs prework_stack_web -f
```
Streams real-time logs from the prework_stack_web service.

### Inspect Service Details:
```
docker service inspect --pretty prework_stack_web
```
Provides detailed information about the prework_stack_web service, including its replicas, networks, and current status.

## Security Configuration

This application is secured by routing all traffic through Nginx, which acts as a reverse proxy. The application's internal ports are not exposed directly, ensuring that it can only be accessed via Nginx on port 80.

### Nginx Configuration Highlights:
- **Rate Limiting:** A rate limit is set at 20 requests per second per IP address to mitigate denial-of-service (DoS) attacks. If requests exceed this rate, they are delayed or dropped.
- **Proxy Setup:** Nginx forwards requests to the Flask app running on port 8000 within the Docker network, preserving important headers such as `X-Real-IP` and `X-Forwarded-For`.

This setup enhances security by preventing direct access to the Flask application, ensuring that all traffic is funneled through Nginx, where it can be monitored and controlled.

## Rolling Updates
Docker Swarm is configured for rolling updates, ensuring that the application can be updated with minimal downtime. The stack deploys multiple replicas, and updates are handled by deploying new instances before terminating the old ones.


## Intent Checks

This project includes several checks to ensure code quality, security, and correctness.

### Flake8 Check
- **Action:** Runs `flake8` to lint the codebase.
- **Outcome:** Identifies and reports any style violations, ensuring that the code adheres to PEP 8 standards.

### Black Check
- **Action:** Runs `black --check` to verify code formatting.
- **Outcome:** Detects and reports any formatting issues, ensuring that the code is consistently formatted.

### Bandit Check
- **Action:** Runs `bandit -r` to scan the codebase for security issues.
- **Outcome:** Reports potential security vulnerabilities, helping to keep the code secure.

### Mypy Check
- **Action:** Runs `mypy` to check for type errors.
- **Outcome:** Identifies type-related issues, ensuring that the code adheres to its type annotations.

## Git & Branching Strategy:

### Master Branch
Represents the production-ready code. Only stable releases are merged here.
### Development Branch (Dev):
Active development happens here. Feature and bug branches are merged into dev after testing.
### Feature/Bug Branches
These branches are created from dev for specific features or bug fixes. They are merged back into dev once complete and tested.

**Versioning Strategy:**
  - **Development Branch (Dev):** 
    - The version includes a `-dev` suffix and is automatically incremented with each push to the `dev` branch. 
    - This allows for continuous integration and testing during development without affecting the production version.
  - **Master Branch:** 
    - When merging from `dev` to `master`, the `-dev` suffix is stripped, and the version is incremented for production releases.
    - This ensures that production versions are clean and ready for deployment.

## Known Issues/Limitations
- The rate limiting configuration in Nginx is basic and may need tuning for different traffic patterns.
- MongoDB certificate handling is basic; further security enhancements could be made.
