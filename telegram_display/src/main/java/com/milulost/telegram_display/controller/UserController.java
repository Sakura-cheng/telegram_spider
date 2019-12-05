package com.milulost.telegram_display.controller;

import com.milulost.telegram_display.bean.*;
import com.milulost.telegram_display.service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
public class UserController {
    @Autowired
    private UserService userService;
    @Autowired
    private AuthorizationService authorizationService;
    @Autowired
    private ContactService contactService;
    @Autowired
    private MessageService messageService;
    @Autowired
    private ChannelService channelService;
    @Autowired
    private GroupService groupService;

    @RequestMapping("/users")
    public List<User> findUsers() {
        return userService.findAll();
    }

    /***
     * 根据id查询user详情
     * @param id
     * @return
     */
    @RequestMapping("/user&userId={id}")
    public User findUserById(@PathVariable("id") Integer id) {
        return userService.findUserById(id);
    }

    /***
     * 根据userId查询授权设备
     * @param userId
     * @return
     */
    @RequestMapping("/authorization&userId={userId}")
    public List<Authorization> findAuthorizationByUserId(@PathVariable("userId") Integer userId) {
        return authorizationService.findByUserId(userId);
    }

    /***
     * 根据userId查询联系人详情
     * @param userId
     * @return
     */
    @RequestMapping("/contact&userId={userId}")
    public List<User> findContactByUserId(@PathVariable("userId") Integer userId) {
        List<Integer> userIdList = contactService.findByUserId(userId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return userList;
    }

    @RequestMapping("/message&userId={userId}&chatUserId={chatUserId}")
    public List<Message> findMessageByFromIdAndToId(@PathVariable("userId") Integer userId, @PathVariable("chatUserId") Integer chatUserId) {
        return messageService.findAll(userId, chatUserId);
    }

    @RequestMapping("/channel&userId={userId}")
    public List<Channel> findChannelByUserId(@PathVariable("userId") Integer userId) {
        return channelService.findAllByUserId(userId);
    }

    @RequestMapping("/channelUser&channelId={channelId}")
    public List<User> findChannelUser(@PathVariable("channelId") Integer channelId) {
        List<Integer> userIdList = channelService.findUserByChannelId(channelId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return userList;
    }

    @RequestMapping("/group&userId={userId}")
    public List<Group> findGroupByUserId(@PathVariable("userId") Integer userId) {
        return groupService.findAllByUserId(userId);
    }

    @RequestMapping("/groupUser&groupId={groupId}")
    public List<User> findGroupUser(@PathVariable("groupId") Integer groupId) {
        List<Integer> userIdList = groupService.findUserByGroupId(groupId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return userList;
    }
}
