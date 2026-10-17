# 作業の引継ぎ

最初に[研究の基本情報](core/project.md)を確認する。作業内容に応じて必要な文書だけを読む。

| 作業 | 参照 |
|---|---|
| サーバー計算・Drive保存・端末切替 | [運用ガイド](../docs/DRIVE_WORKFLOW.md) |
| サーバーで梱包・必要データの取得 | [梱包と取得](../docs/PACKAGING_AND_FETCH.md) |
| 状態確認・ジョブ再開 | [状態とジョブ](../docs/STATUS_AND_JOBS.md) |
| 比較・探索・確認実験 | [研究・比較手順](../docs/RESEARCH_PROTOCOL.md) |
| 解析・作図 | [図の設定](../docs/FIGURE_POLICY.md)と対象analysis_config.json |

複数段階の作業では[task-state.md](templates/task-state.md)を`work/active/<task_id>.md`へコピーする。既存のactive記録を確認し、同じ作業の記録を増やさず更新する。完了時は`work/completed/`へ移し、必要な索引から参照する。未完了の作業を完了扱いで移さない。

安定した研究固有情報はcore/、変化する実行状況はwork/へ置く。チャットだけに実行条件や残作業を残さない。AGENTS.mdへジョブ履歴や長いログを書き足さない。
