package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.Phone;

import java.util.List;

public interface PhoneService {
    List<Phone> findAll();

    void insert(Phone phone);

    void delete(String phone);

    List<Phone> findPhoneByPage(Integer start, Integer limit);
}
