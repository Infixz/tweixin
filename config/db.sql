SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- 用户表
DROP TABLE IF EXISTS `user_user`;
CREATE TABLE `user_user` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `password` varchar(128) NOT NULL,
    `last_login` datetime,
    `is_superuser` bool NOT NULL,
    `username` varchar(75) NOT NULL UNIQUE,
    `email` varchar(254) NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `date_joined` datetime NOT NULL,
    `login_attempted` integer NOT NULL,
    `updated` datetime NOT NULL,
    `secret` varchar(16) NOT NULL,
    `verification_needed` bool NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 微信关联账户
DROP TABLE IF EXISTS `docking_account`;
CREATE TABLE `docking_account` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NOT NULL,
    `uuid` varchar(64) NOT NULL,
    `type` varchar(1) NOT NULL,
    `token` varchar(32),
    `app_id` varchar(32),
    `secret` varchar(64),
    `encoding_aes_key` varchar(43),
    `is_valid` bool NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 企业号子应用关联
DROP TABLE IF EXISTS `docking_account_agent`;
CREATE TABLE `docking_account_agent` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `agent_id` integer NOT NULL,
    `name` varchar(32) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 微信用户
DROP TABLE IF EXISTS `docking_user`;
CREATE TABLE `docking_user` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `openid` varchar(64) NOT NULL,
    `created` integer unsigned NOT NULL,
    `is_active` bool NOT NULL,
    `is_canceled` bool NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE INDEX `docking_user_created` ON `docking_user` (`created`);
CREATE INDEX `docking_user_account_id` ON `docking_user` (`account_id`);

-- 访问令牌存储
DROP TABLE IF EXISTS `docking_access_token`;
CREATE TABLE `docking_access_token` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `access_token` varchar(512) NOT NULL,
    `created` integer unsigned NOT NULL,
    `expired` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 微信用户访问位置信息记录
DROP TABLE IF EXISTS `track_location`;
CREATE TABLE `track_location` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `longitude` integer NOT NULL,
    `latitude` integer NOT NULL,
    `scale` integer,
    `precision` integer,
    `label` varchar(256),
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE INDEX `track_location_created` ON `track_location` (`created`);

-- 素材管理表
-- 素材主表
DROP TABLE IF EXISTS `docking_material`;
CREATE TABLE `docking_material` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `alias` varchar(32) NOT NULL,
    `type` varchar(1) NOT NULL,
    `title` varchar(32) NOT NULL,
    `description` varchar(512) NOT NULL,
    `media_id` varchar(64) NOT NULL,
    `extra` varchar(512) NOT NULL,
    `fltype` varchar(1) NOT NULL,
    `file` varchar(256) NOT NULL,
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 图文消息
DROP TABLE IF EXISTS `docking_material_news`;
CREATE TABLE `docking_material_news` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `alias` varchar(32) NOT NULL,
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 图文消息主体内容
DROP TABLE IF EXISTS `docking_material_news_item`;
CREATE TABLE `docking_material_news_item` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `title` varchar(100) NOT NULL,
    `description` varchar(512) NOT NULL,
    `pltype` varchar(1) NOT NULL,
    `pic_large` varchar(256) NOT NULL,
    `pic_small` varchar(256) NOT NULL,
    `url` varchar(256) NOT NULL,
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 素材与图文消息关联表
DROP TABLE IF EXISTS `docking_material_news_mapping`;
CREATE TABLE `docking_material_news_mapping` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `material_id` integer NOT NULL,
    `news_id` integer NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 图文消息与主体关联表
DROP TABLE IF EXISTS `docking_material_news_item_mapping`;
CREATE TABLE `docking_material_news_item_mapping` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `news_id` integer NOT NULL,
    `item_id` integer NOT NULL,
    `ordering` integer NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 菜单
DROP TABLE IF EXISTS `docking_menu`;
CREATE TABLE `docking_menu` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `parent_id` integer,
    `name` varchar(10) NOT NULL,
    `type` varchar(20) NOT NULL,
    `key` varchar(16) NOT NULL,
    `url` varchar(256) NOT NULL,
    `media_id` varchar(64) NOT NULL,
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 事件响应规则
DROP TABLE IF EXISTS `docking_event_rule`;
CREATE TABLE `docking_event_rule` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `account_id` integer NOT NULL,
    `account_agent_id` integer,
    `key` varchar(16) NOT NULL,
    `material_id` integer NOT NULL,
    `created` integer unsigned NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SET FOREIGN_KEY_CHECKS = 1;
