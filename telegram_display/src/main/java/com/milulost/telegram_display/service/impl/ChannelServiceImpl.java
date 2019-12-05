package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Channel;
import com.milulost.telegram_display.mapper.ChannelMapper;
import com.milulost.telegram_display.service.ChannelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChannelServiceImpl implements ChannelService {
    @Autowired
    private ChannelMapper channelMapper;

    @Override
    public List<Channel> findAllByUserId(Integer userId) {
        return channelMapper.findAllByUserId(userId);
    }

    @Override
    public List<Integer> findUserByChannelId(Integer channelId) {
        return channelMapper.findUserByChannelId(channelId);
    }
}
