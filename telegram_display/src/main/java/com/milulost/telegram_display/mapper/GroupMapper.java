package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Group;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface GroupMapper {
    List<Group> findAllByUserId(@Param("userId") Integer userId);

    List<Group> findAllByUserIdByPage(@Param("start") Integer start, @Param("limit") Integer limit, @Param("userId") Integer userId);

    List<Integer> findUserByGroupId(@Param("groupId") Integer groupId);

    List<Integer> findUserByGroupIdByPage(@Param("start") Integer start, @Param("limit") Integer limit, @Param("groupId") Integer groupId);
}
