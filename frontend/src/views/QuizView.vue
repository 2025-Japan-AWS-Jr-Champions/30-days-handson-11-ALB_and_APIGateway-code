<template>
  <div class="quiz-container">
    <h2>クイズ</h2>

    <div v-if="loading" class="loading">問題を読み込み中...</div>

    <div v-else>
      <div
        v-for="question in questions"
        :key="question.question_id"
        class="question-box"
      >
        <div class="question-image" v-html="question.image_svg"></div>
        <div class="choices">
          <button
            v-for="choice in question.choices"
            :key="choice"
            :class="[
              'choice-btn',
              { selected: selectedAnswers[question.question_id] === choice },
            ]"
            @click="selectAnswer(question.question_id, choice)"
          >
            {{ choice }}
          </button>
        </div>
      </div>

      <button class="submit-btn" @click="submitAnswers" :disabled="submitting">
        {{ submitting ? "送信中..." : "提出" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchQuestions, postAnswer } from "../api/quiz";
import type { Question } from "../types/quiz";

const route = useRoute();
const router = useRouter();

const username = route.query.username as string;
const questions = ref<Question[]>([]);
const selectedAnswers = ref<Record<string, string>>({});
const loading = ref(true);
const submitting = ref(false);

// 問題を取得
onMounted(async () => {
  try {
    const data = await fetchQuestions(username);
    questions.value = data.message.questions;
  } catch (err) {
    console.error(err);
    alert("問題の取得に失敗しました。");
  } finally {
    loading.value = false;
  }
});

function selectAnswer(questionId: string, choice: string) {
  selectedAnswers.value[questionId] = choice;
}

async function submitAnswers() {
  submitting.value = true;
  try {
    const payload = {
      username,
      questions: questions.value.map((q) => ({
        question_id: q.question_id,
        answer: selectedAnswers.value[q.question_id],
      })),
    };

    const result = await postAnswer(payload);

    router.push({
      path: "/result",
      query: {
        username,
        correct: result.correct,
      },
    });
  } catch (err) {
    console.error(err);
    alert("回答の送信に失敗しました。");
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.quiz-container {
  max-width: 700px;
  margin: 2rem auto;
  text-align: center;
}

.question-box {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  background: #fafafa;
}

.question-image svg {
  width: 100px;
  height: 100px;
}

.choices {
  margin-top: 1rem;
}

.choice-btn {
  margin: 0.3rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.choice-btn.selected {
  background: #007bff;
  color: white;
}

.submit-btn {
  margin-top: 1.5rem;
  padding: 0.8rem 1.6rem;
  font-size: 1.1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn:hover {
  background: #218838;
}

.loading {
  color: #555;
}
</style>
