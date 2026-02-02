<script setup lang="ts">
import { ref } from 'vue'

const config = useRuntimeConfig()
const emit = defineEmits(['job-created'])

const form = ref({
  task_title: '',
  category: '',
  difficulty: 3,
  config: {
    fillers: 'default',
    scaling_factor: 1.0
  }
})

const loading = ref(false)
const error = ref('')

async function submitJob() {
  loading.value = true
  error.value = ''
  try {
    await $fetch(`${config.public.apiBase}/jobs`, {
      method: 'POST',
      body: form.value
    })

    // Reset form
    form.value.task_title = ''
    form.value.category = ''
    form.value.difficulty = 3

    emit('job-created')
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="form-container">
    <h3>Create New Label</h3>
    <form @submit.prevent="submitJob">
      <div class="field">
        <label for="task_title">Task Title:</label>
        <input id="task_title" v-model="form.task_title" required placeholder="e.g. Fix Bug #123" />
      </div>

      <div class="field">
        <label for="category">Category:</label>
        <input id="category" v-model="form.category" required placeholder="e.g. Work" />
      </div>

      <div class="field">
        <label for="difficulty">Difficulty (1-5): {{ form.difficulty }}</label>
        <input id="difficulty" type="range" v-model.number="form.difficulty" min="1" max="5" step="1" />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Printing...' : 'Print Label' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  margin-bottom: 20px;
}
.field {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
input[type="text"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
