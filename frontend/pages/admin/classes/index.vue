<template>
  <div>
    <div class="flex items-center gap-3 mb-6">
      <NuxtLink to="/admin" class="text-sm hover:underline" style="color:var(--color-text-muted)">
        ← {{ $t('admin.title') }}
      </NuxtLink>
    </div>
    <h1 class="text-2xl font-bold mb-6">{{ $t('admin.classes_title') }}</h1>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-16 rounded-xl animate-pulse"
           style="background:var(--color-surface)"></div>
    </div>

    <div v-else-if="classes.length === 0"
         class="text-center py-16 rounded-xl border text-sm"
         style="background:var(--color-surface);border-color:var(--color-border);color:var(--color-text-muted)">
      {{ $t('classes.empty') }}
    </div>

    <div v-else class="space-y-3">
      <NuxtLink v-for="cls in classes" :key="cls.id" :to="`/classes/${cls.id}`"
                class="flex items-center justify-between rounded-xl border px-5 py-4 hover:shadow-sm transition"
                style="background:var(--color-surface);border-color:var(--color-border)">
        <div>
          <p class="font-semibold">{{ cls.name }}</p>
          <p class="text-xs mt-0.5" style="color:var(--color-text-muted)">
            {{ cls.student_count }} {{ $t('classes.students') }}
          </p>
        </div>
        <span style="color:var(--color-text-muted)">›</span>
      </NuxtLink>
    </div>

    <p v-if="error" class="mt-4 text-sm text-red-500">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['admin'] })

const { apiFetch } = useApi()

interface ClassItem { id: number; name: string; student_count: number }

const classes = ref<ClassItem[]>([])
const loading = ref(true)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    classes.value = await apiFetch<ClassItem[]>('/api/classes/')
  } catch (e: any) {
    error.value = e?.data?.detail || String(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
