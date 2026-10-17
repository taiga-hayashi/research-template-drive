# .context/work/ — 作業の実施状態

## 役割

進行中と完了した作業の記録を管理する。

## 置くもの

active/、completed/と、関連索引への参照。

## 置かないもの

生データ、巨大ログ、根拠のない完了記録。

## ルール

同じ作業は同じtask_idの記録を更新する。安定したルールはcore/やdocs/へ移して参照する。実験のrun_idと作業のtask_idを混同しない。

## 配置・利用例

```text
active/<task_id>.md
completed/YYYY-MM-DD-<task_id>.md
```

[全フォルダの案内](../../docs/FOLDER_GUIDE.md)を参照する。実際の研究固有ルールはAGENTS.mdと対象studyの仕様に従う。
