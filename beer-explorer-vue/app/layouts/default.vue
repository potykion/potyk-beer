<template>
  <v-app>
    <v-main>
      <slot/>
    </v-main>

    <v-bottom-navigation grow>
      <v-btn  to="/">
        <v-icon>mdi-home</v-icon>

        <span>Мое</span>
      </v-btn>

      <v-btn  to="/prices">
        <v-icon>mdi-cash</v-icon>

        <span>Цены</span>
      </v-btn>


    </v-bottom-navigation>
  </v-app>
</template>
