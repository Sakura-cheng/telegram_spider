package com.milulost.telegram_display;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan("com.milulost.telegram_display.mapper")
@SpringBootApplication
public class TelegramDisplayApplication {

    public static void main(String[] args) {
        SpringApplication.run(TelegramDisplayApplication.class, args);
    }

}
