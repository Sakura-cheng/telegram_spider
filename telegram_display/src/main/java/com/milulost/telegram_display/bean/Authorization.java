package com.milulost.telegram_display.bean;

import java.io.Serializable;
import java.sql.Date;

public class Authorization implements Serializable {
    private Integer id;
    private Integer user_id;
    private String hash;
    private String device_model;
    private String platform;
    private String system_version;
    private String app_name;
    private String app_version;
    private Date date_created;
    private Date date_active;
    private String ip;
    private String country;
    private String region;
    private Integer official_app;

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

    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public String getDevice_model() {
        return device_model;
    }

    public void setDevice_model(String device_model) {
        this.device_model = device_model;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

    public String getSystem_version() {
        return system_version;
    }

    public void setSystem_version(String system_version) {
        this.system_version = system_version;
    }

    public String getApp_name() {
        return app_name;
    }

    public void setApp_name(String app_name) {
        this.app_name = app_name;
    }

    public String getApp_version() {
        return app_version;
    }

    public void setApp_version(String app_version) {
        this.app_version = app_version;
    }

    public Date getDate_created() {
        return date_created;
    }

    public void setDate_created(Date date_created) {
        this.date_created = date_created;
    }

    public Date getDate_active() {
        return date_active;
    }

    public void setDate_active(Date date_active) {
        this.date_active = date_active;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public Integer getOfficial_app() {
        return official_app;
    }

    public void setOfficial_app(Integer official_app) {
        this.official_app = official_app;
    }

    @Override
    public String toString() {
        return "Authorization{" +
                "id=" + id +
                ", user_id=" + user_id +
                ", hash='" + hash + '\'' +
                ", device_model='" + device_model + '\'' +
                ", platform='" + platform + '\'' +
                ", system_version='" + system_version + '\'' +
                ", app_name='" + app_name + '\'' +
                ", app_version='" + app_version + '\'' +
                ", date_created=" + date_created +
                ", date_active=" + date_active +
                ", ip='" + ip + '\'' +
                ", country='" + country + '\'' +
                ", region='" + region + '\'' +
                ", official_app=" + official_app +
                '}';
    }
}
