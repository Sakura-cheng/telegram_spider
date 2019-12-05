package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.User;

import java.util.List;

public interface UserService {
    List<User> findAll();

    User findUserById(Integer id);
}
