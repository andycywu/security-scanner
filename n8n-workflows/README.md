# 🔒 Security Scanner - n8n Workflows

n8n 自動化工作流，幫助推廣產品。

## 📁 Workflows

### 1. 自動化推文 (social-posting.json)
- 監控 GitHub commit → 自動發 Twitter/Facebook
- 定时發布產品宣傳貼文

### 2. 收款確認 (payment-notification.json)
- Wise 收款 → 自動通知 Telegram
- 更新客戶訂單狀態

### 3. 新客戶歡迎 (welcome-customer.json)
- 新訂單 → 自動發送歡迎 Email
- 加入客戶名單

## 🚀 設定方式

1. 打開 n8n (https://n8n.andycywu.cc)
2. 匯入 JSON 檔案
3. 填入 API Keys 和 Token
4. 啟動 Workflow

## 📋 需要的 API

| 服務 | 需要 |
|------|------|
| Twitter/X | API Key |
| Facebook | Page Access Token |
| Telegram | Bot Token |
| Wise | API Key |

---

*建立日期: 2026-02-13*
