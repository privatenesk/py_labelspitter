<script setup lang="ts">
const config = useRuntimeConfig()

// Force client-side fetch to avoid SSR networking issues with localhost
const { data: jobs, refresh } = await useFetch(`${config.public.apiBase}/jobs`, {
    server: false
})

defineExpose({ refresh })
</script>

<template>
  <div class="table-container">
    <div class="header">
      <h3>Job History</h3>
      <button @click="refresh">Refresh</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Time</th>
          <th>Title</th>
          <th>Diff</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in jobs" :key="job.id">
          <td>{{ job.id }}</td>
          <td>{{ new Date(job.created_at).toLocaleString() }}</td>
          <td>{{ job.task_title }}</td>
          <td>{{ job.difficulty }}</td>
          <td :class="job.status.toLowerCase()">{{ job.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  overflow-x: auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.completed { color: green; }
.pending { color: orange; }
.processing { color: blue; }
.failed { color: red; }
</style>
