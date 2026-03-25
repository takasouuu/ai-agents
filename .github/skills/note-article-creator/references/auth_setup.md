# note.com 認証セットアップ

note.com のAPIを使うために認証情報が必要です。以下のいずれかの方法で取得してください。

---

## 方法1: セッションCookieを使う（簡単・推奨）

### 手順

1. **ブラウザでnote.comにログイン**  
   Chrome / Firefox / Safari でいつも使うアカウントでログインする

2. **Cookieを取得**  
   - Chrome の場合：
     1. F12（開発者ツール）を開く
     2. `Application` タブ → `Cookies` → `https://note.com`
     3. `note_session_v5` の値をコピー

   - Firefox の場合：
     1. F12（開発者ツール）を開く
     2. `Storage` タブ → `Cookies` → `https://note.com`
     3. `note_session_v5` の値をコピー

3. **.env ファイルに設定**  
   プロジェクトルートまたはスキルのディレクトリに `.env` ファイルを作成：
   ```
   NOTE_SESSION_V5=ここにコピーした値を貼り付ける
   ```

### 注意
- セッションCookieはログアウトすると無効になります
- 定期的に再取得が必要です（有効期限はnote.comの設定による）
- `.env` ファイルは `.gitignore` に追加してGitにコミットしないよう注意

---

## 方法2: APIトークンを使う

### 手順

1. note.com では現在、公式の個人APIトークン発行機能が提供されていない場合があります  
2. 有効化されている場合は `https://note.com/settings/tokens` から取得可能
3. 取得できた場合は `.env` ファイルに設定：
   ```
   NOTE_USER_TOKEN=取得したトークンを貼り付ける
   ```

---

## .env ファイルのサンプル

```env
# note.com 認証（どちらか一方を設定）
NOTE_SESSION_V5=abc123...your_session_value_here

# または
# NOTE_USER_TOKEN=your_token_here
```

---

## 動作確認

設定後、以下でドライランして認証が通るか確認：

```bash
python scripts/post_draft.py \
  --input article_draft.md \
  --title "テスト" \
  --dry-run
```

ドライランでは実際には投稿されませんが、認証エラーが出る場合はメッセージに従って設定を見直してください。
