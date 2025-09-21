# AWS EC2 Termination Alert

## 日本語

## 概要
このプロジェクトは、EC2インスタンスが削除された際に検知して通知するセキュリティ特化のAWSアーキテクチャです。

## アーキテクチャ
![EC2 Termination Alert Architecture](./images/EC2-termination-architecture.png)


## 処理の流れ
1.EC2 を削除（TerminateInstances を実行）

2.CloudTrailがAPIコール（TerminateInstancesを検知（= 管理イベントを記録）

3.CloudTrailは証跡をS3に保存しつつ、同じ内容をEventBridgeにイベント(JSON)として流す

4.EventBridgeルールがこのイベントにマッチ→Lambdaを起動

5.Lambda がイベント(JSON)から 必要な項目（インスタンスID／実行者ARN／リージョン／時刻 など）を抽出・整形

6.LambdaがSNSにpublish（本文は AWS Chatbot の v1.0 構造化メッセージ）

7.SNS →（HTTPS サブスク）→ AWS Chatbot → Slack に投稿

## セットアップ（最小）
## 実行結果（スクショ）
## セキュリティ配慮（マスク方針・環境変数）
## 今後の拡張（IaC/GuardDuty/複数ID対応 など）

## English
This project is a security-focused AWS architecture to detect and alert when an EC2 instance is terminated.

## Architecture Diagram
![EC2 Termination Alert Architecture](./images/EC2-termination-architecture.png)
