-- MySQL基础数据库初始化脚本
CREATE DATABASE IF NOT EXISTS socialdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE socialdb;

-- 删除已存在的表（如果需要重新创建）
DROP TABLE IF EXISTS team_members;
DROP TABLE IF EXISTS contents;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    email VARCHAR(191) UNIQUE NOT NULL COMMENT '用户邮箱，用于登录',
    hashed_password VARCHAR(255) NOT NULL COMMENT '加密后的密码',
    full_name VARCHAR(191) COMMENT '用户全名',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_superuser BOOLEAN DEFAULT FALSE COMMENT '是否超级管理员',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 团队表
CREATE TABLE teams (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '团队ID',
    name VARCHAR(191) NOT NULL COMMENT '团队名称',
    description TEXT COMMENT '团队描述',
    owner_id INT NOT NULL COMMENT '团队所有者ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队信息表';

-- 团队成员表
CREATE TABLE team_members (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '成员关系ID',
    team_id INT NOT NULL COMMENT '团队ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role VARCHAR(50) NOT NULL COMMENT '角色：admin-管理员, member-普通成员',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_team_user (team_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队成员关系表';

-- 社交账号表
CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '账号ID',
    user_id INT NOT NULL COMMENT '所属用户ID',
    platform VARCHAR(50) NOT NULL COMMENT '平台：facebook,instagram,youtube等',
    username VARCHAR(191) NOT NULL COMMENT '平台用户名',
    platform_id VARCHAR(191) COMMENT '平台账号ID',
    profile_url VARCHAR(191) COMMENT '个人主页URL',
    description TEXT COMMENT '账号描述',
    avatar_url VARCHAR(191) COMMENT '头像URL',
    access_token TEXT COMMENT '访问令牌',
    refresh_token TEXT COMMENT '刷新令牌',
    token_expires_at TIMESTAMP NULL COMMENT '令牌过期时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    followers_count INT DEFAULT 0 COMMENT '粉丝数',
    following_count INT DEFAULT 0 COMMENT '关注数',
    total_posts INT DEFAULT 0 COMMENT '发文总数',
    config JSON COMMENT '账号配置JSON',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_platform_user (user_id, platform, platform_id(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社交平台账号表';

-- 内容表
CREATE TABLE contents (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '内容ID',
    user_id INT NOT NULL COMMENT '创建者ID',
    account_id INT NOT NULL COMMENT '发布账号ID',
    title VARCHAR(191) NOT NULL COMMENT '内容标题',
    content TEXT NOT NULL COMMENT '内容正文',
    media_urls JSON COMMENT '媒体文件URL列表',
    platforms JSON COMMENT '发布平台列表',
    schedule_time TIMESTAMP NULL COMMENT '计划发布时间',
    status VARCHAR(50) DEFAULT 'draft' COMMENT '状态：draft-草稿,scheduled-计划发布,published-已发布,failed-发布失败',
    tags JSON COMMENT '标签列表',
    config JSON COMMENT '发布配置JSON',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='内容发布表';

-- 设备表
CREATE TABLE devices (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '设备ID',
    user_id INT NOT NULL COMMENT '所属用户ID',
    device_name VARCHAR(191) NOT NULL COMMENT '设备名称',
    device_type VARCHAR(50) NOT NULL COMMENT '设备类型：desktop-桌面端,mobile-移动端,tablet-平板',
    device_id VARCHAR(191) UNIQUE NOT NULL COMMENT '设备唯一标识',
    status VARCHAR(50) DEFAULT 'offline' COMMENT '状态：online-在线,offline-离线,disabled-禁用',
    last_heartbeat TIMESTAMP NULL COMMENT '最后心跳时间',
    config JSON COMMENT '设备配置JSON',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备管理表';

-- 插入测试数据
INSERT INTO users (email, hashed_password, full_name, is_superuser) 
VALUES ('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYqeScNazC', 'Admin User', TRUE);

-- 插入测试团队
INSERT INTO teams (name, description, owner_id)
VALUES ('测试团队', '这是一个测试团队', 1);

-- 插入测试账号
INSERT INTO accounts (user_id, platform, username, platform_id, profile_url)
VALUES (1, 'facebook', 'testuser', 'fb123', 'https://facebook.com/testuser');

-- 插入测试内容
INSERT INTO contents (user_id, account_id, title, content, platforms, status)
VALUES (1, 1, '测试内容', '这是一条测试内容', '["facebook"]', 'draft');

-- 插入测试设备
INSERT INTO devices (user_id, device_name, device_type, device_id)
VALUES (1, '测试设备', 'desktop', 'dev123');