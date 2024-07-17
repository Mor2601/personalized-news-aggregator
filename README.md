
# Personalized News Update Aggregator

## Introduction

The project aims to develop a microservice-based application that aggregates news and technology updates based on user preferences. The system will fetch the latest news, pick up the most interesting news using AI based on user preferences (optionally generate concise summaries using AI), and send this information to users via email, Telegram, or other communication channels.

## Features

### User Registration and Preferences
- **Set Preferences:** Users can set their preferences for news categories and technology updates.
- **Update Preferences:** Users can update their preferences at any time.

### News Aggregation
- **Fetch Latest News:** The application fetches the latest news based on user preferences.
- **AI-Based Selection:** Picks the most interesting news using AI.
- **Communication Channels:** Sends news via the user's preferred communication channel (email, Telegram, etc.).
- **Optional AI Summaries:** Optionally generates concise summaries using AI before sending the news.

## Technology

### Microservices
- The application is designed using microservice architecture, ensuring each service is independent and scalable.

### Containerization
- **Docker:** Each service is containerized for consistency and portability.
- **Docker Compose:** Used to manage multi-container Docker applications and define service dependencies.

### Communication
- **Dapr:** Distributed application runtime for service-to-service communication and message queues, facilitating reliable communication between services.

### API Documentation and Testing
- **Swagger/Postman:** API documentation and testing tools are used to ensure the APIs are well-documented and testable.

### AI Integration
- AI is used to select the most interesting news and optionally generate concise summaries.

## Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mor2601/personalized-news-aggregator.git
   cd personalized-news-aggregator
   ```

2. **Ensure Docker and Docker Compose are installed.**

3. **Run Docker Compose to start the application:**
   ```bash
   docker-compose up --build
   ```
   
4. **Access the services and test endpoints:**
   - Use Postman collection provided in the repository to test the API endpoints.

## Testing the Application


- **Postman Collection:** Import the Postman collection provided in the repository to test the endpoints.



