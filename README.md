# research-template-drive

Google Driveを正式保存先として、実験・解析・研究記録を再現できる形で管理する研究フォルダのテンプレートです。

[shunta0213/research-template](https://github.com/shunta0213/research-template) の管理方針を参考に、実験単位のZIP保存と閲覧用要約を組み合わせています。参照元のコードを同梱したものではありません。

## はじめ方（MacのGoogle Drive同期フォルダで作業）

1. GitHubの「Code → Download ZIP」で取得し、展開した中身をDrive内の新しい研究フォルダに配置します。研究ごとのGitHubリポジトリ作成は任意です。
2. READMEに研究目的、DriveフォルダURL、コードの所在、環境構築方法を記録します。
3. [Driveでの日常作業](docs/DRIVE_WORKFLOW.md)、[AGENTS.md](AGENTS.md)、[管理ガイド](docs/RESEARCH_LAYOUT.md)を読み、研究固有の条件・完了基準を追記します。
4. Drive同期フォルダ内のコード・設定・文書を直接編集し、`experiments/<study>/`から実行します。入力とコードは実行前にローカルで利用可能な状態にします。
5. 計算結果を検証して図・主要指標・ノートを更新し、実験またはチャンクごとに再現用ZIPを確定します。Drive上での保存検証まで行います。

GitHubでコードの履歴も管理する場合は「Use this template → Create a new repository」を使えます。Drive内の研究フォルダを日常作業の基準にし、GitHubへ反映するコード・管理文書だけを確認して送信します。詳細は[任意のGitHub併用](docs/DRIVE_WORKFLOW.md#githubを併用する場合任意)を参照してください。

## 構成

|場所|役割|
|---|---|
|src/|共通実装|
|experiments/|実験固有のコード・設定|
|data/inputs/、data/runs/|入力・生データ・checkpoint（Git管理外）|
|analysis/|集計・作図。PNG/PDFと個別パネルを保持|
|docs/|管理ガイド・入出力仕様・判断ログ|
|notes/|日付単位の研究ノート|
|refs/|参考文献・書誌情報|
|scripts/、tests/|補助処理・必要な検証|
|archive/|検証済み保存パッケージ（データはGit管理外）|
|cache/、tmp/|再生成可能なキャッシュ・一時作業（Git管理外）|

## データ管理

結果に影響する条件をconfig_hash、各試行をrun_idで識別し、既存結果を上書きしません。
コード・設定・ノート・閲覧用の図やCSVはDrive同期フォルダで直接扱います。大量の生データや高頻度のチェックポイントはDrive外の作業先で生成し、元の相対パスを保持したZIPにまとめてDriveへ保存します。少量の結果をDrive内で生成する運用も可能ですが、ZIP化しても元ファイルの逐次同期は止まりません。
manifestとSHA-256で検証し、Drive保存の検証前に元データを削除しません。
DVC、uv、ジョブ管理ツールは任意です。

## 含まれるもの

フォルダ構成、エージェント指示、管理ガイド、研究ノートと保存パッケージ説明の雛形です。
実験コード・自動アップロード処理・DVC認証は含みません。

## 自分の研究の情報

- 研究目的:
- DriveフォルダURL:
- コードの所在・版:
- 環境構築:
- 実験索引: study / config_hash / run_id / package_id / 状態 / Driveリンク
