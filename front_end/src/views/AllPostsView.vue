<script setup>
import PostList from "../components/PostList.vue";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

const { result, loading, error } = useQuery(gql`
  query {
    allPosts {
      title,
      slug,
      author {
        user{
          firstName,
          lastName,
          username,
        }
      }
    }
  }
`)
{
  // error: { message: "No connection to the GraphQL API yet." },
};
</script>

<template>
  <h2>Recent Posts</h2>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error" class="warn">{{ error }}</div>
  <PostList v-else :posts="result.allPosts" />
</template>

<style scoped>
  h2 {
    color: blue;
  }
</style>