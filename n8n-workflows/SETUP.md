# 🔒 Security Scanner - n8n 整合指南

## 📁 可用 Workflows

| 檔案 | 名稱 | 功能 |
|------|------|------|
| `social-posting-full.json` | Social Media Auto-Poster (Full) | Twitter + Facebook + Threads |
| `social-posting-v2.json` | Social Media Auto-Poster | Twitter + Facebook |
| `payment-notification-v2.json` | Payment Notification | Wise 收款通知 |

---

## 🚀 快速設定

### 第一步：登入 n8n

1. 打開 https://n8n.andycywu.cc
2. 登入你的帳號

### 第二步：匯入 Workflow

1. 點擊右上角 **「+ Import」**
2. 選擇 JSON 檔案
3. 選擇 `n8n-workflows/social-posting-v2.json`
4. 點擊 **「Import」**

### 第三步：設定 Credentials

#### Twitter/X 設定

1. 點擊 Twitter/X 節點
2. 點擊 **「Create New Credential」**
3. 填入：
   - Client ID: [你的 Twitter API Client ID]
   - Client Secret: [你的 Twitter API Secret]
   - Scopes: `tweet.read tweet.write users.read`
4. 點擊 **「Save」**

#### Facebook 設定

1. 點擊 Facebook 節點
2. 點擊 **「Create New Credential」**
3. 填入：
   - Facebook Page ID: [你的專頁 ID]
   - Access Token: [你的 Page Access Token]
4. 點擊 **「Save」**

#### Telegram 設定

1. 點擊 Telegram 節點
2. 點擊 **「Create New Credential」**
3. 填入：
   - Bot Token: `8344340833:AAF0kCtZ_awsPrs6M2lzclCDmeer6xjXOdw`
4. 點擊 **「Save」**

#### Threads 設定

1. 點擊 Threads 節點
2. 點擊 **「Create New Credential」**
3. 選擇 **「Threads API OAuth2」**
4. 填入：
   - Client ID: [你的 Threads App Client ID]
   - Client Secret: [你的 Threads App Secret]
   - Scopes: `threads_basic threads_content_publish`
5. 點擊 **「Save」**
6. **重要**：Threads API 需要先申請 developer access

**申請 Threads API：**
1. 去 https://developers.threads.net
2. 建立 App
3. 申請 Content Publishing 權限
4. 通過後取得 API Keys

#### Google Sheets 設定（可選）

1. 點擊 Google Sheets 節點
2. 點擊 **「Create New Credential」**
3. 連接你的 Google 帳號
4. 選擇目標 Spreadsheet

### 第四步：啟動 Workflow

1. 點擊右上角 **「Active」** 開關
2. 確認啟動

---

## ⚙️ 環境變數設定

在 n8n 中設定環境變數：

```
WISE_WEBHOOK_URL = https://your-n8n-instance.com/webhook/wise-payment
```

---

## 📊 流程圖

### Social Posting Workflow

```
┌─────────────────┐
│  Schedule Trigger│ (每 24 小時)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Content Generator│ (隨機選擇宣傳內容)
└────────┬────────┘
         │
    ┌────┼────┐
    │         │         │
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Twitter│ │Facebook│ │ Threads│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └────┬────┴────┬────┘
         │
         ▼
┌─────────────────────┐
│ Telegram Notification│ (發送完成通知)
└─────────────────────┘
```

### Payment Notification Workflow

```
┌─────────────────┐
│   Wise Webhook  │ (收款觸發)
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │         │
    ▼         ▼         ┌─────────────────┐
┌───────┐  ┌──────────┐│   Telegram Alert │
│ Google│  │Order Processor│ └────────┬────────┘
│ Sheets │  └─────┬────┘           │
└────────┘        │                │
                  ▼                │
           ┌───────────┐          │
           │Customer Email │◄──────┘
           └───────────┘
```

---

## 🧪 測試方式

### 測試 Social Posting

1. 點擊 **「Execute Node」** 按鈕
2. 選擇 **「From Start Node」**
3. 查看 Twitter/Facebook 是否收到測試貼文

### 測試 Payment Notification

1. 使用 Postman 發送 POST 請求：
   ```
   POST https://n8n.andycywu.cc/webhook/wise-payment
   {
     "amount": 49,
     "currency": "USD",
     "senderName": "Test User",
     "reference": "Security Scanner 測試訂單"
   }
   ```
2. 查看 Telegram 是否收到通知

---

## 🔧 常見問題

### Q: Twitter 發文失敗？

A: 檢查：
- Twitter API Keys 是否正確
- 帳號是否已開啟 API 權限
- 推文內容是否超過 280 字元

### Q: Facebook 發文失敗？

A: 檢查：
- Page Access Token 是否過期
- 專案是否設定為公開
- 是否有 Page Admin 權限

### Q: Telegram 沒收到通知？

A: 檢查：
- Bot Token 是否正確
- Chat ID 是否正確（需要負數格式）
- Workflow 是否已啟動

---

## 📞 支援

如有問題，聯繫：
- Telegram: @singularity_capital_bot
- Email: andycywu@gmail.com

---

*建立日期: 2026-02-13*
*版本: 1.0*
