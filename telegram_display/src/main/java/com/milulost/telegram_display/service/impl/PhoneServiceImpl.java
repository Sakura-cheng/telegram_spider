package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Phone;
import com.milulost.telegram_display.mapper.PhoneMapper;
import com.milulost.telegram_display.service.PhoneService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PhoneServiceImpl implements PhoneService {
    @Autowired
    private PhoneMapper phoneMapper;

    @Override
    public List<Phone> findAll() {
        return phoneMapper.findAll();
    }

    @Override
    public void insert(Phone phone) {
        phoneMapper.insert(phone);
    }

    @Override
    public void delete(String phone) {
        phoneMapper.delete(phone);
    }
}
