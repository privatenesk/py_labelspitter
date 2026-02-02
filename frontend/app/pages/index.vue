<script setup lang="ts">
import { ref } from 'vue'

const jobTable = ref()

function onJobCreated() {
  if (jobTable.value) {
    jobTable.value.refresh()
  }
}
</script>

<template>
  <div class="container">
    <h1>Haptic Productivity Jar</h1>
    <div class="content">
      <LabelForm @job-created="onJobCreated" />
      <JobTable ref="jobTable" />
    </div>
  </div>
</template>

<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f9f9f9;
  color: #333;
  margin: 0;
  padding: 20px;
}
.container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 40px;
}
</style>
