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
REDIS_ENDPOINT=localhost pytest


## **Deployment Strategy**
The deployment strategy leverages Docker Swarm for scalable and resilient deployments. While the current CI/CD pipeline automates testing, version control, and intent checks, it does not yet automatically deploy updates.

### Docker Swarm Overview
Docker Swarm is used to manage and deploy multiple services as a single stack, ensuring scalability and fault tolerance. This setup includes:

- **Flask App (web service):** Running the Flask application.
- **Redis:** Used for caching and quick data access.
- **Nginx:** Acting as a reverse proxy with load balancing.

### Essential Docker Commands
- **Initialize Docker Swarm:**
    ```
    docker swarm init
    ```
- **Build the Docker Image:**
    ```
    docker build -t prework-flask-app .
    ```
    This command builds the Docker image for the Flask application and tags it as `prework-flask-app`.
- **Deploy the Stack:**
    ```
    docker stack deploy -c docker-compose.yml prework_stack
    ```
    Deploys the services defined in `docker-compose.yml` to Docker Swarm as a stack named `prework_stack`.
- **View Service Logs:**
    ```
    docker service logs prework_stack_web -f
    ```
    Streams real-time logs from the `prework_stack_web` service.
- **Inspect Service Details:**
    ```
    docker service inspect --pretty prework_stack_web
    ```
    Provides detailed information about the `prework_stack_web` service, including its replicas, networks, and current status.

### Rolling Updates
Docker Swarm is configured for rolling updates, which ensures minimal downtime during application updates. The stack deploys multiple replicas of services, and updates are handled by deploying new instances before terminating the old ones, ensuring continuous availability.

## **Security Configuration**

This application is secured by routing all traffic through Nginx, which acts as a reverse proxy. The application's internal ports are not exposed directly, ensuring that it can only be accessed via Nginx on port 80.

### Nginx Configuration Highlights:
- **Rate Limiting:** A rate limit is set at 20 requests per second per IP address to mitigate denial-of-service (DoS) attacks. If requests exceed this rate, they are delayed or dropped.
- **Proxy Setup:** Nginx forwards requests to the Flask app running on port 8000 within the Docker network, preserving important headers such as `X-Real-IP` and `X-Forwarded-For`.

This setup enhances security by preventing direct access to the Flask application, ensuring that all traffic is funneled through Nginx, where it can be monitored and controlled.

## **Environment Configuration**

Environment variables are managed through a `.env` file, ensuring that sensitive information like database credentials, API keys, and other secrets are not hardcoded into the application. This file is not included in version control and is securely managed. For even greater security, sensitive information is managed through Docker Swarm secrets, which are securely injected into the running containers without being exposed in the code or Docker images.

## **Dependencies**
The project's dependencies are listed in the `requirements.txt` file, which has been frozen using `pip freeze`. This ensures that all the libraries and their specific versions are consistent across different environments, reducing the chances of compatibility issues.

## **Automated Quality Checks**

Automated tests run as part of the CI/CD pipeline to catch issues early. This project includes several checks to ensure code quality, security, and correctness.

### Flake8 Check
- **Action:** Runs `flake8` to lint the codebase.
- **Outcome:** Identifies and reports any style violations, ensuring that the code adheres to PEP 8 standards.

### Black Check
- **Action:** Runs `black --check` to verify code formatting.
- **Outcome:** Detects and reports any formatting issues, ensuring that the code is consistently formatted.

### Bandit Check
- **Action:** Runs `bandit -r` with a focus on medium and higher severity issues to scan the codebase for security issues.
- **Outcome:** Reports potential security vulnerabilities

### Mypy Check
- **Action:** Runs `mypy` to check for type errors.
- **Outcome:** Identifies type-related issues, ensuring that the code adheres to its type annotations.

## **Git & Branching Strategy**

### Master Branch
Represents the production-ready code. Only stable releases are merged here.

### Development Branch (Dev)
Active development happens here. Feature and bug branches are merged into dev after testing.

### Feature/Bug Branches
These branches are created from dev for specific features or bug fixes. They are merged back into dev once complete and tested.

### Versioning Strategy:
- **Development Branch (Dev):**
  - The version includes a `-dev` suffix and is automatically incremented with each push to the `dev` branch.
  - This allows for continuous integration and testing during development without affecting the production version.
- **Master Branch:**
  - When merging from `dev` to `master`, the `-dev` suffix is stripped, and the version is incremented for production releases.
  - This ensures that production versions are clean and ready for deployment.

## **Storage and Persistence Strategy**

### Current Implementation
The application currently uses Redis for caching and MongoDB for data persistence. Redis is backed by Docker volumes to ensure data persists even after container restarts, providing quick, in-memory storage for the application's state.

### Proposed Future Approach
- **Redis**: Extend its use for session management, token handling, and caching user-specific data to improve application performance.
- **MongoDB**: Implement MongoDB as the primary database for storing user data, application data, and other persistent records. This would be particularly useful for structured data that requires long-term storage and retrieval.
- **Hybrid Approach**: Leverage Redis for fast access to temporary data and MongoDB for long-term data storage. Redis can handle frequent, small transactions (like session tokens), while MongoDB can manage more complex datasets.

## **Fault Tolerance and Resilience**
The application is designed with fault tolerance in mind by deploying multiple replicas via Docker Swarm. However, further resilience could be achieved by implementing automatic failover strategies, where a backup service takes over if the primary service fails. Additionally, using distributed data storage solutions like MongoDB with replication could further safeguard data integrity.

## **Known Issues/Limitations**
- The rate limiting configuration in Nginx is basic and may need tuning for different traffic patterns.
- MongoDB certificate handling is basic; further security enhancements could be made.

## **Development & Debugging**
During development, debugging is made easier by:
- **Exposing Ports:** The Docker Compose file has commented out port mappings, which can be uncommented for easier local development.
- **Debug Mode:** The Flask app's `debug` mode is enabled during development, providing detailed error messages and an interactive debugger.
