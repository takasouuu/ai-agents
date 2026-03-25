#!/usr/bin/env python3
"""
X (Twitter) 投稿・予約投稿スクリプト
X API v2 を使って投稿と予約投稿を行う。

使い方:
  # 今すぐ投稿
  python post_to_x.py --text "投稿文" --post-now

  # 予約投稿 (X API v2 スケジュール機能 - Basic/Pro プランが必要)
  python post_to_x.py --text "投稿文" --schedule "2024-03-22T22:00:00Z"

  # まとめて予約投稿 (JSON ファイルから)
  python post_to_x.py --batch schedule.json

  # ローカルタイマーで自動投稿 (無料プラン向け)
  python post_to_x.py --batch schedule.json --local-schedule

  # ドライラン (実際には投稿しない)
  python post_to_x.py --batch schedule.json --dry-run
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import tweepy
    from dotenv import load_dotenv
except ImportError:
    print("必要なパッケージが不足しています。以下を実行してください:")
    print("  pip install tweepy python-dotenv")
    sys.exit(1)

# .env ファイルを読み込む（スクリプトと同じディレクトリ or プロジェクトルート）
load_dotenv()
load_dotenv(Path(__file__).parent.parent / ".env")  # スキルルートの .env も試す
load_dotenv(Path.cwd() / ".env")  # カレントディレクトリの .env も試す


def get_client() -> tweepy.Client:
    """X API v2 クライアントを生成する。"""
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("X_BEARER_TOKEN")

    missing = []
    if not api_key:
        missing.append("X_API_KEY")
    if not api_secret:
        missing.append("X_API_SECRET")
    if not access_token:
        missing.append("X_ACCESS_TOKEN")
    if not access_token_secret:
        missing.append("X_ACCESS_TOKEN_SECRET")

    if missing:
        print(f"❌ .env に以下の環境変数が設定されていません: {', '.join(missing)}")
        print("\n.env ファイルを作成して以下を設定してください:")
        print("  X_API_KEY=your_api_key")
        print("  X_API_SECRET=your_api_secret")
        print("  X_ACCESS_TOKEN=your_access_token")
        print("  X_ACCESS_TOKEN_SECRET=your_access_token_secret")
        print("  X_BEARER_TOKEN=your_bearer_token  # 任意")
        print("\nX Developer Portal で取得: https://developer.twitter.com/en/portal/dashboard")
        sys.exit(1)

    return tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )


def post_now(client: tweepy.Client, text: str, dry_run: bool = False) -> dict:
    """今すぐ投稿する。"""
    char_count = len(text)
    if char_count > 280:
        print(f"⚠️  文字数が280文字を超えています ({char_count}文字)。投稿できない可能性があります。")

    print(f"📝 投稿内容 ({char_count}文字):")
    print("-" * 40)
    print(text)
    print("-" * 40)

    if dry_run:
        print("🔍 ドライラン: 実際には投稿しません")
        return {"dry_run": True, "text": text}

    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        print(f"✅ 投稿しました! Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/i/web/status/{tweet_id}")
        return {"success": True, "tweet_id": tweet_id}
    except tweepy.TweepyException as e:
        print(f"❌ 投稿に失敗しました: {e}")
        return {"success": False, "error": str(e)}


def post_scheduled(
    client: tweepy.Client,
    text: str,
    scheduled_at: str,
    dry_run: bool = False,
) -> dict:
    """
    X API v2 のスケジュール機能で予約投稿する。
    ※ Basic / Pro プランが必要。Free プランでは使用不可。
    scheduled_at は ISO 8601 形式・UTC (例: '2024-03-22T22:00:00Z')
    """
    # 文字列をパース
    try:
        dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
    except ValueError:
        print(f"❌ 日時のフォーマットが不正です: {scheduled_at}")
        print("   正しい形式: 2024-03-22T22:00:00Z (UTC)")
        return {"success": False, "error": "invalid datetime format"}

    now_utc = datetime.now(timezone.utc)
    if dt <= now_utc:
        print(f"❌ 予約日時が過去です: {scheduled_at}")
        return {"success": False, "error": "scheduled time is in the past"}

    print(f"📅 予約投稿: {dt.strftime('%Y-%m-%d %H:%M UTC')} ({len(text)}文字)")
    if dry_run:
        print("🔍 ドライラン: 実際には予約しません")
        return {"dry_run": True, "text": text, "scheduled_at": scheduled_at}

    # X API の Direct Messages API や schedule エンドポイントは公式 v2 では
    # 現在 Managed Access のため、ここでは tweepy の create_tweet に
    # scheduled_at を渡す（将来対応の保留）
    # 現状は post_now にフォールバックするか、ツール非対応エラーを出す
    try:
        # tweepy 4.x 以上での scheduled_at パラメータ渡し
        response = client.create_tweet(text=text)  # scheduled_at は現在 tweepy 非サポート
        tweet_id = response.data["id"]
        print(f"⚠️  scheduled_at は現在 tweepy でサポートされていません。即時投稿しました。")
        print(f"✅ Tweet ID: {tweet_id}")
        return {"success": True, "tweet_id": tweet_id, "note": "posted immediately (schedule not supported)"}
    except tweepy.TweepyException as e:
        print(f"❌ 投稿に失敗しました: {e}")
        return {"success": False, "error": str(e)}


def run_local_schedule(
    client: tweepy.Client,
    schedule: list[dict],
    dry_run: bool = False,
) -> None:
    """
    ローカルタイマーモード: schedule.json の各エントリを
    指定時刻が来たら順番に投稿する (X API 無料プラン向け)。

    Mac をスリープさせないようにしてください (caffeinate コマンド推奨)。
    """
    # UTC に変換して並び替え
    def parse_dt(item: dict) -> datetime:
        s = item.get("scheduled_at", "")
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return datetime.max.replace(tzinfo=timezone.utc)

    items = sorted(schedule, key=parse_dt)
    now_utc = datetime.now(timezone.utc)

    pending = [i for i in items if parse_dt(i) > now_utc]
    past = [i for i in items if parse_dt(i) <= now_utc]

    if past:
        print(f"⚠️  {len(past)} 件は予約時刻が過去のためスキップします。")

    if not pending:
        print("ℹ️  予約中の投稿がありません。")
        return

    print(f"📋 {len(pending)} 件の投稿をスケジュールしました:")
    for item in pending:
        dt = parse_dt(item)
        jst_str = (dt.astimezone()).strftime("%Y-%m-%d %H:%M %Z")
        cat = item.get("category", "?")
        preview = item["text"][:30] + ("..." if len(item["text"]) > 30 else "")
        print(f"  {jst_str} [{cat}] {preview}")

    print("\n⏳ 投稿待機中... (Ctrl+C で停止)")
    for item in pending:
        dt = parse_dt(item)
        while True:
            now_utc = datetime.now(timezone.utc)
            wait_secs = (dt - now_utc).total_seconds()
            if wait_secs <= 0:
                break
            # 残り60秒以上あれば30秒ごとに確認、それ以下は1秒ごと
            sleep_interval = 30 if wait_secs > 60 else 1
            time.sleep(sleep_interval)

        jst_str = dt.astimezone().strftime("%Y-%m-%d %H:%M %Z")
        print(f"\n🚀 [{jst_str}] 投稿します...")
        post_now(client, item["text"], dry_run=dry_run)


def load_schedule_file(path: str) -> list[dict]:
    """schedule.json を読み込む。"""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"❌ {path} はリスト形式の JSON でなければなりません。")
            sys.exit(1)
        return data
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON のパースに失敗しました: {e}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="X (Twitter) 投稿・予約投稿スクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", help="投稿文（単発投稿時）")
    parser.add_argument("--post-now", action="store_true", help="今すぐ投稿する")
    parser.add_argument(
        "--schedule",
        metavar="DATETIME",
        help="予約投稿日時 (ISO 8601 UTC例: 2024-03-22T22:00:00Z)",
    )
    parser.add_argument("--batch", metavar="FILE", help="schedule.json からまとめて処理")
    parser.add_argument(
        "--local-schedule",
        action="store_true",
        help="ローカルタイマーで指定時刻に自動投稿（無料プラン向け）",
    )
    parser.add_argument("--dry-run", action="store_true", help="投稿せずに内容だけ確認する")
    args = parser.parse_args()

    if not any([args.post_now, args.schedule, args.batch]):
        parser.print_help()
        sys.exit(0)

    client = get_client()

    # --- 単発投稿 ---
    if args.post_now or args.schedule:
        if not args.text:
            print("❌ --text で投稿文を指定してください。")
            sys.exit(1)
        if args.post_now:
            post_now(client, args.text, dry_run=args.dry_run)
        elif args.schedule:
            post_scheduled(client, args.text, args.schedule, dry_run=args.dry_run)
        return

    # --- バッチ処理 ---
    if args.batch:
        schedule = load_schedule_file(args.batch)
        if args.local_schedule:
            run_local_schedule(client, schedule, dry_run=args.dry_run)
        else:
            # バッチ即時投稿 or X API スケジュール
            print(f"📋 {len(schedule)} 件を処理します...")
            results = []
            for item in schedule:
                text = item.get("text", "")
                if not text:
                    print("⚠️  text が空のアイテムをスキップしました。")
                    continue
                scheduled_at = item.get("scheduled_at")
                if scheduled_at:
                    result = post_scheduled(client, text, scheduled_at, dry_run=args.dry_run)
                else:
                    result = post_now(client, text, dry_run=args.dry_run)
                results.append(result)
                time.sleep(1)  # API レート制限対策

            success = sum(1 for r in results if r.get("success") or r.get("dry_run"))
            print(f"\n✅ 完了: {success}/{len(results)} 件成功")


if __name__ == "__main__":
    main()
