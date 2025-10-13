import json
from decimal import Decimal

import boto3

# boto3 を使用して DynamoDB テーブルへアクセスします。
dynamodb = boto3.resource("dynamodb")
quiz_results_table = dynamodb.Table("QuizResults")


def decimal_to_int(obj):
    """
    DynamoDB での `number` 型は `Decimal` 型となります。
    これがあると `json.dumps(...)` することができないので、`int` 型へ直します。
    再帰関数となっています。
    """
    if isinstance(obj, list):
        return [decimal_to_int(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_int(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj)
    else:
        return obj


def lambda_handler(event, context):
    # テーブル全体をスキャンします。
    # テーブルが大きすぎる場合は、一度で取得しきれません。今回は、十分テーブルが小さいとします。
    # また、テーブル全体のスキャンは計算量が悪いです。本番では工夫して回避するべきです。
    response = quiz_results_table.scan()
    items = response["Items"]

    if not items:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps([]),
        }

    # items のなかにある `Decimal` 型を全て `int` 型に直します。
    items = decimal_to_int(items)

    # 正答数（correct）でソートします。
    items.sort(key=lambda x: x.get("correct", 0), reverse=True)

    # 上位5件のみを検索します。現在、結果が 5 つ未満である可能性を考えて `min(5, len(items))` としています。
    top_items = items[: min(5, len(items))]

    return {
        "statusCode": 200,
        "body": json.dumps(top_items),
    }
