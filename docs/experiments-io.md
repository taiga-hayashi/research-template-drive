# 実験と解析の入出力仕様

## 実験ごとに記入する項目

- study・問題定義・入力の出典/版/checksum:
- 条件のパラメータ名・型・単位・正規化・hash対象・スキーマ版:
- seed・モデル・評価予算・完了検証基準:
- 実行時コード版・dirty差分・依存定義:
- 出力キー・ファイル形式・単位・欠損の表現:
- 結果とcheckpointの対応、保存済みチャンクの範囲:
- サーバーでの実行コマンドと再開コマンド:

研究条件を端末の絶対パスから分離する。config_hashの計算方式はstudyごとに固定し、既存hashを再計算して置き換えない。この雛形にhash生成処理は含まれない。

## 解析ごとに記入する項目

[ANALYSIS_CONFIG.json](../templates/ANALYSIS_CONFIG.json)と[ANALYSIS_README.md](../templates/ANALYSIS_README.md)を使う。

- 入力: 対象run・結果package・必要checkpoint package・Drive参照・checksum・展開後の相対パス
- 条件: モデル・seed・予算・checkpoint/evaluation位置・除外理由・集計単位・中心値・ばらつき・欠損処理
- 版: 解析コード・設定・依存関係・実行時snapshot
- 出力: 一意なanalysis_idの下のCSV・PNG/PDF・独立パネル・README・analysis_config.json
- 再現: 同じ入力とコード版・解析設定を指定し、Mac/serverの保存先profileだけを切り替えるコマンド

`analysis_config.json`のrun_idは単独で一意とは限らないため、study・config_hash・モデル・seed・コード版との対応が分かる索引も参照する。複数入力はinputsに列挙し、必要なcheckpointは別の参照として追加する。

## 保存先と状態

端末固有のパスは`config/paths.local.json`に記入する。`data_root`はアーカイブ内の`data/`、`output_root`は`analysis/`に対応する。PestControlの旧階層は変更せず、入力のrelative_pathで対応させる。

実験の計算完了、解析の計算完了、アーカイブ検証、Drive保存検証を別々に記録する。結果だけ保存済みでも、必要なcheckpointが未保存なら再現用一式の保存完了とはしない。

状態判定は[STATUS_AND_JOBS.md](STATUS_AND_JOBS.md)を参照する。解析設定schema_version=2ではprotocol・figure_config・job_record_pathも記録する。既存version=1の記録は保持し、新しい項目を未確認のまま推測で補わない。
