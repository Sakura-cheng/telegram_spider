package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Message;
import com.milulost.telegram_display.bean.User;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatMapper {
    List<Message> findAll(@Param("userId") Integer userId, @Param("chatUserId") Integer chatUserId);

    List<Integer> findFromIdByUserId(@Param("userId") Integer userId);

    List<Integer> findToIdByUserId(@Param("userId") Integer userId);

    List<Message> findMessageByPage(@Param("start") Integer start, @Param("limit") Integer limit, @Param("userId") Integer userId, @Param("chatUserId") Integer chatUserId);
}
