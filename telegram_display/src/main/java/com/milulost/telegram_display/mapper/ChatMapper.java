package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Message;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatMapper {
    List<Message> findAll(@Param("userId") Integer userId, @Param("chatUserId") Integer chatUserId);
}
