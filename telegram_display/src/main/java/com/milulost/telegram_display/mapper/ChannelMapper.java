package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Channel;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChannelMapper {
    List<Channel> findAllByUserId(@Param("userId") Integer userId);

    List<Channel> findAllByUserIdByPage(@Param("start") Integer start, @Param("limit") Integer limit, @Param("userId") Integer userId);

    List<Integer> findUserByChannelId(@Param("channelId") Integer channelId);

    List<Integer> findUserByChannelIdByPage(@Param("start") Integer start, @Param("limit") Integer limit, @Param("channelId") Integer channelId);
}
