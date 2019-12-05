package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.User;
import com.milulost.telegram_display.mapper.UserMapper;
import com.milulost.telegram_display.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;

    @Override
    public List<User> findAll() {
        return userMapper.findAll();
    }

    @Override
    public User findUserById(Integer id) {
        return userMapper.findUserById(id);
    }
}
