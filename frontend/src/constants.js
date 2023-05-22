export default {
  BACKEND_URL: process.env.BACKEND_URL ? process.env.BACKEND_URL : 'http://localhost:5000/api',
  STATIC_BACKEND_URL: process.env.STATIC_BACKEND_URL ? process.env.STATIC_BACKEND_URL : 'http://localhost:5000',
  CONSULTAS_SUBPATH: process.env.VUE_APP_CONSULTAS_SUBPATH,
  AUTH_URL: '/login',
  ABOUT_URL: '/about',
  AUTH_ACCESS_TOKEN_KEY: 'access_token',
  AUTH_USER_KEY: 'current_user'

}
