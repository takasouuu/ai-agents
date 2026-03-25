#!/usr/bin/env python3
"""
note.com 記事生成スクリプト
コンテキストJSONまたはコマンドライン引数から記事のMarkdownを生成する。

使い方:
  # コンテキストファイルから生成
  python generate_article.py --context article_context.json --output article_draft.md

  # 直接説明を渡して生成
  python generate_article.py \
    --topic "GitHub CopilotのAgentモードを試してみた" \
    --points "subagentを使った並列実行,SKILL.mdの仕組み,eval-viewerでの反復改善" \
    --output article_draft.md

  # 現在の会話から自動抽出（コンテキストファイル不要）
  python generate_article.py --auto --output article_draft.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def load_context(path: str) -> dict:
    """コンテキストJSONを読み込む。"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_article_markdown(ctx: dict) -> str:
    """コンテキストから記事のMarkdownを構築する。"""
    title = ctx.get("title", "AI開発の実験まとめ")
    summary_points = ctx.get("summary_points", [])
    background = ctx.get("background", "")
    sections = ctx.get("sections", [])
    got_stuck = ctx.get("got_stuck", [])
    conclusion = ctx.get("conclusion", "")
    references = ctx.get("references", [])
    tags = ctx.get("tags", [])
    date = ctx.get("date", datetime.now().strftime("%Y年%m月%d日"))

    lines = []

    # タイトル
    lines.append(f"# {title}\n")

    # タグ（note.comはタイトル下に表示なし、末尾に記述）
    if tags:
        lines.append(f"*投稿日: {date}*\n")

    # この記事でわかること
    if summary_points:
        lines.append("## この記事でわかること\n")
        for point in summary_points:
            lines.append(f"- {point}")
        lines.append("")

    # 背景・きっかけ
    if background:
        lines.append("## 背景・きっかけ\n")
        lines.append(background)
        lines.append("")

    # 本文セクション
    for section in sections:
        lines.append(f"## {section['heading']}\n")
        lines.append(section.get("content", ""))
        if section.get("code"):
            lines.append("")
            lines.append(f"```{section.get('code_lang', '')}")
            lines.append(section["code"])
            lines.append("```")
        lines.append("")

    # ハマったこと・注意点
    if got_stuck:
        lines.append("## ハマったこと・注意点\n")
        for item in got_stuck:
            if isinstance(item, dict):
                lines.append(f"### {item.get('problem', '')}")
                lines.append(item.get("solution", ""))
                lines.append("")
            else:
                lines.append(f"- {item}")
        lines.append("")

    # まとめ
    if conclusion:
        lines.append("## まとめ\n")
        lines.append(conclusion)
        lines.append("")

    # 参考リンク
    if references:
        lines.append("## 参考リンク\n")
        for ref in references:
            if isinstance(ref, dict):
                lines.append(f"- [{ref.get('title', ref.get('url', ''))}]({ref.get('url', '')})")
            else:
                lines.append(f"- {ref}")
        lines.append("")

    return "\n".join(lines)


def create_sample_context(topic: str, points: list[str]) -> dict:
    """コマンドライン引数からサンプルコンテキストを生成する。"""
    return {
        "title": topic,
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "summary_points": points or [
            "GitHub Copilot Agentモードの実際の使い心地",
            "subagentを使った並列タスク実行のやり方",
            "SKILL.mdの構造と設計のポイント",
        ],
        "background": f"最近 {topic} について実験してみたので、試したことをまとめます。",
        "sections": [
            {
                "heading": "試した内容",
                "content": "以下のことを試しました。\n\n（ここに実験内容を書く）",
            },
            {
                "heading": "実際の手順",
                "content": "以下の手順で進めました。",
                "code": "# コード例をここに",
                "code_lang": "bash",
            },
        ],
        "got_stuck": [
            {
                "problem": "（ハマったこと）",
                "solution": "（解決策）",
            }
        ],
        "conclusion": "今回の実験で◯◯ができるようになりました。引き続き試していきたいです。",
        "tags": ["AI", "GitHub Copilot", "エージェント", "SKILL"],
    }


def main():
    parser = argparse.ArgumentParser(description="note.com 記事を生成する")
    parser.add_argument("--context", help="コンテキストJSONファイルのパス")
    parser.add_argument("--topic", help="記事のトピック（--context なしの場合）")
    parser.add_argument(
        "--points",
        help="要点をカンマ区切りで指定（例: '要点1,要点2,要点3'）",
    )
    parser.add_argument("--output", default="article_draft.md", help="出力ファイルパス")
    parser.add_argument("--auto", action="store_true", help="サンプルコンテキストを自動生成")
    args = parser.parse_args()

    # コンテキスト読み込み
    if args.context:
        ctx = load_context(args.context)
    elif args.topic or args.auto:
        points = args.points.split(",") if args.points else []
        topic = args.topic or "AI開発の実験まとめ — GitHub Copilot・エージェント・スキルを試してみた"
        ctx = create_sample_context(topic, points)
    else:
        print("❌ --context または --topic / --auto を指定してください")
        parser.print_help()
        sys.exit(1)

    # 記事生成
    article_md = build_article_markdown(ctx)

    # 出力
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(article_md, encoding="utf-8")

    print(f"✅ 記事を生成しました: {output_path}")
    print(f"   タイトル: {ctx.get('title', '(未設定)')}")
    print(f"   文字数: {len(article_md)} 文字")
    print()
    print("--- 生成された記事のプレビュー (先頭300文字) ---")
    print(article_md[:300])
    print("...")


if __name__ == "__main__":
    main()
