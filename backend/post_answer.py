import json
import uuid

import boto3

# boto3 を使用して DynamoDB テーブルへアクセスします。
dynamodb = boto3.resource("dynamodb")
questions_table = dynamodb.Table("Questions")
quiz_results_table = dynamodb.Table("QuizResults")


def lambda_handler(event, context):
    # body を受け取ります。
    # ユーザー名と答えた問題の情報が入っています。
    body_str = event["body"]
    body = json.loads(body_str)

    username = body["username"]
    questions = body["questions"]

    correct = 0

    # 正答数を数えます。
    for question in questions:
        # DynamoDB テーブルの中の、`question_id` の問題を検索します。
        # これの回答を取得します。
        answer = questions_table.get_item(Key={"question_id": question["question_id"]})[
            "Item"
        ]["answer"]
        # ユーザーの回答と正答が等しい場合に、正答数をインクリメントします。
        if question["answer"] == answer:
            correct += 1

    result = {
        # パーティションキーのために、`quiz_id` を生成します。
        "quiz_id": str(uuid.uuid4()),
        "username": username,
        "correct": correct,
    }

    # ユーザーの結果を DynamoDB テーブルに保存します。
    quiz_results_table.put_item(Item=result)

    # 正答数を返します。
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "correct": correct,
            }
        ),
    }
