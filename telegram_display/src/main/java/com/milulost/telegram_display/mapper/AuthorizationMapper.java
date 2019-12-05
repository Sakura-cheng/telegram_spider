package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Authorization;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuthorizationMapper {
    List<Authorization> findByUserId(@Param("userId") Integer userId);
}
