<template>
  <div>
    <h2>ユーザーネームを入力してください</h2>
    <input v-model="username" placeholder="例: I love AWS!!" />
    <br /><br />
    <button @click="startQuiz" :disabled="!username">スタート</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const username = ref("");

function startQuiz() {
  router.push({ name: "quiz", query: { username: username.value } });
}
</script>

<style scoped>
input {
  padding: 0.5rem;
  width: 200px;
}
button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
}
</style>
