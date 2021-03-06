package com.milulost.telegram_display.mapper;

import com.milulost.telegram_display.bean.Phone;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PhoneMapper {
    List<Phone> findAll();

    void insert(@Param("phone") Phone phone);

    void delete(@Param("phone") String phone);

    List<Phone> findPhoneByPage(@Param("start") Integer start, @Param("limit") Integer limit);
}
