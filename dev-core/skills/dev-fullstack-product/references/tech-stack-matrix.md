# 技术栈提案参考（阶段 1）

> 用法：按项目形态从下表取推荐项，**先探测本机环境**再定稿，每行给一句选型理由，交用户逐项确认。
> 本文件是**候选池**，不是必须全用；项目用不到的行（如无移动端）直接删掉该行并说明。

## 0. 本机环境探测（提案前先跑）

```bash
node -v; npm -v; pnpm -v 2>/dev/null
java -version 2>&1 | head -1; go version 2>/dev/null; python3 -V
docker info >/dev/null 2>&1 && echo "docker OK" || echo "docker 不可用"
psql --version 2>/dev/null; mysql --version 2>/dev/null; redis-server -v 2>/dev/null
```

> 注：`docker info` 在 Docker Desktop 刚启动时可能误报不可用，隔几秒重试一次再下结论。

## 1. 移动端

| 方案 | 适用 | 注意 |
|---|---|---|
| Flutter | 双端一致性要求高、含大量自绘 UI、团队无 iOS/Android 分工 | 包体大；原生能力要写 platform channel |
| React Native (Expo) | 团队是 React 栈、迭代快、以业务表单/列表为主 | 复杂动画与长列表性能需额外优化 |
| 原生 iOS + Android | 强依赖系统能力（蓝牙、后台定位、推送深度定制）、体验要求极高 | 双份人力与双份测试 |
| 微信小程序 / uni-app | 主入口在微信生态、需要免安装分发 | 审核周期、能力受平台限制 |
| 移动端 H5 | 活动页、分享页、投放落地页 | 需自己处理登录态与分享 |

## 2. 运营管理端

| 方案 | 适用 |
|---|---|
| React + Ant Design Pro | 中后台表格/表单密集，需要现成的权限、布局、CRUD 脚手架 |
| React + shadcn/ui + TanStack Table | 需要视觉定制、组件可控、不吃 antd 主题限制 |
| Vue3 + Element Plus | 团队是 Vue 栈；国内中后台生态成熟 |
| Vue3 + Naive UI / Arco | 需要更现代的视觉与 TS 体验 |

## 3. 后端

| 方案 | 适用 | 注意 |
|---|---|---|
| Java Spring Boot 3.x | 企业级、事务复杂、团队 Java 栈、需要长期演进 | 起步成本高，容器内存占用大 |
| Node.js NestJS | 与前端同语言、IO 密集、迭代快 | CPU 密集任务需另配 worker |
| Go Gin / Kratos | 高并发、低延迟、部署体积小 | ORM 与生态相对薄，业务代码更啰嗦 |
| Python FastAPI | 含 AI/数据处理、需要快速出接口 | 高并发需配 gunicorn/uvicorn 多进程 |

## 4. 数据与中间件

| 项 | 推荐 | 备选 | 触发条件 |
|---|---|---|---|
| 主库 | PostgreSQL 16+ | MySQL 8 | 需要 JSONB/地理/复杂查询选 PG；团队/运维熟 MySQL 选 MySQL |
| 缓存 | Redis 7 | — | 会话、限流、热点缓存、分布式锁 |
| 检索 | Elasticsearch / OpenSearch | PG 全文检索 | 全文检索需求轻量时**不要**上 ES |
| 消息队列 | RabbitMQ / Kafka | Redis Stream | 异步解耦、削峰、事件驱动 |
| 对象存储 | 阿里云 OSS / AWS S3 | MinIO（自建/本地开发） | 本地开发一律用 MinIO，免云账号依赖 |

> **不要过度设计**：0-1 阶段默认「单库 + Redis」，分库分表 / 读写分离 / ES 只在有明确量级依据时引入，
> 并把依据写进提案理由。

## 5. 接口与鉴权

| 项 | 推荐 | 说明 |
|---|---|---|
| 接口协议 | RESTful + OpenAPI 3 | 备选 GraphQL（前端字段需求高度可变）、gRPC（内部服务间） |
| 鉴权 | JWT（access + refresh） | 需要单点/第三方登录时上 OAuth2 / SSO |
| 权限模型 | RBAC（角色-权限-数据范围三层） | 管理端必须支持按角色隐藏菜单 + 后端二次校验 |
| 接口约定 | 统一响应体 `{code,message,data}` + 统一错误码表 | 错误码表在阶段 2 落成文件 |

## 6. 前端工程

| 项 | 候选 |
|---|---|
| 状态管理 | Zustand（轻）/ Redux Toolkit（复杂）/ Pinia（Vue）/ Riverpod（Flutter） |
| 数据请求 | TanStack Query / SWR / RTK Query |
| 表单 | React Hook Form + Zod / Element Plus 表单校验 |
| 图表 | ECharts（国内中后台首选）/ Recharts / AntV |
| 国际化 | i18next / vue-i18n / Flutter intl |

## 7. 工程与运维

| 项 | 推荐 | 说明 |
|---|---|---|
| 容器 | Docker + docker-compose | K8s 只在明确要多副本/多环境编排时上 |
| CI/CD | GitHub Actions / GitLab CI | 最少三条流水线：lint+test、build、deploy |
| 测试 | Vitest/Jest（前端）、Playwright（E2E）、JUnit/Pytest/go test（后端） | E2E 至少覆盖登录 + 主流程 |
| 监控日志 | Prometheus + Grafana + Loki | 轻量项目可只做结构化日志 + 健康检查端点 |
| 错误追踪 | Sentry | 三端都接，含 release 标记 |

## 8. 定稿表（写进进度存档）

| 分类 | 最终方案 | 版本 | 选型理由 | 确认时间 |
|---|---|---|---|---|
