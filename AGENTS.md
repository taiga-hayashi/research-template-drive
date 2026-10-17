# AGENTS.md

この研究の共通管理ルール。最初にREADME.md、docs/DRIVE_WORKFLOW.md、docs/RESEARCH_LAYOUT.mdを読み、対象実験に必要な仕様だけ参照する。.context/INDEX.mdと.context/core/project.mdを確認し、既存のactive作業記録を引き継ぐ。

- 配置先を決める前にdocs/FOLDER_GUIDE.mdと対象フォルダのREADME.mdを読み、役割と既存の研究固有ルールを確認する。新しいstudy・run・解析・保存先にも目的・入出力・版・検証状態のREADMEを残す。
- 新規研究はsrc/、experiments/、data/runs/、analysis/、docs/、notes/を役割別に分ける。既存コードの共通機能を再利用する。
- 1実験1study。結果に影響する条件をconfig_hashで識別し、一意なrun_idで各試行を保存する。既存結果を上書きしない。
- 入力、設定、seed、実行コード版、コマンド、環境、ログ、必要なcheckpointを記録し、失敗・未完了も残す。
- 計算・結果検証・パッケージ検証・Drive保存・解析を別々に記録する。compute_status=completeだけで研究全体を完了としない。overall_statusはdocs/STATUS_AND_JOBS.mdの基準に従う。
- 公平な比較では問題・入力・seed・初期データ・評価予算等を揃える。差異を記録し、未測定値や結果を捏造しない。
- 図はPNG/PDFを同名・対応する相対パスで保存し、必要な個別パネルも独立描画して保持する。SVG等の追加要件も維持する。
- 計算は研究室サーバー、解析はMacまたはサーバーで行う。Driveを正式保存先とし、Macの同期フォルダも利用する。GitHub・DVC導入は任意。
- 解析コードと研究条件を共通化し、端末の入出力先はconfig/paths.local.jsonで分離する。保存先だけでconfig_hashを変えない。
- 解析ごとに一意なanalysis_idを付け、入力run/package・checksum・集計条件・コード版・コマンド・環境を記録する。同じ解析先をMacとサーバーで上書きしない。
- 実験索引と解析索引に計算状態とDrive保存検証を別々に残す。結果とcheckpointが別保存なら両方の対応を記録する。
- Python実行は各端末のDrive外にある既存のローカル仮想環境を使う。MacはMac側、サーバーはサーバー側の環境を使い、Drive内に.venvを作らない。既存環境を勝手に作り直さず、.venv本体を同期・共有・転送しない。環境の場所が不明なら実行前に確認する。
- .gitignoreはDrive同期を除外しない。仮想環境・キャッシュ・一時ファイル・秘密情報はDrive外に置く。大量の生データ・高頻度checkpointはDrive外で生成し、アーカイブでサーバーからDriveへ直接保存する。既存の直接出力は無断で移動しない。
- Driveを正式保存先とする。実験・チャンク単位のアーカイブ（新規はZIP、既存tar等も可）に元の相対パスを保持し、README・主要指標・代表PDFを外に置く。
- コード・文書の通常同期と、大量の計算出力の転送を区別する。大量出力を小ファイルのまま生成のたびに個別送信しない。長時間計算は原則1時間ごと、またはチャンク完了時に整合性のある途中snapshotを保存する。
- アーカイブにmanifest（相対パス・サイズ・SHA-256、manifest自身は除外）を含め、READMEにアーカイブのSHA-256を記録する。実行時コードを固定し、dirty表示だけで再現可能と判断しない。
- .venv、.git、キャッシュ、一時ファイル、秘密情報、過去archiveは転送対象外。依存定義・生データ・必要ログは保持する。
- 変更のない成果物を再送しない。直接アップロードまたはDrive同期の完了後のクラウド上の存在・サイズ・checksumを検証し、必要なら再取得して照合する。検証前に元データを削除しない。
- ローカルの同期フォルダにあることだけでクラウド保存済みとしない。計算完了・パッケージ検証・Drive保存検証を別々に記録する。
- 外部SSDデータは保存先・版・checksumを記録し、Drive未保存なら明示する。
- 入出力仕様はdocs/experiments-io.md、判断はdocs/decisions.md、作業と考察はnotes/YYYY-MM-DD.mdに残す。
- GitやDVC等は導入済みの環境に従う。DVC・ジョブ管理ツールを前提にしない。外部公開・Git push・認証設定は依頼された範囲に従う。
- 新規実験の公平性・完了条件・測定限界はプロジェクト固有ルールとして追加する。過去プロジェクト固有の数値条件を無条件に流用しない。


- 長時間計算はtemplates/JOB_RECORD.jsonへジョブID・依存・ログ・資源・checkpoint・再開手順を記録する。投入済みを計算結果と扱わない。
- 複数段階の作業は.context/work/active/で実施済み・根拠・固定条件・未確認・次の手順を更新する。AGENTS.mdへ作業履歴を蓄積しない。
- 比較条件と探索/確認/診断の区分はdocs/RESEARCH_PROTOCOL.mdに従う。探索後の確認では条件を固定し、独立性を確認する。
- 図はdocs/FIGURE_POLICY.mdと研究の共通設定に従う。集計単位・不確実性・評価軸・checkpoint位置を記録する。

- サーバーでの保存対象指定と取得・復元はdocs/PACKAGING_AND_FETCH.mdに従う。pack前にdry-runで対象を確認し、凍結snapshotから梱包する。fetchは必要なpackageと信頼できるSHA-256を指定し、既存runへ上書き展開しない。

- 新規フォルダ名はdocs/NAMING.mdに従い1要素24文字以内を基本とする。条件・日時・seed・コード版を名前へ詰め込まず、短いIDと完全hashの対応を記録する。既存フォルダや保存済みIDを自動改名しない。
