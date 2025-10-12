<template>
  <div class="result-container">
    <h2>結果発表</h2>

    <div class="score-box">
      <p>ユーザー名：{{ username }}</p>
      <p>正解数：{{ result?.correct ?? "-" }} / 5</p>
    </div>

    <h3>🏆 ランキング TOP 5</h3>

    <div v-if="loading" class="loading">ランキングを取得中...</div>
    <div v-else-if="rankings.length === 0" class="no-data">
      データがありません。
    </div>
    <table v-else class="ranking-table">
      <thead>
        <tr>
          <th>順位</th>
          <th>ユーザー名</th>
          <th>正解数</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in rankings" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ entry.username }}</td>
          <td>{{ entry.correct }}</td>
        </tr>
      </tbody>
    </table>

    <router-link to="/" class="back-btn">← トップに戻る</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { fetchRanking } from "../api/quiz";
import type { AnswerResponse, RankingEntry } from "../types/quiz";

const route = useRoute();
const username = route.query.username as string;

const result = ref<AnswerResponse | null>(null);
const rankings = ref<RankingEntry[]>([]);
const loading = ref(true);

result.value = {
  correct: Number(route.query.correct ?? 0),
};

onMounted(async () => {
  try {
    const data = await fetchRanking();
    rankings.value = data;
  } catch (err) {
    console.error(err);
    alert("ランキングの取得に失敗しました。");
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.result-container {
  max-width: 600px;
  margin: 2rem auto;
  text-align: center;
}

.score-box {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.ranking-table th,
.ranking-table td {
  border: 1px solid #ccc;
  padding: 0.6rem;
}

th {
  background: #f0f0f0;
}

.no-data {
  color: #888;
  margin-top: 1rem;
}

.back-btn {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  background: #007bff;
  color: white;
  text-decoration: none;
}

.back-btn:hover {
  background: #0056b3;
}
</style>
