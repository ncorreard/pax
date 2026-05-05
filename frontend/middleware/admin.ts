export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()
  if (!auth.isLoggedIn) return navigateTo('/auth/login')
  if (auth.user?.role !== 'admin') return navigateTo('/')
})
