# Sports News Tracker
## Overview
iTS objective from this project is to build an application for Website Architecture Analysis Workbook from various sources using Python spiders, Spring Boot server, Kafka, and Java consumer applications. The system architecture involves crawling sports news websites, processing the data, and distributing it to multiple consumer applications for further analysis or display.

## Requirements
1. Java 17
2. scrapy
3. Kafka Server and Zookeeper 

## Components
1. **Python Spiders**
Python spiders are responsible for crawling various sports news websites, such as Google searches.
They extract relevant information such as headlines, articles, and metadata.
This information is sent to the Spring Boot server for further processing.
2. **Spring Boot Server (Java)**
The Spring Boot server receives POST requests from Python spiders containing sports news data.
It processes the received data, which may include validation, normalization, or enrichment.
After processing, the server publishes the information to Kafka topics for distribution.
3. **Kafka**
Kafka acts as a message broker for the system, facilitating communication between the Spring Boot server and Java consumer applications.
It receives sports news data from the Spring Boot server and publishes it to topics.
Topics are consumed by Java consumer applications for further processing.
4. **Java Consumer Applications**
Java consumer applications subscribe to specific Kafka topics.
They consume sports news data published by Kafka in real-time.
Consumer applications may perform additional processing, analysis, or storage of the data.

## Usage
To run the system locally, follow these steps:

* Start Kafka and Zookeeper servers.
```shell
docker run -p 9092:9092 apache/kafka:3.8.0
```

* Run the Spring Boot server.
```shell
cd server
mvn spring-boot:run
```

* Deploy and run the Python spiders to crawl sports news websites.
```shell
cd fetcher/sportscraper
scarpy crawl nbascraper
```
* Launch the Java consumer applications to subscribe to Kafka topics and consume data. We can change the topics in the application.properties file.
```shell
cd client
mvn spring-boot:run
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

