# Phase 8 验收单（可观测性增强：可选请求日志）

本阶段目标（非破坏）：
- 增加问题排查能力，但默认不开，不影响现网行为

## 已做内容
1) 新增可选请求日志开关（默认 false）
- `STAR_OFFICE_REQUEST_LOG_ENABLED=false`
- `STAR_OFFICE_REQUEST_LOG_PATH=`（默认 `<repo>/request.log`）

2) 日志字段（已脱敏）
- 时间、request_id、IP、方法、路径、状态码、耗时、UA
- Bearer token 仅保留尾部少量字符（其余打码）

3) `security_check.py` 增加路径安全检查
- 防止把日志路径配置到敏感目录

## 线上验收
- 不开开关时：线上功能与之前完全一致
- 开启后：仅多出日志文件，不改变业务逻辑

## 回滚
- 环境层：`STAR_OFFICE_REQUEST_LOG_ENABLED=false`
- 代码层：`git revert <phase8_commit>`
