package com.milulost.telegram_display.service.impl;

import com.milulost.telegram_display.bean.Group;
import com.milulost.telegram_display.mapper.GroupMapper;
import com.milulost.telegram_display.service.GroupService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GroupServiceImpl implements GroupService {
    @Autowired
    private GroupMapper groupMapper;

    @Override
    public List<Group> findAllByUserId(Integer userId) {
        return groupMapper.findAllByUserId(userId);
    }

    @Override
    public List<Integer> findUserByGroupId(Integer groupId) {
        return groupMapper.findUserByGroupId(groupId);
    }
}
