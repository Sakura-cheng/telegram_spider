package com.milulost.telegram_display.bean;

import java.io.Serializable;
import java.sql.Date;

public class Message implements Serializable {
    private Integer id;
    private Integer user_id;
    private Integer message_id;
    private String message;
    private Date date;
    private Integer from_id;
    private Integer to_id;

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

    public Integer getMessage_id() {
        return message_id;
    }

    public void setMessage_id(Integer message_id) {
        this.message_id = message_id;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Integer getFrom_id() {
        return from_id;
    }

    public void setFrom_id(Integer from_id) {
        this.from_id = from_id;
    }

    public Integer getTo_id() {
        return to_id;
    }

    public void setTo_id(Integer to_id) {
        this.to_id = to_id;
    }

    @Override
    public String toString() {
        return "Message{" +
                "id=" + id +
                ", user_id=" + user_id +
                ", message_id=" + message_id +
                ", message='" + message + '\'' +
                ", date=" + date +
                ", from_id=" + from_id +
                ", to_id=" + to_id +
                '}';
    }
}
