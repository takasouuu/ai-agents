#!/usr/bin/env python3
"""
note.com ドラフト投稿スクリプト
Markdownファイルをnote.comのAPIで下書き保存する。

使い方:
  # ドライラン（実際には投稿しない）
  python post_draft.py --input article_draft.md --title "記事タイトル" --dry-run

  # ドラフト保存
  python post_draft.py --input article_draft.md --title "記事タイトル" --tags "AI,GitHub Copilot"

  # ドラフト保存（タグなし）
  python post_draft.py --input article_draft.md --title "AIエージェントを試してみた"

環境変数（.env ファイルに設定）:
  NOTE_SESSION_V5   — ブラウザのCookieから取得したセッション値
  または
  NOTE_USER_TOKEN   — note.comのAPIトークン（Developer設定から取得）

認証の取得方法は references/auth_setup.md を参照。
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("❌ 必要なパッケージが不足しています。以下を実行してください:")
    print("  pip install requests python-dotenv")
    sys.exit(1)

# .env ファイルの読み込み
load_dotenv()
load_dotenv(Path(__file__).parent.parent / ".env")
load_dotenv(Path.cwd() / ".env")

NOTE_API_BASE = "https://note.com/api/v2"


def get_auth_headers() -> dict:
    """認証ヘッダーを生成する。セッションCookieまたはAPIトークンを使用。"""
    session_cookie = os.getenv("NOTE_SESSION_V5")
    user_token = os.getenv("NOTE_USER_TOKEN")

    if user_token:
        return {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    elif session_cookie:
        return {
            "Cookie": f"note_session_v5={session_cookie}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        }
    else:
        print("❌ 認証情報が設定されていません。")
        print()
        print(".env ファイルを作成して以下のいずれかを設定してください:")
        print()
        print("  # 方法1: セッションCookie（ブラウザから取得）")
        print("  NOTE_SESSION_V5=your_session_value_here")
        print()
        print("  # 方法2: APIトークン")
        print("  NOTE_USER_TOKEN=your_token_here")
        print()
        print("詳細は references/auth_setup.md を参照してください。")
        sys.exit(1)


def markdown_to_note_body(markdown_text: str) -> str:
    """
    MarkdownテキストをnoteのAPIが受け付けるHTML形式に変換する。
    シンプルな変換のみ対応（code block, heading, list, bold, italic）。
    """
    import re

    text = markdown_text

    # コードブロック（```lang ... ```）
    def replace_code_block(m):
        lang = m.group(1) or ""
        code = m.group(2).strip()
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code class="language-{lang}">{code}</code></pre>'

    text = re.sub(r"```(\w*)\n(.*?)```", replace_code_block, text, flags=re.DOTALL)

    # インラインコード
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # 見出し（H3以下は太字として扱う）
    text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    # 太字・斜体
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    # リンク
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)

    # 箇条書き（- item）
    def replace_list(m):
        items = re.findall(r"^- (.+)$", m.group(0), re.MULTILINE)
        li_items = "".join(f"<li>{item}</li>" for item in items)
        return f"<ul>{li_items}</ul>"

    text = re.sub(r"(^- .+\n?)+", replace_list, text, flags=re.MULTILINE)

    # 段落（空行で区切られたテキスト）
    paragraphs = text.split("\n\n")
    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # すでにHTMLタグで始まる場合はそのまま
        if para.startswith("<"):
            result.append(para)
        else:
            # 単純なテキストを<p>で囲む
            para = para.replace("\n", "<br>")
            result.append(f"<p>{para}</p>")

    return "\n".join(result)


def create_draft(
    title: str,
    body_markdown: str,
    tags: list[str],
    dry_run: bool = False,
) -> dict:
    """note.com にドラフト記事を作成する。"""
    headers = get_auth_headers()
    body_html = markdown_to_note_body(body_markdown)

    payload = {
        "title": title,
        "body": body_html,
        "type": "TextNote",
        "status": "draft",
    }

    # タグの設定
    if tags:
        payload["hashtag_notes_attributes"] = [
            {"hashtag": {"name": tag.strip()}} for tag in tags[:10]  # note.comは最大10タグ
        ]

    print(f"📝 ドラフト投稿")
    print(f"   タイトル: {title}")
    print(f"   タグ: {', '.join(tags) if tags else '(なし)'}")
    print(f"   本文文字数: {len(body_markdown)} 文字")
    print()

    if dry_run:
        print("🔍 ドライラン: 実際には投稿しません")
        print()
        print("--- ペイロード（JSON）---")
        preview_payload = payload.copy()
        preview_payload["body"] = preview_payload["body"][:200] + "...(省略)"
        print(json.dumps(preview_payload, ensure_ascii=False, indent=2))
        return {"dry_run": True, "title": title}

    try:
        response = requests.post(
            f"{NOTE_API_BASE}/notes",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code in (200, 201):
            data = response.json()
            note_data = data.get("data", {})
            note_key = note_data.get("key", "")
            note_id = note_data.get("id", "")
            creator_id = note_data.get("creator", {}).get("urlname", "")

            draft_url = f"https://note.com/{creator_id}/n/{note_key}" if note_key and creator_id else "(URLを取得できませんでした)"

            print(f"✅ ドラフト保存に成功しました！")
            print(f"   下書きURL: {draft_url}")
            print()
            print("📌 次のステップ:")
            print("   1. 上記のURLにアクセスして内容を確認")
            print("   2. サムネイル画像を設定（必要な場合）")
            print("   3. 「公開する」ボタンを押して公開")
            return data
        else:
            print(f"❌ 投稿に失敗しました (HTTP {response.status_code})")
            print(f"   レスポンス: {response.text[:500]}")
            if response.status_code == 401:
                print()
                print("⚠️  認証エラー: NOTE_SESSION_V5 または NOTE_USER_TOKEN が無効です。")
                print("   references/auth_setup.md を参照して再設定してください。")
            sys.exit(1)

    except requests.Timeout:
        print("❌ タイムアウト: note.com のAPIに接続できませんでした。")
        sys.exit(1)
    except requests.ConnectionError:
        print("❌ 接続エラー: インターネット接続を確認してください。")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="note.com にドラフト記事を投稿する")
    parser.add_argument("--input", required=True, help="Markdownファイルのパス")
    parser.add_argument("--title", required=True, help="記事タイトル")
    parser.add_argument(
        "--tags",
        default="",
        help="タグをカンマ区切りで指定（例: 'AI,GitHub Copilot,エージェント'）",
    )
    parser.add_argument("--dry-run", action="store_true", help="ドライラン（実際には投稿しない）")
    args = parser.parse_args()

    # Markdownファイル読み込み
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ ファイルが見つかりません: {input_path}")
        sys.exit(1)

    body_markdown = input_path.read_text(encoding="utf-8")
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    # ドラフト投稿
    create_draft(
        title=args.title,
        body_markdown=body_markdown,
        tags=tags,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
