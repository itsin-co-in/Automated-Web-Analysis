package com.client;

import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
public class KafkaConfig {

    @KafkaListener(topics = "#{'${spring.kafka.consumer.topics}'.split(',')}" )
    public void listen(String message){
        System.out.println("Match Details:\n" + message);
    }
}
