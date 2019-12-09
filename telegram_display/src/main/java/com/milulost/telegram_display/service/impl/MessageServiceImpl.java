package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Message;
import com.milulost.telegram_display.bean.User;
import com.milulost.telegram_display.mapper.ChatMapper;
import com.milulost.telegram_display.service.MessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class MessageServiceImpl implements MessageService {
    @Autowired
    private ChatMapper chatMapper;

    @Override
    public List<Integer> findChatByUserId(Integer userId) {
        List<Integer> fromIdList = chatMapper.findFromIdByUserId(userId);
        List<Integer> toIdList = chatMapper.findToIdByUserId(userId);
        fromIdList.removeAll(toIdList);
        fromIdList.addAll(toIdList);
        return fromIdList;
    }

    @Override
    public List<Message> findMessageByPage(Integer start, Integer limit, Integer userId, Integer chatUserId) {
        return chatMapper.findMessageByPage(start, limit, userId, chatUserId);
    }

    @Override
    public List<Message> findAll(Integer userId, Integer chatUserId) {
        return chatMapper.findAll(userId, chatUserId);
    }
}
