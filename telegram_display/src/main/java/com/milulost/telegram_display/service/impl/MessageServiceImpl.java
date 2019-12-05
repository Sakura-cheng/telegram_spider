package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Message;
import com.milulost.telegram_display.mapper.ChatMapper;
import com.milulost.telegram_display.service.MessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MessageServiceImpl implements MessageService {
    @Autowired
    private ChatMapper chatMapper;

    @Override
    public List<Message> findAll(Integer userId, Integer chatUserId) {
        return chatMapper.findAll(userId, chatUserId);
    }
}
