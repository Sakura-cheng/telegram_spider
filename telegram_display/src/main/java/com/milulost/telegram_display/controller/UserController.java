package com.milulost.telegram_display.controller;

import com.milulost.telegram_display.bean.*;
import com.milulost.telegram_display.service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.AlgorithmConstraints;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")
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
    @Autowired
    private PhoneService phoneService;

    @RequestMapping("/phones")
    public ResultJson<List<Phone>> findPhones() {
        List<Phone> phones = phoneService.findAll();
        return new ResultJson<>(200, "success", phones.size(), phones);
    }

    @RequestMapping("/users")
    public ResultJson<List<User>> findUsers() {
        List<User> users = userService.findAll();
        return new ResultJson<>(200, "success", users.size(), users);
    }

    @RequestMapping("/user&phone={phone}")
    public ResultJson<List<User>> findUserByPhone(@PathVariable("phone") String phone) {
        List<User> users = new ArrayList<>();
        User user = userService.findUserByPhone(phone);
        users.add(user);
        return new ResultJson<>(200, "success", users.size(), users);
    }

    /***
     * 根据id查询user详情
     * @param id
     * @return
     */
    @RequestMapping("/user&userId={id}")
    public ResultJson<List<User>> findUserById(@PathVariable("id") Integer id) {
        List<User> users = new ArrayList<>();
        User user = userService.findUserById(id);
        users.add(user);
        return new ResultJson<>(200, "success", users.size(), users);
    }

    /***
     * 根据userId查询授权设备
     * @param userId
     * @return
     */
    @RequestMapping("/authorization&userId={userId}")
    public ResultJson<List<Authorization>> findAuthorizationByUserId(@PathVariable("userId") Integer userId) {
        List<Authorization> authorizationList = authorizationService.findByUserId(userId);
        return new ResultJson<>(200, "success", authorizationList.size(), authorizationList);
    }

    /***
     * 根据userId查询联系人详情
     * @param userId
     * @return
     */
    @RequestMapping("/contact&userId={userId}")
    public ResultJson<List<User>> findContactByUserId(@PathVariable("userId") Integer userId) {
        List<Integer> userIdList = contactService.findByUserId(userId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userList.size(), userList);
    }
    @RequestMapping("/chat&userId={userId}")
    public ResultJson<List<User>> findChatByUserId(@PathVariable("userId") Integer userId) {
        List<Integer> userIdList = messageService.findChatByUserId(userId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userList.size(), userList);
    }


    @RequestMapping("/message&userId={userId}&chatUserId={chatUserId}")
    public ResultJson<List<Message>> findMessageByFromIdAndToId(@PathVariable("userId") Integer userId, @PathVariable("chatUserId") Integer chatUserId) {
        List<Message> messageList = messageService.findAll(userId, chatUserId);
        return new ResultJson<>(200, "success", messageList.size(), messageList);
    }

    @RequestMapping("/channel&userId={userId}")
    public ResultJson<List<Channel>> findChannelByUserId(@PathVariable("userId") Integer userId) {
        List<Channel> channelList = channelService.findAllByUserId(userId);
        return new ResultJson<>(200, "success", channelList.size(), channelList);
    }

    @RequestMapping("/channelUser&channelId={channelId}")
    public ResultJson<List<User>> findChannelUser(@PathVariable("channelId") Integer channelId) {
        List<Integer> userIdList = channelService.findUserByChannelId(channelId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userList.size(), userList);
    }

    @RequestMapping("/group&userId={userId}")
    public ResultJson<List<Group>> findGroupByUserId(@PathVariable("userId") Integer userId) {
        List<Group> groupList = groupService.findAllByUserId(userId);
        return new ResultJson<>(200, "success", groupList.size(), groupList);
    }

    @RequestMapping("/groupUser&groupId={groupId}")
    public ResultJson<List<User>> findGroupUser(@PathVariable("groupId") Integer groupId) {
        List<Integer> userIdList = groupService.findUserByGroupId(groupId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdList) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userList.size(), userList);
    }
}
