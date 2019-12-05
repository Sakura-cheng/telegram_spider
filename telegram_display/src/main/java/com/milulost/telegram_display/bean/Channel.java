package com.milulost.telegram_display.bean;

import java.io.Serializable;

public class Channel implements Serializable {
    private Integer id;
    private Integer user_id;
    private Integer channel_id;
    private String title;
    private String username;
    private Integer participants_count;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUser_id() {
        return user_id;
    }

    public void setUser_id(Integer user_id) {
        this.user_id = user_id;
    }

    public Integer getChannel_id() {
        return channel_id;
    }

    public void setChannel_id(Integer channel_id) {
        this.channel_id = channel_id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Integer getParticipants_count() {
        return participants_count;
    }

    public void setParticipants_count(Integer participants_count) {
        this.participants_count = participants_count;
    }

    @Override
    public String toString() {
        return "Channel{" +
                "id=" + id +
                ", user_id=" + user_id +
                ", channel_id=" + channel_id +
                ", title='" + title + '\'' +
                ", username='" + username + '\'' +
                ", participants_count=" + participants_count +
                '}';
    }
}
