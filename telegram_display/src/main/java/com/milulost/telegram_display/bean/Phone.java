package com.milulost.telegram_display.bean;

import java.io.Serializable;

public class Phone implements Serializable {
    private Integer id;
    private String phone;
    private Integer status;
    private Integer category;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }

    public Integer getCategory() {
        return category;
    }

    public void setCategory(Integer category) {
        this.category = category;
    }

    @Override
    public String toString() {
        return "Phone{" +
                "id=" + id +
                ", phone='" + phone + '\'' +
                ", status=" + status +
                ", category=" + category +
                '}';
    }
}
