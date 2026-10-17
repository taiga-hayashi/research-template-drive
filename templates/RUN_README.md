# 実験保存パッケージ

- study / config_hash / run_id一覧:
- package_id / 対象（結果 / checkpoint / 両方）:
- 計算状態: partial / failed / complete
- 含むseed・モデル・完了チャンク・checkpoint位置:
- 結果とcheckpointが別保存の場合の対応package_id・Driveリンク:
- 実行コード版・実行時snapshot・dirty差分のSHA-256:
- 実行コマンド・依存関係ファイル・実行環境:
- 実際のサーバー出力先とアーカイブ内の相対パス対応:
- 問題・入力の出典/版/checksum:
- 実験条件・seed・評価予算:
- 含むデータ・図・ログ・必要checkpoint:
- 含めていない依存パッケージの保存先・版・SHA-256:
- 主要結果と測定限界:
- 検証済みの完了基準:
- アーカイブ形式・ファイル名・サイズ・SHA-256:
- 内部manifestの検証結果:
- Drive保存先:
- クラウド保存検証状態: pending / unverified / verified / failed
- 検証日時・クラウド上のサイズ・checksum照合方法と結果:
- 復元方法: 空の保存先でアーカイブのSHA-256と内部manifestを検証して展開する。
- 再現手順・外部依存:

ZIPを新規標準とする。既存のtar等も扱い、再圧縮だけを目的に作り直さない。計算完了とDrive保存検証を区別し、保存検証前に元データを削除しない。
