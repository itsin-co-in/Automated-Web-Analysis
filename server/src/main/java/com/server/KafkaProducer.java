package com.server;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaProducer {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    public boolean sendTopicMessage(String topic, String message){
        this.kafkaTemplate.send(topic, message);
        return true;
    }

}
