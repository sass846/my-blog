import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {
  ApolloClient,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client/core";

const httpLink = createHttpLink({
  uri: "http://localhost:8000/graphql",
});

const cache = new InMemoryCache();

const app = createApp(App)

app.use(router)

app.mount('#app')
