package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.mapper.ContactMapper;
import com.milulost.telegram_display.service.ContactService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ContactServiceImpl implements ContactService {
    @Autowired
    private ContactMapper contactMapper;

    @Override
    public List<Integer> findByUserId(Integer userId) {
        return contactMapper.findByUserId(userId);
    }
}
