package com.milulost.telegram_display.service;

import java.util.List;

public interface ContactService {
    List<Integer> findByUserId(Integer userId);
}
