package com.milulost.telegram_display.controller;

import com.milulost.telegram_display.bean.*;
import com.milulost.telegram_display.service.*;
import org.omg.PortableInterceptor.INACTIVE;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import sun.rmi.server.InactiveGroupException;

import javax.servlet.http.HttpServletRequest;
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
    public ResultJson<List<Phone>> findPhones(HttpServletRequest request) {
        String page = request.getParameter("page");
        String limt = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limt);
        List<Phone> phonesByPage = phoneService.findPhoneByPage(start, Integer.parseInt(limt));
        List<Phone> phones = phoneService.findAll();
        return new ResultJson<>(200, "success", phones.size(), phonesByPage);
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
    public ResultJson<List<Authorization>> findAuthorizationByUserId(HttpServletRequest request, @PathVariable("userId") Integer userId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Authorization> authorizationListByPage = authorizationService.findByUserIdByPage(userId, start, Integer.parseInt(limit));
        List<Authorization> authorizationList = authorizationService.findByUserId(userId);
        return new ResultJson<>(200, "success", authorizationList.size(), authorizationListByPage);
    }

    /***
     * 根据userId查询联系人详情
     * @param userId
     * @return
     */
    @RequestMapping("/contact&userId={userId}")
    public ResultJson<List<User>> findContactByUserId(HttpServletRequest request, @PathVariable("userId") Integer userId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Integer> userIdListByPage = contactService.findByUSerIdByPage(start, Integer.parseInt(limit), userId);
        List<Integer> userIdList = contactService.findByUserId(userId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdListByPage) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userIdList.size(), userList);
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
    public ResultJson<List<Message>> findMessageByFromIdAndToId(HttpServletRequest request, @PathVariable("userId") Integer userId, @PathVariable("chatUserId") Integer chatUserId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Message> messageListByPage = messageService.findMessageByPage(start, Integer.parseInt(limit), userId, chatUserId);
        List<Message> messageList = messageService.findAll(userId, chatUserId);
        return new ResultJson<>(200, "success", messageList.size(), messageListByPage);
    }

    @RequestMapping("/channel&userId={userId}")
    public ResultJson<List<Channel>> findChannelByUserId(HttpServletRequest request, @PathVariable("userId") Integer userId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Channel> channelListByPage = channelService.findAllByUserIdByPage(start, Integer.parseInt(limit), userId);
        List<Channel> channelList = channelService.findAllByUserId(userId);
        return new ResultJson<>(200, "success", channelList.size(), channelListByPage);
    }

    @RequestMapping("/channelUser&channelId={channelId}")
    public ResultJson<List<User>> findChannelUser(HttpServletRequest request, @PathVariable("channelId") Integer channelId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Integer> userIdListByPage = channelService.findUserByChannelIdByPage(start, Integer.parseInt(limit), channelId);
        List<Integer> userIdList = channelService.findUserByChannelId(channelId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdListByPage) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userIdList.size(), userList);
    }

    @RequestMapping("/group&userId={userId}")
    public ResultJson<List<Group>> findGroupByUserId(HttpServletRequest request, @PathVariable("userId") Integer userId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Group> groupListByPage = groupService.findAllByUserIdByPage(start, Integer.parseInt(limit), userId);
        List<Group> groupList = groupService.findAllByUserId(userId);
        return new ResultJson<>(200, "success", groupList.size(), groupListByPage);
    }

    @RequestMapping("/groupUser&groupId={groupId}")
    public ResultJson<List<User>> findGroupUser(HttpServletRequest request, @PathVariable("groupId") Integer groupId) {
        String page = request.getParameter("page");
        String limit = request.getParameter("limit");
        Integer start = (Integer.parseInt(page) - 1) * Integer.parseInt(limit);
        List<Integer> userIdListByPage = groupService.findUserByGroupIdByPage(start, Integer.parseInt(limit), groupId);
        List<Integer> userIdList = groupService.findUserByGroupId(groupId);
        List<User> userList = new ArrayList<>();
        for (Integer id : userIdListByPage) {
            User user = userService.findUserById(id);
            userList.add(user);
        }
        return new ResultJson<>(200, "success", userIdList.size(), userList);
    }

    @RequestMapping("/add")
    public ResultJson<String> add(HttpServletRequest request) {
        String phone = request.getParameter("phone");
        String category = request.getParameter("category");
        Phone addPhone = new Phone();
        addPhone.setId(0);
        addPhone.setPhone(phone);
        addPhone.setStatus(-1);
        addPhone.setCategory(Integer.parseInt(category));
        System.out.println(addPhone);
        phoneService.insert(addPhone);
        return new ResultJson<>(200, "success", 1, "add success!");
    }

    @RequestMapping("/deletePhone")
    public ResultJson<String> deletePhone(HttpServletRequest request) {
        String phone = request.getParameter("phone");
        System.out.println(phone);
        phoneService.delete(phone);
        return new ResultJson<>(200, "success", 1, "delete success!");
    }
}
