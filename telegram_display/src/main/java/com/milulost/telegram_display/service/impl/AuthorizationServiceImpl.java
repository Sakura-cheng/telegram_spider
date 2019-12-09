package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Authorization;
import com.milulost.telegram_display.mapper.AuthorizationMapper;
import com.milulost.telegram_display.service.AuthorizationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AuthorizationServiceImpl implements AuthorizationService {
    @Autowired
    private AuthorizationMapper authorizationMapper;

    @Override
    public List<Authorization> findByUserIdByPage(Integer userId, Integer start, Integer limit) {
        return authorizationMapper.findByUserIdByPage(userId, start, limit);
    }

    @Override
    public List<Authorization> findByUserId(Integer userId) {
        return authorizationMapper.findByUserId(userId);
    }
}
