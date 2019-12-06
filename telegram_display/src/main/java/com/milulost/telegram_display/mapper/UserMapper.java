package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Phone;
import com.milulost.telegram_display.bean.User;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserMapper {
    List<User> findAll();

    User findUserById(@Param("id") Integer id);

    User findUserByPhone(@Param("phone") String phone);
}
