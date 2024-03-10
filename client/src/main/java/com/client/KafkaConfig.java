package com.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
public class KafkaConfig {

    public static final String topic = "nbaBucks";
    @KafkaListener(topics = topic)
    public void listen(String message){
        System.out.println("Match Details:\n" + message);
    }
}
