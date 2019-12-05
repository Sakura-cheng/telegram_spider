package com.milulost.telegram_display.mapper;

import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ContactMapper {
    List<Integer> findByUserId(@Param("userId") Integer userId);
}
