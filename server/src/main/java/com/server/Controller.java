package com.server;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/nba")
public class Controller {

    @Autowired
    private KafkaProducer kafkaProducer;
    @PostMapping("/matches")
    public ResponseEntity<?> processMatch(@RequestBody Match match){

        if (! this.kafkaProducer.sendTopicMessage("nba"+match.getTeam1(),match.toString())) {
            System.out.println("Error: message not sent");
        }
        if (! this.kafkaProducer.sendTopicMessage("nba"+match.getTeam2(),match.toString())) {
            System.out.println("Error: message not sent");
        }
      return ResponseEntity.ok().build();
    }



}
