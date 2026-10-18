# 解析記録

- study / analysis_id:
- 解析の目的・種類（最適化比較 / 予測精度 / 相互作用など）:
- 入力run・結果package・checkpoint packageの対応:
- Drive参照・アーカイブSHA-256・取得後の検証結果:
- 使用モデル・seed・評価予算・checkpoint/evaluation位置:
- 除外したrunと理由、失敗・未完了・欠損の扱い:
- 集計単位・中心値・ばらつき（SD / SE / CI / IQR等）:
- 解析コード版・実行時snapshot・dirty差分の保存先:
- 実行場所（mac / server）・開始終了日時・実際の入出力先:
- 再現コマンド・依存関係ファイル:
- 設定ファイル: analysis_config.json
- 計算状態: pending / queued / running / partial / failed / complete
- 出力検証状態: pending / running / passed / failed / unverified
- 検証根拠への参照・全体の完了状態:
- protocolのphase・版・比較条件表:
- job_record.json・共通図設定とsnapshotへの参照:
- 出力検証（CSV整合性・PNG/PDF対応・独立パネル・表示確認）:
- Drive保存先・保存検証状態: pending / unverified / verified / failed
- 観測結果:
- 解釈と限界:

解析状態とDrive保存検証は別々に記録する。再実行は同じ分類のpdf/・png/・csv/を更新し、新しいanalysis_idを設定と索引に記録する。更新前の実行情報・ソース・出力checksumをdocs/records/analysis_runs/の記録ファイルへ保持し、旧索引の参照先も更新する。plot.ipynbとplot.pyをセットにし、Notebookの各図にMarkdownで読み方を記載する。詳細は[解析・作図の運用](../docs/ANALYSIS_WORKFLOW.md)。
