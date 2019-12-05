package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.Channel;

import java.util.List;

public interface ChannelService {
    List<Channel> findAllByUserId(Integer userId);

    List<Integer> findUserByChannelId(Integer channelId);
}
