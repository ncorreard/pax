<template>
  <div>
    <h1 class="text-2xl font-bold mb-8">{{ $t('admin.title') }}</h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <NuxtLink to="/admin/users"
                class="group rounded-xl border p-6 flex flex-col gap-3 hover:shadow-md transition"
                style="background:var(--color-surface);border-color:var(--color-border)">
        <span class="text-4xl">👤</span>
        <div>
          <p class="font-semibold text-base group-hover:underline">{{ $t('admin.users_title') }}</p>
          <p class="text-sm mt-1" style="color:var(--color-text-muted)">{{ $t('admin.users_desc') }}</p>
        </div>
      </NuxtLink>

      <NuxtLink to="/admin/classes"
                class="group rounded-xl border p-6 flex flex-col gap-3 hover:shadow-md transition"
                style="background:var(--color-surface);border-color:var(--color-border)">
        <span class="text-4xl">🏫</span>
        <div>
          <p class="font-semibold text-base group-hover:underline">{{ $t('admin.classes_title') }}</p>
          <p class="text-sm mt-1" style="color:var(--color-text-muted)">{{ $t('admin.classes_desc') }}</p>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['admin'] })
</script>
