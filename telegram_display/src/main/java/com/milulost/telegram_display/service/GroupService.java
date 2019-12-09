package com.milulost.telegram_display.service;

import com.milulost.telegram_display.bean.Group;

import java.util.List;

public interface GroupService {
    List<Group> findAllByUserId(Integer userId);

    List<Group> findAllByUserIdByPage(Integer start, Integer limit, Integer userId);

    List<Integer> findUserByGroupId(Integer groupId);

    List<Integer> findUserByGroupIdByPage(Integer start, Integer limit, Integer groupId);
}
