# .context/templates/ — 作業引継ぎの雛形

## 役割

複数段階の作業を引き継ぐ記録形式を揃える。

## 置くもの

task-state.md。

## 置かないもの

実際の進捗を埋めた記録、実験・解析の生データ。

## ルール

task-state.mdをwork/active/<task_id>.mdへコピーする。元の雛形を作業ログとして使わない。実験記録用の雛形はプロジェクト直下のtemplates/を使う。

## 配置・利用例

```text
task-state.md → ../work/active/<task_id>.md
```

[全フォルダの案内](../../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
