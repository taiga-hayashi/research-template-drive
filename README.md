# research-template-drive

Google Driveを正式保存先として、実験・解析・研究記録を再現できる形で管理する研究フォルダのテンプレートです。

[shunta0213/research-template](https://github.com/shunta0213/research-template) の管理方針を参考に、実験単位のZIP保存と閲覧用要約を組み合わせています。参照元のコードを同梱したものではありません。

## はじめ方（サーバーで計算し、Mac・サーバーで解析）

1. GitHubの「Code → Download ZIP」で取得し、新しい研究フォルダに展開します。MacではDrive同期フォルダ、サーバーでは作業領域に同じ版のコードを用意します。研究用GitHubリポジトリは任意です。
2. READMEに研究目的・Drive保存先・環境構築を記録し、[AGENTS.md](AGENTS.md)と[管理ガイド](docs/RESEARCH_LAYOUT.md)を確認します。
3. [保存先設定例](config/paths.example.json)を`config/paths.local.json`へコピーし、Mac・サーバーそれぞれの保存先を設定します。研究条件と端末のパスは分けます。
4. [実験索引](templates/EXPERIMENT_INDEX.csv)・[解析索引](templates/ANALYSIS_INDEX.csv)を`docs/`へコピーします。
5. サーバーで計算し、完了したrun・チャンク単位で再現用パッケージをDriveへ直接アップロードして検証します。結果とcheckpointの対応を実験索引に残します。
6. Macまたはサーバーで必要データを取得・検証し、同じ解析コードと[解析設定](templates/ANALYSIS_CONFIG.json)を使います。端末ごとに切り替えるのは保存先設定です。
7. 新しいanalysis_idへ図・CSV・[解析記録](templates/ANALYSIS_README.md)を保存し、Drive保存検証後に解析索引を更新します。

Pythonは各端末のDrive外にある既存のローカル仮想環境で実行します。Macとサーバーで環境本体を共有せず、依存定義と実際のPython・ライブラリ版を記録します。Drive内に`.venv`を作成しません。

詳しい手順とPestControlの既存配置への対応は[DRIVE_WORKFLOW.md](docs/DRIVE_WORKFLOW.md)を参照してください。

## サーバーで梱包し、必要データを取得する

[梱包・取得ガイド](docs/PACKAGING_AND_FETCH.md)に従い、`scripts/artifacts.py`で対象一覧の確認、ZIP作成・manifest検証、rcloneからの選択取得・検証・新規展開を行えます。既存のローカルPython環境と認証済みrcloneを使います。

## 作業を引き継ぎ、完了を判断する

- [状態・ジョブ・再開手順](docs/STATUS_AND_JOBS.md): 計算、検証、Drive保存、解析を別管理
- [AIへの引継ぎ](.context/INDEX.md): 固定条件、実施済みと根拠、未確認、次の手順
- [比較・探索・確認実験](docs/RESEARCH_PROTOCOL.md): 比較条件表と事前固定するprotocol
- [図の共通設定](docs/FIGURE_POLICY.md): モデル色、PNG/PDFと独立パネル、集計・評価軸

これらは記録用の雛形と運用ルールです。自動ジョブ投入・監視・再開、研究結果の妥当性検証や作図への自動適用は実装していません。

## 構成

各フォルダの役割・配置・命名ルールは[フォルダ案内](docs/FOLDER_GUIDE.md)と各フォルダ内のREADME.mdを参照してください。

|場所|役割|
|---|---|
|src/|共通実装|
|experiments/|実験固有のコード・設定|
|data/inputs/、data/runs/|入力・生データ・checkpoint（Git管理外）|
|analysis/|`<study>/<analysis_id>/`ごとの解析結果。PNG/PDFと独立パネルを保持|
|config/|端末別の保存先設定例と研究の共通図設定。個人設定はGit管理外|
|.context/|研究固有の基本情報と作業引継ぎ|
|docs/|管理ガイド・入出力仕様・判断ログ|
|notes/|日付単位の研究ノート|
|refs/|参考文献・書誌情報|
|scripts/、tests/|補助処理・必要な検証|
|archive/|検証済み保存パッケージ（データはGit管理外）|
|cache/、tmp/|再生成可能なキャッシュ・一時作業（Git管理外）|

## データ管理

結果に影響する条件をconfig_hash、各試行をrun_idで識別し、既存結果を上書きしません。
計算は研究室サーバー、解析はMac・サーバーの両方に対応します。Driveを正式保存先にし、各端末のデータ展開先や出力先は設定で切り替えます。大量出力は実験・チャンク単位のアーカイブにまとめ、新規はZIPを標準とし、既存のtar等も扱います。
manifestとSHA-256で検証し、Drive保存の検証前に元データを削除しません。
DVC、uv、ジョブ管理ツールは任意です。

## 含まれるもの

フォルダ構成、エージェント指示、管理ガイド、端末別パスの読込処理、実験・解析の設定と索引・記録の雛形です。
パス読込処理はPython 3.10以上・標準ライブラリのみで動作します。
パッケージ作成・検証・選択取得・展開を含みます。実験・解析本体、自動アップロード、認証設定、DVC認証は含みません。

## 自分の研究の情報

- 研究目的:
- DriveフォルダURL:
- コードの所在・版:
- 環境構築:
- 実験索引: docs/experiment-index.csv
- 解析索引: docs/analysis-index.csv
