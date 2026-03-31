# 雾漫林间动漫评分网站

## 项目概览

一个现代化的动漫评分网站，支持动漫搜索、评分、评论等功能。

## 技术栈

- **前端**: React 19, TypeScript, Vite, Tailwind CSS
- **后端**: Express.js, TypeScript
- **数据库**: MySQL
- **包管理**: pnpm

## 核心功能

1. **用户认证**: 登录、注册、邮箱验证码
2. **动漫浏览**: 
   - 首页（最近更新）
   - 新番动漫（最近2个月上映）
   - 连载动漫
   - 完结动漫
   - 国产动漫
   - 日本动漫
   - 剧场版
   - 每日推荐
3. **动漫搜索**: 支持按标题、描述、工作室搜索，支持年份、状态、工作室筛选
4. **评分系统**: 用户可以为动漫打分（1-5星）
5. **评论系统**: 用户可以发表评论和查看其他用户的评论
6. **管理后台**: 管理员可以添加、编辑、删除动漫

## 目录结构

```
.
├── src/
│   ├── components/          # React组件
│   │   ├── AnimeCard.tsx    # 动漫卡片组件
│   │   ├── AnimeDetailModal.tsx  # 动漫详情弹窗
│   │   ├── AnimeListPage.tsx     # 动漫列表页面组件
│   │   ├── Navbar.tsx       # 导航栏
│   │   ├── SearchBar.tsx    # 搜索栏
│   │   └── ...
│   ├── pages/               # 页面组件
│   │   ├── RecentPage.tsx   # 新番动漫页面
│   │   ├── OngoingPage.tsx  # 连载动漫页面
│   │   ├── CompletedPage.tsx # 完结动漫页面
│   │   ├── ChinesePage.tsx  # 国产动漫页面
│   │   ├── JapanesePage.tsx # 日本动漫页面
│   │   ├── TheaterPage.tsx  # 剧场版页面
│   │   ├── DailyPage.tsx    # 每日推荐页面
│   │   ├── SearchPage.tsx   # 搜索页面
│   │   └── AdminPage.tsx    # 管理后台
│   ├── context/             # React Context
│   │   └── AuthContext.tsx  # 认证上下文
│   ├── types/               # TypeScript类型定义
│   │   └── index.ts         # 类型定义文件
│   ├── config/              # 配置文件
│   │   └── api.ts           # API配置
│   ├── App.tsx              # 主应用组件
│   └── main.tsx             # 入口文件
├── server-simple.ts         # 后端服务器
├── vite.config.ts           # Vite配置
├── tsconfig.json            # TypeScript配置
├── package.json             # 项目依赖
├── .coze                    # Coze配置
└── AGENTS.md                # 本文档
```

## 数据库结构

### animes 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | varchar(255) | 中文标题 |
| title_jp | varchar(255) | 日文标题 |
| description | text | 描述 |
| cover_image | varchar(500) | 封面图片 |
| episodes | int | 集数 |
| status | varchar(50) | 状态（已完结/连载中/未播出） |
| release_year | int | 上映年份 |
| release_date | date | 上映日期 |
| studio | varchar(100) | 制作公司 |
| genre | varchar(255) | 类型 |
| average_rating | decimal(3,2) | 平均评分 |
| rating_count | int | 评分人数 |
| nationality | varchar(50) | 国家（日本/中国等） |
| anime_type | varchar(20) | 动漫类型（热血/奇幻/悬疑等） |
| is_movie | tinyint(1) | 是否为剧场版 |
| created_at | datetime | 创建时间 |

## API 接口

### 动漫相关
- `GET /api/anime` - 获取动漫列表
- `GET /api/anime/recent` - 获取新番动漫（最近2个月）
- `GET /api/anime/search` - 搜索动漫
- `GET /api/anime/filter-options` - 获取筛选选项
- `GET /api/anime/:id` - 获取单个动漫详情
- `POST /api/anime/:id/rate` - 提交评分
- `GET /api/anime/:id/comments` - 获取评论列表
- `POST /api/anime/:id/comments` - 发表评论

### 用户认证
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录
- `GET /api/user` - 获取当前用户信息
- `GET /api/slider-token` - 获取滑块验证Token
- `POST /api/send-code` - 发送邮箱验证码

### 管理后台
- `POST /api/admin/login` - 管理员登录
- `GET /api/admin/animes` - 获取动漫列表
- `POST /api/admin/animes` - 添加新动漫
- `PUT /api/admin/animes/:id` - 更新动漫信息
- `DELETE /api/admin/animes/:id` - 删除动漫

## 开发指南

### 启动前端开发服务器
```bash
pnpm dev
```
前端运行在 http://localhost:5000

### 启动后端服务器
```bash
pnpm run server
```
后端运行在 http://localhost:3001

### 构建生产版本
```bash
pnpm run build
```

### 更新动漫数据
```bash
node update-anime-data.cjs
```

## 关键修改记录

1. **去掉动漫排行页面**: 移除了 RankingPage.tsx 和相关路由，首页重定向到 /recent
2. **添加新番动漫功能**: 新增 /api/anime/recent 接口，筛选最近2个月上映的动漫
3. **数据库更新**: 添加了 release_date 字段，用于更精确的新番筛选
4. **修复字段名**: 统一使用下划线命名（snake_case）与数据库保持一致
5. **API配置**: 设置 API_BASE_URL 为空字符串，通过 Vite 代理访问后端
6. **数据更新脚本**: 创建 update-anime-data.cjs 用于更新动漫数据

## 注意事项

1. 前端通过 Vite 代理 `/api` 请求到后端的 3001 端口
2. 数据库使用线上 MySQL 数据库（59.110.214.50:3306）
3. 新番动漫通过 release_date 或 created_at 字段筛选最近2个月的数据
4. 所有字段名使用下划线命名（snake_case）
