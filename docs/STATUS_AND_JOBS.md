# 計算・検証・保存・解析の状態とジョブ再開

## 状態を独立して記録する

| 項目 | 状態 | 判定の対象 |
|---|---|---|
| compute_status | pending / queued / running / partial / failed / complete | 指定した計算範囲の実行 |
| validation_status | pending / running / passed / failed / unverified | 件数・軌跡・制約・再現用ファイル等の研究固有の検証 |
| package_validation_status | pending / passed / failed / unverified / not_required | アーカイブと内部manifest |
| storage_status | pending / unverified / verified / failed / not_required | クラウド上の保存検証 |
| analysis_status | pending / queued / running / partial / failed / complete / not_required | 関連する解析の実行。解析出力の検証・保存は解析索引で別管理 |
| overall_status | pending / in_progress / failed / complete | 今回約束した範囲全体の完了 |

ジョブの終了コード0や図の存在だけで研究全体をcompleteにしない。compute_status=completeでもvalidation_status=pendingなら「計算完了・検証待ち」と報告する。実行中に確定した一部結果はpartialとし、対象seed・run・cycleの範囲を記録する。

`templates/RUN_STATUS.json`は手動記録用。expected/completedの件数とverification_evidenceを記入する。未確認の件数・結果を推測で埋めない。not_requiredは対象外の理由をREADMEに書いた場合だけ使う。例えば不要なcheckpointの検証・保存に使用できるが、必要な結果パッケージの検証やDrive保存を省略するためには使わない。

overall_status=completeは、定義した計算範囲が完了し、必要な結果検証・パッケージ検証・Drive保存検証・解析出力の検証がすべて通ってから記録する。解析を含めない計算保存タスクではanalysis_status=not_requiredとして理由を残す。結果とcheckpointが別保存なら、それぞれ必要なパッケージ検証・保存検証も確認する。RUN_STATUS.jsonのpackage_validation_statusとstorage_statusは、対象となる全必須パッケージの状態をまとめて記録し、個別の判定は索引とREADMEへ残す。解析を含むタスクでは解析結果のDrive保存検証も確認する。どこかが失敗していれば成功分を保持し、未完了を明示する。

旧索引にvalidation_status等がない場合はunverifiedとして追加する。compute_status=completeを根拠にpassedへ埋め直さない。既存CSVへ新しいヘッダーだけを上書きせず、列を追加して既存行を保持する。

## 長時間計算のジョブ記録

`templates/JOB_RECORD.json`を作業記録の横にコピーする。ジョブID・スケジューラー名・依存ジョブID・実行場所・作業ディレクトリ・起動コマンド・ログ・必要CPU/GPU/メモリ・実際のPython環境を記録する。pueue等を必須にしない。

計算、検証、梱包・Drive保存、解析の各段階を別ジョブにする場合は、先行段階の成功を確認してから進む。ジョブ投入済みは計算結果ではなくqueuedと報告する。自動の依存ジョブ投入・監視はこの雛形に含まれない。

再開時は次を確認する。

1. 元の条件・コード版・seedとcheckpointのchecksum、保存済みcycleを照合する。
2. 再開コマンド・残り範囲・出力先を確認する。完了済みrunへ上書きしない。
3. 元runを継続する場合は、実装がprefix整合性と重複防止を保証することを確認し、継続記録を追加する。保証できない場合は新runで元runを参照する。
4. 同じrunの二重起動を避け、CPU/GPU・メモリ・使用中ジョブを確認する。seed内の依存を保ち、独立した範囲だけを並列化する。
5. 再開後も必要件数・軌跡長・評価予算を検証し、未完了runと失敗ログを残す。

再開可能なcheckpointがあることと、再開を実地検証したことは区別して記録する。認証情報・トークンをコマンドやログの抜粋に保存しない。
