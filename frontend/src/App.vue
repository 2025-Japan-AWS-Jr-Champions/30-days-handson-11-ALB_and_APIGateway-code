<template>
  <div id="app">
    <header>
      <h1>AWS アイコンクイズ</h1>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
#app {
  font-family: "Segoe UI", sans-serif;
  text-align: center;
  margin: 0 auto;
  padding: 2rem;
  max-width: 700px;
}
header {
  background: #232f3e;
  color: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}
</style>
