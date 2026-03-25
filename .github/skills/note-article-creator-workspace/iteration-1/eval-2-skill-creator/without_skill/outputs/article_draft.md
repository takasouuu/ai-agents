# AIエージェント開発でのスキルの作り方：SKILL.md・eval-viewer・description optimization

## はじめに

GitHub Copilot などの AI エージェントを「自分のプロジェクト専用」に育てるとき、単なるプロンプト一行では限界がある。特定のドメイン知識や作業手順を再現性高く注入したいなら、**スキル（SKILL.md）** という仕組みが有効だ。

本記事では、エンジニア向けにスキルの構造・eval-viewer を使った反復改善ループ・description optimization の仕組みを解説する。

---

## 1. SKILL.md とは何か

### 概要

SKILL.md は、AI エージェントに特定の知識・手順・制約を与えるための Markdown ファイルだ。`.github/skills/<スキル名>/SKILL.md` という場所に置き、エージェントに「このタスクにはこのスキルを使え」と指示する。

```
.github/
  skills/
    estimate-creator/
      SKILL.md       ← スキルの本体
      examples/      ← 入出力サンプル
      evals/         ← 評価用ケース
```

### SKILL.md の基本構造

```markdown
# スキル名

## 目的
このスキルが解決する問題を一言で書く。

## 前提条件
- 必要なツール・環境
- 想定入力形式

## 手順
1. ステップ1
2. ステップ2
3. ステップ3

## 出力形式
期待するアウトプットの仕様。

## 注意事項
ハマりやすいポイント・禁止事項。
```

### なぜ SKILL.md が有効なのか

エージェントへの指示が毎回バラバラだと、出力品質にブレが生じる。SKILL.md に「正解の手順」を書いておくことで：

- **再現性**：誰がトリガーしても同じクオリティ
- **保守性**：改善点を SKILL.md だけ直せば全体に反映
- **説明責任**：なぜその出力になったかをファイルで追跡できる

---

## 2. eval-viewer を使った反復改善ループ

### なぜ eval が必要か

スキルを書いただけでは「本当に機能しているか」がわからない。eval（評価）は「スキルあり vs スキルなし」の出力を比較し、改善の方向性を定量的に判断するプロセスだ。

### ディレクトリ構造

```
evals/
  eval-1-basic/
    with_skill/
      outputs/       ← SKILL.md を使ったときの出力
    without_skill/
      outputs/       ← SKILL.md なしの出力
    expected/        ← 期待値（ゴールデンファイル）
```

### 反復改善ループ

```
[1. スキル初稿を書く]
        ↓
[2. eval を実行：with / without で出力を生成]
        ↓
[3. eval-viewer で差分を確認]
        ↓
[4. 足りない指示・曖昧な表現を SKILL.md に追記]
        ↓
[1. に戻る]
```

この PDCA を2〜3回回すだけで、スキルの品質は劇的に上がる経験がある。

### eval-viewer での確認ポイント

- `with_skill` の出力が期待値に近いか
- `without_skill` との差が明確に出ているか（差がなければスキルが機能していない）
- 出力の構造・用語・フォーマットが仕様通りか

---

## 3. description optimization の仕組み

### description とは

各スキルには、skill-creator が参照する **description** フィールドがある。エージェントは「このタスクに対してどのスキルを呼び出すか」を description のテキストで判断する。

```yaml
# skills/manifest.yml（例）
- name: estimate-creator
  description: |
    ソフトウェア開発プロジェクトの工数・費用見積もり Excel ファイルを自動生成するスキル。
    見積もり書作成、工数見積もり、費用試算、開発コスト估算、プロジェクト見積もり、
    MD見積もり、人日計算などと言われたら必ずこのスキルを使うこと。
  file: .github/skills/estimate-creator/SKILL.md
```

### なぜ description を最適化するのか

どれだけ SKILL.md が優れていても、**エージェントが正しいスキルを選択しなければ意味がない**。description が曖昧だと：

- 関係ないスキルが呼ばれる（False Positive）
- 正しいスキルが呼ばれない（False Negative）

どちらも出力品質の劣化につながる。

### 最適化の手法

#### 1. キーワード充実化
ユーザーが使いそうな言い回しを列挙する。「見積もり」だけでなく「工数計算」「費用試算」「人日」など同義語・類義語を網羅する。

#### 2. トリガー文言の明示化
`〜と言われたら必ずこのスキルを使うこと` のように、エージェントへの強い指示を入れる。LLM は指示語に敏感なので、明示的なトリガー文は効果が高い。

#### 3. A/B テスト的な eval
description のバリアント A・B を用意し、同じプロンプトで正しいスキルが選択されるかを eval で検証する。

```
プロンプト例：「このAPIの工数を計算して」
  variant A：estimate-creator が呼ばれる → 合格
  variant B：汎用スキルが呼ばれる → 不合格 → description を修正
```

### description optimization の指標

| 指標 | 説明 |
|------|------|
| Precision | 呼ばれたスキルのうち正解の割合 |
| Recall | 正解スキルが呼ばれた割合 |
| F1 | Precision と Recall の調和平均 |

実用上は Recall を優先しがち（見逃しのほうが痛い）だが、ノイズが多いと Precision も重要になる。

---

## 4. 実践：スキルを1本作るまでの流れ

```bash
# 1. スキルディレクトリを作る
mkdir -p .github/skills/my-skill/{examples,evals/eval-1/{with_skill/outputs,without_skill/outputs,expected}}

# 2. SKILL.md を書く
vim .github/skills/my-skill/SKILL.md

# 3. description を skills manifest に追記
vim .github/skills/manifest.yml

# 4. eval を実行して出力を比較
# （with_skill / without_skill の両方でエージェントを走らせる）

# 5. eval-viewer で確認・フィードバックを得て SKILL.md を改善
```

---

## まとめ

| 要素 | 役割 |
|------|------|
| SKILL.md | エージェントに注入する知識・手順 |
| eval-viewer | with/without スキルの出力を比較し品質を定量評価 |
| description optimization | 正しいスキルが選ばれるようトリガー文言を磨く |

3つをセットで回すことで、AI エージェントを「プロジェクト専用のドメインエキスパート」に育てていける。まずは小さなスキルを1本書いて、eval を1回回してみることをおすすめする。

---

*この記事は GitHub Copilot エージェント + SKILL.md の仕組みをベースに書いています。*
