package com.milulost.telegram_display.bean;

import java.io.Serializable;

public class Group implements Serializable {
    private Integer id;
    private Integer user_id;
    private Integer group_id;
    private String title;
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

    public Integer getGroup_id() {
        return group_id;
    }

    public void setGroup_id(Integer group_id) {
        this.group_id = group_id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Integer getParticipants_count() {
        return participants_count;
    }

    public void setParticipants_count(Integer participants_count) {
        this.participants_count = participants_count;
    }

    @Override
    public String toString() {
        return "Group{" +
                "id=" + id +
                ", user_id=" + user_id +
                ", group_id=" + group_id +
                ", title='" + title + '\'' +
                ", participants_count=" + participants_count +
                '}';
    }
}
