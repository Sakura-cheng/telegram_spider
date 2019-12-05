package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.Authorization;

import java.util.List;

public interface AuthorizationService {
    List<Authorization> findByUserId(Integer userId);
}
