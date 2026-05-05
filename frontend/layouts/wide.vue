<template>
  <div class="min-h-screen flex flex-col" style="background:var(--color-bg);color:var(--color-text)">
    <AppNav />
    <main class="flex-1 mx-auto w-full px-4 py-8 max-w-7xl">
      <slot />
    </main>
    <footer class="border-t py-4 text-center text-xs"
            style="border-color:var(--color-border);color:var(--color-text-muted)">
      PAX · AGPL-3.0 · Progrès en Automatismes par les eXercices
    </footer>
  </div>
</template>
