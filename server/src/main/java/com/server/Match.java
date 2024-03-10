package com.server;


import org.springframework.stereotype.Component;

import java.io.Serializable;

@Component
public class Match implements Serializable {
    private String team1;
    private String team2;
    private String score1;
    private String score2;

    @Override
    public String toString(){
        return "Team1: "+ team1 + " " + score1 + "\nTeam2: " + team2+ " " + score2;
    }

    public void setTeam1(String team1) {
        this.team1 = team1;
    }

    public void setScore1(String score1) {
        this.score1 = score1;
    }

    public void setScore2(String score2) {
        this.score2 = score2;
    }

    public void setTeam2(String team2) {
        this.team2 = team2;
    }

    public String getTeam1() {
        return team1;
    }

    public String getTeam2() {
        return team2;
    }
}
