package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Channel;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChannelMapper {
    List<Channel> findAllByUserId(@Param("userId") Integer userId);

    List<Integer> findUserByChannelId(@Param("channelId") Integer channelId);
}
