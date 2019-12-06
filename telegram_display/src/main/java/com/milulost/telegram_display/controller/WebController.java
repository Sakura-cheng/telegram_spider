package com.milulost.telegram_display.controller;

import com.milulost.telegram_display.bean.User;
import com.milulost.telegram_display.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.http.HttpServletRequest;

@Controller
public class WebController {
    @Autowired
    private UserService userService;

    @RequestMapping("/index")
    public String index() {
        return "index";
    }

    @RequestMapping("/user")
    public String user(HttpServletRequest request, Model model) {
        String phone = request.getParameter("phone");
        String userId = request.getParameter("userId");
        User user = null;

        if (null != phone) {
            user = userService.findUserByPhone(phone);
        } else {
            user = userService.findUserById(Integer.parseInt(userId));
        }

        if (null == user) {
            return "redirect:index";
        }
        model.addAttribute("user", user);
        return "user";
    }

    @RequestMapping("/channelUsers")
    public String channelUsers(HttpServletRequest request, Model model) {
        String channelId = request.getParameter("channelId");
        model.addAttribute("channelId", channelId);
        return "users";
    }

    @RequestMapping("/groupUsers")
    public String groupUsers(HttpServletRequest request, Model model) {
        String groupId = request.getParameter("groupId");
        model.addAttribute("groupId", groupId);
        return "users";
    }

    @RequestMapping("/chat")
    public String chat(HttpServletRequest request, Model model) {
        String userId = request.getParameter("userId");
        String chatUserId = request.getParameter("chatUserId");
        User user = userService.findUserById(Integer.parseInt(userId));
        model.addAttribute("userId", userId);
        model.addAttribute("chatUserId", chatUserId);
        model.addAttribute("user", user);
        return "messages";
    }
}
