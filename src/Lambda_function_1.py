import os, json, boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]  # 環境変数で渡す（ハードコードしない）

def lambda_handler(event, context):
    # 受信イベントをログ（デバッグ用）
    print("=== Received Event ===")
    print(json.dumps(event, ensure_ascii=False))

    detail = event.get("detail", {}) or {}

    event_name = detail.get("eventName", "TerminateInstances")
    region     = detail.get("awsRegion") or event.get("region") or "n/a"
    when       = detail.get("eventTime") or event.get("time") or "n/a"
    user_arn   = (detail.get("userIdentity") or {}).get("arn", "n/a")
    src_ip     = detail.get("sourceIPAddress", "n/a")
    ua         = detail.get("userAgent", "n/a")

    # ★ 最小：最初の1件だけ取得（TerminateInstances想定）
    instance_id = (
        detail.get("requestParameters", {})
         .get("instancesSet", {})
         .get("items", [{}])[0]
         .get("instanceId", "n/a")
    )

    # Chatbot の構造化メッセージ（v1.0）
    payload = {
        "version": "1.0",
        "source": "custom",
        "content": {
            "title": "EC2 termination detected",
            "description": (
                f":warning: *{event_name}*\n"
                f"`Instance` : {instance_id}\n"
                f"`By`       : {user_arn}\n"
                f"`Region`   : {region}\n"
                f"`Time`     : {when}\n"
                f"`SrcIP`    : {src_ip}\n"
                f"`UA`       : {ua}"
            )
        }
    }

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="EC2 TerminateInstances (CloudTrail)",
        Message=json.dumps(payload, ensure_ascii=False)
    )
    print("SNS publish response:", response)
    return {"ok": True, "messageId": response.get("MessageId")}
