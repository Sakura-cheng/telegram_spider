package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.Message;

import java.util.List;

public interface MessageService {
    List<Message> findAll(Integer userId, Integer chatUserId);
}
