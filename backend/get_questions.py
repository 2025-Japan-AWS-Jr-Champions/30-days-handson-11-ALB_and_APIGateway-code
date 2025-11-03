import json

import boto3

# boto3 を使用して DynamoDB テーブルへアクセスします。
dynamodb = boto3.resource("dynamodb")
questions_table = dynamodb.Table("Questions")
quiz_results_table = dynamodb.Table("QuizResults")


def lambda_handler(event, context):
    ## username を受け取ります。
    query_params = event["queryStringParameters"]
    username = query_params.get("username")

    if not username:
        return {"statusCode": 400, "body": json.dumps("Username is required")}

    # テーブル全体をスキャンします。
    # テーブルが大きすぎる場合は、一度で取得しきれません。今回は、十分テーブルが小さいとします。
    # また、テーブル全体のスキャンは計算量が悪いです。本番では工夫して回避するべきです。
    response = questions_table.scan()
    items = response["Items"]

    # 5 問出題するので、問題数がそれに満たない場合はエラーを返します。
    if len(items) < 5:
        return {"statusCode": 500, "body": json.dumps("Not enough questions")}

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": {
                    "questions": [
                        {
                            # answer も返してしまうと、Developer tools などを使用することで答えがわかってしまいます。
                            "question_id": item["question_id"],
                            "image_svg": item["image_svg"],
                            "choices": list(item["choices"]),
                        }
                        for item in items[:5]
                    ],
                    "username": username,
                }
            }
        ),
    }
