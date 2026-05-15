<template>
  <div id="app">
    <header class="navbar">
      <div class="logo">🏥 Egibide Booking</div>
      <nav>
        <router-link to="/">📅 Citas</router-link>
        <router-link to="/clientes">👥 Clientes</router-link>
        <router-link to="/profesionales">👨‍⚕️ Profesionales</router-link>
      </nav>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>
  </div>
</template>

<style>
/* Estilos globales para toda la app */
body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; }

.navbar {
  background-color: #0056b3;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.navbar .logo { font-size: 1.5rem; font-weight: bold; }
.navbar nav { display: flex; gap: 20px; }
.navbar nav a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background 0.3s;
}
.navbar nav a:hover, .navbar nav a.router-link-active {
  background-color: #004494;
}

.main-content { padding: 20px; }
</style>